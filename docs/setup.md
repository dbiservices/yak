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

FYI : The YaK Core container will including the pulling from the Yak Env Container `registry.gitlab.com/yak4all/yakenv:1.0.0` <br>
This container contains all necessary software used by YaK Core <br>

[Here are more details](https://gitlab.com/yak4all/yakenv/-/blob/main/Dockerfile) about the used dockerfile

## 2. Run the container

Define a local directory with the variable `${MY_LOCAL_CONFIGURATION_DIR}`:

```bash
export MY_LOCAL_CONFIGURATION_DIR=$HOME/yak/inventory
mkdir -p ${MY_LOCAL_CONFIGURATION_DIR}
```

Start the container with the below command:

```bash
docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure -e YAK_DEV_UID=$(id -u) -e YAK_DEV_GID=$(id -g) registry.gitlab.com/yak4all/yak:stable bash
```

If it worked well, you should be inside the container with the YaK Software configured.

```
$ docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure -e YAK_DEV_UID=$(id -u) -e YAK_DEV_GID=$(id -g) registry.gitlab.com/yak4all/yak:stable bash
[...]
yak@d47a98f30c99:~/yak$ ansible-inventory --graph
@all:
  |--@ungrouped:
yak@d47a98f30c99:~/yak$ 
```

## 3. Appendix

You want to allow sudo as user ROOT in the container, below parameter must be added in the "docker run" command

```
-e YAK_ENABLE_SUDO=true
```

