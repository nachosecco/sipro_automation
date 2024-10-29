import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test a placement that exists and check that is ok.
@pytest.mark.regression
def test_validated_media_alignment_for_managed_asset():
    case = Case("test_validated_media_alignment_for_managed_asset")

    vpc = case.vpc
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    vast_result.assertXML().assertDuration("00:00:30")

    # This would assert that is only one ad in the vast xml
    vast_xml_asserter = vast_result.assert_vast_xml()
    vast_xml_asserter.assert_ad_count(1)
    vast_xml_asserter.assert_creatives_is_url_in_media_server()
