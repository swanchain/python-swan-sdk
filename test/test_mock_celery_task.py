import pytest
import requests_mock
from swan.common import constants as c


class TestMockCeleryTask:
    @pytest.fixture
    def mock_requests(self, shared_real_engine_api):
        self.engine_api = shared_real_engine_api
        with requests_mock.Mocker() as m:
            m.get(c.CELERY, json={"taskState": "success"})
            yield m

    def test_mock_celery_task(self, mock_requests):
        response = self.engine_api.get_celery_task_status(2)
        assert response == {"taskState": "success"}
