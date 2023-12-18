""" Tests for Computing Providers """

import pytest
import requests
from mock.mock import Mock, MagicMock, patch
from src.api.cp import get_all_cp_machines, get_computing_providers_list
from src.exceptions.request_exceptions import SwanHTTPError, SwanRequestError


class TestAllComputingProviders:
    def test_retrieve_all_cp_machines(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "data": {
                "hardware": [
                    {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
                    {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
                    {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
                ]
            },
        }
        mock_response.raise_for_status.return_value = None
        requests.get = MagicMock(return_value=mock_response)

        # Call the function under test
        result = get_all_cp_machines()

        # Assert that the result is the expected list of hardware configurations
        expected_result = [
            {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
            {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
            {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
        ]
        assert result == expected_result

    def test_function_raises_httperror_if_api_call_fails(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.HTTPError):
            with pytest.raises(SwanHTTPError):
                get_all_cp_machines()

    def test_failed_api_response(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(SwanRequestError):
                get_all_cp_machines()


class TestComputingProvidersListByRegion:
    def test_returns_list_of_computing_providers(self):
        # Mock the requests.post method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [{"provider": "Provider A"}, {"provider": "Provider B"}]
        }
        mock_response.raise_for_status.return_value = None
        requests.post = MagicMock(return_value=mock_response)

        # Call the function you're testing
        result = get_computing_providers_list("region")

        # Assert that the result is a list of dictionaries
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert isinstance(result[1], dict)
        assert len(result) == 2
        assert result[0]["provider"] == "Provider A"
        assert result[1]["provider"] == "Provider B"

    def test_raises_swan_http_error_if_api_call_fails(self):
        # Mock the requests.post method to raise an HTTPError
        with patch('requests.post') as mock_post:
            mock_post.side_effect = requests.exceptions.HTTPError()

            # Call the function under test
            with pytest.raises(SwanHTTPError):
                get_computing_providers_list("region")

    def test_raises_value_error_if_region_not_provided(self):
        with pytest.raises(ValueError):
            get_computing_providers_list("")
        with pytest.raises(ValueError):
            get_computing_providers_list(None)

    def test_raises_swan_http_error(self):
        # Mock the requests.post method to raise an HTTPError
        with patch('requests.post') as mock_post:
            mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

            # Call the function under test
            with pytest.raises(SwanHTTPError):
                get_computing_providers_list("region")

    def test_raises_exception_for_other_types_of_exceptions(self):
        # Mock the requests.post method to raise an exception
        def mock_post(*args, **kwargs):
            raise Exception("An error occurred")

        with patch('requests.post', side_effect=mock_post):
            with pytest.raises(Exception):
                get_computing_providers_list("region")