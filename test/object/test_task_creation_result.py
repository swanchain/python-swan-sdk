# test_task.py
import pytest
from swan.object import TaskCreationResult


@pytest.fixture
def task_creation_result(task_creation_response):
    task_creation_result = TaskCreationResult.load_from_resp(task_creation_response)
    return task_creation_result


def test_task_initialization(task_creation_result):
    assert task_creation_result.task_uuid == "be49dc4b-77f0-40c7-8828-2582d3e694af"
    assert task_creation_result.tx_hash == "0xee1c57d967422935e279b470949c15f1997af7d355b4063c7c9b32f33834dc40"
    assert task_creation_result.instance_type == "C1ae.small"
    assert task_creation_result.price == 0.0
    assert task_creation_result.config_order['config_id'] == 1
    assert task_creation_result.task.created_at == 1726523566
    assert task_creation_result.task.start_at == 1726523566
    assert task_creation_result.task.end_at == 1726527166
    assert task_creation_result.job_source_uri == "https://swanhub-cali.swanchain.io/spaces/4bfc73a7-d588-4dbe-bb6e-3a3ed80e1192"
    assert task_creation_result.wallet_address == "0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224"
    assert task_creation_result.status == "success"
    assert task_creation_result.message == "Task_uuid initialized."

def test_task_dict_access(task_creation_result):
    assert task_creation_result['task_uuid'] == "be49dc4b-77f0-40c7-8828-2582d3e694af"
    assert task_creation_result.get('task_uuid') == "be49dc4b-77f0-40c7-8828-2582d3e694af"
    assert task_creation_result['task']['status'] == "initialized"
    assert task_creation_result['status'] == "success"
    assert task_creation_result.get('status') == "success"