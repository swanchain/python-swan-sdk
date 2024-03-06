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
HardwareConfig.region contains a list of avalibale region for choosen hardware.

```python
hardwares = swan_api.get_hardware_config()
# To get all hardware name and price
price_list = [(hardware.name, hardware.price) for hardware in hardwares]
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
repo.upload_local_to_mcs(<str: bucket_name>, <str: object_name/path>, <MCSAPI: mcs_api>)
```

### Upload Task Source .json and Retireve Source URI

To get source URI use MCS with current repository. Simply call generate_source_uri().
This function will create .json file locally contains all neccessary source information
and upload to provided MCS directory.

```python
# Upload source
response = repo.generate_source_uri(<str: bucket_name>, <str: object_name/path>, <str: local_dir_to_store_json>, <MCSAPI: mcs_api>)

# Output source URI
repo.source_uri
```

### Create Source URI Manually

Use SourceFilesInfo() to create Source URI manually with an existing MCS directory.

```python
source = Repository()

# Connect to MCS
source.mcs_connect(mcs_api)

# Add MCS folder
source.update_bucket_info(<str: bucket_name>, <str: object_name/path>)

# Get source URI
response = repo.generate_source_uri(<str: bucket_name>, <str: object_name/path>, <str: local_dir_to_store_json>, <MCSAPI: mcs_api>)

# Output source URI
source.source_uri
```

## Pay for Swan Orchestrator Task

```python
from swan import SwanContract

contract = SwanContract(<private_key>, <rpc_url>)

# Get price of hardware
# Hardware id can be retrieved from Orchestrator API shown above
price = contract.hardware_info(<hardware_id>)

# Get an estimate of payment in wei
estimate = contract.estimate_payment(<hardware_id>, <duration>)
print(estimate*1e-18)

# Approve token
tx_hash = contract._approve_swan_token(<amount>)

# Payment
tx_hash = contract.lock_revenue(<task_id>, <hardware_id>, <duration>)
```

## Deploying Task Through Orchestrator

### Deployment

To deploy task with source URI to Swan Orchestrator. Use SwanAPI.deploy_task.

```python
response = swan_api.deploy_task(cfg_name=<machine_conf_name>, \
    region=<deployment_region>, start_in=<start_time>, duration=<task_duration>, \
    job_source_uri=<source_uri>, paid=<paid_amount>)

task_uuid = response['data']['task']['uuid']
```

### Check Deployment Status
```python
response = swan_api.get_deployment_info(task_uuid)
```