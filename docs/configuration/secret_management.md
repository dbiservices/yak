## Secrets management
A folder is created for the secrets in the created environement. The customer's private key and public key are stored there in order to connect to AWS.
- If every VirtualMachine is to use the same key, the secret is only created at the environement level
- If each VirtualMachine is to use its own keys, the secrets are created under each server directory

### Create secret directory at the environment level
```
mkdir ~/yak/configuration/infrastructure/aws_testing/secret
```

### Create secret directory at the VirtualMachine level
```
mkdir ~/yak/configuration/infrastructure/aws_testing/srv01/secret
```

### Create your secret files 
The corresponding private/public keys are then stored there. Here is an example of how new keys can be created
```
ssh-keygen -b 4096 -m PEM -t rsa -f ${secret_home}/sshkey -q -N ""
chmod 600 for private key
```

### Test your inventory after having updated all parameters

```
dbi@3f2794bb53e4:~/GIT/yak$ ansible-inventory --graph
@all:
  |--@aws_testing:
  |  |--aws_testing/srv01
  |--@servers:
  |  |--aws_testing/srv01
  |--@ungrouped:

dbi@3f2794bb53e4:~/GIT/yak$ ansible-inventory --host aws_testing/srv01
{
    "ami_id": "ami-07e51b655b107cd9b",
    "ansible_host": "172.21.9.156",
    "ansible_ssh_private_key_file": "/home/dbi/GIT/yak/configuration/infrastructure/aws_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/home/dbi/GIT/yak/configuration/infrastructure/aws_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
```

