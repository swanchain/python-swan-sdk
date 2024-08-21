import logging
import os
import time
from http import HTTPStatus
from typing import Optional
from urllib.parse import urljoin

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa



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
            encryption_key: bytes,
            payment_tx_hash: Optional[str] = None
    ):
        super().__init__(task_uuid, orchestrator, payment_tx_hash)
        self.symmetric_key = os.urandom(32)
        self.temporary_node_uri: Optional[str] = None
        self.encryption_key = encryption_key

    def _is_remote_temporary_node_ready(self) -> bool:
        try:
            if not self.temporary_node_uri:
                self.temporary_node_uri = self.orchestrator.get_private_task_temporary_node_uri(
                    task_uuid=self.task_uuid
                )

            if requests.get(url=self.temporary_node_uri).status_code == HTTPStatus.OK:
                return True
            else:
                return False
        except Exception as e:
            logging.exception(e)
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

    def deploy_task(self, retries: int = 30) -> Task:
        for _ in range(retries):
            if not self._is_remote_temporary_node_ready():
                time.sleep(10)
            else:
                break
        else:
            raise Exception("Task failed to deploy, you could try again")
