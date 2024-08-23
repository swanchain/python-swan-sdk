import pathlib
import time

import swan
import json

from swan import Orchestrator
from swan.object.task import PrivateTask

api_key = '<your_api_key>'
wallet_address = '<WALLET_ADDRESS>'
private_key = '<PRIVATE_KEY>'

# for testnet dev
swan_orchestrator: Orchestrator = swan.resource(
    api_key=api_key,
    service_name='Orchestrator',
    network="testnet",
    login_url='https://swanhub-cali.swanchain.io',      # dev version for testnet login url
    url_endpoint='https://swanhub-cali.swanchain.io'    # dev version for testnet
    # login_url='http://localhost:5008',  # dev version for testnet login url
    # url_endpoint='http://localhost:5008'  # dev version for testnet
)
# for mainnet
# swan_orchestrator: Orchestrator = swan.resource(
#     api_key=api_key,
#     network='mainnet',
#     service_name='Orchestrator'
# )

private_task: PrivateTask = swan_orchestrator.create_private_task(
    project_path=pathlib.Path(__file__).parent / "example_private_project",
    wallet_address=wallet_address,
    private_key=private_key,
    hardware_id=1,
    duration=3600,
    auto_pay=True,
)

# You can serialize the private task object for later loads again
# print(private_task.serialize_to_json())
# private_task = PrivateTask.load_from_json(
#     json_str='{"task_uuid": "e9c48e8c-e362-437c-8968-2ef28f049496", "encryption_key": "REZHbMraY2aTXpEKFo2FgjloXxGnAkmqxoXVVnvWRGY="}',
#     orchestrator=swan_orchestrator
# )

task_uuid = private_task.task_uuid

task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))

print(private_task.serialize_to_json())
private_task.deploy_task(interval=20, retries=100)

### get real url (if no url, please wait for a while, then check again)
for _ in range(100):
    result_url = swan_orchestrator.get_real_url(task_uuid)
    print(f"app url: {result_url}")
    if result_url:
        break
    time.sleep(5)