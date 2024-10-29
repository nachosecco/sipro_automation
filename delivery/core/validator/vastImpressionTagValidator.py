import logging
from core.utils.validationUtils import compare_values
from core.constants import ComparisonType
from core.utils.urlutils import extract_query_param
from urllib.parse import urlparse


class VastImpressionTagValidator:
    def __init__(self, root_xml, tracker_hostname: str):
        self.root_element_xml = root_xml
        self.tracker_url_hostname = tracker_hostname
        self.tracker_url_found = None

    def ad_tag(
        self,
        param_name: str,
        param_value: str,
        comparison_type: ComparisonType = ComparisonType.Equality,
    ):
        logging.debug("Validating  '%s' to have value '%s'", param_name, param_value)
        actual_value = self.__get_ad_tag_query_param(param_name)
        compare_values(actual_value.strip(), param_value, param_name, comparison_type)

    def __get_ad_tag_query_param(self, param_name: str):
        if self.tracker_url_found is None:
            ads = self.root_element_xml.findall("Ad")
            for ad in ads:
                impressions = ad.findall("./InLine/Impression")
                if len(impressions) == 0:
                    impressions = ad.findall("./Wrapper/Impression")

                for impression in impressions:
                    if urlparse(impression.text).hostname == self.tracker_url_hostname:
                        self.tracker_url_found = impression.text
                        break

        return extract_query_param(param_name, self.tracker_url_found)
