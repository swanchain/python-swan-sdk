""" Test Swan API """

import requests
from unittest.mock import Mock, MagicMock, patch

from swan.api.orchestrator import Orchestrator


class TestSwanAPI:
    def setup_method(self):
        orchestrator_url = "https://orchestrator.swanchain.io/"
        api_key = Mock()
        payment_key = Mock()
        self.orchestrator = Orchestrator(orchestrator_url, api_key, payment_key)

    def test_query_price_list_successful(self):
        mock_response = {
            "hardware": [
                {"hardware_status": "available", "hardware_price": "10"},
                {"hardware_status": "occupied", "hardware_price": "20"},
                {"hardware_status": "available", "hardware_price": "30"},
            ]
        }
        self.orchestrator._request_without_params = MagicMock(return_value=mock_response)
        result = self.orchestrator.query_price_list()

        assert isinstance(result, list)
        assert "10" in result
        assert "30" in result

    def test_query_price_list_invalid_data(self):

        with patch.object(self.orchestrator, "_request_without_params") as mock_request:

            mock_request.return_value = "invalid_data"
            result = self.orchestrator.query_price_list()

            assert result is None

    @patch("swan.api.orchestrator.list_repo_contents")
    @patch("swan.api.orchestrator.upload_file")
    @patch("swan.api.orchestrator.os")
    @patch("swan.api.orchestrator.uuid")
    def test_prepare_task(
        self, mock_uuid, mock_os, mock_upload_file, mock_list_repo_contents
    ):
        # Arrange
        mock_os.getenv.return_value = "/tmp"
        mock_uuid.uuid4.return_value = "random_uuid"
        mock_list_repo_contents.return_value = {
            ".env": "env_content",
            "Dockerfile": "dockerfile_content",
            "kubernetes.yaml": "kubernetes_content",
        }
        mock_upload_file.return_value = "mcs_file"

        # Act
        result = self.orchestrator.prepare_task("source_code_url")

        # Assert
        mock_list_repo_contents.assert_called_once_with("source_code_url")
        mock_upload_file.assert_called()
        assert self.orchestrator.task["random_uuid"] == "random_uuid"
        assert self.orchestrator.task["job_source_uri"] == "/tmp/spaces/random_uuid"
        assert result is None

    @patch("swan.api.orchestrator.list_repo_contents")
    @patch("swan.api.orchestrator.upload_file")
    @patch("swan.api.orchestrator.os")
    @patch("swan.api.orchestrator.uuid")
    def test_prepare_task_error(
        self, mock_uuid, mock_os, mock_upload_file, mock_list_repo_contents
    ):

        mock_os.getenv.return_value = "/tmp"
        mock_uuid.uuid4.return_value = "random_uuid"
        mock_list_repo_contents.side_effect = Exception("Error")

        result = self.orchestrator.prepare_task("source_code_url")

        assert result is None

    @patch("swan.api.orchestrator.SwanAPI._request_without_params")
    @patch("swan.api.orchestrator.SwanAPI._request_with_params")
    def test_propose_task(self, mock_request_with_params, mock_request_without_params):

        mock_request_without_params.return_value = {
            "data": {
                "hardware": [
                    {"hardware_name": "config_name", "region": ["region1", "region2"]}
                ]
            }
        }
        mock_request_with_params.return_value = "result"
        self.orchestrator.task = {
            "config_name": "config_name",
            "duration": 10,
            "paid_amount": 100,
            "tx_hash": "tx_hash",
            "job_source_uri": "job_source_uri",
        }

        result = self.orchestrator.propose_task("start_in", "region1")

        mock_request_without_params.assert_called_once()
        mock_request_with_params.assert_called_once()
        assert result == "result"

    @patch("swan.api.orchestrator.SwanAPI._request_without_params")
    @patch("swan.api.orchestrator.SwanAPI._request_with_params")
    def test_propose_task_invalid_region(
        self, mock_request_with_params, mock_request_without_params
    ):

        mock_request_without_params.return_value = {
            "data": {
                "hardware": [
                    {"hardware_name": "config_name", "region": ["region1", "region2"]}
                ]
            }
        }
        self.orchestrator.task = {
            "config_name": "config_name",
            "duration": 10,
            "paid_amount": 100,
            "tx_hash": "tx_hash",
            "job_source_uri": "job_source_uri",
        }

        result = self.orchestrator.propose_task("start_in", "invalid_region")

        mock_request_without_params.assert_called_once()
        mock_request_with_params.assert_not_called()
        assert result is None

    def test_make_payment(self):
        payment = self.orchestrator.make_payment()

    def test_make_payment_invalid_data(self):
        payment = self.orchestrator.make_payment()

    def test_get_payment_info_successful(self):
        mock_response = {
            "payments": [
                {
                    "id": 1,
                    "uuid": "123",
                    "job_id": 1,
                    "order_id": 1,
                    "provider_id": 1,
                    "provider_owner_address": "address",
                    "amount": "10.00000",
                    "token": "token",
                    "status": "created",
                    "claimed": False,
                    "transaction_hash": "hash",
                    "created_at": "time",
                    "updated_at": "time",
                    "deleted_at": "time",
                }
            ],
            "total": 1,
        }
        self.orchestrator._request_without_params = MagicMock(return_value=mock_response)

        result = self.orchestrator.get_payment_info()

        assert isinstance(result, dict)
        assert "payments" in result
        assert "total" in result

    def test_get_payment_info_invalid_data(self):
        with patch.object(self.orchestrator, "_request_without_params") as mock_request:
            mock_request.return_value = "invalid_data"

            result = self.orchestrator.get_payment_info()

            assert result is None

    def test_get_task_status(self):
        mock_response = {
            "data": {
                "deploy_status": "Complete",
            }
        }
        self.orchestrator._request_without_params = MagicMock(return_value=mock_response)

        result = self.orchestrator.get_task_status()

        valid_statuses = [
            "paid",
            "Cancel failed",
            "Cancelled",
            "Submitted",
            "Complete",
            "deployToK8s",
            "Failed",
            "uploadResult",
            "buildImage",
            "downloadSource",
            "Running",
        ]

        assert result in valid_statuses

    def test_get_task_status_invalid_data(self):
        with patch.object(self.orchestrator, "_request_without_params") as mock_request:
            mock_request.return_value = "invalid_data"

            result = self.orchestrator.get_task_status()

            assert result is None

    def test_fetch_task_details(self):
        task_details = self.orchestrator.fetch_task_details()

    def fetch_task_details_invalid_data(self):
        task_details = self.orchestrator.fetch_task_details()
