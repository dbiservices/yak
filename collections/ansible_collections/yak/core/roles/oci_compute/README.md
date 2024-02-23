# oci_compute

Create, start, stop, delete a Linux or Windows instance on OCI on an existing Network Infrastructure.

## Requirements

- Ansible OCI collection must be installed
- AZURE Account and Network parameter must be available

## Variables

This the defaults section

state
- Define the instance state (present, absent, started, stopped)

debug:
- Enable or disable debug mode (true, false)

image_id
- Define the ID of the Oracle server image to be used

## Example Playbook

```yaml
- include_role:
    name: yak.core.oci_compute
  vars:
    state: present
    region: "{{ region_id }}"
    display_name: "{{ machine_name }}"
    winrm_cert_pem_path: "{{ ansible_winrm_cert_pem }}"
```
