from dataclasses import dataclass

from core.query.tables.athena.athena_table import athena_table
from core.query.tables.athena.athena_table_common import AthenaTableCommon


@dataclass
@athena_table("moat")
class AthenaTableMoat(AthenaTableCommon):
    """Fields of the table moat"""
