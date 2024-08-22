# PYTHON SWAN SDK <!-- omit in toc -->

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/) 
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/swanchain)

## Table Of Contents<!-- omit in toc -->

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Overview](#overview)
- [Features](#features)
- [Use Python dotenv](#use-python-dotenv)
- [Quick Start Guide for Swan SDK](#quick-start-guide-for-swan-sdk)
  - [1. Get Orchestrator API Key](#1-get-orchestrator-api-key)
  - [2. Login into Orchestrator Through SDK](#2-login-into-orchestrator-through-sdk)
  - [3. Retrieve available hardware information](#3-retrieve-available-hardware-information)
  - [4. Select hardware\_id and region (Optional)](#4-select-hardware_id-and-region-optional)
  - [5. Estimate Payment Amount (Optional)](#5-estimate-payment-amount-optional)
  - [6a. Create Task with prebuilt image (Optional)](#6a-create-task-with-prebuilt-image-optional)
    - [Choose one of the prebuilt images](#choose-one-of-the-prebuilt-images)
  - [6b. Create Task with Auto Pay](#6b-create-task-with-auto-pay)
  - [6c. Renew Task with Auto Pay (Optional)](#6c-renew-task-with-auto-pay-optional)
  - [6d. Deploy a task without auto\_pay (Optional)](#6d-deploy-a-task-without-auto_pay-optional)
  - [7. Make Payment (Optional)](#7-make-payment-optional)
  - [8. Validate Payment to Deploy Task (Optional)](#8-validate-payment-to-deploy-task-optional)
  - [9. Renew task without auto\_pay (Optional)](#9-renew-task-without-auto_pay-optional)
  - [10. Terminate task (Optional)](#10-terminate-task-optional)
  - [11. Follow-up Task Status (Optional)](#11-follow-up-task-status-optional)
    - [Show results](#show-results)
  - [12. Check Config Order Status (Optional)](#12-check-config-order-status-optional)
- [Examples](#examples)
- [Documentation](#documentation)
- [License](#license)


## Installation

To use Python Swan SDK, use **Python 3.8 or later** and **web3.py 6.15 or later**. Earlier versions are not supported.

**Install via PyPI:**

```bash
pip install swan-sdk
```

**Clone from GitHub:**

```bash
git clone https://github.com/swanchain/python-swan-sdk.git
```

## Quick Start

To deploy a simple application with Swan SDK (see [How to get API KEY](#1-get-orchestrator-api-key)):

```python
import os
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

result = swan_orchestrator.create_task(
    app_repo_image='hello_world',
    wallet_address='<WALLET_ADDRESS>',
    private_key='<PRIVATE_KEY>',
)
task_uuid = result['id']
# Get task info
task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))
```

It may take up to 5 minutes to get the deployment result:

```python
# check the deployed url
result_url = swan_orchestrator.get_real_url(task_uuid)
print(result_url)
```
A sample output:

```
['https://krfswstf2g.anlu.loveismoney.fun', 'https://l2s5o476wf.cp162.bmysec.xyz', 'https://e2uw19k9uq.cp5.node.study']
```

It shows the this task has been deployed to 3 computing providers. If one of the app links is up, open it in the browser will show some simple information.

## Overview

The PYTHON SWAN SDK is a comprehensive toolkit designed to facilitate seamless interactions with the SwanChain API. Tailored for developers, this SDK simplifies the creation and management of computational tasks (CP tasks), making it an indispensable tool for developers working in various tech domains.

GitHub Link: https://github.com/swanchain/python-swan-sdk/tree/main

## Features

- **API Client Integration**: Streamline your development workflow with our intuitive API client.
- **Service Layer Abstractions**: Access complex functionalities through a simplified high-level interface, improving code maintainability.
- **Extensive Documentation**: Access a wealth of information through our comprehensive guides and reference materials located in the `docs/` directory on GitHub.

## Use Python dotenv

It is recommended to store your important personal information in configuration or as environmental variables. Python dotenv allows loading environment variables from `.env` files for easier access and better security.

python-dotenv package: https://pypi.org/project/python-dotenv/ \
Detailed instructions: https://github.com/swanchain/python-swan-sdk/tree/main/docs/configuration.md

## Quick Start Guide for Swan SDK

Jump into using the SDK with this quick example:

### 1. Get Orchestrator API Key

To use `swan-sdk`, an Orchestrator API key is required. 

- Go to [Orchestrator Dashboard](https://orchestrator.swanchain.io/provider-status), switch network to Mainnet.
- Login through MetaMask.
- Click the user icon on the top right.
- Click 'Show API-Key' -> 'New API Key'
- Store your API Key safely, do not share with others.

### 2. Login into Orchestrator Through SDK

To use `swan-sdk` you will need to login to Orchestrator using API Key. (Wallet login is not supported)

```python
import swan

swan_orchestrator = swan.resource(
  api_key="<your_api_key>", 
  service_name='Orchestrator'
)
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

Choose a hardware with its hardware id and region. If no hardware_id is provided in `create_task` function, it will default to use free tier (`hardware_id=0`), and it no region is provided, it will default to `global`.

```python
hardware_id = 0
region = 'global'
```

### 5. Estimate Payment Amount (Optional)

To estimate the payment required for the deployment. Use method `estiamte_payment` in `SwanContract`

```python
duration = 3600 # or duration you want the deployment to run, this field is in seconds
amount = swan_orchestrator.estimate_payment(chosen_hardware.id, duration_seconds)
amount
```

### 6a. Create Task with prebuilt image (Optional)

Auto-pay is on for this tutorial path, in which case task creation, payment, and deployment are all in one. If you do no want to auto-pay, `make_payment` method is available.

For more information about the [create_task Function](/docs/key_functions.md#create_task-function-details).

```python
import json

result = swan_orchestrator.create_task(
    app_repo_image="hello_world",
    wallet_address=wallet_address,
    private_key=private_key
)
print(json.dumps(result, indent=2))
task_uuid = result['id']
# keep track of hardware_id this task using
hardware_id = result['hardware_id']
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

#### Choose one of the prebuilt images

A list of prebuilt app images can be accessed from backend, then choose one of the names as `app_repo_image` in creating task.

```python
swan_orchestrator.get_app_repo_image()
```

Part of example list:

```json
[
  {
      "name":"Tetris",
      "url":"https://github.com/swanchain/awesome-swanchain/tree/main/Tetris"
  },
  {
      "name":"jupyter",
      "url":"https://github.com/swanchain/awesome-swanchain/tree/main/jupyter"
  },
  {
      "name":"Memory",
      "url":"https://github.com/swanchain/awesome-swanchain/tree/main/Memory"
  },
  //...
]
```

### 6b. Create Task with Auto Pay

If you want to deploy a application from a GitHub repo or Lagrange Space repo, and also don't want to set up payment manually, you can set `auto_pay=True` expilicitly in `create_task`. 

Note:
- By default, `auto_pay` is set to `None` so it will not make payment in the process of `create_task`, thus a task is only *initialized*, which will be not deployed. 
- To make task eligible for deploy, you can use `make_payment` method (which consists of `submit_payment` and `validate_payment` methods)

For more information about the [create_task Function](/docs/key_functions.md#create_task-function-details).

The repo content of *repo_uri* must contain a *dockerfile*.

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
# keep track of hardware_id this task using
hardware_id = result['hardware_id']

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

### 6c. Renew Task with Auto Pay (Optional)

Extend `task_uuid` by `duration`. Using auto pay automatically makes a transaction to SWAN contract and extends the task.

```python
renew_task = swan_orchestrator.renew_task(
    task_uuid=task_uuid, 
    duration=3600, # Optional: default 3600 seconds (1 hour)
    auto_pay=True, 
    private_key=private_key,
    hardware_id=hardware_id 
)

if renew_task and renew_task['status'] == 'success':
    print(f"successfully renewed task")
```

### 6d. Deploy a task without auto_pay (Optional)

Create (initialize) a task and then pay the task by yourself. `task_uuid`, `hardware_id`, `duration` are required to submit a payment.

For more information about the [create_task Function](/docs/key_functions.md#create_task-function-details).

The repo content of *repo_uri* must contain a *dockerfile*.

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

If you have already submitted payment, you can use the `tx_hash` with `validate_payment()` to validate the payment to let the task can be deployed. If you 

```python
swan_orchestrator.validate_payment(
    tx_hash=tx_hash,
    task_uuid=task_uuid
)
```

### 9. Renew task without auto\_pay (Optional)

If you have already submitted payment for the renewal of a task, you can use the `tx_hash` with `renew_task` to extend the task.

```python
renew_task = swan_orchestrator.renew_task(
    task_uuid=task_uuid, 
    duration=3600, # seconds
    tx_hash=tx_hash, # tx_hash of payment to swan contract for this task
    hardware_id=hardware_id
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

### 12. Check Config Order Status (Optional)

Check config order status with `task_uuid` and `tx_hash`, for example, when create a task, a config order of type `Creation` is created in database with the payment information if available; when renew a task, a `Renewal` config order is created.

We can check the status of these request to see if the payment has been validated and config order has been executed. 

```python
r = swan_orchestrator.get_config_order_status(task_uuid, tx_hash)
print(r)
```


## Examples

For executable examples consult [examples](https://github.com/swanchain/python-swan-sdk/tree/main/examples).

## Documentation

For comprehensive documentation, including detailed installation guides, usage examples, and complete API references, please consult [more docs](https://github.com/swanchain/python-swan-sdk/tree/main/docs)

## License

The PYTHON SWAN SDK is released under the **MIT** license, details of which can be found in the LICENSE file.
