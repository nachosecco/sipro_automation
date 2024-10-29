import logging
from urllib.parse import parse_qs
from urllib.parse import urlparse

import pytest

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder

TEST_URL = "rtb-test-app.com"

TEST_WITH_SPACES = "test with spaces"


@description(
    """
    Validate that if special chars are sent in a bid request, delivery request is still sent.
    It should not throw 500 error
    """
)
@pytest.mark.regression
def test_special_char_in_field_value_gets_url_encoded():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile("")  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("rtb-test-app.com")
        .bundle("rtb-test-app!=&#")
        .name("%%{appName}")
        .mimes(["{mimeType}"])
        .send()
    )

    rtb_response.is_not_server_error()


@pytest.mark.regression
def test_special_char_is_decoded_name_in_tag():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .bundle("required_value")
        .url(TEST_URL)
        .name(TEST_WITH_SPACES)
        .send()
    )

    rtb_response.is_not_server_error()

    vast_xml = rtb_response.validate_vast().vast_xml()

    ad_tag_element = vast_xml.find("./Ad/Wrapper/VASTAdTagURI")

    if ad_tag_element.text == "":
        logging.error("Ad tag is empty")
        assert False

    ad_tag = ad_tag_element.text
    tag_values = urlparse(ad_tag, allow_fragments=True)

    query_params = parse_qs(tag_values.query)

    app_name_in_vast_tag = query_params["app_name"][0]
    uri_in_vast_tag = query_params["uri"][0]

    if (
        not app_name_in_vast_tag == TEST_WITH_SPACES
        or not uri_in_vast_tag == uri_in_vast_tag
    ):
        logging.error("We have a encoding problem between rtb-bidder & delivery")
        assert False


def test_plus_char_is_encoded_and_accepted():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .bundle("required_value")
        .url(TEST_URL)
        .name(TEST_WITH_SPACES)
        .mimes(
            [
                "application/+dashxml",
                "application/qmx",
                "application/x-mpegURL",
                "application/x-mpegurl",
                "application/xml",
                "text/plain",
                "video/mov",
                "video/mp4",
            ]
        )
        .send()
    )

    rtb_response.is_ok()
    rtb_response.number_of_bids_is(1)
