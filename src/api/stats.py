""" Stats endpoints """

import logging
import requests

from src.api.engine_api import EngineAPI
from src.constants.constants import SWAN_API, STATS_GENERAL
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanConnectionError,
    SwanTimeoutError,
    SwanRequestError,
)


class Stats(EngineAPI):
    def get_general_stats(self):
        """
        Fetches general statistics from the backend service.

        This function sends a GET request to the backend service to retrieve general statistics
        about the system, such as total jobs, running jobs, leading jobs, job duration, total users,
        and space builders.

        Returns:
            dict: A dictionary containing the general statistics if the request is successful, or an error message if not.

        Raises:
            SwanHTTPError: If the HTTP request returned an unsuccessful status code.
            SwanConnectionError: If a connection to the URL cannot be established.
            SwanTimeout: If the request timed out.
            SwanRequestException: For any other type of exception.
        """

        try:
            response = self.api_client._request_without_params(
                method="GET",
                request_path=STATS_GENERAL,
                swan_api=SWAN_API,
                token="GnWAOmfnNa",
            )
            return response  # Returns the JSON response from the API
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors (e.g., 404, 503, etc.)
            logging.info(f"HTTP error occurred: {http_err}")
            raise SwanHTTPError(f"HTTP error occurred: {http_err}")

        except requests.exceptions.ConnectionError as conn_err:
            # Handle errors due to connection problems
            logging.info(f"Connection error occurred: {conn_err}")
            raise SwanConnectionError(f"Connection error occurred: {conn_err}")

        except requests.exceptions.Timeout as timeout_err:
            # Handle request timeout errors
            logging.info(f"Timeout error occurred: {timeout_err}")
            raise SwanTimeoutError(f"Timeout error occurred: {timeout_err}")

        except requests.exceptions.RequestException as req_err:
            # Handle any other request errors
            logging.info(f"An error occurred: {req_err}")
            raise SwanRequestError(f"Request Exception: {req_err}") from req_err
