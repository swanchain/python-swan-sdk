import web3
import logging
import os
from typing import List, Dict
import rsa
import base64
import json
import time
import uuid

from urllib.parse import urlparse
from swan.api_client import APIClient
from swan.common.constant import *
from swan.object.cp_config import HardwareConfig
from swan.common.utils import list_repo_contents, upload_file


class SwanAPI(APIClient):
  
    def __init__(self, api_key: str):
        """Initialize Swan API connection with API key.

        Args:
            api_key: API key for swan services.
        """
        super().__init__(api_key)
        self.orchestrator_url = orchestrator_url
        self.api_key = api_key
        self.payment_key = payment_key
        self.task = {
            "job_source_uri": None,
            "paid_amount": None,
            "duration": None,
            "tx_hash": None,
            "config_name": None,
            "random_uuid": None,
        }

    # Done
    def query_price_list(self):
        """Query the orchestrator for the current instance price list."""
        try:
            response = self._request_without_params(
                GET, CP_MACHINES, self.orchestrator_url, self.token
            )
            available_hardware = list(
                filter(
                    lambda hardware: hardware["hardware_status"] == "available",
                    response["hardware"],
                )
            )
            price_list = list(
                map(lambda hardware: hardware["hardware_price"], available_hardware)
            )
            return price_list
        except:
            logging.error("An error occurred while executing query_price_list()")
            return None
    
    # Done
    def prepare_task(self, source_code_url):
        """Prepare a task for deployment with the required details.
        - source_code_url: URL to the code repository containing Docker/K8s file and env file
        convert source url to job source uri, upload file to mcs? return nothing
        random uuid for job source uri
        """
        try:
            file_contents = list_repo_contents(source_code_url)
            env_contents = file_contents.get(".env")
            dockerfile_contents = file_contents.get("Dockerfile")
            kubernetes_contents = {
                filename: content
                for filename, content in file_contents.items()
                if filename.endswith(".yaml")
            }

            folder_path = os.path.join("tasks", "task" + self.task["random_uuid"])

            new_names = {".env": ".env.production", "Dockerfile": "Dockerfile"}

            for filename, content in [
                ("env", env_contents),
                ("Dockerfile", dockerfile_contents),
            ] + list(kubernetes_contents.items()):
                if content is not None:

                    temp_file_path = os.path.join(
                        os.getenv("file_cache_path"), filename
                    )
                    with open(temp_file_path, "w") as f:
                        f.write(content)

                    new_filename = new_names.get(filename, filename)
                    dest_file_path = os.path.join(folder_path, new_filename)
                    mcs_file = upload_file(
                        temp_file_path, os.getenv("MCS_BUCKET"), dest_file_path
                    )

                    os.remove(temp_file_path)

                    if mcs_file is None:
                        raise Exception(f"Failed to upload {new_filename} to MCS.")
            self.task["random_uuid"] = str(uuid.uuid4())
            api = os.getenv("ORCHESTRATOR_API")
            job_source_uri = f"{api}/spaces/{self.task['random_uuid']}"
            self.task["job_source_uri"] = job_source_uri
            return None
        except:
            logging.error("An error occurred while executing set_url()")
            return None

    # Done
    def propose_task(self, start_in, region):
        """Propose the prepared task to the orchestrator. max duration, valid region
        return task object"""
        response = self._request_without_params(
            GET, CP_MACHINES, self.orchestrator_url, self.token
        )
        regions = set()
        for hardware_info in response["data"]["hardware"]:
            if hardware_info["hardware_name"] == self.task["config_name"]:
                regions.update(hardware_info["region"])
        try:
            if region not in regions:
                logging.error("Invalid region")
            if self.task["duration"] > MAX_DURATION:
                logging.error("Invalid duration")
            params = {
                "paid": self.task["paid_amount"],
                "duration": self.task["duration"],
                "cfg_name": self.task["config_name"],
                "region": region,
                "start_in": start_in,
                "tx_hash": self.task["tx_hash"],
                "job_source_uri": self.task["job_source_uri"],
            }
            result = self._request_with_params(
                POST, DEPLOY_TASK, self.orchestrator_url, params, self.token
            )
            return result
        except Exception as e:
            return None

    # Not done
    def make_payment(self):
        """Make payment for the task build after acceptance by the orchestrator."""
        try:
            result = self._request_without_params(
                POST,
                USER_PROVIDER_PAYMENTS,
                self.orchestrator_url,
                self.token,
                None
            )
            return response
        except Exception:
            logging.error("Failed to make payment.")
            return None
          
    # Done
    def get_payment_info(self):
        """Retrieve payment information from the orchestrator after making the payment."""
        try:
            payment_info = self._request_without_params(
                GET, PROVIDER_PAYMENTS, self.orchestrator_url, self.token
            )
            return payment_info
        except:
            logging.error("An error occurred while executing get_payment_info()")
            return None

    # Done
    def get_task_status(self, task_uuid):
        """Fetch the current status of the task from the orchestrator."""
        try:
            task_status = self._request_without_params(
                GET, DEPLOY_STATUS + str(task_uuid), self.orchestrator_url, self.token
            )
            deploy_status = task_status.get("data", {}).get("deploy_status")
            return deploy_status
        except:
            logging.error("An error occurred while executing get_task_status()")
            return None

    # Not done
    def fetch_task_details(self):
        """Retrieve the deployed URL and credentials/token for access after task success.
        Decrypt the credentials/token with the private key if necessary.
        """
        try:
            private_key = rsa.PrivateKey.load_pkcs1(private_key)
            task_details = self._request_without_params(
                GET, TASK_DETAILS, self.orchestrator_url, self.token
            )
            encrypted_token = task_details.get("token")
            decrypted_token = rsa.decrypt(
                base64.b64decode(encrypted_token), private_key
            )
            decrypted_token = decrypted_token.decode()
            task_details["token"] = decrypted_token
            task_details_json = json.dumps(task_details)
            return task_details_json
        except:
            logging.error("An error occurred while executing fetch_task_details()")
            return None
              
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
        
    def deploy_space(self, cfg_name: str, region: str, start_in: int, duration: int, job_source_uri: str, paid: int = 0.0):
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
            params = {
                "paid": paid,
                "duration": duration,
                "cfg_name": cfg_name,
                "region": region,
                "start_in": start_in,
                "tx_hash": None,
                "job_source_uri": job_source_uri
            }
            result = self._request_with_params(POST, DEPLOY_SPACE, SWAN_API, params, self.token, None)
            return result
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
            response = self._request_with_params(GET, GET_CP_CONFIG, SWAN_API, params, self.token, None)
            return response
        except Exception:
            logging.error("Failed to extract space info.")
            return None
