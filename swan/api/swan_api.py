import web3
import logging
import os
import rsa
import base64
import json
import time


from urllib.parse import urlparse
from swan.api_client import APIClient
from swan.common.constant import *


class SwanAPI(APIClient):

    def __init__(self, orchestrator_url, api_key, payment_key):
        super().__init__(api_key)
        self.orchestrator_url = orchestrator_url
        self.api_key = api_key
        self.payment_key = payment_key
        self.task = {
            "job_source_uri": None,
            "paid_amount": None,
            "duration": None,
            "tx_hash": None,
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
    def set_url(self, source_code_url):
        """Prepare a task for deployment with the required details.
        - source_code_url: URL to the code repository containing Docker/K8s file and env file
        convert source url to job source uri, upload file to mcs? return nothing
        """
        try:
            parsed_url = urlparse(source_code_url)
            path_parts = parsed_url.path.split('/')
            result = '/'.join(path_parts[1:])  
            api = os.getenv("LAGRANGE_API")
            job_source_uri = f"{api}/spaces/{result}"
            self.task["job_source_uri"] = job_source_uri
            return None
        except:
            logging.error("An error occurred while executing set_url()")
            return None
    # Not done
    def propose_task(self, start_in, region, config_name):
        """Propose the prepared task to the orchestrator. max duration, config name taken or not valid, valid region
        return task object"""

        try:
            requirements = {
                "hardware_type": "cpu",
                "hardware": "x86_64",
                "vcpu": 1,
                "memory": 1,
                "region": "us-west-1",
            }

            params = {
                "public_address": wallet_address,
                "user": user,
                "name": name,
                "task_detail": task_detail,
            }
            result = self._request_with_params(
                POST, TASKS, self.orchestrator_url, params, self.token
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
            )
            return result
        except:
            logging.error("An error occurred while executing make_payment()")
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
        # PRIVATE KEY GIVEN THROUGH .ENV FILE
        private_key = os.environ.get("PRIVATE_KEY")
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
