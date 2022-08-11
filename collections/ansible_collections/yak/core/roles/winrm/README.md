# WinRM

Role to generate WinRM configuration for Ansible.

## Role Variables

- `winrm_cert_pem_path`: path to a valid certificat for WinRM.
- `winrm_user`: The ansible user to which the role must map the certificat.

## Example Playbook

```bash
ansible-playbook ./roles/winrm/tests/test.yml
```
