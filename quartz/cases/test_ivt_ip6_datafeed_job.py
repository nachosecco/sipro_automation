import unittest
from core.ivt.ingest_ipv6_datafeed_job import IngestIPv6DataFeedJob


def test_loads_ipv6_data_to_redis():
	"""
	Given a IPv6 block list file
	After job execution
	The blocked ips should be present in the redis
	"""
	ip_address = "2600:8805:2000:750:3196:329a:e166:a147"
	with IngestIPv6DataFeedJob() as test:
		records = [
			{
				"ip": ip_address,
				"fraudType": "sample"
			}
		]
		test.add_file(records)
		test.execute()

		# Search for record with invalid key and it's not found
		value = test.get_record_by_key("sample")
		unittest.TestCase().assertIsNone(value)

		# Search for record with valid key and element is found
		# Confirms key is created using ip value
		value = test.get_record_by_key(ip_address)
		unittest.TestCase().assertIsNotNone(value)
