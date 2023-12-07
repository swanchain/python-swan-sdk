""" APIClient related code """

from swan.common.constants import *
import requests
import json
import logging
from swan.common import utils
from swan.common import constants as c


class APIClient(object):
    def __init__(
        self,
        api_key,
        wallet_address,
        chain_name=None,
        login=True,
        is_calibration=False,
    ):
        self.AUCTION_API = AUCTION_API
        # TODO: Once authentication is Implemented for Auction Engine we can uncomment this
        self.token = None
        self.api_key = (api_key,)
        self.wallet_address = (wallet_address,)
        if login:
            self.api_key_login()

    def api_key_login(self):
        params = {"api_key": self.api_key[0], "wallet_address": self.wallet_address[0]}
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
        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        url = swan_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        response = None
        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.PUT:
            # body = json.dumps(params)
            response = requests.put(url, data=params, headers=header)
        elif method == c.POST:
            if files:
                body = params
                response = requests.post(url, data=body, headers=header, files=files)
            else:
                # body = json.dumps(params) if method == c.POST else ""
                response = requests.post(url, data=params, headers=header)
        elif method == c.DELETE:
            if params:
                body = json.dumps(params)
                response = requests.delete(url, data=body, headers=header)
            else:
                response = requests.delete(url, headers=header)

        # exception handle
        if not str(response.status_code).startswith("2"):
            print(response.status_code)
            json_res = response.json()
            print(json_res["message"])
            return None
        #     raise exceptions.McsAPIException(response)
        #
        # if str(json_res['status']) == 'error':
        #     raise exceptions.McsRequestException(json_res['message'])
        return response.json()

    def _request_without_params(self, method, request_path, swan_api, token):
        return self._request(method, request_path, swan_api, {}, token)

    def _request_with_params(
        self, method, request_path, swan_api, params, token, files
    ):
        return self._request(method, request_path, swan_api, params, token, files)
