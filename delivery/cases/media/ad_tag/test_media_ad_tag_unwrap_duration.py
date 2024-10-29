import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description("Test that unwrap for the duration for a vast tag is 30")
def test_media_ad_tag_unwrap_duration_ok():
    case = Case("test_media_ad_tag_unwrap_duration_ok")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    vast_result.assertLogsDelivery(["The duration is [30] for"])
