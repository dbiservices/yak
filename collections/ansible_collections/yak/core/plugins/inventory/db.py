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
        self.is_component_specific = False
        self.component_name = None

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

        # Get component name
        if "YAK_CORE_COMPONENT" in os.environ:
            self.is_component_specific = True
            self.component_name = os.environ.get('YAK_CORE_COMPONENT')

        # Populate
        self._populate()

    def _populate(self):

        self._log_debug("Starting to populate...")

        query = """
            query inventory($vComponentsName: String) {
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
                        providerImageVariables
                        providerName
                        providerShapeId
                        providerShapeName
                        providerShapeVariables
                        secrets
                        variables
                        components
                    }
                }
                vComponents(condition: {name: $vComponentsName}) {
                     nodes {
                        id
                        name
                        subcomponentTypeName
                        componentTypeName
                        componentTypeVariables
                        subcomponentTypeVariables
                        componentTypeManifest
                        groups
                        }
                    }

                vArtifactsProviders(condition: {isDefault: true}) {
                    nodes {
                        isDefault
                        providerName
                        variables
                        }
                    }
                }
            """

        query_variables = {}
        if self.is_component_specific:
            query_variables = {
                'vComponentsName': self.component_name
            }

        if not self.ssl_verify_certificate:
            requests.packages.urllib3.disable_warnings()
        try:
            response = requests.post(
                self.yak_ansible_transport_url,
                verify=self.ssl_verify_certificate,
                headers=self.headers,
                json={'query': query, 'variables': query_variables }
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
        if not self.is_component_specific:
            self._populate_providers()
            self._populate_infrastructures()
            self._populate_servers()
        if self.is_component_specific:
            if len(self.gql_resultset["vComponents"]["nodes"]) != 1:
                raise AnsibleError("Component '{}' not accesible! Component exits? Syntax is ok?".format(self.component_name))
            self.component = self.gql_resultset["vComponents"]["nodes"][0]
            self._populate_component()

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
        f.write("{}\n".format(value)) # Ensure new line at the end of the file to avoid key issue
        f.close()

        if attribute == "PRIVATE_KEY": # Needed by some playbooks
            if os.system("/usr/bin/ssh-keygen -f {}/{}/{} -y > {}/{}/PUBLIC_KEY"
                            .format(self.secret_dir, secret_id, attribute, self.secret_dir, secret_id)) != 0:
                raise Exception("Unable to generate public key from private key id '{}'.".format(secret_id))

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
            self.inventory.add_child(infra["providerName"].replace("-", "_"), infra_name)
            if "custom_tags" in infra["variables"]:
                # "Name" tag is not allowed, remove it
                infra["variables"]["custom_tags"].pop("Name", None)
                infra["variables"]["custom_tags"].pop("name", None)
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

            self.inventory.add_host(server["name"], group=self.server_group_name)
            self.inventory.add_host(server["name"], group=server["infrastructureName"].replace("-", "_"))
            self._populate_server(server)

    def _populate_server(self, server):
        self._log_debug("Populating server '{}'".format(server))
        self._set_server_tags_precedence(server)
        server_name = server["name"]

        # First, we add the infrastructure variables (because infra groups are not generated in composant mode)
        for infrastructure in self.gql_resultset["vInfrastructures"]["nodes"]:
            if infrastructure["name"] == server["infrastructureName"]:
                self._append_hvars(server_name, infrastructure["variables"])
                for secret in infrastructure["secrets"]:
                    self._log_debug(secret)
                    if secret["type_id"] == 5:
                        self._set_hvars(server_name, "ansible_ssh_private_key_file", "{}/{}/PRIVATE_KEY".format(self.secret_dir, secret["id"]))
                        self._set_hvars(server_name, "ansible_ssh_public_key_file", "{}/{}/PUBLIC_KEY".format(self.secret_dir, secret["id"]))
                    if secret["type_id"] == 6:
                        self._set_hvars(server_name, "ansible_winrm_cert_key_pem", "{}/{}/WINRM_CERTIFICATE_PRIVATE_KEY".format(self.secret_dir, secret["id"]))
                        self._set_hvars(server_name, "ansible_winrm_cert_pem", "{}/{}/WINRM_CERTIFICATE".format(self.secret_dir, secret["id"]))

        # Then, we process with the server variables
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
        self._set_hvars(server_name, 'target_type', 'server')
        self._set_hvars(server_name, 'machine_name', server["name"])
        if "hostname" not in server:
            self._set_hvars(server_name, 'hostname', server["name"])
        self._set_hvars(server_name, 'provider', server["providerName"])

        # OS
        self._set_hvars(server_name, 'ansible_user', server["providerImageAnsibleUser"])
        self._set_hvars(server_name, 'os_type', server["providerImageOsType"].lower())
        self._set_hvars(server_name, 'yak_image_name', server["providerImageName"].lower())
        self._set_hvars(server_name, 'yak_shape_name', server["providerShapeName"].lower())
        self._append_hvars(server_name, server["providerImageVariables"])
        self._append_hvars(server_name, server["providerShapeVariables"])

        # IPs
        self._set_hvars(server_name, 'ansible_host', server["name"])
        for ip in server["ips"]:
            if ip["admin_access"] and ip["ip"] is not None:
                self._set_hvars(server_name, 'ansible_host', ip["ip"])
            ip_mode = ip["mode"]
            if ip["mode"] == "automatic":
                ip_mode = "auto"
            self._set_hvars(server_name, '{}_ip'.format(ip["scope"]), {})
            self.inventory.hosts[server_name].vars['{}_ip'.format(ip["scope"])]["mode"] = ip_mode
            if ip["ip"]:
                self.inventory.hosts[server_name].vars['{}_ip'.format(ip["scope"])]["ip"] = ip["ip"]
            if ip["admin_access"]:
                self._set_hvars(server_name, 'host_ip_access', "{}_ip".format(ip["scope"]))

        if 'public_ip' not in self.inventory.hosts[server_name].vars:
            self.inventory.hosts[server_name].vars['public_ip'] = {}
            self.inventory.hosts[server_name].vars['public_ip']["mode"] = 'none'
        if 'host_ip_access' not in self.inventory.hosts[server_name].vars:
            raise AnsibleError("No 'admin_access' set to 'true' for any of the allocated IPs on server '{}'".format(server_name))

    def _set_server_tags_precedence(self, server):
        # Server custom tags have priority over infrastructure and "Name" key is forbidden as already used by AWS
        if "custom_tags" in server["variables"]:
            servers_tags = server["variables"]["custom_tags"]
            infrastructure_tags = {}
            if "custom_tags" in self.inventory.groups[server["infrastructureName"].replace("-", "_")].vars:
                infrastructure_tags = self.inventory.groups[server["infrastructureName"].replace("-", "_")].vars["custom_tags"]
            merged_tags = servers_tags | infrastructure_tags
            merged_tags.pop("Name", None)
            merged_tags.pop("name", None)
            server["variables"]["custom_tags"] = merged_tags


    def _populate_component(self):

        self.inventory.groups["all"].vars = {**self.inventory.groups["all"].vars, **self.component["mergedVariables"]}
        self.inventory.groups["all"].vars["component_name"] = self.component["name"]
        self.inventory.groups["all"].vars["component_type_name"] = self.component["componentTypeName"]
        self.component_type_name = self.component["componentTypeName"]
        self.inventory.groups["all"].vars["component_type_sub_name"] = self.component["componentTypeSubname"]
        self.component_type_sub_name = self.component["componentTypeSubname"]
        self.inventory.groups["all"].vars["component_type_manifest"] = self.component["componentTypeManifest"]
        self.component_type_manifest = self.component["componentTypeManifest"]

        # populate sub component type
        if "sub_component_types" not in self.component["componentTypeManifest"]:
            raise AnsibleError("No 'sub_component_types' in the manifest file '{}'.".format(self.component_type_name))

        sub_component = None
        for sub_component_item in self.component["componentTypeManifest"]["sub_component_types"]:
            if sub_component_item["name"] == self.component_type_sub_name:
                sub_component = sub_component_item
                break

        if sub_component is None:
            raise AnsibleError("No sub component name '{}' in the manifest file of component type '{}'.".format(self.component_type_sub_name, self.component_type_name))

        for inventory_map in sub_component["inventory_maps"]:
            self._log_debug("_populate_sub_component_type.sub_component_types.group_name: {}".format(inventory_map["group_name"]))
            if inventory_map["group_name"] in self.inventory.groups:
                raise AnsibleError("Duplicated group name '{}' in inventory_maps of component type'{}'.".format(inventory_map["group_name"], self.component_type_name))
            self.inventory.add_group(inventory_map["group_name"])

            # Add hosts to group
            for component_server in self.component["servers"]:
                self.inventory.add_host(component_server["name"], group=component_server["group_name"])

                for server in self.gql_resultset["vServers"]["nodes"]:
                    if server["name"] == component_server["name"]:
                        self._populate_server(server)

                self._populate_sub_component_type_storage(inventory_map, self.inventory.hosts[component_server["name"]])


    def _populate_sub_component_type_storage(self, inventory_map, target):

        target.vars["yak_inventory_os_storages"] = []
        if "storage" in inventory_map:
            storage_variable_name = "yak_manifest_{}".format(inventory_map["storage"])
            self._log_debug("_populate_sub_component_type.storage_variable_name: {}".format(storage_variable_name))
            if storage_variable_name in self.inventory.groups["all"].vars:
                if target.vars["os_type"] not in self.inventory.groups["all"].vars[storage_variable_name]:
                    raise AnsibleError(
                        "No storage for os type '{}' (server '{}') in the variable of inventory_maps of component type '{}'."
                        .format(target.vars["os_type"], target, self.component_type_name)
                    )
                for storage_point in self.inventory.groups["all"].vars[storage_variable_name][target.vars["os_type"]]:
                    target.vars["yak_inventory_os_storages"].append(
                        {**{"storage_point": storage_point}, **self.inventory.groups["all"].vars[storage_variable_name][target.vars["os_type"]][storage_point]}
                    )
            else:
                raise AnsibleError(
                    "No variables '{}' found in the variables of component '{}'."
                    .format(storage_variable_name, self.component_type_name)
                )
