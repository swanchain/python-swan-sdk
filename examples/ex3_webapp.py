import swan
import json

api_key = '<your_api_key>'
wallet_address = '<WALLET_ADDRESS>'
private_key = '<PRIVATE_KEY>'

swan_orchestrator = swan.resource(
    api_key=api_key, 
    network='mainnet', 
    service_name='Orchestrator'
)

result = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/serverless-api',
    wallet_address=wallet_address,
    private_key=private_key,
    auto_pay=True
)

task_uuid = result['id']

task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))

### get real url (if no url, please wait for a while, then check again)
result_url = swan_orchestrator.get_real_url(task_uuid)
print(result_url)