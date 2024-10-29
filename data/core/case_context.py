from dataclasses import dataclass


@dataclass
class CaseContext:
    """This is the context of a case to reuse in query's"""

    placement_guid: str
    min_hour: str
    max_hour: str
