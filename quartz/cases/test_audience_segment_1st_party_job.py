import unittest
import pytest
from core.audience_segment_1st_party_job import (
    AudienceSegment1stPartyJob,
    get_segment_filename,
    DEFAULT_AERO_SEGMENT_BIN,
)


def test_loads_1st_party_device_segments_to_aerospike():
    """
    Given a 1st party device segments file
    After job execution
    The segments should be present in the Aerospike 1st party bin
    """
    with AudienceSegment1stPartyJob() as test:
        devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["1111111111", "2222222222"],
            }
        ]
        test.add_1st_party_device_file(devices)
        test.execute()

        device_segments_list = test.get_1st_party_device_segments_as_list(
            "9595171f-6ce6-30c8-de55-b6025d826985"
        )
        # Same elements in the same number, regardless of order
        unittest.TestCase().assertCountEqual(
            devices[0]["segments"], device_segments_list
        )


def test_supports_duplicate_1st_party_device_segments_within_same_file():
    """
    Given a 1st party device segment file with the same device id present twice
    After job execution
    The segments from both entries should be present in the Aerospike 1st party bin
    """
    with AudienceSegment1stPartyJob() as test:
        devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["1111111111", "2222222222"],
            },
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["3333333333", "4444444444"],
            },
        ]

        test.add_1st_party_device_file(devices)
        test.execute()

        device_segments_list = test.get_1st_party_device_segments_as_list(
            "9595171f-6ce6-30c8-de55-b6025d826985"
        )
        expected_segments = ["1111111111", "2222222222", "3333333333", "4444444444"]
        unittest.TestCase().assertCountEqual(expected_segments, device_segments_list)


def test_supports_duplicate_1st_party_device_segments_across_files():
    """
    Given two 1st party device segment files with the same device id in both
    After job execution
    The segments from both files should be present in the Aerospike 1st party bin
    """
    with AudienceSegment1stPartyJob() as test:
        file_1_devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["1111111111", "2222222222"],
            }
        ]
        file_2_devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["3333333333", "4444444444"],
            }
        ]

        test.add_1st_party_device_file(file_1_devices)
        test.add_1st_party_device_file(file_2_devices)
        test.execute()

        device_segments_list = test.get_1st_party_device_segments_as_list(
            "9595171f-6ce6-30c8-de55-b6025d826985"
        )
        expected_segments = ["1111111111", "2222222222", "3333333333", "4444444444"]
        unittest.TestCase().assertCountEqual(expected_segments, device_segments_list)


def test_appends_new_1st_party_device_segments_to_existing():
    """
    Given a 1st party device segments file with a device id that already exists in Aerospike
    After job execution
    Both the existing and new segments should be present in the Aerospike 1st party bin
    """
    with AudienceSegment1stPartyJob() as test_1:
        file_1_devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["1111111111", "2222222222"],
            }
        ]
        test_1.add_1st_party_device_file(file_1_devices)
        test_1.execute()

        with AudienceSegment1stPartyJob() as test_2:
            file_2_devices = [
                {
                    "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                    "segments": ["3333333333", "4444444444"],
                }
            ]
            test_2.add_1st_party_device_file(file_2_devices)
            # Skip clean to leave records loaded by test_1
            test_2.execute(skip_aerospike_clean=True)

            device_segments_list = test_2.get_1st_party_device_segments_as_list(
                "9595171f-6ce6-30c8-de55-b6025d826985"
            )
            expected_segments = ["1111111111", "2222222222", "3333333333", "4444444444"]

            unittest.TestCase().assertCountEqual(
                expected_segments, device_segments_list
            )


def test_loads_1st_party_cookie_segments_to_aerospike():
    """
    Given a 1st party cookie segments file
    After job execution
    The segments should be present in the Aerospike 1st party bin
    """
    with AudienceSegment1stPartyJob() as test:
        cookies = [
            {
                "id": "9D80DO9TTO8UR8FOB5608G5ARO",
                "segments": ["1111111111", "2222222222"],
            }
        ]
        test.add_1st_party_cookie_file(cookies)
        test.execute()

        cookie_segments_list = test.get_1st_party_cookie_segments_as_list(
            "9D80DO9TTO8UR8FOB5608G5ARO"
        )
        # Same elements in the same number, regardless of order
        unittest.TestCase().assertCountEqual(
            cookies[0]["segments"], cookie_segments_list
        )


def test_multiple_data_distributions_are_added_to_aerospike():
    """
    Given that we have deleted data distributions, we should not attempt to load them
    After job execution
    We should not find any bins for deleted data distributions
    """
    with AudienceSegment1stPartyJob() as test:
        # Prepare the job with a deleted data distribution
        test.set_additional_data_distributions(
            [
                {
                    "default_name": "another_data_distribution",
                    "display_name": "Another Data Distribution",
                    "status": "active",
                    "aerospike_bin_name": "another_dd_bin",
                    "segment_filename_prefix": "another_data_distribution",
                }
            ]
        )
        devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["1111111111", "2222222222"],
            }
        ]
        # Add the device file for our default data distribution
        test.add_1st_party_device_file(devices)
        # Add the device file for our deleted data distribution
        test.add_1st_party_device_file_with_prefix(devices, "another_data_distribution")
        test.execute()
        bins = test.get_bins_for_device_id("9595171f-6ce6-30c8-de55-b6025d826985")
        assert bins[DEFAULT_AERO_SEGMENT_BIN] == ["1111111111", "2222222222"]
        assert bins["another_dd_bin"] == ["1111111111", "2222222222"]


def test_deleted_data_distributions_are_excluded_from_job():
    """
    Given that we have deleted data distributions, we should not attempt to load them
    After job execution
    We should not find any bins for deleted data distributions
    """
    with AudienceSegment1stPartyJob() as test:
        # Prepare the job with a deleted data distribution
        test.set_additional_data_distributions(
            [
                {
                    "default_name": "another_data_distribution",
                    "display_name": "Another Data Distribution",
                    "status": "deleted",
                    "aerospike_bin_name": "another_dd_bin",
                    "segment_filename_prefix": "another_data_distribution",
                }
            ]
        )
        devices = [
            {
                "id": "9595171f-6ce6-30c8-de55-b6025d826985",
                "segments": ["1111111111", "2222222222"],
            }
        ]
        # Add the device file for our default data distribution
        test.add_1st_party_device_file(devices)
        # Add the device file for our deleted data distribution
        test.add_1st_party_device_file_with_prefix(devices, "another_data_distribution")
        test.execute()
        bins = test.get_bins_for_device_id("9595171f-6ce6-30c8-de55-b6025d826985")
        assert "another_dd_bin" not in bins
