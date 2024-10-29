import os
from typing import Dict

import aerospike


class AerospikeUtils:
    """
    Wrapper class for interacting with an Aerospike cluster.
    It takes care of opening and closing the client connection.

    For example:
    with AerospikeUtils("some_namespace", "some_set") as aero:
      aero.put_record(...)
    """

    def __init__(self, aero_namespace, aero_set):
        self.aerospike_host = os.environ.get("AEROSPIKE_HOST", "localhost")
        self.aerospike_port = int(os.environ.get("AEROSPIKE_PORT", 3000))
        self.aero_namespace = aero_namespace
        self.aero_set = aero_set
        self.aero_config = {"hosts": [(self.aerospike_host, self.aerospike_port)]}
        self.aero_client = aerospike.client(self.aero_config)

    def __enter__(self):
        self.aero_client.connect()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.aero_client.close()

    def put_record(self, key, record: Dict, ttl):
        """
        Add or update a record

        key: the unique part of the Aerospike key of the record. This method takes care of prepending the namespace and set to the provided key
        record: a Dict with keys being the bin names and values being the bin values
        ttl: ttl to set for the record in Aerospike
        """
        self.aero_client.put(
            (self.aero_namespace, self.aero_set, key), record, {"ttl": ttl}
        )
