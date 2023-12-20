""" APIClient related code """

import requests
import json
import logging

from src.constants.constants import (
    POST,
    APIKEY_LOGIN,
    SWAN_API,
    GET,
    PUT,
    DELETE,
)
from src.utils import utils


class APIClient(object):
    def __init__(
        self,
        api_key,
        wallet_address,
        chain_name=None,
        login=True,
        is_calibration=False,
    ):
        self.SWAN_API = SWAN_API
        # TODO: Once authentication is Implemented for Auction Engine we can uncomment this
        self.token = None
        self.api_key = api_key
        self.wallet_address = wallet_address
        if login:
            self.api_key_login()
        self.is_calibration = is_calibration
        self.chain_name = chain_name

    def api_key_login(self):
        params = {"api_key": self.api_key, "wallet_address": self.wallet_address}
        # if params.get('apikey') == '' or params.get('access_token') == '' or params.get('chain_name') == '':
        #     logging.error("\033[31mAPIkey, access token, or chain name does not exist\033[0m")
        #     return
        try:
            result = self._request_with_params(
                POST, APIKEY_LOGIN, SWAN_API, params, None, None
            )
            self.token = result["data"]
            logging.info("\033[32mLogin successful\033[0m")
            return self.token
        except Exception as e:
            logging.error(str(e))
            logging.error("\033[31m Please check your APIkey.\033[0m")
            return

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
