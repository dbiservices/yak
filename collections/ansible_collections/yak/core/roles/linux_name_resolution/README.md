Role Name
=========

This role installs a DNS server to resolve given hostnames.
The DNS server used is coredns, see documentation :
https://coredns.io/

The DNS server's dns client is configured to use itself for resolving names.
The DNS server first resolves the dns records configured for it, and then uses the LAN DNS server by default.

This role can be used to setup a DNS server that will be used to resolve a whole infrastructure, or for example to be installed on all the machines so they can resolve the names by using their own DNS server locally. This is useful e.g. for kubernetes component so all machines can know the api server ip address that corresponds to multiple control-plane nodes.

You can call this role from any component easily, see below playbook example.


Requirements
------------

Linux os family must be :
- RedHat
- Debian

Role Variables
--------------
## For etc/hosts

You just need to define the "domain_name" variable if you want to set the domain your hosts will have in /etc/hosts, refer to defaults/main.yml if needed.

## For DNS server 
You need to define dns records to configure as follows :

You can either use raw ip addresses to match the aliases that you want to configure, or use yak-inventory-hostnames, in that case the ip addresses will be evaluated from inventory.

```yaml
dns_records:
  - domain_name: example.com
    aliases: 
      - name: randomdns-test
        ip_addresses:
          - 8.8.8.8 
          - 8.8.4.4
          - 9.9.9.9
      - name: yak-inventory-hostname-test
        yak_inventory_hostnames:
          - rocky8 
          - alma9
```


Dependencies
------------

None

Example Playbook
----------------

```yaml
- name: Ansible Playbook for kubernetes cluster installation 
  hosts: infrastructure
  any_errors_fatal: true
  gather_facts: yes
  strategy: linear
  become: True
  tasks:
    - include_role: 
        name: yak.core.linux_name_resolution
```

Author Information
------------------

Ryan BADAÏ, dbi services
