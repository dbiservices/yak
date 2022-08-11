### Cloud Provider Authentification

#### AWS

For AWS you can authenticate you with the AWS CLI or with the below AWS parameters setting

- temporary keys(valid some hours only)
```
export AWS_ACCESS_KEY_ID="*******"
export AWS_SECRET_ACCESS_KEY="**********"
export AWS_SESSION_TOKEN="***********`
```
- permanent key
```
export AWS_ACCESS_KEY_ID="*******"
export AWS_SECRET_ACCESS_KEY="**********"
```

#### Azure

For Azure you can authenticate you with the az CLI or with the below Azure permanent parameters setting

```
export AZURE_SUBSCRIPTION_ID=****
export AZURE_CLIENT_ID=*****
export AZURE_SECRET=*****
export AZURE_TENANT=*****
```

#### OCI

For Oracle you can authenticate you with the oci CLI or with the below OCI user permanent parameters setting

```
export OCI_USER_ID=****
export OCI_USER_FINGERPRINT=****
export OCI_TENANCY=****
export OCI_REGION=*****
export OCI_USER_KEY_FILE=$FILE_LOCATION
export OCI_USE_NAME_AS_IDENTIFIER=true
```
