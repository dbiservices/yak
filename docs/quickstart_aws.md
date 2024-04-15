# Quickstart for AWS

### Minimum requirements

- AWS infrastructure must exist with private or public IP. [Tutorial to create your own infrastructure here](https://gitlab.com/yak4all/yak/-/blob/main/docs/quickstart_aws_network.md)
- AWS credentials.

### 1. Declare your infrastructure

Once in the container, you can describe the infrastructure you wish to begin with.
Below is an example of an AWS testing infrastructure name "aws_testing":

Create a directory under `./configuration/infrastructure` with your infrastructure name:

```bash
mkdir ./configuration/infrastructure/aws_testing
```

Copy the adaquat template file located under `./configuration/infrastructure_sample`:

```bash
cp  ./configuration/infrastructure_sample/aws/variables.yml  ./configuration/infrastructure/aws_testing
vi ./configuration/infrastructure/aws_testing/variables.yml
```

Adapt at least the below parameter:

- security_group_id
- subnet_id

```yaml
# File ./configuration/infrastructure/aws_testing/variables.yml
is_cloud_environment: yes
provider: aws
availability_zone: eu-central-1a
region_id: eu-central-1
security_group_id:
subnet_id:

custom_tags:
    Environment: Test
    Department: Development YaK
    Business_unit: YaK

```

You should now see your infrastructure in the Ansible inventory:

```bash
$ ansible-inventory --graph --vars
@all:
  |--@aws_testing:
  |  |--{availability_zone = eu-central-1a}
  |  |--{is_cloud_environment = True}
  |  |--{provider = aws}
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

Create a directory under your infrastructure `./configuration/infrastructure/aws_testing` with your server name:

```bash
mkdir ./configuration/infrastructure/aws_testing/srv01
```

Copy one of the below server template file for Linux or Windows under `./configuration/infrastructure/aws_testing/srv01`:

```bash
/configuration/infrastructure_sample/aws/srv-linux-test-01/variables.yml 
/configuration/infrastructure_sample/aws/srv-win-test-01/variables.yml 
```

In our example we choose the Linux templates 
```bash
cp ./configuration/infrastructure_sample/aws/srv-linux-test-01/variables.yml ./configuration/infrastructure/aws_testing/srv01
vi ./configuration/infrastructure/aws_testing/srv01/variables.yml
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
# File ./configuration/infrastructure/aws_testing/srv01/variables.yml
hostname: srv01
is_physical_server: no
ansible_user: ec2-user
host_ip_access: private_ip
private_ip:
   mode: auto
   ip:
public_ip:
   mode: none
   ip:
operating_system: OL8.7-x86_64-HVM-2023-03-07
ami_id: ami-065e2293a3df4c870
instance_type: t3.medium
```

You should now see your server in the Ansible inventory:

```bash
$ ansible-inventory --graph
@all:
  |--@aws_testing:
  |  |--aws_testing/srv01
  |--@servers:
  |  |--aws_testing/srv01
  |--@ungrouped:
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/README.md) about server configuration.

### 3. Create your secret

A SSH key (for Linux) will be used for your server connection. For Windows, you'll need to generate certificate.

Create a directory `secrets` under your infrastructure `./configuration/infrastructure/aws_testing`:

```bash
mkdir ./configuration/infrastructure/aws_testing/secrets
```

#### For Linux (SSH Key)

Generate your default SSH key with the script `gen_secret`:

```bash
cd ./configuration/infrastructure/aws_testing/secrets
gen_secret
cd -
```

You should now see the SSH key used by your server:

```bash
$ ansible-inventory --host aws_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/aws_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/aws_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
```

#### For Windows (Certificate)

```bash
cd ./configuration/infrastructure/aws_testing/secrets
gen_secret

# Set the name of the local user that will have the key mapped to
USERNAME="Ansible"

cat > openssl.conf << EOL
distinguished_name = req_distinguished_name
[req_distinguished_name]
[v3_req_client]
extendedKeyUsage = clientAuth
subjectAltName = otherName:1.3.6.1.4.1.311.20.2.3;UTF8:$USERNAME@localhost
EOL

export OPENSSL_CONF=openssl.conf
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out cert.pem -outform PEM -keyout cert_key.pem -subj "/CN=$USERNAME" -extensions v3_req_client

rm openssl.conf

cd -
```

More options on [the Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html#generate-a-certificate) for Windows managed host.

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/secret_management.md) about key management.

### 4. Copy your AWS Cloud authentication

Use your AWS CLI programmatic access key variables:

```bash
export AWS_ACCESS_KEY_ID="*******"
export AWS_SECRET_ACCESS_KEY="**********"
export AWS_SESSION_TOKEN="***********`
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/cloud_authentication.md) about the Cloud provider authentification.

### 5. Deploy your server

```
ansible-playbook servers/deploy.yml -e target=aws_testing/srv01
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/servers.md) about the server deployment possibilities

### 6. Connect to the server

Ping with the Ansible module to ensure the connectivity works:

```bash
ansible -m ping aws_testing/srv01
```

Connect via SSH to the server:

```bash
ssh aws_testing/srv01
```

### 7. Declare your first component

The component configuration is located under a separated directory structure ./configuration/components

To deploy the disks for your server, you can use a DEMO component

Create a directory under `./configuration/components` with your component name DEMO in our case

```bash
mkdir ./configuration/components/DEMO
```

Copy the adaquat template file located under `./configuration/components_sample/DEMO`:

```bash
cp  ./configuration/components_sample/DEMO/variables.yml  ./configuration/components/DEMO
vi ./configuration/components/DEMO/variables.yml
```
Now you can update the parameters for your required filesystem or windows disks 

```yaml
# File ./configuration/components/DEMO/variables.yml
# Copyright: (c) 2023, dbi services, distributed without any warranty under the terms of the GNU General Public License v3
#
component_type: os_storage/storage

# Variable indicated in the manifest and declaring the servers belonging to group 'my_servers'
yak_manifest_my_servers:
    - aws_testing/srv01

yak_manifest_my_os_storage_config:
    linux:
        - { size_gb: 5, filesystem_type: "xfs", mount_point: "/u01" }
        - { size_gb: 5, filesystem_type: "xfs", mount_point: "/u02" }
    windows:
        - { size_gb: 5, drive_letter: F, partition_label: data   }
        - { size_gb: 5, drive_letter: G, partition_label: backup }
```

### 8. Set the inventory to your DEMO component

```bash
sc DEMO 

ansible-inventory --graph 
@all:
  |--@ungrouped:
  |--@OCI:
  |--@AWS:
  |--@aws_testing:
  |  |--aws_testing/srv01
  |--@my_servers:
  |  |--aws_testing/srv01
```

### 9. Deploy the storage of your DEMO component

This Ansible playbook will deploy the storage of the component attached to your server:

```bash
ansible-playbook servers/deploy.yml -e target=aws_testing/srv01
```

Once completed, connect via SSH to the server and look at the storage layout:

```bash
$ ssh aws_testing/srv01 
$ df -h
Filesystem            Size  Used Avail Use% Mounted on
devtmpfs              3.7G     0  3.7G   0% /dev
tmpfs                 3.7G  8.0K  3.7G   1% /dev/shm
tmpfs                 3.7G   17M  3.7G   1% /run
tmpfs                 3.7G     0  3.7G   0% /sys/fs/cgroup
/dev/nvme0n1p1         10G  1.8G  8.3G  18% /
tmpfs                 757M     0  757M   0% /run/user/1000
/dev/mapper/data-u01  4.0G   62M  4.0G   2% /u01
/dev/mapper/data-u02   12G  119M   12G   1% /u02
```
You are now ready to operate your component for your deploy servers!

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
