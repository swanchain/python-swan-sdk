import base64
import io
import json
import os
import pathlib
import tarfile
from typing import Optional, List, Dict

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


PRIVATE_TASK_DEFAULT_DIRS_EXCLUDE = ".git", "venv", "node_modules", ".github"
BUFFER_SIZE = 8192


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
    # Read the input stream
    data = input_stream.getvalue()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = bytearray()

    for i in range(0, len(data), BUFFER_SIZE):
        chunk = data[i:i + BUFFER_SIZE]
        encrypted_chunk = encryptor.update(chunk)
        encrypted_data.extend(encrypted_chunk)

    encrypted_data.extend(encryptor.finalize())

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


class PrivateProject:
    def __init__(self, download_uri: str, encryption_key_base64: str):
        self.download_uri = download_uri
        self.encryption_key_base64 = encryption_key_base64

    @classmethod
    def build_from_local_project(
            cls,
            swan_orchestrator: 'Orchestrator',
            project_path: pathlib.Path,
            exclude_dirs: Optional[str] = PRIVATE_TASK_DEFAULT_DIRS_EXCLUDE,
    ) -> 'PrivateProject':
        project_tar_gz_stream = pack_project_to_stream(
            project_path=project_path,
            exclude_dirs=exclude_dirs,
        )
        encrypted_stream = encrypt_stream(input_stream=project_tar_gz_stream)
        # first 32 bytes is the encryption key
        encryption_key = encrypted_stream.read(32)
        encryption_key_in_b64 = base64.b64encode(encryption_key).decode("utf-8")

        download_uri = swan_orchestrator.upload_encrypted_project_stream(
            encrypted_stream=encrypted_stream
        )

        return cls(download_uri=download_uri, encryption_key_base64=encryption_key_in_b64)


    def serialize_to_json(self) -> str:
        return json.dumps({
            "download_uri": self.download_uri,
            "encryption_key_base64": self.encryption_key_base64,
        })

    @classmethod
    def load_from_json(cls, private_project_json_str: str) -> 'PrivateProject':
        private_project_dict = json.loads(private_project_json_str)
        download_uri = private_project_dict['download_uri']
        encryption_key_base64 = private_project_dict['encryption_key_base64']
        return cls(download_uri=download_uri, encryption_key_base64=encryption_key_base64)
