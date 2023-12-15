""" Test the Space functionality"""
from src.api.engine_api import EngineAPI
from src.api.space import get_space_deployment_info
from test.mock.client_mock import MockAPIClient


class TestSpaceService:
    """ Test the Space Service class """
    def test_valid_input_parameters(self):


        # Set up valid input parameters
        task_uuid = "12345"
        job_source_uri = "https://example.com/job"
        paid = 1
        duration = 3600
        cfg_name = "config"
        region = "us-west-1"
        start_in = 0
        wallet = "0x1234567890"
        breakpoint()
        # Call the function under test
        response = get_space_deployment_info(
            task_uuid,
            job_source_uri,
            paid,
            duration,
            cfg_name,
            region,
            start_in,
            wallet
        )


        # Assert that the response is a dictionary
        assert isinstance(response, dict)
