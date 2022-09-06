## Secrets management

A default secrets directory must exist under./configuration/infrastructure
Where you must create or upload default keys (private and public key), this key will be used to connect the deployed server

If you want to create keys in the current directory, only execute **gen_secret**

```
mkdir ./configuration/infrastructure/secrets
cd ./configuration/infrastructure/secrets
gen_secret

yak@68053b883b16:~/yak/configuration/infrastructure/secrets$ ls -l
total 8
-rw------- 1 yak yak 3243 Sep  6 16:06 sshkey
-rw-r--r-- 1 yak yak  742 Sep  6 16:06 sshkey.pub
```

- If for all YaK deployments the same key is used, the default secrets files are only needed
- If each environment will use its own keys, the secrets must be created at each component level
- If each server will use its own keys, the secrets must be created under each server level


### Create a "secrets" directory at the environment level

```
mkdir ./configuration/infrastructure/aws_testing/secrets
cd ./configuration/infrastructure/aws_testing/secrets
gen_secret
```

### Create a "secrets" directory at the server level

```
mkdir ./configuration/infrastructure/aws_testing/srv01/secrets
cd ./configuration/infrastructure/aws_testing/srv01/secrets
gen_secret
```

### Create your secret files manualy

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
    "ansible_ssh_private_key_file": "/workspace/yak/configuration/infrastructure/aws_testing/secrets/sshkey",
    "ansible_ssh_public_key_file": "/workspace/yak/configuration/infrastructure/aws_testing/secrets/sshkey.pub",
    "ansible_user": "ec2-user",
. . .
. . .
}
```
