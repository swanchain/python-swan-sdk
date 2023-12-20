""" Engine API Class code """

import logging

from src.api_client import APIClient
from src.constants.constants import PROCESSING_TASKS, GET, POST, JOBS, CELERY


class EngineAPI(object):
    def __init__(self, api_client=None, api_key=None, is_calibration=False):
        if api_client is None:
            api_client = APIClient("placeholder_api_key", "sample_wallet_address")
        self.api_client = api_client
        self.SWAN_API = api_client.SWAN_API
        self.token = self.api_client.token

    def get_celery_task_status(self, task_id):
        params = {"task_id": task_id}
        try:
            response = self.api_client._request_with_params(
                GET, CELERY, self.api_client.SWAN_API, params, self.token, None
            )
            return response
        except:
            logging.error("An error occurred while executing get_celery_task_status()")
            return None

    def get_processing_tasks(self):
        try:
            result = self.api_client._request_without_params(
                GET, PROCESSING_TASKS, self.api_client.SWAN_API, self.token
            )
            return result
        except:
            logging.error("An error occurred while executing get_processing_tasks()")
            return None

    def send_jobs(self, job_data):
        try:
            response = self.api_client._request_with_params(
                POST, JOBS, self.api_client.SWAN_API, job_data, self.token, None
            )
            return response
        except:
            logging.error("An error occurred while executing send_jobs()")
            return None
