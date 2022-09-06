# yak.core

Documentation for the collection.

- [Inventory plugin](#inventory-plugin)
  - [Enable the inventory](#enable-the-inventory)
  - [Inventory configuration file](#inventory-configuration-file)
  - [View the inventory](#view-the-inventory)
  - [Inventory structure](#inventory-structure)
    - [the infrastructure folder](#the-infrastructure-folder)
    - [the infrastructure_sample folder](#the-infrastructure_sample-folder)
    - [The templates folder](#the-templates-folder)
  - [Debug](#debug)

## Inventory plugin

### Enable the inventory

In the Ansible configuration file `ansible.cfg`:

```ini
[inventory]
enable_plugins = yak.core.file
```

### Inventory configuration file

File `inventory/yak.core.file.yml`:

```yml
plugin: yak.core.file
#
# Custom configuration
#
# configuration_base: the folder in which the
# configuration directory can be found
# Environment variable: none
configuration_base: ./

# configuration_directory_name: the configuration
# directory name
# Environment variable: CONFIGURATION_DIRECTORY_NAME
configuration_directory_name: configuration

# infrastructure_directory_name: the name of the
# infrastructure directory
# Environment variable: none
infrastructure_directory_name: infrastructure

# platform_directory_name: the name of the
# platform directory
# Environment variable: none
platform_directory_name: platforms

# debug: to display debugging information in
# stdout for troubleshooting purpose.
# Environment variable: DEBUG
debug: false

# windows_ansible_user: Default user for windows
# Created a instance creation and used as Ansible user
windows_ansible_user: Ansible

# default_server_os_type: Define the default os_type value when not defined
# choices: ["linux", "windows"]
default_server_os_type: linux
```

### View the inventory

```bash
## All hosts
ansible-inventory --graph --vars

## Per hosts
ansible-inventory --host aws_testing/srv-linux-test-01
```

### Inventory structure

#### the infrastructure folder

In this folder, you can describe your infrastructure. You can have multiple
infrastructures across different cloud and on-premises infrastructures.
The general idea is that one infrastructure is on one cloud provider or on-premises
and serves one purpose. Examples:

- oracle_prod_aws: an infrastructure with Oracle databases for production purposes hosted in AWS.
- weblogic_test_azure: an infrastructure with Weblogic servers for testing purposes hosted in Azure.
- devservers_gcloud: an infrastructure with development servers hosted in the Google cloud.
- etc.

In each infrastructure, you'll have servers (Ansible managed hosts). You can have one or thousands
or even more servers.

In each server, you'll have none or multiple components. These components will be considered as
Ansible managed hosts (and can be targeted as Ansible managed hosts). This extends the concept of managed hosts to things like Oracle instances. That means you can then develop playbooks that will target things like Oracle instance instead of a server and allocate Ansible variables specific to these components without having to build or derive
variables in your playbooks. Components can be:

- Oracle instance
- Weblogic instance
- Apache instance
- Nginx server

```bash
./configuration/infrastructure
├── aws_testing # An infrastructure that will be used as an Ansible group
│   ├── srv-test-01 # A server that will be used as an Ansible host
│   │   ├── oraprd01 # A component (in a server) that will be used as an Ansible host
│   │   │   │        # unless explicitly modified, it will use the same IP as the
│   │   │   │        # parent host.
│   │   │   ├── secrets # Secrets for component oraprd01
│   │   │   │   ├── sshkey
│   │   │   │   └── sshkey.pub
│   │   │   └── variables.yml
│   │   ├── secrets # Secrets for server srvnico-01
│   │   │   ├── sshkey
│   │   │   └── sshkey.pub
│   │   └── variables.yml
└── secrets # Default secrets for all groups, servers and components
    │       # wihtout explicit secrets configured.
    ├── sshkey # RSA SSH key to be used as "ansible_ssh_private_key_file".
    │          # Must be RSA to be compatible cross cloud (at least with AWS).
    └── sshkey.pub
```

##### Secret keys

The `secrets` directories store the secrets file that can be use in playbooks.

- There must be at leat one `secrets` directory at the root of the `customer` folder.
- When a secrets directory exists, the dynamic inventory will try to seach for a private
ssh key called `sshkey`. If it exists, it will set the Ansible variable `ansible_ssh_private_key_file`
to this `sshkey` key for the current group or host. If the `sshkey` key doesn't exists, it will
then allocate the parent `sshkey` key for the current group or host.

You can store all kind of secrets that make sense for you in the `secrets` directories. If
you plan to version this `customer` folder in a production infrastructure, you must ignore all
`secrets` folder from being versioned and you should backup those secrets in a secure way.

#### the infrastructure_sample folder

This is a sample folder that you can see to get more information about
configuration. It aims to be documentation.

#### The templates folder

The `templates` folder is used to save and store pre-defined YaK variables that
describe infrastructures. The goal is to avoid repeting same set of variable in the
`customer` folder. This can be organized with the structure of your choice.
For instance:

```yaml
./configuration/templates/
|-- linux
|   `-- storage
|       |-- oracle_instance.yml
|       `-- postgresql_instance.yml
`-- windows
    `-- storage
        `-- sqlserver_instance.yml
```

### Debug

You can export the variable `DEBUG` to `1` to view the debugging information:

```bash
export DEBUG=1
```
