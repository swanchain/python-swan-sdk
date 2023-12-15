""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any, Union
from src.constants.constants import SWAN_API, ALL_CP_MACHINE, COLLATERAL_BALANCE
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanRequestError,
    SwanConnectionError,
    SwanTimeoutError,
)


def get_all_cp_machines() -> List[Dict[str, Any]]:
    """
    Retrieve all computing provider machines available.

    This function makes a GET request to the specified endpoint and
    returns a list of hardware configurations available.


    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a hardware configuration.

    Raises:
        HTTPError: If the API call fails.
        RequestError: If the response is not a valid JSON.
    """
    endpoint = f"{SWAN_API}{ALL_CP_MACHINE}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raises HTTPError for HTTP errors.

        data = response.json()
        if data.get("status") == "success":
            return data.get("data", {}).get("hardware", [])
        else:
            logging.error(f"API returned an error: {data.get('message')}")
            return []
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise SwanHTTPError("Failed to connect to the API endpoint.")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        raise SwanRequestError("Failed to make a request to the API.")
    except ValueError as json_err:
        logging.error(f"JSON decoding error: {json_err}")
        raise json_err


def get_collateral_balance(cp_address: str) -> Dict[str, Union[str, Any]]:
    """
    Retrieves the collateral balance for a given computing provider.

    This function makes a GET request to the '/cp/collateral/<cp_address>' endpoint
    to retrieve the collateral balance associated with the specified computing provider address.

    Args:
        cp_address (str): The computing provider address.

    Returns:
        dict: A dictionary containing the status, message, and data (balance) if successful,
              or status and error message if an error occurs.

    Raises:
        ValueError: If the cp_address is not a valid address format.
        ConnectionError: If there is a problem connecting to the API endpoint.
        Exception: For other unforeseen errors.

    Example:
        get_collateral_balance("0x1234abcd")
        {'status': 'success', 'message': 'Successfully retrieved collateral balance', 'data': {'balance': 100}}
    """

    # Endpoint configuration
    endpoint = f"{SWAN_API}{COLLATERAL_BALANCE}{cp_address}"

    try:
        # Making a GET request to the API
        response = requests.get(endpoint)
        response.raise_for_status()  # Will raise an HTTPError for bad requests

        # Parsing the JSON response
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise SwanHTTPError(
            "An HTTP error occurred while retrieving collateral balance"
        ) from http_err

    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Error connecting: {conn_err}")
        raise SwanConnectionError(
            "A connection error occurred while retrieving collateral balance"
        ) from conn_err

    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error: {timeout_err}")
        raise SwanTimeoutError(
            "A timeout occurred while retrieving collateral balance"
        ) from timeout_err

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error during requests to {endpoint}: {req_err}")
        raise SwanRequestError(
            "An unexpected error occurred while retrieving collateral balance"
        ) from req_err

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error occurred: {e}")
