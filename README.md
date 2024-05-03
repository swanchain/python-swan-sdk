# PYTHON SWAN SDK

[![Made by FilSwan](https://img.shields.io/badge/made%20by-FilSwan-green.svg)](https://www.filswan.com/) 
[![Chat on discord](https://img.shields.io/badge/join%20-discord-brightgreen.svg)](https://discord.com/invite/KKGhy8ZqzK)

## Overview

The PYTHON SWAN SDK is a comprehensive toolkit designed to facilitate seamless interactions with the SwanChain API. Tailored for developers, this SDK simplifies the creation and management of computational tasks (CP tasks), making it an indispensable tool for developers working in various tech domains.

## Features

- **API Client Integration**: Streamline your development workflow with our intuitive API client.
- **Pre-defined Data Models**: Utilize our structured data models for tasks, directories, and source URIs to enhance your application's reliability and scalability.
- **Service Layer Abstractions**: Access complex functionalities through a simplified high-level interface, improving code maintainability.
- **Extensive Documentation**: Access a wealth of information through our comprehensive guides and reference materials located in the `docs/` directory.

## Installation

Setting up the PYTHON SWAN SDK is straightforward.

**Install via PyPI testnet:**

```bash
pip install swan-sdk
```

**Clone from GitHub:**

```bash
git clone https://github.com/swanchain/orchestrator-sdk.git
```

## Quick Start Guide SDK V1

Get started quickly with this basic example:

```python
from swan import SwanAPI

# Initialize the SwanAPI
swan_api = SwanAPI(api_key='your_api_key_here')

# Fetch available hardware configurations
hardwares = swan_api.get_hardware_config()
price_list = [(hardware.name, hardware.price) for hardware in hardwares]

# Create a task
result = swan_api.deploy_task(cfg_name='config1', region='US', start_in=123, duration=123, job_source_uri='uri', paid=123, tx_hash='tx_hash_here', wallet_address='wallet_address_here')
print("Deployment Result:", result)

# Retrieve deployment information
deployment_info = swan_api.get_deployment_info(task_uuid='your_task_uuid_here')
print("Deployment Info:", deployment_info)
```

**On-chain operations with SwanContract:**

```python
swan_contract = SwanContract(private_key='your_private_key_here', contract_info=swan_api.contract_info)

# Example: Estimate lock revenue
estimation = swan_contract.estimate_payment(hardware_id=1, duration=10)
print("Estimated Payment:", estimation * 1e-18)  # Convert to readable format

# Retrieve and display hardware information
hardware_info = swan_contract.hardware_info(1)
print("Hardware Info:", hardware_info)

# Fetch and display Swan token balance
balance = swan_contract.get_swan_balance()
print("Swan Token Balance:", balance * 1e-18)  # Convert to readable format

# Approve and lock Swan tokens
tx_hash = swan_contract.approve_swan_token(amount=100)
print("Transaction Hash:", tx_hash)
lock_result = swan_contract.lock_revenue(task_id='1', hardware_id=1, duration=10)
print("Lock Revenue Result:", lock_result)
```

For additional detailed examples, visit the `docs/` directory.

## Documentation

For comprehensive documentation, including detailed installation guides, usage examples, and complete API references, please consult the `docs/` directory.

## Contributions

We welcome and encourage community contributions! Please refer to our **CONTRIBUTING.md** for guidelines on how to contribute effectively.

## License

The PYTHON SWAN SDK is released under the **MIT-FilSwan** license, details of which can be found in the LICENSE file.
