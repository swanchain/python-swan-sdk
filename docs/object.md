# Swan SDK Object Documentation

## Table Of Contents
- [Introduction](#introduction)
- [Hardware Config](#hardwareconfig)

## Introduction

Swan SDK store API information into python class object for easier navigation on user end. Learn object structure to utilize full functionality of Swan SDK

## HardwareConfig

Hardware configuration is stored in `HardwareConfig` class.

```python
class HardwareConfig:

    def __init__(self, config):
        self.id = config["hardware_id"]
        self.name = config["hardware_name"]
        self.description = config["hardware_description"]
        self.type = config["hardware_type"]
        self.region = config["region"]
        self.price = config["hardware_price"]
        self.status = config["hardware_status"]
```

Individual attribute of a hardware can be retrieved from variables within the `HardwareConfig` class.

HardwareConfig contains `to_dict()` and `to_json()` functions to output all attributes in python dictionary or json format.