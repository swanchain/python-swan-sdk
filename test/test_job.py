"""Tests for Mocking Job Sending Functionality. """

import pytest
import requests_mock
from swan.common import constants as c


class TestMockSendJob:
    @pytest.fixture
    def mock_requests(self, shared_real_engine_api):
        """Fixture to mock network requests for job sending.

        Args:
            shared_real_engine_api: A fixture providing a shared instance of the Engine API.

        Yields:
            A requests mocker object to intercept and mock POST requests.
        """
        self.engine_api = shared_real_engine_api
        with requests_mock.Mocker() as m:
            # Mocking the POST request to the job submission endpoint
            m.post(c.JOBS, json={"job1": "data", "job2": "data"})
            yield m

    def test_mock_job_send(self, mock_requests):
        """Test the mock job sending functionality."""
        # Sending jobs using the mocked job submission endpoint
        response = self.engine_api.send_jobs({"job1": "data", "job2": "data"})

        # Asserting that the response matches the mocked data
        assert response == {"job1": "data", "job2": "data"}
