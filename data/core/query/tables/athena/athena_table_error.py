from dataclasses import dataclass

from core.query.tables.athena.athena_table import athena_table
from core.query.tables.athena.athena_table_common import AthenaTableCommon


@dataclass
@athena_table("error")
class AthenaTableError(AthenaTableCommon):
    """Fields of the table error"""

    COMPANY_GUID = "company_guid"
    PUBLISHER_GUID = "publisher_guid"
    PLACEMENT_GUID = "placement_guid"
    COOKIE_GUID = "cookie_guid"
