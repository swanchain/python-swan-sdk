import logging
from typing import Tuple, Dict, Any

import requests

from src.api.engine_api import EngineAPI
from src.constants.constants import CLAIM_REVIEW, SWAN_API
from src.exceptions.request_exceptions import SwanConnectionError, SwanTimeoutError, SwanHTTPError, SwanRequestError


class Claims(EngineAPI):
    def review_claim(self, task_uuid: str) -> Tuple[Dict[str, Any], int]:
        """
        Review a claim for a given task UUID.
        This function sends a POST request to the claim review endpoint with the specified task UUID.
        It includes detailed exception handling to manage different types of errors effectively.
        Args:
            task_uuid (str): The UUID of the task for which the claim review is to be processed.
        Returns:
            Tuple[Dict[str, Any], int]: A tuple containing the response (a dictionary) and HTTP status code.
        Raises:
            SwanConnectionError: If a network problem (e.g., DNS failure, refused connection, etc.) occurs.
            SwanTimeout: If the request times out.
            SwanHTTPError: For HTTP errors.
            SwanRequestError: For other types of requests-related issues.
            SwanValueError: If the response from the server is not in expected format.
            Exception: For any other unexpected issues.
        Example:
            review_claim("123e4567-e89b-12d3-a456-426655440000")
            ({"message": "Refund approved", "status": "success"}, 200)
        """
        if not task_uuid:
            logging.error("TASK UUID not provided")
            raise ValueError("TASK UUID not provided")

        data = {"task_uuid": task_uuid}  # Payload with task_uuid

        try:
            response = self.api_client._request_with_params(
                method="POST",
                request_path=CLAIM_REVIEW,
                swan_api=SWAN_API,
                params=data,
                token=self.token,
                files=None,
            )

            return response

        except requests.ConnectionError as conn_err:
            logging.error(f"Network problem: {conn_err}")
            raise SwanConnectionError(f"Network problem: {conn_err}")

        except requests.Timeout as timeout_err:
            logging.error(f"Request timed out: {timeout_err}")
            raise SwanTimeoutError(f"Request timed out: {timeout_err}")

        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise SwanHTTPError(f"HTTP error occurred: {http_err}")

        except requests.RequestException as req_err:
            logging.error(f"Error during request: {req_err}")
            raise SwanRequestError(f"Error during request: {req_err}")

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error: {e}")