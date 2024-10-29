from dataclasses import dataclass

from core.query.tables.athena.athena_table import athena_table
from core.query.tables.athena.athena_table_common import AthenaTableCommon


@dataclass
@athena_table("action")
class AthenaTableAction(AthenaTableCommon):
    """Fields of the table action"""

    BATCH_ID = "batch_id"
    TYPE = "type"
    COMPANY_GUID = "company_guid"
    PUBLISHER_GUID = "publisher_guid"
    SITE_GUID = "site_guid"
    PLACEMENT_GUID = "placement_guid"
    USER_AGENT = "user_agent"
    REFERRER = "referrer"
    COOKIE_GUID = "cookie_guid"
    SITE_DOMAIN = "site_domain"
    PLACEMENT_SIZE = "placement_size"
    PLACEMENT_POSITION = "placement_position"
    PLACEMENT_TYPE = "placement_type"
    PLACEMENT_TYPE_GUID = "placement_type_guid"
    GEO = "geo"
    PARTNER_GUID = "partner_guid"
    AD_GUID = "ad_guid"
    FLOOR = "floor"
    CPM = "cpm"
    HE_CPM = "hecpm"
    QUARTILE = "quartile"
    TICK = "tick"
    AIR = "air"
    ERROR = "error"
    SOCIAL = "social"
    BROKER = "broker"
    PARTITION = "partition"
    OFFSET = "offset"
    LOCATION = "location"
    QUALITY = "quality"
    META = "meta"
    THIRD_PARTY = "thirdparty"
    APP_META = "app_meta"
    SEAT_ID = "seat_id"
    BIDDER_GUID = "bidder_guid"
