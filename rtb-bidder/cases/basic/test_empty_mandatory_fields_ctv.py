import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@description(
    """
    This test case is to validate that if mandatory field uid is not passed and app.id is passed as blank in bidrequest then error is thrown.
    It should throw 400 bad request
    It should throw error message "uid parameter or app.id is mandatory"
    """
)
@pytest.mark.regression
def test_empty_app_id():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile("")  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .send()
    )

    (rtb_response
     .is_bad_request()
     .has_error_message("uid parameter or app.id is mandatory")
     )


@description(
    """
    This test case is to validate that if mandatory field uid is passed as blank in bidrequest then error is thrown.
    It should throw 400 bad request
    It should throw error message "uid parameter or app.id is mandatory"
    """
)
@pytest.mark.regression
def test_empty_uid():
    rtb_response = (RtbRequestBuilder
                    # Automatically assigns the placement uid
                    .mobile("test")  # Mobile (app) bid request type builder
                    .set("uid", "")
                    .bid_floor(1)
                    .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
                    .url("rtb-test-app.com")
                    .bundle("rtb-test-app")
                    .name("rtb-test-app")
                    .send())

    (rtb_response
     .is_bad_request()
     .has_error_message("uid parameter or app.id is mandatory")
     )

