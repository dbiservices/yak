# Servers

**Note:** Playbooks must be executed from the YaK home directory /workspace/yak

- [Deploy the server](#deploy-the-server)
- [Deploy server only without the requirements](#deploy-server-only-without-the-requirements)
- [Deploy requirements only](#deploy-requirements-only)
- [Stop the server](#stop-the-server)
- [Start the server](#start-the-server)
- [Patch the server](#patch-the-server)
- [Remove the server](#remove-the-server)

## Deploy the server

```bash
ansible-playbook \
servers/deploy.yml \
-e target=<infrastructure>/<server> \
-e debug=true
```

```bash
ansible -m ping <infrastructure>/<server>     # Test Linux
ansible -m win_ping <infrastructure>/<server> # Test Windows
```

## Deploy server only without the requirements

```bash
ansible-playbook \
servers/deploy.yml \
--tag=server \
-e target=<infrastructure>/<server> \
-e debug=true
```

## Deploy requirements only

```bash
ansible-playbook \
servers/deploy.yml \
--tag=requirements \
-e target=<infrastructure>/<server> \
-e debug=true
```

## Stop the server

```bash
ansible-playbook \
servers/stop.yml \
-e target=<infrastructure>/<server> \
-e debug=true
```

## Start the server

```bash
ansible-playbook \
servers/start.yml \
-e target=<infrastructure>/<server> \
-e debug=true
```

## Patch the server

```bash
ansible-playbook \
servers/patch.yml \
-e target=<infrastructure>/<server> \
-e debug=true
```
## Remove the server

```bash
ansible-playbook \
servers/decommission.yml \
-e target=<infrastructure>/<server> \
-e debug=true
```

