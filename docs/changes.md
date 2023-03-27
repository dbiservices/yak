# Change log

## Issue #81

- `./components` renamed to `./component_types`
- components move from servers directory to `./components`. A component is no longuer defined per server.
- manifest: variable `subcomponents` rename to `sub_component_types`
- manifest: variable `sub_component_types.servers` rename to `sub_component_types.inventory_map`
- manifest: variable `sub_component_types.inventory_map.name` rename to `sub_component_types.inventory_map.group_name`
- variables: `os_storage` and group_name value defined in the manifest file must have in variables a `yak_manifest_` prefix.
- variables: `os_storages` renamed to  `yak_manifest_os_storages`.
- the `component_type` variable must be fully qualified (including the sub component name). E.g. `component_type: os_storage/storage`

