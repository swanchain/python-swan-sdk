import pytest
from swan.api_client import APIClient
from swan.api.engine_api import EngineAPI
@pytest.fixture()
def shared_real_engine_api(scope="module",autouse=True):
    api_client = APIClient("placeholder_api_key","sample_wallet_address")
    engine_api = EngineAPI(api_client)
    return engine_api
