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

custom_tags:
    Environment: Test
    Department: Development YaK
    Business_unit: YaK

storage_devices:
    max_size_gb: 100
    specifications:
        storage_account_type: StandardSSD_LRS
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

Copy one of the below server template file for Linux or Windows under `./configuration/infrastructure/aws_testing/srv01`:

```bash
/configuration/infrastructure_sample/azure/srv-linux-test-01/variables.yml 
/configuration/infrastructure_sample/azure/srv-windows-test-01/variables.yml 
```

In our example we choose the Linux templates 

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
    sku: ol87-lvm
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

### 3. Create your secret

A SSH key (for Linux) will be used for your server connection. For Windows, you'll need to generate certificate.

Create a directory `secrets` under your infrastructure `./configuration/infrastructure/azure_testing`:

```bash
mkdir ./configuration/infrastructure/azure_testing/secrets
```

#### For Linux (SSH Key)

Generate your default SSH key with the script `gen_secret`:

```bash
cd ./configuration/infrastructure/azure_testing/secrets
gen_secret
cd -
```

You should now see the SSH key used by your server:

```bash
$ ansible-inventory --host azure_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/azure_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/azure_testing/secrets/sshkey.pub",
    "ansible_user": "azureuser",
. . .
```

#### For Windows (Certificate)

```bash
cd ./configuration/infrastructure/azure_testing/secrets

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

### 4. Set your AZURE Cloud authentication

Use your AZURE CLI programmatic access key variables:

```bash
export AZURE_SUBSCRIPTION_ID=******
export AZURE_CLIENT_ID=*******
export AZURE_SECRET=********
export AZURE_TENANT=**********
```

or you can also use your SSO authentification if configured 

```bash
az login --tenant <tenant-id-number>
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

Connect via SSH to the Linux server:

```
ssh azure_testing/srv01
```

Connect via RDP to the windows server with the provider information on the output of the deployment:

```
rdp <public_ip/private_ip available in the inventory > Ansible/<generated-password>
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
Now you can update the parameters for your server name and your required filesystem or windows disks 

```yaml
# File ./configuration/components/DEMO/variables.yml
# Copyright: (c) 2023, dbi services, distributed without any warranty under the terms of the GNU General Public License v3
#
component_type: os_storage/storage

# Variable indicated in the manifest and declaring the servers belonging to group 'my_servers'
yak_manifest_my_servers:
    - azure_testing/srv01

yak_manifest_my_os_storage_config:
    linux:
        - { size_GB: 5, filesystem_type: "xfs", mount_point: "/u01" }
        - { size_GB: 5, filesystem_type: "xfs", mount_point: "/u02" }
    windows:
        - { size_GB: 5, drive_letter: F, partition_label: data   }
        - { size_GB: 5, drive_letter: G, partition_label: backup }
```

### 8. Set the inventory to your DEMO component

```bash
sc DEMO 
ansible-inventory --graph 
```

### 9. Deploy the storage of your DEMO component

This Ansible playbook will deploy the storage of the component attached to your server:

```bash
ansible-playbook servers/deploy.yml -e target=azure_testing/srv01
```

Once completed, connect via SSH to the server and look at the storage layout:

```
$ ssh azure_testing/srv01
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
