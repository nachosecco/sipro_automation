import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description("Checking the ctv vast do not contains the rtb-meta-extension ")
def test_meta_rtb_not_present_in_ctv():
    case = Case("test_meta_rtb_not_present_in_ctv")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    if len(ads) == 0:
        logging.error("We are expecting at least 1 ad")
        assert False

    extensions = ads[0].findall("./InLine/Extensions/Extension")

    for extension in extensions:
        extension_type = extension.attr("type")
        if extension_type == "rtb-meta":
            logging.error(
                "we are expecting that the extension rtb-meta not to be present in this ctv placement"
            )
            assert False


@pytest.mark.regression
@description("Checking the instream vast do not contains the rtb-meta-extension ")
def test_meta_rtb_not_present_in_instream():
    case = Case("test_meta_rtb_not_present_in_instream")

    vpc = case.vpc

    vpc.page_url = "https://example.com"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    if len(ads) == 0:
        logging.error("We are expecting at least 1 ad")
        assert False

    extensions = ads[0].findall("./InLine/Extensions/Extension")

    for extension in extensions:
        extension_type = extension.attr("type")
        if extension_type == "rtb-meta":
            logging.error(
                "we are expecting that the extension rtb-meta not to be present in this intstream placement"
            )
            assert False
