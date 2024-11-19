# Guide to deploy SSH Application

## SSH repo

1. fork GitHub repo: https://github.com/sonic-chain/sdk-demo
2. On your local computer, generate ssh key with `ssh-keygen -t rsa -b 4096`
3. Copy the public key as the value of sshkey in deploy.yaml

```yaml
version: "2.0"
type: node-port
services:
  vm:
    image: filswan/ubuntu-ssh-user:22.04
    env:
      - sshkey=<YOUR-LOCAL-SSH-KEY>
      - username=swantouser
    expose:
        - port: 22
        - port: 30002
        - port: 30003
        - port: 30004
        - port: 30005
        - port: 30006
        - port: 30007
deployment:
  vm:
    lagrange:
      count: 1
```

4. Push modification to your GitHub repo

## Deploy SSH Application with Swan SDK

1. Choose a computing provider who can support SSH application

```py
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

available_instances = swan_orchestrator.get_instance_resources()
print(available_instances)
```

In the output of available resources list, choose a `cp_account_address` in `ssh_ready` list of the instance type you want (such as `C1ae.small`):

```
[InstanceResource({
  "hardware_id": 0,
  "instance_type": "C1ae.small",
  "description": "CPU only \u00b7 2 vCPU \u00b7 2 GiB",
  "type": "CPU",
  "region": [
    "Virginia-US",
    "Quebec-CA",
    "Jakarta-ID",
    "Kowloon City-HK",
    "North Rhine-Westphalia-DE",
    "Seoul-KR",
    "Eastern-HK",
    "Ivano-Frankivsk Oblast-UA",
    "Kowloon-HK",
    "Saxony-DE",
    "Jiangsu-CN",
    "Tokyo-JP",
    "Kuala Lumpur-MY",
    "North West-SG",
    "Central and Western District-HK",
    "Central and Western-HK",
    "National Capital Territory of Delhi-IN",
    "Florida-US"
  ],
  "price": "0.48",
  "status": "available",
  "snapshot_id": 1732047600,
  "expiry_time": 1732048445,
  "ssh_ready": [
    {
      "cp_account_address": "0xEf675CA43Ce25b2594079caCE98C7362733E1F5B",
      "region": "Quebec-CA"
    },
    {
      "cp_account_address": "0x4cbe96669516961Ebaf7225Fe07a34d56c4B2B12",
      "region": "North West-SG"
    },
    {
      "cp_account_address": "0x34378963383667F87b5C185A7b716c2C353EF9d2",
      "region": "Florida-US"
    }
  ]
```

2. Deploy SSH application with the selected CP

Deploy the SSH application to use that `cp_account_address`, put it in the `preferred_cp_list`.

```py
result = swan_orchestrator.create_task(
    repo_uri='<YOUR-GITHUB-REPO-URI-FOR-SSH>',
    wallet_address='<WALLET_ADDRESS>',
    private_key='<PRIVATE_KEY>',
    instance_type='<INSTANCE_TYPE>', #such as 'C1ae.small',
    preferred_cp_list=['SSH-READY-CP-ACCOUNT-ADDRESS']
)
task_uuid = result['task_uuid']
# Get task deployment info
task_deployment_info = swan_orchestrator.get_deployment_info(task_uuid=task_uuid)
print(json.dumps(task_deployment_info.to_dict(), indent=2))
```

Please wait for awhile to get the SSH command by

```py
app_urls = swan_orchestrator.get_real_url(task_uuid)
```

If everything goes well, you will get SSH command result like this:

```
['ssh root@38.80.81.17 -p30001']
```

Then you can run this command in your shell. You will see something like the following output:

```
 _                                            
| |                                           
| |     __ _  __ _ _ __ __ _ _ __   __ _  ___ 
| |    / _` |/ _` | '__/ _` | '_ \ / _` |/ _ \
| |___| (_| | (_| | | | (_| | | | | (_| |  __/
|______\__,_|\__, |_|  \__,_|_| |_|\__, |\___|
              __/ |                 __/ |     
             |___/                 |___/      
Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.4.0-174-generic x86_64)

 * Documentation:  https://docs.lagrangedao.org
 * Support:        https://discord.com/invite/8vaB6rKSAu

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@sdk-demo-e5tv:~# 
```
