# ./swan/common/exception.py


class SwanAPIException(Exception):
    
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return f'SwanAPIRequestException: {self.message}\n'


class SwanRequestException(Exception):
    pass


class SwanParamsException(Exception):
    pass