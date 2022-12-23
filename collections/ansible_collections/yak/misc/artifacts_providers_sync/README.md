# Artifacts providers sync

Sync artifacts from s3 to other storage providers:

    - One file at a time
    - Skype files that already exists on Azure with the same size

## Local temporary directory

The script will by default store one file at a time in the `/tmp` directory.
If you want to change the directory, use the environment variable `YAK_ARTIFACTS_SYNC_TMP_DIRECTORY`.

```bash
export YAK_ARTIFACTS_SYNC_TMP_DIRECTORY="/home/yak/tmp-sync-dir"
```

## Create a Python environment

This will create a safe Python environment:

```bash
python3 -m venv /tmp/artifacts_providers_sync
source /tmp/artifacts_providers_sync/bin/activate
```

### Install packages

```bash
pip install boto3 azure-storage-blob azure-identity
```

## Credentials

### Aws

```bash
export AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
export AWS_SESSION_TOKEN="<AWS_SESSION_TOKEN>"
```

### Azure

Get an Azure connection string by following the [documentation here](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=connection-string%2Croles-azure-portal%2Csign-in-azure-cli).

Then export the connection string in a variable `AZURE_STORAGE_CONNECTION_STRING`:

```bash
export AZURE_STORAGE_CONNECTION_STRING='<yourconnectionstring>'
```

## Run the synchronisation

```bash
export AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
export AWS_SESSION_TOKEN="<AWS_SESSION_TOKEN>"
export AZURE_STORAGE_CONNECTION_STRING='<yourconnectionstring>'
python3 ~/dbi/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py
```

