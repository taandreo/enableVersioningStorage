# Enable versioning and soft delete options for storage

This script enables some versioning and soft delete options for an storage account and create a NotDelete lock.  

## Install

pip3 install -r requiriments.txt

## Usage

python3 enable_versioning_storage.py -s <sub_id> -g <resource_group> -n <storage_name>