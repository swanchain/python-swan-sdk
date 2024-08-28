# %%
import swan
import json

api_key = '53Qkrwdeyv'
wallet_address = '0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224'
private_key = 'db397b2a11d152150a4c13da03505578cac58c9b9ac3fef1d26c7c9d9d6447c8'

# %%
swan_orchestrator = swan.resource(
    api_key=api_key, 
    network='testnet',
    service_name='Orchestrator'
)

# %% get task deployment info
task_uuid = 'd1f2d461-7d9d-4c97-ab1b-6073d7dfcb28'

task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))

# %% get real url
result_url = swan_orchestrator.get_real_url(task_uuid)
print(result_url)

# %% get instance resource
instance_resources = swan_orchestrator.get_instance_resources()
print(json.dumps(instance_resources, indent=2))

# %% get instance mapping
print(json.dumps(swan_orchestrator.instance_mapping, indent=2, ensure_ascii=False))

# %% get hardware id
hardware_id = swan_orchestrator.get_instance_hardware_id('G1ae.medium')
print(hardware_id)

# %% 
swan_orchestrator.instance_mapping['G1ae.medium']['price']

# %%
result = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/ChainNode',
    wallet_address=wallet_address,
    private_key=private_key,
    instance_type='C1ae.medium',
    auto_pay=True
)

# %%
task_uuid = result['task_uuid']
instance_type = result['instance_type']
task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_info, indent=2))

# %%
### get real url (if no url, please wait for a while, then check again)
result_url = swan_orchestrator.get_real_url(task_uuid)
print(result_url)
# %%

# %% renew task
renew_result = swan_orchestrator.renew_task(
    task_uuid=task_uuid, 
    duration=3600, # Optional: default 3600 seconds (1 hour)
    auto_pay=True, 
    private_key=private_key,
    instance_type=instance_type
)
# %% terminate task
terminate_result = swan_orchestrator.terminate_task(
    task_uuid=task_uuid
)

# %%
