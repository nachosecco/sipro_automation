import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "In a placement that allows 2 winners and vpc is a apod size=2, it will have 2 ads winning in the vast"
)
def test_rtb_auction_2_winners():
    case = Case("test_rtb_auction_2_winners")
    vpc = case.vpc
    vpc.pod_size = "2"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 2, "There should be two bidders for the auction"

    vast_result.assert_vast_xml().assert_ad_count(2)


@pytest.mark.regression
@description(
    "In a placement that allows 2 winners and vpc is a apod duration=30, it will have 2 ads winning in the vast"
)
def test_rtb_auction_2_winners_adpod_duration():
    case = Case("test_rtb_auction_2_winners_adpod_duration")
    vpc = case.vpc
    vpc.pod_max_dur = "30"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 2, "There should be two bidders for the auction"

    vast_result.assert_vast_xml().assert_ad_count(2)
