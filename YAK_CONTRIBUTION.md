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
  export MY_LOCAL_YAK_DIR=$HOME/GIT/yak
  ```

  - Clone the Yak repository in your $HOME directory 
  ```
  cd $HOME/GIT
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

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.
