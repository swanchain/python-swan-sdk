""" Computing Provider code """

import logging
import requests
from typing import List, Dict, Any, Union, Tuple


from src.constants.constants import (
    SWAN_API,
    ALL_CP_MACHINE,
    COLLATERAL_BALANCE,
    CP_AVAILABLE,
    CP_LIST,
    CP_DISTRIBUTION,
    CP_DETAIL,
)
from src.exceptions.cp_exceptions import (
    SwanCPDetailInvalidInputError,
    SwanCPDetailNotFoundError,
)

from src.exceptions.request_exceptions import (
    SwanHTTPError,
    SwanRequestError,
    SwanConnectionError,
    SwanTimeoutError,
    SwanTooManyRedirectsError,
)

from src.api.engine_api import EngineAPI


class ComputerProvider(EngineAPI):
    def get_all_cp_machines(self) -> List[Dict[str, Any]]:
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

        try:
            response = self.api_client._request_without_params(
                method="GET",
                request_path=ALL_CP_MACHINE,
                swan_api=SWAN_API,
                token=self.token,
            )

            if response.get("status") == "success":
                return response.get("data", {}).get("hardware", [])
            else:
                logging.error(f"API returned an error: {response.get('message')}")
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

    def get_cp_distribution(self) -> Union[List[Dict[str, Any]], None]:
        """
        Retrieve the distribution of computing providers.

        This function makes a GET request to the specified API endpoint to obtain
        the distribution of computing providers. It expects the API to return a list
        of dictionaries with details about each provider.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the distribution of computing providers.
            None: If the request fails or an error occurs.

        Raises:
            SwanHTTPError: For HTTP errors.
            SwanConnectionError: For network-related errors.
            SwanTimeout: For request timeout errors.
            SwanRequestException: For other request-related errors.

        Example:
            api_url = "https://example.com/api/cp_distribution"
            cp_distribution = get_cp_distribution()
        """

        try:
            response = self.api_client._request_without_params(
                method="GET",
                request_path=CP_DISTRIBUTION,
                swan_api=SWAN_API,
                token=self.token,
            )

            return response.get("data", [])
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise SwanHTTPError(
                "An HTTP error occurred while retrieving distribution"
            ) from http_err

        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Error connecting: {conn_err}")
            raise SwanConnectionError(
                "A connection error occurred while retrieving distribution"
            ) from conn_err

        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error: {timeout_err}")
            raise SwanTimeoutError(
                "A timeout occurred while retrieving distribution"
            ) from timeout_err

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error during requests: {req_err}")
            raise SwanRequestError(
                "An unexpected error occurred while retrieving distribution"
            ) from req_err

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")

    def get_computing_providers_list(self, region: str) -> List[Dict[str, Any]]:
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

        data = {"region": region}

        try:
            response = self.api_client._request_with_params(
                method="POST",
                request_path=CP_LIST,
                swan_api=SWAN_API,
                params=data,
                token="GnWAOmfnNa",
                files=None,
            )
            return response
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise SwanHTTPError("HTTPError to connect to the API endpoint.")
        except requests.exceptions.ConnectionError as connection_err:
            logging.error("Failed to connect to the API endpoint.")
            raise SwanConnectionError(
                f"Could not connect to the API endpoint {connection_err}."
            )
        except requests.exceptions.Timeout as timeout_err:
            logging.error("Request to the API endpoint timed out.")
            raise SwanTimeoutError(f"The request to the API timed out {timeout_err}.")
        except ValueError:
            logging.error("Failed to decode the response from the API.")
            raise ValueError("Invalid response received from the API.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise Exception(f"An error occurred: {e}")

    def get_available_computing_providers(self) -> Dict[str, Any]:
        """
        Retrieves available computing providers along with their resources information.

        This function makes a GET request to the 'cp_available' endpoint to fetch the
        active computing providers and their resource allocation details.

        Returns:
            Dict[str, Any]: A dictionary containing the status, message, and data of the response.

        Raises:
            SwanHTTPError: For HTTP request errors.
            SwanConnectionError: For network-related errors.
            SwanTimeout: For request timeout errors.
            SwanTooManyRedirects: For too many redirects.
            SwanRequestException: For other request issues.
            ValueError: For a response that isn't JSON formatted.
            Exception: For any other unforeseen exceptions.

        Example:
            base_url = "https://api.example.com/cp_available"
            result = get_available_computing_providers()
        """

        try:
            response = self.api_client._request_without_params(
                method="GET",
                request_path=CP_AVAILABLE,
                swan_api=SWAN_API,
                token=self.token,
            )

            return response

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise SwanHTTPError(f"HTTP error occurred: {e}")

        except requests.exceptions.ConnectionError as e:
            logging.error(f"ConnectionError occurred: {e}")
            raise SwanConnectionError(f"ConnectionError occurred: {e}")

        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout occurred: {e}")
            raise SwanTimeoutError(f"Timeout occurred: {e}")

        except requests.exceptions.TooManyRedirects as e:
            logging.error(f"TooManyRedirects occurred: {e}")
            raise SwanTooManyRedirectsError(f"TooManyRedirects occurred: {e}")

        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException occurred: {e}")
            raise SwanRequestError(f"RequestException occurred: {e}")

        except ValueError as e:
            logging.error(f"JSON decode error: {e}")
            raise ValueError
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise Exception

    def get_cp_detail(self, cp_id: str) -> Tuple[Dict[str, Any], int]:
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
        if not cp_id or not isinstance(cp_id, int):
            logging.error("cp_id is required but was not provided.")
            raise SwanCPDetailInvalidInputError(
                "cp_id must be provided and cannot be an empty ."
            )

        data = {"cp_id": cp_id}

        try:
            response = self.api_client._request_with_params(
                method="POST",
                request_path=CP_DETAIL,
                swan_api=SWAN_API,
                params=data,
                token="GnWAOmfnNa",
                files=None,
            )
            return response
        except requests.HTTPError as e:
            if e.response.status_code == 404:  # type: ignore
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

    def get_collateral_balance(self, cp_address: str) -> Any:
        """
        Retrieves the collateral balance for a given computing provider.

        This function makes a GET request to the '/cp/collateral/<cp_address>' endpoint
        to retrieve the collateral balance associated with the specified computing provider address.

        Args:
            cp_address (str): The computing provider address.

        Returns:
            dict: A dictionary containing the status, message, and data (balance) if successful,
                  or status and error message if an error occurs.

        Raises:
            ValueError: If the cp_address is not a valid address format.
            ConnectionError: If there is a problem connecting to the API endpoint.
            Exception: For other unforeseen errors.

        Example:
            get_collateral_balance("0x1234abcd")
            {'status': 'success', 'message': 'Successfully retrieved collateral balance', 'data': {'balance': 100}}
        """

        data = {"cp_address": cp_address}

        try:
            response = self.api_client._request_with_params(
                method="GET",
                request_path=COLLATERAL_BALANCE,
                swan_api=SWAN_API,
                params=data,
                token="GnWAOmfnNa",
                files=None,
            )
            return response

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            raise SwanHTTPError(
                "An HTTP error occurred while retrieving collateral balance"
            ) from http_err

        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Error connecting: {conn_err}")
            raise SwanConnectionError(
                "A connection error occurred while retrieving collateral balance"
            ) from conn_err

        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error: {timeout_err}")
            raise SwanTimeoutError(
                "A timeout occurred while retrieving collateral balance"
            ) from timeout_err

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error during requests{req_err}")
            raise SwanRequestError(
                "An unexpected error occurred while retrieving collateral balance"
            ) from req_err

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")
