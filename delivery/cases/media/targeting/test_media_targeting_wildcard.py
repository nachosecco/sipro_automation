import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description("""This tests URL paramter media targeting with wildcard""")
def test_media_targeting_wildcard():
    case = Case("test_media_targeting_wildcard")

    # URL Parameter media targeting rules content_genre=Yankees* content_series=Yankees*RedSox content_title=*Game1
    vpc = case.vpc

    # URL Parameter values matches wildcard targeting rules. An Ad will be served.
    vpc.content_genre = "YankeesGames"
    vpc.content_series = "YankeesVsRedsox"
    vpc.content_title = "YankeesVsRedsoxGame1"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(1)

    # URL parameter values don't match wildcard targeting rules. No Ad will be served.
    vpc.regenerate_automation_framework()
    vpc.content_genre = "HelloYankees"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)

    vpc.regenerate_automation_framework()
    vpc.content_genre = "YankeesGames"
    vpc.content_series = "YankeesVsWhitesox"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)

    vpc.regenerate_automation_framework()
    vpc.content_series = "YankeesVsRedsox"
    vpc.content_title = "YankeesVsRedsoxGame2"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)
