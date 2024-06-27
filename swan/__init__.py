# ./swan/__init__.py

from swan.api.swan_api import SwanAPI
from swan.api_client import APIClient
from swan.contract.swan_contract import SwanContract
from swan.session import Session

DEFAULT_SESSION = None

def setup_default_session(api_key=None, **kwargs):
    """
    Set up a default session, passing through any parameters to the session constructor.
    """
    global DEFAULT_SESSION
    DEFAULT_SESSION = Session(api_key=api_key, **kwargs)

def _get_default_session(api_key=None):
    """
    Get the default session, creating one if needed.

    :return: The default session
    """
    global DEFAULT_SESSION
    if DEFAULT_SESSION is None or (api_key is not None and DEFAULT_SESSION.api_key != api_key):
        setup_default_session(api_key=api_key)

    return DEFAULT_SESSION

def resource(api_key=None, *args, **kwargs):
    """
    Create a resource service client by name using the default session.
    """
    session = _get_default_session(api_key)
    return session.resource(*args, **kwargs)