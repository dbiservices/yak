# Artifacts providers sync

Sync artifacts from s3 to other storage providers (Azure and OCI):

    - One file at a time
    - Skype files that already exists on Azure with the same size

Currently directories are not synchronized it must be integrated

## Local temporary directory

The script will by default store one file at a time in the `/tmp` directory.
If you want to change the directory, use the environment variable `YAK_ARTIFACTS_SYNC_TMP_DIRECTORY`.

```bash
export YAK_ARTIFACTS_SYNC_TMP_DIRECTORY="/home/yak/tmp-sync-dir"
```

## Install python3-venv packages

```bash
sudo apt-get install python3-venv
```

## Create a Python environment

This will create a safe Python environment:

```bash
python3 -m venv /tmp/artifacts_providers_sync
source /tmp/artifacts_providers_sync/bin/activate
```

### Install packages

```bash
pip install boto3 azure-storage-blob azure-identity oci
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

### OCI

Then export the variables:

```bash
export OCI_USER_ID='<OCI_USER_ID>'
export OCI_USER_KEY_FILE='<OCI_USER_KEY_FILE>'
export OCI_USER_FINGERPRINT='<OCI_USER_FINGERPRINT>'
export OCI_TENANCY='<OCI_TENANCY>'
export OCI_REGION='<OCI_REGION>'
```

## Run the synchronisation

```bash
export AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
export AWS_SESSION_TOKEN="<AWS_SESSION_TOKEN>"
#-- Azure
export AZURE_STORAGE_CONNECTION_STRING='<yourconnectionstring>'
#-- OCI
export OCI_USER_ID='<OCI_USER_ID>'
export OCI_USER_KEY_FILE='<OCI_USER_KEY_FILE>'
export OCI_USER_FINGERPRINT='<OCI_USER_FINGERPRINT>'
export OCI_TENANCY='<OCI_TENANCY>'
export OCI_REGION='<OCI_REGION>'
python3 ~/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py all   # All available providers
python3 ~/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py azure # Azure only
python3 ~/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py oci   # OCI only
```

