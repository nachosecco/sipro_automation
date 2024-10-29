import logging

from core.constants import ComparisonType
from core.utils.urlutils import extract_query_param
from core.utils.validationUtils import compare_values


class VastMediaTagValidator:
    def __init__(self, rootXML):
        self.root_element_xml = rootXML
        self.media_tag_url = None

    def ad_tag(
        self,
        param_name: str,
        param_value: str,
        comparison_type: ComparisonType = ComparisonType.Equality,
    ):
        logging.info("Validating  '%s' to have value '%s'", param_name, param_value)
        actual_value = self.__get_ad_tag_query_param(param_name)
        compare_values(actual_value.strip(), param_value, param_name, comparison_type)

    def __get_ad_tag_query_param(self, paramName: str):
        if self.media_tag_url is None:
            ads = self.root_element_xml.findall("Ad")
            for ad in ads:
                tag_uri = ad.find("./Wrapper/VASTAdTagURI")
                if tag_uri is None:
                    tag_uri = ad.find("./InLine/VASTAdTagURI")

                if tag_uri is None:  # go to another ad looking for media if not found
                    continue
                self.media_tag_url = tag_uri.text

        return extract_query_param(paramName, self.media_tag_url)
