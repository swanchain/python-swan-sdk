# ./swan/api_client.py

import requests
import json


from swan.common.constant import GET, PUT, POST, DELETE
from swan.common import utils


class APIClient(object):

    def _request(self, method, request_path, swan_api, params, token, files=False, json_body=False):
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
                if json_body:
                    body = json.dumps(params)
                else:
                    body = params
                response = requests.post(url, data=body, headers=header)
        elif method == DELETE:
            if params:
                body = json.dumps(params)
                response = requests.delete(url, data=body, headers=header)
            else:
                response = requests.delete(url, headers=header)

        return response.json()
    
    def _request_without_params(self, method, request_path, swan_api, token):
        return self._request(method, request_path, swan_api, {}, token)

    def _request_with_params(self, method, request_path, swan_api, params, token, files, json_body=False):
        return self._request(method, request_path, swan_api, params, token, files, json_body=json_body)
