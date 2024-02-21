""" Test Swan API """

import requests
from unittest.mock import Mock, MagicMock, patch

from swan.api.swan_api import SwanAPI


class TestSwanAPI:
    def setup_method(self):
        self.swan_api = SwanAPI()

    def test_query_price_list_successful(self):
        mock_response = {
            "hardware": [
                {"hardware_status": "available", "hardware_price": "10"},
                {"hardware_status": "occupied", "hardware_price": "20"},
                {"hardware_status": "available", "hardware_price": "30"},
            ]
        }
        self.swan_api._request_without_params = MagicMock(return_value=mock_response)
        result = self.swan_api.query_price_list()

        assert isinstance(result, list)
        assert "10" in result
        assert "30" in result

    def test_query_price_list_invalid_data(self):

        with patch.object(self.swan_api, "_request_without_params") as mock_request:

            mock_request.return_value = "invalid_data"
            result = self.swan_api.query_price_list()

            assert result is None

    def test_build_task(self):
        task = self.swan_api.build_task()

    def test_build_task_invalid_data(self):
        task = self.swan_api.build_task()

    def test_propose_task(self):
        task = self.swan_api.propose_task()

    def test_propose_task_invalid_data(self):
        task = self.swan_api.propose_task()

    def test_make_payment(self):
        payment = self.swan_api.make_payment()

    def test_make_payment_invalid_data(self):
        payment = self.swan_api.make_payment()

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
        self.swan_api._request_without_params = MagicMock(return_value=mock_response)

        result = self.swan_api.get_payment_info()

        assert isinstance(result, dict)
        assert "payments" in result
        assert "total" in result

    def test_get_payment_info_invalid_data(self):
        with patch.object(self.swan_api, "_request_without_params") as mock_request:
            mock_request.return_value = "invalid_data"

            result = self.swan_api.get_payment_info()

            assert result is None

    def test_get_task_status(self):
        mock_response = {
            "data": {
                "deploy_status": "Complete",
            }
        }
        self.swan_api._request_without_params = MagicMock(return_value=mock_response)

        result = self.swan_api.get_task_status()

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
        with patch.object(self.swan_api, "_request_without_params") as mock_request:
            mock_request.return_value = "invalid_data"

            result = self.swan_api.get_task_status()

            assert result is None

    def test_fetch_task_details(self):
        task_details = self.swan_api.fetch_task_details()

    def fetch_task_details_invalid_data(self):
        task_details = self.swan_api.fetch_task_details()
