# test_task.py
import pytest
from swan.object import TaskDeploymentInfo


@pytest.fixture
def task_deployment_info_1(task_deployment_response_empty_1):
    task_deployment_info = TaskDeploymentInfo.load_from_result(task_deployment_response_empty_1)
    return task_deployment_info

@pytest.fixture
def task_deployment_info_2(task_deployment_response_empty_2):
    task_deployment_info = TaskDeploymentInfo.load_from_result(task_deployment_response_empty_2)
    return task_deployment_info

@pytest.fixture
def task_deployment_info_3(task_deployment_response_empty_3):
    task_deployment_info = TaskDeploymentInfo.load_from_result(task_deployment_response_empty_3)
    return task_deployment_info


def test_task_deployment_info_init_1(task_deployment_info_1):
    assert task_deployment_info_1.task.uuid == "aff0ef6c-8fec-4e01-b982-629f728bcede"
    assert task_deployment_info_1.task.status == "finished"
    assert task_deployment_info_1.task['status'] == "finished"
    assert task_deployment_info_1.task.task_detail.job_source_uri == "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a"
    assert task_deployment_info_1.task['task_detail'].job_source_uri == "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a"
    assert task_deployment_info_1.task['task_detail']['job_source_uri'] == "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a"
    assert isinstance(task_deployment_info_1.jobs, list)
    assert isinstance(task_deployment_info_1.computing_providers, list)
    assert task_deployment_info_1.status == "success"
    assert task_deployment_info_1.message == "fetch task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede' successfully"


def test_task_deployment_info_init_2(task_deployment_info_2):
    assert task_deployment_info_2.task.uuid == None
    assert task_deployment_info_2.task.status == None
    assert task_deployment_info_2.task.task_detail.job_source_uri == None
    assert isinstance(task_deployment_info_2.jobs, list)
    assert isinstance(task_deployment_info_2.computing_providers, list)
    assert task_deployment_info_2.status == "failed"
    assert task_deployment_info_2.message == "fetch task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede' failed"


def test_task_deployment_info_init_3(task_deployment_info_3):
    assert task_deployment_info_3.task.uuid == None
    assert task_deployment_info_3.task.status == None
    assert task_deployment_info_3.task.task_detail.job_source_uri == None
    assert isinstance(task_deployment_info_3.jobs, list)
    assert isinstance(task_deployment_info_3.computing_providers, list)
    assert task_deployment_info_3.status == "failed"
    assert task_deployment_info_3.message == "Error getting task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede'"

