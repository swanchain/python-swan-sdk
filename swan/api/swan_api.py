import web3
import logging
import os
import rsa
import base64
import json
import time

from swan.api_client import APIClient
from swan.common.constant import *


class SwanAPI(APIClient):

    def __init__(self, orchestrator_url, api_key, payment_key):
        super().__init__(api_key)
        self.orchestrator_url = orchestrator_url
        self.api_key = api_key
        self.payment_key = payment_key

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

    def build_task(self, source_code_url, instance_type, task_name, public_key=None):
        """Prepare a task for deployment with the required details.
        - source_code_url: URL to the code repository containing Docker/K8s file and env file
        - instance_type: Type of instance needed for the task
        - task_name: A name for the task
        - public_key: Optional public key for accessing confidential data
        """
        try:
            {
                "data": {
                    "files": [
                        {
                            "cid": None,
                            "created_at": None,
                            "name": None,
                            "updated_at": None,
                            "url": None,
                        },
                        {
                            "cid": None,
                            "created_at": None,
                            "name": None,
                            "updated_at": None,
                            "url": None,
                        },
                    ],
                    "job": [
                        {
                            "bidder_id": None,
                            "build_log": None,
                            "container_log": None,
                            "created_at": None,
                            "duration": None,
                            "ended_at": None,
                            "hardware": None,
                            "job_result_uri": None,
                            "job_source_uri": None,
                            "name": None,
                            "provider_status": {
                                "multi_address": None,
                                "name": None,
                                "online": None,
                                "score": None,
                                "status": None,
                            },
                            "status": None,
                            "storage_source": None,
                            "task_uuid": None,
                            "updated_at": None,
                            "uuid": None,
                        },
                        {
                            "bidder_id": None,
                            "build_log": None,
                            "container_log": None,
                            "created_at": None,
                            "duration": None,
                            "ended_at": None,
                            "hardware": None,
                            "job_result_uri": None,
                            "job_source_uri": None,
                            "name": None,
                            "provider_status": {
                                "multi_address": None,
                                "name": None,
                                "online": None,
                                "score": None,
                                "status": None,
                            },
                            "status": None,
                            "storage_source": None,
                            "task_uuid": None,
                            "updated_at": None,
                            "uuid": None,
                        },
                        {
                            "bidder_id": None,
                            "build_log": None,
                            "container_log": None,
                            "created_at": None,
                            "duration": None,
                            "ended_at": None,
                            "hardware": None,
                            "job_result_uri": None,
                            "job_source_uri": None,
                            "name": None,
                            "provider_status": {
                                "multi_address": None,
                                "name": None,
                                "online": None,
                                "score": None,
                                "status": None,
                            },
                            "status": None,
                            "storage_source": None,
                            "task_uuid": None,
                            "updated_at": None,
                            "uuid": None,
                        },
                    ],
                    "nft": {
                        "chain_id": None,
                        "contract_address": None,
                        "status": None,
                        "tokens": [],
                    },
                    "owner": {
                        "avatar": None,
                        "created_at": None,
                        "full_name": None,
                        "github_username": None,
                        "homepage": None,
                        "public_address": None,
                        "tier": None,
                        "twitter_username": None,
                        "updated_at": None,
                    },
                    "space": {
                        "activeOrder": {
                            "config": {
                                "description": None,
                                "hardware": None,
                                "hardware_id": None,
                                "hardware_type": None,
                                "memory": None,
                                "name": None,
                                "price_per_hour": None,
                                "vcpu": None,
                            },
                            "created_at": None,
                            "duration": None,
                            "ended_at": None,
                            "order_type": None,
                            "region": None,
                            "space_name": None,
                            "started_at": None,
                            "updated_at": None,
                        },
                        "created_at": None,
                        "expiration_time": None,
                        "is_public": None,
                        "last_stop_reason": None,
                        "license": None,
                        "likes": None,
                        "name": None,
                        "sdk": None,
                        "status": None,
                        "status_code": None,
                        "task_uuid": None,
                        "updated_at": None,
                        "uuid": None,
                    },
                    "task": {
                        "created_at": None,
                        "leading_job_id": None,
                        "name": None,
                        "status": None,
                        "task_detail_cid": None,
                        "updated_at": None,
                        "uuid": None,
                    },
                },
                "message": None,
                "status": None,
            }
            params = {
                "source_code_url": source_code_url,
                "instance_type": instance_type,
                "task_name": task_name,
                "public_key": public_key,
            }
            result = self._request_with_params(
                POST, BUILD_TASK, self.orchestrator_url, params, self.token
            )
            return result
        except:
            logging.error("An error occurred while executing build_task()")
            return None

    def propose_task(self, name, wallet_address, user, start_in, duration):
        """Propose the prepared task to the orchestrator."""
        try:
            requirements = {
                "hardware_type": "cpu",
                "hardware": "x86_64",
                "vcpu": 1,
                "memory": 1,
                "region": "us-west-1",
            }
            task_detail = {
                "duration": duration,
                "job_result_uri": None,
                "job_source_uri": None,
                "type": "instance",
                "status": None,
                "storage_source": STORAGE_LAGRANGE,
                "bidder_limit": 3,
                "hardware": None,
                "start_at": int(time.time() + start_in),
                "end_at": str(task_detail["start_at"] + task_detail["duration"]),
                "price_per_hour": str["price_per_hour"],
                "requirements": requirements,
                "created_at": str(int(time.time())),
                "updated_at": str(int(time.time())),
                "amount": 0,
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

    # Done ???
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
