from dataclasses import dataclass

from core.query.tables.druid.druid_common_dimensions import CommonDimensionsDruid


@dataclass
class NetworkDimensionsDruid(CommonDimensionsDruid):
    """Dimensions that are share in network table"""

    ALL = "all"
    BUYER = "buyer"
    MEDIA_TYPE = "mediatype"
    VIEWABILITY = "viewability"
    OPP_FILTERS = "oppfilters"
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
