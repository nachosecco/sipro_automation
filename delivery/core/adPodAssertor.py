import logging
import xml.etree.ElementTree as ET
from core.utils.dateUtils import dateUtils
from core.vpc import VPC


class adPod:
    """This class represent the expected values of a AdPod"""

    def __init__(self):
        self.pod_size = "0"
        """This represent how many ads in ad pod should be in the response"""
        self.ads_duration = "0"
        """This represent how long is the sum of ads in ad pod should be in the response"""
        self.max_ad_duration = "0"
        """This represent the max of a ad in the ad pod that could in the response"""
        self.min_ad_duration = "0"
        """This represent the min of a ad in the ad pod that could in the response"""
        self.first_media_id = ""
        """This represent the id that should have the first sequence in the response"""
        self.last_media_id = ""
        """This represent the id that should have the last sequence in the response"""
        self.ads_size_in_vast = "0"
        """This represent sum of all the ads that in the vast the response"""
        self.ads_size_not_in_adpod = "0"
        """This represent sum of all the ads that are not in ad pod"""

    def toString(self):
        description = "No values"
        if int(self.pod_size.strip() or 0) > 0:
            description = "pod_size :" + str(self.pod_size)

        if int(self.ads_duration.strip() or 0) > 0:
            description += " ads_duration :" + str(self.ads_duration)

        if int(self.max_ad_duration.strip() or 0) > 0:
            description += " max_ad_duration :" + str(self.max_ad_duration)

        if int(self.min_ad_duration.strip() or 0) > 0:
            description += " min_ad_duration :" + str(self.min_ad_duration)

        if len(self.first_media_id) > 0:
            description += " first_media_id :" + str(self.first_media_id)

        if len(self.last_media_id) > 0:
            description += " last_media_id :" + str(self.last_media_id)

        return description


class adPodAssertor:
    """This class represent the class that would assert the vast against the values of a AdPod"""

    def __init__(self, vastXML: ET, vpc: VPC):
        self.vastXML = vastXML
        self.vpc = vpc

    def isVastHasTheExpectedPod(self, expected_adpod: adPod):
        """Deprecated use does_vast_have_the_expected_pod"""
        return self.does_vast_have_the_expected_pod(expected_adpod)

    def does_vast_have_the_expected_pod(self, expected_adpod: adPod):
        """This would assert the values
        (ads_size,ads_duration,max_ad_duration,min_ad_duration,first_media_id,last_media_id)
        of the expected adPod to the found in the vast"""
        expected_adpod = self.__cleanAdPodValues(expected_adpod)
        found_vast_pod_values = self.__foundPodValues()
        expected = expected_adpod

        logging.info(
            "Expected values are "
            + expected_adpod.toString()
            + " and the found in the vast is "
            + found_vast_pod_values.toString()
            + " and the vpc input information is "
            + self.__messageAdPodFromVPC()
        )

        expected_pod_size = int(expected.pod_size.strip()) or 0
        found_vast_pod_size = int(found_vast_pod_values.pod_size or 0)

        if expected_pod_size > 0 and expected_pod_size != found_vast_pod_size:
            logging.error(
                f"Targeting adPod the expected pod_size[{expected_pod_size}] "
                f"are not equal of the vast response[{found_vast_pod_values}]"
            )
            return False

        if int(expected.ads_duration.strip() or 0) > 0 and int(
            expected.ads_duration
        ) != int(found_vast_pod_values.ads_duration or 0):
            logging.error(
                "Targeting geo the expected ads_duration("
                + str(int(expected.ads_duration.strip() or 0))
                + ") are not equal of the vast response("
                + str(int(found_vast_pod_values.ads_duration or 0))
                + ")"
            )
            return False

        if int(expected.max_ad_duration.strip() or 0) > 0 and int(
            expected.max_ad_duration
        ) != int(found_vast_pod_values.max_ad_duration or 0):
            logging.error(
                "Targeting geo the expected ads_duration("
                + str(int(expected.max_ad_duration.strip() or 0))
                + ") are not equal of the vast response("
                + str(int(found_vast_pod_values.max_ad_duration or 0))
                + ")"
            )
            return False

        if int(expected.min_ad_duration.strip() or 0) > 0 and int(
            expected.min_ad_duration
        ) != int(found_vast_pod_values.min_ad_duration or 0):
            logging.error(
                "Targeting geo the expected ads_duration("
                + str(int(expected.min_ad_duration.strip() or 0))
                + ") are not equal of the vast response("
                + str(int(found_vast_pod_values.min_ad_duration or 0))
                + ")"
            )
            return False
        if (
            len(expected.first_media_id) > 0
            and expected.first_media_id != found_vast_pod_values.first_media_id
        ):
            logging.error(
                f"Targeting adPod the expected first_media_id[{expected.first_media_id}] "
                f" are not equal of the vast response[{found_vast_pod_values.first_media_id}]"
            )
            return False

        if (
            len(expected.last_media_id) > 0
            and expected.last_media_id != found_vast_pod_values.last_media_id
        ):
            logging.error(
                f"Targeting adPod the expected last_media_id[{expected.last_media_id}] "
                f"are not equal of the vast response[{found_vast_pod_values.last_media_id}]"
            )
            return False

        return True

    def __cleanAdPodValues(self, expectedAdpod: adPod):
        if isinstance(expectedAdpod.pod_size, int):
            expectedAdpod.pod_size = str(expectedAdpod.pod_size)

        if isinstance(expectedAdpod.ads_duration, int):
            expectedAdpod.ads_duration = str(expectedAdpod.ads_duration)

        if isinstance(expectedAdpod.ads_size_in_vast, int):
            expectedAdpod.ads_size_in_vast = str(expectedAdpod.ads_size_in_vast)

        if isinstance(expectedAdpod.max_ad_duration, int):
            expectedAdpod.max_ad_duration = str(expectedAdpod.max_ad_duration)

        if isinstance(expectedAdpod.min_ad_duration, int):
            expectedAdpod.min_ad_duration = str(expectedAdpod.min_ad_duration)

        return expectedAdpod

    def __messageAdPodFromVPC(self):
        description = ""
        vpc = self.vpc
        if vpc.pod_size != "[REPLACE]":
            description += "pod_size=" + vpc.pod_size

        if vpc.pod_max_dur != "[REPLACE]":
            description += " pod_max_dur=" + vpc.pod_max_dur

        if vpc.pod_min_ad_dur != "[REPLACE]":
            description += " pod_min_ad_dur=" + vpc.pod_min_ad_dur

        if vpc.pod_max_ad_dur != "[REPLACE]":
            description += " pod_max_ad_dur=" + vpc.pod_max_ad_dur

        if len(description) == 0:
            return "No values for input in the VPC"

        return description.strip()

    def __foundPodValues(self):
        foundVastPodValues = adPod()
        ads = self.vastXML.findall("./Ad")
        lastSequence = 0
        pod_size = 0
        ads_duration = 0
        for ad in ads:
            if "sequence" in ad.attrib:  ##if has a sequence is in the adpod
                sequence = int(ad.attrib["sequence"])
                if sequence == 1:
                    foundVastPodValues.first_media_id = ad.attrib["id"]
                if sequence > lastSequence:
                    foundVastPodValues.last_media_id = ad.attrib["id"]
                pod_size += 1
                durationVast = ad.find("./InLine/Creatives/Creative/Linear/Duration")
                if durationVast is None:
                    durationVast = ad.find(
                        "./Wrapper/Creatives/Creative/Linear/Duration"
                    )
                if durationVast is not None:
                    duration = dateUtils().toSeconds(durationVast.text)
                    ads_duration += duration
                    if (
                        int(foundVastPodValues.min_ad_duration) == 0
                        or int(foundVastPodValues.min_ad_duration) > duration
                    ):
                        foundVastPodValues.min_ad_duration = str(duration)
                    if int(foundVastPodValues.max_ad_duration) < duration:
                        foundVastPodValues.max_ad_duration = str(duration)
        foundVastPodValues.pod_size = str(pod_size)
        foundVastPodValues.ads_duration = str(ads_duration)
        foundVastPodValues.ads_size_in_vast = str(len(ads))
        foundVastPodValues.ads_size_not_in_adpod = str(len(ads) - pod_size)
        self.foundVastPodValues = foundVastPodValues
        return foundVastPodValues
