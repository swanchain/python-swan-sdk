"""Tests for APIClient class. """
import pytest

from swan.api_client import APIClient
from swan.common import constants as c
from swan.common.constants import SWAN_API


class TestAPIClient:
    """Test suite for the APIClient class."""

    def test_api_key_and_wallet_address(self):
        # Given
        api_key = "12345"
        wallet_address = "abcde"
        api_client = APIClient(api_key, wallet_address)

        # When
        result_api_key = api_client.api_key
        result_wallet_address = api_client.wallet_address

        # Then
        assert result_api_key == api_key
        assert result_wallet_address == wallet_address

    def test_api_key_login_with_valid_credentials(self, mocker):
        # Given
        api_key = "12345"
        wallet_address = "abcde"
        api_client = APIClient(api_key, wallet_address)

        # Mocking the _request_with_params method to simulate API response
        mocker.patch.object(
            api_client, "_request_with_params", return_value={"data": "token"}
        )

        # When
        token = api_client.api_key_login()

        # Then
        assert token == "token"

    def test_make_get_request_with_valid_parameters(self, mocker):
        # Given
        api_key = "12345"
        wallet_address = "abcde"
        api_client = APIClient(api_key, wallet_address)

        # Mocking the _request method to simulate API response
        mocker.patch.object(
            api_client, "_request", return_value={"data": "response_data"}
        )

        # When
        response = api_client._request(
            c.GET, "/path", SWAN_API, {"param": "value"}, "token"
        )

        # Then
        assert response == {"data": "response_data"}

    def test_init_with_chain_name(self):
        # Given
        api_key = "12345"
        wallet_address = "abcde"
        chain_name = "chain1"

        # When
        api_client = APIClient(api_key, wallet_address, chain_name=chain_name)

        # Then
        assert api_client.chain_name == chain_name

    def test_init_without_logging_in(self):
        # Given
        api_key = "12345"
        wallet_address = "abcde"

        # When
        api_client = APIClient(api_key, wallet_address, login=False)

        # Then
        assert api_client.token is None

    def test_api_key_login_with_valid_credential(self, mocker):
        """Test API key login with valid credentials using mock object."""
        api_key = "12345"
        wallet_address = "abcde"
        api_client = APIClient(api_key, wallet_address)

        # Mocking the _request_with_params method to simulate API response
        mocker.patch.object(
            api_client, "_request_with_params", return_value={"data": "token"}
        )

        token = api_client.api_key_login()

        assert token == "token"

    def test_api_key_login_with_invalid_credentials(self, mocker):
        # Given
        api_key = "12345"
        wallet_address = "abcde"
        api_client = APIClient(api_key, wallet_address)

        # Mocking the _request_with_params method to simulate API response
        mocker.patch.object(
            api_client,
            "_request_with_params",
            side_effect=Exception("Invalid credentials"),
        )

        # When
        token = api_client.api_key_login()

        # Then
        assert token is None

    def test_init_with_calibration_true(self):
        # Given
        api_key = "12345"
        wallet_address = "abcde"

        # When
        api_client = APIClient(api_key, wallet_address, is_calibration=True)

        # Then
        assert api_client.is_calibration is True
