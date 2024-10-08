#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleError
import os
import requests

def graphQLRequest(graphql_request, graphql_request_variables):
    response = requests.post(
        url=os.environ.get('YAK_ANSIBLE_TRANSPORT_URL'),
        headers={
            "Authorization": "Bearer {}".format(os.environ.get('YAK_ANSIBLE_HTTP_TOKEN')),
            "Content-Type": "application/json",
        },
        json={
            "query": graphql_request,
            "variables": graphql_request_variables,
        },
    )
    if response.status_code != 200:
        raise AnsibleError(f"API error: {response}\n{response.text}")
    if "errors" in response.json():
        raise AnsibleError("GraphQL error: {}\n".format(response.json()["errors"][0]["message"]))
    if graphql_request.lstrip().startswith('query'):
        return response.json()["data"]
