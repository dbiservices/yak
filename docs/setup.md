# Setup

## Minimum requirements

- Container management software (e.g. docker).
- Local directory must exist to map your configuration.
- Internet access to download the container.

## 1. Get the container

Pull the YaK Core container `registry.gitlab.com/yak4all/yak:stable` to your workstation:

```bash
docker pull registry.gitlab.com/yak4all/yak:stable
```

FYI : The YaK Core container will including the pulling from the Yak Env Container `registry.gitlab.com/yak4all/yakenv:stable` <br>
This container contains all necessary software used by YaK Core <br>

[Here are more details](https://gitlab.com/yak4all/yakenv/-/blob/main/Dockerfile) about the used dockerfile

## 2. Run the container

Generate the below script which will create 
 - The required local persistant directories 
 - The container run script 
 - An alias "yak" that you can to execute your container

```bash
cat << EOF > $HOME/yak.sh

export MY_LOCAL_INFRASTRUCTURE_DIR=${HOME}/yak/infrastructure
export MY_LOCAL_COMPONENTS_DIR=${HOME}/yak/components
export MY_LOCAL_COMPONENT_TYPES_DIR=${HOME}/yak/component_types

echo  "my dir is : \$MY_LOCAL_INFRASTRUCTURE_DIR"

mkdir -p \$MY_LOCAL_INFRASTRUCTURE_DIR
mkdir -p \$MY_LOCAL_COMPONENTS_DIR
mkdir -p \$MY_LOCAL_COMPONENT_TYPES_DIR

docker run -it --rm --name yak --pull always \
           -v \${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure \
           -v \${MY_LOCAL_COMPONENTS_DIR}:/workspace/yak/configuration/components \
           -v \${MY_LOCAL_COMPONENT_TYPES_DIR}:/workspace/yak/component_types \
           -e YAK_DEV_UID=$(id -u) -e YAK_DEV_GID=$(id -g) \
           registry.gitlab.com/yak4all/yak:stable bash
EOF

chmod +x $HOME/yak.sh
alias yak=$HOME/yak.sh
echo "alias yak=$HOME/yak.sh" >> $HOME/.bash_profile
```

Execute you yak alias and if it worked well, you should be inside the container with the YaK Software configured.
```
$ yak 
yak@d47a98f30c99:~/yak$ ansible-inventory --graph
@all:
  |--@infrastructures:
  |--@ungrouped:
yak@d47a98f30c99:~/yak$ 
```

## 3. Appendix

You want to allow sudo as user ROOT in the container, the parametere below must be added in the "docker run" command

```
-e YAK_ENABLE_SUDO=true
```

