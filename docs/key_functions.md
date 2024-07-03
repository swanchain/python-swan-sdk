
## Key Functions Details

### create_task Function Details

```python
swan.resource(api_key="<your_api_key>", service_name='Orchestrator').create_task(**kwargs)
```

Creates task on SWAN orchestrator.

#### Request Syntax

```python
response = swan.resource(api_key="<your_api_key>", service_name='Orchestrator').create_task(
  wallet_address="string", 
  hardware_id=-1, 
  region="string",
  duration=3600,
  app_repo_image="string",
  job_source_uri="string",
  repo_uri="string"
  repo_branch="string",
  repo_owner="string", 
  repo_name="string",
  start_in=300, 
  auto_pay=False,
  private_key="string"
)

# To get task_uuid
response['id']
```
PARAMETERS:
- **wallet_address** (string) **[REQUIRED]** - The wallet address to be asscioated with newly create task
- **hardware_id** (integer) - id of cp/hardware configuration set. Defaults to hardware chosen in set_default_task_config. If hardware not set, will default to 0 (Free tier).
- **region** (string) - region of hardware. Defaults to global.
- **duration** (integer) - duration of service runtime in seconds. Defaults to 3600 seconds (1 hour).
- **app_repo_image** (string) - The name of a demo space. If app_repo_image is used, auto_pay will be True by default. To learn more about auto_pay, check out auto_pay parameter. If you want turn auto_pay off, set auto_pay to False
- **job_source_uri** (string) - The job source URI to be deployed. If this is provided, app_repo_image and repo_uri are ignored. The repository must contain a dockerfile
- **repo_uri** (string) - The The URI of the repo to be deployed. The repository must contain a dockerfile \
**IMPORTANT** Only one of job_source_uri, app_repo_image, and repo_uri will be used at a time, but at least 1 must be provided. The priority is job_source_uri. If job_source_uri is not provided, app_repo_image will be used. If app_repo_image is not provided, then repo_uri will be used.
- **repo_branch** (string) - branch of the repo to be deployed.
- **repo_owner** (string) - owner of the repo to be deployed.
- **repo_name** (string) - name of the repo to be deployed.
- **start_in** (integer) - unix timestamp of starting time. Defaults to 300 seconds (5 minutes)
- **auto_pay** (Boolean) - Automatically pays to deploy task if set to True. If True, private_key must be provided.
- **private_key** Wallet's private_key, only used if auto_pay is True
