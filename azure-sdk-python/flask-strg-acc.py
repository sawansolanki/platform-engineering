import os
from azure.common.credentials import ServicePrincipalCredentials
from flask import Flask, request , render_template
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, SkuName, Sku, Kind

app = Flask(__name__)

subscription_id = os.environ["subscription_id"]
client_id = os.environ["client_id"]
secret = os.environ["secret"]
tenant = os.environ["tenant"]

credentials = ClientSecretCredential(
        tenant_id=tenant,
        client_id=client_id,
        client_secret=secret
    )

client = ResourceManagementClient(credentials, subscription_id)
# Variable configuration
# Resource Group Configuration

@app.route('/createstrg')
def CreateStorage():

    resource_group_name = str(request.args.get('rgname'))
    location = str(request.args.get('location', default='eastus'))
    storageaccountname = str(request.args.get('storageaccountname'))
    # Create Resource Group
    parameters = {"location" : location}
    client.resource_groups.create_or_update(resource_group_name, parameters)

    params = {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": location,
            "isHnsEnabled": True,
            "encryption": {
                "services": {
                "file": {
                    "key_type": "Account",
                    "enabled": True
                },
                "blob": {
                    "key_type": "Account",
                    "enabled": True
                }
                },
                "key_source": "Microsoft.Storage"
            },
            "minimum_tls_version": "TLS1_2",
            "tags": {
                "key1": "value1",
                "key2": "value2"
            }
            }
    # Create Azure Storage Account
    storage_account_param =  StorageAccountCreateParameters(sku=Sku(name=SkuName.standard_ragrs), kind="StorageV2", location = location)
    storage_client = StorageManagementClient(credentials, subscription_id)
    storage_async_operation = storage_client.storage_accounts.begin_create(resource_group_name, storageaccountname, params)
    storage_account = storage_async_operation.result()
    return "Storage account created successfully!"

if __name__ == "__main__":
    app.run(debug=True)
