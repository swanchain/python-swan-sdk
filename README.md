markdown
Copy code
# SWAN SDK

## Overview

The SWAN SDK provides a streamlined and efficient interface for interacting with our API. It's tailored for easy creation and management of CP tasks, making it a versatile tool for a wide range of applications.

## Features

- **Easy API Integration**: Simplify your workflow with our user-friendly API client.
- **Data Models**: Leverage our pre-built models for tasks, directory, and source URI.
- **Service Abstractions**: Gain access to high-level functionalities through our service layer.
- **Comprehensive Documentation**: Discover detailed guides and references in the `docs/` directory.

## Installation

Install the SDK with ease:

(no ready yet)
```bash
pip install swan-sdk
```

Install from Github:

```bash
git clone https://github.com/swanchain/orchestrator-sdk.git
git checkout release/v0.1.0
```

## Quick Start Guide
Jump into using the SDK with this quick example:

```python

from swan import SwanAPI

# Initialize the Swan Service
swan_api = SwanAPI(api_key='')

# Retrieve List of Hardwares
hardwares = swan_api.get_hardware_config()
price_list = [(hardware.name, hardware.price) for hardware in hardwares]

# Deploy task
result = swan_api.deploy_task(cfg_name='', region='', start_in=123, duration=123, job_source_uri='', paid=123)
result

# Check task info
swan_api.get_deployment_info(task_uuid='')
```
Lock Swan Token onchain:

```python
swan_contract = SwanContract(private_key='', rpc_url='')

# Test esimate lock revenue
estimation = swan_contract.estimate_payment(hardware_id=1, duration=10)
estimation*1e-18

# Test get hardware info
hardware_info = swan_contract.hardware_info(1)
hardware_info

# Test get swan token balance
balance = swan_contract._get_swan_balance()
balance*1e-18

# Test get gas
gas = swan_contract._get_swan_gas()
gas*1e-18

# Approve Swan Token
tx_hash = swan_contract._approve_swan_token(amount = 100)
tx_hash

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
