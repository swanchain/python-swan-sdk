# import pytest
# import requests_mock
# import requests
# from swan.common import constants as c
#
#
# class TestMockSendJob:
#     @pytest.fixture
#     def mock_requests(self, shared_real_engine_api):
#         self.engine_api = shared_real_engine_api
#         with requests_mock.Mocker() as m:
#             m.post(c.JOBS, json={"job1": "data", "job2": "data"})
#             yield m
#
#     def test_mock_job_send(self, mock_requests):
#         response = self.engine_api.send_jobs({"job1": "data", "job2": "data"})
#         assert response == {"job1": "data", "job2": "data"}
