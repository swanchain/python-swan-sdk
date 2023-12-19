""" Tests for Computing Providers """
import logging

import pytest
import requests
from mock.mock import Mock, MagicMock, patch

from src.api.cp import ComputerProvider
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanRequestError,
    SwanConnectionError,
    SwanTimeoutError,
)


class TestComputingProviders:
    def setup(self):
        self.provider = ComputerProvider()

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
        result = self.provider.get_all_cp_machines()

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
                self.provider.get_all_cp_machines()

    def test_failed_api_response(self):
        # Mock the requests.get method to raise an exception
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(SwanRequestError):
                self.provider.get_all_cp_machines()

    def test_valid_list_of_dictionaries(self):
        # Mock the requests.get method to return a successful response
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "data": [{"provider": "A", "count": 10}, {"provider": "B", "count": 5}]
            }

            # Call the function you're testing
            result = self.provider.get_cp_distribution()

            # Assert that the result is a list of dictionaries
            assert isinstance(result, list)
            assert all(isinstance(item, dict) for item in result)

    def test_returns_empty_list_when_api_call_returns_empty_data(self):
        # Mock the requests.get method to return an empty response
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": []}

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is an empty list
            assert result == []

    def test_handle_connection_errors(self):
        # Mock the requests.get method to raise a ConnectionError
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            with pytest.raises(SwanConnectionError):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("Error connecting: ")

        # Mock the requests.get method to raise a Timeout
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            with pytest.raises(SwanTimeoutError):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("Timeout error: ")

        # Mock the requests.get method to raise a RequestException
        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(SwanRequestError):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("Error during requests to ")

        # Mock the requests.get method to raise an unexpected exception
        with patch("requests.get", side_effect=Exception):
            with pytest.raises(Exception):
                self.provider.get_cp_distribution()
                logging.error.assert_called_with("An unexpected error occurred: ")

    def test_handle_timeout_errors(self):
        # Mock the requests.get method to raise a Timeout exception
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            with pytest.raises(SwanTimeoutError):
                self.provider.get_cp_distribution()

    def test_valid_field_types(self):
        # Mock the requests.get method to return a response with invalid field types
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "data": [
                    {
                        "provider_id": "1",
                        "name": "Provider 1",
                        "cpu_cores": "4",
                        "memory": "8GB",
                        "storage": "500GB",
                    },
                    {
                        "provider_id": "2",
                        "name": "Provider 2",
                        "cpu_cores": "8",
                        "memory": "16GB",
                        "storage": "1TB",
                    },
                ]
            }

            # Call the function under test
            expected_response = {
                "data": [
                    {
                        "provider_id": "1",
                        "name": "Provider 1",
                        "cpu_cores": "4",
                        "memory": "8GB",
                        "storage": "500GB",
                    },
                    {
                        "provider_id": "2",
                        "name": "Provider 2",
                        "cpu_cores": "8",
                        "memory": "16GB",
                        "storage": "1TB",
                    },
                ]
            }

            # Assert that the result is None
            assert mock_get.return_value.json.return_value == expected_response

    def test_api_returns_data_with_missing_fields(self):
        # Mock the requests.get method to return a response with missing fields
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "data": [{"provider_id": 1, "name": "Provider 1"}, {"provider_id": 2}]
            }

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is a list of dictionaries
            assert isinstance(result, list)
            assert all(isinstance(item, dict) for item in result)

            # Assert that the missing fields are replaced with None
            assert result[0]["provider_id"] == 1
            assert result[0]["name"] == "Provider 1"
            assert result[1]["provider_id"] == 2
            assert "name" not in result

    def test_api_returns_incomplete_data(self):
        # Mock the requests.get method to return incomplete data
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"data": []}

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is an empty list
            assert result == []

            # Assert that no exceptions were raised
            assert not isinstance(result, Exception)

    def test_unexpected_data_format(self):
        # Mock the requests.get method to return a response with unexpected data format
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"result": "success"}

            # Call the function under test
            result = self.provider.get_cp_distribution()

            # Assert that the result is None
            assert result == []

    def test_retrieve_all_cp_machines(self):
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
        result = self.provider.get_all_cp_machines()
        expected_result = [
            {"name": "Machine 1", "cpu": "Intel i7", "ram": "16GB"},
            {"name": "Machine 2", "cpu": "AMD Ryzen 5", "ram": "8GB"},
            {"name": "Machine 3", "cpu": "Intel i5", "ram": "12GB"},
        ]
        assert result == expected_result
