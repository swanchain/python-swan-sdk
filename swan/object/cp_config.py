# ./swan/object/cp_config.py

import json

class HardwareConfig:

    def __init__(self, config):
        self.id = config["hardware_id"]
        self.name = config["hardware_name"]
        self.description = config["hardware_description"]
        self.type = config["hardware_type"]
        self.region = config["region"]
        self.price = config["hardware_price"]
        self.status = config["hardware_status"]
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "region": self.region,
            "price": self.price,
            "status": self.status
        }

    def to_json(self):
        return json.dump(self, default=lambda o: o.__dict__,
                         sort_keys=True, indent=4)