import unittest
import json
from swan.object.cp_config import InstanceResource

class TestInstanceConfig(unittest.TestCase):

    def setUp(self):
        self.config = {
            "hardware_id": 0,
            "hardware_name": "C1ae.small",
            "hardware_description": "CPU only · 2 vCPU · 2 GiB",
            "hardware_type": "CPU",
            "region": [
                "Virginia-US",
                "Quebec-CA",
                "Jakarta-ID"
            ],
            "hardware_price": "0.0",
            "hardware_status": "available"
        }

        self.instance_config = InstanceResource(self.config)

    def test_init(self):
        self.assertEqual(self.instance_config.hardware_id, self.config["hardware_id"])
        self.assertEqual(self.instance_config.instance_type, self.config["hardware_name"])
        self.assertEqual(self.instance_config.description, self.config["hardware_description"])
        self.assertEqual(self.instance_config.type, self.config["hardware_type"])
        self.assertEqual(self.instance_config.region, self.config["region"])
        self.assertEqual(self.instance_config.price, self.config["hardware_price"])
        self.assertEqual(self.instance_config.status, self.config["hardware_status"])

    def test_to_dict(self):
        expected_dict = {
            "hardware_id": self.config["hardware_id"],
            "instance_type": self.config["hardware_name"],
            "description": self.config["hardware_description"],
            "type": self.config["hardware_type"],
            "region": self.config["region"],
            "price": self.config["hardware_price"],
            "status": self.config["hardware_status"]
        }
        # print(self.instance_config.to_dict())
        self.assertEqual(self.instance_config.to_dict(), expected_dict)

    def test_to_json(self):
        expected_json = json.dumps({
            "hardware_id": self.config["hardware_id"],
            "instance_type": self.config["hardware_name"],
            "description": self.config["hardware_description"],
            "type": self.config["hardware_type"],
            "region": self.config["region"],
            "price": self.config["hardware_price"],
            "status": self.config["hardware_status"]
        }, indent=2)
        # print(self.instance_config.to_json())
        self.assertEqual(self.instance_config.to_json(), expected_json)

    def test_to_str(self):
        expected_json = json.dumps({
            "hardware_id": self.config["hardware_id"],
            "instance_type": self.config["hardware_name"],
            "description": self.config["hardware_description"],
            "type": self.config["hardware_type"],
            "region": self.config["region"],
            "price": self.config["hardware_price"],
            "status": self.config["hardware_status"]
        }, indent=2)
        expected_str = str(expected_json)
        # print(str(self.instance_config))
        self.assertEqual(str(self.instance_config), expected_str)

    def test_getitem(self):
        self.assertEqual(self.instance_config["hardware_id"], self.config["hardware_id"])
        self.assertEqual(self.instance_config["instance_type"], self.config["hardware_name"])
        self.assertEqual(self.instance_config["description"], self.config["hardware_description"])
        self.assertEqual(self.instance_config["type"], self.config["hardware_type"])
        self.assertEqual(self.instance_config["region"], self.config["region"])
        self.assertEqual(self.instance_config["price"], self.config["hardware_price"])
        self.assertEqual(self.instance_config["status"], self.config["hardware_status"])

    def test_get(self):
        self.assertEqual(self.instance_config.get("hardware_id"), self.config["hardware_id"])
        self.assertEqual(self.instance_config.get("instance_type"), self.config["hardware_name"])
        self.assertEqual(self.instance_config.get("description"), self.config["hardware_description"])
        self.assertEqual(self.instance_config.get("type"), self.config["hardware_type"])
        self.assertEqual(self.instance_config.get("region"), self.config["region"])
        self.assertEqual(self.instance_config.get("price"), self.config["hardware_price"])
        self.assertEqual(self.instance_config.get("status"), self.config["hardware_status"])
        self.assertIsNone(self.instance_config.get("non_existent_key"))
        self.assertEqual(self.instance_config.get("non_existent_key", "default_value"), "default_value")

    def test_repr(self):
        expected_repr = f"InstanceResource({self.instance_config.to_json()})"
        print(repr(self.instance_config))
        self.assertEqual(repr(self.instance_config), expected_repr)

    def test_update_config(self):
        new_config = {
            "hardware_id": 1,
            "hardware_name": "C2ae.medium",
            "hardware_description": "CPU only · 4 vCPU · 4 GiB",
            "hardware_type": "CPU",
            "region": [
                "California-US",
                "Ontario-CA",
                "Singapore-SG"
            ],
            "hardware_price": "0.1",
            "hardware_status": "unavailable"
        }
        self.instance_config.hardware_id = new_config["hardware_id"]
        self.instance_config.instance_type = new_config["hardware_name"]
        self.instance_config.description = new_config["hardware_description"]
        self.instance_config.type = new_config["hardware_type"]
        self.instance_config.region = new_config["region"]
        self.instance_config.price = new_config["hardware_price"]
        self.instance_config.status = new_config["hardware_status"]

        self.assertEqual(self.instance_config.hardware_id, new_config["hardware_id"])
        self.assertEqual(self.instance_config.instance_type, new_config["hardware_name"])
        self.assertEqual(self.instance_config.description, new_config["hardware_description"])
        self.assertEqual(self.instance_config.type, new_config["hardware_type"])
        self.assertEqual(self.instance_config.region, new_config["region"])
        self.assertEqual(self.instance_config.price, new_config["hardware_price"])
        self.assertEqual(self.instance_config.status, new_config["hardware_status"])

if __name__ == '__main__':
    unittest.main()