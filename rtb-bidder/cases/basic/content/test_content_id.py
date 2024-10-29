import logging

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder

EXPECTED_URL = "https://cdndev.altitude-arena.com/c6internaltestpage/test_vast_mp4.xml?content_id=CP-4715-test-id"


@description(
    """
	This test case is for sending any content id.
	The aligned media is an managed placement with the format to accept content id
	"""
)
def test_content_id():
    rtb_response = (
        RtbRequestBuilder.mobile()
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .content_id("CP-4715-test-id")
        .send()
    )

    vast_response = (
        rtb_response.is_ok()
        .number_of_bids_is(1)
        .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
        .ad_count_is(1)
        .vast_version_is("4.0")
        .vast_xml()
    )

    ads = vast_response.findall("Ad")
    tag_url = ads[0].find("./Wrapper/VASTAdTagURI").text

    if tag_url != EXPECTED_URL:
        logging.error(
            "we are expecting to see the the vast response the uri of [%s] but we got [%s]",
            EXPECTED_URL,
            tag_url,
        )
        assert False
