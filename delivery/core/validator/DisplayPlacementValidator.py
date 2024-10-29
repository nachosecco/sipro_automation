import json
import logging
import os
from urllib.parse import urlparse, parse_qs

import requests

from core.constants import AUTOMATION_FRAMEWORK_ID_DELIVERY
from core.utils.stringUtils import subStringBetween
from core.utils.urlutils import get_delivery_url
from core.validator.displayPlacementResultAssertor import DisplayPlacementResultAssertor
from core.vastXMLAssertor import VastResultAssertor
from core.vpc import VPC


def call_url_and_log(
    url: str,
    filePath: str,
    expectedStatusCode: int,
):
    logging.info("Testing the delivery url => " + url)
    response = requests.get(url)

    if not response.status_code == expectedStatusCode:
        logging.warning(
            "The status code of the request was " + str(response.status_code)
        )

    assert response.status_code == expectedStatusCode
    with open(filePath, "w") as f:
        f.write(response.text)
    return response


class DisplayPlacementValidator:
    def test(self, vpc: VPC, expectedStatusCode=200) -> VastResultAssertor:
        displayURL = vpc.display_url()
        self.directoryPathPlayerResponse = "build/case" + vpc._automationFramework + "/"
        os.makedirs(self.directoryPathPlayerResponse, exist_ok=True)

        logging.info("Testing id track ==> " + vpc._automationFramework)

        playerResponseFilePath = self.directoryPathPlayerResponse + "playerResponse.js"
        playerResponse = call_url_and_log(
            displayURL, playerResponseFilePath, expectedStatusCode
        )
        logging.info(playerResponse.text)
        vJson = json.loads(subStringBetween(playerResponse.text, "var v = ", ";"))

        dpl_url = f"{vJson.get('dplUrl')}&loc={get_delivery_url()}&id={vpc._automationFramework}&{AUTOMATION_FRAMEWORK_ID_DELIVERY}={vpc._automationFramework}"

        url_values = urlparse(dpl_url, allow_fragments=True)

        query_params = parse_qs(url_values.query)

        tid_in_url = query_params["tid"][0]

        dplResponseFilePath = self.directoryPathPlayerResponse + "dplResponse.js"
        dplResponse = call_url_and_log(dpl_url, dplResponseFilePath, expectedStatusCode)

        return DisplayPlacementResultAssertor(
            dplResponse,
            dplResponse.status_code,
            vpc,
            self.directoryPathPlayerResponse,
            vJson,
            tid_in_url,
        )
