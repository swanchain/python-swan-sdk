import logging
import os
import uuid

from swan.api_client import APIClient
from swan.common.constant import *
from swan.object import HardwareConfig, Task
# from swan.common.utils import list_repo_contents, upload_file


class SwanAPI(APIClient):
  
    def __init__(self, api_key: str, login: bool = True, environment: str = ""):
        """Initialize user configuration and login.

        Args:
            api_key: SwanHub API key, generated through website
            login: Login into Swanhub or Not
            environment: Selected server 'production/calibration'
        """
        self.token = None
        self.api_key = api_key
        self.environment = environment
        if login:
            self.api_key_login()

    def api_key_login(self):
        """Login with SwanHub API Key.

        Returns:
            A str access token for further SwanHub API access in
            current session.
        """
        params = {"api_key": self.api_key}
        try:
            result = self._request_with_params(
                POST, APIKEY_LOGIN, SWAN_API, params, None, None
            )
            self.token = result["data"] 
            logging.info("Login Successfully!")
        except:
            logging.error("Login Failed!")
    
    # def prepare_task(self, source_code_url):
    #     """Prepare a task for deployment with the required details.
    #     - source_code_url: URL to the code repository containing Docker/K8s file and env file
    #     convert source url to job source uri, upload file to mcs? return nothing
    #     random uuid for job source uri
    #     """
    #     try:
    #         self.task = {
    #                     "job_source_uri": None,
    #                     "paid_amount": None,
    #                     "duration": None,
    #                     "tx_hash": None,
    #                     "config_name": None,
    #                     "random_uuid": None,
    #                 }

    #         file_contents = list_repo_contents(source_code_url)
    #         env_contents = file_contents.get(".env")
    #         dockerfile_contents = file_contents.get("Dockerfile")
    #         kubernetes_contents = {
    #             filename: content
    #             for filename, content in file_contents.items()
    #             if filename.endswith(".yaml")
    #         }

    #         folder_path = os.path.join("tasks", "task" + self.task["random_uuid"])

    #         new_names = {".env": ".env.production", "Dockerfile": "Dockerfile"}

    #         for filename, content in [
    #             ("env", env_contents),
    #             ("Dockerfile", dockerfile_contents),
    #         ] + list(kubernetes_contents.items()):
    #             if content is not None:

    #                 temp_file_path = os.path.join(
    #                     os.getenv("file_cache_path"), filename
    #                 )
    #                 with open(temp_file_path, "w") as f:
    #                     f.write(content)

    #                 new_filename = new_names.get(filename, filename)
    #                 dest_file_path = os.path.join(folder_path, new_filename)
    #                 mcs_file = upload_file(
    #                     temp_file_path, os.getenv("MCS_BUCKET"), dest_file_path
    #                 )

    #                 os.remove(temp_file_path)

    #                 if mcs_file is None:
    #                     raise Exception(f"Failed to upload {new_filename} to MCS.")
    #         self.task["random_uuid"] = str(uuid.uuid4())
    #         api = os.getenv("ORCHESTRATOR_API")
    #         job_source_uri = f"{api}/spaces/{self.task['random_uuid']}"
    #         self.task["job_source_uri"] = job_source_uri
    #         return None
    #     except:
    #         logging.error("An error occurred while executing set_url()")
    #         return None
              
    def get_hardware_config(self):
        """Query current hardware list object.
        
        Returns:
            list of HardwareConfig object.
            e.g. obj.to_dict() -> 
            {
                'id': 0, 
                'name': 'C1ae.small', 
                'description': 'CPU only · 2 vCPU · 2 GiB', 
                'type': 'CPU', 
                'reigion': ['North Carolina-US'], 
                'price': '0.0', 
                'status': 'available'
            }
        """
        try:
            response = self._request_without_params(GET, GET_CP_CONFIG, SWAN_API, self.token)
            self.all_hardware = [HardwareConfig(hardware) for hardware in response["data"]["hardware"]]
            return self.all_hardware
        except Exception:
            logging.error("Failed to fetch hardware configurations.")
            return None
        
    def deploy_task(self, cfg_name: str, region: str, start_in: int, duration: int, job_source_uri: str, paid: int = 0.0):
        """Sent deploy space request via orchestrator.

        Args:
            cfg_name: name of cp/hardware configuration set.
            region: region of hardware.
            start_in: unix timestamp of starting time.
            duration: duration of service runtime in unix time.
            job_source_uri: source uri for space.

        Returns:
            JSON response from backend server including 'task_uuid'.
        """
        try:
            if self._verify_hardware_region(cfg_name, region):
                params = {
                    "paid": paid,
                    "duration": duration,
                    "cfg_name": cfg_name,
                    "region": region,
                    "start_in": start_in,
                    "tx_hash": None,
                    "job_source_uri": job_source_uri
                }
                result = self._request_with_params(POST, DEPLOY_TASK, SWAN_API, params, self.token, None)
                return result
            else:
                raise Exception
        except Exception:
            logging.error("Failed to deploy space.")
            return None
        
    def get_deployment_info(self, task_uuid: str):
        """Retrieve deployment info of a deployed space with task_uuid.

        Args:
            task_uuid: uuid of space task, in deployment response.

        Returns:
            Deployment info.
        """
        try:
            params = {
                "task_uuid": task_uuid
            }
            response = self._request_with_params(GET, DEPLOYMENT_INFO, SWAN_API, params, self.token, None)
            return response
        except Exception:
            logging.error("Failed to extract space info.")
            return None

    def get_payment_info(self):
        """Retrieve payment information from the orchestrator after making the payment.
        """
        try:
            payment_info = self._request_without_params(
                GET, PROVIDER_PAYMENTS, SWAN_API, self.token
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
        hardwares = self.get_hardware_config()
        for hardware in hardwares:
            if hardware.id == hardware_name:
                if region in hardware.region:
                    return True
                return False
        return False
