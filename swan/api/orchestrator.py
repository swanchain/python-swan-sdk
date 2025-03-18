import json
import logging
import time
import traceback
from typing import List, Optional, Union, Dict, Any

from eth_account import Account

from swan.api_client import OrchestratorAPIClient
from swan.common.constant import *
from swan.common.exception import SwanAPIException
from swan.common.utils import validate_ip_or_cidr, parse_resource_string
from swan.contract.swan_contract import SwanContract
from swan.object import InstanceResource
from swan.object import (
    TaskCreationResult,
    TaskDeploymentInfo,
    TaskList,
    TaskRenewalResult,
    TaskTerminationMessage,
    PaymentResult,
    TaskDetail,
    GPUSelectionList,
    CustomInstanceResult
)
from swan.object.task_spec import (
    TaskSpec,
    ResourceUrlTaskSpec,
    HardwareSpec,
    GpuSpec,
    YamlTaskSpec,
    DockerfileTaskSpec, TaskSpecFactory,
)


class Orchestrator(OrchestratorAPIClient):
  
    def __init__(self, api_key: str, login: bool = True, network="mainnet", verification: bool = True, token = None, url_endpoint: str = None):
        """Initialize user configuration and login.

        Args:
            api_key: Orchestrator API key, generated through website
            login: Login into Orchestrator or Not
            url_endpoint: Selected server 'production/calibration'
        """
        self.token = token
        self.api_key = api_key
        self.contract_info = None
        self.url_endpoint = url_endpoint
        self.region = "global"
        self.all_hardware = None
        self.instance_mapping = None

        if url_endpoint:
            self.swan_url = url_endpoint
            logging.info(f"Using {url_endpoint}")
        elif network == "testnet":
            self.swan_url = ORCHESTRATOR_API_TESTNET
            logging.info("Using Testnet")
        else:
            self.swan_url = ORCHESTRATOR_API_MAINNET
            logging.info("Using Mainnet")

        if login:
            self.api_key_login()
        if self.token:
            self.get_contract_info(verification)
            self._get_instance_mapping()
        
        self._get_hardware_config()


    def api_key_login(self):
        """Login with Orchestrator API Key.

        Returns:
            A str access token for further Orchestrator API access in
            current session.
        """
        params = {"api_key": self.api_key}
        try:
            result = self._request_with_params(
                POST, SWAN_APIKEY_LOGIN, self.swan_url, params, None, None
            )
            if result["status"] == "failed":
                raise SwanAPIException("Login Failed")
            self.token = result["data"] 
            logging.info("Login Successfully!")
        except SwanAPIException as e:
            logging.error(e.message)
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())

    def _get_source_uri(
            self, 
            repo_uri,
            repo_branch=None,
            wallet_address=None, 
            instance_type=None,
            custom_instance=None
        ):
        try:
            if not wallet_address:
                raise SwanAPIException(f"No wallet_address provided")

            params = {
                "wallet_address": wallet_address,
                "repo_uri": repo_uri,
                "repo_branch": repo_branch,
                "dp": "true",
            }

            if custom_instance:
                params["custom_instance"] = json.dumps(custom_instance)
            elif instance_type:
                hardware_id = self.get_instance_hardware_id(instance_type)
                if hardware_id is None:
                    raise SwanAPIException(f"Invalid instance_type {instance_type}")
                params["hardware_id"] = hardware_id
            else:
                raise SwanAPIException(f"Missing instance_type or custom_instance")
                
            response = self._request_with_params(POST, GET_SOURCE_URI, self.swan_url, params, self.token, None)
            job_source_uri = ""
            if response and response.get('data'):
                job_source_uri = response['data']['job_source_uri']
        
            return job_source_uri
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None


    def get_contract_info(self, verification: bool = True):
        response = self._request_without_params(GET, GET_CONTRACT_INFO, self.swan_url, self.token)
        self.contract_info = response["data"]["contract_info"]["contract_detail"]
        return True
        
    def _get_hardware_config(self, available = True):
        """Query current hardware list object.
        
        Returns:
            list of HardwareConfig object.
            e.g. obj.to_dict() -> 
            {
                'id': 0, 
                'name': 'C1ae.small', 
                'description': 'CPU only · 2 vCPU · 2 GiB', 
                'type': 'CPU', 
                'region': ['North Carolina-US'], 
                'price': '0.0', 
                'status': 'available'
            }
        """
        try:
            response = self._request_without_params(GET, GET_CP_CONFIG_DP, self.swan_url, self.token)
            self.all_hardware = [InstanceResource(hardware) for hardware in response["data"]["hardware"]]
            self.instance_mapping = {hardware.instance_type: hardware.to_dict() for hardware in self.all_hardware}
            if available:
                hardwares_info = [hardware.to_dict() for hardware in self.all_hardware if hardware.status == "available"]
            else:
                hardwares_info = [hardware.to_dict() for hardware in self.all_hardware]
            return hardwares_info
        except Exception:
            logging.error("Failed to fetch hardware configurations.")
            return None
        
    def _get_instance_mapping(self):
        try:
            response = self._request_without_params(GET, GET_CP_CONFIG_DP, self.swan_url, self.token)
            self.all_hardware = [InstanceResource(hardware) for hardware in response["data"]["hardware"]]
            self.instance_mapping = {hardware.instance_type: hardware.to_dict() for hardware in self.all_hardware}
        except Exception:
            logging.error("Failed to fetch hardware configurations.")
            return None
        
    def get_instance_resources(self, available = True) -> Optional[List[InstanceResource]]:
        """Query current hardware list object.
        
        Returns:
            list of instance resource object.
            e.g. obj.to_dict() -> 
            {
                'hardware_id': 0, 
                'instance_type': 'C1ae.small', 
                'description': 'CPU only · 2 vCPU · 2 GiB', 
                'type': 'CPU', 
                'region': ['North Carolina-US'], 
                'price': '0.0', 
                'status': 'available',
                'snapshot_id': 1731004200,
                'expire_time': 1731005239
            }
        """
        try:
            response = self._request_without_params(GET, GET_CP_CONFIG_DP, self.swan_url, self.token)
            instance_res = [InstanceResource(hardware) for hardware in response["data"]["hardware"]]
            if available:
                instance_res = [instance for instance in instance_res if instance.status == "available"]
            return instance_res
        except Exception:
            logging.error("Failed to fetch instance resources.")
            return []
    
    def get_instance_hardware_id(self, instance_type):
        try:
            return self.instance_mapping[instance_type]['hardware_id']
        except:
            logging.error(f"Undefined instance type {instance_type}.")
            return None

    def get_hardware_instance(self, instance_type: str) -> Optional[Dict[str, Any]]:
        try:
            return self.instance_mapping[instance_type]
        except:
            logging.error(f"Undefined instance type {instance_type}.")
            return None
    
    def get_instance_price(self, instance_type):
        try:
            return float(self.instance_mapping[instance_type]['price'])
        except:
            logging.error(f"Undefined instance type {instance_type}.")
            return None
        
    def get_gpu_selection_list(self, region):
        try:
            params = {
                "region": region,
            }
            response = self._request_with_params(GET, GET_GPU_SELECTION_LIST, self.swan_url, params, self.token, None)
            return GPUSelectionList.load_from_resp(response)
        except Exception as e:
            logging.error(f"Failed to fetch gpu selection list. {e}")
            return None

    def get_custom_instance_result(self, custom_instance: Optional[dict] = {}, region: Optional[str] = 'global'):
        try:
            params = self.validate_custom_instance(custom_instance)
            
            if region:
                params["region"] = region

            response = self._request_with_params(POST, CUSTOM_INSTANCE, self.swan_url, params, self.token, None)
            return CustomInstanceResult.load_from_resp(response)
        except Exception as e:
            logging.error(f"Failed to fetch custom instance info. {e}")
            return None

    def validate_custom_instance(self, custom_instance: Optional[dict] = {}):
        """Validate custom instance input"""
        # gpu_model should be a string
        gpu_model = custom_instance.get("gpu_model")
        gpu_count = custom_instance.get("gpu_count")

        if gpu_count > 0:
            if not gpu_model:
                raise SwanAPIException("gpu model is not a string with gpu count is greater than 0.")

        # cpu, memory, storage and gpu_count should be integer and greater than 0
        int_inputs = ["cpu", "memory", "storage"]
        for key in int_inputs:
            if key not in custom_instance or not isinstance(custom_instance[key], int) or custom_instance[key] <= 0:
                raise SwanAPIException(f"{key} should be a positive integer")

        return custom_instance


    def terminate_task(self, task_uuid: str) -> Optional[TaskTerminationMessage]:
        """
        Terminate a task

        Args:
            task_uuid: uuid of task.

        Returns:
            TaskTerminationMessage object
        """
        try:
            params = {
                "task_uuid": task_uuid
            }

            result = self._request_with_params(
                    POST, 
                    TERMINATE_TASK, 
                    self.swan_url, 
                    params, 
                    self.token, 
                    None
                )
            
            return TaskTerminationMessage.load_from_resp(result)
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None


    def claim_review(self, task_uuid: str):
        """
        Review the uptime of a task

        Args:
            task_uuid: uuid of space task.

        Returns:
            JSON of claim successfuly of not
        """
        try:
            params = {
                "task_uuid": task_uuid
            }

            result = self._request_with_params(
                    POST, 
                    CLAIM_REVIEW, 
                    self.swan_url, 
                    params, 
                    self.token, 
                    None
                )
            
            return result
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
    
    def get_app_repo_image(self, name: str = ""):
        if not name:
            return self._request_without_params(
                GET, 
                PREMADE_IMAGE, 
                self.swan_url, 
                self.token
            )
        else:
            params = {"name": name}
            return self._request_with_params(
                GET, 
                PREMADE_IMAGE, 
                self.swan_url, 
                params, 
                self.token, 
                None
            )

    def _deploy_task(self, wallet_address: str, task_spec: TaskSpec):
        try:
            preferred_cp_list = task_spec.preferred_cp_list
            ip_whitelist = task_spec.ip_whitelist
            job_source_uri = None
            if isinstance(task_spec, ResourceUrlTaskSpec):
                job_source_uri = task_spec.get_deployment_content()
            elif isinstance(task_spec, YamlTaskSpec):
                pass
            elif isinstance(task_spec, DockerfileTaskSpec):
                pass

            preferred_cp = None
            if preferred_cp_list and isinstance(preferred_cp_list, list):
                preferred_cp = ','.join(preferred_cp_list)

            ip_whitelist_str = None
            if ip_whitelist and isinstance(ip_whitelist, list):
                # validate ip address
                for ip in ip_whitelist:
                    if not validate_ip_or_cidr(ip):
                        raise SwanAPIException(f"Invalid ip address: {ip}")
                ip_whitelist_str = ','.join(ip_whitelist)

            region = task_spec.region
            instance_type = task_spec.hardware_spec.instance_type
            if instance_type is not None:
                # instance_type not none, this is not custom config
                custom_instance = None
            else:
                # custom config

                gpu_spec: GpuSpec = task_spec.hardware_spec.gpus[0] if task_spec.hardware_spec.gpus else None
                custom_instance = {
                    "cpu": task_spec.hardware_spec.cpu,
                    "memory": task_spec.hardware_spec.memory,
                    "storage": task_spec.hardware_spec.storage,
                }
                if gpu_spec:
                    custom_instance["gpu_model"] = gpu_spec.gpu_model
                    custom_instance["gpu_count"] = gpu_spec.count
                else:
                    custom_instance["gpu_model"] = None
                    custom_instance["gpu_count"] = 0

            # validate wallet address should be corresponding to the payment private key
            if task_spec.auto_pay_private_key is not None:
                # Create an Account object from the private key
                account = Account.from_key(task_spec.auto_pay_private_key)
                if account.address != wallet_address:
                    raise SwanAPIException(f"Wallet address {wallet_address} "
                                           f"should be corresponding to the auto payment wallet: {account.address}")

            # create task deployment
            params = {
                "duration": task_spec.duration_in_secs,
                "cfg_name": instance_type,
                "region": region,
                "start_in": 600,
                "wallet": wallet_address,
                "job_source_uri": job_source_uri,
                "deploy_type": int(task_spec.deploy_type.value),
                "deploy_content": task_spec.get_deployment_content(),
            }
            if preferred_cp:
                params["preferred_cp"] = preferred_cp
            if ip_whitelist_str:
                params["ip_whitelist"] = ip_whitelist_str

            if custom_instance:
                params["custom_instance"] = json.dumps(custom_instance)
                custom_instance_result: CustomInstanceResult = self.get_custom_instance_result(custom_instance, region)
                if not custom_instance_result:
                    raise SwanAPIException(f"Please check your custom instance input.")
                if not custom_instance_result.available:
                    raise SwanAPIException(f"Custom instance {custom_instance} is not available in {region}.")
            else:
                if not self._verify_hardware_region(instance_type, region):
                    raise SwanAPIException(f"No {instance_type} machine in {region}.")

            result = self._request_with_params(
                POST,
                CREATE_TASK,
                self.swan_url,
                params,
                self.token,
                None
            )

            try:
                task_uuid = result['data']['task']['uuid']
            except Exception as e:
                raise SwanAPIException(f"Task creation failed, {str(e)}.")

            tx_hash = None
            tx_hash_approve = None
            config_order = None
            amount = None
            if task_spec.auto_pay_private_key:
                config_result = self.make_payment(
                    task_uuid=task_uuid,
                    duration=task_spec.duration_in_secs,
                    private_key=task_spec.auto_pay_private_key,
                )
                if config_result and isinstance(config_result, dict):
                    tx_hash = config_result.get('tx_hash')
                    config_order = config_result.get('data')
                    tx_hash_approve = config_result.get('tx_hash_approve')
                    amount = config_result.get('amount')

            result['config_order'] = config_order
            result['tx_hash'] = tx_hash
            result['tx_hash_approve'] = tx_hash_approve
            result['id'] = task_uuid
            result['task_uuid'] = task_uuid
            result['instance_type'] = instance_type
            result['price'] = amount

            # logging.info(f"Task created successfully, {task_uuid=}, {tx_hash=}, {instance_type=}")
            return TaskCreationResult.load_from_resp(result)

        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
        return None

    def create_task(
            self,
            wallet_address: str, 
            instance_type: Optional[str] = None, 
            region: Optional[str] = "global",
            duration: Optional[int] = 3600, 
            app_repo_image: Optional[str] = None,
            job_source_uri: Optional[str] = None, 
            repo_uri: Optional[str] = None,
            repo_branch: Optional[str] = None,
            auto_pay: Optional[bool] = True,
            private_key: Optional[str] = None,
            start_in: Optional[int] = None,
            preferred_cp_list: Optional[List[str]] = None,
            ip_whitelist: Optional[List[str]] = None,
            custom_instance: Optional[dict] = None,
            base_task_spec: Optional[Union[YamlTaskSpec, DockerfileTaskSpec]] = None,
        ) -> Optional[TaskCreationResult]:
        """
        Create a task via the orchestrator.

        Args:
            wallet_address: The user's wallet address.
            instance_type: The type(name) of the hardware. (Default = `C1ae.small`)
            region: The region of the hardware. (Default: global)
            duration: The duration of the service runtime in seconds. (Default = 3600)
            app_repo_image: Optional. The name of a demo space.
            job_source_uri: Optional. The job source URI to be deployed. If this is provided, app_repo_image and repo_uri are ignored.
            repo_uri: Optional. The URI of the repo to be deployed. If job_source_uri and app_repo_image are not provided, this is required.
            repo_branch: Optional. The branch of the repo to be deployed. In the case that repo_uri is provided, if repo_branch is given, it will be used.
            start_in: Optional. The starting time (expected time for the app to be deployed, not mandatory). (Default = 300)
            auto_pay: Optional. Automatically call the submit payment method on the contract and validate payment to get the task deployed. 
            If True, the private key and wallet must be in .env (Default = False). Otherwise, the user must call the submit payment method on the contract and validate payment.
            private_key: Optional. The wallet's private key, only used if auto_pay is True.
            preferred_cp_list: Optional. A list of preferred cp account address(es).
            ip_whitelist: Optional. A list of IP addresses which can access the application.
            custom_instance: Optional. A dictionary containing custom instance information. If provided, instance_type is ignored.
            base_task_spec: Optional. A predefined task specification,
        
        Raises:
            SwanExceptionError: If neither app_repo_image nor job_source_uri is provided.
            
        Returns:
            TaskCreationResult object
        """
        try:
            if not wallet_address:
                raise SwanAPIException(f"No wallet_address provided, please pass in a wallet_address")

            if auto_pay:
                if not private_key:
                    raise SwanAPIException(f"please provide private_key")

            if not region:
                region = 'global'

            if not duration or duration < 3600:
                raise SwanAPIException(f"Duration must be no less than 3600 seconds")

            if not custom_instance and not instance_type and not base_task_spec:
                raise SwanAPIException(f"Please provide either custom_instance or instance_type or deploy_task_spec "
                                       f"to determine the hardware configuration")

            hardware_spec: Optional[HardwareSpec] = None
            if custom_instance:
                logging.info(f"Input custom instance {custom_instance}, {region=} {duration=} (seconds)")
                custom_instance = self.validate_custom_instance(custom_instance)
                hardware_spec = HardwareSpec(
                    cpu=custom_instance.get("cpu"),
                    memory=custom_instance.get("memory"),
                    storage=custom_instance.get("storage"),
                    gpus=[
                        GpuSpec(gpu_model=custom_instance.get("gpu_model"), count=custom_instance.get("gpu_count"))
                    ],
                    instance_type=None,
                )
            elif instance_type:
                hardware_instance = self.get_hardware_instance(instance_type=instance_type)

                if hardware_instance is None:
                    raise SwanAPIException(f"Invalid instance_type {instance_type}")
                hardware_description = hardware_instance.get("description")
                hardware_description_dict = parse_resource_string(resource_string=hardware_description)
                hardware_spec = HardwareSpec(
                    cpu=hardware_description_dict.get("cpu"),
                    memory=hardware_description_dict.get("memory"),
                    storage=hardware_description_dict.get("storage"),
                    gpus=[
                        GpuSpec(gpu_model=hardware_description_dict.get("gpu_model"),
                                count=hardware_description_dict.get("gpu_count"))
                    ],
                    instance_type=instance_type,
                )
                logging.info(f"Input instance {instance_type}, {region=} {duration=} (seconds)")

            elif base_task_spec:
                # no extra handling for the task data source if a task spec is passing in
                pass

            if not job_source_uri and not base_task_spec:
                if app_repo_image:
                    if auto_pay == None and private_key:
                        auto_pay = True
                    repo_res = self.get_app_repo_image(app_repo_image)
                    if repo_res and repo_res.get("status", "") == "success":
                        repo_uri = repo_res.get("data", {}).get("url", "")
                        if repo_uri == "":
                            raise SwanAPIException(f"Invalid app_repo_image url")
                    else:
                        raise SwanAPIException(f"Invalid app_repo_image")

                if repo_uri:
                    job_source_uri = self._get_source_uri(
                        repo_uri=repo_uri,
                        repo_branch=repo_branch,
                        wallet_address=wallet_address,
                        instance_type=instance_type,
                        custom_instance=custom_instance
                    )
                else:
                    raise SwanAPIException(f"Please provide app_repo_image, or job_source_uri, or repo_uri")

            if not job_source_uri and not base_task_spec:
                raise SwanAPIException(f"Cannot get task deployment content, we need a job_source_uri or "
                                       f"dockerfile/yaml deployment file content. Please double check your parameters")

            logging.info(f"Using deployment content: {job_source_uri=} {base_task_spec=}")

            if base_task_spec is None:
                base_task_spec = TaskSpecFactory.build_resource_url_task(
                    resource_url=job_source_uri,
                    hardware_spec=hardware_spec,
                    region=region,
                    start_in=start_in,
                    duration_in_secs=duration,
                    auto_pay_private_key=auto_pay and private_key,
                    preferred_cp_list=preferred_cp_list,
                    ip_whitelist=ip_whitelist,
                )

            else:
                # deploy_task_spec is not None,
                # if there are non-default arguments, override the arguments to the deploy_task_spec
                #
                if wallet_address:
                    base_task_spec.wallet_address = wallet_address
                if job_source_uri:
                    base_task_spec.resource_uri = job_source_uri
                if hardware_spec:
                    # override from custom instance or instance type
                    base_task_spec.hardware_spec = hardware_spec
                if region != "global":
                    base_task_spec.region = region
                if start_in is not None:
                    base_task_spec.start_in = start_in
                if duration:
                    base_task_spec.duration_in_secs = duration
                if auto_pay and private_key:
                    base_task_spec.auto_pay_private_key = private_key
                if preferred_cp_list:
                    base_task_spec.preferred_cp_list = preferred_cp_list
                if ip_whitelist:
                    base_task_spec.ip_whitelist = ip_whitelist
                if isinstance(base_task_spec, YamlTaskSpec):
                    if not base_task_spec.yaml_content:
                        raise SwanAPIException(f"yaml_content of deploy_task_spec object should not be empty")
                elif isinstance(base_task_spec, DockerfileTaskSpec):
                    if not base_task_spec.dockerfile_content:
                        raise SwanAPIException(f"dockerfile_content of deploy_task_spec object should not be empty")

            return self._deploy_task(wallet_address=wallet_address, task_spec=base_task_spec)
        except Exception as e:
            logging.exception(e)


    def estimate_payment(self, duration: float = 3600, instance_type: str = None):
        """Estimate required amount.

        Args:
            duration: duration in seconds for task runtime.
            instance_type: instance type, e.g. C1ae.small
        
        Returns:
            int estimated price in SWAN.
            e.g. (price = 10 SWAN, duration = 1 hr (3600 seconds)) -> 10 SWAN
        """
        try:
            price = self.get_instance_price(instance_type=instance_type)
            duration_hour = duration/3600
            amount = price * duration_hour
            return amount
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
        
    def approve_allowance(self, private_key: str, amount: float):
        """
        Approve in advance for the contract

        Args:
            private_key: private key of owner
            amount: amount to approve (in ether)

        Returns:
            tx_hash
        """
        try:
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            contract = SwanContract(private_key, self.contract_info)
            logging.info(f"Approving in advance (in ether), {amount=}")
            amount_wei = contract.to_wei(amount)
            tx_hash = contract.approve_payment(amount_wei)
            logging.info(f"Approved in advance (in ether), {amount=}. Got {tx_hash=}")
            return tx_hash
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
        
    def get_allowance(self, private_key: str):
        """
        Get allowance of the contract

        Args:
            private_key: private key of owner

        Returns:
            allowance in ether
        """
        try:
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            contract = SwanContract(private_key, self.contract_info)
            allowance = contract.get_allowance()
            amount = contract.from_wei(allowance)
            logging.info(f"Got allowance (in ether), {amount=}")
            return amount
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
    
    def submit_payment(
            self, 
            task_uuid, 
            private_key, 
            duration = 3600, 
            **kwargs
        ) -> Optional[PaymentResult]:
        """
        Submit payment for a task

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            private_key: private key of owner
            duration: duration of service runtime (seconds).

        Returns:
            tx_hash
        """
        try:
            task_detail: TaskDetail = self.get_task_detail(task_uuid)
            hardware_id = task_detail.hardware_id
            price_per_hour = float(task_detail.price_per_hour)
            if hardware_id is None:
                raise SwanAPIException(f"Invalid hardware_id for task {task_uuid}")
            
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            contract = SwanContract(private_key, self.contract_info)
        
            payment: PaymentResult = contract.submit_payment(
                task_uuid=task_uuid, 
                hardware_id=hardware_id, 
                price_per_hour=price_per_hour,
                duration=duration
            )
            logging.info(f"Payment submitted, {task_uuid=}, {duration=}, {hardware_id=}. Got {payment.tx_hash=}")
            return payment
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def renew_payment(
            self, 
            task_uuid, 
            private_key, 
            duration = 3600, 
            **kwargs
        ) -> Optional[PaymentResult]:
        """
        Submit payment for a task

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            private_key: private key of owner
            duration: duration of service runtime (seconds).

        Returns:
            tx_hash
        """
        try:
            task_detail: TaskDetail = self.get_task_detail(task_uuid)
            hardware_id = task_detail.hardware_id
            price_per_hour = float(task_detail.price_per_hour)
            if hardware_id is None:
                raise SwanAPIException(f"Invalid hardware_id {hardware_id}")
            
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            contract = SwanContract(private_key, self.contract_info)
        
            payment: PaymentResult = contract.renew_payment(
                task_uuid=task_uuid, 
                hardware_id=hardware_id, 
                price_per_hour=price_per_hour,
                duration=duration
            )
            logging.info(f"Payment submitted, {task_uuid=}, {duration=}, {hardware_id=}. Got {payment.tx_hash=}")
            return payment
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def validate_payment(
            self,
            tx_hash,
            task_uuid
        ):
        """
        Validate payment for a task on SWAN backend

        Args:
            tx_hash: tx_hash of submitted payment
            task_uuid: unique id returned by `swan_api.create_task`

        Returns:
            JSON response from backend server including 'task_uuid'.
        """
        
        try:
            if tx_hash and task_uuid:
                params = {
                    "tx_hash": tx_hash,
                    "task_uuid": task_uuid
                }
                result = self._request_with_params(
                    POST, 
                    TASK_PAYMENT_VALIDATE, 
                    self.swan_url, 
                    params, 
                    self.token, 
                    None
                )
                logging.info(f"Payment validation request sent, {task_uuid=}, {tx_hash=}")
                return result
            else:
                raise SwanAPIException(f"{tx_hash=} or {task_uuid=} invalid")
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
    
    def make_payment(self, 
                     task_uuid, 
                     private_key, 
                     duration=3600
                     ):
        """
        Submit payment for a task and validate it on SWAN backend

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            duration: duration of service runtime (seconds).
        
        Returns:
            JSON response from backend server including 'task_uuid'.
        """
        try:
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            if payment := self.submit_payment(
                task_uuid=task_uuid, 
                duration=duration, 
                private_key=private_key, 
            ):
                time.sleep(3)
                if res := self.validate_payment(
                    tx_hash=payment.tx_hash, 
                    task_uuid=task_uuid
                ):
                    res['tx_hash'] = payment.tx_hash
                    res['tx_hash_approve'] = payment.tx_hash_approve
                    res['amount'] = payment.amount
                    logging.info(f"Payment and validation submitted successfully, {task_uuid=}, {payment}")
                    return res
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
        return None
    

    def renew_task(
            self, 
            task_uuid: str, 
            duration: int = 3600, 
            tx_hash: Optional[str] = None, 
            auto_pay: Optional[bool] = True, 
            private_key: Optional[str] = None, 
            **kwargs
        ) -> Optional[TaskRenewalResult]:
        """
        Submit payment for a task renewal (if necessary)
        Extend a task

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            duration: duration of service runtime (seconds).
            tx_hash: (optional)tx_hash of submitted payment
            private_key: (required if no tx_hash)
            auto_pay: (required True if no tx_hash but with private_key provided)
        
        Returns:
            TaskRenewalResult object
        """
        try:
            if not (auto_pay and private_key) and not tx_hash:
                raise SwanAPIException(f"auto_pay off or tx_hash not provided, please provide a tx_hash or set auto_pay to True and provide private_key")

            tx_hash_approve = None
            amount = None
            if not tx_hash:
                payment: PaymentResult = self.renew_payment(
                    task_uuid=task_uuid, 
                    duration=duration, 
                    private_key=private_key
                )
                if payment:
                    logging.info(f"renew payment transaction hash, {payment=}")
                    tx_hash = payment.tx_hash
                    tx_hash_approve = payment.tx_hash_approve
                    amount = payment.amount
                else:
                    logging.warning(f"renwal payment failed, {task_uuid=}, {duration=}")
                    return None
            else:
                logging.info(f"will use given payment transaction hash, {tx_hash=}")
                amount = self.estimate_payment(
                    duration=duration, 
                    instance_type=self.get_task_instance_type(task_uuid)
                )

            if tx_hash and task_uuid:
                params = {
                    "task_uuid": task_uuid,
                    "duration": duration,
                    "tx_hash": tx_hash
                }

                result = self._request_with_params(
                        POST, 
                        RENEW_TASK, 
                        self.swan_url, 
                        params, 
                        self.token, 
                        None
                    )
                result.update({
                    "tx_hash_approve": tx_hash_approve,
                    "tx_hash": tx_hash,
                    "price": amount,
                    "task_uuid": task_uuid
                })
                logging.info(f"Task renewal request sent successfully, {task_uuid=} {tx_hash=}, {duration=}")
                return TaskRenewalResult.load_from_resp(result)
            else:
                raise SwanAPIException(f"{tx_hash=} or {task_uuid=} invalid")
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
        

    def get_config_order_status(self, task_uuid: str, tx_hash: str):
        """
        Get the status of a task order (for example, a task renewal order)
        
        Args:
            task_uuid: uuid of task.
            tx_hash: transaction hash of the payment.
        """

        try:
            if not task_uuid:
                raise SwanAPIException(f"Invalid task_uuid")
            
            if not tx_hash:
                raise SwanAPIException(f"Invalid tx_hash")

            params = {
                "task_uuid": task_uuid,
                "tx_hash": tx_hash
            }

            result = self._request_with_params(
                    POST, 
                    CONFIG_ORDER_STATUS, 
                    self.swan_url, 
                    params, 
                    self.token, 
                    None
                )
            logging.info(f"getting config order status request sent successfully, {task_uuid=} {tx_hash=}")
            return result
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
        
        
    def get_deployment_info(self, task_uuid: str) -> Optional[TaskDeploymentInfo]:
        """Retrieve deployment info of a deployed space with task_uuid.

        Args:
            task_uuid: uuid of space task, in deployment response.

        Returns:
            TaskDeploymentInfo object
        """
        try:
            response = self._request_without_params(GET, DEPLOYMENT_INFO+task_uuid, self.swan_url, self.token)
            return TaskDeploymentInfo.load_from_resp(response)
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None


    def get_task_list(self, 
            wallet_address: str,
            page: int = 1,
            size: int = 5,
        ) -> Optional[TaskList]:
        """
        Get the list of tasks for a wallet address

        Args:
            wallet_address: wallet address of the user
            page: page number
            size: number of tasks per page

        Returns:
            TaskList object
        """
        try:
            params = {
                "wallet_address": wallet_address,
                "page": page,
                "size": size
            }
            response = self._request_with_params(
                GET, 
                TASK_LIST, 
                self.swan_url, 
                params,
                self.token,
                None
            )
            return TaskList.load_from_resp(response)
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None


    def get_real_url(self, task_uuid: str) -> Optional[List[str]]:
        task_info: TaskDeploymentInfo = self.get_deployment_info(task_uuid)
        try:
            jobs = task_info['jobs']
            deployed_url = []
            for job in jobs:
                try:
                    if job['job_real_uri']:
                        deployed_url.append(job['job_real_uri'])
                except:
                    continue
            return deployed_url
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def get_payment_info(self):
        """Retrieve payment information from the orchestrator after making the payment.
        """
        try:
            payment_info = self._request_without_params(
                GET, PROVIDER_PAYMENTS, self.swan_url, self.token
            )
            return payment_info
        except:
            logging.error("An error occurred while executing get_payment_info()")
            return None

    def _verify_hardware_region(self, instance_type: str, region: str):
        """Verify if the hardware exist in given region.

        Args:
            instance_type: cfg name (hardware name).
            region: geological regions.

        Returns:
            True when hardware exist in given region.
            False when hardware does not exist or do not exit in given region.
        """
        self._get_hardware_config()  # make sure all_hardware is updated all the time
        for hardware in self.all_hardware:
            if hardware.instance_type == instance_type:
                if region in hardware.region or (region.lower() == 'global' and hardware.status == 'available'):
                    return True
        return False


    def get_task_instance_type(self, task_uuid: str) -> Optional[str]:
        try:
            if not task_uuid:
                raise SwanAPIException(f"Invalid task_uuid")
            task_info: TaskDeploymentInfo = self.get_deployment_info(task_uuid)
            if not task_info:
                raise SwanAPIException(f"Get task {task_uuid} failed")
            if not task_info.task.uuid:
                raise SwanAPIException(f"Task {task_uuid} not found")
            return task_info['task']['task_detail']['hardware']
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def get_task_detail(self, task_uuid: str) -> Optional[TaskDetail]:
        try:
            if not task_uuid:
                raise SwanAPIException(f"Invalid task_uuid")
            task_info: TaskDeploymentInfo = self.get_deployment_info(task_uuid)
            if not task_info or not task_info.task or not task_info.task.task_detail:
                raise SwanAPIException(f"Get task {task_uuid} failed")
            if not task_info.task.uuid:
                raise SwanAPIException(f"Task {task_uuid} not found")
            return task_info.task.task_detail
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None