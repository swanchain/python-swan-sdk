""" All exceptions class for SDK """


class SwanAPIException(Exception):
    def __init__(self, response):
        print(response.text + ", " + str(response.status_code))
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = "Invalid JSON error message from swan: {}".format(
                response.text
            )
        else:
            if "error_code" in json_res.keys() and "error_message" in json_res.keys():
                self.code = json_res["error_code"]
                self.message = json_res["error_message"]
            else:
                self.code = "None"
                self.message = "System error"

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, "request", None)

    def __str__(self):  # pragma: no cover
        return "API Request Error(error_code=%s): %s" % (self.code, self.message)


class SwanRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "SwanRequestException: %s" % self.message


class SwanParamsException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "SwanParamsException: %s" % self.message


class HTTPError(Exception):
    """
    Custom exception for HTTP errors.

    Attributes:
        message (str): A message describing the error.
    """

    def __init__(self, message):
        """
        Initialize the exception with a message.

        Args:
            message (str): A message describing the error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A string describing the exception.
        """
        return f"SwanHTTPError: {self.message}"


class ConnectionError(Exception):
    """
    Custom exception for connection errors.

    Attributes:
        message (str): A message describing the error.
    """

    def __init__(self, message):
        """
        Initialize the exception with a message.

        Args:
            message (str): A message describing the error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A string describing the exception.
        """
        return f"SwanConnectionError: {self.message}"


class TimeoutError(Exception):
    """
    Custom exception for timeout errors.

    Attributes:
        message (str): A message describing the error.
    """

    def __init__(self, message):
        """
        Initialize the exception with a message.

        Args:
            message (str): A message describing the error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A string describing the exception.
        """
        return f"SwanTimeoutError: {self.message}"


class RequestError(Exception):
    """
    Custom exception for general request errors.

    Attributes:
        message (str): A message describing the error.
    """

    def __init__(self, message):
        """
        Initialize the exception with a message.

        Args:
            message (str): A message describing the error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A string describing the exception.
        """
        return f"SwanRequestError: {self.message}"

