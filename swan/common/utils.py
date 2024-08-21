# ./swan/common/utils.py
import io
import pathlib
import tarfile
from typing import Optional, List

import requests
import os
import json
import re
import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


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


def pack_project_to_stream(
        project_path: pathlib.Path,
        exclude_dirs: Optional[List[str]] = None
) -> io.BytesIO:
    """
    Pack the project directory into a tar.gz stream, excluding specified directories.

    Args:
    project_path (pathlib.Path): The path to the project directory.
    exclude_dirs (Optional[List[str]]): List of directory names to exclude.

    Returns:
    io.BytesIO: A stream containing the packed project as tar.gz.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    # Create a BytesIO object to hold the tar.gz data
    tar_stream = io.BytesIO()

    # Create a tarfile object, which will write to our BytesIO stream
    with tarfile.open(fileobj=tar_stream, mode="w:gz") as tar:
        # Walk through the project directory
        for item in project_path.rglob("*"):
            # Check if the item is a directory and if it should be excluded
            if item.is_dir() and item.name in exclude_dirs:
                continue

            # If it's not an excluded directory, add it to the tar
            # We use arcname to make paths relative to project_path
            tar.add(item, arcname=item.relative_to(project_path.parent))

    # Reset the stream position to the beginning
    tar_stream.seek(0)
    return tar_stream


def encrypt_stream(input_stream: io.BytesIO) -> io.BytesIO:
    """
    Encrypt a BytesIO stream using AES-256 in CBC mode with PKCS7 padding.
    The key is embedded in the output stream.

    Args:
    input_stream (io.BytesIO): The input stream to encrypt.

    Returns:
    io.BytesIO: A stream containing the key, IV, and encrypted data.
    """
    # Generate a random 256-bit key
    key = os.urandom(32)  # 32 bytes = 256 bits

    # Generate a random 128-bit IV (Initialization Vector)
    iv = os.urandom(16)  # 16 bytes = 128 bits

    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Create a padder
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    # Read the input stream
    data = input_stream.getvalue()

    # Pad the data
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Create the output stream
    output_stream = io.BytesIO()

    # Write the key
    output_stream.write(key)

    # Write the IV
    output_stream.write(iv)

    # Write the encrypted data
    output_stream.write(encrypted_data)

    # Reset the stream position to the beginning
    output_stream.seek(0)

    return output_stream
