
# conftest.py
import pytest
from swan.object import TaskCreationResult

@pytest.fixture
def task_creation_response():
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
def task_creation_response_empty():
    return {
        "data": None,
        "message": "Task creation failed.",
        "status": "failed",
        "tx_hash": None,
        "id": "be49dc4b-77f0-40c7-8828-2582d3e694af",
        "task_uuid": "be49dc4b-77f0-40c7-8828-2582d3e694af",
        "instance_type": "C1ae.small",
        "price": 0.0
    }


@pytest.fixture
def task_deployment_response():
    return {
        "data": {
            "computing_providers": [
                {
                    "beneficiary": "0xC2522AE0392c6AFc61C7f3B2e4dF3c5E8A69a794",
                    "cp_account_address": "0xE974b17d9D730CAe75a228Df7eCa452e31E06276",
                    "created_at": 1723741012,
                    "freeze_online": None,
                    "id": 111,
                    "lat": 45.5075,
                    "lon": -73.5887,
                    "multi_address": [
                        "/ip4/38.80.81.161/tcp/8085"
                    ],
                    "name": "swancp.pvm.nebulablock.com",
                    "node_id": "04da2df41b0bc7804c6fe92205ee00a919412b74cf63647a340baee75e3b89c3ca1cf0b80163c18e36be57885aa7b6af011c813e8ec4b4559a4732293119e6b670",
                    "online": 0,
                    "owner_address": "0xC2522AE0392c6AFc61C7f3B2e4dF3c5E8A69a794",
                    "region": "Quebec-CA",
                    "task_types": "[1, 2, 3, 4]",
                    "updated_at": 1726604646,
                    "version": "2.0",
                    "worker_address": "0xC2522AE0392c6AFc61C7f3B2e4dF3c5E8A69a794"
                },
                {
                    "beneficiary": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186",
                    "cp_account_address": "0x1734A9f10367B34985Ef87d73bA6101E3C619E84",
                    "created_at": 1725249052,
                    "freeze_online": None,
                    "id": 113,
                    "lat": 45.5075,
                    "lon": -73.5887,
                    "multi_address": [
                        "/ip4/38.140.46.60/tcp/8086/"
                    ],
                    "name": "test-dd",
                    "node_id": "04211ef2396c6fa4ef2142e4b38b1979144c825b279c28f67e11dbbd41cd2a7d18055953ff423af7263ec03f5624384f04cf0959a399d1f608691cb0e0c07545bb",
                    "online": 0,
                    "owner_address": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186",
                    "region": "Quebec-CA",
                    "task_types": "[3]",
                    "updated_at": 1726604647,
                    "version": "2.0",
                    "worker_address": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186"
                },
                {
                    "beneficiary": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94",
                    "cp_account_address": "0x2bd6a6f41b37152677F8b4946490580F63494abD",
                    "created_at": 1722488518,
                    "freeze_online": 1,
                    "id": 99,
                    "lat": 35.8639,
                    "lon": -78.535,
                    "multi_address": [
                        "/ip4/40.143.96.125/tcp/10011"
                    ],
                    "name": "new-cp-001",
                    "node_id": "04d5b210591aa5aff5b4e49ad6a3ec57b72aefcdc99cd7888fff80b5991452d8a8dce099312cfb7e78637e04e9824a7274160e49176a00394745701ed450a113e2",
                    "online": 1,
                    "owner_address": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94",
                    "region": "North Carolina-US",
                    "task_types": "[1, 2, 3, 4]",
                    "updated_at": 1726604586,
                    "version": "2.0",
                    "worker_address": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94"
                }
            ],
            "config_orders": [
                {
                    "config_id": 1,
                    "created_at": 1725522770,
                    "duration": 7200,
                    "ended_at": None,
                    "error_code": None,
                    "id": 649,
                    "order_type": "Creation",
                    "preferred_cp_list": None,
                    "refund_tx_hash": None,
                    "region": "global",
                    "space_id": None,
                    "start_in": 300,
                    "started_at": 1725522770,
                    "status": "payment_consumed",
                    "task_uuid": "aff0ef6c-8fec-4e01-b982-629f728bcede",
                    "tx_hash": "0x0454c0fdb27f8ed1f686146bdb7dce3f5e31a0d16c8f500590dc7493e10ff980",
                    "updated_at": 1725522787,
                    "uuid": "480253ec-3850-44e7-8019-b1479c6534d0"
                }
            ],
            "jobs": [
                {
                    "build_log": "wss://log.pvm.nebulablock.com:8085/api/v1/computing/lagrange/spaces/log?job_uuid=130efdf3-12d1-467c-a4b7-5bd1ef7ba95f&type=build",
                    "comments": "Ended(deployToK8s). deployToK8s: updated job_result_uri. deployToK8s(Submitted).",
                    "container_log": "wss://log.pvm.nebulablock.com:8085/api/v1/computing/lagrange/spaces/log?job_uuid=130efdf3-12d1-467c-a4b7-5bd1ef7ba95f&type=container&order=private",
                    "cp_account_address": "0xE974b17d9D730CAe75a228Df7eCa452e31E06276",
                    "created_at": 1725522791,
                    "duration": 7200,
                    "ended_at": 1725529992,
                    "hardware": "C1ae.small",
                    "id": 882,
                    "job_real_uri": "ssh root@38.80.81.161 -p30001",
                    "job_result_uri": "https://286cb2c989.acl.swanipfs.com/ipfs/QmW32zeickDp8CfpohedKuDshYdk6zKDuJCzDjy33VwiCX",
                    "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a",
                    "name": "Job-130efdf3-12d1-467c-a4b7-5bd1ef7ba95f",
                    "node_id": "04da2df41b0bc7804c6fe92205ee00a919412b74cf63647a340baee75e3b89c3ca1cf0b80163c18e36be57885aa7b6af011c813e8ec4b4559a4732293119e6b670",
                    "start_at": 1725522792,
                    "status": "Ended",
                    "storage_source": "swanhub",
                    "task_uuid": "aff0ef6c-8fec-4e01-b982-629f728bcede",
                    "type": None,
                    "updated_at": 1725530007,
                    "uuid": "130efdf3-12d1-467c-a4b7-5bd1ef7ba95f"
                },
                {
                    "build_log": "wss://log.dev2.crosschain.computer:8086/api/v1/computing/lagrange/spaces/log?job_uuid=2f91ef67-2aa8-4f06-be43-f08434d29da8&type=build",
                    "comments": "Ended(deployToK8s). deployToK8s: no job_result_uri from api. deployToK8s(Submitted).",
                    "container_log": "wss://log.dev2.crosschain.computer:8086/api/v1/computing/lagrange/spaces/log?job_uuid=2f91ef67-2aa8-4f06-be43-f08434d29da8&type=container",
                    "cp_account_address": "0x1734A9f10367B34985Ef87d73bA6101E3C619E84",
                    "created_at": 1725522792,
                    "duration": 7200,
                    "ended_at": 1725529992,
                    "hardware": "C1ae.small",
                    "id": 883,
                    "job_real_uri": "https://lol7vgmp60.dev2.crosschain.computer",
                    "job_result_uri": None,
                    "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a",
                    "name": "Job-2f91ef67-2aa8-4f06-be43-f08434d29da8",
                    "node_id": "04211ef2396c6fa4ef2142e4b38b1979144c825b279c28f67e11dbbd41cd2a7d18055953ff423af7263ec03f5624384f04cf0959a399d1f608691cb0e0c07545bb",
                    "start_at": 1725522792,
                    "status": "Ended",
                    "storage_source": "swanhub",
                    "task_uuid": "aff0ef6c-8fec-4e01-b982-629f728bcede",
                    "type": None,
                    "updated_at": 1725530007,
                    "uuid": "2f91ef67-2aa8-4f06-be43-f08434d29da8"
                },
                {
                    "build_log": "wss://log.cp.filezoo.com.cn:10011/api/v1/computing/lagrange/spaces/log?job_uuid=da7553f6-f72e-498d-9b2a-beca4dc5a1f5&type=build",
                    "comments": "Ended(deployToK8s). deployToK8s: updated job_result_uri. deployToK8s(pullImage). pullImage: no job_result_uri from api. pullImage(Submitted).",
                    "container_log": "wss://log.cp.filezoo.com.cn:10011/api/v1/computing/lagrange/spaces/log?job_uuid=da7553f6-f72e-498d-9b2a-beca4dc5a1f5&type=container&order=private",
                    "cp_account_address": "0x2bd6a6f41b37152677F8b4946490580F63494abD",
                    "created_at": 1725522792,
                    "duration": 7200,
                    "ended_at": 1725529992,
                    "hardware": "C1ae.small",
                    "id": 884,
                    "job_real_uri": "ssh root@40.143.96.125 -p30002",
                    "job_result_uri": "https://42f6d9f62851.acl.swanipfs.com/ipfs/QmXbvJ31cairZ8SbfDew6LMne3cmx4ZrUZNLn4YZRQvL1C",
                    "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a",
                    "name": "Job-da7553f6-f72e-498d-9b2a-beca4dc5a1f5",
                    "node_id": "04d5b210591aa5aff5b4e49ad6a3ec57b72aefcdc99cd7888fff80b5991452d8a8dce099312cfb7e78637e04e9824a7274160e49176a00394745701ed450a113e2",
                    "start_at": 1725522792,
                    "status": "Ended",
                    "storage_source": "swanhub",
                    "task_uuid": "aff0ef6c-8fec-4e01-b982-629f728bcede",
                    "type": None,
                    "updated_at": 1725530007,
                    "uuid": "da7553f6-f72e-498d-9b2a-beca4dc5a1f5"
                }
            ],
            "task": {
                "comments": "finish_pending(completed).",
                "created_at": 1725522770,
                "end_at": 1725529970,
                "id": 629,
                "leading_job_id": "130efdf3-12d1-467c-a4b7-5bd1ef7ba95f",
                "name": None,
                "refund_amount": None,
                "refund_wallet": "0xFbc1d38a2127D81BFe3EA347bec7310a1cfa2373",
                "source": "v2",
                "start_at": 1725522770,
                "start_in": 300,
                "status": "finished",
                "task_detail": {
                    "amount": 0.0,
                    "bidder_limit": 3,
                    "created_at": 1725522770,
                    "dcc_node_job_source_uri": None,
                    "dcc_selected_cp_list": None,
                    "duration": 7200,
                    "end_at": 1725529970,
                    "hardware": "C1ae.small",
                    "job_result_uri": None,
                    "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a",
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
                        "uuid": "4449d5db-2e75-4b06-9921-529438b15d62"
                    },
                    "start_at": 1725522770,
                    "status": "paid",
                    "storage_source": "swanhub",
                    "type": "None",
                    "updated_at": 1725522770
                },
                "task_detail_cid": "https://plutotest.acl.swanipfs.com/ipfs/QmbKWXkCmHXffXM55oHcTmDBHruwGnmWRGZH6xw23gMxU9",
                "tx_hash": None,
                "type": "None",
                "updated_at": 1725619030,
                "user_id": 6,
                "uuid": "aff0ef6c-8fec-4e01-b982-629f728bcede"
            }
        },
        "message": "fetch task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede' successfully",
        "status": "success"
    }


@pytest.fixture
def task_deployment_response_empty_1():
    return {
        "data": {
            "computing_providers": [
            ],
            "config_orders": [
            ],
            "jobs": [
            ],
            "task": {
                "comments": "finish_pending(completed).",
                "created_at": 1725522770,
                "end_at": 1725529970,
                "id": 629,
                "leading_job_id": None,
                "name": None,
                "refund_amount": None,
                "refund_wallet": "0xFbc1d38a2127D81BFe3EA347bec7310a1cfa2373",
                "source": "v2",
                "start_at": 1725522770,
                "start_in": 300,
                "status": "finished",
                "task_detail": {
                    "amount": 0.0,
                    "bidder_limit": 3,
                    "created_at": 1725522770,
                    "dcc_node_job_source_uri": None,
                    "dcc_selected_cp_list": None,
                    "duration": 7200,
                    "end_at": 1725529970,
                    "hardware": "C1ae.small",
                    "job_result_uri": None,
                    "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/086a36b1-b06e-49fb-85fe-095d83d8ac6a",
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
                        "uuid": "4449d5db-2e75-4b06-9921-529438b15d62"
                    },
                    "start_at": 1725522770,
                    "status": "paid",
                    "storage_source": "swanhub",
                    "type": "None",
                    "updated_at": 1725522770
                },
                "task_detail_cid": "https://plutotest.acl.swanipfs.com/ipfs/QmbKWXkCmHXffXM55oHcTmDBHruwGnmWRGZH6xw23gMxU9",
                "tx_hash": None,
                "type": "None",
                "updated_at": 1725619030,
                "user_id": 6,
                "uuid": "aff0ef6c-8fec-4e01-b982-629f728bcede"
            }
        },
        "message": "fetch task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede' successfully",
        "status": "success"
    }


@pytest.fixture
def task_deployment_response_empty_2():
    return {
        "data": None,
        "message": "fetch task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede' failed",
        "status": "failed"
    }

@pytest.fixture
def task_deployment_response_empty_3():
    return {
        "data": {
            "computing_providers": [
            ],
            "config_orders": [
            ],
            "jobs": [
            ],
            "task": None
        },
        "message": "Error getting task info for task_uuid='aff0ef6c-8fec-4e01-b982-629f728bcede'",
        "status": "failed"
    }


@pytest.fixture
def task_list_response():
    return {
        "data": {
            "list": [
                {
                    "computing_providers": [
                        {
                            "beneficiary": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186",
                            "cp_account_address": "0x6f43E3e5B70aa5BF5818c56D509BDd092D0907E0",
                            "created_at": 1722488655,
                            "freeze_online": 1,
                            "id": 100,
                            "lat": 45.5075,
                            "lon": -73.5887,
                            "multi_address": [
                                "/ip4/38.140.46.60/tcp/8086"
                            ],
                            "name": "test-dd",
                            "node_id": "04241e19381a8fad4cc98ef6de0a7e417e6d662ff49d8096cff9ec4b08798eeb96687ff5c7b4bde1adb8ccdbb579f16ac0f2c4e0853406282a37285582879dde49",
                            "online": 0,
                            "owner_address": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186",
                            "region": "Quebec-CA",
                            "task_types": "[1, 2, 3, 4]",
                            "updated_at": 1727290151,
                            "version": "2.0",
                            "worker_address": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186"
                        },
                        {
                            "beneficiary": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94",
                            "cp_account_address": "0x2bd6a6f41b37152677F8b4946490580F63494abD",
                            "created_at": 1722488518,
                            "freeze_online": 1,
                            "id": 99,
                            "lat": 35.8639,
                            "lon": -78.535,
                            "multi_address": [
                                "/ip4/40.143.96.125/tcp/10011"
                            ],
                            "name": "new-cp-001",
                            "node_id": "04d5b210591aa5aff5b4e49ad6a3ec57b72aefcdc99cd7888fff80b5991452d8a8dce099312cfb7e78637e04e9824a7274160e49176a00394745701ed450a113e2",
                            "online": 1,
                            "owner_address": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94",
                            "region": "North Carolina-US",
                            "task_types": "[1, 2, 3, 4, 5]",
                            "updated_at": 1727290151,
                            "version": "2.0",
                            "worker_address": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94"
                        }
                    ],
                    "config_orders": [
                        {
                            "config_id": 2,
                            "created_at": 1724879753,
                            "duration": 3600,
                            "ended_at": None,
                            "error_code": None,
                            "id": 486,
                            "order_type": "Renewal",
                            "preferred_cp_list": None,
                            "refund_tx_hash": None,
                            "region": "global",
                            "space_id": None,
                            "start_in": 300,
                            "started_at": 1724879804,
                            "status": "payment_consumed",
                            "task_uuid": "f5e15f63-bee2-48f6-8dea-67cc4187979d",
                            "tx_hash": "0x0d2995fa837c95d2ab9ea9a22b23f610540df704c2c20f69a168a96a75a92297",
                            "updated_at": 1724879809,
                            "uuid": "ff4e6145-5739-4c0d-b6fd-c2dfed41ee0c"
                        },
                        {
                            "config_id": 2,
                            "created_at": 1724879753,
                            "duration": 3600,
                            "ended_at": None,
                            "error_code": None,
                            "id": 485,
                            "order_type": "Creation",
                            "preferred_cp_list": None,
                            "refund_tx_hash": None,
                            "region": "global",
                            "space_id": None,
                            "start_in": 300,
                            "started_at": 1724879753,
                            "status": "payment_consumed",
                            "task_uuid": "f5e15f63-bee2-48f6-8dea-67cc4187979d",
                            "tx_hash": "0x8358bf0f704730faa205131fa0f1a89238c7f678991ca69f51cebfc82c005e17",
                            "updated_at": 1724879765,
                            "uuid": "19961a1b-fdf8-49a6-ac1b-a852edbd7e84"
                        }
                    ],
                    "jobs": [
                        {
                            "build_log": "wss://log.dev2.crosschain.computer:8086/api/v1/computing/lagrange/spaces/log?space_id=b43a3c03-043f-4999-94dc-9620b4ef58ab&type=build",
                            "comments": "Complete(Running). Running(Submitted).",
                            "container_log": "wss://log.dev2.crosschain.computer:8086/api/v1/computing/lagrange/spaces/log?space_id=b43a3c03-043f-4999-94dc-9620b4ef58ab&type=container",
                            "cp_account_address": "0x6f43E3e5B70aa5BF5818c56D509BDd092D0907E0",
                            "created_at": 1724879765,
                            "duration": 7200,
                            "ended_at": 1724886969,
                            "hardware": "C1ae.medium",
                            "id": 627,
                            "job_real_uri": "https://4p597psevy.dev2.crosschain.computer",
                            "job_result_uri": None,
                            "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/b43a3c03-043f-4999-94dc-9620b4ef58ab",
                            "name": "Job-b014b641-97a2-4417-a484-c6e72f9ad8f6",
                            "node_id": "04241e19381a8fad4cc98ef6de0a7e417e6d662ff49d8096cff9ec4b08798eeb96687ff5c7b4bde1adb8ccdbb579f16ac0f2c4e0853406282a37285582879dde49",
                            "start_at": 1724879769,
                            "status": "Complete",
                            "storage_source": "swanhub",
                            "task_uuid": "f5e15f63-bee2-48f6-8dea-67cc4187979d",
                            "type": None,
                            "updated_at": 1724887024,
                            "uuid": "b014b641-97a2-4417-a484-c6e72f9ad8f6"
                        },
                        {
                            "build_log": "wss://log.cp.filezoo.com.cn:10011/api/v1/computing/lagrange/spaces/log?job_uuid=b4f912de-561a-4af8-948e-61281c20ea82&type=build",
                            "comments": "Complete(Running). Running(Submitted).",
                            "container_log": "wss://log.cp.filezoo.com.cn:10011/api/v1/computing/lagrange/spaces/log?job_uuid=b4f912de-561a-4af8-948e-61281c20ea82&type=container",
                            "cp_account_address": "0x2bd6a6f41b37152677F8b4946490580F63494abD",
                            "created_at": 1724879769,
                            "duration": 7200,
                            "ended_at": 1724886973,
                            "hardware": "C1ae.medium",
                            "id": 628,
                            "job_real_uri": "https://1a2d7syje6.cp.filezoo.com.cn",
                            "job_result_uri": None,
                            "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/b43a3c03-043f-4999-94dc-9620b4ef58ab",
                            "name": "Job-b4f912de-561a-4af8-948e-61281c20ea82",
                            "node_id": "04d5b210591aa5aff5b4e49ad6a3ec57b72aefcdc99cd7888fff80b5991452d8a8dce099312cfb7e78637e04e9824a7274160e49176a00394745701ed450a113e2",
                            "start_at": 1724879773,
                            "status": "Complete",
                            "storage_source": "swanhub",
                            "task_uuid": "f5e15f63-bee2-48f6-8dea-67cc4187979d",
                            "type": None,
                            "updated_at": 1724887024,
                            "uuid": "b4f912de-561a-4af8-948e-61281c20ea82"
                        }
                    ],
                    "task": {
                        "comments": "finish_pending(completed).",
                        "created_at": 1724879753,
                        "end_at": 1724886953,
                        "id": 471,
                        "leading_job_id": "b014b641-97a2-4417-a484-c6e72f9ad8f6",
                        "name": None,
                        "refund_amount": None,
                        "refund_wallet": "0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224",
                        "source": "v2",
                        "start_at": 1724879753,
                        "start_in": 300,
                        "status": "finished",
                        "task_detail": {
                            "amount": 1.0,
                            "bidder_limit": 3,
                            "created_at": 1724879753,
                            "dcc_node_job_source_uri": None,
                            "dcc_selected_cp_list": None,
                            "duration": 3600,
                            "end_at": 1724883353,
                            "hardware": "C1ae.medium",
                            "job_result_uri": None,
                            "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/b43a3c03-043f-4999-94dc-9620b4ef58ab",
                            "price_per_hour": "1.0",
                            "requirements": {
                                "hardware": "None",
                                "hardware_type": "CPU",
                                "memory": "4",
                                "preferred_cp_list": None,
                                "region": "global",
                                "storage": None,
                                "update_max_lag": None,
                                "vcpu": "4"
                            },
                            "space": {
                                "activeOrder": {
                                    "config": {
                                        "description": "CPU only · 4 vCPU · 4 GiB",
                                        "hardware": "CPU only",
                                        "hardware_id": 1,
                                        "hardware_type": "CPU",
                                        "memory": 4,
                                        "name": "C1ae.medium",
                                        "price_per_hour": 1.0,
                                        "vcpu": 4
                                    }
                                },
                                "name": "0",
                                "uuid": "fd461d48-f280-4555-97ea-a8a49b352d18"
                            },
                            "start_at": 1724879753,
                            "status": "paid",
                            "storage_source": "swanhub",
                            "type": "None",
                            "updated_at": 1724879753
                        },
                        "task_detail_cid": "https://plutotest.acl.swanipfs.com/ipfs/QmQBSJJmZWssDHMxrcrhSa3TDpPe5HWi5FFkVNo6kBAzKq",
                        "tx_hash": None,
                        "type": "None",
                        "updated_at": 1724975228,
                        "user_id": 6,
                        "uuid": "f5e15f63-bee2-48f6-8dea-67cc4187979d"
                    }
                },
                {
                    "computing_providers": [
                        {
                            "beneficiary": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186",
                            "cp_account_address": "0x6f43E3e5B70aa5BF5818c56D509BDd092D0907E0",
                            "created_at": 1722488655,
                            "freeze_online": 1,
                            "id": 100,
                            "lat": 45.5075,
                            "lon": -73.5887,
                            "multi_address": [
                                "/ip4/38.140.46.60/tcp/8086"
                            ],
                            "name": "test-dd",
                            "node_id": "04241e19381a8fad4cc98ef6de0a7e417e6d662ff49d8096cff9ec4b08798eeb96687ff5c7b4bde1adb8ccdbb579f16ac0f2c4e0853406282a37285582879dde49",
                            "online": 0,
                            "owner_address": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186",
                            "region": "Quebec-CA",
                            "task_types": "[1, 2, 3, 4]",
                            "updated_at": 1727290151,
                            "version": "2.0",
                            "worker_address": "0x9A5D8Ac48Eb205eCf0B45428bF19DC1ADC1BC186"
                        },
                        {
                            "beneficiary": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94",
                            "cp_account_address": "0x2bd6a6f41b37152677F8b4946490580F63494abD",
                            "created_at": 1722488518,
                            "freeze_online": 1,
                            "id": 99,
                            "lat": 35.8639,
                            "lon": -78.535,
                            "multi_address": [
                                "/ip4/40.143.96.125/tcp/10011"
                            ],
                            "name": "new-cp-001",
                            "node_id": "04d5b210591aa5aff5b4e49ad6a3ec57b72aefcdc99cd7888fff80b5991452d8a8dce099312cfb7e78637e04e9824a7274160e49176a00394745701ed450a113e2",
                            "online": 1,
                            "owner_address": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94",
                            "region": "North Carolina-US",
                            "task_types": "[1, 2, 3, 4, 5]",
                            "updated_at": 1727290151,
                            "version": "2.0",
                            "worker_address": "0xBdDe0ffED293638De69ABD0fCf42237AD3F2cf94"
                        }
                    ],
                    "config_orders": [
                        {
                            "config_id": 2,
                            "created_at": 1724877962,
                            "duration": 3600,
                            "ended_at": None,
                            "error_code": None,
                            "id": 483,
                            "order_type": "Creation",
                            "preferred_cp_list": None,
                            "refund_tx_hash": None,
                            "region": "global",
                            "space_id": None,
                            "start_in": 300,
                            "started_at": 1724877962,
                            "status": "payment_consumed",
                            "task_uuid": "99de8f36-64fb-4c67-a054-c86897513235",
                            "tx_hash": "0x4a623275e19f2ff16d3efadb1e047926f363be8d25d4193e015892c6a40b9d40",
                            "updated_at": 1724877974,
                            "uuid": "8a29cddd-ab9c-4e1e-aa3b-0f8d12fab144"
                        },
                        {
                            "config_id": 2,
                            "created_at": 1724877962,
                            "duration": 3600,
                            "ended_at": None,
                            "error_code": None,
                            "id": 484,
                            "order_type": "Renewal",
                            "preferred_cp_list": None,
                            "refund_tx_hash": None,
                            "region": "global",
                            "space_id": None,
                            "start_in": 300,
                            "started_at": 1724878186,
                            "status": "payment_consumed",
                            "task_uuid": "99de8f36-64fb-4c67-a054-c86897513235",
                            "tx_hash": "0xe808583a9e44c814e25bf9b46d462e1efffa8848944cb24208d0ab6699671a30",
                            "updated_at": 1724878189,
                            "uuid": "2acd0c25-a79a-4a0b-8371-c31de1ed40fa"
                        }
                    ],
                    "jobs": [
                        {
                            "build_log": "wss://log.dev2.crosschain.computer:8086/api/v1/computing/lagrange/spaces/log?space_id=e7726edc-ac2a-4475-915e-e822e1f32ceb&type=build",
                            "comments": "Running: del job for cp. Running(Submitted). Submitted: no job_result_uri from api. no status from api yet.",
                            "container_log": "wss://log.dev2.crosschain.computer:8086/api/v1/computing/lagrange/spaces/log?space_id=e7726edc-ac2a-4475-915e-e822e1f32ceb&type=container",
                            "cp_account_address": "0x6f43E3e5B70aa5BF5818c56D509BDd092D0907E0",
                            "created_at": 1724877977,
                            "duration": 7200,
                            "ended_at": 1724878262,
                            "hardware": "C1ae.medium",
                            "id": 624,
                            "job_real_uri": "https://ad3v1w5qez.dev2.crosschain.computer",
                            "job_result_uri": None,
                            "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/e7726edc-ac2a-4475-915e-e822e1f32ceb",
                            "name": "Job-db39c612-891d-45b5-8c7f-908b5939227d",
                            "node_id": "04241e19381a8fad4cc98ef6de0a7e417e6d662ff49d8096cff9ec4b08798eeb96687ff5c7b4bde1adb8ccdbb579f16ac0f2c4e0853406282a37285582879dde49",
                            "start_at": 1724877982,
                            "status": "Cancelled",
                            "storage_source": "swanhub",
                            "task_uuid": "99de8f36-64fb-4c67-a054-c86897513235",
                            "type": None,
                            "updated_at": 1724878268,
                            "uuid": "db39c612-891d-45b5-8c7f-908b5939227d"
                        },
                        {
                            "build_log": "wss://log.cp.filezoo.com.cn:10011/api/v1/computing/lagrange/spaces/log?job_uuid=a88ec931-5ade-401b-b94c-ce9a49192794&type=build",
                            "comments": "Running: del job for cp. Running(Submitted).",
                            "container_log": "wss://log.cp.filezoo.com.cn:10011/api/v1/computing/lagrange/spaces/log?job_uuid=a88ec931-5ade-401b-b94c-ce9a49192794&type=container",
                            "cp_account_address": "0x2bd6a6f41b37152677F8b4946490580F63494abD",
                            "created_at": 1724877982,
                            "duration": 7200,
                            "ended_at": 1724878262,
                            "hardware": "C1ae.medium",
                            "id": 625,
                            "job_real_uri": "https://vwhgznhb9m.cp.filezoo.com.cn",
                            "job_result_uri": None,
                            "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/e7726edc-ac2a-4475-915e-e822e1f32ceb",
                            "name": "Job-a88ec931-5ade-401b-b94c-ce9a49192794",
                            "node_id": "04d5b210591aa5aff5b4e49ad6a3ec57b72aefcdc99cd7888fff80b5991452d8a8dce099312cfb7e78637e04e9824a7274160e49176a00394745701ed450a113e2",
                            "start_at": 1724877985,
                            "status": "Cancelled",
                            "storage_source": "swanhub",
                            "task_uuid": "99de8f36-64fb-4c67-a054-c86897513235",
                            "type": None,
                            "updated_at": 1724878268,
                            "uuid": "a88ec931-5ade-401b-b94c-ce9a49192794"
                        }
                    ],
                    "task": {
                        "comments": None,
                        "created_at": 1724877962,
                        "end_at": 1724878262,
                        "id": 470,
                        "leading_job_id": "db39c612-891d-45b5-8c7f-908b5939227d",
                        "name": None,
                        "refund_amount": None,
                        "refund_wallet": "0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224",
                        "source": "v2",
                        "start_at": 1724877962,
                        "start_in": 300,
                        "status": "terminated",
                        "task_detail": {
                            "amount": 1.0,
                            "bidder_limit": 3,
                            "created_at": 1724877962,
                            "dcc_node_job_source_uri": None,
                            "dcc_selected_cp_list": None,
                            "duration": 3600,
                            "end_at": 1724881562,
                            "hardware": "C1ae.medium",
                            "job_result_uri": None,
                            "job_source_uri": "https://swanhub-cali.swanchain.io/spaces/e7726edc-ac2a-4475-915e-e822e1f32ceb",
                            "price_per_hour": "1.0",
                            "requirements": {
                                "hardware": "None",
                                "hardware_type": "CPU",
                                "memory": "4",
                                "preferred_cp_list": None,
                                "region": "global",
                                "storage": None,
                                "update_max_lag": None,
                                "vcpu": "4"
                            },
                            "space": {
                                "activeOrder": {
                                    "config": {
                                        "description": "CPU only · 4 vCPU · 4 GiB",
                                        "hardware": "CPU only",
                                        "hardware_id": 1,
                                        "hardware_type": "CPU",
                                        "memory": 4,
                                        "name": "C1ae.medium",
                                        "price_per_hour": 1.0,
                                        "vcpu": 4
                                    }
                                },
                                "name": "0",
                                "uuid": "b8ced717-fd8f-4822-a516-227273f582c4"
                            },
                            "start_at": 1724877962,
                            "status": "paid",
                            "storage_source": "swanhub",
                            "type": "None",
                            "updated_at": 1724877962
                        },
                        "task_detail_cid": "https://plutotest.acl.swanipfs.com/ipfs/QmY8Qav9hax2GfDYDuBh6ctMQek9FGVLvdVVXzWswkXoZQ",
                        "tx_hash": "0x54cd0b2f1ea096ef40f8ed8182d8f719acc2c93574d77fdc596bf41b82e68619",
                        "type": "None",
                        "updated_at": 1724878268,
                        "user_id": 6,
                        "uuid": "99de8f36-64fb-4c67-a054-c86897513235"
                    }
                }
            ],
            "page": 1,
            "size": 2,
            "total": 40,
            "total_page": 20
        },
        "message": "fetch task list for user wallet:0xaA5812Fb31fAA6C073285acD4cB185dDbeBDC224 successfully",
        "status": "success"
    }