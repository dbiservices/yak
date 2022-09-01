# Setup YaK

## Requirements 

To use Yak in your environment the below requirement must be done 

  - container management software as docker-cli must be installed and running
  - local storage must exist to make your configuration persistant 
  - internet access must exist to download the container

## Setup

  - pull the Yak Community container registry.gitlab.com/yak4all/yak:latest to your workstation

  ```docker pull registry.gitlab.com/yak4all/yak:latest```

  - Define a local storage with the variable ${MY_LOCAL_CONFIGURATION_DIR} 

  ```export MY_LOCAL_CONFIGURATION_DIR=$HOME/yak```

  - Start the container with the below command 

  ```docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash```

   If it works you should be inside the container with the YaK Software configured

```
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

To get an example how setup a new environment and servers
[example](https://gitlab.com/yak4all/yak/-/blob/main/configuration/README.md)

## Appendix 


## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
