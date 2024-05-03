# ./swan/common/utils.py
import requests
import os
import json
import re
import datetime
import time
from urllib.parse import urlparse
from swan.common.file import File

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


def list_repo_contents(source_code_url):
    """
    Lists the contents of a GitHub or IPFS repository and gets the raw contents of the .env file, the Dockerfile, and all .yml files.

    Parameters:
    source_code_url (str): The URL of the repository.

    Returns:
    dict: A dictionary where the keys are the filenames and the values are the raw contents of the files.
    """
    file_contents = {}

    if "github.com" in source_code_url:
        # Handle GitHub links
        # Extract the username and repository name from the URL
        parts = source_code_url.split("/")
        user = parts[-2]
        repo = parts[-1]

        url = f"https://api.github.com/repos/{user}/{repo}/contents"
        response = requests.get(url)
        response.raise_for_status()
        repo_contents = response.json()

        for item in repo_contents:
            if item["type"] == "file" and (
                item["name"] in [".env", "Dockerfile"]
                or re.search(r"\.yml$", item["name"])
            ):
                raw_url = item["download_url"]
                file_content = requests.get(raw_url).text
                if file_content is not None:
                    file_contents[item["name"]] = file_content
    else:
        # Handle IPFS links
        parsed_url = urlparse(source_code_url)
        gateway_url = f"{parsed_url.scheme}://{parsed_url.netloc}/ipfs/"
        file_hash = source_code_url.split("/")[-1]
        response = requests.get(gateway_url + file_hash)
        response.raise_for_status()
        file_contents[file_hash] = response.text

    return file_contents


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