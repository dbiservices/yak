# On-premise Infrastructure Integration

- your On-premise network infrastructure must already exist, with access from the YaK Server 

### 1. Declare your infrastructure

Once in the container, you can describe the infrastructure you wish to begin with.
Below is an example of an On-premise testing infrastructure name "onpremise_testing":

Create a directory under `./configuration/infrastructure` with your infrastructure name:

```bash
mkdir ./configuration/infrastructure/onpremise_testing
```

Create an empty variable.yml inside the new created directory:
```bash
touch ./configuration/infrastructure/onpremise_testing/variables.yml
```

Add at least the below parameter into your variables.yml file:

```yaml
# File ./configuration/infrastructure/onpremise_testing/variables.yml
is_cloud_environment: no
provider: on-premises
```

You should now see your infrastructure in the Ansible inventory:

```bash
$ ansible-inventory --graph --vars
@all:
  |--@onpremise_testing:
  |  |--{provider = on-premises}
  |  |--{target_type = infrastructure}
```

### 2. Create your secret

A SSH key (for Linux) will be used for your server connection. For Windows, you'll need to generate certificate.

Create a directory `secrets` under your infrastructure `./configuration/infrastructure/onpremise_testing`:

```bash
mkdir ./configuration/infrastructure/onpremise_testing/secrets
```

#### 2.1 For Linux (SSH Key)

Generate your default SSH key with the script `gen_secret`:

```bash
cd ./configuration/infrastructure/onpremise_testing/secrets
gen_secret
cd -
```

You should now see the SSH key used by your server:

```bash
$ ansible-inventory --host onpremise_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/onpremise_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/onpremise_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
```

#### 2.2  For Windows (Certificate)

```bash
cd ./configuration/infrastructure/onpremise_testing/secrets

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


### 3. Add your First Linux Server

#### 3.1 Configure your server 

Create a directory under your infrastructure `./configuration/infrastructure/onpremise_testing` with your server name:

```bash
mkdir ./configuration/infrastructure/onpremise_testing/srv01
```

 Create an empty variable.yml inside the new created directory:
```bash
touch ./configuration/infrastructure/onpremise_testing/srv01/variables.yml
```

Add at the below parameter into your variables.yml file:

   - ansible_user: Username that will be allowed to connect to the Linux server with the declared sshkey

```yaml
# File ./configuration/infrastructure/onpremise_testing/srv01/variables.yml
hostname: srv01
ansible_user: ansible
host_ip_access: private_ip
private_ip:
   mode: manual
   ip: 192.168.222.111
```

#### 3.2 Give SSH Access to your server 

Keep in mind that Ansible controller (aka as our YaK container) must have ssh access with a user allowed to sudo. 
In this example, we have a user named ansible and added sudo for it. 

No we have to exchange ssh key to make the connection from YaK to the VM password-less:

```bash
ssh-copy-id ansible@192.168.222.111
```

#### 3.3 Test Ansible connection to the Linux server 

```bash
ansible -m ping onpremise_testing/srv01
````

### 4. Add your First Windows Server

#### 4.1 Configure your server 

Create a directory under your infrastructure `./configuration/infrastructure/onpremise_testing` with your server name:

```bash
mkdir ./configuration/infrastructure/onpremise_testing/srvwin01
```

Create an empty variable.yml inside the new created directory:
```bash
touch ./configuration/infrastructure/onpremise_testing/srvwin01/variables.yml
```

Add at the below parameter into your variables.yml file:

   - ansible_user: Username that will be allowed to connect to the Windows server with the declared certkey

```yaml
# File ./configuration/infrastructure/onpremise_testing/srvwin01/variables.yml
hostname: srvwin01
ansible_user: ansible
host_ip_access: private_ip
private_ip:
   mode: manual
   ip: 192.168.222.111
```

#### 4.2 Give WINRM Access to your server 

Keep in mind that Ansible controller (aka as our YaK container) must have WINRM access to a local Admin user. 
In this example, we have a user named Ansible and added sudo for it. 

1. Adapt the winrm_configuration.ps1 script with your username, password and secret (certkey). you can find this script in the below  folder
[yak/docs/configuration/winrm_configuration.ps1](yak/docs/configuration/winrm_configuration.ps1)

2. Open powershell.exe (64x) as administrator on your windows server
3. Copy and past the winrm_configuration.ps1 and then run it in your powershell session
4. Test your connection with the next command

```bash
$ ansible onpremise_testing/srvwin01 -m win_ping
onpremise_testing/srvwin01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

#### 4.3 Test Ansible connection to the Windows server 

```bash
ansible onpremise_testing/srvwin01 -m win_ping
````





