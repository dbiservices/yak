#!/usr/bin/python
# Copyright: (c) 2023, dbi services, distributed without any warranty under the terms of the GNU General Public License v3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleError
from ..module_utils.graphql_utils import graphQLRequest
import os
import requests

__metaclass__ = type

DOCUMENTATION = r'''
---
module: yak_component_state_update

short_description: Modify the YaK component state.

# If this is part of a collection, yo
# u need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    component_state_name:
        description: The state of the component.
        required: true
        type: str
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        component_state_name=dict(type='str', required=True),
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


    if os.environ.get('YAK_INVENTORY_TYPE') is None:
        msg = f"Missing YAK_INVENTORY_TYPE!"
        module.fail_json(msg=msg)

    if str(os.environ.get('YAK_INVENTORY_TYPE').lower()) != "database":
        msg = f"YAK_INVENTORY_TYPE is not database!"
        module.fail_json(msg=msg)
            
    # DB or file based inventory?
    if os.environ.get('YAK_ANSIBLE_HTTP_TOKEN') is None or os.environ.get('YAK_ANSIBLE_TRANSPORT_URL') is None:
        msg = f"Missing YAK_ANSIBLE_HTTP_TOKEN OR YAK_ANSIBLE_TRANSPORT_URL!"
        module.fail_json(msg=msg)

    if os.environ.get('YAK_CORE_COMPONENT') is None:
        msg = f"Missing YAK_CORE_COMPONENT environment variable!"
        module.fail_json(msg=msg)

    api_update_component(os.environ.get('YAK_CORE_COMPONENT'), component_state_name=module.params['component_state_name'])
         
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def api_update_component(component_name: str, basic_variables: dict = None, advanced_variables: dict = None, component_state_name: str=None):
    graphql_request = """
    mutation componentUpdate ($pComponentName: String!, $pBasicVariables: JSON, $pAdvancedVariables: JSON, $pComponentStateName: String! ) {
        componentUpdate(
                input: {pComponentName: $pComponentName, 
                pAdvancedVariables: $pAdvancedVariables,
                pBasicVariables: $pBasicVariables,
                pComponentStateName: $pComponentStateName}
            ) { integer } 
        }
    """
    graphql_request_variables = {"pComponentName": component_name, 
                                 "pBasicVariables": basic_variables, 
                                 "pAdvancedVariables": advanced_variables,
                                 "pComponentStateName": component_state_name}
    graphQLRequest(graphql_request, graphql_request_variables)


def main():
    run_module()

if __name__ == '__main__':
    main()
