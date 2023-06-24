class APIException(Exception):
    def __init__(self, code, message):
        self.message = message
        self.code = code


class APIAccessDenied(APIException):
    def __init__(
        self, code="access_denied", message="Invalid or missing authorization"
    ):
        self.message = message
        self.code = code


class APINotFound(APIException):
    def __init__(self, code="not_found", message="Resource could not be found"):
        self.message = message
        self.code = code
