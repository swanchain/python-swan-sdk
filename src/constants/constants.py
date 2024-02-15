""" Constants used in the project """

# Base APIs
SWAN_API = "http://swanhub-cali.swanchain.io"

# APIs
TOKEN_VALIDATION = "/api_token/validate"
STATS_GENERAL = "/stats/general"
TASK_BIDDING = "/task/bidding"
APIKEY_LOGIN = "/login_by_api_key"
ALL_CP_MACHINE = "/cp/machines"
PAYMENT_VALIDATION = "/payment_validate"
CLAIM_REVIEW = "/claim_review"
DEPLOYMENT_SPACE = "/v1/space_deployment/"
CP_DISTRIBUTION = "/cp_distribution"
CP_LIST = "/cp_list"
COLLATERAL_BALANCE = "/cp/collateral/<string:cp_address>"
CP_DETAIL = "cp_detail/<string:cp_id>"
CP_AVAILABLE = "/cp_available"
API_TOKEN = "/api_token"
DELETE_API_TOKEN = '/api_token/delete'
VALIDATE_API_TOKEN = '/api_token/validate'
ADDRESS_FROM_TOKEN = '/address_from_token'

# Request
GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"

# Auction api
CELERY = "/celery/task/status/"
JOBS = "/lagrange/jobs"
PROCESSING_TASKS = "/api/tasks/processing"
DASHBOARD = "/"
