""" Utility functions for SDK """


import logging
import requests
from decimal import Decimal
from typing import Tuple, Dict, Any

from src.api.engine_api import EngineAPI
from src.constants.constants import SWAN_API, PAYMENT_VALIDATION
from src.exceptions.request_exceptions import (
    SwanConnectionError,
    SwanTimeoutError,
    SwanHTTPError,
)
from src.exceptions.swan_base_exceptions import SwanRequestException


def parse_params_to_str(params):
    url = "?"
    for key, value in params.items():
        url = url + str(key) + "=" + str(value) + "&"
    return url[0:-1]


class Payments(EngineAPI):
    def validate_payment(
        self, payment_chain_id: str, payment_tx_hash: str, paid_amount: float
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Validates a payment by sending a POST request to the payment validation API.

        Args:
            payment_chain_id (str): The chain ID where the payment contract is deployed.
            payment_tx_hash (str): The transaction hash of the payment in the contract.
            paid_amount (float): The amount of money which should be paid in the transaction.

        Returns:
            Tuple[bool, Dict[str, Any]]: A tuple containing a boolean indicating the success of the validation,
            and a dictionary with the response data.

        Raises:
            SwanConnectionError: If a network problem occurs.
            SwanTimeout: If the request times out.
            SwanTooManyRedirects: If too many redirects happen.
            SwanHTTPError: For HTTP errors.
            SwanRequestException: For any other request issues.
            ValueError: If the response from the API is not as expected.
            KeyError: If expected keys are missing in the response.
        """
        if not payment_chain_id or not payment_tx_hash or not paid_amount:
            raise ValueError("Please provide necessary parameters")

        data = {
            "chain_id": payment_chain_id,
            "tx_hash": payment_tx_hash,
            "paid_amount": f"{Decimal(paid_amount):.5f}",  # Formatting to match the required decimal format
        }

        try:
            response = self.api_client._request_with_params(
                method="POST",
                request_path=PAYMENT_VALIDATION,
                swan_api=SWAN_API,
                params=data,
                token=self.token,
                files=None,
            )

            if response is None:
                raise ValueError("Invalid response from API")

            status = response.get("status") == "Success"
            return status, response

        except requests.exceptions.ConnectionError as e:
            logging.error(f"Network problem: {e}")
            raise SwanConnectionError(f"Network problem: {e}")
        except requests.exceptions.Timeout as e:
            logging.error(f"Request timed out: {e}")
            raise SwanTimeoutError(f"Request timed out: {e}")
        except requests.exceptions.TooManyRedirects as e:
            logging.error(f"Too many redirects: {e}")
            raise
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error: {e}")
            raise SwanHTTPError(f"Request failed: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise SwanRequestException(f"Request failed: {e}")
        except KeyError as e:
            logging.error(f"Missing data in response: {e}")
            raise KeyError(f"Missing data in response: {e}")
        except ValueError as e:
            logging.error(f"Invalid response: {e}")
            raise ValueError(f"Invalid response: {e}")
