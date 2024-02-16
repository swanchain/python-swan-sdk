# ./swan/api_client.py

import requests
import json
import logging

from swan.common.constant import GET, PUT, POST, DELETE, SWAN_API, APIKEY_LOGIN
from swan.common import utils


class APIClient(object):

    def __init__(self, api_key: str, login: bool = True, environment: str = ""):
        """Initialize user configuration and login

        Args:
            api_key: SwanHub API key, generated through website
            login: Login into Swanhub or Not
            environment: Selected server 'production/calibration'
        """
        self.token = None
        self.api_key = api_key
        self.environment = environment
        if login:
            self.api_key_login()

    def api_key_login(self):
        """Login with SwanHub API Key

        Returns:
            A str access token for further SwanHub API access in
            current session.
        """
        params = {"api_key": self.api_key}
        try:
            result = self._request_with_params(
                POST, APIKEY_LOGIN, SWAN_API, params, None, None
            )
            self.token = result["data"]
            logging.info("Login Successfully!")
        except:
            logging.error("Login Failed!")

    def _request(self, method, request_path, swan_api, params, token, files=False):
        if method == GET:
            request_path = request_path + utils.parse_params_to_str(params)
        url = swan_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        response = None
        if method == GET:
            response = requests.get(url, headers=header)
        elif method == PUT:
            # body = json.dumps(params)
            response = requests.put(url, data=params, headers=header)
        elif method == POST:
            if files:
                body = params
                response = requests.post(url, data=body, headers=header, files=files)
            else:
                # body = json.dumps(params) if method =POST else ""
                response = requests.post(url, data=params, headers=header)
        elif method == DELETE:
            if params:
                body = json.dumps(params)
                response = requests.delete(url, data=body, headers=header)
            else:
                response = requests.delete(url, headers=header)

        return response.json()

    def _request_without_params(self, method, request_path, swan_api, token):
        return self._request(method, request_path, swan_api, {}, token)

    def _request_with_params(
        self, method, request_path, swan_api, params, token, files
    ):
        return self._request(method, request_path, swan_api, params, token, files)
