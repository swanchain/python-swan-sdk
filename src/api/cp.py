""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any
from src.constants.constants import SWAN_API, ALL_CP_MACHINE
from src.exceptions.exceptions import HTTPError, RequestError


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
        raise HTTPError("Failed to connect to the API endpoint.")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        raise RequestError("Failed to make a request to the API.")
    except ValueError as json_err:
        logging.error(f"JSON decoding error: {json_err}")
        raise json_err


