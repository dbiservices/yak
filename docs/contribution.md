# Contribution

## Requirements

- Container management software (e.g. docker).
- Local directory must exist to map your configuration.
- Internet access to download the container.

## Setup

1. pull the Yak Core container `registry.gitlab.com/yak4all/yak:latest` to your workstation

```bash
docker pull registry.gitlab.com/yak4all/yak:latest
```

FYI : The YaK Core container will including the pulling from the Yak Env Container `registry.gitlab.com/yak4all/yakenv:1.0.0` <br>
This container contains all necessary softwares used by YaK Core <br>
see here for more information : https://gitlab.com/yak4all/yakenv/-/blob/main/Dockerfile

2. Define a local storage with the variable `${MY_LOCAL_YAK_DIR}`

```bash
export MY_LOCAL_YAK_DIR=$HOME/GIT/yak
```

3. Clone the YaK repository in your $HOME directory

```bash
cd $HOME/GIT
git clone git@gitlab.com:yak4all/yak.git
```

4. Start the container with the below command
```
docker run -it --rm -e YAK_ENABLE_SUDO=true --name yak --pull always -v ${HOME}/.ssh:/workspace/.ssh -v ${MY_LOCAL_YAK_DIR}:/workspace/yak registry.gitlab.com/yak4all/yak:latest bash
```

If it works you should be inside the container with the YaK repository available for contribution

```bash
docker run -it --rm -e YAK_ENABLE_SUDO=true --name yak --pull always -v ${HOME}/.ssh:/workspace/.ssh -v ${MY_LOCAL_YAK_DIR}:/workspace/yak registry.gitlab.com/yak4all/yak:latest bash

INFO: type 'yakhelp' to display the help of YaK

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

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
