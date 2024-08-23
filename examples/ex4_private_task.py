import pathlib
import time

from jedi import Project

import swan
import json

from swan import Orchestrator
from swan.object.private_project import PrivateProject
from swan.object.task import PrivateTask

api_key = '<your_api_key>'
wallet_address = '<WALLET_ADDRESS>'
private_key = '<PRIVATE_KEY>'

# for testnet dev
swan_orchestrator: Orchestrator = swan.resource(
    api_key=api_key,
    service_name='Orchestrator',
    network="testnet",
)
# for mainnet
# swan_orchestrator: Orchestrator = swan.resource(
#     api_key=api_key,
#     network='mainnet',
#     service_name='Orchestrator'
# )

private_project = PrivateProject.build_from_local_project(
    swan_orchestrator=swan_orchestrator,
    project_path=pathlib.Path(__file__).parent / "example_private_project",
)

serialized_private_project = private_project.serialize_to_json()

# An uploaded project can be serialized and stored elsewhere and use it later
print(serialized_private_project)
private_project = PrivateProject.load_from_json(
    private_project_json_str=serialized_private_project,
)

private_task: PrivateTask = swan_orchestrator.create_private_task(
    private_project=private_project,
    wallet_address=wallet_address,
    private_key=private_key,
    hardware_id=1,
    duration=3600,
    auto_pay=True,
)

task_uuid = private_task.task_uuid

task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))

print(private_task.serialize_to_json())
private_task.deploy_task(interval=10, retries=200)

### get real url (if no url, please wait for a while, then check again)
for _ in range(100):
    result_url = swan_orchestrator.get_real_url(task_uuid)
    print(f"app url: {result_url}")
    if result_url:
        break
    time.sleep(5)