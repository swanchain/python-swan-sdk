""" Task Custom exceptions """


class SwanTaskInvalidInputError(Exception):
    """
    Custom exception for input parameters are invalid for Task

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
        return f"SwanTaskInvalidInputError: {self.message}"
