# Copyright: (c) 2022, dbi services, distributed without any warranty under the terms of the GNU General Public License v3
from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.plugins.inventory import Cacheable
from ansible.plugins.inventory import Constructable
import yaml
import glob
import os.path
from pathlib import Path
from os import environ
import stat

DOCUMENTATION = r'''
    name: yak.core.file
    plugin_type: inventory
    short_description: Ansible inventory from the YaK configruation
    description: Returns Ansible inventory from the YaK configruation
    options:
      plugin:
        description: Name of the plugin
        required: true
        choices: ['yak.core.file']
      debug:
        description: Debug mode for developers
        required: false
        choices: [True, False]
      configuration_base:
        description: Path to the directory of the configuration directory
        required: false
      configuration_directory_name:
        description: configuration directory name
        required: false
      infrastructure_directory_name:
        description: infrastructure directory name
        required: false
      platform_directory_name:
        description: platform directory name
        required: false
      windows_ansible_user:
        description: The user to be create/used for Windows machine
        required: false
      default_server_os_type:
        description: Define the default os_type value when not defined
        required: false
        choices: ["linux", "windows"]
'''

# This class overload the inital Ansible class
# https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/inventory/__init__.py


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'yak.core.file'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.debug = False
        self.configuration_directory_name = "configuration"
        self.infrastructure_directory_name = "infrastructure"
        self.platform_directory_name = "platforms"
        self.configuration_base = "/opt/{}".format(self.NAME)
        self.configuration_path = \
            "{}/{}".format(self.configuration_base,
                           self.configuration_directory_name)
        self.windows_ansible_user = "Ansible"
        self.default_server_os_type = "linux"
        self.server_group_name = "servers"
        self.allowed_providers = ['aws', 'azure', 'oci', 'on-premises']
        self.secret_permissions = stat.S_IRUSR | stat.S_IWUSR

    # Functions used by Ansible
    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('yak.core.file.yml',
                              'yak.core.file.yaml')):
                return True
        self.display.debug(
            ("yak.core.file inventory filename",
             " must end with 'yak.core.file.yml'",
             " or 'yak.core.file.yaml'"))
        return False

    def _log_debug(self, msg):
        if self.debug:
            print(msg)

    def _log_warning(self, msg):
        print('WARNING: {}'.format(msg))

    def _load_yaml_file(self, file_path, warning_only=False):
        yaml_content = {}
        self._log_debug(
            "Opening yaml file '{}'.".format(file_path)
        )
        try:
            file = open(file_path, 'r')
            self._log_debug(
                "Loading yaml file '{}'.".format(file_path)
            )
            try:
                yaml_content = yaml.load(file, Loader=yaml.FullLoader)
            except yaml.YAMLError as ex:
                if not warning_only:
                    raise AnsibleError(ex)
            file.close()
        except Exception as ex:
            self._log_debug(
                "Missing expected yaml file '{}'."
                .format(file_path)
            )
            if not warning_only:
                raise AnsibleError(ex)
            else:
                self._log_warning(
                    "Missing expected yaml file '{}'."
                    .format(file_path)
                )

        self._log_debug(yaml_content)
        return yaml_content

    def parse(self, inventory, loader, path, cache=False):

        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        # Checking debug
        if self.get_option('debug'):
            if self.get_option('debug') is True:
                self.debug = True
            else:
                raise AnsibleError(
                    "Parameter 'debug' can be True or False only.")
        if environ.get('DEBUG') is not None and int(environ.get('DEBUG')) == 1:
            self.debug = True

        # Checking configuration_directory_name
        if self.get_option('configuration_directory_name'):
            self.configuration_directory_name = self.get_option(
                'configuration_directory_name')
        if environ.get('CONFIGURATION_DIRECTORY_NAME') is not None:
            self.configuration_directory_name = \
                environ.get('CONFIGURATION_DIRECTORY_NAME')

        # Checking infrastructure_directory_name
        if self.get_option('infrastructure_directory_name'):
            self.infrastructure_directory_name = self.get_option(
                'infrastructure_directory_name')

        # Checking platform_directory_name
        if self.get_option('platform_directory_name'):
            self.platform_directory_name = self.get_option(
                'platform_directory_name')

        # Checking configuration_base
        if self.get_option('configuration_base'):
            self.configuration_path = os.path.abspath(
                "{}/{}/{}".format(
                    os.getcwd(),
                    self.get_option('configuration_base'),
                    self.configuration_directory_name)
            )

        if not Path(self.configuration_path).is_dir():
            raise AnsibleError(
                "Is not a valid configuration path '{}'."
                .format(self.configuration_path))

        # Checking windows ansible user
        if self.get_option('windows_ansible_user'):
            self.windows_ansible_user = self.get_option(
                'windows_ansible_user')

        # Checking windows ansible user
        if self.get_option('default_server_os_type'):
            self.default_server_os_type = self.get_option(
                'default_server_os_type')

        # Start populating
        self._populate_infrastructure_global_variables()
        self._populate_infrastructure()

    def _populate_infrastructure_global_variables(self):

        variables_yaml = self._load_yaml_file(
            "{}/{}/variables.yml" .format(
                self.configuration_path,
                self.infrastructure_directory_name
            )
        )

        self.inventory.groups['all'].vars = variables_yaml
        self.inventory.groups['all'].vars['yak_inventory_type'] = 'file'

        self._populate_infrastructure_global_secrets()

    def _populate_infrastructure_global_secrets(self):
        master_secrets = "{}/{}/secrets".format(
            self.configuration_path, self.infrastructure_directory_name)
        self._log_debug(master_secrets)
        if not os.path.exists("{}".format(master_secrets)):
            raise AnsibleError(
                "Missing global secret directory '{}/sshkey'."
                .format(master_secrets))
        self.inventory.groups['all'].vars["ansible_ssh_private_key_file"] = \
            "{}/{}/secrets/sshkey".format(
            self.configuration_path, self.infrastructure_directory_name)
        self.inventory.groups['all'].vars["ansible_ssh_public_key_file"] = \
            "{}/{}/secrets/sshkey.pub".format(
            self.configuration_path, self.infrastructure_directory_name)
        self.inventory.groups['all'].vars["ansible_winrm_cert_pem"] = \
            "{}/{}/secrets/cert.pem".format(
            self.configuration_path, self.infrastructure_directory_name)
        self.inventory.groups['all'].vars["ansible_winrm_cert_key_pem"] = \
            "{}/{}/secrets/cert_key.pem".format(
            self.configuration_path, self.infrastructure_directory_name)
        self.inventory.groups['all'].vars["yak_secrets_directory"] = \
            master_secrets

        os.chmod(self.inventory.groups['all'].vars["ansible_ssh_private_key_file"], self.secret_permissions)
        os.chmod(self.inventory.groups['all'].vars["ansible_winrm_cert_pem"], self.secret_permissions)
        os.chmod(self.inventory.groups['all'].vars["ansible_winrm_cert_key_pem"], self.secret_permissions)

    def _set_auth_secrets(self, target, base_directory):
        self._log_debug(
            "## _set_auth_secrets => testing: {} | {}"
            .format(target, base_directory))
        if os.path.exists("{}/sshkey".format(base_directory)):
            self._log_debug(
                "## _set_auth_secrets => returns: {}/sshkey"
                .format(base_directory))
            target.vars["ansible_ssh_private_key_file"] = \
                "{}/sshkey".format(base_directory)
            os.chmod(target.vars["ansible_ssh_private_key_file"], self.secret_permissions)
            target.vars["ansible_ssh_public_key_file"] = \
                "{}/sshkey.pub".format(base_directory)
            target.vars["yak_secrets_directory"] = base_directory
            if 'os_type' in target.vars:
                if target.vars["os_type"] == "windows":
                    target.vars["ansible_user"] = self.windows_ansible_user
                    target.vars["ansible_connection"] = "winrm"
                    target.vars["ansible_winrm_transport"] = "certificate"
                    target.vars["ansible_winrm_server_cert_validation"] = "ignore"
                    if os.path.exists("{}/cert_key.pem".format(base_directory))  \
                            and os.path.exists("{}/cert.pem".format(base_directory)):
                        target.vars["ansible_winrm_cert_pem"] = \
                            "{}/cert.pem".format(base_directory)
                        os.chmod(target.vars["ansible_winrm_cert_pem"], self.secret_permissions)
                        target.vars["ansible_winrm_cert_key_pem"] = \
                            "{}/cert_key.pem".format(base_directory)
                        os.chmod(target.vars["ansible_winrm_cert_key_pem"], self.secret_permissions)
                        target.vars["yak_secrets_directory"] = base_directory

    def check_and_sanitize_infrastructure_variables(self, config):
        config_sanitized = config
        # Cloud providers
        if "provider" not in config_sanitized:
            raise AnsibleError(
                "No provider found. Choose one of these: '{}'".format(
                    self.allowed_providers)
            )
        config_sanitized["provider"] = config["provider"].lower()
        if config_sanitized["provider"] not in self.allowed_providers:
            raise AnsibleError(
                "Provider '{}' is not in allowed list: '{}'".format(
                    config_sanitized["provider"], self.allowed_providers)
            )
        return config_sanitized

    def _populate_infrastructure(self):

        for infrastructure_file in glob.glob("{}/{}/*/".format(
                self.configuration_path,
                self.infrastructure_directory_name)):
            if os.path.basename(infrastructure_file[:-1]) == 'secrets':
                continue
            group = os.path.basename(infrastructure_file[:-1])
            group = self.inventory.add_group(group)
            self.inventory.add_child('all', group)

            # Add group vars
            group_config_yaml = self._load_yaml_file(
                "{}/{}/{}/variables.yml".format(
                    self.configuration_path,
                    self.infrastructure_directory_name,
                    group
                )
            )

            infrastructure_variables = \
                self.check_and_sanitize_infrastructure_variables(
                    group_config_yaml
                )
            self.inventory.groups[group].vars = infrastructure_variables
            self._set_auth_secrets(
                self.inventory.groups[group],
                "{}/{}/{}/secrets"
                .format(
                    self.configuration_path,
                    self.infrastructure_directory_name,
                    group)
            )
            self.current_provider = \
                self.inventory.groups[group].vars["provider"]

            self._add_hosts(group)

    def _add_hosts(self, group):

        group_server = self.inventory.add_group(self.server_group_name)
        for host_file in glob.glob("{}/{}/{}/*/".format(
                self.configuration_path,
                self.infrastructure_directory_name,
                group)):
            if os.path.basename(host_file[:-1]) == 'secrets':
                continue
            host = "{}/{}".format(group, os.path.basename(host_file[:-1]))
            machine_name = os.path.basename(host_file[:-1])
            self.inventory.add_host(host, group=group)
            self.inventory.add_host(host, group=group_server)

            # Add host vars
            host_config_yaml = self._load_yaml_file(
                "{}/{}/{}/variables.yml".format(
                    self.configuration_path,
                    self.infrastructure_directory_name,
                    host
                )
            )

            if host_config_yaml is not None:
                self.inventory.hosts[host].vars = host_config_yaml

            # Default variable for hosts
            self.inventory.hosts[host].vars["target_type"] = 'server'
            self.inventory.hosts[host].vars["machine_name"] = machine_name
            if 'os_type' not in self.inventory.hosts[host].vars:
                self.inventory.hosts[host].vars["os_type"] = \
                    self.default_server_os_type

            # Add ssh key
            self._set_auth_secrets(
                self.inventory.hosts[host],
                "{}/{}/{}/secrets".format(
                    self.configuration_path,
                    self.infrastructure_directory_name,
                    host)
            )

            # IPs policy
            # ** When host_ip_access doesn't exists, set default to private
            if 'host_ip_access' not in self.inventory.hosts[host].vars:
                self.inventory.hosts[host].vars["host_ip_access"] = 'private_ip'
            # ** When private_ip doesn't exists or is null, set to auto
            if 'private_ip' not in self.inventory.hosts[host].vars or \
                    self.inventory.hosts[host].vars["private_ip"] is None:
                self.inventory.hosts[host].vars["private_ip"] = {
                    "mode": "auto"}
            # ** When public_ip doesn't exists or is null, set to auto
            if 'public_ip' not in self.inventory.hosts[host].vars or  \
                    self.inventory.hosts[host].vars["public_ip"] is None:
                self.inventory.hosts[host].vars["public_ip"] = {
                    "mode": "none"}
            # ** When private_ip and is a string, set manual IP
            if type(self.inventory.hosts[host].vars["private_ip"]) is str:
                self.inventory.hosts[host].vars["private_ip"] = {
                    "mode": "manual",
                    "ip": self.inventory.hosts[host].vars["private_ip"]
                }
            # ** When public_ip and is a string, set manual IP
            if type(self.inventory.hosts[host].vars["public_ip"]) is str:
                self.inventory.hosts[host].vars["public_ip"] = {
                    "mode": "manual",
                    "ip": self.inventory.hosts[host].vars["public_ip"]
                }
            # ** When private_ip.mode doesn't exists, set default
            if 'mode' not in self.inventory.hosts[host].vars["private_ip"]:
                self.inventory.hosts[host].vars["private_ip"]["mode"] = \
                    'auto'
            # ** When public_ip.mode doesn't exists, set default
            if 'mode' not in self.inventory.hosts[host].vars["public_ip"]:
                self.inventory.hosts[host].vars["public_ip"]["mode"] = \
                    'auto'
            # ** When private_ip.mode exists check allowed values
            if self.inventory.hosts[host].vars["private_ip"]["mode"] not in \
                    ['manual', 'auto']:
                raise AnsibleError((
                    "private_ip.mode can be 'manual' or 'auto'."
                    " Current for server '{}' is '{}'")
                    .format(
                        host,
                        self.inventory.hosts[host].vars["private_ip"]["mode"]
                ))
            # ** When public_ip.mode exists check allowed values
            if self.inventory.hosts[host].vars["public_ip"]["mode"] not in \
                    ['none', 'manual', 'auto']:
                raise AnsibleError((
                    "private_ip.mode can be 'none', 'manual' or 'auto'."
                    " Current for server '{}' is '{}'")
                    .format(
                        host,
                        self.inventory.hosts[host].vars["public_ip"]["mode"]
                ))
            # ** Set ansible_host
            if self.inventory.hosts[host].vars['host_ip_access'] == 'public_ip' and \
                    self.inventory.hosts[host].vars["public_ip"]["mode"] == 'none':
                raise AnsibleError((
                    "[{}] 'host_ip_access' is set to 'public_ip' "
                    "but 'public_ip.mode' is set to none."
                ).format(host))
            # ** Set ansible_host
            if 'ip' in self.inventory.hosts[host].vars[
                    self.inventory.hosts[host].vars['host_ip_access']
            ]:
                self.inventory.hosts[host].vars["ansible_host"] = \
                    self.inventory.hosts[host].vars[
                        self.inventory.hosts[host].vars['host_ip_access']
                ]['ip']

            # Initiate list of storage
            self.inventory.hosts[host].vars["storages"] = []

            # Populate components on current host
            self._add_components(group, host)

    def _add_components(self, group, host):

        for component_file in glob.glob("{}/{}/{}/*/".format(
                self.configuration_path,
                self.infrastructure_directory_name,
                host)):
            if os.path.basename(component_file[:-1]) == 'secrets':
                continue
            component = "{}/{}".format(host,
                                       os.path.basename(component_file[:-1]))
            self.inventory.add_host(
                component, group=group)

            # Overwrite with component vars
            component_config_yaml = self._load_yaml_file(
                "{}/{}/{}/variables.yml".format(
                    self.configuration_path,
                    self.infrastructure_directory_name,
                    component
                )
            )

            if component_config_yaml is not None:
                self.inventory.hosts[component].vars = \
                    {**self.inventory.hosts[host].vars,
                        **component_config_yaml}


            # Default variable for components
            self.inventory.hosts[component].vars["parent_target_name"] = host
            self.inventory.hosts[component].vars["target_type"] = 'component'

            # Add ansible key file
            self._set_auth_secrets(
                self.inventory.hosts[component],
                "{}/{}/{}/secrets".format(
                    self.configuration_path,
                    self.infrastructure_directory_name,
                    component)
            )

            # Add to component_type group
            if 'component_type' in self.inventory.hosts[component].vars:
                self.inventory.add_group(
                    self.inventory.hosts[component].vars["component_type"])
                self.inventory.add_host(
                    component,
                    group=self.inventory.hosts[
                        component].vars["component_type"]
                )

            # Add storage
            if 'storage' in component_config_yaml:

                storage_config_yaml = self._load_yaml_file(
                   "{}/templates/{}.yml".format(
                        self.configuration_path,
                        component_config_yaml["storage"]
                    )
                )

                if self.current_provider not in \
                        storage_config_yaml["volumes"]:
                    raise AnsibleError(
                        "Storage volume for provider '{}' not found in '{}'."
                        .format(self.current_provider, storage_config_file))

                # Add template vars to component vars
                self.inventory.hosts[component].vars["storage"] = \
                    storage_config_yaml
                self.inventory.hosts[component].vars["storage"]["volumes"] = \
                    self.inventory.hosts[
                        component
                ].vars["storage"]["volumes"][self.current_provider]

                # Add template var to server
                self.inventory.hosts[host].vars["storages"].append(
                    self.inventory.hosts[component].vars["storage"]
                )

            # Add template
            if 'templates' in component_config_yaml:
                for template in component_config_yaml["templates"]:

                    template_config_yaml = self._load_yaml_file(
                        "components/{}/templates/{}.yml". format(
                            component_config_yaml["component_type"],
                            template["path"]
                        ),
                        warning_only=True
                    )

                    # Add template vars to component vars
                    self.inventory.hosts[component].vars[template["name"]] = \
                        template_config_yaml
