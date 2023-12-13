"""Tests for Mock Celery Task. """

import pytest
import requests_mock

from src.constants.constants import CELERY


class TestMockCeleryTask:
    @pytest.fixture
    def mock_requests(self, shared_real_engine_api):
        """Fixture to mock network requests for Celery tasks.

        Args:
            shared_real_engine_api: A fixture that provides a shared Engine API instance.

        Yields:
            A requests mocker object, which intercepts and mocks responses for network requests.
        """
        self.engine_api = shared_real_engine_api
        with requests_mock.Mocker() as m:
            # Mocking the GET request to the Celery endpoint
            m.get(CELERY, json={"taskState": "success"})
            yield m

    def test_mock_celery_task(self, mock_requests):
        """Test the mock Celery task query.

        This test verifies that the `get_celery_task_status` method correctly interprets and
        returns the mocked response for a Celery task query. The expected behavior is to return
        a dictionary with the task state.
        """
        # Query the mocked Celery task status
        response = self.engine_api.get_celery_task_status(2)

        # Asserting that the response matches the mocked data
        assert response == {"taskState": "success"}
