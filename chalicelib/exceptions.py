from chalice import ChaliceViewError

class DatabaseConnectionError(ChaliceViewError):
    STATUS_CODE = 501