# azure_virtualmachine

Create, start, stop, delete a Linux or Windows Azure server on an existing Network Infrastructure.

## Requirements
------------

- Ansible Azure collection must be installed
- AZURE Account and Network parameter must be available

## Variables
---------

This the defaults section

state
- Define the instance state (present, absent, started, stopped)

debug:
- Enable or disable debug mode (true, false)

image_id
- Define the ID of the Amazon Machine Image (AMI) to be used


## Example Playbook

```yaml
- include_role:
    name: yak.core.azure_virtualmachine
  vars:
    state: present
    server_name: "{{ machine_name }}"
    ssh_public_key: "{{ ansible_ssh_public_key_file }}"
    ssh_private_key: "{{ ansible_ssh_private_key_file }}"
    winrm_cert_pem_path: "{{ ansible_winrm_cert_pem }}"
    winrm_user: "{{ ansible_user }}"
    os_admin_username: "{{ ansible_user }}"
```