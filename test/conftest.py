""" Test Configuration for Pytest. """

import pytest
import os
from dotenv import load_dotenv

from src.api.engine_api import EngineAPI
from src.api_client import APIClient

# Load environment variables from a .env file
load_dotenv()

# Retrieve environment variables
api_key = os.getenv("api_key")
wallet_address = os.getenv("wallet_address")
wrong_wallet_address = os.getenv("wrong_wallet_address")
wrong_api_key = os.getenv("wrong_api_key")


@pytest.fixture()
def shared_real_engine_api():
    """Fixture to provide a shared Engine API instance."""
    # Initialize the API client with real credentials
    api_client = APIClient(api_key, wallet_address, True)

    # Create an Engine API instance using the API client
    engine_api = EngineAPI(api_client)

    return engine_api
