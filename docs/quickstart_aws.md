# Quickstart for AWS

### Minimum requirements

- AWS infrastructure must exist with private or public IP.
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

Copy the adaquat template file located under `./configuration/infrastructure/aws_testing/srv01`:

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
   mode: auto
   ip:
operating_system: OL8.5-x86_64-HVM-2021-11-24
ami_id: ami-07e51b655b107cd9b
instance_type: t3.medium
ec2_volumes_params:
  - device_name: /dev/sda1
    ebs:
      volume_type: gp2
      volume_size: 10
      delete_on_termination: true
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

Create a directory under your server `./configuration/infrastructure/aws_testing/srv01/postgres` with your component name:

```bash
mkdir ./configuration/infrastructure/aws_testing/srv01/postgres
```

Copy component template file located under `./configuration/infrastructure/aws_testing/srv01/postgres`:

```bash
cp ./configuration/infrastructure_sample/aws/srv-linux-test-01/COMP/variables.yml ./configuration/infrastructure/aws_testing/srv01/postgres
```

This component has a type `postgresql_instance` and requires a predefined storage layout `linux/storage/postgresql_instance`:

```yaml
# File ./configuration/infrastructure/aws_testing/srv01/postgres/variables.yml
component_type: postgresql_instance
storage: linux/storage/postgresql_instance
```

**Optional:** You can use another official storage template available in the YaK project:

```bash
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

You should now see your component `aws_testing/srv01/postgres` in the Ansible inventory:

```bash
$ ansible-inventory --graph
@all:
  |--@aws_testing:
  |  |--aws_testing/srv01
  |  |--aws_testing/srv01/postgres
  |--@postgresql_instance:
  |  |--aws_testing/srv01/postgres
  |--@servers:
  |  |--aws_testing/srv01
  |--@ungrouped:
```

### 8. Deploy the deployment storage requirements

This Ansible playbook will deploy the storage requirements for each component attached to the server:

```bash
ansible-playbook servers/deploy.yml -e target=aws_testing/srv01 --tags=requirements
```

Once completed, connect via SSH to the server and look at the storage layout:

```bash
$ ssh aws_testing/srv01 df -h
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
