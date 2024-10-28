
# Key Functions Details <!-- omit in toc -->

- [Core Functions](#core-functions)
  - [`get_instance_resources` Details](#get_instance_resources-details)
  - [`create_task` Details](#create_task-details)
  - [`get_deployment_info` Details](#get_deployment_info-details)
  - [`get_real_url` Details](#get_real_url-details)
  - [`renew_task` Details](#renew_task-details)
  - [`terminate_task` Details](#terminate_task-details)
- [Other Functions](#other-functions)
  - [`make_payment` Details](#make_payment-details)
  - [`renew_payment` Details](#renew_payment-details)
  - [`submit_payment` Details](#submit_payment-details)
  - [`validate_payment` Details](#validate_payment-details)
  - [`get_app_repo_image` Details](#get_app_repo_image-details)

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
  instance_type=None, 
)
```

PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - The task_uuid to be extended
- **duration** (integer) - id of cp/hardware configuration set. Defaults to 0 (Free tier).
- **tx_hash** (string) - The tx_hash of payment
- **auto_pay** (Boolean) - Automatically pays to extend task if set to True. If True(default), private_key must be provided.
**IMPORTANT** If auto_pay is False, tx_hash must be provided
- **private_key** (string) - Wallet's private_key, only used if auto_pay is True
- **instance_type** (string) **[REQUIRED]** - instance type of hardware config. Defaults to 'C1ae.small' (Free tier).


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


## Other Functions

Functions in this category should be used more as references to know logic behind the core functions.

### `make_payment` Details

This function consists of two steps: `submit_payment` and `validate_payment`. Only the payment for a task is validated, the task can be deployed.

```python
swan_orchestrator.make_payment(**kwargs)
```

Submit a payment to SWAN contract for a task

**Request Syntax**:

```python
response = swan_orchestrator.make_payment(
  task_uuid="string",
  private_key="string", 
  duration = 3600, 
  instance_type=None, 
)
```
PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - task_uuid of task being paid for
- **private_key** (string) **[REQUIRED]** - Wallet's private_key
- **duration** (integer) - duration of service runtime in seconds. Defaults to 3600 seconds (1 hour).
- **instance_type** (string) - instance type of hardware config. Defaults to 'C1ae.small' (Free tier).


### `renew_payment` Details

```python
swan_orchestrator.renew_payment(**kwargs)
```

Submit a payment to SWAN contract for a task

**Request Syntax**:

```python
response = swan_orchestrator.renew_payment(
  task_uuid="string",
  private_key="string", 
  duration = 3600, 
  instance_type=None, 
)
```
PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - task_uuid of task being paid for
- **private_key** (string) **[REQUIRED]** - Wallet's private_key
- **duration** (integer) - duration of service runtime in seconds. Defaults to 3600 seconds (1 hour).
- **instance_type** (string) - instance type of hardware config. Defaults to 'C1ae.small' (Free tier).


### `submit_payment` Details

```python
swan_orchestrator.submit_payment(**kwargs)
```

Submit a payment to SWAN contract for a task

**Request Syntax**:

```python
response = swan_orchestrator.submit_payment(
  task_uuid="string",
  private_key="string", 
  duration = 3600, 
  instance_type=None, 
)
```
PARAMETERS:
- **task_uuid** (string) **[REQUIRED]** - task_uuid of task being paid for
- **private_key** (string) **[REQUIRED]** - Wallet's private_key
- **duration** (integer) - duration of service runtime in seconds. Defaults to 3600 seconds (1 hour).
- **instance_type** (string) - instance type of hardware config. Defaults to 'C1ae.small' (Free tier).


### `validate_payment` Details
```python
swan_orchestrator.validate_payment(**kwargs)
```

Deploy task on orchestrator with proof of payment

**Request Syntax**:
```python
response = swan_orchestrator.validate_payment(
  tx_hash="string",
  task_uuid="string"
)
```
PARAMETERS:
- **tx_hash** (string) **[REQUIRED]** - tx_hash/receipt of payment to SWAN contract for task with task_uuid 
- **task_uuid** (string) **[REQUIRED]** - task_uuid of task being extended


### `get_app_repo_image` Details

```python
swan_orchestrator.get_app_repo_image(**kwargs)
```

Finds repository image of pre-defined applications

**Request Syntax**:

```python
response = swan_orchestrator.get_app_repo_image(
  name="string"
)
```
PARAMETERS:
- **name** (string) - If name is provided, it will return the repository image of pre-defined applications. If name is not provided, returns all repository image of pre-defined applications.

