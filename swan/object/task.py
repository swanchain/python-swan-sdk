import base64
import json
import logging
import time
from http import HTTPStatus
from typing import Optional, Dict, Any
from urllib.parse import urljoin

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class UnexpectedTemporaryNodeStatus(Exception):
    pass


def encrypt_symmetric_key_with_rsa(symmetric_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_symmetric_key


class Task:
    def __init__(self, task_uuid: str, orchestrator: "Orchestrator", payment_tx_hash: Optional[str] = None):
        self.task_uuid = task_uuid
        self.orchestrator = orchestrator
        self.payment_tx_hash = payment_tx_hash


class PrivateTask(Task):

    def __init__(
            self,
            task_uuid: str,
            orchestrator: "Orchestrator",
            encryption_key_base64: str,
            payment_tx_hash: Optional[str] = None
    ):
        super().__init__(task_uuid, orchestrator, payment_tx_hash)
        self.temporary_node_uri: Optional[str] = None
        self.encryption_key_base64 = encryption_key_base64
        self.encryption_key: Optional[bytes] = base64.b64decode(encryption_key_base64)

    def _is_remote_temporary_node_ready(self) -> bool:
        try:
            if not self.temporary_node_uri:
                resp_dict = self.orchestrator.get_private_task_temporary_node_uri(
                    task_uuid=self.task_uuid
                )
                self.temporary_node_uri = resp_dict["data"]["temporary_node_uri"]

            temporary_node_status_uri = urljoin(self.temporary_node_uri, "system_status")
            status_resp = requests.get(url=temporary_node_status_uri)
            if status_resp.status_code != HTTPStatus.OK:
                logging.info(f"Waiting for the temporary node {self.temporary_node_uri} to be deployed...")
                return False
            system_status = status_resp.json()
            logging.info(f"Waiting for the temporary node {self.temporary_node_uri} to be initialized...")
            if system_status["data"]["status"] == "INITIALIZED":
                return True
            elif system_status["data"]["status"] == "CREATED":
                return False
            else:
                raise UnexpectedTemporaryNodeStatus(f"Unexpected temporary node status: {system_status}")
        except UnexpectedTemporaryNodeStatus as e:
            raise e
        except Exception as e:
            logging.exception(e)
            logging.info(f"Waiting for the temporary node to be created...")
            return False

    def get_temporary_node_public_key(self) -> rsa.RSAPublicKey:
        public_key_uri = urljoin(self.temporary_node_uri, "public_key")
        public_key_resp = requests.get(url=public_key_uri, timeout=10)
        public_key_resp.raise_for_status()
        public_key_str = public_key_resp.json()["public_key"]

        # Convert the PEM string to bytes
        pem_data = public_key_str.encode('utf-8')

        # Load the public key
        public_key = serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )

        # Ensure it's an RSA public key
        if isinstance(public_key, rsa.RSAPublicKey):
            return public_key
        else:
            raise ValueError("The provided key is not an RSA public key")

    def serialize_to_json(self) -> str:
        data: Dict[str, Any] = {
            "task_uuid": self.task_uuid,
            "encryption_key": self.encryption_key_base64
        }
        return json.dumps(data)

    @classmethod
    def load_from_json(cls, json_str: str, orchestrator: "Orchestrator") -> "PrivateTask":
        data = json.loads(json_str)
        task = cls(
            task_uuid=data["task_uuid"],
            orchestrator=orchestrator,
            encryption_key_base64=data["encryption_key"],
        )
        return task

    def deploy_task(self, interval: int = 5, retries: int = 30) -> dict:
        for _ in range(retries):
            if not self._is_remote_temporary_node_ready():
                time.sleep(interval)
            else:
                break
        else:
            raise Exception("Task failed to deploy, you could try again")

        temporary_node_public_key = self.get_temporary_node_public_key()
        encrypted_symmetric_key = encrypt_symmetric_key_with_rsa(self.encryption_key, temporary_node_public_key)

        logging.info(f"Sending data decryption key to temporary node {self.temporary_node_uri}...")
        deploy_uri = urljoin(self.temporary_node_uri, "deploy")
        resp = requests.post(deploy_uri, json={
            "data_decryption_key": base64.b64encode(encrypted_symmetric_key).decode("utf-8"),
        })
        return resp.json()
