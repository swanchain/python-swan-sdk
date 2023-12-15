""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any, Union
from src.constants.constants import SWAN_API, ALL_CP_MACHINE, CP_DISTRIBUTION
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


def get_cp_distribution() -> Union[List[Dict[str, Any]], None]:
    """
    Retrieve the distribution of computing providers.

    This function makes a GET request to the specified API endpoint to obtain
    the distribution of computing providers. It expects the API to return a list
    of dictionaries with details about each provider.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the distribution of computing providers.
        None: If the request fails or an error occurs.

    Raises:
        SwanHTTPError: For HTTP errors.
        SwanConnectionError: For network-related errors.
        SwanTimeout: For request timeout errors.
        SwanRequestException: For other request-related errors.

    Example:
        api_url = "https://example.com/api/cp_distribution"
        cp_distribution = get_cp_distribution()
    """

    endpoint = f"{SWAN_API}{CP_DISTRIBUTION}"

    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise SwanHTTPError(
            "An HTTP error occurred while retrieving distribution"
        ) from http_err

    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Error connecting: {conn_err}")
        raise SwanConnectionError(
            "A connection error occurred while retrieving distribution"
        ) from conn_err

    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error: {timeout_err}")
        raise SwanTimeoutError(
            "A timeout occurred while retrieving distribution"
        ) from timeout_err

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error during requests to {endpoint}: {req_err}")
        raise SwanRequestError(
            "An unexpected error occurred while retrieving distribution"
        ) from req_err

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error occurred: {e}")
