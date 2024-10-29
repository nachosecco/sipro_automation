import logging

import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "This is a case of re-using a duration of a programmatic demand that was unwrapped "
)
def test_rtb_unwrapping_with_cache_ok():
    case = Case("test_rtb_unwrapping_with_cache_ok")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    expected_creative_id = "37980001"
    expected_duration = "15"

    # we are only assertion that the log contains buyer (guid is not available, in the logs until this moment)
    logs = []
    for log in vast_result.delivery_logs().logs:
        if (
            log.find(f"The duration is [{expected_duration}]") != -1
            and log.find(expected_creative_id) != -1
        ):
            logs.append(log)

    if len(logs) == 0:
        logging.error("The expected creative and duration didn't match ")
        assert False


@pytest.mark.regression
@description(
    "This test case is to validate using default duration when there is no duration found in the wrapper"
)
def test_ne_default_duration_when_wrapper_has_no_duration():

    case = Case("test_ne_default_duration_when_wrapper_has_no_duration")

    vpc = case.vpc
    vpc.pod_max_dur = "30"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    vast_result.assert_logs_delivery("Using default duration for media")
