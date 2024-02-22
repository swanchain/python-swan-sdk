# ./swan/common/utils.py
import requests
import re
from urllib.parse import urlparse
from swan_mcs import BucketAPI
from swan.common import mcs_api
from swan.common.file import File


def parse_params_to_str(params):
    url = "?"
    for key, value in params.items():
        url = url + str(key) + "=" + str(value) + "&"
    return url[0:-1]


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


def upload_file(file_path: str, bucket_name: str, dest_file_path: str) -> File:
    """
    Upload a file by file path, bucket name and the target path
    :rtype: object
    :param file_path: the source file path
    :param bucket_name: the bucket name user want to upload
    :param dest_file_path: the destination of the file you want to store exclude the bucket name
    :return: File Object
    """

    bucket_client = BucketAPI(mcs_api)
    # check if file exist
    file_data = bucket_client.upload_file(bucket_name, dest_file_path, file_path)
    return file_data
