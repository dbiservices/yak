# Quickstart for AZURE

### Minimum requirements

- AZURE infrastructure must exist with private or public IP.
- AZURE credentials.

### 1. Declare your infrastructure

Once in the container, you can describe the infrastructure you wish to begin with.
Below is an example of an AZURE testing infrastructure name "azure_testing":

Create a directory under `./configuration/infrastructure` with your infrastructure name:

```
mkdir ./configuration/infrastructure/azure_testing
```

Copy the adaquat template file located under `./configuration/infrastructure_sample`:

```
cp  ./configuration/infrastructure_sample/azure/variables.yml  ./configuration/infrastructure/azure_testing
vi ./configuration/infrastructure/azure_testing/variables.yml
```

Adapt at least the below parameter:

- subscription id
- resource_group
- virtual_network_name
- security_group
- subnet_name

```yaml
# File ./configuration/infrastructure/azure_testing/variables.yml
is_cloud_environment: yes
environment: production
ansible_user: azureuser
provider: azure
subscription:
    id:
    name: Azure subscription Name
resource_group: dbi-testing-yak-rg
virtual_network_name: dbi-testing-yak-nsg
subnet_name: dbi-testing-yak-subnet
security_group: dbi-testing-yak-nsg
```

You should now see your infrastructure in the Ansible inventory:

```
$ ansible-inventory --graph azure_testing--vars
yak@7c3380657dd5:~/yak$ ansible-inventory --graph azure_testing  --vars
@azure_testing:
  |--{ansible_user = azureuser}
  |--{environment = production}
  |--{is_cloud_environement = True}
  |--{provider = azure}
  |--{resource_group = dbi-testing-yak-rg}
  |--{security_group = dbi-testing-yak-nsg}
  |--{subnet_name = dbi-testing-yak-subnet}
  |--{subscription = {'id': '54752284-75ab-4fbc-a9b0-*******', 'name': 'Azure subscription'}}
  |--{virtual_network_name = dbi-testing-yak-network}
```
[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/infrastructure.md) about infrastructure declaration.

### 2. Declare your first server

Create a directory under your infrastructure `./configuration/infrastructure/azure_testing` with your server name:

```
mkdir ./configuration/infrastructure/azure_testing/srv01
```

Copy the adaquat template file located under `./configuration/infrastructure/azure_testing/srv01`:

```
cp ./configuration/infrastructure_sample/azure/srv-linux-test-01/variables.yml ./configuration/infrastructure/azure_testing/srv01
vi ./configuration/infrastructure/azure_testing/srv01/variables.yml
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
# File ./configuration/infrastructure/azure_testing/srv01/variables.yml
vi ./configuration/infrastructure/azure_testing/srv01/variables.yml
hostname: srv01
is_physical_server: no
ansible_user: azureuser
host_ip_access: public_ip
private_ip:
    mode: auto
    ip: 
public_ip:
    mode: auto
    ip: 
vm_size: Standard_B2ms
image:
    offer: Oracle-Linux
    publisher: Oracle
    sku: ol85-lvm
    version: latest

```

You should now see your server in the Ansible inventory:

```
$ ansible-inventory --graph
@all:
  |--@azure_testing:
  |  |--azure_testing/srv01
  |--@servers:
  |  |--azure_testing/srv01
  |--@ungrouped:
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/README.md) about server configuration.

### 3. Create your default ssh key

This ssh key will be used for your server connection.

Create a directory `secrets` under your infrastructure `./configuration/infrastructure/azure_testing`:

```
mkdir ./configuration/infrastructure/azure_testing/secrets
```

Generate your default SSH key with the script `gen_secret`:

```
cd ./configuration/infrastructure/azure_testing/secrets
gen_secret
cd -
```

You should now see the SSH key used by your server:

```
$ ansible-inventory --host azure_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/azure_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/azure_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/secret_management.md) about key management.

### 4. Copy your AZURE Cloud authentication

Use your AZURE CLI programmatic access key variables:

```bash
export AZURE_SUBSCRIPTION_ID=******
export AZURE_CLIENT_ID=*******
export AZURE_SECRET=********
export AZURE_TENANT=**********

```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/configuration/cloud_authentication.md) about the Cloud provider authentification.

### 5. Deploy your server

```
ansible-playbook servers/deploy.yml -e target=azure_testing/srv01
```

[Here are more details](https://gitlab.com/yak4all/yak/-/blob/main/docs/servers.md) about the server deployment possibilities

### 6. Connect to the server

Ping with the Ansible module to ensure the connectivity works:

```
ansible -m ping azure_testing/srv01
```

Connect via SSH to the server:

```
ssh azure_testing/srv01
```

### 7. Declare your first component

Create a directory under your server `./configuration/infrastructure/azure_testing/srv01/postgres` with your component name:

```
mkdir ./configuration/infrastructure/azure_testing/srv01/postgres
```

Copy component template file located under `./configuration/infrastructure/azure_testing/srv01/postgres`:

```
cp ./configuration/infrastructure_sample/azure/srv-linux-test-01/COMP/variables.yml ./configuration/infrastructure/azure_testing/srv01/postgres
```

This component has a type `postgresql_instance` and requires a predefined storage layout `linux/storage/postgresql_instance`:

```yaml
# File ./configuration/infrastructure/azure_testing/srv01/postgres/variables.yml
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

You should now see your component `azure_testing/srv01/postgres` in the Ansible inventory:

```
$ ansible-inventory --graph
@all:
  |--@azure_testing:
  |  |--azure_testing/srv01
  |  |--azure_testing/srv01/postgres
  |--@postgresql_instance:
  |  |--azure_testing/srv01/postgres
  |--@servers:
  |  |--azure_testing/srv01
  |--@ungrouped:
```

### 8. Deploy the deployment storage requirements

This Ansible playbook will deploy the storage requirements for each component attached to the server:

```
ansible-playbook servers/deploy.yml -e target=azure_testing/srv01 --tags=requirements
```

Once completed, connect via SSH to the server and look at the storage layout:

```
$ ssh azure_testing/srv01 df -h
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
