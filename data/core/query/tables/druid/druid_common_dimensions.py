from dataclasses import dataclass


@dataclass
class CommonDimensionsDruid:
    """Dimensions that are share in all tables"""

    COUNTRY = "country"
    DOMAIN = "domain"
    VIABILITY = "viewability"
    DEVICE = "device"
    OPERATING_SYSTEM = "operatingsystem"
    APP_NAME = "appname"
    APP_BUNDLE = "appbundle"
    MEDIA_TYPE = "mediatype"
    PUBLISHER = "publisher"
    SITE = "site"
    PLACEMENT = "placement"
    MOAT = "moat"
    STATE = "state"
    CITY = "city"
    DMA = "dma"
    COMPANY = "company"
    DEVICE_MAKE = "deviceMake"
