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

```py
import json
import swan

swan_orchestrator = swan.resource(api_key='<SWAN_API_KEY>', service_name='Orchestrator')

result = swan_orchestrator.create_task(
    repo_uri='<YOUR-GITHUB-REPO-URI-FOR-SSH>',
    wallet_address='<WALLET_ADDRESS>',
    private_key='<PRIVATE_KEY>',
    instance_type='C1ae.small'
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
