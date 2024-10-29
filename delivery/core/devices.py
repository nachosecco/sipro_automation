## For more user agent examples,
# 1 visit https://deviceatlas.com/blog/list-smart-tv-user-agent-strings
# 2 visit https://deviceatlas.com/blog/list-of-user-agent-strings

from enum import Enum


class DeviceType(Enum):
    """This is a mapping between our Targeting Device Type names and the RTB Device Type integers
    This could be split in the future if the need arises, but for now we only need the name for
    Targeting assertions and the RTB integer for RTB assertions.
    """

    OTHER = 1
    DESKTOP = 2
    CONNECTEDTV = 3
    SMARTPHONE = 4
    TABLET = 5


class DeviceOs(Enum):
    """List of OS names we have for Targeting.
    The value is the casing that will be expected from the RTB object assertion
    """

    IOS = "iOS"
    ANDROID = "Android"
    WINDOWS = "Windows"
    OSX = "OSX"
    LINUX = "Linux"
    OTHER = "Other"


class Device:
    """Holder of Device Info"""

    def __init__(
        self,
        ua,
        device_type=DeviceType.OTHER,
        make="",
        model="",
        os=DeviceOs.OTHER,
        os_version="",
    ) -> None:
        self.ua = ua
        self.rtb_type = device_type.value
        self.targeting_type = device_type.name
        self.make = make
        self.model = model
        self.os = os.value
        self.os_version = os_version


DEVICE_SMARTPHONE_APPLE = Device(
    ua="Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    device_type=DeviceType.SMARTPHONE,
    make="Apple",
    model="iPhone 13 Pro Max",
    os=DeviceOs.IOS,
    os_version="15.0",
)

DEVICE_SMARTPHONE_SAMSUNG = Device(
    ua="Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    device_type=DeviceType.SMARTPHONE,
    make="Samsung",
    model="SM-S906N",
    os=DeviceOs.ANDROID,
    os_version="12",
)

DEVICE_CTV_ROKU = Device(
    ua="Mozilla/5.0 (compatible; U; NETFLIX) AppleWebKit/533.3 (KHTML, like Gecko) Qt/4.7.0 Safari/533.3 Netflix/3.2 (DEVTYPE=RKU-42XXX-; CERTVER=0) QtWebKit/2.2, Roku 3/7.0 (Roku, 4200X, Wireless)",
    device_type=DeviceType.CONNECTEDTV,
    make="Roku",
    model="4200X",
    os=DeviceOs.OTHER,
    os_version="4.7.0",
)

DEVICE_TABLET_LG = Device(
    ua="Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36",
    device_type=DeviceType.TABLET,
    make="LG",
    model="V410",
    os=DeviceOs.ANDROID,
    os_version="5.0.2",
)

DEVICE_TABLET_APPLE_IOS = Device(
    ua="AppleCoreMedia/1.0.0.16H71 (iPad; U; CPU OS 12_5_6 like Mac OS X; en_us)",
    device_type=DeviceType.TABLET,
    make="Apple",
    model="iPad",
    os=DeviceOs.IOS,
    os_version="12.5.6",
)

DEVICE_DESKTOP_MAC = Device(
    ua="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    device_type=DeviceType.DESKTOP,
    make="Apple",
    os=DeviceOs.OSX,
    os_version="10.11.2",
)
