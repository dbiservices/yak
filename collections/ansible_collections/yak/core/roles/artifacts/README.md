# Artifacts

Copy any files from an artifact provider (AWS S3, Azure Storage Blob, OCI object storage, etc)
into an instance at the specified location.

The role copies artifacts from the artifact provider to the destination instance (no intermediaries).

## Prerequisites

- The artifact structures and files must exist.
- You must have correct credentials and permissions to access artifacts.
- Per artifact provider requisites:
  - `aws_s3`: a bucket named 'yak' and the secret key in environment variables.
  - `azure_storage_blob`: a storage user and a container both named 'yak' and the secret key in environment variables.
  - `oci_object_storage`: a bucket named 'yak' and the secret key in environment variables.

## Variables

### From configuration

- `artifacts.provider`: the supported provider of your artifacts:
  - `aws_s3`
  - `azure_storage_blob`
  - `oci_object_storage`
- `artifacts.variables`: dictionary of variables specific to an artifact provider.
  - `aws_s3`:
    - `bucket_name`
  - `azure_storage_blob`:
    - `storage_account_name`
    - `container`
  - `oci_object_storage`:
    - `bucket_name`

#### Example

```yaml
artifacts:
  provider: aws_s3
  variables:
    bucket_name: yak-artifacts
```

### From components

- `artifact`: the name of the artifact (can be a relative path).
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

## Example

```yaml
  roles:
    - role: yak.core.artifacts
      vars:
        artifact_files: rdbms/oracle/gold_images/19c/orainstall.zip
        destination_path: /tmp
        destination_owner: oracle
        destination_group: oinstall
```

## Tests

```bash
## View all combinations
ansible-playbook --list-tasks collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml
## Test all combinations
ansible-playbook collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml
## Test one combination
ansible-playbook collections/ansible_collections/yak/core/roles/artifacts/tests/test.yml --tags=aws_s3_linux
```
