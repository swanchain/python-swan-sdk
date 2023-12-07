"""Tests for APIClient class. """

from swan.api_client import APIClient


class TestAPIClient:
    def test_init_with_api_key_and_wallet_address(self):
        """Test the initialization of APIClient with API key and wallet address."""
        api_key = "test_api_key"
        wallet_address = "test_wallet_address"
        api_client = APIClient(api_key, wallet_address)

        assert api_client.api_key == api_key
        assert api_client.wallet_address == wallet_address

    def test_api_key_and_wallet_address(self):
        """Test setting and retrieving API key and wallet address in APIClient."""
        api_key = "12345"
        wallet_address = "abcde"
        api_client = APIClient(api_key, wallet_address)

        assert api_client.api_key == api_key
        assert api_client.wallet_address == wallet_address

    def test_api_key_login_with_valid_credentials(self, mocker):
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
