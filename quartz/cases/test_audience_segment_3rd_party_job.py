import pytest
import unittest
from core.audience_segment_3rd_party_job  import AudienceSegment3rdPartyJob


def test_loads_lr_device_segments_to_aerospike():
	with AudienceSegment3rdPartyJob() as test:
		devices = [
			{
				"id": "9595171f-6ce6-30c8-de55-b6025d826985",
				"segments": ["1111111111", "2222222222"]
			}
		]
		test.add_lr_device_file(devices)
		test.execute()

		lr_device_segments_list = test.get_lr_device_segments_as_list("9595171f-6ce6-30c8-de55-b6025d826985")
		# Same elements in the same number, regardless of order
		unittest.TestCase().assertCountEqual(devices[0]['segments'], lr_device_segments_list)


def test_supports_duplicate_lr_device_segments_within_same_file():
	with AudienceSegment3rdPartyJob() as test:
		devices = [
			{
				"id": "9595171f-6ce6-30c8-de55-b6025d826985",
				"segments": ["1111111111", "2222222222"]
			},
			{
				"id": "9595171f-6ce6-30c8-de55-b6025d826985",
				"segments": ["3333333333", "4444444444"]
			}
		]

		test.add_lr_device_file(devices)
		test.execute()

		lr_device_segments_list = test.get_lr_device_segments_as_list("9595171f-6ce6-30c8-de55-b6025d826985")
		expected_segments = ["1111111111", "2222222222", "3333333333", "4444444444"]
		unittest.TestCase().assertCountEqual(expected_segments, lr_device_segments_list)


def test_supports_duplicate_lr_device_segments_across_files():
	with AudienceSegment3rdPartyJob() as test:
		file_1_devices = [
			{
				"id": "9595171f-6ce6-30c8-de55-b6025d826985",
				"segments": ["1111111111", "2222222222"]
			}
		]
		file_2_devices = [
			{
				"id": "9595171f-6ce6-30c8-de55-b6025d826985",
				"segments": ["3333333333", "4444444444"]
			}
		]

		test.add_lr_device_file(file_1_devices)
		test.add_lr_device_file(file_2_devices)
		test.execute()

		lr_device_segments_list = test.get_lr_device_segments_as_list("9595171f-6ce6-30c8-de55-b6025d826985")
		expected_segments = ["1111111111", "2222222222", "3333333333", "4444444444"]
		unittest.TestCase().assertCountEqual(expected_segments, lr_device_segments_list)


def test_appends_new_lr_device_segments_to_existing():
	with AudienceSegment3rdPartyJob() as test_1:
		file_1_devices = [
			{
				"id": "9595171f-6ce6-30c8-de55-b6025d826985",
				"segments": ["1111111111", "2222222222"]
			}
		]
		test_1.add_lr_device_file(file_1_devices)
		test_1.execute()

		with AudienceSegment3rdPartyJob() as test_2:
			file_2_devices = [
				{
					"id": "9595171f-6ce6-30c8-de55-b6025d826985",
					"segments": ["3333333333", "4444444444"]
				}
			]
			test_2.add_lr_device_file(file_2_devices)
			# Skip clean to leave records loaded by test_1
			test_2.execute(skip_aerospike_clean=True)

			lr_device_segments_list = test_2.get_lr_device_segments_as_list("9595171f-6ce6-30c8-de55-b6025d826985")
			expected_segments = ["1111111111", "2222222222", "3333333333", "4444444444"]

			unittest.TestCase().assertCountEqual(expected_segments, lr_device_segments_list)


def test_loads_lr_cookie_segments_to_aerospike():
	with AudienceSegment3rdPartyJob() as test:
		cookies = [
			{
				"id": "9D80DO9TTO8UR8FOB5608G5ARO",
				"segments": ["1111111111", "2222222222"]
			}
		]
		test.add_lr_cookie_file(cookies)
		test.execute()

		lr_cookie_segments_list = test.get_lr_cookie_segments_as_list("9D80DO9TTO8UR8FOB5608G5ARO")
		# Same elements in the same number, regardless of order
		unittest.TestCase().assertCountEqual(cookies[0]['segments'], lr_cookie_segments_list)
