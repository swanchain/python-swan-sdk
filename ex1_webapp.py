import swan
import json
import os
from dotenv import load_dotenv

load_dotenv("../.env")

api_key = os.getenv("SWAN_API_KEY")
wallet_address = os.getenv("WALLET_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

swan_orchestrator = swan.resource(
    api_key=api_key,
    network='testnet', 
    service_name='Orchestrator',
)

result = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/ChainNode',
    wallet_address=wallet_address,
    private_key=private_key,
    auto_pay=True
)

task_uuid = result['task_uuid']
instance_type = result['instance_type']
task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))

### get real url (if no url, please wait for a while, then check again)
result_url = swan_orchestrator.get_real_url(task_uuid)
print(result_url)