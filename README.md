# PYTHON SWAN SDK <!-- omit in toc -->

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/) 
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/swanchain)

## Table Of Contents<!-- omit in toc -->

- [Quickstart](#quickstart)
  - [Installation](#installation)
  - [Get Orchestrator API Key](#get-orchestrator-api-key)
  - [Get Storage API Key](#get-storage-api-key)
  - [Using Swan](#using-swan)
- [A Sample Tutorial](#a-sample-tutorial)
  - [Orchestrator](#orchestrator)
    - [Fetch available instance resources](#fetch-available-instance-resources)
    - [Create and deploy a task](#create-and-deploy-a-task)
    - [Optional: Create and deploy a task with custom instance](#optional-create-and-deploy-a-task-with-custom-instance)
      - [Step 1: Get GPU Selection List](#step-1-get-gpu-selection-list)
      - [Step 2: Define Custom Instance](#step-2-define-custom-instance)
      - [Step 3: Check Custom Instance Availability](#step-3-check-custom-instance-availability)
      - [Step 4: Create Task with Custom Instance](#step-4-create-task-with-custom-instance)
    - [Check information of an existing task](#check-information-of-an-existing-task)
    - [Access application instances of an existing task](#access-application-instances-of-an-existing-task)
    - [Renew an existing task](#renew-an-existing-task)
    - [Terminate an existing task](#terminate-an-existing-task)
  - [Storage](#storage)
    - [Create and Delete Buckets](#create-and-delete-buckets)
    - [Upload Folders](#upload-folders)
    - [Manipulate Files](#manipulate-files)
    - [Get Bucket Information](#get-bucket-information)
- [License](#license)


## Quickstart

This guide details the steps needed to install or update the SWAN SDK for Python. The SDK is a comprehensive toolkit designed to facilitate seamless interactions with the SwanChain API.

### Installation

To use Swan SDK, you first need to install it and its dependencies. Before installing Swan SDK, install Python 3.8 or later and web3.py(==6.20.3).


Install the latest Swan SDK release via **pip**:

```bash
pip install swan-sdk
```

Or install via GitHub:

```bash
git clone https://github.com/swanchain/python-swan-sdk.git
cd python-swan-sdk
pip install .
```

### Get Orchestrator API Key

To use `swan-sdk` Orchestrator service, an Orchestrator API key is required. 

Steps to get an Orchestrator API Key:

- Go to [Swan Chain Console](https://console.swanchain.io/api-keys). Make sure you're under the Mainnet environment.
- Login through MetaMask.
- Click 'Generate API Key'.
- Store your API Key safely, do not share with others.

### Get Storage API Key

To use the `swan-sdk` Multi-Chain Storage (MCS) service, an MCS API key is required. 

Steps to get a MCS API Key:

- Go to [Multi Chain Storage](https://www.multichain.storage/home). Make sure you're under the Mainnet environment.
- Login through MetaMask.
- Click the gear icon on the top right and select 'Setting'.
- Click 'Create API Key'.
- Store your API Key safely, do not share with others.

### Using Swan

To use Swan SDK, you must first import it and indicate which service you're going to use:

```python
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

# create a storage resource, you will need to use an mcs api key
swan_storage = swan.resource(api_key='<MCS_API_KEY>', service_name='Storage')
```


With `Orchestrator` service, you can create and deploy instance applications as an Orchestrator task with the service.

```python
result = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/hello_world',
    wallet_address='<WALLET_ADDRESS>',
    private_key='<PRIVATE_KEY>',
    instance_type='C1ae.small'
)
task_uuid = result['task_uuid']
```

Then you can follow up task deployment information and the URL for running applications.

```python
# Get task deployment info
task_deployment_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_deployment_info.to_dict(), indent=2))

# Get application instances URL
app_urls = swan_orchestrator.get_real_url(task_uuid)
print(app_urls)
```

With the `Storage` service, you can create buckets and upload files to them.

```python
# Create a bucket called 'my-bucket'
swan_storage.create_bucket(bucket_name='my-bucket')

# upload a file to the bucket
swat_storage.upload_file(bucket_name='my-bucket', object_name='my-file', folder_path='my-folder/my-file')
```
## A Sample Tutorial

For more detailed samples, consult [SDK Samples](https://github.com/swanchain/python-sdk-docs-samples).

For detailed description of functions, please check [Key Functions](./docs/key_functions.md).

### Orchestrator

Orchestrator allows you to create task to run application instances to the powerful distributed computing providers network.

#### Fetch available instance resources

Before using Orchestrator to deploy task, it is necessary to know which instance resources are available. Through `get_instance_resources` you can get a list of available instance resources including their `region` information. From the output list, you can choose an `instance_type` by checking the description for the hardware configuration requirements.

```python
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

available_resources = swan_orchestrator.get_instance_resources()
print(available_resources)
```

#### Create and deploy a task

Deploy a simple application with Swan SDK:

```python
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

result = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/hello_world',
    wallet_address='<WALLET_ADDRESS>',
    private_key='<PRIVATE_KEY>',
    instance_type='C1ae.small'
)
task_uuid = result['task_uuid']
# Get task deployment info
task_deployment_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_deployment_info.to_dict(), indent=2))
```

It may take up to 5 minutes to get the deployment result:

```python
# Get application instances URL
app_urls = swan_orchestrator.get_real_url(task_uuid)
print(app_urls)
```
A sample output:

```
['https://krfswstf2g.anlu.loveismoney.fun', 'https://l2s5o476wf.cp162.bmysec.xyz', 'https://e2uw19k9uq.cp5.node.study']
```

It shows that this task has three applications. Open the URL in the web browser you will view the application's information if it is running correctly.


#### Optional: Create and deploy a task with custom instance

Instead of using the pre-defined instance types, you can also define your own instance configurations. 

##### Step 1: Get GPU Selection List

First, retrieve the list of available GPUs using the `get_gpu_selection_list` function to check the available GPU models in certain region.

```python
region = 'all'  # Can be 'all', 'global', or specific regions like 'Quebec-CA'
gpu_list = swan_orchestrator.get_gpu_selection_list(region)
```

This step provides information about which GPUs are available in the specified region.

- `region='all'`: will list all regions for GPU resources with max capacity (the maximum will be aggregated within each available region)
- `region='global'`: will list all GPU resources across worldwide (aggregated within global range)
- `region='Quebec-CA'`: will list all GPU resources in this region

##### Step 2: Define Custom Instance

Define the custom instance with the desired specifications (`cpu`, `memory`, `storage`, `gpu_model`, and `gpu_count` are required; memory and storage units are in gigabytes GB; for these parameters, only integers are acceptable):

```python
custom_instance = {
    "cpu": 2,
    "memory": 2,
    "storage": 5,
    "gpu_model": "NVIDIA 3080",
    "gpu_count": 1
}
```

##### Step 3: Check Custom Instance Availability

Use the `get_custom_instance_result` function to check the price and availability of the custom instance:

```python
region = 'Quebec-CA'  # Specify the desired region
result = swan_orchestrator.get_custom_instance_result(custom_instance, region)
```

This function will return information about whether the custom instance is available and its pricing.


Example response:

```json
{
  "available": true,
  "custom_instance": {
    "cpu": 2,
    "gpu_count": 1,
    "gpu_model": "NVIDIA 3080",
    "memory": 2,
    "region": "Quebec-CA",
    "storage": 5
  },
  "price_expiry_time": "2025-01-20 18:41:52 UTC",
  "price_per_hour": 1.98
}
```

##### Step 4: Create Task with Custom Instance

If the custom instance is available, proceed to create the task with that custom instance:

```python
result: TaskCreationResult = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/MusicGen',
    wallet_address='<WALLET_ADDRESS>',
    private_key='<PRIVATE_KEY>',
    custom_instance=custom_instance
)
```

Note that when providing a `custom_instance`, the `instance_type` parameter is ignored in the task creation process.

By following these steps, you can efficiently select GPUs, check the availability of a custom instance, and create a task using the custom specifications.


#### Check information of an existing task

With Orchestrator, you can check information for an existing task to follow up or view task deployment.

```python
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

# Get an existing task deployment info
task_deployment_info = swan_orchestrator.get_deployment_info(<task_uuid>)
print(json.dumps(task_deployment_info.to_dict(), indent=2))
```

#### Access application instances of an existing task

With Orchestrator, you can easily get the deployed application instances for an existing task.

```python
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

# Get application instances URL
app_urls = swan_orchestrator.get_real_url(<task_uuid>)
print(app_urls)
```

#### Renew an existing task

You can extend task duration before task duration ends by using `renew_task`.

```python
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

swan_orchestrator.renew_task(
    task_uuid=<task_uuid>, 
    duration=3600, # Optional: default 3600 seconds (1 hour)
    private_key=<PRIVATE_KEY>
)
```

#### Terminate an existing task

You can also early terminate an existing task and its application instances. By terminating task, you will stop all the related running application instances and thus you will get refund of the remaining task duration.

```python
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

# Terminate an existing task (and its application instances)
swan_orchestrator.terminate_task(<task_uuid>)
```

### Storage

#### Create and Delete Buckets
```python
import swan

# create a storage resource, you will need to use an mcs api key
swan_storage = swan.resource(api_key='<MCS_API_KEY>', service_name='Storage')

# create a bucket
swan_storage.create_bucket(bucket_name='my-bucket')

# delete a bucket
swan_storage.delete_bucket(bucket_name='my-bucket')
```

#### Upload Folders

You can create a folder but also upload an MCS or IPFS folder
```python
import swan

# create a storage resource, you will need to use an mcs api key
swan_storage = swan.resource(api_key='<MCS_API_KEY>', service_name='Storage')

my_mcs_path = 'my-folder/my-mcs-folder'
my_ipfs_path = 'my-folder/my-ipfs-folder'

# create a bucket
swan_storage.create_bucket(bucket_name='my-bucket')

# create a folder, it will be stored under bucket_name/prefix/folder_name
swan_storage.create_folder(bucket_name='my-bucket', folder_name='my-folder', prefix='my-prefix')

# upload a folder as an MCS folder under bucket_name/object_name
swan_storage.upload_folder(bucket_name='my-bucket', folder_name='my-mcs-folder', folder_path=my_mcs_path)

# upload a folder as an IPFS folder under bucket_name/object_name
bucket_client.upload_ipfs_folder(bucket_name='my-bucket', folder_name='my-ipfs-folder', folder_path=my_ipfs_path)
```


#### Manipulate Files

```python
import swan

# create a storage resource, you will need to use an mcs api key
swan_storage = swan.resource(api_key='<MCS_API_KEY>', service_name='Storage')

my_file_path = 'my-folder/my-file'
my_file_download_path = 'my-folder/downloaded-file'

# create a bucket
swan_storage.create_bucket(bucket_name='my-bucket')

# upload a file
swan_storage.upload_file(bucket_name='my-bucket', object_name='my-file', file_path=my_file_path)

# download a file located at bucket_name/object_name
swan_storage.download_file(bucket_name='my-bucket', object_name='my-file', local_filename=my_file_download_path)

# delete a file located at bucket_name/object_name
swan_storage.delete_file(bucket_name='my-bucket', object_name='my-file')
```

#### Get Bucket Information

```python
import swan

# create a storage resource, you will need to use an mcs api key
swan_storage = swan.resource(api_key='<MCS_API_KEY>', service_name='Storage')

# get in information of a bucket
print(swan_storage.get_bucket(bucket_name='my-bucket').to_json())
```

Sample output:
```
{
    "address": "0xA87...9b0",
    "bucket_name": "test-bucket",
    "bucket_uid": "8721a157-8233-4d08-bb11-1911e759c2bb",
    "created_at": "2023-01-04T17:52:04Z",
    "deleted_at": null,
    "file_number": 4,
    "is_active": true,
    "is_deleted": false,
    "is_free": true,
    "max_size": 34359738368,
    "size": 9988,
    "updated_at": "2023-01-04T17:52:04Z"
}
```


```python
# get information about a specific file
print(swan_storage.get_file(bucket_name='my-bucket', object_name='my-file').to_json())
```


Sample output:
```
{
    "address": "0xA87...9b0",
    "bucket_uid": "8721a157-8233-4d08-bb11-1911e759c2bb",
    "created_at": "2023-02-08T18:35:33Z",
    "deleted_at": null,
    "filehash": "65a8e27d8879283831b664bd8b7f0ad4",
    "gateway": "https://fce2d84f11.calibration-swan-acl.filswan.com/",
    "id": 6153,
    "ipfs_url": "https://ipfs.multichain.storage/ipfs/Qm...",
    "is_deleted": false,
    "is_folder": false,
    "name": "file1.txt",
    "object_name": "file1.txt",
    "payloadCid": "Qm...",
    "pin_status": "Pinned",
    "prefix": "",
    "size": 13,
    "type": 2,
    "updated_at": "2023-02-08T18:35:33Z"
}
```


```python
# get a list of files in a bucket
for i in swan_storage.list_files(bucket_name='my-bucket'):
    print(i.to_json())
```
Sample output:

```
[
  {
    "address": "0xA87...9b0",
    "bucket_uid": "8721a157-8233-4d08-bb11-1911e759c2bb",
    "created_at": "2023-02-08T18:35:33Z",
    "deleted_at": null,
    "filehash": "65a8e27d8879283831b664bd8b7f0ad4",
    "gateway": "https://fce2d84f11.calibration-swan-acl.filswan.com/",
    "id": 6153,
    "ipfs_url": "https://ipfs.multichain.storage/ipfs/Qm...",
    "is_deleted": false,
    "is_folder": false,
    "name": "file1.txt",
    "object_name": "file1.txt",
    "payloadCid": "Qm...",
    "pin_status": "Pinned",
    "prefix": "",
    "size": 13,
    "type": 2,
    "updated_at": "2023-02-08T18:35:33Z"
  },
  {
    "address": "0xA87...9b0",
    "bucket_uid": "8721a157-8233-4d08-bb11-1911e759c2bb",
    "created_at": "2023-02-08T18:35:33Z",
    "deleted_at": null,
    "filehash": "65a8e27d8879283831b664bd8b7f0ad4",
    "gateway": "https://fce2d84f11.calibration-swan-acl.filswan.com/",
    "id": 6153,
    "ipfs_url": "https://ipfs.multichain.storage/ipfs/Qm...",
    "is_deleted": false,
    "is_folder": false,
    "name": "file1.txt",
    "object_name": "file1.txt",
    "payloadCid": "Qm...",
    "pin_status": "Pinned",
    "prefix": "",
    "size": 13,
    "type": 2,
    "updated_at": "2023-02-08T18:35:33Z"
  },
...
]
```

## License

The PYTHON SWAN SDK is released under the **MIT** license, details of which can be found in the LICENSE file.
