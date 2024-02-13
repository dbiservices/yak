# Copyright: (c) 2023, dbi services
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
      yak_ansible_debug:
        description: Debug mode for developers
        required: false
        choices: [True, False]
      yak_ansible_transport_url:
        description: URI to the Graphql endpoint
        required: false
      ssl_verify_certificate:
        description: Instruct the requests to YaK to bypass certificate verification.
        required: false
        choices: [True, False]
'''


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'yak.core.db'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.debug = False
        self.ssl_verify_certificate = True
        self.yak_ansible_transport_url = None
        self.windows_ansible_user = "Ansible"
        self.default_server_os_type = "linux"
        self.prov_grp_name = "providers"
        self.infra_grp_name = "infrastructures"
        self.server_group_name = "servers"
        self.component_group_name = "components"
        self.gql_resultset = None
        self.secret_dir = "/tmp/secrets"
        self.local_ssh_config_file = "{}/.ssh".format(os.path.expanduser('~'))

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('yak.core.db.yml',
                              'yak.core.db.yaml')):
                return True
        self.display.debug(
            ("yak.core.file inventory filename",
             " must end with 'yak.core.db.yml'",
             " or 'yak.core.db.yaml'"))
        return False

    def _log_debug(self, msg):
        if self.debug:
            print("# DEBUG: {}".format(msg))

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
        if self.get_option('yak_ansible_debug') is not None:
            self.debug = self.get_option('yak_ansible_debug')
        if environ.get('YAK_ANSIBLE_DEBUG') is not None and str(environ.get('YAK_ANSIBLE_DEBUG')) in ['true', '1', 'yes']:
            self.debug = True
        self._log_debug("debug: {}".format(self.debug))

        # Derive components absolute path
        self.components_base = os.path.abspath("{}/components".format(os.getcwd()))
        self._log_debug("components_base: {}".format(self.components_base))

        # Checking HTTP Bearer token
        if environ.get('YAK_ANSIBLE_HTTP_TOKEN') is None:
            raise AnsibleError("No YAK_ANSIBLE_HTTP_TOKEN defined.")

        # Checking ssl_verify_certificate
        if self.get_option('ssl_verify_certificate') is not None:
            self.ssl_verify_certificate = self.get_option('ssl_verify_certificate')
        if environ.get('YAK_ANSIBLE_SSL_VERIFY_CERTIFICATE') is not None and \
            str(environ.get('YAK_ANSIBLE_SSL_VERIFY_CERTIFICATE').lower()) in ['false', '0', 'no']:
            self.ssl_verify_certificate = False
        self._log_debug("ssl_verify_certificate: {}".format(self.ssl_verify_certificate))

        # Checking YAK_ANSIBLE_TRANSPORT_URL
        if self.get_option('yak_ansible_transport_url') is not None:
            self.yak_ansible_transport_url = str(self.get_option('yak_ansible_transport_url'))
        if environ.get('YAK_ANSIBLE_TRANSPORT_URL') is not None:
            self.yak_ansible_transport_url = str(environ.get('YAK_ANSIBLE_TRANSPORT_URL'))
        self._log_debug("yak_ansible_transport_url: {}".format(self.yak_ansible_transport_url))

        if self.yak_ansible_transport_url is None:
            raise AnsibleError("No YAK_ANSIBLE_TRANSPORT_URL defined.")

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
            query inventory {
              vSecrets {
                nodes {
                  id
                  name
                  secretValues
                  typeId
                  typeName
                  expirationTs
                }
              }
              vProviders {
                nodes {
                  id
                  isCloudEnvironment
                  name
                  variables
                }
              }
              vInfrastructures {
                nodes {
                  id
                  name
                  providerId
                  providerName
                  secrets
                  variables
                }
              }
              vServers {
                nodes {
                  id
                  infrastructureId
                  infrastructureName
                  ips
                  name
                  providerId
                  providerImageId
                  providerImageName
                  providerImageAnsibleUser
                  providerImageOsType
                  providerImageSpecifications
                  providerName
                  providerShapeId
                  providerShapeName
                  providerShapeSpecifications
                  secrets
                  variables
                }
              }
            }
            """
        if not self.ssl_verify_certificate:
            requests.packages.urllib3.disable_warnings()
        try:
            response = requests.post(
                self.yak_ansible_transport_url,
                verify=self.ssl_verify_certificate,
                headers=self.headers,
                json={'query': query}
            )
        except Exception as e:
            raise AnsibleError("An exception occurred: {}".format(str(e)))

        self._log_debug(response.__dict__)
        if response.status_code != 200:
            raise AnsibleError("Error during GraphQL execution: {}".format(response.__dict__))
        if 'errors' in response.json():
            raise AnsibleError("GraphQL error: {}".format(response.json()["errors"]))

        self.gql_resultset = response.json()["data"]

        self._populate_internal_variables()
        self._populate_secrets()
        self._populate_providers()
        self._populate_infrastructures()
        self._populate_servers()
        # self._populate_group_components()
        # self._populate_component_deployments()

    def _populate_internal_variables(self):
        self._set_gvars('all', 'yak_inventory_type', 'database')
        self._set_gvars('all', 'ansible_winrm_read_timeout_sec', 60)
        self._set_gvars('all', 'ansible_winrm_transport', 'certificate')
        self._set_gvars('all', 'ansible_winrm_server_cert_validation', 'ignore')
        self._set_gvars('all', 'yak_local_ssh_config_file', "{}/config".format(self.local_ssh_config_file))
        os.makedirs(self.local_ssh_config_file, exist_ok=True)

    def _write_secret(self, secret_id, attribute, value):
        os.makedirs("{}/{}".format(self.secret_dir, secret_id), exist_ok=True)
        descriptor = os.open(
            path="{}/{}/{}".format(self.secret_dir, secret_id, attribute),
            flags=(
                os.O_WRONLY   # access mode: write only
                | os.O_CREAT  # create if not exists
                | os.O_TRUNC  # truncate the file to zero
            ),
            mode=0o600
        )
        f = open(descriptor, "w")
        f.write(value)
        f.close()

        if attribute == "PRIVATE_KEY": # Needed by some playbooks
            os.system("/usr/bin/ssh-keygen -f {}/{}/{} -y > {}/{}/PUBLIC_KEY"
                        .format(self.secret_dir, secret_id, attribute, self.secret_dir, secret_id))

    def _populate_secrets(self):

        for secret in self.gql_resultset["vSecrets"]["nodes"]:

            self._log_debug(secret)

            if secret["typeId"] == 5 or secret["typeId"] == 6:  # SSH(5) or WINRM(6)
                for secretValue in secret["secretValues"]:
                    self._write_secret(
                        secret_id=secret["id"],
                        attribute=secretValue["attribute"],
                        value=secretValue["value"]
                    )

            if secret["typeId"] == 4:  # OCI credentials (we need to write the SSK key in a file):
                for secretValue in secret["secretValues"]:
                    if secretValue["attribute"] == "OCI_USER_KEY_FILE":
                        self._write_secret(
                            secret_id=secret["id"],
                            attribute=secretValue["attribute"],
                            value=secretValue["value"]
                        )

    def _populate_providers(self):

        self.inventory.add_group(self.prov_grp_name)
        for provider in self.gql_resultset["vProviders"]["nodes"]:
            self.inventory.add_group(self._fmt_std(provider["name"]))
            self.inventory.add_child(self.prov_grp_name, self._fmt_std(provider["name"].replace("-", "_")))
            self._append_gvars(self._fmt_std(provider["name"].replace("-", "_")), provider["variables"])
            self._set_gvars(self._fmt_std(provider["name"].replace("-", "_")), 'provider', provider["name"].replace("-", "_"))
            self._set_gvars(self._fmt_std(provider["name"].replace("-", "_")), 'is_cloud_environment', provider["isCloudEnvironment"])

    def _populate_infrastructures(self):

        self.inventory.add_group(self.infra_grp_name)
        for infra in self.gql_resultset["vInfrastructures"]["nodes"]:
            infra_name = infra["name"].replace("-", "_")
            self.inventory.add_group(infra_name)
            self.inventory.add_child(self.infra_grp_name, infra_name)
            self.inventory.add_child(infra["providerName"], infra_name)
            self._append_gvars(infra_name, infra["variables"])
            for secret in infra["secrets"]:
                self._log_debug(secret)
                if secret["type_id"] == 5:
                    self._set_gvars(infra_name, "ansible_ssh_private_key_file", "{}/{}/PRIVATE_KEY".format(self.secret_dir, secret["id"]))
                    self._set_gvars(infra_name, "ansible_ssh_public_key_file", "{}/{}/PUBLIC_KEY".format(self.secret_dir, secret["id"]))
                if secret["type_id"] == 6:
                    self._set_gvars(infra_name, "ansible_winrm_cert_key_pem", "{}/{}/WINRM_CERTIFICATE_PRIVATE_KEY".format(self.secret_dir, secret["id"]))
                    self._set_gvars(infra_name, "ansible_winrm_cert_pem", "{}/{}/WINRM_CERTIFICATE".format(self.secret_dir, secret["id"]))

    def _populate_servers(self):

        self.inventory.add_group(self.server_group_name)
        for server in self.gql_resultset["vServers"]["nodes"]:
            server_name = server["name"]
            self.inventory.add_host(server_name, group=self.server_group_name)
            self.inventory.add_host(server_name, group=server["infrastructureName"].replace("-", "_"))
            self._append_hvars(server_name, server["variables"])
            if server["providerImageOsType"].lower() == "windows":
                self._set_hvars(server_name, "ansible_connection", "winrm")
            for secret in server["secrets"]:
                if secret["type_id"] == 5:
                    self._set_hvars(server_name, "ansible_ssh_private_key_file", "{}/{}/PRIVATE_KEY".format(self.secret_dir, secret["id"]))
                    self._set_hvars(server_name, "ansible_ssh_public_key_file", "{}/{}/PUBLIC_KEY".format(self.secret_dir, secret["id"]))
                if secret["type_id"] == 6:
                    self._set_hvars(server_name, "ansible_winrm_cert_key_pem", "{}/{}/WINRM_CERTIFICATE_PRIVATE_KEY".format(self.secret_dir, secret["id"]))
                    self._set_hvars(server_name, "ansible_winrm_cert_pem", "{}/{}/WINRM_CERTIFICATE".format(self.secret_dir, secret["id"]))
            self._set_hvars(server_name, 'storages', [])
            self._set_hvars(server_name, 'target_type', 'server')
            self._set_hvars(server_name, 'machine_name', server["name"])
            if "hostname" not in server:
                self._set_hvars(server_name, 'hostname', server["name"])

            # OS
            self._set_hvars(server_name, 'ansible_user', server["providerImageAnsibleUser"])
            self._set_hvars(server_name, 'os_type', server["providerImageOsType"].lower())
            self._set_hvars(server_name, 'yak_image_name', server["providerImageName"].lower())
            self._set_hvars(server_name, 'yak_shape_name', server["providerShapeName"].lower())
            self._append_hvars(server_name, server["providerImageSpecifications"])
            self._append_hvars(server_name, server["providerShapeSpecifications"])

            # IPs
            self._set_hvars(server_name, 'ansible_host', server["name"])
            for ip in server["ips"]:
                if ip["admin_access"] and ip["ip"] is not None:
                    self._set_hvars(server_name, 'ansible_host', ip["ip"])
                    self._set_hvars(server_name, 'host_ip_access', "{}_ip".format(ip["scope"]))
                ip_mode = ip["mode"]
                if ip["mode"] == "automatic":
                    ip_mode = "auto"
                self._set_hvars(server_name, '{}_ip'.format(ip["scope"]), {})
                self.inventory.hosts[server_name].vars['{}_ip'.format(ip["scope"])]["mode"] = ip_mode
                if ip["ip"]:
                    self.inventory.hosts[server_name].vars['{}_ip'.format(ip["scope"])]["ip"] = ip["ip"]

            if 'public_ip' not in self.inventory.hosts[server_name].vars:
                self.inventory.hosts[server_name].vars['public_ip'] = {}
                self.inventory.hosts[server_name].vars['public_ip']["mode"] = 'none'
            if 'host_ip_access' not in self.inventory.hosts[server_name].vars:
                self._set_hvars(server_name, 'host_ip_access', "private_ip")


    # def _populate_group_components(self):

    #     self.inventory.add_group(self.component_group_name)
    #     for cp in self.gql_resultset["components"]["nodes"]:
    #         self.inventory.add_group(cp["name"])
    #         self.inventory.add_child(self.component_group_name, cp["name"])

    #         if 'templates' in cp["manifest"]:
    #             for template in cp["manifest"]["templates"]:
    #                 template_path = "{}/{}/templates/{}.yml".format(self.components_base, cp["name"], template["path"])
    #                 try:
    #                     template_yaml = yaml.load(open(template_path, 'r'), Loader=yaml.FullLoader)
    #                 except yaml.YAMLError as ex:
    #                     raise AnsibleError(
    #                         "Error reading template '{}': '{}'".format(template_path, ex)
    #                     )

    #                 self._log_debug(template_yaml)
    #                 self._set_gvars(cp["name"], template["name"], template_yaml)

    # def _populate_component_deployments(self):

    #     for cpd in self.gql_resultset["componentDeployments"]["nodes"]:
    #         cpd_name = cpd["name"]
    #         if len(cpd["componentDeploymentsServers"]["nodes"]) == 1:
    #             server = cpd["componentDeploymentsServers"]["nodes"][0]
    #             srv_name = "{}/{}".format(server["server"]["infrastructure"]["name"], server["server"]["name"])
    #             self.inventory.add_host(cpd_name, group=cpd["component"]["name"])
    #             self.inventory.add_host(cpd_name, group=server["server"]["infrastructure"]["name"])
    #             self._append_hvars(cpd_name, self.inventory.hosts[srv_name].vars)
    #             self._append_hvars(cpd_name, cpd["variables"])
    #             self._set_hvars(cpd_name, 'parent_target_name', srv_name)
    #             self._set_hvars(cpd_name, 'target_type', "component")
    #             self._set_hvars(cpd_name, 'component_deployment_uuid', cpd["uuid"])
    #             self._set_hvars(cpd_name, 'component', cpd["component"])
    #             self._set_hvars(cpd_name, 'storage', self.storageTemplatesPerOsTypes[str(cpd["component"]["storageTemplate"]["id"])][str(server["server"]["image"]["operatingSystem"]["operatingSystemType"]["id"])])
    #         if len(cpd["componentDeploymentsServers"]["nodes"]) > 1:
    #             self.inventory.add_group(cpd_name)
    #             self.inventory.add_child(cpd["component"]["name"], cpd_name)
    #             for server in cpd["componentDeploymentsServers"]["nodes"]:
    #                 srv_name = "{}/{}".format(server["server"]["infrastructure"]["name"], server["server"]["name"])
    #                 self.inventory.add_host(srv_name, group=cpd_name)
    #                 self._append_gvars(cpd_name, cpd["variables"])
    #                 self._set_hvars(srv_name, 'is_master', server["isMaster"])
    #                 self._set_gvars(cpd_name, 'component_deployment_uuid', cpd["uuid"])
    #                 self._set_gvars(cpd_name, 'component', cpd["component"])
    #                 # TODO: component storage should be added only once
    #                 self.inventory.hosts[srv_name].vars['storages'].append(self.storageTemplatesPerOsTypes[str(cpd["component"]["storageTemplate"]["id"])][str(server["server"]["image"]["operatingSystem"]["operatingSystemType"]["id"])])
