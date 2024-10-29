from dataclasses import dataclass


@dataclass
class TrafficShapingRecord:
    bidder_guid: str
    hour: str
    app_bundle_id: str
    placement_guid: str
    transaction_guid: str
