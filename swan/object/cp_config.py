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
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
    

    def to_instance_dict(self):
        return {
            "hardware_id": self.id,
            "instance_type": self.name,
            "description": self.description,
            "type": self.type,
            "region": self.region,
            "price": self.price,
            "status": self.status
        }


class InstanceResource:

    def __init__(self, config):
        self.hardware_id = config["hardware_id"]
        self.instance_type = config["hardware_name"]
        self.description = config["hardware_description"]
        self.type = config["hardware_type"]
        self.region = config["region"]
        self.price = config["hardware_price"]
        self.status = config["hardware_status"]
    
    def to_dict(self):
        return {
            "hardware_id": self.hardware_id,
            "instance_type": self.instance_type,
            "description": self.description,
            "type": self.type,
            "region": self.region,
            "price": self.price,
            "status": self.status
        }
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
    
    def __str__(self) -> str:
        return str(self.to_json())
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_json()})"
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
