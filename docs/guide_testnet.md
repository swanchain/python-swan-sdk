# Using Swan SDK on Testnet <!-- omit in toc -->

- [1. Get Orchestrator API Key](#1-get-orchestrator-api-key)
- [2. Login into Orchestrator Through SDK](#2-login-into-orchestrator-through-sdk)

### 1. Get Orchestrator API Key

To use `swan-sdk`, an Orchestrator API key is required. 

**By default, the backend system will be the mainnet. To use the testnet, set `network='testnet'`.**

- For Mainnet, go to [Orchestrator Dashboard](https://orchestrator.swanchain.io/provider-status), switch network to Mainnet.
- For Testnet, go to [Orchestrator Dashboard Testnet](https://orchestrator-test.swanchain.io/provider-status), switch network to Proxima.
- Login through MetaMask.
- Click the user icon on the top right.
- Click 'Show API-Key' -> 'New API Key'
- Store your API Key safely, do not share with others.

### 2. Login into Orchestrator Through SDK

To use `swan-sdk` you will need to login to Orchestrator using API Key. (Wallet login is not supported)

```python
import swan

# To use testnet
swan_orchestrator = swan.resource(
  api_key="<your_api_key>", 
  network='testnet',
  service_name='Orchestrator'
)

# To use mainnet
swan_orchestrator = swan.resource(
  api_key="<your_api_key>", 
  service_name='Orchestrator'
)
```
