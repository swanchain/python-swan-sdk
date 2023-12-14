""" Tasks module and APIs"""
import logging
from typing import Dict, Any

import requests

from src.constants.constants import SWAN_API, TASK_BIDDING
from src.exceptions.exceptions import (
    HTTPError,
    RequestError,
    ConnectionError,
    TimeoutError,
)


def get_task_bidding(task_id) -> Dict[str, Any]:
    """
    Fetches the current state of a bidding task from the API.

    This function makes a GET request to the TASK_BIDDING endpoint of the API
    to retrieve the current state of a bidding task identified by `task_id`.

    Args:
        task_id (str): The unique identifier of the task.

    Returns:
        dict: A dictionary containing the response data, including
              the task bidding information if the request is successful.

    Raises:
        HTTPError: For HTTP-related errors.
        ConnectionError: For network-related errors.
        TimeoutError: If the request times out.
        RequestError: For other request-related errors.
    """
    base_url = SWAN_API
    # Construct the full URL for the API endpoint
    url = f"{base_url}/{TASK_BIDDING}"

    # Parameters to be sent with the request
    params = {"task_id": task_id}

    # Make the GET request to the API endpoint
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()  # Raises an exception for HTTP errors
    except requests.exceptions.HTTPError as http_err:
        logging.info("HTTP error occurred on TASK_BIDDING API ")
        raise HTTPError(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        logging.info("ConnectionError error occurred on TASK_BIDDING API ")
        raise ConnectionError(f"Connection error occurred: {conn_err}")

    except requests.exceptions.Timeout as timeout_err:
        logging.info("TimeoutError error occurred on TASK_BIDDING API ")
        raise TimeoutError(f"Timeout error occurred: {timeout_err}")

    except requests.exceptions.RequestException as req_err:
        logging.info("RequestError error occurred on TASK_BIDDING API ")
        raise RequestError(f"API request failed: {req_err}")

    return response.json()
