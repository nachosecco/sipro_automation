import unittest
from core.ivt.ingest_ipv4_datafeed_job import IngestIPv4DataFeedJob

def test_loads_ipv4_data_to_redis():
	"""
	Given a IPv4 block list file
	After job execution
	The blocked ips should be present in the redis
	"""
	ip_address = "100.100.101.100"
	with IngestIPv4DataFeedJob() as test:
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
