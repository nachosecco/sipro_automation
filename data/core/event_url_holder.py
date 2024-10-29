import json
from dataclasses import dataclass


@dataclass
class EventUrlsHolder:
    """Will hold every url that can be called in an event from and ad"""

    ad_id: str
    media_name: str
    impression: str
    start: str
    firstQuartile: str
    midpoint: str
    thirdQuartile: str
    complete: str
    click: str
