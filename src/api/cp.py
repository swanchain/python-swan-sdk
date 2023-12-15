""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any, Tuple
from src.constants.constants import SWAN_API, ALL_CP_MACHINE
from src.exceptions.cp_exceptions import (
    SwanCPDetailInvalidInputError,
    SwanCPDetailNotFoundError,
)
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
