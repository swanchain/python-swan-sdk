# ./swan/common/__init__.py
from swan_mcs import APIClient

import os
def init_mcs_api():
    return APIClient(
        os.getenv("MCS_API_KEY"), os.getenv("MCS_ACCESS_TOKEN"), "polygon.mainnet"
    )


mcs_api = init_mcs_api()
