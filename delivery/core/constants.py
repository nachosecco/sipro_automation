import requests
from enum import Enum

REPLACE = "[REPLACE]"
UNKNOWN = "UNKNOWN"
NOT_EMPTY = "NOT_EMPTY"
NOT_FOUND = "NOT_FOUND"
IP_ADDRESS_VALIDATION_REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
AUTOMATION_FRAMEWORK_ID_DELIVERY = "automationFrameworkIdDelivery"
NUMBER_PLACEHOLDER = 0
FAKE_BIDDER_URL = "https://fakebidder.rowdy.cc/rtbResponse?"
MULTI_VALUE_SEPARATOR = ";;"
PYTHON_REQUEST_UA = "python-requests/" + requests.__version__


class ComparisonType(Enum):
    Equality = 1
    Startswith = 2
    Contains = 3
    Endswith = 4
    Pattern = 5
    NotEmpty = 6
