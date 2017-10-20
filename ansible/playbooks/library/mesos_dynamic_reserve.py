#!/usr/bin/python


from ansible.module_utils.basic import *
import requests
import json
import commands

import collections
 

DOCUMENTATION = '''
---
module: mesos_dyanmic_reserve  
short_description: Manage your repos on Github  
'''

EXAMPLES = '''
- name: Create a github Repo
  github_repo:
    github_auth_key: "..."
    name: "Hello-World"
    description: "This is your first repository"
    private: yes
    has_issues: no
    has_wiki: no
    has_downloads: no
  register: result
'''


# try:
#     from types import SimpleNamespace as Namespace
# except ImportError:
#     # Python 2.x fallback
#     from argparse import Namespace



# extract only slaves which have field, hostname
def find_target_host(hostname, nodes):
    for host in nodes:
        if host['type'] == 'agent' and host['hostname'] == hostname:
            return host
    raise Exception('host not found. ' + hostname)


def port_range_to_size(port_range_str):
    range_str = port_range_str[1:-1]
    range_list = range_str.split(',')

    ports_size = 0
    for ports_str in range_list:
        port_range = ports_str.split('-')
        ports_size = ports_size + (int(port_range[1]) - int(port_range[0]))
    return ports_size


def find_range_from_size(port_size, ports):
    range_str = ports[1:-1]
    range_list = range_str.split(',')
    ranges = []
    for port_str in range_list:
        port_range = port_str.split('-')
        low_port, high_port = int(port_range[0]), int(port_range[1])

        if port_size - (high_port - (low_port + 1)) > 0:
            port_size = port_size - (high_port - (low_port + 1))
            ranges.append((low_port + 1, high_port))
        else:
            ranges.append((low_port + 1, (low_port + port_size)))
            break
    return ranges


def split_into_reserve_and_unreserve(resources, existing_role):
    res_op = dict(cpus=0.0, disk=0.0, gpus=0.0, mem=1500.0, ports_num=0)
    unres_op = {}
    for resource_type in resources:
        amount = existing_role.get(resource_type)
        if amount is None:
            continue
        if amount > resources[resource_type]:
            unres_op[resource_type] = amount - resources[resource_type]
        elif amount < resources[resource_type]:
            res_op[resource_type] = resources[resource_type] - amount

    return res_op, unres_op


def check_if_possible_to_reserve(resources, unreserved):
    ranges = []
    for resource_type in resources:
        if resource_type == 'ports_num':
            unreserved_size = port_range_to_size(unreserved.get("ports"))
            if resources[resource_type] > unreserved_size:
                raise Exception('request exceeds unreserved capacity' + resource_type)
            ranges = find_range_from_size(resources['ports_num'], unreserved['ports'])
        elif unreserved.get(resource_type) is None:
            continue
        elif unreserved[resource_type] < resources[resource_type]:
            raise Exception('request exceeds unreserved capacity' + resource_type)
    if ranges:
        resources['ranges'] = ranges
        del resources['ports_num']
    return resources


def to_reqest(op_type, op, host_id, role_def):
    request = collections.OrderedDict()
    request['type'] = op_type.upper()
    request[op_type] = dict(agent_id=dict(value=host_id))
    request[op_type]['resources'] = []

    for resource_type in op:
        res = {}
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
    host = find_target_host(role_def['hostname'], nodes)
    # already is there reserved role?
    existing_role = host['reserved_resources'].get(role_def['name'])

    reserve, unreserve = role_def['resources'], {}
    if existing_role:
        existing_role['ports_num'] = port_range_to_size(existing_role['ports'])
        reserve, unreserve = split_into_reserve_and_unreserve(reserve, existing_role) 

    if reserve:
        check_if_possible_to_reserve(reserve, host['unreserved_resources'])
    
    if unreserve.get('ports_num'):
        unreserve['ranges'] = find_range_from_size(unreserve['ports_num'], host['reserved_resources']['ports'])

    reserve_req = to_reqest('reserve_resources', reserve, host['id'], role_def)
    unreserve_req = to_reqest('unreserve_resources', unreserve, host['id'], role_def)
    return reserve_req, unreserve_req


def send_request(token, mesos_url, req):
    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/json"
    }
    with open('/dcos/abc.json', 'wb') as fp:
        json.dump(req, fp)

    url = "{}{}".format(mesos_url, '/mesos/api/v1')
    # result = requests.post(url, json.dumps(req), headers=headers, verify=False) 
    result={}
    return result


def handle_dynamic_reservation(req):
    #nodes = json.loads(req.nodes_status, object_hook=lambda d: Namespace(**d))
    nodes = req['nodes_status']
    role_def = req['mesos_role']
    token = req['token']
    mesos_url = req['url']

    reserve_req, unreserve_req = convert_role_to_requests(role_def, nodes)

    if not reserve_req and not unreserve_req:
        return False, dict(status=0)

    if reserve_req:
        result1 = send_request(token, mesos_url, reserve_req)
        # if result1.status_code != 202:
        #     raise Exception(result1.json())
    # if unreserve_req:
    #     result2 = send_request(token, mesos_url, unreserve_req)
    #     if result2.status_code != 202:
    #         raise Exception(result2.json())

    # default: something went wrong
    meta = {"status": 202}
    return True, meta


def main():
    # type can str, bool, dict, list,
    fields = dict(
        url=dict(type='str', required=True),
        token=dict(type='str', required=True),
        mesos_role=dict(type='dict', required=True),
        nodes_status=dict(type='list', required=True))

    ret = {}
   # fields is spec , module.params is input, meta is output of module
    module = AnsibleModule(argument_spec=fields)
    try:
        has_chanaged, ret = handle_dynamic_reservation(module.params)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        ret['message'] = e
        module.fail_json(msg=e, **ret)

    module.exit_json(changed=has_chanaged, meta=ret)


if __name__ == '__main__':
    main()
    # script_dir = os.path.dirname(__file__)
    # node_file = open(script_dir + '/node.json', 'r')
    # role_file = open(script_dir + '/role.json', 'r')
    # node_json = node_file.read()
    # role_json = role_file.read()
    # req = {"nodes_status": node_json, "mesos_role": role_json, "token": "12345", "url": "hello"}
    # handle_dynamic_reservation(req)
