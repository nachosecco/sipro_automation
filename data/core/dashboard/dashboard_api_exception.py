class DashboardApiException(Exception):
    """Custom exception class, when we have issues using dashboard api"""

    def __init__(self, message):
        super().__init__(message)
