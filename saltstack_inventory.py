#!/usr/bin/env python
"""
Ansible dynamic inventory script for Saltstack (http://saltstack.com)
"""
import sys
import json

DOCUMENTATION = '''
---
inventory: Saltstack
short_description: SaltStack minion inventory script
description:
  - Generates inventory of SaltStack managed minions
'''

try:
    import salt
    import salt.client
except ImportError as e:
    print("ImportError: ", e.msg)
    sys.exit(1)

data = {'_meta': {'hostvars': {},
                  'all': {'children': ['ungrouped']},
                  'ungrouped': {'hosts': []}}
        }  # data to be returned

local = salt.client.LocalClient()


def get_hosts(minion_id='*'):
    """
    Returns a list of all minions managed by salt master
    """
    roles = local.cmd(minion_id, 'grains.item', ['roles'])
    result = local.cmd(minion_id, 'grains.items')
    for minion in result:
        data['_meta']['hostvars'][minion] = {'ip': [result[minion]['ipv4'][0]]}
    for minion, grains in roles.items():
        if grains['roles']:
            for role in grains['roles']:
                if role not in data:
                    data[role] = {'hosts': []}
                data[role]['hosts'].append(minion)
                if role not in data['_meta']['all']['children']:
                    data['_meta']['all']['children'].append(role)
        else:
            data['_meta']['ungrouped']['hosts'].append(minion)
    return json.dumps(data)


def get_host(minion_id):
    """
    Returns the ipv4 address of a minion
    """
    result = local.cmd(minion_id, 'grains.items')
    data = {'ipv4': result[minion_id]['ipv4'][0]}
    return json.dumps(data)


def main():
    # """
    # generate the salt inventory for ansible
    # includes detailed grain data
    # """
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print(get_hosts())
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        print(get_host(sys.argv[2]))
    else:
        print("Need an argument, either --list or --host <host>")


if __name__ == "__main__":
    main()
