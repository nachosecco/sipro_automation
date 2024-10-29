import pytest
from core.case import Case
from core.Description import description
from core.validator.DisplayPlacementValidator import DisplayPlacementValidator


@pytest.mark.regression
@description(
    """Assert the suppressDisplayClickthrough field is False when the suppress clickthrough setting is disabled for a company"""
)
def test_display_suppress_clickthrough_inactive():
    case = Case("test_display_suppress_clickthrough_inactive")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    assert dpl_result.vJsonPlayerResponse["suppressDisplayClickthrough"] is False


@pytest.mark.regression
@description(
    """Assert the suppressDisplayClickthrough field is True when the suppress clickthrough setting is enabled for a company"""
)
def test_display_suppress_clickthrough_active():
    case = Case("test_display_suppress_clickthrough_active")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    assert dpl_result.vJsonPlayerResponse["suppressDisplayClickthrough"] is True
