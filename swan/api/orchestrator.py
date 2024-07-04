import logging
import traceback
import json
import time

from eth_account import Account
from eth_account.messages import encode_defunct

from swan.api_client import APIClient
from swan.common.constant import *
from swan.object import HardwareConfig
from swan.common.exception import SwanAPIException
from swan.contract.swan_contract import SwanContract

class Orchestrator(APIClient):
  
    def __init__(self, api_key: str, login: bool = True, network="testnet", verification: bool = True, token = None, url_endpoint: str = None):
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
        self.cfg_name = None
        self.hardware_id_free = 0
        self.wallet_address = None
        self.region = "global"
        self.all_hardware = None

        if url_endpoint:
            self.swan_url = url_endpoint
        elif network == "mainnet":
            self.swan_url = ORCHESTRATOR_API_MAINNET
        else:
            self.swan_url = ORCHESTRATOR_API_TESTNET

        if login:
            self.api_key_login()
        if self.token:
            pub_addr = ORCHESTRATOR_PUBLIC_ADDRESS_MAINNET if network == "mainnet" else ORCHESTRATOR_PUBLIC_ADDRESS_TESTNET
            self.get_contract_info(verification, orchestrator_public_address=pub_addr)
        
        self.get_hardware_config()


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

    def get_source_uri(
            self, 
            repo_uri,
            wallet_address=None, 
            hardware_id=None,
            repo_branch=None,
            repo_owner=None, 
            repo_name=None,
        ):
        try:
            if hardware_id == None:
                raise SwanAPIException(f"No hardware_id provided")
            
            if not wallet_address:
                raise SwanAPIException(f"No wallet_address provided")

            params = {
                "repo_owner": repo_owner,
                "repo_name": repo_name,
                "repo_branch": repo_branch,
                "wallet_address": wallet_address,
                "hardware_id": hardware_id,
                "repo_uri": repo_uri
            }
            response = self._request_with_params(POST, GET_SOURCE_URI, self.swan_url, params, self.token, None)
            job_source_uri = ""
            if response and response.get('data'):
                job_source_uri = response['data']['job_source_uri']
        
            return job_source_uri
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None


    def get_contract_info(self, verification: bool = True, orchestrator_public_address = ORCHESTRATOR_PUBLIC_ADDRESS_TESTNET):
        response = self._request_without_params(GET, GET_CONTRACT_INFO, self.swan_url, self.token)
        if verification:
            if not self.contract_info_verified(
                response["data"]["contract_info"], 
                response["data"]["signature"], 
                orchestrator_public_address
            ):
                return False
        self.contract_info = response["data"]["contract_info"]["contract_detail"]
        return True
    
    def contract_info_verified(
            self, 
            contract_info, 
            signature, 
            orchestrator_public_address = ORCHESTRATOR_PUBLIC_ADDRESS_TESTNET
        ):
        message_json = json.dumps(contract_info)
        msghash = encode_defunct(text=message_json)
        public_address = Account.recover_message(msghash, signature=signature)
        if public_address == orchestrator_public_address:
            return True
        return False
        
    def get_hardware_config(self, available = True):
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
            response = self._request_without_params(GET, GET_CP_CONFIG, self.swan_url, self.token)
            self.all_hardware = [HardwareConfig(hardware) for hardware in response["data"]["hardware"]]
            if available:
                hardwares_info = [hardware.to_dict() for hardware in self.all_hardware if hardware.status == "available"]
            else:
                hardwares_info = [hardware.to_dict() for hardware in self.all_hardware]
            return hardwares_info
        except Exception:
            logging.error("Failed to fetch hardware configurations.")
            return None
    
    def get_cfg_name(self, hardware_id=0):
        try:
            self.get_hardware_config()  # make sure all_hardware is updated all the time
            hardware = [hardware for hardware in self.all_hardware if hardware.id == hardware_id][0]
            cfg_name = hardware.name
            return cfg_name
        except:
            logging.error("Failed to set hardware configurations.")
            return None
    
    def get_config(self):
        current_config = {
                    "hardware_id": self.hardware_id_free,
                    "cfg_name": self.cfg_name,
                    "region": self.region
                }
        return current_config

    def terminate_task(self, task_uuid: str):
        """
        Terminate a task

        Args:
            task_uuid: uuid of space task.

        Returns:
            JSON of terminated successfully or not
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
            
            return result
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

    def create_task(
            self,
            wallet_address, 
            hardware_id: int = None, 
            region: str = "global",
            duration: int = 3600, 
            app_repo_image: str = "",
            auto_pay = None,
            job_source_uri: str = "", 
            repo_uri=None,
            repo_branch=None,
            repo_owner=None, 
            repo_name=None,
            private_key = None,
            start_in: int = 300,
            paid = None
        ):
        """
        Create a task via the orchestrator.

        Args:
            wallet_address: The user's wallet address.
            hardware_id: The ID of the hardware configuration set. (Default = 0)
            region: The region of the hardware. (Default: global)
            duration: The duration of the service runtime in seconds. (Default = 3600)
            app_repo_image: Optional. The name of a demo space.
            job_source_uri: Optional. The job source URI to be deployed. If this is provided, app_repo_image and repo_uri are ignored.
            repo_uri: Optional. The URI of the repo to be deployed. If job_source_uri and app_repo_image are not provided, this is required.
            repo_branch: Optional. The branch of the repo to be deployed.
            repo_owner: Optional. The owner of the repo to be deployed.
            repo_name: Optional. The name of the repo to be deployed.
            start_in: Optional. The starting time (expected time for the app to be deployed, not mandatory). (Default = 300)
            auto_pay: Optional. Automatically call the submit payment method on the contract and validate payment to get the task deployed. 
            If True, the private key and wallet must be in .env (Default = False). Otherwise, the user must call the submit payment method on the contract and validate payment.
            private_key: Optional. The wallet's private key, only used if auto_pay is True.
        
        Raises:
            SwanExceptionError: If neither app_repo_image nor job_source_uri is provided.
            
        Returns:
            JSON response from the backend server including the 'task_uuid'.
        """
        try:
            if not wallet_address:
                raise SwanAPIException(f"No wallet_address provided, please pass in a wallet_address")

            if auto_pay:
                if not private_key:
                    raise SwanAPIException(f"please provide private_key if using auto_pay")

            if not region:
                region = 'global'

            if hardware_id is None:
                hardware_id = 0
                self.hardware_id_free = 0  # to save the default hardware_id for possible task renewals
            else:
                self.hardware_id_free = None

            if cfg_name := self.get_cfg_name(hardware_id):
                logging.info(f"Using {cfg_name} machine, {hardware_id=} {region=}")
                print(f"Using {cfg_name} machine, {hardware_id=} {region=}")
            else:
                raise SwanAPIException(f"Invalid hardware_id selected")
            
            if paid is None:
                paid = self.estimate_payment(duration, hardware_id)
            
            if not job_source_uri:
                if app_repo_image:
                    if auto_pay == None:
                        auto_pay = True
                    repo_res = self.get_app_repo_image(app_repo_image)
                    if repo_res and repo_res.get("status", "") == "success":
                        repo_uri = repo_res.get("data", {}).get("url", "")
                        if repo_uri == "":
                            raise SwanAPIException(f"Invalid app_repo_image url")
                    else:
                        raise SwanAPIException(f"Invalid app_repo_image")

                if repo_uri:
                    job_source_uri = self.get_source_uri(
                            repo_uri=repo_uri,
                            wallet_address=wallet_address, 
                            hardware_id=hardware_id,
                            repo_branch=repo_branch,
                            repo_owner=repo_owner,
                            repo_name=repo_name
                        )
                else:
                    raise SwanAPIException(f"Please provide app_repo_image, or job_source_uri, or repo_uri")

            if self._verify_hardware_region(cfg_name, region):
                params = {
                    "paid": paid,
                    "duration": duration,
                    "cfg_name": cfg_name,
                    "region": region,
                    "start_in": start_in,
                    "wallet": wallet_address,
                    "job_source_uri": job_source_uri
                }
                result = self._request_with_params(
                    POST, 
                    CREATE_TASK, 
                    self.swan_url, 
                    params, 
                    self.token, 
                    None
                )
                task_uuid = result['data']['task']['uuid']
            else:
                raise SwanAPIException(f"No {cfg_name} machine in {region}.")
            
            if auto_pay:
                result = self.make_payment(
                    task_uuid=task_uuid, 
                    duration=duration, 
                    private_key=private_key, 
                    hardware_id=hardware_id
                )

            if result and isinstance(result, dict):
                result['id'] = task_uuid
            return result

        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def estimate_payment(self, duration : float = 3600, hardware_id = None):
        """Estimate required funds.

        Args:
            hardware_id: integer id of hardware, can be retrieve through Swan API.
            duration: duration in hours for space runtime.
        
        Returns:
            int estimated price in SWAN.
            e.g. (price = 10 SWAN, duration = 1 hr) -> 10 SWAN
        """
        try:
            if hardware_id is None:
                raise SwanAPIException(f"Invalid hardware_id")
            
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            contract = SwanContract("", self.contract_info)

            duration_hour = duration/3600
            amount = contract.estimate_payment(hardware_id, duration_hour)
            return contract._wei_to_swan(amount)
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
    
    def submit_payment(self, task_uuid, private_key, duration = 3600, hardware_id = None):
        """
        Submit payment for a task

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            hardware_id: id of cp/hardware configuration set
            duration: duration of service runtime (seconds).

        Returns:
            tx_hash
        """
        try:
            if hardware_id is None:
                raise SwanAPIException(f"Invalid hardware_id")
            
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            contract = SwanContract(private_key, self.contract_info)
        
            return contract.submit_payment(task_uuid=task_uuid, hardware_id=hardware_id, duration=duration)
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
                    '/v2/task_payment_validate', 
                    self.swan_url, 
                    params, 
                    self.token, 
                    None
                )
                return result
            else:
                raise SwanAPIException(f"{tx_hash=} or {task_uuid=} invalid")
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
    
    def make_payment(self, task_uuid, private_key, duration=3600, hardware_id = None):
        """
        Submit payment for a task and validate it on SWAN backend

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            hardware_id: id of cp/hardware configuration set
            duration: duration of service runtime (seconds).
        
        Returns:
            JSON response from backend server including 'task_uuid'.
        """
        try:
            if hardware_id is None:
                raise SwanAPIException(f"Invalid hardware_id") 
            
            if not private_key:
                raise SwanAPIException(f"No private_key provided.")
            if not self.contract_info:
                raise SwanAPIException(f"No contract info on record, please verify contract first.")
            
            if tx_hash := self.submit_payment(
                task_uuid=task_uuid, 
                duration=duration, 
                private_key=private_key, 
                hardware_id=hardware_id
            ):
                time.sleep(3)
                if res := self.validate_payment(
                    tx_hash=tx_hash, 
                    task_uuid=task_uuid
                ):
                    res['tx_hash'] = tx_hash
                    return res
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
        return None
    

    def renew_task(self, task_uuid: str, duration = 3600, tx_hash = "", auto_pay = False, private_key = None, hardware_id = None):
        """
        Submit payment for a task renewal and renew a task

        Args:
            task_uuid: unique id returned by `swan_api.create_task`
            hardware_id: id of cp/hardware configuration set
            duration: duration of service runtime (seconds).
        
        Returns:
            JSON response from backend server including 'task_uuid'.
        """
        try:
            if hardware_id is None:
                hardware_id = self.hardware_id_free
                if hardware_id is None:
                    raise SwanAPIException(f"Invalid hardware_id")
            
            if not (auto_pay and private_key) and not tx_hash:
                raise SwanAPIException(f"auto_pay off or tx_hash not provided, please provide a tx_hash or set auto_pay to True and provide private_key")

            if not tx_hash:
                tx_hash = self.submit_payment(task_uuid=task_uuid, duration=duration, private_key=private_key, hardware_id=hardware_id)
            
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
                return result
            else:
                raise SwanAPIException(f"{tx_hash=} or {task_uuid=} invalid")
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None
        
        
    def get_deployment_info(self, task_uuid: str):
        """Retrieve deployment info of a deployed space with task_uuid.

        Args:
            task_uuid: uuid of space task, in deployment response.

        Returns:
            Deployment info.
        """
        try:
            response = self._request_without_params(GET, DEPLOYMENT_INFO+task_uuid, self.swan_url, self.token)
            return response
        except Exception as e:
            logging.error(str(e) + traceback.format_exc())
            return None

    def get_real_url(self, task_uuid: str):
        deployment_info = self.get_deployment_info(task_uuid)
        try:
            jobs = deployment_info['data']['jobs']
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

    def _verify_hardware_region(self, hardware_name: str, region: str):
        """Verify if the hardware exist in given region.

        Args:
            hardware_name: cfg name
            region: geological regions.

        Returns:
            True when hardware exist in given region.
            False when hardware does not exist or do not exit in given region.
        """
        self.get_hardware_config()  # make sure all_hardware is updated all the time
        for hardware in self.all_hardware:
            if hardware.name == hardware_name:
                if region in hardware.region or (region.lower() == 'global' and hardware.status == 'available'):
                    return True
        return False
