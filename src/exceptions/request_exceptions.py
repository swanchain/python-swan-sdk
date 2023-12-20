""" SWAN Custom exceptions for requests """


class SwanHTTPError(Exception):
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


class SwanConnectionError(Exception):
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


class SwanTimeoutError(Exception):
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


class SwanRequestError(Exception):
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


class SwanTooManyRedirectsError(Exception):
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
        return f"SwanTooManyRedirects: {self.message}"
