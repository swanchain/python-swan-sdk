""" Test Swan API """

import requests
from mock.mock import Mock, MagicMock, patch

from swan.api.swan_api import SwanAPI


class TestSwanAPI:
    def setup_method(self):
        self.swan_api = SwanAPI()

    def test_query_price_list(self):
        price_list = self.swan_api.query_price_list()

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
