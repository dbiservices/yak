from pathlib import Path
from sys import argv
import os
import boto3
from botocore.client import Config
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import json

# Variables
## Global
DEFAULT_SYNC_TARGET = "all" # Sync from AWS to all other providers, or choose "oci", "azure"
AWS_SECRETS_MANAGER_SECRETS=["bucketSync/Azure", "bucketSync/OCI"]

## AWS
AWS_S3_BUCKET_NAME = 'dbi-services-yak-artifacts'

## AZURE
AZ_BLOB_SERVICE_CONTAINER = 'yakartifacts'
AZ_STORAGE_ACCOUNT_URL = "https://yakartifacts.blob.core.windows.net"

## OCI
OCI_BUCKET_NAME = 'dbi-services-yak-artifacts'
OCI_REGION = 'eu-zurich-1'
OCI_TENANCY_NAMESPACE = 'zrbhy7g7atj1'
OCI_ENDPOINT_URL = f'https://{OCI_TENANCY_NAMESPACE}.compat.objectstorage.{OCI_REGION}.oraclecloud.com'


# Functions
def get_aws_sec_manager_secrets(secret_name):
    """Sets secrets env variables fetch from aws secrets manager
    """
    secrets_manager_client = boto3.client('secretsmanager', region_name="eu-central-1")    
    try:
        secret_dict = secrets_manager_client.get_secret_value(
            SecretId=secret_name,
        )
    except Exception as e :
        return None
    
    secret_dict = json.loads(secret_dict['SecretString'])
    for key, value in secret_dict.items():
        os.environ[key]=value


def s3_object_already_exists_in_azure(aws_s3_object, az_blob_list):
    for blob in az_blob_list:
        if aws_s3_object['Key'] == blob.name:
            if aws_s3_object['Size'] == blob.size:
                # Object exists with same size
                return True, True
            else:
                # Object exists with different size
                return True, False
    return False, False

def s3_object_already_exists_in_oci(aws_s3_object, oci_s3_objects):
    for oci_s3_object in oci_s3_objects:
        if aws_s3_object['Key'] == oci_s3_object['Key']:
            if aws_s3_object['Size'] == oci_s3_object['Size']:
                # Object exists with same size
                return True, True
            else:
                # Object exists with different size
                return True, False
    return False, False

def get_oci_objects_not_in_aws(aws_s3_objects, oci_s3_objects) -> list[str]:
    oci_s3_objects_names = [ oci_s3_object["Key"] for oci_s3_object in oci_s3_objects ]
    aws_s3_objects_names = [ aws_s3_object["Key"] for aws_s3_object in aws_s3_objects ]
    list_of_objects_to_delete = [ oci_object_name for oci_object_name in oci_s3_objects_names if not oci_object_name  in aws_s3_objects_names ]
    return list_of_objects_to_delete

def get_azure_objects_not_in_aws(aws_s3_objects, az_blob_list) -> list[str]:
    azure_objects_names = [ blob.name for blob in az_blob_list ]
    aws_s3_objects_names = [ aws_s3_object["Key"] for aws_s3_object in aws_s3_objects ]
    list_of_objects_to_delete = [ blob_name for blob_name in azure_objects_names if not blob_name in aws_s3_objects_names ]
    return list_of_objects_to_delete

def lambda_handler(event, context):
    if os.getenv("USE_SECRETS_MANAGER", 0) == "1": #Env var must be 1 in lambda
        for aws_secret in AWS_SECRETS_MANAGER_SECRETS:
            get_aws_sec_manager_secrets(aws_secret)

    TEMP_DOWNLOAD_DIR = os.getenv("YAK_ARTIFACTS_SYNC_TMP_DIRECTORY","/tmp") # Dir that will serve as a buffer to download files from AWS and upload them to other providers
    # S3 credentials for OCI. My profile --> Generate secret key
    OCI_ACCESS_KEY = os.getenv("OCI_ACCESS_KEY_ID")
    OCI_SECRET_KEY = os.getenv("OCI_SECRET_KEY")

    print("Starting synchronization script...")
    print(f"Artifacts download directory : {TEMP_DOWNLOAD_DIR} \n")
    sync_target = DEFAULT_SYNC_TARGET
    if len(argv) == 2:
        sync_target = argv[1].lower()

    # Clients
    aws_s3_client = boto3.client("s3")
    aws_s3_objects = aws_s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET_NAME).get("Contents")

    if sync_target == 'all' or sync_target == 'azure':
        # Acquire a credential object
        credential = DefaultAzureCredential()

        try:
            # Try connecting with serviceprincipal credentials : AZURE_CLIENT_ID, AZURE_TENANT_ID and AZURE_CLIENT_SECRET env variables
            # Or file created with az login
            az_blob_service_client = BlobServiceClient(
                account_url=AZ_STORAGE_ACCOUNT_URL,
                credential=credential)
        except Exception: # Otherwise use connection string if env var is set
            az_blob_service_client = BlobServiceClient.from_connection_string(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

        az_container_client = az_blob_service_client.get_container_client(container=AZ_BLOB_SERVICE_CONTAINER)
        # Get all the list from generator once to increase script speed instead of calling it multiple times
        az_blob_list = list(az_container_client.list_blobs())
        # Delete old objects
        objects_to_delete = get_azure_objects_not_in_aws(aws_s3_objects, az_blob_list)
        if objects_to_delete: print(f"Following objects will be deleted : {objects_to_delete}")
        for obj in objects_to_delete : az_container_client.delete_blob(obj)

    if sync_target == 'all' or sync_target == 'oci':
        oci_s3_client = boto3.client(
            service_name='s3',
            region_name=OCI_REGION,
            aws_access_key_id=OCI_ACCESS_KEY,
            aws_secret_access_key=OCI_SECRET_KEY,
            endpoint_url=OCI_ENDPOINT_URL,
            config=Config(signature_version='s3v4')
        )
        oci_s3_objects = oci_s3_client.list_objects_v2(Bucket=OCI_BUCKET_NAME).get("Contents")
        # Delete old objects
        objects_to_delete = get_oci_objects_not_in_aws(aws_s3_objects, oci_s3_objects)
        if objects_to_delete: print(f"Following objects will be deleted : {objects_to_delete}")
        for obj in objects_to_delete: oci_s3_client.delete_object(Bucket=OCI_BUCKET_NAME, Key=obj)

    # Code
    for aws_s3_object in aws_s3_objects:
        if aws_s3_object['Key'][-1] == '/':
            continue

        # print('# Object: [{} byte(s)] {}'.format(aws_s3_object['Size'], aws_s3_object['Key']))
        local_object_name = f"{TEMP_DOWNLOAD_DIR}/{aws_s3_object['Key']}"
        path = Path(local_object_name)

        # print('# Creating local directory "{}/{}"'.format(TEMP_DOWNLOAD_DIR, aws_s3_object['Key']))
        Path(path.parent.absolute()).mkdir(parents=True, exist_ok=True)


        if sync_target == 'all' or sync_target == 'oci':

            object_exists_in_oci, object_has_same_size_in_oci = \
                s3_object_already_exists_in_oci(aws_s3_object, oci_s3_objects)

            if not object_exists_in_oci or (object_exists_in_oci and not object_has_same_size_in_oci):
                print(f"# Object: [{aws_s3_object['Size']} byte(s)] {aws_s3_object['Key']}")

                print(f'# Download aws s3 object to "{local_object_name}"')
                aws_s3_client.download_file(
                    Bucket=AWS_S3_BUCKET_NAME,
                    Key=aws_s3_object['Key'],
                    Filename=local_object_name
                )

                if object_exists_in_oci and not object_has_same_size_in_oci:
                    print(f"# Removing object \"{aws_s3_object['Key']}\" in OCI from bucket \"{OCI_BUCKET_NAME}\"")
                    # oci_object_storage.delete_object(oci_namespace, OCI_BUCKET_NAME, aws_s3_object['Key'])

                print(f"# Uploading object in OCI to bucket \"{OCI_BUCKET_NAME}\" with object name \"{aws_s3_object['Key']}\"")
                with open(file=local_object_name, mode="rb") as data:
                    oci_s3_client.put_object(Bucket=OCI_BUCKET_NAME, Key=aws_s3_object['Key'], Body=data)

                print(f'# Removing local file "{local_object_name}"\n')
                Path(local_object_name).unlink()


        if sync_target == 'all' or sync_target == 'azure':

            object_exists_in_azure, object_has_same_size_in_azure = \
                s3_object_already_exists_in_azure(aws_s3_object, az_blob_list)

            if not object_exists_in_azure or (object_exists_in_azure and not object_has_same_size_in_azure):

                print(f'# Download aws s3 object to "{local_object_name}"')
                aws_s3_client.download_file(
                    Bucket=AWS_S3_BUCKET_NAME,
                    Key=aws_s3_object['Key'],
                    Filename=local_object_name
                )

                if object_exists_in_azure and not object_has_same_size_in_azure:
                    print(f"# Removing object \"{aws_s3_object['Key']}\" in Azure from bucket \"{AZ_BLOB_SERVICE_CONTAINER}\"")
                    az_container_client.delete_blob(aws_s3_object['Key'])

                print(f"# Uploading object in Azure to bucket \"{AZ_BLOB_SERVICE_CONTAINER}\" with object name \"{aws_s3_object['Key']}\"")
                blob_client = az_blob_service_client.get_blob_client(
                        container=AZ_BLOB_SERVICE_CONTAINER, blob=aws_s3_object['Key']
                    )
                with open(file=local_object_name, mode="rb") as data:
                    blob_client.upload_blob(data)

                print('# Removing local file "{}" \n'.format(local_object_name))
                Path(local_object_name).unlink()

    print("If you don't see any object names in the output, it means everything is already synchronized.")
    print("Synchronization script finished successfully.")

if __name__ == "__main__":
    # If script is called by hand, invoke lambda handler with dummy args
    lambda_handler("","")