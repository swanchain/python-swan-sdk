# ./swan/api_client.py

import requests
import json
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
from pathlib import Path

from swan.common.constant import *
from swan.common.params import Params
from swan.common import exception, utils




# Orchestrator APIClient
class OrchestratorAPIClient(object):

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




# Bucket APIClient
class BucketAPIClient(object):
    def __init__(self, api_key, access_token=None, chain_name=None, login=True, is_calibration=False):
        self.token = None
        # if chain_name is None:
        #     chain_name = "polygon.mainnet"
        self.is_calibration = is_calibration
        self.api_key = api_key
        self.access_token = access_token
        self.MCS_API = Params(self.is_calibration).MCS_API
        if login:
            self.api_key_login()

    def get_params(self):
        return self._request_without_params(GET, MCS_PARAMS, self.MCS_API, self.token)

    def get_price_rate(self):
        return self._request_without_params(GET, PRICE_RATE, self.MCS_API, self.token)

    def get_gateway(self):
        res = self._request_without_params(
            GET, GET_GATEWAY, self.MCS_API, self.token)
        if res:
            gateway = res["data"][0]
            return gateway
        else:
            logging.error("\033[31m Get Gateway error\033[0m")
            return

    def api_key_login(self):
        params = {'apikey': self.api_key}
        # if params.get('apikey') == '' or params.get('access_token') == '' or params.get('chain_name') == '':
        #     logging.error("\033[31mAPIkey, access token, or chain name does not exist\033[0m")
        #     return
        try:
            result = self._request_with_params(
                POST, APIKEY_LOGIN, self.MCS_API, params, None, None)
            self.token = result['data']
            logging.info("\033[32mLogin successful\033[0m")
            return self.token
        except:
            logging.error("\033[31m Please check your APIkey.\033[0m")
            return

    def _request(self, method, request_path, mcs_api, params, token, files=False):
        if method == GET:
            request_path = request_path + utils.parse_params_to_str(params)
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        response = None
        if method == GET:
            response = requests.get(url, headers=header)
        elif method == PUT:
            body = json.dumps(params)
            response = requests.put(url, data=body, headers=header)
        elif method == POST:
            if files:
                body = params
                response = requests.post(
                    url, data=body, headers=header, files=files)
            else:
                body = json.dumps(params) if method == POST else ""
                response = requests.post(url, data=body, headers=header)
        elif method == DELETE:
            if params:
                body = json.dumps(params)
                response = requests.delete(url, data=body, headers=header)
            else:
                response = requests.delete(url, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            json_res = response.json()
            # print(json_res['message'])
            return None
        #     raise exceptions.McsAPIException(response)
        #
        # if str(json_res['status']) == 'error':
        #     raise exceptions.McsRequestException(json_res['message'])
        return response.json()

    def _request_stream_upload(self, request_path, mcs_api, params, token):
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        path = Path(params['file'][0])
        size = path.stat().st_size
        filename = path.name
        with tqdm(
                desc=filename,
                total=size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            encode = MultipartEncoder(params)
            body = MultipartEncoderMonitor(
                encode, lambda monitor: bar.update(monitor.bytes_read - bar.n)
            )
            header['Content-Type'] = body.content_type
            response = requests.post(url, data=body, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exception.McsAPIException(response)
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise exception.McsRequestException(json_res['message'])

        return response.json()

    def _request_bucket_upload(self, request_path, mcs_api, params, token):
        url = mcs_api + request_path
        header = {}
        if token:
            header["Authorization"] = "Bearer " + token
        # send request
        encode = MultipartEncoder(params)
        previous = Previous()
        body = MultipartEncoderMonitor(
            encode, lambda monitor: self.bar.update(
                previous.update(monitor.bytes_read)),
        )
        header['Content-Type'] = body.content_type
        response = requests.post(url, data=body, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise exception.McsAPIException(response)
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise exception.McsRequestException(json_res['message'])

        return response.json()

    def upload_progress_bar(self, file_name, file_size):
        self.bar = tqdm(desc=file_name, total=file_size,
                        unit='B', unit_scale=True, unit_divisor=1024)

    def _request_without_params(self, method, request_path, mcs_api, token):
        return self._request(method, request_path, mcs_api, {}, token)

    def _request_with_params(self, method, request_path, mcs_api, params, token, files):
        return self._request(method, request_path, mcs_api, params, token, files)


class Previous():
    def __init__(self):
        self.previous = 0

    def update(self, new):
        self.old = self.previous
        self.previous = new
        return self.previous - self.old
