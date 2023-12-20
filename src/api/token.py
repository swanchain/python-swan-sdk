""" Token Related functionalities"""

import requests

from src.api.engine_api import EngineAPI
from src.constants.constants import SWAN_API, TOKEN_VALIDATION
from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanConnectionError,
    SwanTimeoutError,
    SwanRequestError,
)
from src.exceptions.task_exceptions import SwanTaskInvalidInputError


class Token(EngineAPI):
    def validate_token(self, token):
        """
        Validate an API token by sending it to the server.

        This function sends a POST request to the APIs validation endpoint
        with the provided API token. It returns the server's response indicating
        whether the token is valid or invalid.

        Args:
            token (str): The API token to be validated.

        Returns:
            dict: A dictionary containing the server's response, including
                  the status of the token ('Token Validated' or 'Token Invalid')
                  and the response status code.

        Example:
            response = validate_api_token("your_api_token")
        """

        if not token:
            raise SwanTaskInvalidInputError("Please Provide TASK ID")

        # The endpoint for validating the API token
        data = {"token": token}

        try:
            response = self.api_client._request_with_params(
                method="POST",
                request_path=TOKEN_VALIDATION,
                swan_api=SWAN_API,
                params=data,
                token="GnWAOmfnNa",
                files=None,
            )
            return response

        except requests.exceptions.HTTPError as errh:
            # Raise a custom HTTPError
            raise SwanHTTPError(f"HTTP Error: {errh}") from errh

        except requests.exceptions.ConnectionError as errc:
            # Raise a custom ConnectionError
            raise SwanConnectionError(f"Connection Error: {errc}") from errc

        except requests.exceptions.Timeout as errt:
            # Raise a custom TimeoutError
            raise SwanTimeoutError(f"Timeout Error: {errt}") from errt

        except requests.exceptions.RequestException as err:
            # Raise a custom RequestError
            raise SwanRequestError(f"Request Exception: {err}") from err
