from dataclasses import dataclass

from core.query.tables.athena.athena_table import athena_table
from core.query.tables.athena.athena_table_common import AthenaTableCommon


@dataclass
@athena_table("adattempt")
class AthenaTableAdAttempt(AthenaTableCommon):
    """Fields of the table adattempt"""

    RECEIVED_TIME = "receivedtime"
    TYPE = "type"
    COMPANY_GUID = "companyguid"
    PUBLISHER_GUID = "publisherguid"
    SITE_GUID = "siteguid"
    PLACEMENT_GUID = "placementguid"
    MEDIA_GUID = "mediaguid"
    COOKIE_GUID = "cookieguid"
    K_BROKER = "k_broker"
    K_PARTITION = "k_partition"
    K_OFFSET = "k_offset"
    ADVERTISER_GUID = "advertiser_guid"
    CAMPAIGN_GUID = "campaign_guid"
    IO_GUID = "io_guid"
    DEAL_ID = "deal_id"
    DEAL_GUID = "deal_guid"
    BIDDER_GUID = "bidder_guid"
    COUNTRY = "country"
    STATE = "state"
    DMA = "dma"
    IA_NHT = "ia_nht"
    DOUBLE_VERIFY = "double_verify"
    VIEWABILITY = "viewability"
    PLACEMENT_SIZE = "placement_size"
    MEDIA_TYPE = "media_type"
    SITE_DOMAIN = "site_domain"
    USER_AGENT = "user_agent"
    DEVICE_TYPE = "device_type"
    OPERATING_SYSTEM = "operating_system"
    APPNAME = "appname"
    APPBUNDLE_ID = "appbundleid"
    SEAT_ID = "seat_id"
    CITY = "city"
