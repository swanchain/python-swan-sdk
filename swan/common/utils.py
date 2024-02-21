# ./swan/common/utils.py
import requests
import re


def parse_params_to_str(params):
    url = "?"
    for key, value in params.items():
        url = url + str(key) + "=" + str(value) + "&"
    return url[0:-1]

def list_repo_contents(repo_url):
    """
    Lists the contents of a GitHub repository and gets the raw contents of the .env file, the Dockerfile, and all .yml files.

    Parameters:
    repo_url (str): The URL of the repository.

    Returns:
    dict: A dictionary where the keys are the filenames and the values are the raw contents of the files.
    """
    parts = repo_url.split('/')
    user = parts[-2]
    repo = parts[-1]

    url = f"https://api.github.com/repos/{user}/{repo}/contents"
    response = requests.get(url)
    response.raise_for_status()
    repo_contents = response.json()

    file_contents = {}
    for item in repo_contents:
        if item['type'] == 'file' and (item['name'] in ['.env', 'Dockerfile'] or re.search(r'\.yml$', item['name'])):
            raw_url = item['download_url']
            file_content = read_file_from_url(raw_url)
            if file_content is not None:
                file_contents[item['name']] = file_content

    return file_contents

def get_raw_github_url(web_url):
    return web_url.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/')

def read_file_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print('Failed to get file')
        return None
