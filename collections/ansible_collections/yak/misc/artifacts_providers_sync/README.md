# Artifacts providers sync

The artifacts synchronization is performed in an automated way through an AWS lambda that triggers when objects are created or deleted from the "dbi-services-yak-artifacts" bucket.

The goal is to set "dbi-services-yak-artifacts" as a source of truth and have the exact same state in azure and oci.

The logic is the following :

- Get all objects metadata from aws "dbi-services-yak-artifacts" bucket as well as azure and oci
- Check if files from AWS exist in other providers. If not, delete them
- Check if files with the same name have the same size. If not, replace them with new version.

## Prepare credentials

### Aws

Use the 3 usual credentials for aws :

```bash
export AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
export AWS_SESSION_TOKEN="<AWS_SESSION_TOKEN>"
```

### Azure credentials

Bot types of credentials can be used for azure, either connection string or service principal, however the service principal is used in the lambda function

#### Using connection string

Get an Azure connection string by following the [documentation here](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=connection-string%2Croles-azure-portal%2Csign-in-azure-cli#authenticate-to-azure-and-authorize-access-to-blob-data).

Then export the connection string in a variable `AZURE_STORAGE_CONNECTION_STRING`:

```bash
export AZURE_STORAGE_CONNECTION_STRING='<yourconnectionstring>'
```

#### Using service principal

An Azure service principal is a security identity used by user-created apps, services, and automation tools to access specific Azure resources.

```bash
export AZURE_CLIENT_ID="" # Application id
export AZURE_TENANT_ID=""
export AZURE_CLIENT_SECRET=""
```

### OCI

Connect to OCI using YaK account

Use oci S3 credentials as following :

```bash
export OCI_ACCESS_KEY_ID='<OCI_ACCESS_KEY_ID>'
export OCI_SECRET_KEY='<OCI_SECRET_KEY>'
```

If you don't have s3 credentials, connect with yak account for artifacts sync; go to "My profile" --> "customer secret keys" and generate a new credential

## AWS lambda

### Run the lambda function manually

The lambda function was created in the dbi-LambdaDeveloper account in aws testing.

Simply go to lambda and select the "synchornize_artifacts" function.

Then, click on "test" to run it manually.

### How to build the lambda

We first need to build the lambda layers. We need to use an amazon linux with python3.12 for building the layers otherwise it won't work.

The reason for this is that some python dependencies require binary dependencies. Those dependencies are built during the pip install and depend on an other dependency "glibc" which is on the system. The glibc version is detected during compile time and set at the moment, thus it won't work when building on different platform as the glibc version used will be different.

To fix the issue we're forced to use the proper amazon linux version for the python version used, see here if you want more detail: <https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html>

Follow the steps to proceed:

Build two layers for following packages : azure-storage-blob and azure-identity

Build docker image in yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/lambda.

This image is needed for creating lambda layers.

Build :
> docker build -t amazon-linux-python:3.12 .

Run it :
> docker run -d amazon-linux-python:3.12

Exec into it :
> docker exec -it <container_id> bash

Run the following for creating layer for storage :

```bash
mkdir python
cd python
pip install azure-storage-blob -t .
cd ..
zip -r azure_storage_layer.zip python/
```

Then delete everything :
> rm -rf python

Repeat for identity layer :

```bash
mkdir python
cd python
pip install azure-identity -t .
cd ..
zip -r azure_identity_layer.zip python/
```

Ctrl-D to disconnect from the container.

Copy the layers to your host :

```bash
docker cp container_id:/var/task/azure_storage_layer.zip .
docker cp container_id:/var/task/azure_identity_layer.zip .
```

Upload those layers into lambda.

Create the function :
The function must use the proper role for fetching azure and oci secrets.
It must have the proper trigger configured to run when the bucket is updated as well.

Use the "sync.py" code for the function.

Set env var "USE_SECRETS_MANAGER" to "1" in aws lambda config for the function.

It now can be runned manually in lambda, or it will be triggered on bucket changes.

## Run the synchronisation manually

### Local temporary directory

The script will by default store one file at a time in the `/tmp` directory.
If you want to change the directory, use the environment variable `YAK_ARTIFACTS_SYNC_TMP_DIRECTORY`.

```bash
export YAK_ARTIFACTS_SYNC_TMP_DIRECTORY="/home/yak/tmp-sync-dir"
```

### Install python3-venv packages

```bash
sudo apt-get install python3-venv
```

### Create a Python environment

This will create a safe Python environment:

```bash
python3 -m venv /tmp/artifacts_providers_sync
source /tmp/artifacts_providers_sync/bin/activate
```

### Install packages

```bash
pip install boto3 azure-storage-blob azure-identity
```

### Run the synchronization

```bash
export AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
export AWS_SESSION_TOKEN="<AWS_SESSION_TOKEN>"
#-- set Azure credentials
export AZURE_CLIENT_ID="" # Application id
export AZURE_TENANT_ID=""
export AZURE_CLIENT_SECRET=""
#-- OCI
export OCI_ACCESS_KEY_ID='<OCI_ACCESS_KEY_ID>'
export OCI_SECRET_KEY='<OCI_SECRET_KEY>'
# Run the script
python3 ~/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py all   # All available providers
python3 ~/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py azure # Azure only
python3 ~/yak/collections/ansible_collections/yak/misc/artifacts_providers_sync/sync.py oci   # OCI only
```
