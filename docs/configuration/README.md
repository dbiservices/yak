## Yak Core Ansible Inventory configuration

[[_TOC_]]

### Inventory parsing

- The inventory will only parse the configuration files available under the directory ./configuration/infrastructure
- Per default this directory is empty
- We made you some provider and host templates available under configuration/infrastructure_sample that can be copied and adapted

### Inventory structure

The YaK Core as it's own Ansible dynamic inventory structure, which respect the below structure

```
configuration/
│
├── infrastructure
│   ├── {infrastructure_name_1}
│   │   ├── variables.yml
│   │   ├── {server_name}
│   │   │   ├── variables.yml
│   │   │   └── {component}
│   │   │       └── variables.yml
│   │   ├── {server_name}
│   │   │   ├── variables.yml
│   │   │   └── {component}
│   │   │       └── variables.yml
│   │   └── ...
│   │
│   └── {infrastructure_name_2}
│       └── ...
│
├── infrastructure_sample
│   └── aws
│       ├── variables.yml
│       ├── srv-linux-test-01
│       │   ├── variables.yml
│       │   └── COMP
│       │       └── variables.yml
│       ├── srv-win-test-01
│       │   ├── variables.yml
│       │   └── COMP
│       │       └── variables.yml
│       └── ...
├── templates
    |-- linux
    |   `-- storage
    |       |-- oracle_instance.yml
    |       |-- postgresql_instance.yml
    |       `-- sqlserver_instance.yml
    `-- windows
        `-- storage
            `-- sqlserver_instance.yml
```

### Create a new infrastructure

[Go to the documentation.](infrastructure.md)

### Create your infrastructure/server secrets

[Go to the documentation.](secret_management.md)

### Cloud Provider Authentification

[Go to the documentation.](cloud_authentication.md)

### Create servers and deploy storage configuration

[Link to ../servers/README.md](../servers.md)
