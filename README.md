# PYTHON SWAN SDK

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/) 
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/KKGhy8ZqzK)

## Overview

The PYTHON SWAN SDK provides a streamlined and efficient interface for interacting with our API. It's tailored for easy creation and management of CP tasks, making it a versatile tool for a wide range of applications.

## Features

- **Easy API Integration**: Simplify your workflow with our user-friendly API client.
- **Data Models**: Leverage our pre-built models for tasks, directory, and source URI.
- **Service Abstractions**: Gain access to high-level functionalities through our service layer.
- **Comprehensive Documentation**: Discover detailed guides and references in the `docs/` directory.

## Installation

Install the SDK with ease.

From pypi testnet:

```bash
pip install -i https://test.pypi.org/simple/ orchestrator-sdk
```

Install from Github:

```bash
git clone https://github.com/swanchain/orchestrator-sdk.git
git checkout dev
```

## Quick Start Guide SDK V1
Jump into using the SDK with this quick example:

```python

from swan import SwanAPI

# Initialize the Swan Service
# Perform verification and retrieve signed contract address store in SWANAPI.contract_info
swan_api = SwanAPI(api_key='')

# Retrieve List of Hardwares
hardwares = swan_api.get_hardware_config()
price_list = [(hardware.name, hardware.price) for hardware in hardwares]

# Deploy task
# tx_hash from lock_payment from swan payment cotract (see demo code below)
result = swan_api.deploy_task(cfg_name='', region='', start_in=123, duration=123, job_source_uri='', paid=123, tx_hash='', wallet_address='')
print(result)

# Check task info
swan_api.get_deployment_info(task_uuid='')
```
Lock Swan Token onchain:

```python
swan_contract = SwanContract(private_key='', contract_info=swan_api.contract_info)

# Test esimate lock revenue
estimation = swan_contract.estimate_payment(hardware_id=1, duration=10)
print(estimation*1e-18)

# Test get hardware info
hardware_info = swan_contract.hardware_info(1)
hardware_info

# Test get swan token balance
balance = swan_contract._get_swan_balance()
print(balance*1e-18)

# Test get gas
gas = swan_contract._get_swan_gas()
print(gas*1e-18)

# Approve Swan Token
tx_hash = swan_contract._approve_swan_token(amount=100)
print(tx_hash)

# Lock payment
r = swan_contract.lock_revenue(task_id='1', hardware_id=1, duration=0)
```

For more detailed examples, visit the docs/ directory.

## Documentation
For in-depth documentation, including installation guides, usage examples, and API references, refer to the docs/ directory.

## Contributions
We encourage contributions! Please consult our contribution guidelines in **CONTRIBUTING.md**.

## License
The SWAN SDK is released under the **MIT-FilSwan** license. For more details, see the LICENSE file.
