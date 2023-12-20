""" Tests Related to Users and Claims """


import pytest
import requests
from unittest.mock import Mock, patch
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanConnectionError,
    SwanTimeoutError,
    SwanRequestError
)
from src.utils.utils import Claims


class TestReviewClaim:
    # Sends a POST request to the claim review endpoint with the specified task UUID and returns a tuple containing
    # the response (a dictionary) and HTTP status code.
    # def test_send_post_request(self):
    #     # Mock the requests.post method to return a mock response
    #     mock_response = Mock()
    #     mock_response.json.return_value = {
    #         "message": "Refund approved",
    #         "status": "success",
    #     }
    #     mock_response.status_code = 200
    #     with patch("requests.post", return_value=mock_response) as mock_post:
    #         # Call the function under test
    #         response, status_code = review_claim("123e4567-e89b-12d3-a456-426655440000")
    #
    #         # Assert that requests.post was called with the correct arguments
    #         mock_post.assert_called_once_with(
    #             "http://swanhub-cali.swanchain.io/claim_review",
    #             data={"task_uuid": "123e4567-e89b-12d3-a456-426655440000"},
    #         )
    #
    #         # Assert that the response and status code are correct
    #         assert response == {"message": "Refund approved", "status": "success"}
    #         assert status_code == 200

    #  Handles HTTP errors and returns a SwanHTTPError.
    def test_handle_http_errors(self):
        claim = Claims()
        # Mock the requests.post method to raise an HTTPError
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.HTTPError("HTTP error occurred")

            # Call the function under test and assert that it raises a SwanHTTPError
            with pytest.raises(SwanHTTPError):
                claim.review_claim("123e4567-e89b-12d3-a456-426655440000")

    #  Handles invalid JSON response and returns a ValueError.
    def test_handle_invalid_json_response(self):
        claim = Claims()
        # Mock the requests.post method to return a response with invalid JSON
        mock_response = Mock()
        mock_response.json.side_effect = Exception("Invalid JSON response received")
        with patch("requests.post", return_value=mock_response):
            # Call the function under test and assert that it raises a ValueError
            with pytest.raises(Exception):
                claim.review_claim("123e4567-e89b-12d3-a456-426655440000")

    #  Handles successful response and returns the response data and status code.
    # def test_handle_successful_response(self):
    #     # Mock the requests.post method to return a successful response
    #     claim = Claims()
    #     mock_response = Mock()
    #     mock_response.json.return_value = {
    #         "message": "Refund approved",
    #         "status": "success",
    #     }
    #     mock_response.status_code = 200
    #     with patch("requests.post", return_value=mock_response):
    #         # Call the function under test
    #         response, status_code = claim.review_claim("123e4567-e89b-12d3-a456-426655440000")
    #
    #         # Assert that the response and status code are correct
    #         assert response == {"message": "Refund approved", "status": "success"}
    #         assert status_code == 200

    #  Raises a ValueError if task_uuid is not provided.
    def test_raise_value_error(self):
        claim = Claims()
        # Call the function under test and assert that it raises a ValueError
        with pytest.raises(ValueError):
            claim.review_claim("")

    #  Handles network problems (e.g., DNS failure, refused connection, etc.) and returns a SwanConnectionError.
    def test_handle_network_problems(self):
        claim = Claims()
        # Mock the requests.post method to raise a ConnectionError
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.ConnectionError("Network problem")

            # Call the function under test and assert that it raises a SwanConnectionError
            with pytest.raises(SwanConnectionError):
                claim.review_claim("123e4567-e89b-12d3-a456-426655440000")

    #  Handles request timeout and returns a SwanTimeoutError.
    def test_handle_request_timeout(self):
        claim = Claims()
        # Mock the requests.post method to raise a Timeout
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.Timeout("Request timed out")

            # Call the function under test and assert that it raises a SwanTimeoutError
            with pytest.raises(SwanTimeoutError):
                claim.review_claim("123e4567-e89b-12d3-a456-426655440000")

    #  Handles other types of requests-related issues and returns a SwanRequestError.
    def test_handle_other_request_issues(self):
        claim = Claims()
        # Mock the requests.post method to raise a RequestException
        with patch("requests.post") as mock_post:
            mock_post.side_effect = requests.RequestException("Error during request")

            # Call the function under test and assert that it raises a SwanRequestError
            with pytest.raises(SwanRequestError):
                claim.review_claim("123e4567-e89b-12d3-a456-426655440000")

    #  Handles unexpected issues and returns an Exception.
    def test_handle_unexpected_issues(self):
        claim = Claims()
        # Mock the requests.post method to raise an unexpected exception
        with patch("requests.post") as mock_post:
            mock_post.side_effect = Exception("Unexpected error")

            # Call the function under test and assert that it raises an Exception
            with pytest.raises(Exception):
                claim.review_claim("123e4567-e89b-12d3-a456-426655440000")
