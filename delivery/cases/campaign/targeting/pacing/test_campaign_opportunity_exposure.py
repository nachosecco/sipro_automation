import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason


@pytest.mark.regression
@description(
    "Asserting opportunity exposure of 50% of Campaign for a sample size of 10"
)
def test_campaign_targeting_pacing_opportunity_exposure():
    case = Case("test_campaign_targeting_pacing_opportunity_exposure")

    vpc = case.vpc

    counter = 0
    for i in range(10):
        vpc.regenerate_automation_framework()
        vast_result = VastValidator().test(vpc)

        if vast_result.validate_filter_reason(
            FilterReason.BLOCKED_EXPOSURE_THROTTLE
        ).is_filter_reason_found():
            counter += 1

    if counter < 3 or counter > 6:
        logging.error(
            f"The total number of blocked exposure ({counter}) is outside of the expected probability range of ~ 50% "
            "(we are using [3, 6] for a sample size of 10)."
        )
        assert False
