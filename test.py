import swan
import json
 
api_key = 'Z926BmQJyp'
# wallet_address = '<WALLET_ADDRESS>'
# private_key = '<PRIVATE_KEY>'
 
swan_orchestrator = swan.resource(
    api_key=api_key,
    network='testnet',
    service_name='Orchestrator'
)