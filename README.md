# PYTHON SWAN SDK

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/) 
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/swanchain)

## Table Of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Use Python dotenv (Optional)](#use-python-dotenv)
- [Quick Guide](#quick-start-guide-sdk-v2)
  1. [Get Orchestrator API Key](#1-get-orchestrator-api-key)
  2. [Login to Orchestrator](#2-login-into-Orchestrator-through-sdk)
  3. [Retrieve CP Hardware Info](#3-retrieve-avaliable-hardware-informaitons)
  4. [Get Job Source URI](#4-get-job_source_uri)
  5. [Create Task](#5-create-task)
  6. [Use Swan Payment Contract](#6-connect-to-swan-payment-contract)
  7. [Esitmate Task Payment](#7-esitmate-payment-amount)
  8. [Submit Payment](#8-submit-payment)
  9. [Validate Payment and Delpoy Task](#9-validate-payment-to-deploy-task)
  10. [Follow-Up Deployed Task Status (Optional)](#10-follow-up-task-status-optional)
- [Executale Example](#examples)
- [Documentation](#documentation)
- [Contribution](#contributions)
- [License](#license)

## Overview

The PYTHON SWAN SDK is a comprehensive toolkit designed to facilitate seamless interactions with the SwanChain API. Tailored for developers, this SDK simplifies the creation and management of computational tasks (CP tasks), making it an indispensable tool for developers working in various tech domains.

GitHub Link: https://github.com/swanchain/python-swan-sdk/tree/main

## Features

- **API Client Integration**: Streamline your development workflow with our intuitive API client.
- **Pre-defined Data Models**: Utilize our structured data models for tasks, directories, and source URIs to enhance your application's reliability and scalability.
- **Service Layer Abstractions**: Access complex functionalities through a simplified high-level interface, improving code maintainability.
- **Extensive Documentation**: Access a wealth of information through our comprehensive guides and reference materials located in the `docs/` directory on GitHub.

## Installation

Setting up the PYTHON SWAN SDK is straightforward.

To use Python Swan SDK, use **Python 3.8 or later** and **web3.py 6.15 or later**. Earlier versions are not supported.

**Install via PyPI:**

```bash
pip install swan-sdk==0.0.2
```

**Clone from GitHub:**

```bash
git clone https://github.com/swanchain/orchestrator-sdk.git
git checkout release/v0.0.2-1
```

## Use Python dotenv

It is recommended to store your important personal information in configuration or as environmental variables. Python dotenv allows loading environment variables from `.env` files for easier access and better security.

python-dotenv package: https://pypi.org/project/python-dotenv/ \
Detailed instructions: https://github.com/swanchain/python-swan-sdk/tree/release/v0.0.2-1/docs/configuration.md

## Quick Start Guide for Swan SDK

Jump into using the SDK with this quick example:

### 1. Get Orchestrator API Key

To use `swan-sdk`, an Orchestrator API key is required. 

- Go to Orchestrator Dashboard: https://orchestrator.swanchain.io/provider-status
- Login through MetaMask.
- Click the user icon on the top right.
- Click 'Show API-Key' -> 'New API Key'
- Store your API Key safely, do not share with others.

### 2. Login into Orchestrator Through SDK

To use `swan-sdk` you will need to login to Orchestrator using API Key. (Wallet login is not supported)

```python
from swan import SwanAPI

swan_api = SwanAPI(api_key="<your_api_key>")
```

### 3. Retrieve available hardware information

Orchestrator provides a selection of Computing Providers with different hardware.
Use `SwanAPI().get_hardware_config()` to retrieve all available hardware on Orchestrator.

Hardware config contains a unique hardware ID, hardware name, description, hardware type (CPU/GPU), price per hour, available region and current status.

See all available hardware in a Python dictionary:

```python
hardwares = swan_api.get_hardware_config()
hardwares_info = [hardware.to_dict() for hardware in hardwares if hardware.status == "available"] 
hardwares_info
```
You can use 
```python
from swan.object import HardwareConfig
```
to check the hardware information like this:
- `HardwareConfig().status` shows the availability of the hardware.
- `HardwareConfig().region` is a list of all regions this hardware is available in.

Useful example: Retrieve the hardware with hardware ID 0:
```python
hardwares = swan_api.get_hardware_config()
chosen_hardware = [hardware for hardware in hardwares if hardware.id == 0][0]
print(chosen_hardware.to_dict())
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

### 4. Get job_source_uri

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
print(job_source_uri)
```

### 5. Connect to Swan Payment Contract

Payment of Orchestrator deployment is paid through the Swan Payment Contract. To navigate the contract ABIs. First create a `SwanContract()` instance:

```python
from swan.contract.swan_contract import SwanContract

contract = SwanContract('<your_private_key>', swan_api.contract_info)
```

### 6. Estimate Payment Amount

To estimate the payment required for the deployment. Use `SwanContract().estiamte_payment()`

```python
duration_hour = 1 # or duration you want the deployment to run
amount = contract.estimate_payment(chosen_hardware.id, duration_hour)
print(amount) # amount is in wei, 18 decimals
```

### 7. Create Task

Before paying for the task. First, create a task on Orchestrator using desired task attributes.

```python
import json

duration_hour = 1
# Notice that from here, you need to convert the duration to seconds
duration = 3600*duration_hour
cfg_name = chosen_hardware.name

result = swan_api.create_task(
    cfg_name=cfg_name, 
    region='<region_name>', # e.g. 'North Carolina-US' or chosen_hardware.region[0]
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

**The `task['uuid']` will be used in the following operations.**



### 8. Submit Payment

- **If you got error about insufficient balance, please make sure you have enough balance in your wallet.**
- *If you have Error like "to_wei() does not exist", please make sure you have web3.py 6.15 or later.*

Use `SwanContract().submit_payment()` to pay for the task. The TX hash is the receipt for the payment.

```python
tx_hash = contract.submit_payment(task_uuid, chosen_hardware.id, duration) # duration in seconds
```

### 9. Validate Payment to Deploy Task

Use `SwanAPI().validate_payment()` to validate the payment using TX hash and deploy the task.

```python
swan_api.validate_payment(
    tx_hash=tx_hash,
    task_uuid=task_uuid
)
```

### 10. Follow-up Task Status (Optional)

#### Show results

Get the deploy URI to test your deployed task using `SwanAPI().get_real_uri()`.

```python
r = swan_api.get_real_url(task_uuid)
print(r)
```

#### Show task details
Get the task details using `SwanAPI().get_deployment_info()`.

```python
r = swan_api.get_deployment_info(task_uuid)
print(r)
```
Simple output
```
{
   "data":{
      "computing_providers":[
         
      ],
      "jobs":[
         
      ],
      "task":{
         "created_at":"1714877536",
         "end_at":"1714881125",
         "leading_job_id":"None",
         "refund_amount":"None",
         "status":"accepting_bids",
         "task_detail_cid":"task_detail_cid",
         "tx_hash":"None",
         "updated_at":"1714877801",
         "uuid":"204cd1be-30b0-4915-a635-4b9dbf1a3b5e"
      }
   },
   "message":"fetch task info for task_uuid='204cd1be-30b0-4915-a635-4b9dbf1a3b5e' successfully",
   "status":"success"
}
```


## Examples
For executable examples consult https://github.com/swanchain/python-swan-sdk/tree/release/v0.0.2.post1/examples

## Documentation

For comprehensive documentation, including detailed installation guides, usage examples, and complete API references, please consult https://github.com/swanchain/python-swan-sdk/tree/release/v0.0.2.post1/docs

## License

The PYTHON SWAN SDK is released under the **MIT** license, details of which can be found in the LICENSE file.
