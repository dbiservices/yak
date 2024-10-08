#!/usr/bin/python

from __future__ import absolute_import, division, print_function
from ansible.errors import AnsibleError
from ..module_utils.graphql_utils import graphQLRequest
import requests
import os

__metaclass__ = type

DOCUMENTATION = r'''
---
module: yak_component_variables_update
short_description: Update a single YAK component variable
description:
    - This module updates a single component variable in the YAK system using a GraphQL query.
options:
    component_name:
        description: The name of the component to update
        required: true
        type: str
    variable_name:
        description: The name of the variable to update
        required: true
        type: str
    value:
        description: The new value for the variable
        required: true
        type: str
'''

EXAMPLES = r'''
- name: Update component variable
  yak.core.yak_component_variables_update:
    component_name: "postgres1"
    variable_name: "version"
    value: "12"
'''

RETURN = r'''
message:
    description: The output message that the module generates
    type: str
    returned: always
'''
from ansible.module_utils.basic import AnsibleModule

# Define the available arguments/parameters that a user can pass to the module
module_args = dict(
component_name=dict(type='str', required=True),
variable_name=dict(type='str', required=True),
value=dict(type='str', required=True)
)

# Seed the result dict in the object
result = dict(
    changed=False,
    message=''
)

# Create the module object
module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
)


def get_variables_query(component_name):
    graphql_request = """
    query GetComponentVariables($name: String!) {
    vComponents(condition: {name: $name}) {
        edges {
        node {
            basicVariables
            advancedVariables
            id
        }
        }
    }
    }
    """
    
    graphql_request_variables = {"name": component_name} 
    query_result = graphQLRequest(graphql_request, graphql_request_variables)["vComponents"]["edges"][0]["node"]
    basic_variables = query_result.get("basicVariables")
    advanced_variables = query_result.get("advancedVariables")
    return basic_variables, advanced_variables

def update_variables_query(component_name, basic_variables, advanced_variables):
    graphql_request = """
    mutation UpdateComponentVariables($pAdvancedVariables: JSON = "", $pBasicVariables: JSON = "", $pComponentName: String = "") {
        componentUpdate(
            input: {pAdvancedVariables: $pAdvancedVariables, pBasicVariables: $pBasicVariables, pComponentName: $pComponentName}
        ) {
            clientMutationId
            integer
        }
    }
    """
    
    graphql_request_variables = {
        "pComponentName": component_name,
        "pBasicVariables": basic_variables,
        "pAdvancedVariables": advanced_variables
    } 
    query_result = graphQLRequest(graphql_request, graphql_request_variables)
    return query_result

def run_module():
    # If the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # Implement the logic to update the component variables using GraphQL
    try:
        component_name = module.params['component_name']
        variable_name = module.params['variable_name']
        variable_value= module.params['value']

        # Here you would implement the function to update the database using GraphQL
        # For now, we'll just leave it as a placeholder
        def update_component_variable(component_name, variable_name, variable_value):
            # Implement your GraphQL query and database update logic here
            # This is where you'd make the actual changes to the database
            basic_variables, advanced_variables = get_variables_query(component_name)
            
            if variable_name in advanced_variables:
                if advanced_variables.get(variable_name) != variable_value:
                    advanced_variables[variable_name] = variable_value
                    update_variables_query(component_name, basic_variables, advanced_variables)
                    result['changed'] = True
                    result['message'] = f"Variable named {variable_name} properly modified to {variable_value}"
                else:
                    result['message'] = f"Variable named {variable_name} already has the proper value, no changes done."
            elif variable_name in basic_variables:
                if basic_variables.get(variable_name) != variable_value:
                    basic_variables[variable_name] = variable_value
                    update_variables_query(component_name, basic_variables, advanced_variables)
                    result['changed'] = True
                    result['message'] = f"Variable named {variable_name} properly modified to {variable_value}"
                else:
                    result['message'] = f"Variable named {variable_name} already has the proper value, no changes done."
            else:
                msg = f"Variable named {variable_name} doesn't exists !"
                module.fail_json(msg=msg)

        update_component_variable(component_name, variable_name, variable_value)

    except Exception as e:
        module.fail_json(msg=f"Error updating component variables: {str(e)}", **result)

    # In the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()