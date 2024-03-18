from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
from azure.mgmt.sql import SqlManagementClient
import os

subscription_id = os.environ["subscription_id"]
client_id = os.environ["client_id"]
secret = os.environ["secret"]
tenant = os.environ["tenant"]

credentials = ClientSecretCredential(
        tenant_id=tenant,
        client_id=client_id,
        client_secret=secret
    )

resource_client = ResourceManagementClient(credentials, subscription_id)

server_name = "sawandataopsserver"
database_name = "sa1database"
resource_group_name = "Paid_RG"
location = "eastus"

sql_client = SqlManagementClient(credentials, subscription_id)

server = sql_client.servers.begin_create_or_update(
    resource_group_name,
    server_name,
    {
        "location": location,
        "administrator_login": "sawanadmin",
        "administrator_login_password": "SawanadAserminpass1@"
    }
).result()

print(f"SQL Server '{server_name}' created successfully.")


database = sql_client.databases.begin_create_or_update(
    resource_group_name,
    server_name,
    database_name,
    {
        "location": location,
        "sku": {
            "name": "S0"
        }
    }
).result()

print(f"Database '{database_name}' created successfully.")
