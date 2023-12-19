""" Tests for Computing Providers """

import pytest
import requests
from mock.mock import Mock, MagicMock, patch  # type: ignore

from src.api.cp import (
    get_all_cp_machines,
    get_cp_detail,
    get_available_computing_providers,
    get_collateral_balance,
)
from src.constants.constants import SWAN_API, CP_AVAILABLE
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanRequestError,
    SwanConnectionError,
)


class TestComputingProviders:
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

    def test_retrieve_collateral_balance_valid_address(self):
        # Mock the requests.get method to return a mock response
        with patch("requests.get") as mock_get:
            # Set up the mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
            mock_get.return_value = mock_response

            # Call the function with a valid computing provider address
            result = get_collateral_balance("0x1234abcd")

            # Assert that the response is as expected
            assert result == {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }

    # NOTE: do not uncomment before ApiClient changes
    # def test_invalid_address_format(self):
    #     # Arrange
    #     cp_address = "invalid_address"
    #
    #     # Act and Assert
    #     with pytest.raises(SwanRequestError):
    #         get_collateral_balance(cp_address)

    def test_return_error_message(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            # Call the function under test
            with pytest.raises(SwanRequestError) as e:
                get_collateral_balance("0x1234abcd")
            # Assert that the exception message is correct
            assert (
                str(e.value)
                == "SwanRequestError: An unexpected error occurred while retrieving collateral balance"
            )

    def test_get_collateral_balance_request(self):
        # Mock the requests.get method to return a mock response
        with patch("requests.get") as mock_get:
            # Set up the mock response
            mock_response = Mock()
            mock_response.json.return_value = {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }
            mock_get.return_value = mock_response

            # Call the function you're testing
            result = get_collateral_balance("0x1234abcd")

            # Assert that requests.get was called with the correct endpoint
            mock_get.assert_called_once_with(
                "http://swanhub-cali.swanchain.io/cp/collateral/0x1234abcd"
            )

            # Assert that the result is the expected dictionary
            assert result == {
                "status": "success",
                "message": "Successfully retrieved collateral balance",
                "data": {"balance": 100},
            }

    def test_retrieve_valid_cp_detail(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {"cp_id": "123", "name": "Test CP"}
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response) as mock_get:
            # Call the function with a valid cp_id
            cp_id = "123"
            response, status_code = get_cp_detail(cp_id)

            # Assert that the requests.get method was called with the correct URL
            mock_get.assert_called_once_with(f"{SWAN_API}/{cp_id}")

            # Assert that the response data and status code are correct
            assert response == {"cp_id": "123", "name": "Test CP"}
            assert status_code == 200

    def test_returned_dictionary_contains_expected_keys(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3",
        }
        mock_response.status_code = 200
        requests.get = MagicMock(return_value=mock_response)

        # Call the function you're testing
        response, status_code = get_cp_detail("cp_id")

        # Assert that the response contains all expected keys
        assert "key1" in response
        assert "key2" in response
        assert "key3" in response

    def test_http_status_code_type(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {"data": "mock_data"}
        mock_response.status_code = 200
        with patch("requests.get", return_value=mock_response):
            # Call the function under test
            response, status_code = get_cp_detail("cp_id")

            # Assert that the status code is of the expected type
            assert isinstance(status_code, int)

    def test_valid_json_response(self):
        # Mock the requests.get method to return a mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "message": "Data retrieved successfully",
            "data": {"providers": ["provider1", "provider2"]},
        }
        mock_response.raise_for_status.return_value = None
        requests.get = MagicMock(return_value=mock_response)

        # Call the function under test
        result = get_available_computing_providers()

        # Assert that the result is the expected JSON response
        assert result == {
            "status": "success",
            "message": "Data retrieved successfully",
            "data": {"providers": ["provider1", "provider2"]},
        }

    def test_api_endpoint_not_available(self):
        # Mock the requests.get method to raise a ConnectionError
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(SwanConnectionError):
                get_available_computing_providers()

    def test_invalid_json_response(self):
        # Mock the requests.get method to return an invalid JSON response
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.side_effect = ValueError

            # Call the function under test
            with pytest.raises(ValueError):
                get_available_computing_providers()

    def test_empty_json_response(self):
        # Mock the requests.get method to return an empty JSON response
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {}

            # Call the function under test
            result = get_available_computing_providers()

            # Assert that the result is an empty dictionary
            assert result == {}

            # Assert that the requests.get method was called with the correct URL
            mock_get.assert_called_once_with(f"{SWAN_API}{CP_AVAILABLE}")
