""" Task Test File """
import pytest
import requests
from mock.mock import patch, Mock

from src.api.task import get_task_bidding


class TestTask:
    def test_successful_get_task_bidding(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {"task_id": "12345", "status": "bidding"}
        with patch("requests.get", return_value=mock_response) as mock_get:
            # Call the function under test
            result = get_task_bidding("12345")

            # Assert that requests.get was called with the correct arguments
            mock_get.assert_called_once_with(
                "https://swanhub-cali.swanchain.io/task/bidding",
                params={"task_id": "12345"},
                timeout=15,
            )

            # Assert that the result is the expected dictionary
            assert result == {"task_id": "12345", "status": "bidding"}

    def test_task_id_parameter_is_none(self):
        # Call the function with task_id as None
        response = get_task_bidding(None)

        # Assert that the response is an error message
        assert isinstance(response, str)

    def test_empty_task_id(self):
        # Call the function with an empty task_id
        response = get_task_bidding("")

        # Assert that the response is an error message
        assert isinstance(response, dict)
        assert "error" in response

    def test_api_endpoint_not_available(self):
        # Mock the requests.get method to raise a ConnectionError
        with pytest.raises(ConnectionError):
            with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
                get_task_bidding("task_id")
