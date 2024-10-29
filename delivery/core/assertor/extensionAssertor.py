import logging
from typing import List


class ExpectedCategory:
    """Represents a category that is expected to be in the extesion of an ad."""

    def __init__(self, category):
        self.category: List[str] = category


class AdExtensionAsserter:
    def __init__(self, xml_root):
        self.xmlRoot = xml_root
        self.ads = self.xmlRoot.findall("Ad")

    def assert_price_are(self, expected_prices):
        """Asserts that the ads being returned contains an extension of type price having values expected_price."""
        valid = len(expected_prices) == len(self.ads)
        if not valid:
            logging.error(
                "The number of expected prices does not match the number of ads"
            )
        assert valid

        index = 0
        for ad in self.ads:
            extension = get_extension_by_type(ad, "SiprocalPrice", None)
            expected_price = expected_prices[index]
            valid = extension is not None and extension.text == str(expected_price)
            if not valid:
                logging.error(
                    f"The expected value is [{expected_price}] and the actual value is [{extension.text}]"
                )
            assert valid
            index = index + 1

    def assert_categories_are(self, expected_categories: List[ExpectedCategory]):
        """Asserts that the ads being returned contains an extension of type category having values
        expected_categories by each ad."""
        valid = len(expected_categories) == len(self.ads)
        if not valid:
            logging.error(
                "The number of expected categories does not match the number of ads"
            )
        assert valid

        index = 0
        for ad in self.ads:
            extension = get_extension_by_type(ad, "SiprocalCategory", "")
            if extension is None:
                logging.error("The extension SiprocalCategory is not found")
                assert False

            expected_categories_ad = expected_categories[index].category
            expected_categories_ad.sort()
            categories_in_vast = []
            categories_in_vast_tag = extension.findall(".Category")
            for category in categories_in_vast_tag:
                categories_in_vast.append(category.text)
            categories_in_vast.sort()

            valid = categories_in_vast == expected_categories_ad

            if not valid:
                logging.error(
                    f"The expected categories are [{expected_categories_ad}] "
                    f"and the actual value is [{categories_in_vast}]"
                )
            assert valid
            index = index + 1

    def assert_adomain(self, index, expected_adomain):
        domain_path = "/Adomain[" + str(index) + "]"
        self.__assert_extension(expected_adomain, "SiprocalAdomain", domain_path)

    def assert_noAdomain(self):
        self.__assert_extension(None, "SiprocalAdomain", None)

    def __assert_extension(self, expected_value, type, custom_xml_path):
        assert len(self.ads) > 0
        for ad in self.ads:
            extension = get_extension_by_type(ad, type, custom_xml_path)
            if expected_value is None:
                assert extension is None
            else:
                valid = extension is not None and extension.text == str(expected_value)
                if not valid:
                    logging.error(
                        f"The expected value is [{expected_value}] and the actual value is [{extension.text}]"
                    )
                assert valid


def get_extension_by_type(ad, extension_type, custom_xml_path):
    """Returns the extension that has its type attribute equals to extension_type
    or all extensions if extension_type is blank."""
    ad_child = ad.find("./InLine") or ad.find("./Wrapper")
    if ad_child is None:
        return None
    if len(extension_type) == 0:
        return ad.findall("./Extensions")

    custom_xml_path = custom_xml_path or ""
    return ad_child.find(
        f"./Extensions/Extension/[@type='{extension_type}']{custom_xml_path}"
    )
