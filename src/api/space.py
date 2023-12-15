""" Space related functions """

import requests
import logging
from typing import Dict, Any
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from src.constants.constants import SWAN_API, GET_DEPLOYMENT_INFO
from src.exceptions.request_exceptions import (
    SwanRequestError,
    SwanTimeoutError,
    SwanHTTPError,
)
from src.exceptions.swan_base_exceptions import SwanValueError


def get_space_deployment_info(
    task_uuid: str,
    job_source_uri: str,
    paid: int,
    duration: int,
    cfg_name: str,
    region: str,
    start_in: int,
    wallet: str,
) -> Dict[str, Any]:
    """
    Posts deployment data to the space deployment API for a given task UUID.

    Args:
        task_uuid (str): The unique identifier for the task.
        job_source_uri (str): URI for the job source.
        paid (int): Indicate whether the job is paid or not (1 for paid, 0 for unpaid).
        duration (int): Duration of the job in seconds.
        cfg_name (str): Configuration name.
        region (str): The region where the job is deployed.
        start_in (int): The start time in seconds.
        wallet (str): The wallet address.

    Returns:
        Dict[str, Any]: A dictionary containing the response data.

    Raises:
        SwanValueError: If any of the parameters are invalid.
        SwanConnectionError: If there is a network problem.
        SwanHTTPError: For HTTP errors.
        SwanTimeoutError: If the request times out.
        SwanRequestError: For other types of requests exceptions.
    """

    if not task_uuid or not job_source_uri or not cfg_name or not region or not wallet:
        raise ValueError("Required parameters are missing or invalid")

    url = f"{SWAN_API}{GET_DEPLOYMENT_INFO}{task_uuid}"

    data = {
        "job_source_uri": job_source_uri,
        "paid": paid,
        "duration": duration,
        "cfg_name": cfg_name,
        "region": region,
        "start_in": start_in,
        "wallet": wallet,
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()

        # Check if response content is not empty and is JSON format
        if response.content:
            return response.json()
        else:
            return {"message": "No content in response"}

    except ValueError as ve:
        logging.error(f"Invalid input: {ve}")
        raise SwanValueError(f"Invalid input: {ve}")
    except ConnectionError as ce:
        logging.error("Network problem occurred")
        raise SwanValueError(f"Network problem occurred: {ce}")
    except Timeout as tm:
        logging.error("Request timed out")
        raise SwanTimeoutError(f"Request timed out: {tm}")
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise SwanHTTPError(f"HTTP error occurred: {http_err}")
    except RequestException as err:
        logging.error(f"Error during requests to {url} : {err}")
        raise SwanRequestError(f"Error during requests to {url} : {err}")

