import swan

api_key = '<your_api_key>'
wallet_address = '<WALLET_ADDRESS>'
private_key = '<PRIVATE_KEY>'

swan_orchestrator = swan.resource(
    api_key=api_key, 
    network='mainnet', 
    service_name='Orchestrator'
)

### check the hardware ID for other hardware types
# available_hardware = swan_orchestrator.get_hardware_config()
# print(json.dumps(available_hardware, indent=2))

result = swan_orchestrator.create_task(
    repo_uri='https://github.com/swanchain/awesome-swanchain/tree/main/Llama3-8B-LLM-Chat',
    wallet_address=wallet_address,
    private_key=private_key,
    hardware_id=13,
    duration=3600,
    auto_pay=True
)

task_uuid = result['id']

task_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(task_info)

### get real url (if no url, please wait for a while, then check again)
result_url = swan_orchestrator.get_real_url(task_uuid)
print(result_url)