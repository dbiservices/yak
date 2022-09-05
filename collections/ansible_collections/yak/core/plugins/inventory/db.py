# Copyright: (c) 2022, dbi services
# This file is part of YaK core.
# Yak core is free software distributed without any warranty under the terms of the GNU General Public License v3 as published by the Free Software Foundation, https://www.gnu.org/licenses/gpl-3.0.txt

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.plugins.inventory import Cacheable
from ansible.plugins.inventory import Constructable
import yaml
import requests
requests.packages.urllib3.disable_warnings()
import os.path
from os import environ

# TODO: [WARNING]: Found both group and host with same name: A-test-component-04
# TODO: [WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details

DOCUMENTATION = r'''
    name: yak.core.db
    plugin_type: inventory
    short_description: Returns Ansible inventory from the YaK database backend.
    description: Returns Ansible inventory from the YaK database backend.
    options:
      plugin:
        description: Name of the plugin
        required: true
        choices: ['yak.core.db']
      debug:
        description: Debug mode for developers
        required: false
        choices: [True, False]
      gql_transport_url:
        description: URI to the Graphql endpoint
        required: false
      ssl_verify_certificate:
        description: Instruct the requests to YaK to bypass certificate verification.
        required: false
        choices: [True, False]
      windows_ansible_user:
        description: The user to be create/used for Windows machine
        required: false
      default_server_os_type:
        description: Define the default os_type value when not defined
        required: false
        choices: ["linux", "windows"]
'''


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'yak.core.db'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.debug = False
        self.ssl_verify_certificate = True
        self.windows_ansible_user = "Ansible"
        self.default_server_os_type = "linux"
        self.prov_grp_name = "providers"
        self.infra_grp_name = "infrastructures"
        self.server_group_name = "servers"
        self.component_group_name = "components"

    def verify_file(self, path):
        return True

    def _log_debug(self, msg):
        if self.debug:
            print(msg)

    def _fmt_std(self, name):
        return name.replace("-", "_").replace(" ", "_")

    def _append_gvars(self, group_name, variables):
        self.inventory.groups[group_name].vars.update(variables)

    def _append_hvars(self, host_name, variables):
        if not isinstance(variables, dict):
            raise AnsibleError(
                "Host variables is not a valid JSON. Format detected: '{}'"
                .format(type(variables))
            )

        if len(variables) > 0:
            self.inventory.hosts[host_name].vars.update(variables)

    def _set_gvars(self, group_name, var_name, var_value):
        self.inventory.groups[group_name].vars[var_name] = var_value

    def _set_hvars(self, host_name, var_name, var_value):
        self.inventory.hosts[host_name].vars[var_name] = var_value

    def parse(self, inventory, loader, path, cache=False):

        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        # Checking debug
        if self.get_option('debug') is not None:
            self.debug = self.get_option('debug')
        if environ.get('DEBUG') is not None and str(environ.get('DEBUG')) in ['true', '1', 'yes']:
            self.debug = True
        self._log_debug("## debug: {}".format(self.debug))

        # Derive components absolute path
        self.components_base = os.path.abspath("{}/components".format(os.getcwd()))
        self._log_debug("## components_base: {}".format(self.components_base))

        # Checking HTTP Bearer token
        if environ.get('YAK_ANSIBLE_HTTP_TOKEN') is None:
            raise AnsibleError("No YAK_ANSIBLE_HTTP_TOKEN defined.")

        # Checking ssl_verify_certificate
        if self.get_option('ssl_verify_certificate') is not None:
            self.ssl_verify_certificate = self.get_option('ssl_verify_certificate')
        if environ.get('YAK_SSL_VERIFY_CERTIFICATE') is not None and \
          str(environ.get('YAK_SSL_VERIFY_CERTIFICATE').lower()) in ['false', '0', 'no']:
            self.ssl_verify_certificate = False
        self._log_debug("## ssl_verify_certificate: {}".format(self.debug))

        # Checking GQL_TRANSPORT_URL
        if environ.get('GQL_TRANSPORT_URL') is None:
            self.gql_transport_url = str(self.get_option('gql_transport_url'))
        else:
            self.gql_transport_url = str(environ.get('GQL_TRANSPORT_URL'))

        # Checking windows ansible user
        if self.get_option('windows_ansible_user'):
            self.windows_ansible_user = self.get_option(
                'windows_ansible_user')

        # Checking windows ansible user
        if self.get_option('default_server_os_type'):
            self.default_server_os_type = self.get_option(
                'default_server_os_type')

        # GraphQL Auth
        self.headers = {
            'content-type': "application/json",
            'Authorization': 'Bearer {}'.format(environ.get('YAK_ANSIBLE_HTTP_TOKEN'))
        }

        # Populate
        self._populate()

    def _populate(self):

        self._log_debug("Starting to populate...")

        query = """
query inventoryQuery {
  providers {
    nodes {
      name
      variables
      isCloudEnvironment
    }
  }
  infrastructures {
    nodes {
      name
      variables
      uuid
      provider {
        name
      }
    }
  }
  servers {
    nodes {
      name
      isPhysicalServer
      hostAccessPublicIp
      privateIpMode {
        name
      }
      publicIpMode {
        name
      }
      hasPrivateIp
      hasPublicIp
      privateIp
      publicIp
      serverState {
        name
      }
      uuid
      variables
      infrastructure {
        name
      }
      shape {
        specifications
      }
      image {
        specifications
        operatingSystem {
          name
          version
          operatingSystemType {
            name
          }
        }
        ansibleUser
      }
    }
  }
  storageTemplateOperatingSystemTypes {
    nodes {
      variables
      storageTemplateId
    }
  }
  components {
    nodes {
      id
      name
      manifest
    }
  }
  storageTemplatesPerOsTypes {
    nodes {
      storageTemplatesOsTypes
    }
  }
  componentDeployments {
    nodes {
      uuid
      name
      variables
      component {
        id
        name
        storageTemplate {
          id
          name
        }
      }
      componentDeploymentsServers {
        nodes {
          id
          isMaster
          server {
            name
            infrastructure {
              name
            }
            image {
              operatingSystem {
                operatingSystemType {
                  id
                }
              }
            }
          }
        }
      }
    }
  }
}
            """
        if not self.ssl_verify_certificate:
            requests.packages.urllib3.disable_warnings()
        self.gql_result = requests.post(
            self.gql_transport_url,
            verify=self.ssl_verify_certificate,
            headers=self.headers,
            json={'query': query}
        ).json()["data"]

        self._log_debug(self.gql_result)
        self.storageTemplatesPerOsTypes = self.gql_result["storageTemplatesPerOsTypes"]["nodes"][0]["storageTemplatesOsTypes"]
        self._log_debug(self.storageTemplatesPerOsTypes)

        self._populate_internal_variables()
        self._populate_providers()
        self._populate_infrastructures()
        self._populate_servers()
        self._populate_group_components()
        self._populate_component_deployments()

    def _populate_internal_variables(self):
        self._set_gvars('all', 'yak_inventory_type', 'database')

    def _populate_providers(self):

        # secrets (TODO: find a better way)
        self._set_gvars('all', 'ansible_ssh_private_key_file', "/workspace/yak/configuration/infrastructure/secrets/sshkey")
        self._set_gvars('all', 'ansible_ssh_public_key_file', "/workspace/yak/configuration/infrastructure/secrets/sshkey.pub")
        self._set_gvars('all', 'ansible_winrm_cert_key_pem', "/workspace/yak/configuration/infrastructure/secrets/cert_key.pem")
        self._set_gvars('all', 'ansible_winrm_cert_pem', "/workspace/yak/configuration/infrastructure/secrets/cert.pem")
        self._set_gvars('all', 'ansible_winrm_read_timeout_sec', 60)

        self.inventory.add_group(self.prov_grp_name)
        for provider in self.gql_result["providers"]["nodes"]:
            self.inventory.add_group(self._fmt_std(provider["name"]))
            self.inventory.add_child(self.prov_grp_name, self._fmt_std(provider["name"]))
            self._append_gvars(self._fmt_std(provider["name"]), provider["variables"])
            self._set_gvars(self._fmt_std(provider["name"]), 'provider', provider["name"])
            self._set_gvars(self._fmt_std(provider["name"]), 'is_cloud_environment', provider["isCloudEnvironment"])

    def _populate_infrastructures(self):

        self.inventory.add_group(self.infra_grp_name)

        for infra in self.gql_result["infrastructures"]["nodes"]:
            self.inventory.add_group(infra["name"])
            self.inventory.add_child(self.infra_grp_name, infra["name"])
            self.inventory.add_child(self._fmt_std(infra["provider"]["name"]), infra["name"])
            self._set_gvars(infra["name"], 'infrastructure_uuid', infra["uuid"])
            self._append_gvars(infra["name"], infra["variables"])

    def _populate_servers(self):

        self.inventory.add_group(self.server_group_name)
        for srv in self.gql_result["servers"]["nodes"]:
            srv_name = "{}/{}".format(srv["infrastructure"]["name"],srv["name"])
            self.inventory.add_host(srv_name, group=self.server_group_name)
            self.inventory.add_host(srv_name, group=srv["infrastructure"]["name"])
            self._append_hvars(srv_name, srv["variables"])
            self._append_hvars(srv_name, srv["image"]["specifications"])
            self._append_hvars(srv_name, srv["shape"]["specifications"])
            self._set_hvars(srv_name, 'storages', [])
            self._set_hvars(srv_name, 'target_type', 'server')
            self._set_hvars(srv_name, 'machine_name', srv["name"])
            self._set_hvars(srv_name, 'server_uuid', srv["uuid"])
            self._set_hvars(srv_name, 'is_physical_server', srv["isPhysicalServer"])
            self._set_hvars(srv_name, 'ansible_user', srv["image"]["ansibleUser"])
            self._set_hvars(srv_name, 'os_type', srv["image"]["operatingSystem"]["operatingSystemType"]["name"])
            self._set_hvars(srv_name, 'os_name', srv["image"]["operatingSystem"]["name"])
            self._set_hvars(srv_name, 'os_version', srv["image"]["operatingSystem"]["version"])
            # IPs
            if srv["hostAccessPublicIp"] is False:
                self._set_hvars(srv_name, 'ansible_host', srv["privateIp"])
                self._set_hvars(srv_name, 'host_ip_access', "private_ip")
            else:
                self._set_hvars(srv_name, 'ansible_host', srv["publicIp"])
                self._set_hvars(srv_name, 'host_ip_access', "private_ip")
            self.inventory.hosts[srv_name].vars["private_ip"] = {}
            self.inventory.hosts[srv_name].vars["public_ip"] = {}
            self.inventory.hosts[srv_name].vars["private_ip"]["mode"] = srv["privateIpMode"]["name"]
            self.inventory.hosts[srv_name].vars["public_ip"]["mode"] = srv["publicIpMode"]["name"]
            if srv["privateIpMode"]["name"] in ['manual', 'auto']:
                self.inventory.hosts[srv_name].vars["private_ip"]["ip"] = srv["privateIp"]
            if srv["publicIpMode"]["name"] in ['manual', 'auto']:
                self.inventory.hosts[srv_name].vars["public_ip"]["ip"] = srv["publicIp"]

    def _populate_group_components(self):

        self.inventory.add_group(self.component_group_name)
        for cp in self.gql_result["components"]["nodes"]:
            self.inventory.add_group(cp["name"])
            self.inventory.add_child(self.component_group_name, cp["name"])

            if 'templates' in cp["manifest"]:
                for template in cp["manifest"]["templates"]:
                    template_path = "{}/{}/templates/{}.yml".format(self.components_base, cp["name"], template["path"])
                    try:
                        template_yaml = yaml.load(open(template_path, 'r'), Loader=yaml.FullLoader)
                    except yaml.YAMLError as ex:
                        raise AnsibleError(
                            "Error reading template '{}': '{}'".format(template_path, ex)
                        )

                    self._log_debug(template_yaml)
                    self._set_gvars(cp["name"], template["name"], template_yaml)

    def _populate_component_deployments(self):

        for cpd in self.gql_result["componentDeployments"]["nodes"]:
            cpd_name = cpd["name"]
            if len(cpd["componentDeploymentsServers"]["nodes"]) == 1:
                server = cpd["componentDeploymentsServers"]["nodes"][0]
                srv_name = "{}/{}".format(server["server"]["infrastructure"]["name"], server["server"]["name"])
                self.inventory.add_host(cpd_name, group=cpd["component"]["name"])
                self.inventory.add_host(cpd_name, group=server["server"]["infrastructure"]["name"])
                self._append_hvars(cpd_name, self.inventory.hosts[srv_name].vars)
                self._append_hvars(cpd_name, cpd["variables"])
                self._set_hvars(cpd_name, 'parent_target_name', srv_name)
                self._set_hvars(cpd_name, 'target_type', "component")
                self._set_hvars(cpd_name, 'component_deployment_uuid', cpd["uuid"])
                self._set_hvars(cpd_name, 'component', cpd["component"])
                self._set_hvars(cpd_name, 'storage', self.storageTemplatesPerOsTypes[str(cpd["component"]["storageTemplate"]["id"])][str(server["server"]["image"]["operatingSystem"]["operatingSystemType"]["id"])])
            if len(cpd["componentDeploymentsServers"]["nodes"]) > 1:
                self.inventory.add_group(cpd_name)
                self.inventory.add_child(cpd["component"]["name"], cpd_name)
                for server in cpd["componentDeploymentsServers"]["nodes"]:
                    srv_name = "{}/{}".format(server["server"]["infrastructure"]["name"], server["server"]["name"])
                    self.inventory.add_host(srv_name, group=cpd_name)
                    self._append_gvars(cpd_name, cpd["variables"])
                    self._set_hvars(srv_name, 'is_master', server["isMaster"])
                    self._set_gvars(cpd_name, 'component_deployment_uuid', cpd["uuid"])
                    self._set_gvars(cpd_name, 'component', cpd["component"])
                    # TODO: component storage should be added only once
                    self.inventory.hosts[srv_name].vars['storages'].append(self.storageTemplatesPerOsTypes[str(cpd["component"]["storageTemplate"]["id"])][str(server["server"]["image"]["operatingSystem"]["operatingSystemType"]["id"])])
