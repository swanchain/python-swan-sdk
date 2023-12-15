""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any, Tuple
from src.constants.constants import SWAN_API, ALL_CP_MACHINE, CP_AVAILABLE
from src.exceptions.cp_exceptions import (
    SwanCPDetailInvalidInputError,
    SwanCPDetailNotFoundError,
)
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanRequestError,
    SwanConnectionError,
    SwanTimeoutError,
    SwanTooManyRedirectsError,
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


def get_cp_detail(cp_id: str) -> Tuple[Dict[str, Any], int]:
    """
    Retrieves details for a computing provider (cp) based on the given cp_id.

    Args:
        cp_id (str): The identifier of the computing provider.

    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing the response data as a dictionary and the HTTP status code.

    Raises:
        CPDetailInvalidInputError: If the cp_id is not provided or an empty string.
        CPDetailNotFoundError: If the cp is not found.
        SwanHTTPError
        ConnectionError
        SwanTimeoutError
        SwanRequestError
    """
    if not cp_id:
        logging.error("cp_id is required but was not provided.")
        raise SwanCPDetailInvalidInputError(
            "cp_id must be provided and cannot be an empty string."
        )

    url = f"{SWAN_API}/{cp_id}"  # Replace with your actual API URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise SwanCPDetailNotFoundError(
                f"Computing provider with {cp_id} not found."
            )
        raise SwanHTTPError(f"HTTP error occurred: {e}")
    except requests.ConnectionError:
        raise SwanConnectionError("Connection error occurred.")
    except requests.Timeout:
        raise SwanTimeoutError("Request timed out.")
    except requests.RequestException:
        raise SwanRequestError("Error during request.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise Exception("An unexpected error occurred.")


def get_available_computing_providers() -> Dict[str, Any]:
    """
    Retrieves available computing providers along with their resources information.

    This function makes a GET request to the 'cp_available' endpoint to fetch the
    active computing providers and their resource allocation details.

    Returns:
        Dict[str, Any]: A dictionary containing the status, message, and data of the response.

    Raises:
        SwanHTTPError: For HTTP request errors.
        SwanConnectionError: For network-related errors.
        SwanTimeout: For request timeout errors.
        SwanTooManyRedirects: For too many redirects.
        SwanRequestException: For other request issues.
        ValueError: For a response that isn't JSON formatted.
        Exception: For any other unforeseen exceptions.

    Example:
        base_url = "https://api.example.com/cp_available"
        result = get_available_computing_providers()
    """
    url = f"{SWAN_API}{CP_AVAILABLE}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise SwanHTTPError(f"HTTP error occurred: {e}")

    except requests.exceptions.ConnectionError as e:
        logging.error(f"ConnectionError occurred: {e}")
        raise SwanConnectionError(f"ConnectionError occurred: {e}")

    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout occurred: {e}")
        raise SwanTimeoutError(f"Timeout occurred: {e}")

    except requests.exceptions.TooManyRedirects as e:
        logging.error(f"TooManyRedirects occurred: {e}")
        raise SwanTooManyRedirectsError(f"TooManyRedirects occurred: {e}")

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException occurred: {e}")
        raise SwanRequestError(f"RequestException occurred: {e}")

    except ValueError as e:
        logging.error(f"JSON decode error: {e}")
        raise ValueError
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise Exception
