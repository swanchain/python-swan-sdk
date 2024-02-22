# ./swan/object/task.py

import json

class Task:

    def __init__(
            self, 
            job_source_uri: str =None, 
            paid_amount: int = None, 
            duration: int = None, 
            tx_hash:str = None, 
            config_name: str = None, 
            region: str = None,
            task_uuid: str = None, 
            task_name: str = None
            ):
        self.job_source_uri = job_source_uri
        self.paid_amount = paid_amount
        self.duration = duration
        self.tx_hash = tx_hash
        self.config_name = config_name
        self.region = region
        self.task_uuid = task_uuid
        self.task_name = task_name
    
    def to_dict(self):
        return {
            "task_name": self.task_name,
            "task_uuid": self.task_uuid,
            "region": self.region,
            "config_name": self.config_name,
            "tx_hash": self.tx_hash,
            "duration": self.duration,
            "paid_amount": self.paid_amount,
            "job_source_uri": self.job_source_uri
        }

    def to_json(self):
        return json.dump(self, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)