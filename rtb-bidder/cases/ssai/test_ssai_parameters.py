import pytest

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder


@description(
    """
    Test ssai parameter valued as 3 is sent to delivery.
    """
)
@pytest.mark.regression
def test_send_ssai_parameter_from_bidder_service():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .ssai(3)
        .send()
    )

    (
        rtb_response.is_ok()
            .number_of_bids_is(1)
            .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
            .ad_count_is(1)
    )
