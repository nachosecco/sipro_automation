import pytest

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder


@description(
    """
    Test eid parameter valued as byte array is sent to delivery.
    """
)
@pytest.mark.regression
def test_send_eid_parameter_from_bidder_service():
    json = [
        {
            "uids": [
                {
                    "id": "uid11",
                    "atype": "integer",
                    "ext": {
                    }
                },
                {
                    "id": "uid12",
                    "atype": "integer",
                    "ext": {
                    }
                },
                {
                    "id": "uid13",
                    "atype": "integer",
                    "ext": {
                    }
                }
            ],
            "source": "string",
            "ext": {
            }
        },
        {
            "uids": [
                {
                    "id": "uid21",
                    "atype": "integer",
                    "ext": {
                    }
                },
                {
                    "id": "uid22",
                    "atype": "integer",
                    "ext": {
                    }
                },
                {
                    "id": "uid23",
                    "atype": "integer",
                    "ext": {
                    }
                }
            ],
            "source": "string",
            "ext": {
            }
        }
    ]
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .eid(json)
        .send()
    )

    (
        rtb_response.is_ok()
            .number_of_bids_is(1)
            .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
            .ad_count_is(1)
    )
