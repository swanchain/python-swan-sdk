
# Key Functions Details <!-- omit in toc -->

- [Core Functions](#core-functions)
  - [`get_instance_resources` Details](#get_instance_resources-details)
  - [`create_task` Details](#create_task-details)
  - [`get_deployment_info` Details](#get_deployment_info-details)
  - [`get_real_url` Details](#get_real_url-details)
  - [`renew_task` Details](#renew_task-details)
  - [`terminate_task` Details](#terminate_task-details)

## Core Functions

### `get_instance_resources` Details

```python
swan_orchestrator.get_instance_resources(**kwargs)
```

Get a list of instance resources (available or all). The full list of resource configurations can be used as a full reference to the definition of instance configurations.

**Request Syntax**:

```python
response = swan_orchestrator.get_instance_resources(available = True)
```

PARAMETERS:
- **available** (boolean) - indicate to show resources are available or all. If True, returned list only contains available resources, otherwise, all resource configurations will be returned.



### `create_task` Details

```python
swan_orchestrator.create_task(**kwargs)
```

Creates task on SWAN orchestrator.

**Request Syntax**:

```python
response = swan_orchestrator.create_task(
  wallet_address="string", 
  instance_type="string", 
  region="string",
  duration=3600,
  app_repo_image="string",
  job_source_uri="string",
  repo_uri="string",
  repo_branch="string",
  auto_pay=True,
  private_key="string",
  preferred_cp_list="list"
  ip_whitelist="list"
)
```

PARAMETERS:
- **wallet_address** (string) **[REQUIRED]** - The wallet address to be asscioated with newly create task
- **instance_type** (string) - instance type of hardware config. Defaults to 'C1ae.small' (Free tier).
- **region** (string) - region of hardware. Defaults to global.
- **duration** (integer) - duration of service runtime in seconds. Defaults to 3600 seconds (1 hour).
- **app_repo_image** (string) - The name of a demo space. If app_repo_image is used, auto_pay will be True by default. To learn more about auto_pay, check out auto_pay parameter. If you want turn auto_pay off, set auto_pay to False
- **job_source_uri** (string) - The job source URI to be deployed. If this is provided, app_repo_image and repo_uri are ignored. The repository must contain a dockerfile
- **repo_uri** (string) - The The URI of the repo to be deployed. The repository must contain a dockerfile. Please see [repo_uri](repo_uri.md)
- **repo_branch**: (string). The branch of the repo to be deployed. In the case that repo_uri is provided, if repo_branch is given, it will be used. Please see [repo_uri](repo_uri.md)
**IMPORTANT** Only one of job_source_uri, app_repo_image, and repo_uri will be used at a time, but at least 1 must be provided. The priority is job_source_uri. If job_source_uri is not provided, app_repo_image will be used. If app_repo_image is not provided, then repo_uri will be used.
- **auto_pay** (Boolean) - Automatically pays to deploy task if set to True. If True(default), private_key must be provided.
- **private_key** (string) - Wallet's private_key, only used if auto_pay is True
- **preferred_cp_list**: (list) - A list of preferred cp account addresses.
- **ip_whitelist**: (list) - A list of IP addresses which can access the application.


### `get_deployment_info` Details

```python
swan_orchestrator.get_deployment_info(**kwargs)
```

Get deployment information about a task

**Request Syntax**:

```python
response = swan_orchestrator.get_deployment_info(
  task_uuid="string"
)
```
PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - The task_uuid to get status of.


### `get_real_url` Details

```python
swan_orchestrator.get_real_url(**kwargs)
```

Get real url of task

**Request Syntax**:

```python
response = swan_orchestrator.get_real_url(
  task_uuid="string"
)
```
PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - Get real url of task at task_uuid


### `renew_task` Details
```python
swan_orchestrator.renew_task(**kwargs)
```

Renews a task

```python
response = swan_orchestrator.renew_task(
  task_uuid="string"
  duration=3600, 
  tx_hash="string", 
  auto_pay = True, 
  private_key="string", 
)
```

PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - The task_uuid to be extended
- **duration** (integer) - Duration to extend (default to 3600 seconds)
- **tx_hash** (string) - Optional. The tx_hash of payment
- **auto_pay** (Boolean) - Automatically pays to extend task if set to True. If True(default), private_key must be provided. (default to True)
**IMPORTANT** If auto_pay is False, tx_hash must be provided
- **private_key** (string) - Wallet's private_key, only used if auto_pay is True


### `terminate_task` Details

```python
swan_orchestrator.terminate_task(**kwargs)
```

Terminates a task and gives a refund based on time remaining

**Request Syntax**:

```python
response = swan_orchestrator.terminate_task(
  task_uuid="string"
)
```
PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - The task_uuid to be terminates

