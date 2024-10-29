import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator

EXPECTED_URL = "https://cdndev.altitude-arena.com/c6internaltestpage/test_vast_mp4.xml?content_id=CP-4715-test-id"


@description("This would test that content id is in the delivery response")
@pytest.mark.regression
def test_content_id():
    case = Case("test_content_id")

    vpc = case.vpc
    vpc.content_id = "CP-4715-test-id"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)
    vast_response = vast_result.assert_vast_xml().root_element_xml
    ads = vast_response.findall("Ad")
    tag_url = ads[0].find("./Wrapper/VASTAdTagURI").text

    if tag_url != EXPECTED_URL:
        logging.error(
            "we are expecting to see the the vast response the uri of [%s] but we got [%s]",
            EXPECTED_URL,
            tag_url,
        )
        assert False
