## Secrets management

A folder is created for the secrets in each infrastructure. The customer's private and public keys are stored there to connect to AWS.

- If all servers will use the same key, the secret is only created at the infrastructure level
- If each server will use its own key, the secrets are created under each server directory

### Create a "secrets" directory at the infrastructure level

```
mkdir ~/yak/configuration/infrastructure/aws_testing/secrets
```

### Create a "secrets" directory at the server level

```
mkdir ~/yak/configuration/infrastructure/aws_testing/srv01/secrets
```

### Create your secret files

The corresponding private/public keys are then stored there. Here is an example of how new keys can be created

```
ssh-keygen -b 4096 -m PEM -t rsa -f ${secret_home}/sshkey -q -N ""
chmod 600 for a private key
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
