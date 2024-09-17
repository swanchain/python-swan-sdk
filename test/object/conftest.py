
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