import web3

from swan.api_client import APIClient

class SwanAPI(APIClient):

    def __init__(self, orchestrator_url, api_key, payment_key): 
        self.orchestrator_url = orchestrator_url 
        self.api_key = api_key 
        self.payment_key = payment_key
 
    def query_price_list(self): 
        """Query the orchestrator for the current instance price list. 
        """ 
        pass 
 
    def build_task(self, source_code_url, instance_type, task_name, public_key=None): 
        """Prepare a task for deployment with the required details. 
        - source_code_url: URL to the code repository containing Docker/K8s file and env file 
        - instance_type: Type of instance needed for the task 
        - task_name: A name for the task 
        - public_key: Optional public key for accessing confidential data 
        """ 
        pass 
 
    def propose_task(self): 
        """Propose the prepared task to the orchestrator. 
        """ 
        pass 
    
    def make_payment(self): 
        """Make payment for the task build after acceptance by the orchestrator. 
        """ 
        pass 
 
    def get_payment_info(self): 
        """Retrieve payment information from the orchestrator after making the payment. 
        """ 
        pass 
 
    def get_task_status(self): 
        """Fetch the current status of the task from the orchestrator. 
        """ 
        pass 
 
    def fetch_task_details(self): 
        """Retrieve the deployed URL and credentials/token for access after task success. 
        Decrypt the credentials/token with the private key if necessary. 
        """ 
        pass 
