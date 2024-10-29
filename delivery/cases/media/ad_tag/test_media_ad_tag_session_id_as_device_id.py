import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import ComparisonType
from core.dto.cookie import UserCookie


@pytest.mark.regression
def test_media_ad_tag_session_id_generated_when_device_id_is_0():
    case = Case("test_media_ad_tag_session_id_as_device_id")
    vpc = case.vpc
    vpc.did = "00000000-0000-0000-0000-000000000000"
    vast_result_first = VastValidator().test(vpc)

    assert_cookie = vast_result_first.assertCookie()
    expected_cookie = UserCookie()
    expected_cookie.sessionUUID = "true"
    assert_cookie.assert_expected_user_cookies_in_logs(expected_cookie)
    expected_device_id = assert_cookie.get_device_id()

    # Validate the second request got the session id as device id
    vpc.regenerate_automation_framework()
    vast_result_second = VastValidator().test(vpc)
    assert_media_tags = vast_result_second.assertXML().assertMediaTags()
    assert_media_tags.ad_tag("device_id", expected_device_id, ComparisonType.Startswith)


@pytest.mark.regression
def test_media_ad_tag_session_id_not_generated_when_device_id_is_sent():
    case = Case("test_media_ad_tag_session_id_as_device_id")
    vpc = case.vpc
    vpc.did = "39f364d9-4d77-5a59-a429-0bf9e99b1a23"
    vast_result = VastValidator().test(vpc)
    assert_cookie = vast_result.assertCookie()

    expected_cookie = UserCookie()
    expected_cookie.sessionUUID = "false"
    assert_cookie.assert_expected_user_cookies_in_logs(expected_cookie)


@pytest.mark.regression
def test_media_ad_tag_session_id_is_generated_when_device_id_is_replace():
    case = Case("test_media_ad_tag_session_id_as_device_id")
    vpc = case.vpc
    vpc.did = "[REPLACE]"
    vast_result = VastValidator().test(vpc)
    assert_cookie = vast_result.assertCookie()

    expected_cookie = UserCookie()
    expected_cookie.sessionUUID = "true"
    assert_cookie.assert_expected_user_cookies_in_logs(expected_cookie)


@pytest.mark.regression
def test_media_ad_tag_when_session_id_then_liveramp_cookie_sync_url_is_removed():
    case = Case("test_media_ad_tag_session_id_as_device_id")
    vpc = case.vpc
    vpc.did = "[REPLACE]"
    vast_result = VastValidator().test(vpc)
    # using any of the many ways to create a sessionId, and we check livaram cookie sync is not sent
    vast_result.assertXML().assertTagImpressionNotContainsText(
        "http://idsync.rlcdn.com"
    )


@pytest.mark.regression
def test_media_ad_tag_when_session_id_then_bidder_cookie_sync_url_not_removed():
    case = Case("test_media_ad_tag_session_id_as_device_id")
    vpc = case.vpc
    vpc.did = "[REPLACE]"
    vast_result = VastValidator().test(vpc)
    # using one of the many ways to create a sessionId, and we check dsp cookie sync is sent
    # This case needs discussion: CP-2637
    # Added because is the current behavior
    vast_result.assertXML().assertTagImpressionContainsText("https://cookiesyncurl.net")
