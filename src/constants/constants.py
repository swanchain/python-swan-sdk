""" Constants used in the project """

# Base APIs
SWAN_API = "http://swanhub-cali.swanchain.io"
AUCTION_API = "http://172.16.200.12:5003"

# APIs

TOKEN_VALIDATION = '/api_token/validate'
STATS_GENERAL = "/stats/general"
TASK_BIDDING = "/task/bidding"
APIKEY_LOGIN = "/login_by_api_key"
ALL_CP_MACHINE = "/cp/machines"
CP_LIST = "/cp_list"
CP_DETAIL = "cp_detail/<string:cp_id>"

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

