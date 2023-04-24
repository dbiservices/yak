#!/usr/bin/python
# Copyright: (c) 2023, dbi services, distributed without any warranty under the terms of the GNU General Public License v3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleError
import ruamel.yaml
import os

__metaclass__ = type

DOCUMENTATION = r'''
---
module: yak_inventory_update

short_description: Modify the YaK configuration file parameters.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    server_name:
        description: The name of the server.
        required: false
        type: str
    server_state:
        description: The state of the server.
        required: false
        type: str
    private_ip:
        description: The private IP of the host defined in server_name.
        required: false
        type: str
    public_ip:
        description: The public IP of the host defined in server_name.
        required: false
        type: str
    infrastructure_name:
        description: The name of the server.
        required: false
        type: str
    variables:
        description: Variable to add/update to the infrastructure variables.
        required: false
        type: dict
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_name=dict(type='str', required=False),
        private_ip=dict(type='str', required=False),
        public_ip=dict(type='str', required=False),
        infrastructure_name=dict(type='str', required=False),
        variables=dict(type='dict', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        inventory_type='',
        inventory_file='',
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # DB or file based inventory?
    if os.environ.get('YAK_ANSIBLE_HTTP_TOKEN') is not None and os.environ.get('YAK_ANSIBLE_TRANSPORT_URL') is not None:
        result['inventory_type'] = 'database'

        if module.params['server_name'] is not None:
            # TODO: update server IP + state
            pass

        if module.params['infrastructure_name'] is not None:
            # TODO: update variables
            pass

    else:

        yml = {}

        if module.params['server_name'] is not None:

            yml = load_yml(module.params['server_name'])
            result['inventory_file'] = yml["file_path"]

            if module.params['private_ip'] is not None and len(module.params['private_ip']) > 2:
                if 'private_ip' in yml["variables"]:
                    yml["variables"]["private_ip"]["ip"] = module.params['private_ip']
                else:
                    yml["variables"]["private_ip"] = {"mode": "auto", "ip": module.params['private_ip']}
                result['changed'] = True
            if module.params['public_ip'] is not None and len(module.params['public_ip']) > 2:
                if 'public_ip' in yml["variables"]:
                    yml["variables"]["public_ip"]["ip"] = module.params['public_ip']
                else:
                    yml["variables"]["public_ip"] = {"mode": "auto", "ip": module.params['public_ip']}
                result['changed'] = True

        if module.params['infrastructure_name'] is not None:

            yml = load_yml(module.params['infrastructure_name'])
            result['inventory_file'] = yml["file_path"]

            if module.params['variables'] is not None:
                for variable in module.params['variables']:
                    yml["variables"][variable] = module.params['variables'][variable]
                    result['changed'] = True

        if result['changed'] is True:
            save_variables(yml)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def load_yml(target_name):

    variables_file_path = ''
    for root, dirs, filenames in os.walk('/workspace/yak/configuration/infrastructure'):
        for dir_name in dirs:
            if '{}/{}'.format(root, dir_name).endswith(target_name):
                variables_file_path = '{}/{}/variables.yml'.format(root, dir_name)
                break

    try:
        variables_file = open(variables_file_path, 'r')
    except Exception as e:
        raise AnsibleError(
            "Issue while reading variable file '{}' of target '{}': [{}]\n"
            .format(variables_file_path, target_name, e)
        )

    yaml = ruamel.yaml.YAML()
    try:
        variables_yml = yaml.load(variables_file)
        variables_file.close()
    except Exception as e:
        raise AnsibleError("Issue loading yaml file '{}': [{}]\n".format(variables_file_path, e))

    return {"file_path": variables_file_path, "variables": variables_yml}

def save_variables(yml):
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=4, sequence=4, offset=2)
    try:
        variables_file = open(yml["file_path"], 'w')
        yaml.dump(yml["variables"], variables_file)
        variables_file.close()
    except Exception as e:
        raise AnsibleError("Issue while writing variable file: {}\n".format(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
