# Sample Tutorial for Swan SDK
Jump into using the SDK with this quick example:

## Table Of Contents
1. [Get Orchestrator API Key](#1-get-orchestrator-api-key)
2. [Login to Orchestrator](#2-login-into-orchestrator-through-sdk)
3. [Use Swan Payment Contract](#3-connect-to-swan-payment-contract)
4. [Retrieve CP Hardware Info](#4-retrieve-avaliable-hardware-informaitons)
5. [Get Job Source URI](#5-get-job_source_uri)
6. [Esitmate Task Payment](#6-esitmate-payment-amount)
7. [Create Task](#7-create-task)
8. [Submit Payment](#8-submit-payment)
9. [Validate Payment and Delpoy Task](#9-validate-payment-to-deploy-task)
10. [Follow Up Deployed Task Status (Optional)](#10-follow-up-task-status-optional)

### 1. Get Orchestrator API Key

To use `swan-sdk` Orchestrator API key is required. 
- Go to Swan Dashboard: https://orchestrator.swanchain.io/provider-status
- Login through MetaMask.
- Click the user icon on top right.
- Click 'Show API-Key' -> 'New API Key'
- Store your API Key safely, do not share with others.

### 2. Login into Orchestrator Through SDK

To use `swan-sdk` you will need to login to Orchestrator using API Key. (Wallet login is not supported)

```python
from swan import SwanAPI

swan_api = SwanAPI(api_key="<your_api_key>")
```

### 3. Connect to Swan Payment Contract

Payment of Orchestrator deployment is paid through Swan Payment Contract. To navigate the contract ABIs. First create a `SwanContract()` instance:
```python
from swan.contract.swan_contract import SwanContract

contract = SwanContract('<your_private_key>', swan_api.contract_info)
```

### 4. Retrieve Avaliable Hardware Informaitons

Orchestrator provides selection of Computing Providers with different hardwares.
Use `SwanAPI().get_hardware_config()` to retrieve all avaliable hardwares on Orchestrator.

Each hardware is stored in `HardwareConfig()` object.
```python
from swan.object import HardwareConfig
```

Hardware config contains an unique hardware ID, hardware name, description, hardware type (CPU/GPU), price per hour, avaliable region and current status.

See all avaliable hardware in a python dictionary:
```python

hardwares = swan_api.get_hardware_config()
hardwares_info = [hardware.to_dict() for hardware in hardwares if hardware.status == "available"] 
hardwares_info
```
`HardwareConfig().status` shows the avalibility of the hardware.
`HardwareConfig().region` is a list of all region this hardware is avaliable in.

Retrieve the hardware with hardware id 0:
```python
hardwares = swan_api.get_hardware_config()
chosen_hardware = [hardware for hardware in hardwares if hardware.id == 0]
chosen_hardware.to_dict()
```

Sample output:
```
{'id': 0,
 'name': 'C1ae.small',
 'description': 'CPU only · 2 vCPU · 2 GiB',
 'type': 'CPU',
 'reigion': ['North Carolina-US', ...],
 'price': '0.0',
 'status': 'available'
}
```

### 5. Get job_source_uri

`job_source_uri` can be create through `SwanAPI().get_source_uri()` API.

Generate a source URI
A demo tetris docker image on GitHub as repo_uri: 'https://github.com/alphaflows/tetris-docker-image.git'
```python
job_source_uri = swan_api.get_source_uri(
    repo_uri='<your_git_hub_link/your_lagrange_space_link>',
    hardware_id=chosen_hardware.id,
    wallet_address='<your_wallet_address>'
)

job_source_uri = job_source_uri['data']['job_source_uri']
```

### 6. Esitmate Payment Amount
To estimate the payment required for the deployment. Use `SwanContract().estiamte_payment()`
```python
duration_hour = 1 # or duration you want the deployment to run
amount = contract.estimate_payment(chosen_hardware.id, duration_hour)
amount # amount is in wei, 18 decimals
```

### 7. Create Task

Before paying for the task. First create a task on Orchestrator using desired task attributes.
```python
import json

duration = 3600*duration_hour
cfg_name = chosen_hardware.name

result = swan_api.create_task(
    cfg_name=cfg_name, 
    region='<region_name>', 
    start_in=300,  # in seconds
    duration=duration, 
    job_source_uri=job_source_uri, #repo.source_uri
    paid=contract._wei_to_swan(amount), # from wei to swan amount/1e18
    wallet_address='<your_wallet_address>',
)
task_uuid = result['data']['task']['uuid']

print(json.dumps(result, indent=2)) # Print response
```

Sample output:
```
{
  "data": {
    "task": {
      "created_at": "1714254304",
      "end_at": "1714257898",
      "leading_job_id": null,
      "refund_amount": null,
      "status": "initialized",
      "task_detail_cid": "https://data.mcs.lagrangedao.org/ipfs/QmXLSaBqtoWZWAUoiYxM3EDxh14kkhpUiYkVjZSK3BhfKj",
      "tx_hash": null,
      "updated_at": "1714254304",
      "uuid": "f4799212-4dc2-4c0b-9209-c0ac7bc48442"
    }
  },
  "message": "Task_uuid initialized.",
  "status": "success"
}
```

The `task['uuid']` will be used in following operations.

### 8. Submit Payment

Use `SwanContract().submit_payment()` to pay for the task. The TX hash is the receipt for the payment.
```python
tx_hash = contract.submit_payment(task_uuid, hardware_id, duration)
```

### 9. Validate Payment to Deploy Task

Use `SwanAPI().validate_payment()` to validate the payment using TX hash and deploy the task.
```python
swan_api.validate_payment(
    tx_hash=tx_hash,
    task_uuid=task_uuid
)
```

### 10. Follow up Task Status (Optional)

#### Show results

Get the deploy URI to test your task deployment using `SwanAPI().get_real_uri()`.
```python
r = swan_api.get_real_url(task_uuid)
print(r)
```