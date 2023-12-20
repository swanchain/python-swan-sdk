""" Computing Provider Custom Exceptions """


class SwanCPDetailInvalidInputError(Exception):
    """
    Custom exception for input parameters are invalid for CP details

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
        return f"SwanCPDetailInvalidInputError: {self.message}"


class SwanCPDetailNotFoundError(Exception):
    """
    Custom exception CP is not found

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
        return f"SwanCPDetailNotFoundError: {self.message}"
