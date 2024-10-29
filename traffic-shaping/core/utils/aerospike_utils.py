import logging
import os
import hashlib

import aerospike

# Constants
AEROSPIKE_NAMESPACE = "tempcache"
AEROSPIKE_SET = "traffic_shaping"
BLOCKED_BIDDERS_BIN = "bidder_guids"


def get_hashed_record_key(raw_key):
    """
    Hash the raw key to get the hashed key
    :param raw_key: the raw key to be hashed
    :return: the hashed key
    """
    return hashlib.md5(raw_key.encode("utf-8")).hexdigest()


class AerospikeClient:
    """
    Wrapper class for interacting with an Aerospike cluster.
    It takes care of opening and closing the client connection.

    For example:
    with AerospikeClient() as aero:
            aero.get_record(...)
    """

    def __init__(self):
        self.aerospike_host = os.environ.get("AEROSPIKE_HOST", "localhost")
        self.aerospike_port = int(os.environ.get("AEROSPIKE_PORT", 3000))
        self.aero_config = {"hosts": [(self.aerospike_host, self.aerospike_port)]}
        logging.info(
            f"Connecting to Aerospike at {self.aerospike_host}:{self.aerospike_port}"
        )
        self.aero_client = aerospike.client(self.aero_config)

    def __enter__(self):
        self.aero_client.connect()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.aero_client.close()


# Gets an aerospike record's bins by key, hashing the key first
def get_bins(key):
    """
    Get a record from Aerospike
    :param key: hashed key of the record
    :return: the bins as a Dict
    """
    hashed_key = get_hashed_record_key(key)
    with AerospikeClient() as aero:
        _, _, bins = aero.aero_client.get(
            (AEROSPIKE_NAMESPACE, AEROSPIKE_SET, hashed_key)
        )
        return bins
