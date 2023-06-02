from pathlib import Path
from sys import argv
import os
import boto3
from azure.storage.blob import BlobServiceClient
import oci

# Default variables
target = 'all'
if len(argv) == 2:
    target = argv[1].lower()
temporary_directory = '/tmp'
if "YAK_ARTIFACTS_SYNC_TMP_DIRECTORY" in os.environ:
    temporary_directory = os.getenv('YAK_ARTIFACTS_SYNC_TMP_DIRECTORY')

s3_bucket_name = 'dbi-services-yak-artifacts'
az_blob_service_container = 'yakartifacts'
oci_bucket_name = 'dbi-services-yak-artifacts'


# Clients
s3_client = boto3.client("s3")
s3_bucket = boto3.resource('s3').Bucket(s3_bucket_name)
s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name).get("Contents")

if target == 'all' or target == 'azure':
    az_blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
    az_container_client = az_blob_service_client.get_container_client(container=az_blob_service_container)

if target == 'all' or target == 'oci':
    config = {
        "user": os.getenv('OCI_USER_ID'),
        "key_file": os.getenv('OCI_USER_KEY_FILE'),
        "fingerprint": os.getenv('OCI_USER_FINGERPRINT'),
        "tenancy": os.getenv('OCI_TENANCY'),
        "region": os.getenv('OCI_REGION')
    }
    oci.config.validate_config(config)
    oci_object_storage = oci.object_storage.ObjectStorageClient(config)
    oci_namespace = oci_object_storage.get_namespace().data

# Helpers
def s3_object_already_exists_in_azure(object):
    blob_list = az_container_client.list_blobs()
    for blob in blob_list:
        if object['Key'] == blob.name:
            if object['Size'] == blob.size:
                # Object exists with same size
                return True, True
            else:
                # Object exists with different size
                return True, False
    return False, False

def s3_object_already_exists_in_oci(object):
    oci_objects = oci_object_storage.list_objects(oci_namespace, oci_bucket_name, prefix=object['Key'], fields='name,size')
    if len(oci_objects.data.objects) > 0:
        if object['Key'] == oci_objects.data.objects[0].name:
            if object['Size'] == oci_objects.data.objects[0].size:
                # Object exists with same size
                return True, True
            else:
                # Object exists with different size
                return True, False
    return False, False

# Code
for object in s3_objects:

    print('# Object: [{} byte(s)] {}'.format(object['Size'], object['Key']))
    local_object_name = '{}/{}'.format(temporary_directory, object['Key'])

    if object['Key'][-1] == '/':

        print('# Creating local directory "{}/{}"'.format(temporary_directory, object['Key']))
        Path(local_object_name).mkdir(parents=True, exist_ok=True)

    elif object['Key'][-1] != '/':

        if target == 'all' or target == 'oci':

            object_exists_in_oci, object_has_same_size_in_oci = \
                s3_object_already_exists_in_oci(object)

            if not object_exists_in_oci or (object_exists_in_oci and not object_has_same_size_in_oci):

                print('# Download object to "{}"'.format(local_object_name))
                s3_client.download_file(
                    Bucket=s3_bucket_name,
                    Key=object['Key'],
                    Filename=local_object_name
                )

                if object_exists_in_oci and not object_has_same_size_in_oci:
                    print('# Removing object "{}" in OCI from bucket "{}"'.format(object['Key'], oci_bucket_name))
                    oci_object_storage.delete_object(oci_namespace, oci_bucket_name, object['Key'])

                print('# Uploading object in OCI to bucket "{}" with object name "{}"'.format(oci_bucket_name, object['Key']))
                with open(file=local_object_name, mode="rb") as data:

                    objet = oci_object_storage.put_object(
                            oci_namespace,
                            oci_bucket_name,
                            object['Key'],
                            data
                        )

                print('# Removing local file "{}"'.format(local_object_name))
                Path(local_object_name).unlink()


        if target == 'all' or target == 'azure':

            object_exists_in_azure, object_has_same_size_in_azure = \
                s3_object_already_exists_in_azure(object)

            if not object_exists_in_azure or (object_exists_in_azure and not object_has_same_size_in_azure):

                print('# Download object to "{}"'.format(local_object_name))
                s3_client.download_file(
                    Bucket=s3_bucket_name,
                    Key=object['Key'],
                    Filename=local_object_name
                )

                if object_exists_in_azure and not object_has_same_size_in_azure:
                    print('# Removing object "{}" in Azure from bucket "{}"'.format(object['Key'], az_blob_service_container))
                    az_container_client.delete_blob(object['Key'])

                print('# Uploading object in Azure to bucket "{}" with object name "{}"'.format(az_blob_service_container, object['Key']))
                blob_client = az_blob_service_client.get_blob_client(
                        container=az_blob_service_container, blob=object['Key']
                    )
                with open(file=local_object_name, mode="rb") as data:
                    blob_client.upload_blob(data)

                print('# Removing local file "{}"'.format(local_object_name))
                Path(local_object_name).unlink()
