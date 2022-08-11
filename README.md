This page will give you the Global information of the YaK project

[[_TOC_]]

## How to contribute

Please see [instructions](CONTRIBUTION.md).

## How to build a release

```bash
Not defined Yet
```

## Ansible configuration file

In the ansible.cfg file you will find all default location of the different ansible files (roles, collections, inventory)
```
[defaults]
collections_paths = ./collections:/etc/ansible/collections
roles_path = ./components/oracle_instance/roles:./components/postgresql_instance/roles:./components/sqlserver_instance/roles
inventory = ./inventory/yak.core.file.yml
gathering = smart
callbacks_enabled = profile_tasks

[inventory]
enable_plugins = yak.core.file, yak.core.db
any_unparsed_is_failed = True
```

## Project inventory

This project use a dynamic inventory build from the configuration files available in
`./configuration` directory.

You can have a look on the inventory content using the standard `ansible` command:

```bash
ansible-inventory all --graph
```

More details about the inventory structure can be found in the inventory
[plugin documentation](https://gitlab.com/dbiservices/yak/yak/-/tree/master/collections/ansible_collections/yak/core).

## New environment example

To get an example how setup a new environment and servers
[example](https://gitlab.com/dbiservices/yak/yak/-/blob/master/configuration/README.md).


## Ansible Roles and collections

Ansible Roles and collections are pulled from the projects based on the structure from the YAK group and *ansible* subgroups
[dbi_ansible_roles](https://gitlab.com/dbiservices/yak/yak_ansible_roles).





