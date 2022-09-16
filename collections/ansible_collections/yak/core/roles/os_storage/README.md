# os_storage

Role to apply the storage template to the cloud instance.
This role is cloud provider agnostic and will create the cloud devices, map them to the
instance and create the expected FS layout as described in the storage template.

## Requirements

- `vm_name`.
- `volumes` dictionary.
- `filesystems` dictionary.

## Example Playbook

```yaml
- include_role:
    name: yak.core.os_storage
  vars:
    vm_name: "{{ machine_name }}"
    volumes: "{{ storage.volumes }}"
    filesystems: "{{ storage.filesystems }}"
  loop: "{{ storages }}"
  loop_control:
    loop_var: storage
```
