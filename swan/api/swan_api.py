import web3
import logging
import os
from typing import List, Dict

from swan.api_client import APIClient
from swan.common.constant import *
from swan.object.cp_config import HardwareConfig


class SwanAPI(APIClient):

    def __init__(self, api_key: str):
        """Initialize Swan API connection with API key.

        Args:
            api_key: API key for swan services.
        """
        super().__init__(api_key)

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
            response = self._request_without_params(
                GET, GET_CP_CONFIG, SWAN_API, self.token
            )
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
            result = self._request_with_params(
                POST, DEPLOY_SPACE, SWAN_API, params, self.token, None
            )
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
            response = self._request_with_params(
                GET, GET_CP_CONFIG, SWAN_API, params, self.token, None
            )
            return response
        except Exception:
            logging.error("Failed to extract space info.")
            return None