# Artifacts

Copy any files from an artifact provider (AWS S3, Azure Storage Blob, OCI object storage, etc)
into an instance at the specified location.

The role copies artifacts from the artifact provider to the destination instance (no intermediaries).

## Prerequisites

- The artifact structures and files must exist.
- You must have correct credentials and permissions to access artifacts.
- Per provider requisites:
  - `aws_s3`: a bucket named 'yak' and the secret key in environment variables.
  - `azure_storage_blob`: a storage user and a container both named 'yak' and the secret key in environment variables.
  - `oci_object_storage`: a bucket named 'yak' and the secret key in environment variables.

# Variables

- `artifact_provider`: the provider of your artifacts:
  - `aws_s3`
  - `azure_storage_blob`
  - `oci_object_storage`
- `artifact`: the name of the artifact (can be a relative path).
- `destination_path`: the directory into which to copy the artifact.
- `destination_owner`: the owner of the artifact at destination.
- `destination_group`: the group of the artifact at destination.


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
    - role: artifacts
      vars:
        artifact_provider: aws_s3
        artifact_file: rdbms/oracle/gold_images/19c/orainstall.zip
        destination_path: /u01/app/install
        destination_owner: oracle
        destination_group: oinstall
```
