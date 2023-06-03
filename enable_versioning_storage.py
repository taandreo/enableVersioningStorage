from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ManagementLockClient
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--subscriptionId", required=True, type=str, help="Subscription Id where the storage account is located")
parser.add_argument("-g", "--group", required=True, type=str, help="Subscription Id where the storage account is located")
parser.add_argument("-n", "--name", required=True, type=str, help="Storage account name")

args = parser.parse_args()

def main():
    enable_versioning(args.subscriptionId, args.group, args.name)
    enable_lock(args.subscriptionId, args.group, args.name)

def enable_versioning(sub_id, group, storage):
    cred = DefaultAzureCredential()
    storage_client = StorageManagementClient(cred, sub_id)
    properties = storage_client.blob_services.get_service_properties(group, storage)
    # Enable versioning
    properties.is_versioning_enabled = True
    # Enable change feed
    # Change feed keep track of create, modification, and delete changes to blobs.
    properties.change_feed.enabled = True
    properties.change_feed.retention_in_days = 30
    # Enables soft delete for containers
    properties.container_delete_retention_policy.enabled = True
    properties.container_delete_retention_policy.days = 30
    # Enables soft delete for blobs
    properties.delete_retention_policy.enabled = True
    properties.delete_retention_policy.days = 30
    # Enables point in time restore for containers
    properties.restore_policy.enabled = True
    properties.restore_policy.days = 29

    storage_client.blob_services.set_service_properties(group, storage, parameters=properties)

def enable_lock(sub_id, group, storage):
    cred = DefaultAzureCredential()
    lock_client = ManagementLockClient(cred, sub_id)
    note = "This storage account is used to hold several terraform states objects, and cannot be deleted"
    lock_object = lock_client.management_locks.models.ManagementLockObject(level="CanNotDelete", notes=note)
    lock_client.management_locks.create_or_update_at_resource_level(group,
        resource_provider_namespace="Microsoft.Storage", parent_resource_path="",
        resource_type="storageAccounts", resource_name=storage, lock_name="CanNotDeleteLock", 
        parameters=lock_object)

main()