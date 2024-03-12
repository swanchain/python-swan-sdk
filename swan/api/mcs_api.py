import logging
from hashlib import md5
from queue import Queue
import threading
import urllib.request
import logging
import glob
import tarfile
import os
import json
import requests
import traceback
from contextlib import closing
from swan.common.utils import object_to_filename

from swan.common.constant import *
from swan.api_client import APIClient

class MCSAPI(APIClient):
    
    def __init__(self, api_key, access_token=None,  MCS_API=None, login=True):
        self.token = None
        self.api_key = api_key
        self.access_token = access_token
        self.MCS_API = MCS_API if MCS_API else MCS_POLYGON_MAIN_API
        self.gateway = None
        if login:
            self.api_key_login()
            self.gateway = self.get_gateway()

    def api_key_login(self):
        params = {'apikey': self.api_key}
        try:
            result = self._request_with_params(
                POST, "/api/v2/user/login_by_api_key", self.MCS_API, params, None, None, json_body=True)
            self.token = result['data']
            logging.info("\033[32mLogin successful\033[0m")
            return self.token
        except Exception as e:
            logging.error("\033[31m Please check your APIkey.\033[0m")
            logging.error(str(e) + "\n" + traceback.format_exc())
            logging.error(result)
            return None

    def list_buckets(self):
        try:
            result = self._request_without_params(
                GET, BUCKET_LIST, self.MCS_API, self.token)
            bucket_info_list = []
            data = result['data']
            if data:
                for bucket in data:
                    bucket_info: Bucket = Bucket(bucket)
                    bucket_info_list.append(bucket_info)
            return bucket_info_list
        except:
            logging.error("An error occurred while executing list_buckets()")
            return None

    def create_bucket(self, bucket_name):
        params = {'bucket_name': bucket_name}
        try:
            result = self._request_with_params(
                POST, CREATE_BUCKET, self.MCS_API, params, self.token, None, json_body=True)
            if result['status'] == 'success':
                logging.info("\033[32mBucket created successfully\033[0m")
                return True
            else:
                logging.error("\033[31m" + result['message'] + "\033[0m")
        except:
            logging.error("\033[31mThis bucket already exists\033[0m")

        return False

    def delete_bucket(self, bucket_name):
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {'bucket_uid': bucket_id}
            result = self._request_with_params(
                GET, DELETE_BUCKET, self.MCS_API, params, self.token, None, json_body=True)
            if result['status'] == 'success':
                logging.info("\033[32mBucket delete successfully\033[0m")
                return True
        except:
            logging.error("\033[31mCan't find this bucket\033[0m")
        return False

    def get_bucket(self, bucket_name='', bucket_id=''):
        bucketlist = self.list_buckets()
        if bucketlist:
            if bucket_id != '' and bucket_name != '':
                for bucket in bucketlist:
                    if bucket.bucket_name == bucket_name and bucket.bucket_uid == bucket_id:
                        return bucket
            if bucket_name != '' and bucket_id == '':
                for bucket in bucketlist:
                    if bucket.bucket_name == bucket_name:
                        return bucket
            if bucket_name == '' and bucket_id != '':
                for bucket in bucketlist:
                    if bucket.bucket_uid == bucket_id:
                        return bucket
        logging.error("\033[31mUser does not have this bucket\033[0m")
        return None

    # object name
    def get_file(self, bucket_name, object_name):
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {"bucket_uid": bucket_id, "object_name": object_name}

            result = self._request_with_params(
                GET, GET_FILE, self.MCS_API, params, self.token, None, json_body=True)

            if result:
                return File(result['data'], self.gateway)
        except Exception as e:
            logging.error("\033[31mCannot get file\033[0m")
            logging.error(f'{str(e)} \n {traceback.format_exc()}')
            logging.error(result)
        return

    def create_folder(self, bucket_name, folder_name, prefix=''):
        if not folder_name:
            logging.error("\033[31mFolder name cannot be empty")
            return False
        try:
            bucket_id = self._get_bucket_id(bucket_name)
            params = {"file_name": folder_name,
                      "prefix": prefix, "bucket_uid": bucket_id}
            result = self._request_with_params(
                POST, CREATE_FOLDER, self.MCS_API, params, self.token, None, json_body=True)
            if result['status'] == 'success':
                logging.info("\033[31mFolder created successfully\033[0m")
                return True
            else:
                logging.error("\033[31m" + result['message'] + "\033[0m")
                return False
        except:
            logging.error("\033[31mCan't create this folder")
            return False

    def delete_file(self, bucket_name, object_name):
        try:
            prefix, file_name = object_to_filename(object_name)
            file_list = self._get_full_file_list(bucket_name, prefix)
            if file_list is None:
                return False

            file_id = ''
            for file in file_list:
                if file.name == file_name:
                    file_id = file.id
            params = {'file_id': file_id}
            if file_id == '':
                logging.error("\033[31mCan't find the file\033[0m")
                return False
            result = self._request_with_params(
                GET, DELETE_FILE, self.MCS_API, params, self.token, None, json_body=True)
            if result['status'] == 'success':
                logging.info("\033[32mFile delete successfully\033[0m")
                return True
            else:
                logging.error("\033[31mCan't delete the file\033[0m")
                return False
        except:
            logging.error("\033[31mCan't find this bucket\033[0m")
            return False

    def list_files(self, bucket_name, prefix='', limit=10, offset=0):

        if type(limit) is not int or type(offset) is not int:
            logging.error("\033[31mInvalid parameters\033[0m")
            return None

        try:
            bucket_id = self._get_bucket_id(bucket_name)
            if bucket_id == '':
                logging.error("\033[31mCan't find this bucket\033[0m")
                return None
        except Exception as e:
            logging.error("\033[31mCan't find this bucket\033[0m")
            logging.error(f"{str(e)} \n {traceback.format_exc()}")
            return None

        try:
            params = {'bucket_uid': bucket_id, 'prefix': prefix,
                      'limit': limit, 'offset': offset}
            result = self._request_with_params(
                GET, FILE_LIST, self.MCS_API, params, self.token, None , json_body=True)
            if result['status'] == 'success':
                files = result['data']['file_list']
                file_list = []
                for file in files:
                    file_info: File = File(file, self.gateway)
                    file_list.append(file_info)
                return file_list
        except Exception as e:
            logging.error("\033[31mCan't list files\033[0m")
            logging.error(f"{str(e)} \n {traceback.format_exc()}")
            logging.error(result)
            return None

    def upload_file(self, bucket_name, object_name, file_path, replace=False):
        try:
            prefix, file_name = object_to_filename(object_name)
            bucket_id = self._get_bucket_id(bucket_name)
            if bucket_id is None:
                logging.error("\033[31mCan't find this bucket\033[0m")
                return None
            if not file_name:
                logging.error("\033[31mFile name cannot be empty")
                return None

            # if os.stat(file_path).st_size == 0:
            #     logging.error("\033[31mFile size cannot be 0\033[0m")
            #     return None

            file_size = os.stat(file_path).st_size
            with open(file_path, 'rb') as file:
                file_hash = md5(file.read()).hexdigest()
            result = self._check_file(bucket_id, file_hash, file_name, prefix)

            # Replace file if already existed
            if result['data']['file_is_exist'] and replace:
                self.delete_file(bucket_name, object_name)
                result = self._check_file(
                    bucket_id, file_hash, file_name, prefix)
            if not (result['data']['file_is_exist']):
                if not (result['data']['ipfs_is_exist']):
                    with open(file_path, 'rb') as file:
                        i = 0
                        queue = Queue()
                        self.upload_progress_bar(
                            file_name, file_size)
                        for chunk in self._read_chunks(file):
                            i += 1
                            queue.put((str(i), chunk))
                        file.close()
                    threads = list()
                    for i in range(3):
                        worker = threading.Thread(
                            target=self._thread_upload_chunk, args=(queue, file_hash, file_name))
                        threads.append(worker)
                        worker.start()
                    for thread in threads:
                        thread.join()
                    result = self._merge_file(
                        bucket_id, file_hash, file_name, prefix)
                if result is None:
                    logging.error("\033[31m Merge file failed\033[0m")
                    return None
                file_id = result['data']['file_id']
                file_info = self._get_file_info(file_id)
                if file_info is None:
                    logging.error("\033[31m Get file info failed\033[0m")
                    return None
                self._create_folders(bucket_name, prefix)
                logging.info("\033[32mFile upload successfully\033[0m")
                return file_info
            logging.error("\033[31mFile already exists\033[0m")
            return None
        except Exception as e:
            logging.error("\033[31mError while uploading file\033[0m")
            logging.error(f"{str(e)} \n {traceback.format_exc()}")
            return None

    def _create_folders(self, bucket_name, path):
        bucket_id = self._get_bucket_id(bucket_name)
        if bucket_id:
            path, folder_name = object_to_filename(path)
            while folder_name:
                params = {"file_name": folder_name,
                          "prefix": path, "bucket_uid": bucket_id}
                self._request_with_params(
                    POST, CREATE_FOLDER, self.MCS_API, params, self.token, None, json_body=True)
                path, folder_name = object_to_filename(path)
            return True
        else:
            logging.error("\033[31mBucket not found\033[0m")
            return False

    def _upload_to_bucket(self, bucket_name, object_name, file_path):
        if os.path.isdir(file_path):
            return self.upload_folder(bucket_name, object_name, file_path)
        else:
            return self.upload_file(bucket_name, object_name, file_path)

    def upload_folder(self, bucket_name, object_name, folder_path):
        prefix, folder_name = object_to_filename(object_name)
        folder_res = self.create_folder(bucket_name, folder_name, prefix)
        if folder_res is True:
            res = []
            files = os.listdir(folder_path)
            for f in files:
                f_path = os.path.join(folder_path, f)
                upload = self._upload_to_bucket(
                    bucket_name, os.path.join(object_name, f), f_path)
                res.append(upload)

            self._create_folders(bucket_name, prefix)
            return res
        return None

    def upload_ipfs_folder(self, bucket_name, object_name, folder_path):
        # folder_name = os.path.basename(object_name) or os.path.basename(folder_path)
        # prefix = os.path.normpath(os.path.dirname(object_name)) if os.path.dirname(object_name) else ''
        prefix, folder_name = object_to_filename(object_name)

        if not folder_name:
            logging.error("\033[31mFolder name cannot be empty")
            return False

        bucket_uid = self._get_bucket_id(bucket_name)
        if bucket_uid:
            files = self._read_files(folder_path, folder_name)
            form_data = {"folder_name": folder_name,
                         "prefix": prefix, "bucket_uid": bucket_uid}
            res = self._request_with_params(
                POST, PIN_IPFS, self.MCS_API, form_data, self.token, files, json_body=True)
            if res and res["data"]:
                self._create_folders(bucket_name, prefix)
                folder = (File(res["data"], self.gateway))
                return folder
            else:
                logging.error("\033[31mIPFS Folder Upload Error\033[0m")
                return None
        else:
            logging.error("\033[31mBucket not found\033[0m")
            return None

    def download_file(self, bucket_name, object_name, local_filename):
        try:
            file = self.get_file(bucket_name, object_name)
        except:
            logging.error('\033[31mFile does not exist\033[0m')
            return False

        try:
            ipfs_url = file.ipfs_url
            with open(local_filename, 'wb') as f:
                if file.size > 0:
                    data = urllib.request.urlopen(ipfs_url)
                    if data:
                        f.write(data.read())
                        logging.info(
                            "\033[32mFile downloaded successfully\033[0m")
                        return True
                    else:
                        logging.error('\033[31mDownload failed\033[0m')
                        return False
        except:
            logging.error('\033[31mDownload failed\033[0m')
            return False

    def download_ipfs_folder(self, bucket_name, object_name, folder_path):
        folder = self.get_file(bucket_name, object_name)
        if folder is None:
            logging.error('\033[31mFolder does not exist\033[0m')
            return False
        dir_name, folder_name = os.path.split(folder_path)
        download_url = folder.gateway + "/api/v0/get?arg=" + \
            folder.payloadCid + "&create=true"

        if os.path.exists(folder_path):
            logging.error('\033[31mFolder already exists\033[0m')
            return False
        try:
            with closing(requests.post(download_url, stream=True)) as resp:
                if resp.status_code != 200:
                    logging.error('\033[31mFile download failed\033[0m')
                    return False
                with tarfile.open(fileobj=resp.raw, mode="r|*") as tar:
                    tar.extractall(path=dir_name)
                first_name = next(iter(tar), None).name
                if dir_name != "":
                    first_name = dir_name + "/" + first_name
                os.rename(first_name, folder_path)
            return True
        except Exception:
            logging.error('\033[31mFile download failed\033[0m')
            return False

    def _check_file(self, bucket_id, file_hash, file_name, prefix=''):
        params = {'bucket_uid': bucket_id, 'file_hash': file_hash,
                  'file_name': file_name, 'prefix': prefix}
        return self._request_with_params(POST, CHECK_UPLOAD, self.MCS_API, params, self.token, None, json_body=True)

    def _upload_chunk(self, file_hash, file_name, chunk):
        params = {'hash': file_hash, 'file': (file_name, chunk)}
        return self._request_bucket_upload(UPLOAD_CHUNK, self.MCS_API, params, self.token)

    def _thread_upload_chunk(self, queue, file_hash, file_name):
        while not queue.empty():
            chunk = queue.get()
            self._upload_chunk(file_hash, chunk[0] + '_' + file_name, chunk[1])

    def _merge_file(self, bucket_id, file_hash, file_name, prefix=''):
        params = {'bucket_uid': bucket_id, 'file_hash': file_hash,
                  'file_name': file_name, 'prefix': prefix}
        return self._request_with_params(POST, MERGE_FILE, self.MCS_API, params, self.token, None, json_body=True)

    def _read_chunks(self, file, chunk_size=10485760):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

    def _get_bucket_id(self, bucket_name):
        bucketlist = self.list_buckets()
        if bucketlist:
            for bucket in bucketlist:
                if bucket.bucket_name == str(bucket_name):
                    return bucket.bucket_uid
        return None

    def _get_full_file_list(self, bucket_name, prefix=''):
        bucket_id = self._get_bucket_id(bucket_name)
        if bucket_id is None:
            return None
        params = {'bucket_uid': bucket_id,
                  'prefix': prefix, 'limit': 10, 'offset': 0}
        count = self._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None, json_body=True)['data'][
            'count']
        file_list = []
        for i in range(count // 10 + 1):
            params['offset'] = i * 10
            result = \
                self._request_with_params(GET, FILE_LIST, self.MCS_API, params, self.token, None, json_body=True)['data'][
                    'file_list']
            for file in result:
                file_info: File = File(file, self.gateway)
                file_list.append(file_info)
        return file_list

    def _get_file_info(self, file_id):
        params = {'file_id': file_id}
        result = self._request_with_params(
            GET, FILE_INFO, self.MCS_API, params, self.token, None, json_body=True)
        file_info = File(result['data'], self.gateway)
        return file_info

    def get_gateway(self):
        try:
            result = self._request_without_params(
                GET, GET_GATEWAY, self.MCS_API, self.token)
            if result is None:
                return
            data = result['data']
            return 'https://' + data[0]
        except:
            logging.error("\033[31m" "Get Gateway failed" "\033[0m")
            return

    def _read_files(self, root_folder, folder_name):
        # Create an empty list to store the file tuples
        file_dict = []

        # Use glob to retrieve the file paths in the directory and its subdirectories
        file_paths = glob.glob(os.path.join(
            root_folder, '**', '*'), recursive=True)

        # Loop through each file path and read the contents of the file
        for file_path in file_paths:
            if os.path.isfile(file_path):
                # Get the relative path from the root folder
                upload_path = folder_name + "/" + \
                    os.path.relpath(file_path, root_folder)
                file_dict.append(('files', (
                    upload_path, open(file_path, 'rb'))))

        return file_dict

        
class Bucket:
    def __init__(self, bucket_data):
        self.deleted_at = bucket_data["deleted_at"]
        self.updated_at = bucket_data["updated_at"]
        self.created_at = bucket_data["created_at"]
        self.file_number = bucket_data["file_number"]
        self.bucket_name = bucket_data["bucket_name"]
        self.is_deleted = bucket_data["is_deleted"]
        self.is_active = bucket_data["is_active"]
        self.is_free = bucket_data["is_free"]
        self.size = bucket_data["size"]
        self.max_size = bucket_data["max_size"]
        self.address = bucket_data["address"]
        self.bucket_uid = bucket_data["bucket_uid"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class File:
    def __init__(self, file_data, gateway = 'https://ipfs.io'):
        self.name = file_data["name"]
        self.address = file_data["address"]
        self.bucket_uid = file_data["bucket_uid"]
        self.filehash = file_data["file_hash"]
        self.prefix = file_data["prefix"]
        self.size = file_data["size"]
        self.payloadCid = file_data["payload_cid"]
        self.ipfs_url = gateway + '/ipfs/' + file_data["payload_cid"]
        self.pin_status = file_data["pin_status"]
        self.is_deleted = file_data["is_deleted"]
        self.is_folder = file_data["is_folder"]
        self.id = file_data["id"]
        self.updated_at = file_data["updated_at"]
        self.created_at = file_data["created_at"]
        self.deleted_at = file_data["deleted_at"]
        self.gateway = gateway
        self.object_name = file_data["object_name"]
        self.type = file_data["type"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)