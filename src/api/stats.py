""" Stats endpoints """


import logging
import requests
from src.constants.constants import SWAN_API, STATS_GENERAL


def get_general_stats():
    """
    Fetches general statistics from the backend service.

    This function sends a GET request to the backend service to retrieve general statistics
    about the system, such as total jobs, running jobs, leading jobs, job duration, total users,
    and space builders.

    Returns:
        dict: A dictionary containing the general statistics if the request is successful, or an error message if not.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.exceptions.ConnectionError: If a connection to the URL cannot be established.
        requests.exceptions.Timeout: If the request timed out.
        requests.exceptions.RequestException: For any other type of exception.
    """
    url = f"{SWAN_API}/{STATS_GENERAL}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        return response.json()  # Returns the JSON response from the API
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 404, 503, etc.)
        logging.info(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error: {http_err}"}
    except requests.exceptions.ConnectionError as conn_err:
        # Handle errors due to connection problems
        logging.info(f"Connection error occurred: {conn_err}")
        return {"error": f"Connection error: {conn_err}"}
    except requests.exceptions.Timeout as timeout_err:
        # Handle request timeout errors
        logging.info(f"Timeout error occurred: {timeout_err}")
        return {"error": f"Timeout error: {timeout_err}"}
    except requests.exceptions.RequestException as req_err:
        # Handle any other request errors
        logging.info(f"An error occurred: {req_err}")
        return {"error": f"General error: {req_err}"}
