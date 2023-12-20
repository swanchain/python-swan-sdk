"""Test class for EngineAPI """

from unittest.mock import patch
from src.api_client import APIClient
from src.api.engine_api import EngineAPI
from test.mock.client_mock import MockAPIClient


class TestEngineAPI:
    def test_get_processing_tasks(self):
        # Instantiate EngineAPI with MockAPIClient
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)

        # Call the method you're testing
        response = engine_api.get_processing_tasks()

        # Assert that the response is what you expect
        assert response == {
            "task1": {"task_instance_data": "task_1_data"},
            "task2": {"task_instance_data": "task_2_data"},
        }

    def test_get_celery_task_status_with_valid_task_id(self):
        # Instantiate EngineAPI with MockAPIClient
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)

        # Call the method you're testing
        response = engine_api.get_celery_task_status("valid_task_id")

        # Assert that the response is what you expect
        expected_response = {"status": "success", "data": "task_status"}
        assert response == expected_response

    def test_handle_api_request_exceptions(self):
        # Instantiate EngineAPI with MockAPIClient
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)

        # Mock the _request_with_params method to raise an exception
        def mock_request_with_params(*args, **kwargs):
            raise Exception("API request failed")

        engine_api.api_client._request_with_params = mock_request_with_params

        # Call the method you're testing
        response = engine_api.get_celery_task_status("task_id")

        # Assert that the response is None
        assert response is None

    def test_handle_logging_exceptions(self):
        # Instantiate EngineAPI with MockAPIClient
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)

        # Mock the _request_without_params method to raise an exception
        with patch.object(
            engine_api.api_client,
            "_request_without_params",
            side_effect=Exception("An error occurred"),
        ):
            # Call the method you're testing
            result = engine_api.get_processing_tasks()

        # Assert that the result is None
        assert result is None
