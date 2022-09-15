Artifacts
=========

Role used to manage Artificats (software binaries); This role manage downloads of files depending on a variable strucuture.

Software delivery
----------------------
As of licensing restrictions about software distribution for various editors.
The download of the Oracle software onto the Artifact repository is left over to each customer.

The software editor licensing conditions must be accepted prior downloading the software.


Role Variables (fixed)
----------------------
n.a

Playbook Variables
------------------
 * Artifacts managed through control node
 ```
   vars:
     - pv_artifacts_repo:
         provider: ansible_control_node
         # remote_src = false when Artifacts available on control-node
         remote_src: false
         path: "{{ gv_appliance_home }}
 ```

 * Artifacts managed through AWS s3 bucket
 ```
   vars:
     - pv_artifacts_repo:
         provider: aws_s3
         # AWS S3 blucket name
         bucket_name: "yak-artifacts"
         # s3 prefixes are similar to folders (organize data)
         prefix: "rdbms/oracle"
         remote_src: true
         # managed node properties for copied files on managed node
         path: "/u01/app/oracle/artifacts"
         owner: "oracle"
         group: "oinstall"
 ```
Prerequisites
-------------

The O.S owner & Group of the folder (pv_artifacts_repo.path) on the managed nodes are prerequisites unless Artifacts are managed on Ansible Control Node.

Artifact (repository) structure
--------------------------------

The Artificat "repository" structure is not fixed at all. Actually, the folder layout supports the concept of flat file versioning for distinct componnents.

For instance to manage Oracle database software major and "minor" release 
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

Example
-------
### Playbook

```
- name: Download some artificats
  hosts: dev
  vars:
    - pv_artifacts_repo:
        provider: aws_s3
        # AWS S3 blucket name
        bucket_name: "yak-artifacts"
        # s3 prefixes are similar to folders (organize data)
        prefix: "rdbms/oracle"
        remote_src: true
        # managed node properties for copied files
        path: "/u01/app/oracle/artifacts"
        owner: "oracle"
        group: "oinstall"

    # variable used in role(s): ora_packages
    - pv_artifacts_list:
        - "rdbms/oracle/file1.zip"
        - "rdbms/oracle/file2.zip"
        - "rdbms/oracle/file3.zip"
  environment:
    # variables used in role(s): yak.core.artifacts
    # only required for artifacts if pv_artifact_repo.provider = aws_s3
    - AWS_ACCESS_KEY_ID     : "{{ lookup('env','AWS_ACCESS_KEY_ID') }}"
    - AWS_SECRET_ACCESS_KEY : "{{ lookup('env','AWS_SECRET_ACCESS_KEY') }}"
    - AWS_SESSION_TOKEN     : "{{ lookup('env','AWS_SESSION_TOKEN') }}"
  roles:
    - artifacts
```


### Command line
    # ansible-playbook roles/ora_rdbms_base/tests/test.yml
    # ansible-playbook roles/artifacts/tests/download_from_aws-s3_to_ansible-control-node.yml

Notes
-------

n/a
