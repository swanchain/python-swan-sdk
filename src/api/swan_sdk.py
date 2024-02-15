import logging

from src.api_client import APIClient
from src.constants.constants import PROCESSING_TASKS, GET, POST, JOBS, CELERY
class SwanSDK: 

    def __init__(self, orchestrator_url, api_key, payment_key, api_client=None): 

        if api_client is None:
            api_client = APIClient("placeholder_api_key", "sample_wallet_address")
        self.orchestrator_url = orchestrator_url 

        self.api_key = api_key 

        self.payment_key = payment_key 

 

    def query_price_list(self): 

        """ 

        Query the orchestrator for the current instance price list. 

        """ 
        price_list = self.api_client._request_without_params(
            GET, PROCESSING_TASKS, self.api_client.SWAN_API, self.token
        )
        return price_list
 

 

    def init_sdk(self): 

        """ 

        Initialize SDK configuration with orchestrator URL, API key, and payment key. 

        """ 

        pass 

 

    def build_task(self, source_code_url, instance_type, task_name, public_key=None): 

        """ 

        Prepare a task for deployment with the required details. 

        - source_code_url: URL to the code repository containing Docker/K8s file and env file 

        - instance_type: Type of instance needed for the task 

        - task_name: A name for the task 

        - public_key: Optional public key for accessing confidential data 

        """ 

        pass 

 

    def propose_task(self): 

        """ 

        Propose the prepared task to the orchestrator. 

        """ 

        pass 

 

    def make_payment(self): 

        """ 

        Make payment for the task build after acceptance by the orchestrator. 

        """ 

        pass 

 

    def get_payment_info(self): 

        """ 

        Retrieve payment information from the orchestrator after making the payment. 

        """ 
        return payment_info.toDict()

        pass 

 

    def get_task_status(self): 

        """ 

        Fetch the current status of the task from the orchestrator. 

        """ 
        return task.status
        pass 

 

    def fetch_task_details(self): 

        """ 

        Retrieve the deployed URL and credentials/token for access after task success. 

        Decrypt the credentials/token with the private key if necessary. 

        """ 
        
        if task.status == "success":

            return 
        pass 
