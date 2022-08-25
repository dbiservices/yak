## Yak Ansible Inventory configuration

[[_TOC_]]

### inventory parsing

- the inventory will only parse the configuration files available under the directory ./configuration/infrastructure
- per default this directory is empty
- We made you some provider and host templates available under configuration/infrastructure_sample that can be copied and adapted

### inventory structure

The YaK as it's own Ansible dynamic inventory structure, which respect the below structure

```
configuration/
│
├── infrastructure
│   ├── {environment_name_1}
│   │   ├── variables.yml
│   │   ├── {server_name}
│   │   │   ├── variables.yml
│   │   │   └── {application}
│   │   │       └── variables.yml
│   │   ├── {server_name}
│   │   │   ├── variables.yml
│   │   │   └── {application}
│   │   │       └── variables.yml
│   │   └── ...
│   │
│   └── {environment_name_2}
│       └── ...
│
├── infrastructure_example
│   └── aws_yak_test
│       ├── variables.yml
│       ├── srv-linux-test-01
│       │   ├── variables.yml
│       │   └── ORA
│       │       └── variables.yml
│       ├── srv-ol8-ora
│       │   ├── variables.yml
│       │   └── CDB01
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

### Create a New environment

[Link to NEW_ENVIRONMENT.md](doc/NEW_ENVIRONMENT.md)

[example](https://gitlab.com/yak4all/yak/-/blob/main/configuration/README.md)


### Create your environment/Virtual Machine secrets

[Link to SECRET_MANAGEMENT.md](doc/SECRET_MANAGEMENT.md)

### Cloud Provider Authentification

[Link to CLOUD_AUTHENTIFICATION.md](doc/CLOUD_AUTHENTIFICATION.md)

### Create Virtual Machine and storage configuration

[Link to ../servers/README.md](../servers/README.md)

### Create your component (database)

- [Link to Oracle Instance](https://gitlab.com/dbiservices/yak/yak_components/oracle_instance/-/blob/main/README.md)
- [Link to PostgreSQL Instance](https://gitlab.com/dbiservices/yak/yak_components/postgresql_instance/-/blob/main/README.md)
- [Link to SQLServer Instance ](https://gitlab.com/dbiservices/yak/yak_components/sqlserver_instance/-/blob/main/README.md)

