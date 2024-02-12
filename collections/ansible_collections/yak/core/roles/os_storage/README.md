# yak_inventory_os_storages

Role to apply the storage template to the cloud instance.
This role is cloud provider agnostic and will create the cloud devices, map them to the
instance and create the expected FS layout as described in the storage template.

## Requirements

### In the inventory (global, infrastructure, server level)

```
storage_devices:
  max_size_gb: 100  # Valid for Linux
  specifications:   # Valid for Linux and Windows if applicable
    xxxxxxxxxx: xxxxxxxxxxxxxx
```

### In the component variables

```
yak_manifest_[yak_inventory_os_storages]:  # The variable name from the manifest prefixed by 'yak_manifest_' is expected by YaK core.
    linux:   # FS for Linux
        - { size_gb: 36, filesystem_type: "xfs", mount_point: "/u01" }
        - { size_gb: 16, filesystem_type: "xfs", mount_point: "/u02" }
        - { size_gb:  8, filesystem_type: "xfs", mount_point: "/u03" }
        - { size_gb:  8, filesystem_type: "xfs", mount_point: "/u04" }
        - { size_gb: 24, filesystem_type: "xfs", mount_point: "/u90" }
    windows:  # Disks for windows
        - { size_gb: 5, drive_letter: F, partition_label: data   }
        - { size_gb: 5, drive_letter: G, partition_label: backup }
```
