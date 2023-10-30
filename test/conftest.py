import pytest, os
from swan.api_client import APIClient
from swan.api.engine_api import EngineAPI
from dotenv import load_dotenv

abs_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(abs_path + '/.env_test')
api_key = os.getenv('api_key')
wallet_address = os.getenv('wallet_address')
wrong_wallet_address = os.getenv('wrong_wallet_address')
wrong_api_key = os.getenv('wrong_api_key')

@pytest.fixture()
def shared_real_engine_api(scope="module",autouse=True):
    api_client = APIClient(api_key,wallet_address, True)
    engine_api = EngineAPI(api_client)
    return engine_api
