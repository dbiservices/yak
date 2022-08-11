# Servers

 Take care ! All below playbooks must be executed from the yak home directory /workspace/yak

- [Guidance of the playbooks structure](#guidance-of-the-playbooks-structure)
  - [Server](#server)
- [Work per group](#work-per-group)
  - [Deploy all instances](#deploy-all-instances)
  - [Deploy requirments only all instances](#deploy-requirments-only-all-instances)
  - [Remove all instances](#remove-all-instances)
- [Deploy Instance for a specific {provider:aws,azure,oci}](#Deploy-Instance-for-a-specific-{provider:aws,azure,oci})
  - [Linux](#linux)
    - [Deploy the instance](#deploy-the-instance)
    - [Deploy requirements only](#deploy-requirements-only)
    - [Stop the instance](#stop-the-instance)
    - [Start the instance](#start-the-instance)
    - [Patch the instance](#patch-the-instance)
    - [Remove the instance](#remove-the-instance)
  - [Windows](#windows)
    - [Deploy the instance](#deploy-the-instance-1)
    - [Deploy requirements only](#deploy-requirements-only-1)
    - [Stop the instance](#stop-the-instance-1)
    - [Start the instance](#start-the-instance-1)
    - [Remove the instance](#remove-the-instance-1)

## Guidance of the playbooks structure

### Server

Playbooks to deploy/change or decommission of the servers

```
servers/deploy.yml -e target=aws_yak_test/srv-linux-test-01
                 change.yml ...
                 decommission.yml -e target=aws_yak_test/srv-linux-test-01

server/change.yml
	0 - Crosscheck attributes vs reality
	1 - Update attribute of component
	2 - Apply (-tag <PRE|EXEC|POST|ROLLBACK>`
```

## Work per group

### Deploy all instances

```bash
ansible-playbook \
servers/deploy.yml \
-e target=servers
```

### Deploy requirments only all instances

```bash
ansible-playbook \
servers/deploy.yml \
-e target=servers
```

### Remove all instances

```bash
ansible-playbook \
servers/decommission.yml \
-e target=servers
```

## Deploy Instance for a specific {provider:aws,azure,oci}

### Linux

#### Deploy the instance

```bash
ansible-playbook \
servers/deploy.yml \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```

```bash
## Test
ansible -m ping {provider}_yak_test/srv-linux-test-01
```


#### Deploy server only eithout the requirements

```bash
ansible-playbook \
servers/deploy.yml \
--tag=server \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```

#### Deploy requirements only

```bash
ansible-playbook \
servers/deploy.yml \
--tag=component_requirements \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```

#### Stop the instance

```bash
ansible-playbook \
servers/stop.yml \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```

#### Start the instance

```bash
ansible-playbook \
servers/start.yml \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```

#### Patch the instance

```bash
ansible-playbook \
servers/patch.yml \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```
#### Remove the instance

```bash
ansible-playbook \
servers/decommission.yml \
-e target={provider}_yak_test/srv-linux-test-01 \
-e debug=true
```

### Windows

#### Deploy the instance

```bash
ansible-playbook \
servers/deploy.yml \
-e target={provider}_yak_test/srv-win-test-01 \
-e debug=true
```

```bash
## Test
ansible -m win_ping aws_yak_test/srv-win-test-01
```

#### Deploy requirements only

```bash
ansible-playbook \
servers/deploy.yml \
--tag=component_requirements \
-e target={provider}_yak_test/srv-win-test-01 \
-e debug=true
```

#### Stop the instance

```bash
ansible-playbook \
servers/stop.yml \
-e target={provider}_yak_test/srv-win-test-01 \
-e debug=true
```

#### Start the instance

```bash
ansible-playbook \
servers/start.yml \
-e target={provider}_yak_test/srv-win-test-01 \
-e debug=true
```

#### Remove the instance

```bash
ansible-playbook \
servers/decommission.yml \
-e target={provider}_yak_test/srv-win-test-01 \
-e debug=true
```
