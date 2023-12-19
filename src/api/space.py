""" Space related functions """
from decimal import Decimal

import requests
import logging
from typing import Dict, Any
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from src.api.engine_api import EngineAPI
from src.constants.constants import SWAN_API, DEPLOYMENT_SPACE
from src.exceptions.request_exceptions import (
    SwanRequestError,
    SwanTimeoutError,
    SwanHTTPError,
)
from src.exceptions.swan_base_exceptions import SwanValueError


class Space(EngineAPI):
    def deploy_space_v1(
        self,
        paid: Decimal,
        duration: int,
        cfg_name: str,
        region: str,
        start_in: int,
        tx_hash: str,
        job_source_uri: str,
    ) -> Dict[str, Any]:
        """
        Deploy a space with given parameters.

        This function sends a POST request to a space deployment API endpoint. It handles the necessary data formatting
        and error checking.

        Args:
            paid (Decimal): The amount paid for the deployment.
            duration (int): The duration of the deployment.
            cfg_name (str): The name of the configuration.
            region (str): The region for the deployment.
            start_in (int): The start time in minutes.
            tx_hash (str): The transaction hash.
            job_source_uri (str): The URI of the job source.

        Returns:
            Dict[str, Any]: A dictionary containing the response data.

        Raises:
            SwanValueError: If any of the parameters are invalid.
            SwanConnectionError: If there is a network problem.
            SwanHTTPError: For HTTP errors.
            SwanTimeoutError: If the request times out.
            SwanRequestError: For other types of requests exceptions.

        Example:
            response = deploy_space_with_url(
                        paid=Decimal("100.00"),
                        duration=30,
                        cfg_name="example_config",
                        region="us-west-1",
                        start_in=15,
                        start_in (int): The start time in minutes.
                        tx_hash="1234567890abcdef",
                        job_source_uri="http://source.example.com"
                    )
        """

        # TODO: Enhance to use;
        #  if any(arg is None or arg == '' for arg in args):
        #         raise ValueError("Required parameters are missing or invalid")

        if (
            not paid
            or not job_source_uri
            or not cfg_name
            or not region
            or not start_in
            or not duration
            or not tx_hash
        ):
            raise SwanValueError("Required parameters are missing or invalid")

        data = {
            "job_source_uri": job_source_uri,
            "paid": str(paid),
            "duration": duration,
            "cfg_name": cfg_name,
            "region": region,
            "start_in": start_in,
            "tx_hash": tx_hash,
        }

        try:
            response = self.api_client._request_with_params(
                method="POST",
                request_path=DEPLOYMENT_SPACE,
                swan_api=SWAN_API,
                params=data,
                token="GnWAOmfnNa",
                files=None,
            )
            return response

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
            logging.error(f"Error during requests{err}")
            raise SwanRequestError(f"Error during request {err}")
