import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason


@description(
    """
 This test case validates when appname in global blocklist media should get filtered.
 Configuration :-
                 Placement:-  ctv
                 Aligned Demand:- Count = 1
"""
)
@pytest.mark.regression
def test_placement_global_blocklist_appname():
    case = Case("test_placement_global_blocklist_appname")

    vpc = case.vpc

    vpc.app_name = "test_placement_global_blocklist_appname"
    vast_result = VastValidator().test(vpc)

    vast_result.assertFilter(FilterReason.APP_NAME_GLOBAL_BLOCKLIST)

    vast_result.assert_vast_xml().assert_ad_count(0)


@description(
    """
 This test case validates when app bundle id in global blocklist media should get filtered.
 Configuration :-
                  Placement:-  ctv
                  Aligned Demand:- Count = 1
"""
)
@pytest.mark.regression
def test_placement_global_blocklist_appbundle():
    case = Case("test_placement_global_blocklist_appbundle")

    vpc = case.vpc

    vpc.app_id = "test_placement_global_blocklist_appbundle"
    vast_result = VastValidator().test(vpc)

    vast_result.assertFilter(FilterReason.APP_BUNDLE_GLOBAL_BLOCKLIST)

    vast_result.assert_vast_xml().assert_ad_count(0)


@description(
    """
 This test case validates when domain(page_url) in global blocklist media should get filtered.
 Configuration :-
                Placement:-  instream
                Aligned Demand:- Count = 1
"""
)
@pytest.mark.regression
def test_placement_global_blocklist_domain():
    case = Case("test_placement_global_blocklist_domain")

    vpc = case.vpc

    vpc.page_url = "cyberblock.com"
    vast_result = VastValidator().test(vpc)

    vast_result.assertFilter(FilterReason.APP_DOMAIN_GLOBAL_BLOCKLIST)

    vast_result.assert_vast_xml().assert_ad_count(0)
