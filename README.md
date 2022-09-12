# YaK

Get complete control of your hybrid cloud infrastructure with very few expertise. YaK deploys and configures your servers across various public cloud providers and/or on-premise in the same predictable way.

YaK Core is backed by [dbi services](https://www.dbi-services.com). Start free with an open-source license and extend your powers anytime with components to operate third-party software: Oracle, PostgreSQL, etc. More information on https://www.dbi-services.com/en/yak/components.

## Principles

The YaK is based on the following principles:

- **No lock-in:** The YaK Core is, and will stay entirely open source.
- **Extensibility:** add support for any cloud providers.
- **Modularity:** add components to operate any third-party software (Oracle, PostgreSQL, etc.).
- **Simplicity:** most effortless IT cross cloud provider automation system.
- **Powerfulness:** automate your operations in parallel on cloud providers such as AWS, Azure, and OCI.
- **Maintainability:** based on entirely Ansible and on Python if no Ansible native support available.

## Setup a Demo env.

Access our YaK Core demo environment to get a straightforward and fast introduction! <br>
Try it, to see how it works in real life.

| Steps                                                        | 
| ----------------------------------------------------------- |
|  Open https://yakdemo.dbi-services.com in a Web broswer  (Recommendation: Google Chrome)         |
|  Set Username: **yak**   and Password: **yak**  and click on **"Sign in"**   | 
| <img src="/install/img/YaK_login.png"  width="300" height="250"> |
| Double-click on **"Yak Demo"** on the top-left corner and enter **"startdemo aws"** |
| <img src="/install/img/YaK_demo.png" width="600" height="300">   |

## Setup your own Yak cloud infrastructure 

You want to install and configure Yak Core for your own Cloud provider environments, then follow the below corresponding cloud provider "Setup Instructions"

###  requirements

- Container management software (e.g., docker).
- Internet access to download the container.

### 1. Get the container

Pull the YaK Core container `registry.gitlab.com/yak4all/yak:stable` to your workstation:

```bash
docker pull registry.gitlab.com/yak4all/yak:latest
```

**FYI:** The YaK Core container will include the pulling from the Yak Env
Container `registry.gitlab.com/yak4all/yakenv:1.0.0`. This container contains
the required packages used by YaK Core.

[Here are more details](https://gitlab.com/yak4all/yakenv/-/blob/main/Dockerfile) about the used Docker file.

### 2. Run the container

Define a local directory with the variable `${MY_LOCAL_CONFIGURATION_DIR}`:

```bash
export MY_LOCAL_CONFIGURATION_DIR=$HOME/yak
mkdir -p ${MY_LOCAL_CONFIGURATION_DIR}
```

Start the container with the below command:

```bash
docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash
```

If it worked well, you should be inside the container with the YaK software configured:

```
$ docker run -it --rm --name yak --pull always -v ${MY_LOCAL_CONFIGURATION_DIR}:/workspace/yak/configuration/infrastructure registry.gitlab.com/yak4all/yak bash
[...]
yak@d47a98f30c99:~/yak$ ansible-inventory --graph
@all:
  |--@ungrouped:
yak@d47a98f30c99:~/yak$
```

### 3. Declare your infrastructure

You want to configure Yak Core for your own Cloud provider environments, then follow the below corresponding cloud provider "Setup Instructions"

- [Amazon AWS Quickstart Instructions](docs/quickstart_aws.md)
- [Microsoft Azure Quickstart Instructions](docs/quickstart_azure.md)
- [Oracle OCI Quickstart Instructions](docs/quickstart_oci.md)

## Contribute

You are more than welcome to give us your feedback.
We hope to welcome many of your here to use and enhance the YaK Core package with new cloud providers and features :-).

Please see [Contribution instructions](docs/contribution.md)

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.

