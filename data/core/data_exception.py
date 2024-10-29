class DataException(Exception):
    """Custom exception class, when we have generic messages"""

    def __init__(self, message):
        super().__init__(message)
