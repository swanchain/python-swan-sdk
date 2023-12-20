""" Token API tests """
from mock.mock import patch

from src.api.token import Token


class TestToken:
    def setup_method(self):
        self.token_obj = Token()

    def test_valid_api_token(self):
        # Mock the requests.post method to return a successful response
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"status": "Token Validated"}

            # Call the validate_token function with a valid API token
            response = self.token_obj.validate_token("valid_token")

            # Assert that the response is as expected
            assert response == {"status": "Token Validated"}

    def test_invalid_api_token(self):
        # Mock the requests.post method to return an unsuccessful response
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {"status": "Token Invalid"}

            # Call the validate_token function with an invalid API token
            response = self.token_obj.validate_token("invalid_token")

            # Assert that the response indicates the token is invalid
            assert response == {"status": "Token Invalid"}
