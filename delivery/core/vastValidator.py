import os
import requests
import logging
import xml.etree.ElementTree as ET

from core.vastClientSideValidator import VastClientSideResult, VastClientSideValidator
from core.vastXMLAssertor import VastResultAssertor
from core.vpc import VPC
from core.configuration import Configuration


# Call the vpc controller & checks:
# that the status is the expected value (200)
# then use a client side parse to validate to check the vast is valid
# return a VastResultAssertor to do assertions more related to the case of the test
class VastValidator:
    def test(
        self, vpc: VPC, expectedStatusCode=200, configOverride: Configuration = None
    ) -> VastResultAssertor:
        vpcURL = vpc.url()
        self.vpc = vpc
        self.directoryPathVastResponse = (
            "build/case" + self.vpc._automationFramework + "/"
        )
        logging.info("Testing id track ==> " + vpc._automationFramework)

        logging.info("Testing the delivery url => " + vpcURL)
        vastResponse = requests.get(vpcURL)
        headers = vastResponse.headers

        # always check that the status code is the expected one.
        if not vastResponse.status_code == expectedStatusCode:
            logging.warning(
                "The status code of the request was " + str(vastResponse.status_code)
            )

        assert vastResponse.status_code == expectedStatusCode

        if not vastResponse.ok:
            return VastResultAssertor(
                None,
                vastResponse.status_code,
                self.vpc,
                self.directoryPathVastResponse,
                headers,
                configOverride,
            )

        directoryPathVastResponse = "build/case" + vpc._automationFramework + "/"
        os.makedirs(directoryPathVastResponse, exist_ok=True)

        with open(directoryPathVastResponse + "vastResponse.xml", "w") as f:
            f.write(vastResponse.text)
        vastParseResponse = ET.parse(directoryPathVastResponse + "vastResponse.xml")

        # always check that is a valid vast
        resultClient = VastClientSideValidator(
            vastResponse.text, vpc._automationFramework
        ).execute()
        assert resultClient.validVast

        # Calling to each event of tracking
        self.__callToEvents(resultClient)
        self.__callToImpressions(resultClient.impressions)
        self.__callToClickEvents(resultClient.clickUrls, configOverride)

        return VastResultAssertor(
            vastParseResponse,
            vastResponse.status_code,
            self.vpc,
            self.directoryPathVastResponse,
            headers,
            configOverride,
        )

    def __callToEvents(self, vastClientSide: VastClientSideResult):
        for tracker in vastClientSide.tracksEvents:
            self.__callToEvent(tracker["start"][0], "start")
            self.__callToEvent(tracker["firstQuartile"][0], "firstQuartile")
            self.__callToEvent(tracker["midpoint"][0], "midpoint")
            self.__callToEvent(tracker["thirdQuartile"][0], "thirdQuartile")
            self.__callToEvent(tracker["complete"][0], "complete")

    def __callToImpressions(self, impressions):
        for impression in impressions:
            if "rollimp" in impression["url"]:
                self.__callToEvent(impression["url"], "rollimp")

    def __callToClickEvents(self, clickUrls, config: Configuration):
        for clickUrl in clickUrls:
            self.__callToEvent(clickUrl["url"], "rollck")
            # called twice as logs were not getting pushed to elastic search.
            if config and config.read_event_logs:
                self.__callToEvent(clickUrl["url"], "rollck")

    def __callToEvent(self, track, name):
        track += (
            "&automationFrameworkEvent" + name + "=" + self.vpc._automationFramework
        )
        logging.debug("The  " + name + " event  has the url => " + track)
        response_event = requests.get(track)
        if not response_event.ok:
            logging.error(
                f"The event [{name}] was not ok: {track} and have a status code of [{response_event.status_code}]"
            )
        assert response_event.ok
