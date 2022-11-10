# Artifacts

Copy any files from an artifact provider (AWS S3, Azure Storage Blob, OCI object storage, etc)
into an instance at the specified location.

The role copies artifacts from the artifact provider to the destination instance (no intermediaries).

The role will preserve the target server's artifact path (directory structure). For instance, if you want `rdbms/oracle/dmk/dmk_dbbackup-21-02.zip` in `/tmp`, it will be copied like this: `/tmp/rdbms/oracle/dmk/dmk_dbbackup-21-02.zip`. Same behavior for all providers on Linux and Windows.

## Prerequisites

- The artifact structures and files must exist in the artifact provider.
- You must have correct credentials and permissions to access artifacts.
- Per artifact provider requisites:
  - `aws_s3`: a bucket named 'yak' and the AWS secret keys in environment variables.
  - `azure_storage_blob`: a Blob SAS token in the environement variable `AZURE_AZCOPY_BLOB_SAS_TOKEN` with at least read permissions (can be generated in the GUI, check the Azure documentation for more information about SAS token).
  - `oci_object_storage`: a bucket named 'yak' and the OCI secret keys in environment variables.
  - `yak_local_storage`: A local directory in the container with the artifacts. This would most likely be a mount point from the host. The default is `/yak_local_storage,` but you can change the default by changing the environment variable `YAK_LOCAL_STORAGE_PATH` (example: `export YAK_LOCAL_STORAGE_PATH=/yak_local_storage`).

### From configuration

The configuration dictionary variable can be stored in the global `variables.yml` file, in an infrastructure `variables.yml` file, or for each server in the server's `variables.yml` file.

- `artifacts`
  - `provider`: the supported provider of your artifacts:
    - `aws_s3`
    - `azure_storage_blob`
    - `oci_object_storage`
    - `yak_local_storage`
  - `variables`: dictionary of variables specific to an artifact provider.
    - `aws_s3`:
      - `bucket_name`
    - `azure_storage_blob`:
      - `storage_account_name`
      - `container`
    - `oci_object_storage`:
      - `namespace_name`
      - `bucket_name`
    - `yak_local_storage`: none

#### Example aws_s3

```yaml
artifacts:
  provider: aws_s3
  variables:
    bucket_name: yak-artifacts
```

#### Example azure_storageblob

```yml
artifacts:
  provider: azure_storageblob
  variables:
    storage_account_name: yakartifacts
    container: yakartifacts
```

#### Example azure_storageblob

```yml
artifacts:
  provider: oci_object_storage
  variables:
    namespace_name: zrbhy7g7atj1
    bucket_name: dbi-services-yak-artifacts
```

#### Example yak_local_storage

```yml
artifacts:
  provider: azure_storageblob
  variables:
    provider: yak_local_storage
```
### From components

- `artifact_files`: a list of the artifact name relative to the bucket name (without the bucket name).
- `destination_path`: the directory into which to copy the artifact.
- `destination_owner`: the owner of the artifact at destination.
- `destination_group`: the group of the artifact at destination (for Linux only).

## Artifact (repository) structure

The Artificat "repository" structure is not fixed at all.
For instance to manage Oracle database software major and "minor" release:

```
└── rdbms
    └── oracle
        ├── AutoUpgrade
        │   └── 20210721
        ├── combo_ojvm+db_release_updates
        │   └── 19c
        │       └── 220118
        ├── dmk
        ├── gold_images
        │   └── 19c
        ├── interim_patches
        │   └── 19c
        ├── Opatch
        │   └── 19c
        │       └── 12.2.0.1.28
        ├── Pre-Upgrade
        │   └── 19c
        └── tools
```

## Examples

You have one example for each provider on Linux and Windows in the test file: `collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml`.

## Tests

```bash
## View all combinations
ansible-playbook --list-tasks collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml
## Test all combinations
ansible-playbook collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml
## Test one combination
ansible-playbook collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml --tags=aws_s3_linux
```
