# Setup YaK

## Requirements 

To use Yak in your environment the below requirement must be done 

  - container management software as docker-cli must be installed and running
  - local storage must exist to make your local yak repository available
  - internet access must exist to download the container

## Contribution

  - pull the Yak Community container registry.gitlab.com/yak4all/yak:latest to your workstation
  ```
  docker pull registry.gitlab.com/yak4all/yak:latest
  ```

  - Define a local storage with the variable ${MY_LOCAL_YAK_DIR} 
  ```
  export MY_LOCAL_YAK_DIR=$HOME/yak
  ```

  - Clone the Yak repository in your $HOME directory 
  ```
  cd $HOME
  git clone git@gitlab.com:yak4all/yak.git
  ```

  - Start the container with the below command 
```
docker run -it --rm -e YAK_ENABLE_SUDO=true --name yak --pull always -v ${HOME}/.ssh:/workspace/.ssh -v ${MY_LOCAL_YAK_DIR}:/workspace/yak registry.gitlab.com/yak4all/yak:latest bash
```


   If it works you should be inside the container with the Yak repository available for contribution

```
docker run -it --rm -e YAK_ENABLE_SUDO=true --name yak --pull always -v ${HOME}/.ssh:/workspace/.ssh -v ${MY_LOCAL_YAK_DIR}:/workspace/yak registry.gitlab.com/yak4all/yak:latest bash

INFO: type 'yakhelp' to display the help of YAK

yak@d915a92de516:~/yak$ aig
@all:
  |--@demo_aws:
  |  |--demo_aws/linux
  |  |--demo_aws/linux/ORA
  |--@oracle_instance:
  |  |--demo_aws/linux/ORA
  |--@servers:
  |  |--demo_aws/linux
  |--@ungrouped:
yak@d915a92de516:~/yak$
```

## Appendix 


## License

GNU General Public License v3.0 or later
See COPYING to see the full text.








### Clone yak repo from dbi gitlab

 Create ssh key and store public key in dbi gitlab
```bash
ssh-keygen
cat /home/<user>/.ssh/id_rsa.pub
```
 Copy public key and import into dbi gitlab (Edit Profile / ssh Keys / add key)

create GIT directory and  variables for DBI YAK Environment in .profile file
```bash
mkdir -p ~ GIT
echo "export DBI_YAK_HOME=$HOME/GIT/yak" >> ~/.bashrc
echo "export DBI_GIT_HOME=$HOME/GIT" >> ~/.bashrc
cd
. .bashrc
```

ForMacOs .bashrc must be replaced to .bash_profile

Now perform git clone

```bash
cd $DBI_GIT_HOME
git clone git@gitlab.com:dbiservices/yak/yak.git
```

Add the hook script, that will update the permission of the sshkey files and re-excute a pull to update the file permission

```bash
cd yak
git config --local core.hooksPath .githooks/
git pull git@gitlab.com:dbiservices/yak/yak.git
```

This message must be displayed after the pull

```bash
hooks/post-merge: executing: ./generate_keys.sh set-permissions-only
```

### pull docker image with yak

```bash
sudo docker pull public.ecr.aws/dbi-services/dbi-dev:latest
```

```bash
docker images
REPOSITORY                            TAG       IMAGE ID       CREATED       SIZE
public.ecr.aws/dbi-services/dbi-dev   latest    5fa2f5baf66c   5 hours ago   1.74GB
```

### create alias to start docker daemon and docker container

-- Linux and Windows WLS
```bash
echo "alias docker_start='sudo /etc/init.d/docker start' >> ~/.bashrc
echo "alias yak='sudo docker run -it --rm --name dbi_dev -v $DBI_YAK_HOME:/workspace/yak -v $HOME/.ssh:/workspace/.ssh -e YAK_DEV_UID=$(id -u) -e YAK_DEV_GID=$(id -g) public.ecr.aws/dbi-services/dbi-dev:latest bash'" >> ~/.bashrc
cd
. .bashrc
```

-- MacOs
```bash
echo "alias yak='docker run -it --rm --name dbi_dev -v $DBI_YAK_HOME:/workspace/yak -v $HOME/.ssh:/workspace/.ssh -e YAK_DEV_UID=$(id -u) -e YAK_DEV_GID=$(id -g) public.ecr.aws/dbi-services/dbi-dev:latest bash'" >> ~/.bashrc
cd
. .bash_profile
```

### start docker container
Now we can start the docker container with the alias "yak" and test if it's working

```bash
yak
#OUTPUT should be like this
INFO: Creating group dbi => groupadd -g 1000 dbi
INFO: Creating user dbi  => useradd -u 1000 -m -g dbi -s /bin/bash dbi

# ls should working and you should see the files
dbi@8db9e9c2ea2f:~/yak$ ls
CONTRIBUTION.md  README.md  ansible.cfg  collections  configuration  generate_keys.sh  git_repos.sh  install  inventory  playbooks  requirements.yml  roles

```
Gratulation you have successfully installed yak environment! :)

### Appendix : MacOs and Docker Destkop

MacOS has some times an issue with the storage mapping (workaround with a docker volume)

```bash
docker volume create --driver=local --name yak --opt o=bind --opt device=$HOME/GIT/yak --opt type=local
docker run -it -u dbi --rm --name dbi_dev -v yak:/home/dbi/GIT/yak public.ecr.aws/dbi-services/dbi-dev:latest
```

And the Alias for an automatic execution

```bash
alias yak='docker run -it --rm --name dbi_dev -v yak:/workspace/yak -v $HOME/.ssh:/workspace/.ssh -e YAK_DEV_UID=$(id -u) -e YAK_DEV_GID=$(id -g) public.ecr.aws/dbi-services/dbi-dev:latest bash'
```

For the Mac users the local group must be a local group and the "staff" group
```bash
DBI-LT-HER2:GIT her$ ls -l
drwx------  18 her  DBI-SERVICES\Domain Users  576 Mar 17 14:25 yak`
```

### Test your container

``` bash
dbi_yak@26b59d7acd54:~/yak$ ansible --version
[DEPRECATION WARNING]: Ansible will require Python 3.8 or newer on the controller starting with Ansible 2.12. Current version: 3.7.3
(default, Jan 22 2021, 20:04:44) [GCC 8.3.0]. This feature will be removed from ansible-core in version 2.12. Deprecation warnings can
be disabled by setting deprecation_warnings=False in ansible.cfg.
ansible [core 2.11.1]
  config file = /home/dbi_yak/GIT/ansible.cfg
  configured module search path = ['/home/dbi_yak/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.7/dist-packages/ansible
  ansible collection location = /home/dbi_yak/GIT/collections
  executable location = /usr/local/bin/ansible
  python version = 3.7.3 (default, Jan 22 2021, 20:04:44) [GCC 8.3.0]
  jinja version = 3.0.1
  libyaml = True
```

### Clone the Ansible Roles (Inside the container)

This script currently only run on Linux, under Windows you will get file format issues

```bash
./git_repos.sh
```

