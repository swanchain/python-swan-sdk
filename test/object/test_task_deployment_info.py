# test_task.py
import pytest
from swan.object import TaskDeploymentInfo


@pytest.fixture
def task_deployment_info(task_deployment_response):
    task_deployment_info = TaskDeploymentInfo.load_from_resp(task_deployment_response)
    return task_deployment_info


def test_task_deployment_info_init(task_deployment_info):
    assert task_deployment_info.task.uuid == "aff0ef6c-8fec-4e01-b982-629f728bcede"
    assert task_deployment_info.task.status == "finished"
    assert task_deployment_info.task.task_detail.job_source_uri == "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a"
    assert task_deployment_info.jobs[0].status == "Ended"
    assert task_deployment_info.jobs[1].hardware == "C1ae.small"
    assert task_deployment_info.computing_providers[0].cp_account_address == "0xE974b17d9D730CAe75a228Df7eCa452e31E06276"
    assert task_deployment_info.config_orders[0].config_id == 1
    assert task_deployment_info.message == "fetch task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede' successfully"
    assert task_deployment_info.status == "success"


def test_task_dict_access(task_deployment_info):
    assert task_deployment_info.task['uuid'] == "aff0ef6c-8fec-4e01-b982-629f728bcede"
    assert task_deployment_info.task['status'] == "finished"
    assert task_deployment_info.task['task_detail'].job_source_uri == "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a"
    assert task_deployment_info.jobs[0]['status'] == "Ended"
    assert task_deployment_info.jobs[1]['hardware'] == "C1ae.small"
    assert task_deployment_info.computing_providers[0]['cp_account_address'] == "0xE974b17d9D730CAe75a228Df7eCa452e31E06276"
