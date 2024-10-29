from dataclasses import dataclass

from core.query.tables.athena.athena_table import athena_table
from core.query.tables.athena.athena_table_common import AthenaTableCommon


@dataclass
@athena_table("rtb")
class AthenaTableRTB(AthenaTableCommon):
    """Fields of the table rtb"""

    BATCH_ID = "batch_id"
    AUCTION_GUID = "auction_guid"
    COMPANY_GUID = "company_guid"
    PUBLISHER_GUID = "publisher_guid"
    SITE_GUID = "site_guid"
    PLACEMENT_GUID = "placement_guid"
    USER_AGENT = "user_agent"
    REFERRER = "referrer"
    LOCATION = "location"
    USER_GUID = "user_guid"
    RESULT = "result"
    DOMAIN = "domain"
    DIMENSION = "dimension"
    GEO = "geo"
    BIDDER_ID = "bidder_id"
    BIDDERS = "bidders"
    FLOOR = "floor"
    W_CPM = "wcpm"
    CPM = "cpm"
    QUALITY = "quality"
    THIRD_PARTY = "thirdparty"
    META = "meta"
    BROKER = "broker"
    PARTITION = "partition"
    OFFSET = "offset"
    APP_META = "app_meta"
    BIDDER_DEAL_DETAILS = "bidder_deal_details"
    PLACEMENT_TYPE = "placement_type"
    BLOCKED_BIDDERS_GUIDS = "blocked_bidders_guids"
