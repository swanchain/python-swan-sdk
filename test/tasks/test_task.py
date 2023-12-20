""" Task Test File """

import pytest
from mock.mock import patch, Mock

from src.api.task import Task
from src.exceptions.task_exceptions import SwanTaskInvalidInputError


class TestTask:
    def setup_method(self):
        self.task = Task()

    def test_successful_get_task_bidding(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {"task_id": "12345", "status": "bidding"}
        with patch("requests.get", return_value=mock_response) as mock_get:
            # Call the function under test
            result = self.task.get_task_bidding("12345")

            # Assert that requests.get was called with the correct arguments
            mock_get.assert_called_once_with(
                'http://swanhub-cali.swanchain.io/task/bidding?task_id=12345',
                headers={'Authorization': 'Bearer GnWAOmfnNa'},
            )

    def test_task_id_parameter_is_none(self):
        # Call the function with task_id as None and expect an exception
        with pytest.raises(SwanTaskInvalidInputError) as exc_info:
            self.task.get_task_bidding(None)

        # Check if the error message is as expected
        assert str(exc_info.value) == "SwanTaskInvalidInputError: Please Provide TASK ID"

    def test_empty_task_id(self):
        # Call the function with an empty task_id
        with pytest.raises(SwanTaskInvalidInputError) as exc_info:
            self.task.get_task_bidding("")

        # Check if the error message is as expected
        assert str(exc_info.value) == "SwanTaskInvalidInputError: Please Provide TASK ID"

    def test_api_endpoint_not_available(self):
        # Mock the requests.get method to raise a ConnectionError
        with patch("requests.get", side_effect=ConnectionError):
            with pytest.raises(ConnectionError):
                self.task.get_task_bidding("task_id")
