""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any
from src.constants.constants import SWAN_API, ALL_CP_MACHINE, CP_LIST
from src.exceptions.request_exceptions import SwanHTTPError, SwanRequestError, SwanConnectionError, SwanTimeoutError


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


def get_computing_providers_list(region: str) -> List[Dict[str, Any]]:
    """
    Fetches a list of computing providers from the API based on the given region and hardware.

    Args:
        region (str): The region for which computing providers are requested.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing details of computing providers.

    Raises:
        SwanHTTPError: If the API call fails.
        SwanConnectionError: If there is a network problem connecting to the API.
        SwanTimeoutError: If the request to the API times out.
        ValueError: If the response from the API cannot be decoded.
        Exception: For other types of exceptions.

    """
    if not region:
        raise ValueError("Please provide a valid Region")

    url = f"{SWAN_API}{CP_LIST}"
    data = {"region": region}

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise SwanHTTPError("HTTPError to connect to the API endpoint.")
    except requests.exceptions.ConnectionError as connection_err:
        logging.error("Failed to connect to the API endpoint.")
        raise SwanConnectionError(f"Could not connect to the API endpoint {connection_err}.")
    except requests.exceptions.Timeout as timeout_err:
        logging.error("Request to the API endpoint timed out.")
        raise SwanTimeoutError(f"The request to the API timed out {timeout_err}.")
    except ValueError:
        logging.error("Failed to decode the response from the API.")
        raise ValueError("Invalid response received from the API.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise Exception(f"An error occurred: {e}")