import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description(
    "This is will test single media return by campaign"
    " all media will have back-fill priority/weight and same cpm"
    " it will execute 50 times and compare results of tags to know if is between expected numbers"
)
@pytest.mark.regression
def test_campaign_return_single_media():
    case = Case("test_campaign_return_single_media")

    vpc = case.vpc
    executions = range(50)
    found_tags = {}
    for execution in executions:
        vpc.regenerate_automation_framework()

        vast_result = VastValidator().test(vpc)

        vast_result.assert_vast_xml().assert_ad_count(1)

        ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

        for ad in ads:
            tag_url = ad.find("./Wrapper/VASTAdTagURI")

            logging.debug(f"For the execution {execution} it got {tag_url.text}")
            tag_executed = found_tags.get(tag_url.text, 0) + 1
            found_tags[tag_url.text] = tag_executed

    logging.info(f"Executed by tags\n {found_tags}")
    for v in found_tags.values():
        if v < 10 or v > 30:
            logging.error(
                "The tags values %s are are not between the expected targets (>=10 & <=30"
                "The config of the media are all back-fill so it should be somewhat similar",
                found_tags.values(),
            )
            assert False
