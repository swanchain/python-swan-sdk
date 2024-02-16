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

    def test_propose_task(self):
        task = self.swan_api.propose_task()

    def test_make_payment(self):
        payment = self.swan_api.make_payment()

    def test_get_payment_info(self):
        payment_info = self.swan_api.get_payment_info()

    def test_get_task_status(self):
        task_status = self.swan_api.get_task_status()

    def test_fetch_task_details(self):
        task_details = self.swan_api.fetch_task_details()
