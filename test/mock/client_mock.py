""" Mock client"""
from src.constants.constants import PROCESSING_TASKS, CELERY


class MockAPIClient:
    def __init__(self, api_key, wallet_address):
        self.SWAN_API = "https://swanhub-cali.swanchain.io"
        self.token = "mock_token"

    def _request_without_params(self, method, endpoint, api_base, token):
        if endpoint == PROCESSING_TASKS:
            return {
                "task1": {"task_instance_data": "task_1_data"},
                "task2": {"task_instance_data": "task_2_data"},
            }
        return None

    def _request_with_params(
        self, method, endpoint, api_base, params, token, additional_headers
    ):
        if endpoint == CELERY and params.get("task_id") == 2:
            return {"taskState": "success"}
        return {"status": "success", "data": "task_status"}
