# os_storage

Role to apply the minimum requirements (minimal packages, hostname, and server time and timezone) to a server.

## Requirements

- `host_name`.
- `role_time_zone`:
  - default: `Europe/Zurich`.
- `os_type`:
  - default `linux`.

## Example Playbook

```yaml
- include_role:
    name: yak.core.os_prerequisites
  vars:
    host_name: "{{ hostname }}"
```
