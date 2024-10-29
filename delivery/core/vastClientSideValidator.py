import os
import logging
from core.templateGenerator import TemplateGeneratorVastClientParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


# This Is the class that holds the information of the result to the call to the client side, to get information related to the vast
class VastClientSideResult:
    def __init__(
        self,
        validVast: bool,
        trackEvents,
        pathToHTMLVastClientJS: str,
        impressions,
        clickUrls,
    ):
        self.validVast = validVast
        self.tracksEvents = trackEvents
        self.pathToHTMLVastClientJS = pathToHTMLVastClientJS
        self.impressions = impressions
        self.clickUrls = clickUrls


# This would execute on the client side a parse of the vast using
# WebDriver of chrome
#
class VastClientSideValidator:
    def __init__(self, vastXML: str, caseId: str):
        self.vastXML: str = vastXML
        self.caseId = caseId

    def execute(self) -> VastClientSideResult:
        pathToHTMLVastClientJS = TemplateGeneratorVastClientParser(
            self.caseId
        ).generate(self.vastXML)

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.set_capability("loggingPrefs", {"browser": "ALL"})

        chrome_driver_path = os.getenv(
            "CHROME_DRIVER_PATH", "/usr/local/bin/chromedriver"
        )

        service = ChromeService(chrome_driver_path)

        driver = webdriver.Chrome(
            service=service,
            options=options,
        )
        driver.get("file://" + pathToHTMLVastClientJS)

        vast_is_valid = True
        for entry in driver.get_log("browser"):
            if entry["level"] == "SEVERE":
                logging.error(
                    "There was a problem in the vast client side validation: "
                    + str(entry["message"])
                )
                vast_is_valid = False

        trackers = []
        clickUrls = []
        impressions = []
        try:
            dataJSTrackers = driver.execute_script("return trackerData || [];")
            for tracker in dataJSTrackers:
                trackers.append(tracker["trackingEvents"])
                for clickUrl in tracker["videoClickTrackingURLTemplates"]:
                    clickUrls.append(clickUrl)

            dataJSImpressions = driver.execute_script("return impressions || [];")
            for impression in dataJSImpressions:
                impressions.append(impression)
        except Exception as e:
            logging.warning(
                "The error "
                + str(e)
                + "There was a error looking the tracking/impressions"
            )

        driver.close()
        return VastClientSideResult(
            vast_is_valid, trackers, pathToHTMLVastClientJS, impressions, clickUrls
        )
