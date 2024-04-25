# ./swan/common/constant.py

SWAN_API = "https://orchestrator-api.swanchain.io"

# Swan API
SWAN_APIKEY_LOGIN = "/login_by_api_key"
DEPLOY_TASK = "/v1/space_deployment"
DEPLOYMENT_INFO = "/v1/space_deployment/"
DEPLOYED_URL = "/v1/space_deploymnet/job_real_url"
GET_CP_CONFIG = "/cp/machines"
PROVIDER_PAYMENTS = "/provider/payments"
CREATE_TASK = "/v2/task_deployment"

# API Syntax
REST_API_VERSION = "v1"
GET = "GET"
PUT = "PUT"
POST = "POST"
DELETE = "DELETE"

# Contract
PAYMENT_CONTRACT_ABI = "PaymentContract.json"
SWAN_TOKEN_ABI = "SwanToken.json"
CLIENT_CONTRACT_ABI = "ClientPayment.json"

# Contract Address
# PAYMENT_CONTRACT_ADDRESS = "0xF0F98f476b1a5c1c6EA97eEb23d8796F553246d9"
# CLIENT_CONTRACT_ADDRESS = "0xe356a758fA1748dfBE71E989c876959665a66ddA"
PAYMENT_CONTRACT_ADDRESS = "0xB48c5D1c025655BA79Ac4E10C0F19523dB97c816"
TOKEN_CONTRACT_ADDRESS = "0x91B25A65b295F0405552A4bbB77879ab5e38166c"
CLIENT_CONTRACT_ADDRESS = "0x9c5397F804f6663326151c81bBD82bb1451059E8"

# Other
CONTRACT_TIMEOUT = 300
STORAGE_LAGRANGE: str = "lagrange"
ORCHESTRATOR_API = "orchestrator-api.swanchain.io"
MAX_DURATION = 1209600

# MCS API
MCS_POLYGON_MAIN_API = "https://api.swanipfs.com"
MCS_POLYGON_MUMBAI_API = "https://calibration-mcs-api.filswan.com"
MCS_BSC_API = 'https://calibration-mcs-bsc.filswan.com'
FIL_PRICE_API = "https://api.filswan.com/stats/storage"
MCS_PARAMS = "/api/v1/common/system/params"
PRICE_RATE = "/api/v1/billing/price/filecoin"
PAYMENT_INFO = "/api/v1/billing/deal/lockpayment/info"
TASKS_DEALS = "/api/v1/storage/tasks/deals"
MINT_INFO = "/api/v1/storage/mint/info"
UPLOAD_FILE = "/api/v1/storage/ipfs/upload"
DEAL_DETAIL = "/api/v1/storage/deal/detail/"
USER_REGISTER = "/api/v1/user/register"
USER_LOGIN = "/api/v1/user/login_by_metamask_signature"
GENERATE_APIKEY = "/api/v1/user/generate_api_key"
APIKEY_LOGIN = "/api/v2/user/login_by_api_key"
COLLECTIONS = "/api/v1/storage/mint/nft_collections"
COLLECTION = "/api/v1/storage/mint/nft_collection"
CREATE_BUCKET = "/api/v2/bucket/create"
BUCKET_LIST = "/api/v2/bucket/get_bucket_list"
DELETE_BUCKET = "/api/v2/bucket/delete"
FILE_INFO = "/api/v2/oss_file/get_file_info"
DELETE_FILE = "/api/v2/oss_file/delete"
CREATE_FOLDER = "/api/v2/oss_file/create_folder"
CHECK_UPLOAD = "/api/v2/oss_file/check"
UPLOAD_CHUNK = "/api/v2/oss_file/upload"
MERGE_FILE = "/api/v2/oss_file/merge"
FILE_LIST = "/api/v2/oss_file/get_file_list"
GET_FILE = "/api/v2/oss_file/get_file_by_object_name"
GET_GATEWAY = "/api/v2/gateway/get_gateway"
PIN_IPFS = "/api/v2/oss_file/pin_files_to_ipfs"