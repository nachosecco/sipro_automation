import hashlib
import json
import os
from typing import List

from core.aerospike_utils import AerospikeUtils
from core.vpc import VPC

TRAFFIC_SHAPING_COMPANY_NAME = "delivery_regression_traffic_shaping"


class TrafficShaping:
    """
    A class to encapsulate any testing functionality related to Traffic Shaping
    Relies on the BIDDER_DATA_FILE environment variable. This file is populated by the generate_bidder_data_file.py script.
    """

    def __init__(self):
        self.aero_namespace = "tempcache"
        self.aero_set = "traffic_shaping"
        self.aero_bin = "bidder_guids"
        self.aero_ttl = 1800  # 30 minutes

        self.path_to_bidder_data_file = os.getenv("BIDDER_DATA_FILE")
        if not self.path_to_bidder_data_file:
            raise ValueError(
                "The Bidder Data file path is required, set the env variable `BIDDER_DATA_FILE`"
            )

        self.bidder_name_to_guid_cache = {}

    def load_blocked_bidders_cache(
        self, vpc: VPC, blocked_bidder_names: List[str]
    ) -> List[str]:
        """
        Load the traffic_shaping Aerospike cache

        vpc: The VPC object of the test case. Used for building the 'key' of the Aerospike record.
        blocked_bidder_names: A List of bidders to include as being blocked for the given key.
        returns : List of blocked bidder guids
        """
        with AerospikeUtils(self.aero_namespace, self.aero_set) as aero_utils:
            raw_key = vpc.uid + vpc.app_id
            hashed_key = hashlib.md5(raw_key.encode("utf-8")).hexdigest()

            bidder_guids = self._get_bidder_guids_from_names(blocked_bidder_names)

            aero_utils.put_record(
                hashed_key, {self.aero_bin: bidder_guids}, self.aero_ttl
            )
            return bidder_guids

    def _get_bidder_guids_from_names(self, bidder_names: List[str]):
        """
        Use the Bidder data file to convert Bidder names to GUIDs

        bidder_names: List of Bidder names to find GUIDs for
        """
        bidder_guids = []
        with open(self.path_to_bidder_data_file, "r") as bidder_file:
            for bidder in bidder_file:
                bidder_details = json.loads(bidder)
                bidder_name = bidder_details.get("name", "")
                bidder_company_name = bidder_details.get("company_name", "")
                if (
                    bidder_name in bidder_names
                    and bidder_company_name == TRAFFIC_SHAPING_COMPANY_NAME
                ):
                    bidder_guids.append(bidder_details.get("guid", "GUID_NOT_FOUND"))

        if len(bidder_guids) != len(bidder_names):
            raise RuntimeError(
                "Unable to find GUIDs in the Bidder Data file for all provided Bidder names"
            )

        return bidder_guids
