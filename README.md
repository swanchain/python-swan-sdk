# PYTHON SWAN SDK <!-- omit in toc -->

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/) 
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/swanchain)

## Table Of Contents<!-- omit in toc -->

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Use Python dotenv](#use-python-dotenv)
- [Quick Start Guide for Swan SDK](#quick-start-guide-for-swan-sdk)
  - [1. Get Orchestrator API Key](#1-get-orchestrator-api-key)
  - [2. Login into Orchestrator Through SDK](#2-login-into-orchestrator-through-sdk)
  - [3. Retrieve available hardware information](#3-retrieve-available-hardware-information)
  - [4. Select hardware\_id and region (Optional)](#4-select-hardware_id-and-region-optional)
  - [5. Estimate Payment Amount (Optional)](#5-estimate-payment-amount-optional)
  - [6a. Create Task with prebuilt image](#6a-create-task-with-prebuilt-image)
  - [6b. Create Task with Auto Pay](#6b-create-task-with-auto-pay)
  - [6c. Renew Task with Auto Pay (optional)](#6c-renew-task-with-auto-pay-optional)
  - [6d. Deploy a task without auto\_pay (no private\_key)](#6d-deploy-a-task-without-auto_pay-no-private_key)
  - [7. Make Payment (Optional)](#7-make-payment-optional)
  - [8. Validate Payment to Deploy Task (Optional)](#8-validate-payment-to-deploy-task-optional)
  - [9. Renew task without private\_key (Optional)](#9-renew-task-without-private_key-optional)
  - [10. Terminate task (Optional)](#10-terminate-task-optional)
  - [11. Follow-up Task Status (Optional)](#11-follow-up-task-status-optional)
    - [Show results](#show-results)
- [Examples](#examples)
- [Documentation](#documentation)
- [License](#license)

## Overview

The PYTHON SWAN SDK is a comprehensive toolkit designed to facilitate seamless interactions with the SwanChain API. Tailored for developers, this SDK simplifies the creation and management of computational tasks (CP tasks), making it an indispensable tool for developers working in various tech domains.

GitHub Link: https://github.com/swanchain/python-swan-sdk/tree/main

## Features

- **API Client Integration**: Streamline your development workflow with our intuitive API client.
- **Service Layer Abstractions**: Access complex functionalities through a simplified high-level interface, improving code maintainability.
- **Extensive Documentation**: Access a wealth of information through our comprehensive guides and reference materials located in the `docs/` directory on GitHub.

## Installation

Setting up the PYTHON SWAN SDK is straightforward.

To use Python Swan SDK, use **Python 3.8 or later** and **web3.py 6.15 or later**. Earlier versions are not supported.

**Install via PyPI:**

```bash
pip install swan-sdk
```

**Clone from GitHub:**

```bash
git clone https://github.com/swanchain/python-swan-sdk.git
```

## Use Python dotenv

It is recommended to store your important personal information in configuration or as environmental variables. Python dotenv allows loading environment variables from `.env` files for easier access and better security.

python-dotenv package: https://pypi.org/project/python-dotenv/ \
Detailed instructions: https://github.com/swanchain/python-swan-sdk/tree/main/docs/configuration.md

## Quick Start Guide for Swan SDK

Jump into using the SDK with this quick example:

### 1. Get Orchestrator API Key

To use `swan-sdk`, an Orchestrator API key is required. 

- Go to [Orchestrator Dashboard](https://orchestrator.swanchain.io/provider-status), you can switch network between Testnet (Proxima) and Mainnet.
- Login through MetaMask.
- Click the user icon on the top right.
- Click 'Show API-Key' -> 'New API Key'
- Store your API Key safely, do not share with others.

### 2. Login into Orchestrator Through SDK

To use `swan-sdk` you will need to login to Orchestrator using API Key. (Wallet login is not supported)

**By default, the backend system will be the testnet. To use the mainnet, set `network='mainnet'`. To use another backend (for example dev environment on Testnet), set `url_endpoint='<target_backend_url>'`.**

```python
import swan

# To use testnet
swan_orchestrator = swan.resource(api_key="<your_api_key>", service_name='Orchestrator')

# To use mainnet
swan_orchestrator = swan.resource(api_key="<your_api_key>", network='mainnet', service_name='Orchestrator')

# To use other backend
swan_orchestrator = swan.resource(api_key="<your_api_key>", url_endpoint='<url_endpoint>', service_name='Orchestrator')
```

### 3. Retrieve available hardware information

Orchestrator provides a selection of Computing Providers with different hardware.
Use `swan_orchestrator.get_hardware_config()` to retrieve all available hardware on Orchestrator.

Hardware config contains a unique hardware ID, hardware name, description, hardware type (CPU/GPU), price per hour, available region and current status.

See all available hardware in a Python dictionary:

```python
hardwares = swan_orchestrator.get_hardware_config()
```

`hardwares[idx]["status"]` shows the availability of the hardware.
`hardwares[idx]["region"]` is a list of all regions this hardware is available in.

Retrieve the hardware with hardware ID 0:

```python
hardwares = swan_orchestrator.get_hardware_config()
chosen_hardware = [hardware for hardware in hardwares if hardware['id'] == 0][0]
```

Sample output:

```
{'id': 0,
 'name': 'C1ae.small',
 'description': 'CPU only · 2 vCPU · 2 GiB',
 'type': 'CPU',
 'region': ['North Carolina-US', ...],
 'price': '0.0',
 'status': 'available'
}
```

Retrieve individual hardware attributes:
```python
print(chosen_hardware['id']) # hardware id
print(chosen_hardware['name']) # hardware name
print(chosen_hardware['description']) # hardware description
print(chosen_hardware['type']) # hardware type
print(chosen_hardware['region']) # all avaliable hardware region
print(chosen_hardware['price']) # current hardware price
print(chosen_hardware['status']) # overall hardware avaliablility
```

### 4. Select hardware_id and region (Optional)
choose a hardware with its hardware id and region. If no hardware_id is provided in future functions, it will default to free tier, and it no region is provided, it will default to global.

```python
hardware_id = 0
region = 'global'
```

### 5. Estimate Payment Amount (Optional)

To estimate the payment required for the deployment. Use `SwanContract().estiamte_payment()`

```python
duration = 3600 # or duration you want the deployment to run, this field is in seconds
amount = swan_orchestrator.estimate_payment(chosen_hardware.id, duration_seconds)
amount
```

### 6a. Create Task with prebuilt image

Auto-pay is on for this tutorial path, in which case task creation, payment, and deployment are all in one. If you do no want to auto-pay, `make_payment` method is available.

A list of prebuilt app images can be accessed from backend, then choose one of the names as `app_repo_image` in creating task.

```python
swan_orchestrator.get_app_repo_image()
```

For more information about the [create_task Function](/docs/key_functions.md#create_task-function-details).

```python
import json

result = swan_orchestrator.create_task(
    app_repo_image="hello-world",
    wallet_address=wallet_address,
    private_key=private_key
)
print(json.dumps(result, indent=2))
task_uuid = result['id']
```

Sample output:
```
{
  "data": {
    "config_id": 1,
    "created_at": 1719591738,
    "duration": 3600,
    "ended_at": null,
    "error_code": null,
    "id": 2439,
    "order_type": "Creation",
    "refund_tx_hash": null,
    "region": "global",
    "space_id": null,
    "start_in": 300,
    "started_at": 1719591738,
    "status": "pending_payment_confirm",
    "task_uuid": "21d3fc99-d4ea-4a42-bdad-797ec15b42de",
    "tx_hash": "0x32596b525c574847a00e477b1cc463a43dd841b085da7de715b4ff0da1db6400",
    "updated_at": 1719591746,
    "uuid": "5b0e098d-284a-46cd-9ef9-d0ca6008785f"
  },
  "message": "Query order status success.",
  "status": "success",
  "tx_hash": "0x32596b525c574847a00e477b1cc463a43dd841b085da7de715b4ff0da1db6400",
  "id": "21d3fc99-d4ea-4a42-bdad-797ec15b42de"
}
```
To see how to renew this task, visit step 7b.
This is the end of this path A, go to Step 10


### 6b. Create Task with Auto Pay

If you want to deploy a application from a GitHub repo or Lagrange Space repo, and also don't want to set up payment manually, you can set `auto_pay=True` expilicitly in `create_task`.

For more information about the [create_task Function](/docs/key_functions.md#create_task-function-details).

**repo_uri must contain a dockerfile**

```python
import json

repo_uri = '<GitHub URL to be deployed. Repo must contain a dockerfile>'

result = swan_orchestrator.create_task(
    wallet_address=wallet_address,
    repo_uri=repo_uri,
    auto_pay=True, # 
    private_key=private_key, # Wallet's private key
    hardware_id=0, # Optional: Defaults to 0 (free tier)
    region='global', # Optional: Defaults to global
    duration=duration, # Optional: Defaults to 3600 seconds
)

# To get the task_uuid, check line below
task_uuid = result['id']

print(json.dumps(result, indent=2)) # Print response
```

Sample output:

```
{
  "data": {
    "config_id": 2,
    "created_at": 1719606062,
    "duration": 3600,
    "ended_at": null,
    "error_code": null,
    "id": 2453,
    "order_type": "Creation",
    "refund_tx_hash": null,
    "region": "North Carolina-US",
    "space_id": null,
    "start_in": 300,
    "started_at": 1719606062,
    "status": "pending_payment_confirm",
    "task_uuid": "00000000-cfaf-4a00-acd8-fe929414cd84",
    "tx_hash": "0x0000000000000000000000000000000000000000000000000",
    "updated_at": 1719606070,
    "uuid": "d4f61285-655a-4f61-a4e0-e6160619c975"
  },
  "message": "Query order status success.",
  "status": "success",
  "tx_hash": "0x0000000000000000000000000000000000000000000000000",
  "id": "00000000-cfaf-4a00-acd8-fe929414cd84"
}
```

### 6c. Renew Task with Auto Pay (optional)

Extend `task_uuid` by `duration`. Using auto pay automatically makes a transaction to SWAN contract and extends the task.

```python
renew_task = swan_orchestrator.renew_task(
    task_uuid=task_uuid, 
    duration=3600, # Optional: Defaults to 3600 seconds (1 hour)
    auto_pay=True, # Optional: Defaults to False, in this demo path set to True
    private_key=private_key,
    hardware_id=hardware_id # Optional: Defaults to 0 (free tier)
)

if renew_task and renew_task['status'] == 'success':
    print(f"successfully renewed task")
```

This is the end of this path B, go to Step 11

### 6d. Deploy a task without auto_pay (no private_key)

Create (initialize) a task and then pay the task by yourself. `task_uuid`, `hardware_id`, `duration` are required to submit a payment.

For more information about the [create_task Function](/docs/key_functions.md#create_task-function-details).

**repo_uri must contain a dockerfile**

```python
import json

repo_uri = '<url of code repo GitHub URL to be deployed. Repo must contain a dockerfile>'

result = swan_orchestrator.create_task(
    wallet_address=wallet_address,
    repo_uri=repo_uri,
    hardware_id=hardware_id, # Optional: Defaults to 0 (free tier)
    region='global', # Optional: Defaults to global
    duration=duration, # Optional: Defaults to 3600 seconds
    auto_pay=False, # Optional: Defaults to false
)

task_uuid = result['id']

print(json.dumps(result, indent=2)) # Print response
```

Sample output:

```
{
  "data": {
    "task": {
      "comments": null,
      "created_at": 1719606552,
      "end_at": 1719610152,
      "id": 1,
      "leading_job_id": null,
      "refund_amount": null,
      "refund_wallet": "0x000000",
      "source": "v2",
      "start_at": 1719606552,
      "start_in": 300,
      "status": "initialized",
      "task_detail": {
        "amount": 1.0,
        "bidder_limit": 3,
        "created_at": 1719606552,
        "duration": 3600,
        "end_at": 1719610152,
        "hardware": "C1ae.medium",
        "job_result_uri": null,
        "job_source_uri": "https://job-source-uri",
        "price_per_hour": "1.0",
        "requirements": {
...
  "message": "Task_uuid initialized.",
  "status": "success",
  "id": "0000000-f395-484f-8ef8-2d4bc5a31e42"
}
```

The `task['id']` will be used in the following operations.

### 7. Make Payment (Optional)

Use `swan_orchestrator.make_payment()` to pay and deploy the task, which combines `submit_payment` and `validate_payment`. 

```python
swan_orchestrator.make_payment(
    task_uuid=task_uuid,
    private_key=private_key,
    duration=3600, # Optional: Defaults to 3600 seconds (1 hour)
    hardware_id=hardware_id # Optional: Defaults to 0 (free tier)
)
```

### 8. Validate Payment to Deploy Task (Optional)

If you have already submitted payment, you can use the `tx_hash` with `validate_payment()` to validate the payment to let the task can be deployed.

```python
swan_orchestrator.validate_payment(
    tx_hash=tx_hash,
    task_uuid=task_uuid
)
```

### 9. Renew task without private_key (Optional)

If you have already submitted payment for the renewal of a task, you can use the `tx_hash` with `renew_task` to extend the task.

```python
renew_task = swan_orchestrator.renew_task(
    task_uuid=task_uuid, 
    duration=60, # Optional: Defaults to 3600 seconds (1 hour)
    tx_hash=tx_hash, # tx_hash of payment to swan contract for this task
    hardware_id=hardware_id # Optional: Defaults to 0 (free tier)
)

if renew_task and renew_task['status'] == 'success':
    print(f"successfully renewed {task_uuid}")
else:
    print(f"Unable to renew {task_uuid}")
```

### 10. Terminate task (Optional)

Early terminate a task.

```python
terminate_status = swan_orchestrator.terminate_task(task_uuid)
if terminate_status['status'] == 'success':
    print(f"Terminated {task_uuid} successfully")
else:
    print(f"Failed to terminate {task_uuid}")
```

### 11. Follow-up Task Status (Optional)

#### Show results

Get the deploy URI to test your deployed task on the web using `swan_orchestrator.get_real_uri()`.

```python
r = swan_orchestrator.get_real_url(task_uuid)
print(r)
```

Sample Output:
```
['https://real_url_link']
```


## Examples

For executable examples consult [examples](https://github.com/swanchain/python-swan-sdk/tree/release/v0.0.4/examples).

## Documentation

For comprehensive documentation, including detailed installation guides, usage examples, and complete API references, please consult [more docs](https://github.com/swanchain/python-swan-sdk/tree/release/v0.0.4/docs)

## License

The PYTHON SWAN SDK is released under the **MIT** license, details of which can be found in the LICENSE file.
