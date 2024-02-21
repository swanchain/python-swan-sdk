# ./swan/common/utils.py
import requests
import os
import json


def parse_params_to_str(params):
    url = "?"
    for key, value in params.items():
        url = url + str(key) + "=" + str(value) + "&"
    return url[0:-1]


def list_repo_contents(user, repo):
    """Lists the contents of a GitHub repository.

    Parameters:
    user (str): The username of the repository owner.
    repo (str): The name of the repository.

    Returns:
    list: A list of dictionaries representing the files in the repository.
    """
    url = f"https://api.github.com/repos/{user}/{repo}/contents"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def read_file_from_url(url):
    """Reads a file from a URL.

    Parameters:
    url (str): The URL of the file.

    Returns:
    str: The content of the file.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text

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