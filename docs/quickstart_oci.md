# Quickstart for OCI

### Minimum requirements

- OCI infrastructure must exist with private or public IP.
- OCI credentials.

### 1. Declare your infrastructure

Once in the container, you can describe the infrastructure you wish to begin with.
Below is an example of an OCI testing infrastructure name "oci_testing":

Create a directory under `./configuration/infrastructure` with your infrastructure name:

```
mkdir ./configuration/infrastructure/oci_testing
```

Copy the adaquat template file located under `./configuration/infrastructure_sample`:

```
cp  ./configuration/infrastructure_sample/oci/variables.yml  ./configuration/infrastructure/oci_testing
vi ./configuration/infrastructure/oci_testing/variables.yml
```

Adapt at least the below parameter:

- compartment_id
- availability_domain
- security_list
- subnet_id

```yaml
# File ./configuration/infrastructure/oci_testing/variables.yml
is_cloud_environement: yes
environment: oci_testing
ansible_user: opc
operating_system: Oracle-Linux-8.3-2021.05.12-0
provider: oci
region_id: eu-zurich-1
compartment_id: ****
availability_domain: *****
security_list: ******
subnet_id: ******
```

You should now see your infrastructure in the Ansible inventory:

```
$ ansible-inventory --graph --vars
@all:
  |--@oci_testing:
  |  |--{ami_id = ami-07e51b655b107cd9b}
  |  |--{availability_zone = eu-central-1a}
  |  |--{environment = oci-testing}
  |  |--{instance_type = t3.large}
  |  |--{is_cloud_environment = True}
  |  |--{operating_system = OL8.5-x86_64-HVM-2021-11-24}
  |  |--{provider = oci}
  |  |--{region_id = eu-central-1}
  |  |--{security_group_id = sg-*****}
  |  |--{subnet_id = subnet-**********}
  |--@servers:
  |--@ungrouped:
  |--{ansible_winrm_read_timeout_sec = 60}
  |--{yak_inventory_type = file}
  |--{yak_local_ssh_config_file = ~/yak/configuration/infrastructure/.ssh/config}
  |--{yak_secrets_directory = /workspace/yak/configuration/infrastructure/secrets}
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/infrastructure.md) about infrastructure declaration.

### 2. Declare your first server

Create a directory under your infrastructure `./configuration/infrastructure/oci_testing` with your server name:

```
mkdir ./configuration/infrastructure/oci_testing/srv01
```

Copy the adaquat template file located under `./configuration/infrastructure/oci_testing/srv01`:

```
cp ./configuration/infrastructure_sample/oci/srv-linux-test-01/variables.yml ./configuration/infrastructure/oci_testing/srv01
vi ./configuration/infrastructure/oci_testing/srv01/variables.yml
```

Adapt at least the below parameters:

- hostname
- host_ip_access: private_ip|public_ip
- private_ip
  - mode : manual | auto
  - ip : ip_address_value | or leave_it_empty_with_auto
- public_ip
  - mode : manual | auto | none
    - ip : ip_address_value | or leave_it_empty_with_auto_or_none

```yaml
# File ./configuration/infrastructure/oci_testing/srv01/variables.yml
hostname: srv01
is_physical_server: no
ansible_user: opc
host_ip_access: public_ip
private_ip:
    mode: auto
    ip: 
public_ip:
    mode: auto
    ip: 
operating_system: Oracle-Linux-8.5-2022.01.24-0
image_id: ocid1.image.oc1.eu-zurich-1.aaaaaaaamtulj4fmm6cx6xq6delggc5jhfoy652lbxxj2xbnzzxik7sgsnva
shape:
    name: VM.Standard.E4.Flex
    memory_in_gbs: 12
    ocpus: 8
```

You should now see your server in the Ansible inventory:

```
$ ansible-inventory --graph
@all:
  |--@oci_testing:
  |  |--oci_testing/srv01
  |--@servers:
  |  |--oci_testing/srv01
  |--@ungrouped:
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/README.md) about server configuration.

### 3. Create your default ssh key

This ssh key will be used for your server connection.

Create a directory `secrets` under your infrastructure `./configuration/infrastructure/oci_testing`:

```
mkdir ./configuration/infrastructure/oci_testing/secrets
```

Generate your default SSH key with the script `gen_secret`:

```
cd ./configuration/infrastructure/oci_testing/secrets
gen_secret
cd -
```

You should now see the SSH key used by your server:

```
$ ansible-inventory --host oci_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/oci_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/oci_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/secret_management.md) about key management.

### 4. Copy your OCI Cloud authentication

Use your OCI CLI programmatic access key variables:

```bash
export OCI_USER_ID=*****
export OCI_USER_FINGERPRINT=*****
export OCI_TENANCY=*****
export OCI_REGION=eu-zurich-1
export OCI_USER_KEY_FILE=$HOME/.ssh/oracleidentitycloudservice.pem
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/cloud_authentication.md) about the Cloud provider authentification.

### 5. Deploy your server

```
ansible-playbook servers/deploy.yml -e target=oci_testing/srv01
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/servers.md) about the server deployment possibilities

### 6. Connect to the server

Ping with the Ansible module to ensure the connectivity works:

```
ansible -m ping oci_testing/srv01
```

Connect via SSH to the server:

```
ssh oci_testing/srv01
```

### 7. Declare your first component

Create a directory under your server `./configuration/infrastructure/oci_testing/srv01/postgres` with your component name:

```
mkdir ./configuration/infrastructure/oci_testing/srv01/postgres
```

Copy component template file located under `./configuration/infrastructure/oci_testing/srv01/postgres`:

```
cp ./configuration/infrastructure_sample/oci/srv-linux-test-01/COMP/variables.yml ./configuration/infrastructure/oci_testing/srv01/postgres
```

This component has a type `postgresql_instance` and requires a predefined storage layout `linux/storage/postgresql_instance`:

```yaml
# File ./configuration/infrastructure/oci_testing/srv01/postgres/variables.yml
component_type: postgresql_instance
storage: linux/storage/postgresql_instance
```

**Optional:** You can use another official storage template available in the YaK project:

```
$ tree configuration/templates/
configuration/templates/
|-- linux
|   `-- storage
|       |-- demo_instance.yml
|       |-- mongodb_instance.yml
|       |-- oracle_instance.yml
|       |-- postgresql_instance.yml
|       |-- sqlserver_instance.yml
|       `-- weblogic_domain.yml
`-- windows
    `-- storage
        `-- sqlserver_instance.yml
```

You should now see your component `oci_testing/srv01/postgres` in the Ansible inventory:

```
$ ansible-inventory --graph
@all:
  |--@oci_testing:
  |  |--oci_testing/srv01
  |  |--oci_testing/srv01/postgres
  |--@postgresql_instance:
  |  |--oci_testing/srv01/postgres
  |--@servers:
  |  |--oci_testing/srv01
  |--@ungrouped:
```

### 8. Deploy the deployment storage requirements

This Ansible playbook will deploy the storage requirements for each component attached to the server:

```
ansible-playbook servers/deploy.yml -e target=oci_testing/srv01 --tags=requirements
```

Once completed, connect via SSH to the server and look at the storage layout:

```
$ ssh oci_testing/srv01 df -h
Filesystem            Size  Used Avail Use% Mounted on
devtmpfs              3.7G     0  3.7G   0% /dev
tmpfs                 3.7G  8.0K  3.7G   1% /dev/shm
tmpfs                 3.7G   17M  3.7G   1% /run
tmpfs                 3.7G     0  3.7G   0% /sys/fs/cgroup
/dev/nvme0n1p1         10G  1.8G  8.3G  18% /
tmpfs                 757M     0  757M   0% /run/user/1000
/dev/mapper/data-u01  4.0G   62M  4.0G   2% /u01
/dev/mapper/data-u02   12G  119M   12G   1% /u02
/dev/mapper/data-u90   24G  205M   24G   1% /u90
```

You are now ready to operate your components on your server!

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
