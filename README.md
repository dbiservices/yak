# YaK

YaK Commnunity is your solution to deploy and configure your machines accross the Public Cloud Providers without any provider competency and dependency. 
With YaK you will have a uniq entry point to deploy, configure and manage all your machines for any Cloud provider.
Additional YaK as some products on top with subscription to deploy and manage your Oracle and PostgreSQL Database, more information on http://dbi-services.com/en/yak/components

## Design Principles

  - Source code based on Ansible and Python written in a Collextion yak.yak
  - No need to do any specific Ansible configuration.
  - YaK is fully based on Ansible Community.
  - YaK include it's own ansible inventory model.
       - Cross Cloud Provider
       - Multilevel (Environement/Server/Component)
  - Same command as ansible-playbook ansible-inventory are used.
  - Describe infrastructure for all Cloud Provider together in JSON as Ansible.
  - Manage machines instantly for differents Cloud Provider as AWS,Azure,OCI in parallel.
  - Be the easiest IT Cross Cloud Provider automation system to use, ever.
  - Allow development for additional Cloud Provider or Components

## YaK Demo

   Access our YaK DEMO environment to get a very fast introduction on it , How it works in real life :-) https://......

## Use YaK

Please see [Setup Instructions](setup.md)

## Yak documentation




## Project inventory

This project use a dynamic inventory build from the configuration files available in
`./configuration` directory.

You can have a look on the inventory content using the standard `ansible` command:

```bash
ansible-inventory all --graph
```

More details about the inventory structure can be found in the inventory
[plugin documentation](https://gitlab.com/yak4all/yak/-/tree/main/collections/ansible_collections/yak/core).

## New environment example

To get an example how setup a new environment and servers
[example](https://gitlab.com/yak4all/yak/-/blob/main/configuration/README.md).

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.

