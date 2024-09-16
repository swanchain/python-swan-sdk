
# conftest.py
import pytest
from swan.object import Task

@pytest.fixture
def task_data():
    return {
        "data": {
            "task": {
                "comments": None,
                "created_at": 1726523566,
                "end_at": 1726527166,
                "id": 2457,
                "leading_job_id": None,
                "name": None,
                "refund_amount": None,
                "refund_wallet": "0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224",
                "source": "v2",
                "start_at": 1726523566,
                "start_in": 300,
                "status": "initialized",
                "task_detail": {
                    "amount": None,
                    "bidder_limit": 3,
                    "created_at": 1726523566,
                    "dcc_node_job_source_uri": None,
                    "dcc_selected_cp_list": None,
                    "duration": 3600,
                    "end_at": 1726527166,
                    "hardware": "C1ae.small",
                    "job_result_uri": None,
                    "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/4bfc73a7-d588-4dbe-bb6e-3a3ed80e1192",
                    "price_per_hour": "0.0",
                    "requirements": {
                        "hardware": "None",
                        "hardware_type": "CPU",
                        "memory": "2",
                        "preferred_cp_list": None,
                        "region": "global",
                        "storage": None,
                        "update_max_lag": None,
                        "vcpu": "2"
                    },
                    "space": {
                        "activeOrder": {
                            "config": {
                                "description": "CPU only · 2 vCPU · 2 GiB",
                                "hardware": "CPU only",
                                "hardware_id": 0,
                                "hardware_type": "CPU",
                                "memory": 2,
                                "name": "C1ae.small",
                                "price_per_hour": 0.0,
                                "vcpu": 2
                            }
                        },
                        "name": "0",
                        "uuid": "91c88e1c-45bb-479a-b12e-8ed78938040c"
                    },
                    "start_at": 1726523566,
                    "status": "paid",
                    "storage_source": "swanhub",
                    "type": "None",
                    "updated_at": 1726523566
                },
                "task_detail_cid": None,
                "tx_hash": None,
                "type": "None",
                "updated_at": 1726523566,
                "user_id": 4,
                "uuid": "be49dc4b-77f0-40c7-8828-2582d3e694af"
            }
        },
        "message": "Task_uuid initialized.",
        "status": "success",
        "config_order": {
            "config_id": 1,
            "created_at": 1726523566,
            "duration": 3600,
            "ended_at": None,
            "error_code": None,
            "id": 3219,
            "order_type": "Creation",
            "preferred_cp_list": None,
            "refund_tx_hash": None,
            "region": "global",
            "space_id": None,
            "start_in": 300,
            "started_at": 1726523566,
            "status": "pending_payment_confirm",
            "task_uuid": "be49dc4b-77f0-40c7-8828-2582d3e694af",
            "tx_hash": "0xee1c57d967422935e279b470949c15f1997af7d355b4063c7c9b32f33834dc40",
            "updated_at": 1726523577,
            "uuid": "39dc2dc5-a22c-4b60-9783-c00924357564"
        },
        "tx_hash": "0xee1c57d967422935e279b470949c15f1997af7d355b4063c7c9b32f33834dc40",
        "id": "be49dc4b-77f0-40c7-8828-2582d3e694af",
        "task_uuid": "be49dc4b-77f0-40c7-8828-2582d3e694af",
        "instance_type": "C1ae.small",
        "price": 0.0
    }

@pytest.fixture
def task(task_data):
    task = Task(task_data)
    return task
