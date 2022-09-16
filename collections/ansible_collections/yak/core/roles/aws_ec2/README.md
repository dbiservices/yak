# aws_ec2

Create, start, stop, delete a Linux or Windows AWS EC2 instance on an existing Network Infrastructure.

## Requirements

- Ansible Amazon.ec2 module must be installed.
- AWS Account and Network parameter must be available.

## Variables

state:
- Define the instance state (present, absent, started, stopped)

debug:
- Enable or disable debug mode (true, false)

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- include_role:
    name: yak.core.aws_ec2
  vars:
    state: present
    server_name: "{{ machine_name }}"
    ec2_key_name: "{{ machine_name }}"
    image_id: "{{ ami_id }}"
    local_ssh_key:
        path: "{{ ansible_ssh_private_key_file|dirname }}"
        private_key_name: "{{ ansible_ssh_private_key_file|basename }}"
        public_key_name: "{{ ansible_ssh_public_key_file|basename }}"
    volumes_params: "{{ ec2_volumes_params }}"
    winrm_cert_pem_path: "{{ ansible_winrm_cert_pem }}"
    winrm_user: "{{ ansible_user }}"
    os_admin_username: "{{ ansible_user }}"
```
