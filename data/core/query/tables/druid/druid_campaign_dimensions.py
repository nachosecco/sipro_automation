from dataclasses import dataclass

from core.query.tables.druid.druid_common_dimensions import CommonDimensionsDruid


@dataclass
class CampaignDimensionsDruid(CommonDimensionsDruid):
    """Dimensions that are share in campaign table"""

    ALL = "all"
    BUYER = "buyer"
    INSERTION_ORDER = "insertionorder"
    CAMPAIGN = "campaign"
    MEDIA = "media"
    OPPFILTERS = "oppfilters"
    CONTENT_CATEGORIES = "contentcategories"
    CONTENT_GENRE = "contentgenre"
    CONTENT_TITLE = "contenttitle"
    CONTENT_SERIES = "contentseries"
    CONTENT_MEDIA_RATING = "contentmediarating"
    CONTENT_LIVESTREAM = "contentlivestream"
    CONTENT_LENGTH = "contentlength"
    CONTENT_NETWORK_NAME = "contentnetworkname"
    CONTENT_CHANNEL_NAME = "contentchannelname"
    POD_SEQUENCE = "podsequence"
    DEVICE_MAKE = "devicemake"
