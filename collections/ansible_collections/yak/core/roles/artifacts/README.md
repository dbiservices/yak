Artifacts
=========

Role used to manage Artificats (software binaries); This role manage downloads of files depending on a variable strucuture.


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
