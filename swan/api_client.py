# ./swan/api_client.py

import requests
import json
import logging
from tqdm import tqdm
from pathlib import Path
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

from swan.common.constant import GET, PUT, POST, DELETE, SWAN_API
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
    
    def _request_stream_upload(self, request_path, swan_api, params, token):
        url = swan_api + request_path
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
            raise Exception
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise Exception

        return response.json()

    def _request_bucket_upload(self, request_path, swan_api, params, token):
        url = swan_api + request_path
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
            raise Exception
        json_res = response.json()
        if str(json_res['status']) == 'error':
            raise Exception

        return response.json()

    def upload_progress_bar(self, file_name, file_size):
        self.bar = tqdm(desc=file_name, total=file_size,
                        unit='B', unit_scale=True, unit_divisor=1024)

    def _request_without_params(self, method, request_path, swan_api, token):
        return self._request(method, request_path, swan_api, {}, token)

    def _request_with_params(self, method, request_path, swan_api, params, token, files, json_body=False):
        return self._request(method, request_path, swan_api, params, token, files, json_body=json_body)

class Previous():
    def __init__(self):
        self.previous = 0

    def update(self, new):
        self.old = self.previous
        self.previous = new
        return self.previous - self.old