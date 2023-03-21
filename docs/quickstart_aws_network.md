# Quickstart for AWS

### Minimum requirements

- AWS credentials.

### 1. Declare your infrastructure

**DISCLAIMER**: Infrastructure deployment will only work the exact example given is this documentation, improvements will be coming soon.


Once in the container, you can describe the infrastructure you wish to begin with.
Below is an example of an AWS testing infrastructure named "aws_testing":

Create a directory under `./configuration/infrastructure` with your infrastructure name:

```bash
mkdir ./configuration/infrastructure/aws_testing
```

Copy the adaquat template file located under `./configuration/infrastructure_sample/`:

```bash
cp  ./configuration/infrastructure_sample/aws_network/variables.yml  ./configuration/infrastructure/aws_testing
vi ./configuration/infrastructure/aws_testing/variables.yml
```

Adapt the below parameter:

- region_id: 
- availability_zone: 
- vpc_name: 
- vpc_cidr_block: 
- subnet_list:
    - az_value: 
    - subnet_cidr: 
    - subnet_tag_name:
    - public: yes | no 
    - nat_gw: yes | no 
    - nat_target: 
- igw_tag_name: 
- security_group_name:

The nat_gw variable is optionnal, fill it with yes only if you want a nat gateway linked to your subnet(s).  
**A nat gateway MUST be created in a PUBLIC subnet.**  
The **nat_target** variable must be filled with the name of the **PRIVATE** subnet you want to link to the nat gateway, if you want one.


```yaml
# File ./configuration/infrastructure/aws_testing/variables.yml
is_cloud_environment: yes
provider: aws
region_id: eu-central-1
availability_zone: eu-central-1a
vpc_name: yak_vpc_test
vpc_cidr_block: 10.10.0.0/16
subnet_list:
    - az_value: eu-central-1a
      subnet_cidr: 10.10.1.0/24
      subnet_tag_name: yak_subnet_public_1
      public: "yes"
      nat_gw: "yes"
      nat_target: /
    - az_value: eu-central-1a
      subnet_cidr: 10.10.2.0/24
      subnet_tag_name: yak_subnet_private_1
      public: "no"
      nat_gw: "no"
      nat_target: yak_subnet_private_1
    - az_value: eu-central-1b
      subnet_cidr: 10.10.3.0/24
      subnet_tag_name: yak_subnet_public_2
      public: "no"
      nat_gw: "no"
      nat_target: /
    - az_value: eu-central-1b
      subnet_cidr: 10.10.4.0/24
      subnet_tag_name: yak_subnet_private_2
      public: "no"
      nat_gw: "no"
      nat_target: /
igw_tag_name: yak_igw_test
security_group_name: yak_sg
ip_list:
  - 192.168.1.0/32
  - 172.0.0.1/32
TCP_ports_security_group_public_IP: 
  - 22
  - 80
  - 443
TCP_ports_security_group_other_IP: 
  - 22
  - 80
  - 443
UDP_ports_security_group_public_IP: 
  - 10050
  - 10051
UDP_ports_security_group_other_IP: 
  - 10050
  - 10051
```

You should now see your infrastructure in the Ansible inventory:

```bash
$ ansible-inventory --graph --vars
@all:
  |--@aws_testing:
  |  |--{TCP_ports_security_group_other_IP = [22, 80, 443]}
  |  |--{TCP_ports_security_group_public_IP = [22, 80, 443]}
  |  |--{UDP_ports_security_group_other_IP = [10050, 10051]}
  |  |--{UDP_ports_security_group_public_IP = [10050, 10051]}
  |  |--{availability_zone = ********}
  |  |--{igw_tag_name = ******}
  |  |--{ip_list = ['192.168.1.0/32', '172.0.0.1/32']}
  |  |--{is_cloud_environment = True}
  |  |--{provider = aws}
  |  |--{region_id = ************}
  |  |--{security_group_name = ******}
  |  |--{subnet_list = [{'az_value': ******, 'subnet_cidr': ********, 'subnet_tag_name': *******, 'nat_gw': **}],[...]}
  |  |--{vpc_cidr_block = *********}
  |  |--{vpc_name = ********}
  |--@servers:
  |--@ungrouped:
  |--{ansible_winrm_read_timeout_sec = 60}
  |--{yak_inventory_type = file}
  |--{yak_local_ssh_config_file = ~/yak/configuration/infrastructure/.ssh/config}
  |--{yak_secrets_directory = /workspace/yak/configuration/infrastructure/secrets}
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/infrastructure.md) about infrastructure declaration.


### 2. Copy your AWS Cloud authentication

Use your AWS CLI programmatic access key variables:

```bash
export AWS_ACCESS_KEY_ID="*******"
export AWS_SECRET_ACCESS_KEY="**********"
export AWS_SESSION_TOKEN="***********`
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/cloud_authentication.md) about the Cloud provider authentification.

### 3. Deploy your infrastructure

```
ansible-playbook infrastructure/deploy.yml -e target=infrastructure/aws_testing
```


## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
