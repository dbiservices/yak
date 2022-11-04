#!/usr/bin/python
# Copyright: (c) 2022, dbi services, distributed without any warranty under the terms of the GNU General Public License v3

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
    target:
        description: The target to be modify.
        required: true
        type: str
    private_ip:
        description: The private IPof the host defined in target.
        required: false
        type: str
    public_ip:
        description: The public IPof the host defined in target.
        required: false
        type: str
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        target=dict(type='str', required=True),
        private_ip=dict(type='str', required=False),
        public_ip=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
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

    variables_file_path = ''

    for root, dirs, filenames in os.walk('/workspace/yak/configuration/infrastructure'):
        for dir_name in dirs:
            if '{}/{}'.format(root,dir_name).endswith(module.params['target']):
                variables_file_path='{}/{}/variables.yml'.format(root,dir_name)
                break

    try:
        variables_file = open(variables_file_path, 'r')
    except Exception as e:
        raise AnsibleError(
            "Issue while reading variable file '{}' of target '{}': [{}]\n"
            .format(variables_file_path, module.params['target'], e)
        )

    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=4, sequence=4, offset=2)
    try:
        variables_yml = yaml.load(variables_file)
        variables_file.close()
    except Exception as e:
        raise AnsibleError("Issue loading yaml file '{}': [{}]\n".format(variables_file_path,e))

    if module.params['private_ip'] is not None:
        if 'private_ip' in variables_yml:
            variables_yml["private_ip"]["ip"] = module.params['private_ip']
        else:
            variables_yml["private_ip"] = {"mode": "auto", "ip": module.params['private_ip']}
        result['changed'] = True
    if module.params['public_ip'] is not None and len(module.params['public_ip']) > 2:
        if 'public_ip' in variables_yml:
            variables_yml["public_ip"]["ip"] = module.params['public_ip']
        else:
            variables_yml["public_ip"] = {"mode": "auto", "ip": module.params['public_ip']}
        result['changed'] = True

    try:
        variables_file = open(variables_file_path, 'w')
        yaml.dump(variables_yml, variables_file)
        variables_file.close()
    except Exception as e:
        raise AnsibleError("Issue while writing variable file '{}': [{}]\n".format(variables_file_path,e))

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()