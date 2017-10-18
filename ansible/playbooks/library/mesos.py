#!/usr/bin/python


from ansible.module_utils.basic import *
import requests
import json
import commands

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

def portRangeToSize(portsRangeStr):
    range_str = portsRangeStr[1:-1]
    range_list = range_str.split(',')

    ports_size = 0
    for ports_str in range_list:
        port_range = ports_str.split('-')
        ports_size = ports_size + (int(port_range[1]) - int(port_range[0]))
    return ports_size

def findRangeFromSize(portSize, ports):
    
    range_str = ports[1:-1]
    portRangeList = range_str.split(',')
    ranges = []
    for port_str in portRangeList:
        port_range = port_str.split('-')
        low_port, high_port = int(port_range[0]), int(port_range[1])
          
        if portSize - (high_port - low_port) > 0:
            portSize = portSize - (high_port - low_port)
            ranges.append((low_port, high_port))
        else:
            ranges.append( (low_port, (low_port + portSize)) )  
            break
    return ranges

         
def devide_into_Requests(role_def, existing_role):
    reserve_req = dict(cpus=0.0, disk=0.0, gpus=0.0, mem=1500.0, ports_num=0)
    unreserve_req = {}
    for resource_type in role_def:
        resource = existing_role.get(resource_type)
        if resource is None:
            continue
        if resource > role_def[resource_type]:
            unreserve_req[resource_type] = resource - role_def[resource_type]
        elif resource < role_def[resource_type]:
            reserve_req[resource_type] = role_def[resource_type] - resource
        else:
            del role_def['ports']
    
    return reserve_req, unreserve_req


def validate_request(req, unreserved):
    ranges = [] 
    for resource_type in req:
        if resource_type == 'ports_num':
            portsNum = portRangeToSize(unreserved.get("ports"))
            if req[resource_type] > portsNum: 
                raise Exception('no more space')
            ranges = findRangeFromSize(req['ports_num'], unreserved['ports'])
            

        elif unreserved[resource_type] < req[resource_type]:
            raise Exception(resource_type + ' not enough resource')
    if ranges:
        req['ranges'] = ranges
        del req['ports_num']
    return req


def convert_role_to_requests(role_def, nodes):

    host = find_target_host(role_def['hostname'], nodes)

    # already is there reserved role? 
    existing_role = host['reserved_resources'].get(role_def['name'])

    reserve, unreserve = role_def, {}
    if existing_role:
        existing_role['ports_num'] = portRangeToSize(existing_role['ports'])
        reserve, unreserve = devide_into_Requests(role_def, existing_role)
    
    
    unreservedRes = host['unreserved_resources']
    if reserve:
        reserve = validate_request(reserve, unreservedRes)
  
    if unreserve.get('ports_num'):
        unreserve['ranges'] = findRangeFromSize(unreserve['ports_num'], host['reserved_resources']['ports'])

    return reserve, unreserve


def handle_dynamic_reservation(req):
    #nodes = json.loads(req.nodes_status, object_hook=lambda d: Namespace(**d))
    nodes = json.loads(req['nodes_status'])
    role_def = json.loads(req['mesos_role'])['role']
    token = req['token']
    mesos_url = req['url']

    reserveReq, unreserveReq = convert_role_to_requests(role_def, nodes)


    headers = {
        "Authorization": "token {}".format(token),
        "Accept": "application/json"
    }

    url = "{}{}".format(mesos_url, '/mesos/api/v1')
    result = requests.post(url, json.dumps(req['role_def']), headers=headers)


    if result.status_code == 201:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()

    # default: something went wrong
    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta



def main():
    # type can str, bool, dict, list,
    fields = {
        "url": {"required": True, "type": "str"},
        "token": {"required": True, "type": "str"},
        "mesos_role": {"required": True, "type": "str"},
        "nodes_status": {"required": True, "type": "str"}
    }

    ret = {}
   # fields is spec , module.params is input, meta is output of module
    module = AnsibleModule(argument_spec={fields})
    try:
        has_chanaged, whatIsIt, ret = handle_dynamic_reservation(module.params)
    except Exception as e:
        ret['message'] = e
        module.fail_json(msg=e, **ret)

    module.exit_json(changed=has_chanaged, meta=ret.meta)


if __name__ == '__main__':
    main()
    # script_dir = os.path.dirname(__file__)
    # node_file = open(script_dir + '/node.json', 'r')
    # role_file = open(script_dir + '/role.json', 'r')
    # node_json = node_file.read()
    # role_json = role_file.read()
    # req = {"nodes_status": node_json, "mesos_role": role_json, "token": "12345", "url": "hello"}
    # handle_dynamic_reservation(req)
    
