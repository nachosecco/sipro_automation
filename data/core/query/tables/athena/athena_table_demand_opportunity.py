from dataclasses import dataclass

from core.query.tables.athena.athena_table import athena_table
from core.query.tables.athena.athena_table_common import AthenaTableCommon


@dataclass
@athena_table("opportunity")
class AthenaTableDemandOpportunity(AthenaTableCommon):
    """Fields of the table opportunity"""

    BATCH_ID = "batch_id"
    TYPE = "type"
    COMPANY_GUID = "company_guid"
    PUBLISHER_GUID = "publisher_guid"
    SITE_GUID = "site_guid"
    PLACEMENT_GUID = "placement_guid"
    MEDIA_GUID = "media_guid"
    COOKIE_GUID = "cookie_guid"
    ADVERTISER_GUID = "advertiser_guid"
    CAMPAIGN_GUID = "campaign_guid"
    IO_GUID = "io_guid"
    DEAL_ID = "deal_id"
    DEAL_GUID = "deal_guid"
    BIDDER_GUID = "bidder_guid"
    COUNTRY = "country"
    STATE = "state"
    DMA = "dma"
    VIEWABILITY = "viewability"
    PLACEMENT_SIZE = "placement_size"
    MEDIA_TYPE = "media_type"
    SITE_DOMAIN = "site_domain"
    USER_AGENT = "user_agent"
    DEVICE_TYPE = "device_type"
    OPERATING_SYSTEM = "operating_system"
    APP_NAME = "app_name"
    APP_BUNDLE_ID = "app_bundle_id"
    FILTER_REASON = "filter_reason"
    POD_NAME = "pod_name"
    KAFKA_PARTITION = "kafka_partition"
    KAFKA_OFFSET = "kafka_offset"
    CITY = "city"
    DEVICE_MAKE = "device_make"
    MEDIA_INFO = "media_info"
    CONTENT_INFO = "content_info"
    USING_SESSION_ID_AS_UID = "using_session_id_as_uid"
