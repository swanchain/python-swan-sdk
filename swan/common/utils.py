# ./swan/common/utils.py
import requests
import os
import json
import re
import datetime

def parse_params_to_str(params):
    url = "?"
    for key, value in params.items():
        url = url + str(key) + "=" + str(value) + "&"
    return url[0:-1]

def object_to_filename(object_name):
    index = object_name.rfind('/')
    if index == -1:
        prefix = ''
        file_name = object_name
    else:
        prefix = object_name[0:index]
        file_name = object_name[index + 1:]
    return prefix, file_name


def get_raw_github_url(web_url):
    return web_url.replace(
        "https://github.com/", "https://raw.githubusercontent.com/"
    ).replace("/blob/", "/")


def read_file_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to get file")
        return None

def get_contract_abi(abi_name: str):
    """Get local contract directory.

    Args:
        abi_name: name and extension of the ABI file.

    Returns:
        Loaded abi file data in JSON.
    """
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/contract/abi/"
    with open(parent_path + abi_name, 'r') as abi_file:
        abi_data = json.load(abi_file)
        return json.dumps(abi_data)
    

def datetime_to_unixtime(datetime_str: str):
    try:
        datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        unix_timestamp = datetime_obj.timestamp()
        return unix_timestamp
    except:
        return datetime_str