# Using Swan SDK

## Using Swan Orchestrator APIs

Swan Orchestrator APIs allow user to check machine configuration and deploy tasks.

### Login to Swan Orchestrator with API Key

Swan SDK can only login to Orchestrator through official API key.
Generate API key using your wallet on Swan Orchestrator website.

```python
from swan import SwanAPI

api_key = <your_swan_hub_api_key>
swan_api = SwanAPI(api_key)
```

### Retrieving CP Machine Hardware Info

Hardware information can be retrieved from Swan Orchestrator API.
Task can only be deployed in any region when the choosen hardware is avaliable in that region.
HardwareConfig().region contains a list of avalibale region for choosen hardware.

```python
# Returns a list of HardwareConfig() objects
hardwares = swan_api.get_hardware_config()
# To get all hardware name and price
price_list = [(hardware.name, hardware.price) for hardware in hardwares]
```

HardwareConfig() object contains:
```python
{
    "id": <hardware_id>,
    "name": <hardware_name>,
    "description": <hardware_description>,
    "type": <hardware_type>, # CPU/GPU
    "reigion": <list_of_valiable_regions>,
    "price": <price_per_hour>,
    "status": <current_status>
}
```

To retrieve specific hardware infomation

```python
hardware_attribute = HardwareConfig().<attribute_name>
```

Dictionary object or JSON object of hardware:
```python
HardwareConfig().to_dict()

HardwareConfig().to_json()
```

## Using MCS APIs

MCS provides file storage on IPFS server.

### Login to MCS with API Key
MCS SDK can only login to multichain.storage through official API key.

```python
from swan import MCSAPI

api_key = <your_mcs_api_key>
mcs_api = MCSAPI(api_key)
```

### Create MCS Bucket
Create MCS bucket for all mcs related operation.

```python
mcs_api.create_bucket(<bucket_name: str>)
```

## Generate Task Source URI
To deploy task on Swan Orchestrator. Remote source is required. Task deployment
API requires source uri, which should contain a .json file with deployment information.

Source URI can be generated using Swan SDK.

### Create Repository

Create an online repository (folder) to store your project on MCS.

```python
from swan.object import Repository

repo = Repository()

# Add local directory
repo.add_local_dir('<local_project_directory>')

# Upload Directory to MCS
repo.upload_local_to_mcs(<bucket_name: str>, <object_name/path: str>, mcs_api)
```

### Upload Task Source .json and Retireve Source URI

To get source URI use MCS with current repository. Simply call generate_source_uri().
This function will create .json file locally contains all neccessary source information
and upload to provided MCS directory.

```python
# Upload source
response = repo.generate_source_uri(<bucket_name: str>, <object_name/path: str>, <local_dir_to_store_json: str>, mcs_api)

# Output source URI
repo.source_uri
```

### Create Source URI Manually

Use SourceFilesInfo() to create Source URI manually with an existing MCS directory.

```python
source = Repository()

# Connect to MCS
source.mcs_connection(mcs_api)

# Add MCS folder
source.update_bucket_info(<bucket_name: str>, <object_name/path: str>)

# Get source URI
response = source.generate_source_uri(<bucket_name: str>, <object_name/path: str>, <local_dir_to_store_json: str>, mcs_api)

# Output source URI
source.source_uri
```

## Pay for Swan Orchestrator Task

```python
from swan import SwanContract

contract = SwanContract(<private_key: str>, <rpc_url: str>)

# Get price of hardware
# Hardware id can be retrieved from Orchestrator API shown above
price = contract.hardware_info(<hardware_id: int>)

# Get an estimate of payment in wei
estimate = contract.estimate_payment(<hardware_id: int>, <duration: int>)
print(estimate*1e-18)

# Approve token
tx_hash = contract._approve_swan_token(<amount: int>)

# Payment
tx_hash = contract.lock_revenue(<task_id: int>, <hardware_id: int>, <duration: int>)
```

## Deploying Task Through Orchestrator

### Deployment

To deploy task with source URI to Swan Orchestrator. Use SwanAPI.deploy_task.

```python
response = swan_api.deploy_task(cfg_name=<machine_conf_name: str>, \
    region=<deployment_region: str>, start_in=<start_time: int>, duration=<task_duration: int>, \
    job_source_uri=<source_uri: str>, paid=<paid_amount: float>)

task_uuid = response['data']['task']['uuid']
```

### Check Deployment Status
```python
response = swan_api.get_deployment_info(task_uuid)
```