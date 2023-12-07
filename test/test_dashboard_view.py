import pytest
import requests_mock
from swan.common import constants as c


class TestMockSendJob:
    @pytest.fixture
    def mock_requests(self, shared_real_engine_api):
        self.engine_api = shared_real_engine_api
        nested_data = {
            "task1": {"task_instance_data": "task_1_data"},
            "task2": {"task_instance_data": "task_2_data"},
        }
        with requests_mock.Mocker() as m:
            m.get(c.PROCESSING_TASKS, json=nested_data)
            yield m

    def test_mock_processing_tasks(self, mock_requests):
        response = self.engine_api.get_processing_tasks()
        assert response == {
            "task1": {"task_instance_data": "task_1_data"},
            "task2": {"task_instance_data": "task_2_data"},
        }
