""" Test Swan API """

import requests
import pytest
from unittest.mock import Mock, MagicMock, patch

from swan.api.orchestrator import Orchestrator
from swan.object.cp_config import HardwareConfig


class TestOrchestrator:
    
    def setup_method(self):
        orchestrator_url = "https://orchestrator.swanchain.io/"
        api_key = Mock()
        token = Mock()

        mock_response_contract = {
            'data': {
                'contract_info': {
                    'contract_detail': {
                        'client_contract_address': '0x9c5397F804f6663326151c81bBD82bb1451059E8', 
                        'payment_contract_address': '0xB48c5D1c025655BA79Ac4E10C0F19523dB97c816', 
                        'rpc_url': 'https://rpc-atom-internal.swanchain.io', 
                        'swan_token_contract_address': '0x91B25A65b295F0405552A4bbB77879ab5e38166c'
                        }, 
                    }
            },
            'message': 'Contract info retrieved successfully.', 
            'status': 'success'
        }
        self.patcher_contract = patch.object(Orchestrator, '_request_without_params')
        self.mock_get_contract_info = self.patcher_contract.start()
        self.mock_get_contract_info.return_value = mock_response_contract

        self.orchestrator = Orchestrator(orchestrator_url, api_key, token=token, verification=False)
        config = [
                    {
                        "hardware_status": "available",
                        "hardware_price": "10",
                        "region": "ON",
                        "hardware_type": "gpu",
                        "hardware_description": None,
                        "hardware_id": 0,
                        "hardware_name": "Test1"
                    }
                ]
        self.orchestrator.all_hardware = [HardwareConfig(hardware) for hardware in config]
        
        self.patcher_contract.stop()

    def tearDown(self):
        pass
    
    @patch("swan.api.orchestrator.Orchestrator._request_without_params")
    def test_get_hardware_config(self, mock_request_without_params):
        mock_request_without_params.return_value = {
            "data" : {
                "hardware": [
                    {
                        "hardware_status": "available",
                        "hardware_price": "10",
                        "region": "ON",
                        "hardware_type": "gpu",
                        "hardware_description": None,
                        "hardware_id": 0,
                        "hardware_name": "Test1"
                    }, 
                    {
                        "hardware_status": "available",
                        "hardware_price": "20",
                        "region": "ON",
                        "hardware_type": "cpu",
                        "hardware_description": None,
                        "hardware_id": 1,
                        "hardware_name": "Test2"
                    },
                    {
                        "hardware_status": "unavailable",
                        "hardware_price": "30",
                        "region": "ON",
                        "hardware_type": "gpu",
                        "hardware_description": None,
                        "hardware_id": 2,
                        "hardware_name": "Test3"
                    },
                ]
            }
            
        }

        response = self.orchestrator.get_hardware_config()

        assert len(self.orchestrator.all_hardware) == 3
        assert self.orchestrator.all_hardware[0].id == 0
        assert self.orchestrator.all_hardware[2].status == 'unavailable'
        assert [hardware for hardware in response if hardware['id'] == 1][0]['id'] == 1
        assert len(response) == 2
        assert response[0]["price"] == '10'
        assert response[1]["type"] == "cpu"


    @patch("swan.api.orchestrator.Orchestrator.estimate_payment")
    @patch("swan.api.orchestrator.Orchestrator._verify_hardware_region")
    @patch("swan.api.orchestrator.Orchestrator._request_with_params")
    @patch("swan.api.orchestrator.Orchestrator.make_payment")
    @patch("swan.api.orchestrator.Orchestrator.get_source_uri")
    def test_create_task_repo(
        self, 
        mock_estimate_payment, 
        mock__verify_hardware_region, 
        mock__request_with_params,
        mock_make_payment,
        mock_get_source_uri
    ):
        mock_estimate_payment.return_value = 0
        mock__verify_hardware_region.return_value = True
        mock__request_with_params.return_value = {
            "data": {
                "task": {
                    "comments": None,
                    "created_at": 1719606552,
                    "end_at": 1719610152,
                    "id": 1,
                    "leading_job_id": None,
                    "refund_amount": None,
                    "refund_wallet": "0x000000",
                    "source": "v2",
                    "start_at": 1719606552,
                    "start_in": 300,
                    "status": "initialized",
                    "task_detail": {
                        "amount": 1.0,
                        "bidder_limit": 3,
                        "created_at": 1719606552,
                        "duration": 3600,
                        "end_at": 1719610152,
                        "hardware": "C1ae.medium",
                        "job_source_uri": "https://job-source-uri",
                        "price_per_hour": "1.0"
                    },
                    "uuid": "00000000-cfaf-4a00-acd8-fe929414cd84",
                }
            },
            "message": "Task_uuid initialized.",
            "status": "success",
        }
        
        mock_make_payment.return_value = {
            "data": {
                "config_id": 2,
                "created_at": 1719606062,
                "duration": 3600,
                "ended_at": None,
                "error_code": None,
                "id": 2453,
                "order_type": "Creation",
                "refund_tx_hash": None,
                "region": "North Carolina-US",
                "space_id": None,
                "start_in": 300,
                "started_at": 1719606062,
                "status": "pending_payment_confirm",
                "task_uuid": "00000000-cfaf-4a00-acd8-fe929414cd84",
                "tx_hash": "0x0000000000000000000000000000000000000000000000000",
                "updated_at": 1719606070,
                "uuid": "d4f61285-655a-4f61-a4e0-e6160619c975"
            },
            "message": "Query order status success.",
            "status": "success",
            "tx_hash": "0x0000000000000000000000000000000000000000000000000",
        }
        
        mock_get_source_uri.return_value = "test_uri"

        result = self.orchestrator.create_task(
            wallet_address="dummy",
            repo_uri="dummy",
            private_key="dummy", # Wallet's private key
            hardware_id=0, # Optional: Defaults to 0 (free tier)
            region='global', # Optional: Defaults to global
            duration=3600, # Optional: Defaults to 3600 seconds
        )
        
        assert result['id'] == "00000000-cfaf-4a00-acd8-fe929414cd84"
        assert result['data']['task']['id'] == 1
        mock__request_with_params.assert_called_once()


    @patch("swan.api.orchestrator.Orchestrator._request_with_params")
    def test_renew_task(
        self, 
        mock_request_with_params
    ):
        mock_request_with_params.return_value = {
            "status": "success",
            "tx_hash": "1"
        }

        response = self.orchestrator.renew_task(
            task_uuid="123x", 
            duration=60, # Optional: Defaults to 3600 seconds (1 hour)
            tx_hash="1"
        )

        assert response['status'] == "success"
        assert response['tx_hash'] == "1"
        mock_request_with_params.assert_called_once()
