class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class RequestError(Error):
    """Exception raised when a request parameter is invlaid
    Attributes:
        errorType -- type of the error
        message -- explanation of the error
        statusCode --  HTTP status code
    """

    def __init__(self, message):
        self.errorType = "BAD_REQUEST"
        self.message = message
        self.statusCode = 422
