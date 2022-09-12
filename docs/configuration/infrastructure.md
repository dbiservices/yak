# Infrastructure sample

YaK Core currently can help you deploying your infrastructure for 3 public Cloud provider as ( OCI, Azure, AWS).
To help you declaring your new infrastructure we provide you a sample directory for each Cloud provider available under ./configuration_sample

```
yak@ccf94de8138f:~/yak/configuration/infrastructure_sample$ ls -l
total 32
drwxr-xr-x 1 yak yak 4096 Sep  6 15:20 aws
drwxr-xr-x 1 yak yak 4096 Sep  6 15:20 azure
drwxr-xr-x 1 yak yak 4096 Sep  6 15:20 oci
drwxr-xr-x 1 yak yak 4096 Sep  6 15:20 secrets
```

# Infrastructure deployment

To help you deploying an infrastructure, we have created a **quickstart** for each cloud provider

....
....
....

# Infrastructure parameter

All parameters defined at the infrastructure level are inherit at the server and component sub level. Therefor don't hesitate to define some default parameters at the infrastructure level. Thus if at the server level no Image ID is provider the default Image from the infrastucture will be used.

# Infrastructure ssh key

It is only mandatory to have global ssk key under ./configuration/infrastructure/secrets which will be inherit for all  infrastructure and server you will create.
But you can create an ssh key directory with his key at each level, which will automatically overwrite the default one.

# Infrastucture Authentification

You can set your permanent credentials for all cloud provider in one sessions, thus you can deploy new infrastructure for each provider without making a new Authentification.





