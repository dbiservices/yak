## YaK Core Ansible Inventory configuration

[[_TOC_]]

### Inventory parsing

- The inventory will only parse the configuration files available under the directory ./configuration/infrastructure and ./configuration/components
- Per default the directory ./configuration/infrastructure is empty
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
│   │   ├── {server_name}
│   │   │   ├── variables.yml
│   │   └── ...
│   │
│   └── {infrastructure_name_2}
│       └── ...
│
├── components
│   ├── {component_name_1}
│   │    └── variables.yml
│   └── {component_name_2}
│       └── variables.yml
│
└── infrastructure_sample
    └── aws
        ├── variables.yml
        ├── srv-linux-test-01
        │   ├── variables.yml
        ├── srv-win-test-01
        │   ├── variables.yml
        └── ...

```

### Create a new infrastructure

[Go to the documentation.](infrastructure.md)

### Create your infrastructure/server secrets

[Go to the documentation.](secret_management.md)

### Cloud Provider Authentification

[Go to the documentation.](cloud_authentication.md)

### Create servers and deploy storage configuration

[Link to ../servers/README.md](../servers.md)
