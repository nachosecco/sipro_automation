from enum import Enum


class MediaSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    CUSTOM = "custom"


class GeoTargeting:
    def __init__(self):
        self.country = ""
        self.region = ""
        self.regionName = ""
        self.city = ""
        self.cityName = ""
        self.dma = ""
        self.postalCode = ""

    def __repr__(self):
        message = ""
        if len(self.country) > 0:
            message = "Country: [" + self.country + "]"
        if len(self.region) > 0:
            message += " Region: [" + self.region + "]"
        if len(self.regionName) > 0:
            message += " Region Name: [" + self.regionName + "]"
        if len(self.city) > 0:
            message += " City: [" + self.city + "]"
        if len(self.cityName) > 0:
            message += " City Name: [" + self.cityName + "]"
        if len(self.dma) > 0:
            message += " DMA: [" + self.dma + "]"
        if len(self.postalCode) > 0:
            message += " Postal Code: [" + self.postalCode + "]"
        return message


class DeviceTargeting:
    """This is class related to device targeting, and the expected values"""

    def __init__(self):
        self.type = ""
        self.os = ""
        self.version = ""
        self.vendor = ""
        self.model = ""

    def __repr__(self):
        message = ""
        if len(self.type) > 0:
            message += " Type: [" + self.type + "]"
        if len(self.os) > 0:
            message += " Os: [" + self.os + "]"
        if len(self.version) > 0:
            message += " version: [" + self.version + "]"
        if len(self.vendor) > 0:
            message += " vendor: [" + self.vendor + "]"
        if len(self.model) > 0:
            message += " model: [" + self.model + "]"
        return message


class MediaSizeTargeting:
    def __init__(self, size: type(MediaSize), custom=""):
        self.size = size
        self.custom = custom

    def to_value(self):
        return f"{self.size.value}{self.custom}"


class targeting:
    def __init__(self):
        self.geo = GeoTargeting()
        self.deviceTargeting = DeviceTargeting()

    def geo(self):
        return self.geo
