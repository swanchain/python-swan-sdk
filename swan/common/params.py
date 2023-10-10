import logging
from swan.common.constants import SWAN_API

class Params:
    def __init__(self):
        self.SWAN_API = SWAN_API

    def get_params(self):

        param_vars = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        param_dict = {}
        for i in param_vars:
            param_dict[i] = getattr(self, i)

        return param_dict

    def __str__(self):
        return self.get_params
