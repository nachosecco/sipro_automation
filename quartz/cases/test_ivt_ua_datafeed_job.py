import unittest
from core.ivt.ingest_ua_datafeed_job import IngestUADatafeedJob


def test_loads_ua_data_to_redis():
	"""
	Given a UA block list file
	After job execution
	The blocked ips should be present in the redis
	"""
	user_agent = "Mozilla/5.0 (compatible; Yahoo Ad monitoring;)  tands-prod-eng.hlfs-prod---sieve.hlfs-desktop/1613274029-0"
	with IngestUADatafeedJob() as test:
		records = [
			{
				"line": user_agent
			}
		]
		test.add_file(records)
		test.execute()
		# Search for record with valid key and element is found
		# Confirms key is created using ip value
		value = test.get_record_by_key(user_agent)
		unittest.TestCase().assertIsNotNone(value)
