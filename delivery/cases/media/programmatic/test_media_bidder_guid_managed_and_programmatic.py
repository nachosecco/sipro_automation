from core.case import Case
from core.vastValidator import VastValidator
import logging
import pytest


@pytest.mark.regression
def call_delivery_framework_with_retry(retryCounter=0):
    case = Case(
        "test_media_bidder_guid_managed_and_programmatic"
    )  # This is the file to test this case
    vpc = case.vpc

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    xmlElement = vastResult.xmlRoot

    ads = xmlElement.findall("Ad")
    if len(ads) < 2 and retryCounter < 3:
        retryCounter = retryCounter + 1
        return call_delivery_framework_with_retry(retryCounter)
    return ads


# This would test a placement with managed media & programmatic
# media and check the trackers in impression for [bidder_guid] that should be in the programmatic demand
# and not in the managed media
@pytest.mark.regression
def test_media_bidder_guid_managed_and_programmatic():
    ads = call_delivery_framework_with_retry()
    if len(ads) < 2:
        logging.warn("It cannot be tested, is missing one ad")
        return

    adProgramatic = ads[0]
    adManaged = ads[1]

    # Using expected id(12345) for the programmatic demand
    if ads[1].get("id") == "12345":
        adProgramatic = ads[1]
        adManaged = ads[0]

    foundBidderGuidInProgrammaticWithValue = False

    for impression in adProgramatic.findall("./InLine/Impression"):
        if "bidder_guid" in impression.text:
            value = impression.text.split("bidder_guid")[1]

            foundBidderGuidInProgrammaticWithValue = len(value.strip()) > 0

    foundBidderGuidInManagedWithValue = False
    foundValueBidderGuidInManaged = ""
    for impression in adManaged.findall("./InLine/Impression"):
        if "bidder_guid" in impression.text:
            foundValueBidderGuidInManaged = impression.text.split("bidder_guid")[1]
            if len(foundValueBidderGuidInManaged) > 0:
                foundValueBidderGuidInManaged = foundValueBidderGuidInManaged[1:]
                foundValueBidderGuidInManaged = foundValueBidderGuidInManaged.replace(
                    "[", ""
                )
                foundValueBidderGuidInManaged = foundValueBidderGuidInManaged.replace(
                    "]", ""
                )

            foundBidderGuidInManagedWithValue = (
                len(foundValueBidderGuidInManaged.strip()) > 0
            )

    if not (foundBidderGuidInProgrammaticWithValue):
        logging.error(
            "Is expected that the bidder_guid to have a value in programmatic media"
        )
        assert False

    if foundBidderGuidInManagedWithValue:
        logging.error(
            "In the managed media the the bidder_guid it has to be empty but contains ["
            + foundValueBidderGuidInManaged
            + "] in the managed media"
        )
        assert False
