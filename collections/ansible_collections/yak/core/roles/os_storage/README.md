# os_storage

Role to apply the storage template to the cloud instance.
This role is cloud provider agnostic and will create the cloud devices, map them to the
instance and create the expected FS layout as described in the storage template.

## Requirements

### In the inventory (global, infrastructure, server level)

```
storage_devices:
  min_size_gb: 10   # Valid for Linux
  max_size_gb: 100  # Valid for Linux
  specifications:   # Valid for Linux and Windows if applicable
    xxxxxxxxxx: xxxxxxxxxxxxxx
```

### In the component variables

```
os_storage:  # The variable name `os_storage` is expected by YaK core.
    linux:   # FS for Linux
        - { min_size_gb: 36, filesystem_type: "xfs", mount_point: "/u01" }
        - { min_size_gb: 16, filesystem_type: "xfs", mount_point: "/u02" }
        - { min_size_gb:  8, filesystem_type: "xfs", mount_point: "/u03" }
        - { min_size_gb:  8, filesystem_type: "xfs", mount_point: "/u04" }
        - { min_size_gb: 24, filesystem_type: "xfs", mount_point: "/u90" }
    windows:  # Disks for windows
        - { min_size_gb: 5, drive_letter: F, partition_label: data   }
        - { min_size_gb: 5, drive_letter: G, partition_label: backup }
```
