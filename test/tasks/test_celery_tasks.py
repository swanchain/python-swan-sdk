"""Tests for Mock Celery Task. """
from mock.mock import MagicMock

from src.api.engine_api import EngineAPI
from test.mock.client_mock import MockAPIClient


class TestMockCeleryTask:
    def test_mock_celery_task(self):
        """Test the mock Celery task query.

        This test verifies that the `get_celery_task_status` method correctly interprets and
        returns the mocked response for a Celery task query. The expected behavior is to return
        a dictionary with the task state.
        """
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)
        # Query the mocked Celery task status
        response = engine_api.get_celery_task_status(2)

        # Asserting that the response matches the mocked data
        expected_response = {"taskState": "success"}
        assert response == expected_response

    def test_returns_response_object_with_valid_task_id(self):
        # Instantiate EngineAPI with MockAPIClient
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)

        # Mock the _request_with_params method to return a response object
        mock_response = {"status": "success", "data": "task_status"}
        engine_api.api_client._request_with_params = MagicMock(
            return_value=mock_response
        )

        # Call the method you're testing
        task_id = "valid_task_id"
        response = engine_api.get_celery_task_status(task_id)

        # Assert that the response is a response object
        assert response == mock_response

    def test_returns_none_when_response_is_empty(self):
        # Instantiate EngineAPI with MockAPIClient
        mock_api_client = MockAPIClient("dummy_api_key", "dummy_wallet_address")
        engine_api = EngineAPI(api_client=mock_api_client)

        # Mock the _request_with_params method to return an empty response
        engine_api.api_client._request_with_params = MagicMock(return_value=None)

        # Call the method you're testing
        response = engine_api.get_celery_task_status("task_id")

        # Assert that the response is None
        assert response is None
