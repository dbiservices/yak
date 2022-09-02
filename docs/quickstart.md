# Quickstart

## Requirements

- Container management software (e.g. docker).
- Local directory must exist to map your configuration.
- Internet access to download the container.

## Setup

1. pull the Yak Community container `registry.gitlab.com/yak4all/yak:latest` to your workstation:

```bash
docker pull registry.gitlab.com/yak4all/yak:latest
```

2. Define a local storage with the variable `${MY_LOCAL_CONFIGURATION_DIR}`:

```bash
export MY_LOCAL_CONFIGURATION_DIR=$HOME/yak
```

3. Start the container with the below command:

```bash
docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash
```

If it worked well, you should be inside the container with the YaK Software configured.

```bash
$ docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash

INFO: type 'yakhelp' to display the help of YAK

===========================================================

As of demo this environment as some restriction

The servers
       - provisioning allows only instance_type=t3.micro
       - are automatically destroyed after 4h
       - are only reachable from the YaK container
            ssh demo/linux
       - storage size can't be extended

 Disclaimer about usage of YaK

===========================================================
yak@d47a98f30c99:~/yak$ aig
@all:
  |--@ungrouped:
yak@d47a98f30c99:~/yak$
```

## Configuration

Once in the container, you must describe the environment that you wish to begin with.
To get an example of how to set up a new environment and servers, [go to this page](https://gitlab.com/yak4all/yak/-/blob/main/configuration/README.md).

**Note**: This project uses an Ansible dynamic inventory build from the configuration files available in the `./configuration` directory.
You can have a look at the inventory content using the standard `ansible` command:

```bash
ansible-inventory all --graph
```

[Here are more details](https://gitlab.com/yak4all/yak/-/tree/main/collections/ansible_collections/yak/core) about the inventory structure.

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
