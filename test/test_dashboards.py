"""Tests for Mock Send Job functionality """

import pytest
import requests_mock
from swan.common import constants as c


class TestMockSendJob:
    @pytest.fixture
    def mock_requests(self, shared_real_engine_api):
        """Fixture to mock network requests for processing tasks.

        Args:
            shared_real_engine_api: A fixture providing a shared instance of the Engine API.

        Yields:
            A requests mocker object to intercept and mock responses for network requests.
        """
        self.engine_api = shared_real_engine_api
        nested_data = {
            "task1": {"task_instance_data": "task_1_data"},
            "task2": {"task_instance_data": "task_2_data"},
        }

        with requests_mock.Mocker() as m:
            # Mocking the GET request to the processing tasks endpoint
            m.get(c.PROCESSING_TASKS, json=nested_data)
            yield m

    def test_mock_processing_tasks(self, mock_requests):
        """Test the mock processing tasks query."""
        # Querying the mocked processing tasks
        response = self.engine_api.get_processing_tasks()

        # Asserting that the response matches the mocked data
        assert response == {
            "task1": {"task_instance_data": "task_1_data"},
            "task2": {"task_instance_data": "task_2_data"},
        }
