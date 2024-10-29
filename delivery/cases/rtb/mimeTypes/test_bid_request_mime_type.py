import pytest

from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_bid_request_mime_type_mp4_default_values():
    """
    This test uses a video placement with a programmatic demand media aligned that will return at least 1 impression.
    Expected: given that we are not sending custom mime_types parameter to the tag request, bid request should contain default values
     "video/mp4", "video/3gpp", "video/webm"
    """
    case = Case("test_bid_request_mime_type_mp4")  # This is the file to test this case

    vpc = case.vpc
    vpc.page_url = "siprocal.com"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    vast_result.validate_rtb_bid_request().is_mimes_as_expected(
        ["video/mp4", "video/3gpp", "video/webm"]
    )


@pytest.mark.regression
def test_bid_request_mime_type_mp4_parameter_values():
    """
    This test uses a video placement with a programmatic demand media aligned that will return at least 1 impression.
    Expected: given that we are sending custom mime_types parameter to the tag request, bid request should contain the value being sent"""
    case = Case("test_bid_request_mime_type_mp4")  # This is the file to test this case

    vpc = case.vpc
    vpc.page_url = "siprocal.com"
    vpc.mime_types = "video/mp4"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    vast_result.validate_rtb_bid_request().is_mimes_as_expected(["video/mp4"])
