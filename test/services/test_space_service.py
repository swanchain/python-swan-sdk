""" Test the Space functionality"""

import pytest
from decimal import Decimal
from mock.mock import patch, MagicMock
from requests import RequestException, Timeout
from requests.models import HTTPError

from src.api.space import Space
from src.exceptions.request_exceptions import (
    SwanRequestError,
    SwanHTTPError,
    SwanTimeoutError,
    SwanConnectionError,
)
from src.exceptions.swan_base_exceptions import SwanValueError


class TestSpaceService:
    """Test the Space Service class"""

    def setup(self):
        self.space = Space()

    # Please do not uncomment before APiClient change
    # def test_send_post_request_with_valid_parameters(self):
    #     # Mock the requests.post method to return a mock response
    #     mock_response = Mock()
    #     mock_response.content = '{"message": "Success"}'
    #     mock_response.json.return_value = {"message": "Success"}
    #     mock_response.raise_for_status.return_value = None
    #     requests.post = MagicMock(return_value=mock_response)
    #
    #     # Call the deploy_space_v1 function with valid parameters
    #     response = self.space.deploy_space_v1(
    #         paid=Decimal("100.00"),
    #         duration=30,
    #         cfg_name="example_config",
    #         region="us-west-1",
    #         start_in=15,
    #         tx_hash="1234567890abcdef",
    #         job_source_uri="http://source.example.com",
    #     )
    #
    #     # Assert that the requests.post method was called with the correct URL and data
    #     requests.post.assert_called_with(
    #         "http://swanhub-cali.swanchain.io/v1/space_deployment/",
    #         data={
    #             "job_source_uri": "http://source.example.com",
    #             "paid": "100.00",
    #             "duration": 30,
    #             "cfg_name": "example_config",
    #             "region": "us-west-1",
    #             "start_in": 15,
    #             "tx_hash": "1234567890abcdef",
    #         },
    #     )
    #
    #     # Assert that the response is the expected JSON data
    #     assert response == {"message": "Success"}

    # def test_response_data_not_empty_and_json_format(self):
    #     # Mock the requests.post method to return a mock response
    #     mock_response = Mock()
    #     mock_response.content = '{"message": "Success"}'
    #     mock_response.json.return_value = {"message": "Success"}
    #     mock_response.raise_for_status.return_value = None
    #     requests.post = MagicMock(return_value=mock_response)
    #
    #     # Call the self.space.deploy_space_v1 function with valid parameters
    #     response = self.space.deploy_space_v1(
    #         paid=Decimal("100.00"),
    #         duration=30,
    #         cfg_name="example_config",
    #         region="us-west-1",
    #         start_in=15,
    #         tx_hash="1234567890abcdef",
    #         job_source_uri="http://source.example.com",
    #     )
    #
    #     # Assert that the response is a dictionary
    #     assert isinstance(response, JSON)
    #
    #     # Assert that the response contains the expected data
    #     assert response == {"message": "Success"}
    #
    #     # Assert that requests.post was called with the correct arguments
    #     requests.post.assert_called_once_with(
    #         "http://swanhub-cali.swanchain.io/v1/space_deployment/",
    #         data={
    #             "job_source_uri": "http://source.example.com",
    #             "paid": "100.00",
    #             "duration": 30,
    #             "cfg_name": "example_config",
    #             "region": "us-west-1",
    #             "start_in": 15,
    #             "tx_hash": "1234567890abcdef",
    #         },
    #     )

    def test_invalid_input(self):
        # Test case with missing required parameters
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=None,
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case with invalid paid parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("0.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case with invalid job_source_uri parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="",
            )

        # Test case with invalid cfg_name parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case with invalid region parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case with invalid start_in parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=None,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case with invalid duration parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=None,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case with invalid tx_hash parameter
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="",
                job_source_uri="http://source.example.com",
            )

    def test_raises_swan_value_error(self):
        # Test case where paid parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=None,
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case where job_source_uri parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri=None,
            )

        # Test case where cfg_name parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name=None,
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case where region parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region=None,
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case where start_in parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=None,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case where duration parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=None,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

        # Test case where tx_hash parameter is missing
        with pytest.raises(SwanValueError):
            self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash=None,
                job_source_uri="http://source.example.com",
            )

    def test_raises_swan_request_error(self):
        # Mock the requests.post method to raise a RequestException
        with patch("requests.post", side_effect=RequestException):
            with pytest.raises(SwanRequestError):
                self.space.deploy_space_v1(
                    paid=Decimal("100.00"),
                    duration=30,
                    cfg_name="example_config",
                    region="us-west-1",
                    start_in=15,
                    tx_hash="1234567890abcdef",
                    job_source_uri="http://source.example.com",
                )

    def test_raises_swan_http_error(self):
        # Mock the requests.post method to raise an HTTPError
        with patch("requests.post") as mock_post:
            mock_post.side_effect = HTTPError("HTTP error occurred")

            # Call the self.space.deploy_space_v1 function and assert that it raises a SwanHTTPError
            with pytest.raises(SwanHTTPError):
                self.space.deploy_space_v1(
                    paid=Decimal("100.00"),
                    duration=30,
                    cfg_name="example_config",
                    region="us-west-1",
                    start_in=15,
                    tx_hash="1234567890abcdef",
                    job_source_uri="http://source.example.com",
                )

    def test_request_timeout(self):
        # Mock the requests.post method to raise a Timeout exception
        with patch("requests.post", side_effect=Timeout):
            with pytest.raises(SwanTimeoutError):
                self.space.deploy_space_v1(
                    paid=Decimal("100.00"),
                    duration=30,
                    cfg_name="example_config",
                    region="us-west-1",
                    start_in=15,
                    tx_hash="1234567890abcdef",
                    job_source_uri="http://source.example.com",
                )

    def test_empty_response_content(self):
        # Mock the requests.post method to return a mocked response
        with patch("requests.post") as mock_post:
            # Create a mock response object with the desired attributes
            mock_response = MagicMock()
            mock_response.content = b""
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"id": 4414961072}  # Mocked JSON response

            mock_post.return_value = mock_response

            # Call the self.space.deploy_space_v1 function
            response = self.space.deploy_space_v1(
                paid=Decimal("100.00"),
                duration=30,
                cfg_name="example_config",
                region="us-west-1",
                start_in=15,
                tx_hash="1234567890abcdef",
                job_source_uri="http://source.example.com",
            )

            # Assert that the response has the expected id
            assert response["id"] == 4414961072
