# test_task.py
import pytest
from swan.object import TaskList
from swan.object.models import TaskInfo


@pytest.fixture
def task_list(task_list_response):
    task_list = TaskList.load_from_resp(task_list_response)
    return task_list

@pytest.fixture
def task_list_response(task_list_response):
    return task_list_response

def test_task_list(task_list):
    assert isinstance(task_list.task_list, list)
    assert isinstance(task_list.task_list[0], TaskInfo)
    assert task_list.status == "success"
    assert task_list.message == "fetch task list for user wallet:0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224 successfully"
    assert task_list.task_list[0].computing_providers[0].beneficiary == "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186"
    assert task_list.task_list[0].task.uuid == "f5e15f63-bee2-48f6-8dea-67cc4187979d"
    assert task_list.task_list[1].task.leading_job_id == "db39c612-891d-45b5-8c7f-908b5939227d"

def test_task_list_to_dict(task_list):
    task_list_dict = task_list.to_dict()
    assert task_list_dict['page'] == 1
    assert task_list_dict['size'] == 2
    assert task_list_dict['total'] == 40