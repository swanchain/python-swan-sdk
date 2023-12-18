""" Tests for Payments functionality """


import pytest
import requests
from src.utils.utils import validate_payment
from unittest.mock import Mock, patch, MagicMock
from src.exceptions.request_exceptions import (
    SwanConnectionError,
    SwanTimeoutError,
    SwanHTTPError,
)


class TestValidatePayment:
    def test_valid_payment_success(self):
        # Mock the requests.post method to return a successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "Success"}
        requests.post = MagicMock(return_value=mock_response)

        # Call the method you're testing
        result = validate_payment("chain_id", "tx_hash", 10.0)

        # Assert that the result is as expected
        assert result == (True, {"status": "Success"})

    def test_missing_parameters(self):
        # Call the method you're testing without providing necessary parameters
        with pytest.raises(ValueError):
            validate_payment("", "tx_hash", 10.0)
        with pytest.raises(ValueError):
            validate_payment("chain_id", "", 10.0)
        with pytest.raises(ValueError):
            validate_payment("chain_id", "tx_hash", None)

    #  Validates a payment with payment_tx_hash as empty string.
    def test_empty_payment_tx_hash(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = ""
        paid_amount = 10.0

        # Act and Assert
        with pytest.raises(ValueError):
            validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Validates a payment with payment_chain_id as empty string.
    def test_empty_payment_chain_id(self):
        # Arrange
        payment_chain_id = ""
        payment_tx_hash = "tx_hash"
        paid_amount = 10.0

        # Act and Assert
        with pytest.raises(ValueError):
            validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Validates a payment with paid_amount as empty string.
    def test_empty_paid_amount(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = "tx_hash"
        paid_amount = ""

        # Act and Assert
        with pytest.raises(ValueError):
            validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Raises ValueError when payment_chain_id is None.
    def test_none_payment_chain_id(self):
        # Arrange
        payment_chain_id = None
        payment_tx_hash = "tx_hash"
        paid_amount = 10.0

        # Act and Assert
        with pytest.raises(ValueError):
            validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Raises ValueError when payment_tx_hash is None.
    def test_none_payment_tx_hash(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = None
        paid_amount = 10.0

        # Act and Assert
        with pytest.raises(ValueError):
            validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Raises ValueError when paid_amount is None.
    def test_none_paid_amount(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = "tx_hash"
        paid_amount = None

        # Act and Assert
        with pytest.raises(ValueError):
            validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Raises SwanConnectionError when there is a network problem.
    def test_network_problem(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = "tx_hash"
        paid_amount = 10.0

        # Mock the requests.post method to raise a ConnectionError
        with pytest.raises(SwanConnectionError):
            with patch(
                "requests.post", side_effect=requests.exceptions.ConnectionError
            ):
                validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Raises SwanTimeoutError when the request times out.
    def test_request_timeout(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = "tx_hash"
        paid_amount = 10.0

        # Mock the requests.post method to raise a Timeout
        with pytest.raises(SwanTimeoutError):
            with patch("requests.post", side_effect=requests.exceptions.Timeout):
                validate_payment(payment_chain_id, payment_tx_hash, paid_amount)

    #  Raises SwanHTTPError when there is an HTTP error.
    def test_http_error(self):
        # Arrange
        payment_chain_id = "chain_id"
        payment_tx_hash = "tx_hash"
        paid_amount = 10.0

        # Mock the requests.post method to raise an HTTPError
        with pytest.raises(SwanHTTPError):
            with patch("requests.post", side_effect=requests.exceptions.HTTPError):
                validate_payment(payment_chain_id, payment_tx_hash, paid_amount)
