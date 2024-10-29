from dataclasses import dataclass


@dataclass
class AthenaTableCommon:
    """Common Fields of all tables"""

    DATE_TIME = "date_time"
    TRANSACTION_GUID = "transaction_guid"
    IP_ADDRESS = "ip_address"
    IP_ADDRESS_OVERRIDE = "ip_address_override"
