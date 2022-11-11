from pathlib import Path
import os
import boto3
from azure.storage.blob import BlobServiceClient

# Default variables
temporary_directory = '/tmp'
if "YAK_ARTIFACTS_SYNC_TMP_DIRECTORY" in os.environ:
    temporary_directory = os.getenv('YAK_ARTIFACTS_SYNC_TMP_DIRECTORY')

s3_bucket_name = 'dbi-services-yak-artifacts'
az_blob_service_container = 'yakartifacts'


# Clients
s3_client = boto3.client("s3")
s3_bucket = boto3.resource('s3').Bucket(s3_bucket_name)
s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name).get("Contents")
az_blob_service_client = BlobServiceClient.from_connection_string(
                            os.getenv('AZURE_STORAGE_CONNECTION_STRING')
                        )
az_container_client = az_blob_service_client.get_container_client(container=az_blob_service_container)

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


# Code
for object in s3_objects:

    print('# Object: [{} byte(s)] {}'.format(object['Size'], object['Key']))
    local_object_name = '{}/{}'.format(temporary_directory, object['Key'])

    if object['Key'][-1] == '/':

        print('# Creating local directory "{}/{}"'.format(temporary_directory, object['Key']))
        Path(local_object_name).mkdir(parents=True, exist_ok=True)

    elif object['Key'][-1] != '/':

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
