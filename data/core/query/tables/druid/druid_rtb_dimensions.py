from dataclasses import dataclass

from core.query.tables.druid.druid_common_dimensions import CommonDimensionsDruid


@dataclass
class RTBDimensionsDruid(CommonDimensionsDruid):
    """Dimensions that are share in rtb hourly table"""

    BUYERS = "buyers"
    CONTENT_CATEGORIES = "contentcategories"
    CONTENT_GENRE = "contentgenre"
    CONTENT_TITLE = "contenttitle"
    CONTENT_SERIES = "contentseries"
    CONTENT_MEDIA_RATING = "contentmediarating"
    CONTENT_LIVESTREAM = "contentlivestream"
    CONTENT_LENGTH = "contentlength"
    CONTENT_LANGUAGE = "contentlanguage"
    CONTENT_NETWORK_NAME = "contentnetworkname"
    CONTENT_CHANNEL_NAME = "contentchannelname"
    ADVERTISER_ID = "advertiserid"
    CAMPAIGN_ID = "campaignid"
    CREATIVE_ID = "creativeid"
    DEAL_ID = "dealid"
    ADVERTISER_DOMAIN = "advertiserdomain"
    SEAT_ID = "seatid"
