# Quickstart for AWS

## Minimum requirements

- Container management software (e.g., docker).
- Internet access to download the container.
- AWS infrastructure must exist with private or public IP.
- AWS credentials.

## 1. Get the container

Pull the YaK Core container `registry.gitlab.com/yak4all/yak:latest` to your workstation:

```bash
docker pull registry.gitlab.com/yak4all/yak:latest
```

**FYI:** The YaK Core container will include the pulling from the Yak Env
Container `registry.gitlab.com/yak4all/yakenv:1.0.0`. This container contains
the required packages used by YaK Core.

[Here are more details](https://gitlab.com/yak4all/yakenv/-/blob/main/Dockerfile) about the used Docker file.

## 2. Run the container

Define a local directory with the variable `${MY_LOCAL_CONFIGURATION_DIR}`:

```bash
export MY_LOCAL_CONFIGURATION_DIR=$HOME/yak
mkdir -p ${MY_LOCAL_CONFIGURATION_DIR}
```

Start the container with the below command:

```bash
docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash
```

If it worked well, you should be inside the container with the YaK software configured:

```
$ docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash
[...]
yak@d47a98f30c99:~/yak$ ansible-inventory --graph
@all:
  |--@ungrouped:
yak@d47a98f30c99:~/yak$
```

## 3. Declare your infrastructure

Once in the container, you can describe the infrastructure you wish to begin with.
Below is an example of an AWS testing infrastructure name "aws_testing":

Create a directory under `./configuration/infrastructure` with your infrastructure name:

```
mkdir ./configuration/infrastructure/aws_testing
```

Copy the adaquat template file located under `./configuration/infrastructure_sample`:

```
cp  ./configuration/infrastructure_sample/aws/variables.yml  ./configuration/infrastructure/aws_testing
vi ./configuration/infrastructure/aws_testing/variables.yml
```

Adapt at least the below parameter:

- security_group_id
- subnet_id

```yaml
# File ./configuration/infrastructure/aws_testing/variables.yml
is_cloud_environment: yes
operating_system: Oracle Linux 8.3
provider: aws
availability_zone: eu-central-1a
instance_type: t3.large
ami_id: ami-0211d10fb4a04824a
region_id: eu-central-1
security_group_id: sg-*****
subnet_id: subnet-**********
```

You should now see your infrastructure in the Ansible inventory:

```
$ ansible-inventory --graph --vars
@all:
  |--@aws_testing:
  |  |--{ami_id = ami-07e51b655b107cd9b}
  |  |--{availability_zone = eu-central-1a}
  |  |--{environment = aws-testing}
  |  |--{instance_type = t3.large}
  |  |--{is_cloud_environment = True}
  |  |--{operating_system = OL8.5-x86_64-HVM-2021-11-24}
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

## 4. Declare your first server

Create a directory under your infrastructure `./configuration/infrastructure/aws_testing` with your server name:

```
mkdir ./configuration/infrastructure/aws_testing/srv01
```

Copy the adaquat template file located under `./configuration/infrastructure/aws_testing/srv01`:

```
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
operating_system: OL8.5-x86_64-HVM-2021-11-24
ami_id: ami-07e51b655b107cd9b
instance_type: t3.large
ec2_volumes_params:
  - device_name: /dev/sda1
    ebs:
      volume_type: gp2
      volume_size: 10
      delete_on_termination: true
```

You should now see your server in the Ansible inventory:

```
$ ansible-inventory --graph
@all:
  |--@aws_testing:
  |  |--aws_testing/srv01
  |--@servers:
  |  |--aws_testing/srv01
  |--@ungrouped:
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/README.md) about server configuration.

### 5. Create your default ssh key

This ssh key will be used for your server connection.

Create a directory `secrets` under your infrastructure `./configuration/infrastructure/aws_testing`:

```
mkdir ./configuration/infrastructure/aws_testing/secrets
```

Generate your default SSH key with the script `gen_secret`:

```
cd ./configuration/infrastructure/aws_testing/secrets
gen_secret
cd -
```

You should now see the SSH key used by your server:

```
$ ansible-inventory --host aws_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/aws_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/aws_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/secret_management.md) about key management.

### 6. Copy your AWS Cloud authentication

Use your AWS CLI programmatic access key variables:

```bash
export AWS_ACCESS_KEY_ID="*******"
export AWS_SECRET_ACCESS_KEY="**********"
export AWS_SESSION_TOKEN="***********`
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/cloud_authentication.md) about the Cloud provider authentification.

### 7. Deploy your server

```
ansible-playbook servers/deploy.yml -e target=aws_testing/srv01
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/servers.md) about the server deployment possibilities

### 8. Connect to the server

Ping with the Ansible module to ensure the connectivity works:

```
ansible -m ping aws_testing/srv01
```

Connect via SSH to the server:

```
ssh aws_testing/srv01
```

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
