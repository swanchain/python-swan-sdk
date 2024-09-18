# test_task.py
import pytest
from swan.object import TaskCreationResult
from swan.object.models import dict_to_dataclass

@pytest.fixture
def task_creation_result_empty(task_creation_response_empty):
    task_creation_result_empty = TaskCreationResult.load_from_result(task_creation_response_empty)
    return task_creation_result_empty

def test_dict_to_dataclass():
    data_class_instance1 = dict_to_dataclass(TaskCreationResult, {})
    data_class_instance2 = dict_to_dataclass(TaskCreationResult, None)
    assert isinstance(data_class_instance1, TaskCreationResult)
    assert data_class_instance1.task_uuid == None
    assert isinstance(data_class_instance2, TaskCreationResult)
    assert data_class_instance2.task_uuid == None
    assert data_class_instance2.task.uuid == None
    assert data_class_instance2.config_order.uuid == None
    assert data_class_instance2['task']['uuid'] == None
    assert data_class_instance2['config_order']['uuid'] == None


def test_task_initialization(task_creation_result_empty):
    assert task_creation_result_empty.task_uuid == "be49dc4b-77f0-40c7-8828-2582d3e694af"
    assert task_creation_result_empty.tx_hash == None
    assert task_creation_result_empty.instance_type == 'C1ae.small'
    assert task_creation_result_empty.price == 0.0
    assert task_creation_result_empty.config_order['config_id'] == None
    assert task_creation_result_empty.task.status == None
    assert task_creation_result_empty.task.created_at == None
    assert task_creation_result_empty.task.start_at == None
    assert task_creation_result_empty.task.end_at == None
    assert task_creation_result_empty.job_source_uri == None
    assert task_creation_result_empty.wallet_address == None

def test_task_dict_access(task_creation_result_empty):
    assert task_creation_result_empty['task_uuid'] == "be49dc4b-77f0-40c7-8828-2582d3e694af"
    assert task_creation_result_empty.get('task_uuid') == "be49dc4b-77f0-40c7-8828-2582d3e694af"
    assert task_creation_result_empty['status'] == "failed"
    assert task_creation_result_empty.get('status') == "failed"
    assert task_creation_result_empty['task']['status'] == None
    assert task_creation_result_empty['message'] == "Task creation failed."