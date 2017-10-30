#!/usr/bin/python

import collections
import sys
import traceback
import requests
import json
import commands
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: mesos_dyanmic_reserve  

short_description: mesos dynamic reservation for both reserve/unreserve operation
rule of dynamic reservation

version_added: "2.3"

description: with givien parameters, 
this module figures out reserve part and unreserve part and requests both operation respectfully
operation:
  description:
    - reserve: even if you only reserve parts of all resources, all params in json format are required with value of 0
    - unreserve: provide only unreseved params of the resources 
  role definition 
    resources:
      cpus: 1.0
      mem: 1500
      gpus: 2.0
      disk: 1000 
      ports_num: 3000

options:
    url: 
        description: 
          - Adminrouter url of DC/OS 
    token:
        description
          - DC/OS request token 

    mesos_role: 
        description:
          - role_definition check out below.

    nodes_status: 
        description: 
          - result of command, "dcos node --json" 

author: 
    - jonggun kim
'''

EXAMPLES = '''
- name: Create Dynamic reserve requests
  mesos_dynamic_reserve:
    url: http://dcos_cluster_url
    token: dcos_token
    mesos_role: role_definition
    nodes_status: result_of_command_dcos_node_json
  register: body_json

- name: Do operation
  uri:
    url: "http://dcos_cluster_url/mesos/api/v1"
    method: POST
    validate_certs: False
    headers: 
      Authorization: "token=dcos_token"
      Accept: "application/json" 
    body_format: json
    body: "{{ item }}"
    status_code: 202, 409
  with_items: "{{body_json.state}}"

'''

RETURN = '''
state:
    description: body of mesos dynamic reservation in list
    type: list
'''




# try:
#     from types import SimpleNamespace as Namespace
# except ImportError:
#     # Python 2.x fallback
#     from argparse import Namespace



# extract only slaves which have field, hostname
def find_target_host(hostname, nodes):
    '''
    find target from result of command 'dcos node --json'
    '''

    for host in nodes:
        if host['type'] == 'agent' and host['hostname'] == hostname:
            return host
    raise Exception('host not found. ' + hostname)


def port_range_to_size(port_range_str):
    '''
    return size of port ranges
    '''

    range_str = port_range_str[1:-1]
    range_list = range_str.split(',')

    ports_size = 0
    for ports_str in range_list:
        port_range = ports_str.split('-')
        ports_size = ports_size + (int(port_range[1]) - int(port_range[0]))

    return ports_size


def find_range_from_size(port_size, ports):
    '''
    return part of given port ranges as the given size
    '''

    range_str = ports[1:-1]
    range_list = range_str.split(',')
    ranges = []
    for port_str in range_list:
        port_range = port_str.split('-')
        low_port, high_port = int(port_range[0]), int(port_range[1])

        if port_size - (high_port - low_port) > 0:
            port_size = port_size - (high_port - low_port)
            ranges.append((low_port, high_port))
        else:
            ranges.append((low_port, (low_port + port_size)))
            break

    return ranges


def split_into_reserve_and_unreserve(new_role, existing_role):
    '''
    convert ansible parameters to reserve, unreserve operations
    '''

    res_op = dict(cpus=0.0, disk=0.0, gpus=0.0, mem=0.0, ports_num=0)
    unres_op = {}
    for resource_type in new_role:
        amount = existing_role.get(resource_type)
        # it means this type of resource is not reserved in the existing role before 
        if amount is None:
            res_op[resource_type] = new_role[resource_type]
        elif amount < new_role[resource_type]:
            res_op[resource_type] = new_role[resource_type] - amount
        elif amount > new_role[resource_type]:
            unres_op[resource_type] = amount - new_role[resource_type]

    return (res_op if not all(value == 0 for value in res_op.values()) else None) , (unres_op if unres_op else None) 


def check_if_possible_to_reserve(reserve_op, available_res):
    '''
    verify if given reserve operation is valid by comparing with unreserved resrouces of cluster
    '''

    for resource_type in reserve_op:
        if resource_type == 'ports_num':
            unreserved_size = port_range_to_size(available_res['ports'])
            if reserve_op[resource_type] > unreserved_size:
                raise Exception('request exceeds unreserved capacity' + resource_type)
            ranges = find_range_from_size(reserve_op['ports_num'], available_res['ports'])
        elif available_res.get(resource_type) is None:
            raise Exception('{} is not available'.format(resource_type))
        elif available_res[resource_type] < reserve_op[resource_type]:
            raise Exception('{} is not enough to reserve '.format(resource_type))
    if ranges:
        reserve_op['ranges'] = ranges
        del reserve_op['ports_num']
    return reserve_op


def to_reqest(op_type, op, host_id, role_def):
    '''
    append mesos resource reservation part to requested resource
    '''

    request = collections.OrderedDict()
    request['type'] = op_type.upper()
    request[op_type] = dict(agent_id=dict(value=host_id))
    request[op_type]['resources'] = []

    for resource_type in op:
        res = collections.OrderedDict()
        is_scala = True if resource_type != 'ranges' else False
        res['type'] = "SCALAR" if is_scala else "RANGES"
        res['name'] = resource_type if  is_scala else 'ports'
        res['reservation'] = dict(principal=role_def['principal'])
        res['role'] = role_def['name']

        if is_scala:
            res['scalar'] = dict(value=op[resource_type])
        else:
            res['ranges'] = dict(range=[])
            for pair in op['ranges']:
                res['ranges']['range'].append(dict(begin=pair[0], end=pair[1]))

        request[op_type]['resources'].append(res)
    return request


def convert_role_to_requests(role_def, nodes):
    ''' 
    convert ansible params to mesos reserve/unreserve operations by comparing with values of exisiting role 
    with given values, operations can be just reserve, or unreserve op, both 
    '''

    host = find_target_host(role_def['hostname'], nodes)
    # already is there reserved role?
    existing_role = host['reserved_resources'].get(role_def['name'])

    if existing_role:
        existing_role['ports_num'] = port_range_to_size(existing_role['ports']) if 'ports' in existing_role else 0
        reserve_op, unreserve_op = split_into_reserve_and_unreserve(role_def['resources'], existing_role) 
    else:
        reserve_op, unreserve_op = role_def['resources'], None
    
    reserve_req = unreserve_req = None
    if reserve_op:
        check_if_possible_to_reserve(reserve_op, host['unreserved_resources'])
        reserve_req = to_reqest('reserve_resources', reserve_op, host['id'], role_def)
    
    if unreserve_op:
        if 'ports_num' in unreserve_op:
            unreserve_op['ranges'] = find_range_from_size(unreserve_op['ports_num'], existing_role['ports'])
            del unreserve_op['ports_num']
        unreserve_req = to_reqest('unreserve_resources', unreserve_op, host['id'], role_def)

    return reserve_req, unreserve_req


def send_request(token, mesos_url, payload):
    headers = {
        "Authorization": "token={}".format(token),
        "Accept": "application/json"
    }
  
    url = "{}{}".format(mesos_url, '/mesos/api/v1')
    result = requests.post(url, json=payload, headers=headers, verify=False) 
    # print('status code: {}'.format(result.status_code))
    #return result
    return 202


def handle_dynamic_reservation(req):
    ''' The highest level method of mesos dynamic reservation 
    this method defines general step of dynamic reservation for both reserve/unreserve operation
    the steps below 
    1) Get params from ansible parameters 
    2) convert params to reservve/unreserve operations. 
        if param 's value  is hight then exisiting value, the param will be part of reserve OP
        if param 's value is lower then existiing value, the param will be part of unreserve op
        as a result, some params are higher and some params are lower than existing. both operations are created
    3) verify the created operations by comparing it with unreserved resources of the mesos cluster 
    4) return the operations in list object with name, state 
    '''

    nodes = req['nodes_status']
    role_def = req['mesos_role']
    token = req['token']
    mesos_url = req['url']

    reserve_req, unreserve_req = convert_role_to_requests(role_def, nodes)

    payloads = []
    if reserve_req:
        payloads.append(reserve_req)
    if unreserve_req: 
        payloads.append(unreserve_req)
    
    if not payloads:
        result = dict(changed=False, message='status')
    else:
        result = dict(changed=True, original_message='status 202', state=payloads, message='')
    
    return result


def main():
    # type can str, bool, dict, list,
    fields = dict(
        url=dict(type='str', required=True),
        token=dict(type='str', required=True),
        mesos_role=dict(type='dict', required=True),
        nodes_status=dict(type='list', required=True))

   # fields is spec , module.params is input, meta is output of module
    module = AnsibleModule(argument_spec=fields)
    try:
        ret = handle_dynamic_reservation(module.params)
        module.exit_json(**ret)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        module.fail_json(msg=e)



if __name__ == '__main__':
    main()
