import json
import logging
import socket

from core.constants import REPLACE
from core.validator.rtb_auction_validator import RtbAuctionValidator


class RtbBidRequestValidator:
    """Class to do validations of the rtb request"""

    def __init__(self, deliver_log):
        self.__auction_validator = RtbAuctionValidator(deliver_log)
        self.bidder_name = self.__auction_validator.bidder_name
        self.placement_type = self.__auction_validator.placement_type
        self.rtb_version = self.__auction_validator.rtb_version
        self.bid_request = self.__auction_validator.bid_request
        self.bidders = self.__auction_validator.bidders

    def is_bidder_name_as_expected(self, expected_bidder_name):
        equal_name = self.bidder_name == expected_bidder_name
        if not equal_name:
            logging.error(
                f"The expected name [{expected_bidder_name}] is not equal to [{self.bidder_name}]"
            )
        return equal_name

    def is_placement_type_as_expected(self, expected_placement_type):
        return self.placement_type == expected_placement_type

    def is_rtb_version_as_expected(self, expected_rtb_version):
        return self.rtb_version == expected_rtb_version

    def is_required_properties_valid(self):
        assert isinstance(self.bid_request["id"], str)
        impressions = self.bid_request["imp"]
        assert impressions is not None and len(impressions) > 0
        impression = impressions[0]
        assert isinstance(impression["id"], str)

        return True

    def is_video_object_valid(self):
        impressions = self.bid_request["imp"]
        assert impressions is not None and len(impressions) > 0
        impression = impressions[0]
        video = impression["video"]
        assert video is not None
        mimes = video["mimes"]
        assert len(mimes) > 0
        for mime in mimes:
            assert mime[0:6] == "video/"
        min_duration = video["minduration"]
        assert isinstance(min_duration, int)
        max_duration = video["maxduration"]
        assert isinstance(max_duration, int)
        assert min_duration <= max_duration

        return True

    def is_app_object_valid(self):
        app = self.bid_request["app"]
        assert app is not None
        assert isinstance(app["id"], str)

        return True

    def is_device_object_as_expected(self, expected_device, no_validation=False):
        device = self.bid_request.get("device", None)
        assert device is not None

        if no_validation:
            return device == expected_device

        # Replace ua, ip and ifa which change for each test run
        assert isinstance(device["ua"], str)
        expected_device["ua"] = device["ua"]

        # Check if IP address is valid
        socket.inet_aton(device["ip"])
        expected_device["ip"] = device["ip"]

        # Check ifa
        assert isinstance(device["ifa"], str)
        expected_device["ifa"] = device["ifa"]

        return device == expected_device

    def is_user_as_expected(self, expected_user):
        user = self.bid_request.get("user", None)
        assert user is not None
        return user == expected_user

    def is_app_object_as_expected(self, case_name):
        expected_app = (
            self.__get_expected_app_object_rtb26(case_name)
            if self.rtb_version == "2.6"
            else self.__get_expected_app_object_common(case_name)
        )
        app = self.bid_request.get("app", None)
        assert app is not None
        expected_app["id"] = app["id"]
        expected_app["publisher"]["id"] = app["publisher"]["id"]
        equal = app == expected_app
        if not equal:
            logging.error(
                f"The expected app \n {expected_app}  \n is not equal to \n {app}"
            )
        return equal

    @staticmethod
    def __get_expected_app_object_common(case_name):
        return {
            "id": "REPLACE",
            "name": "[REPLACE]",
            "sectioncat": [],
            "pagecat": [],
            "ver": "[REPLACE]",
            "bundle": "[REPLACE]",
            "publisher": {
                "id": "REPLACE",
                "name": case_name,
                "domain": "",
            },
            "content": {
                "title": "[REPLACE]",
                "series": "[REPLACE]",
                "genre": "[REPLACE]",
                "language": "[REPLACE]",
            },
            "keywords": "",
        }

    def __get_expected_app_object_rtb26(self, case_name):
        expected_app = self.__get_expected_app_object_common(case_name)
        expected_app["content"]["network"] = {"name": REPLACE}
        expected_app["content"]["channel"] = {"name": REPLACE}
        return expected_app

    def is_imp_object_as_expected(self, expected_imp):
        imp = self.bid_request.get("imp", None)
        assert imp is not None
        assert len(imp) == 1
        assert len(expected_imp) == 1
        expected_imp[0]["id"] = imp[0]["id"]
        expected_imp[0]["tagid"] = imp[0]["tagid"]
        logging.info("\n\nImp:")
        logging.info(json.dumps(imp))
        logging.info("\n\nExpected_imp:")
        logging.info(json.dumps(expected_imp))
        return imp == expected_imp

    def is_regs_object_as_expected(self, expected_regs):
        regs = self.bid_request.get("regs", None)
        assert regs is not None
        return regs == expected_regs

    def is_ext_object_as_expected(self, expected_ext):
        ext = self.bid_request.get("ext", None)
        assert ext is not None
        return self.__is_ext_objects_the_same(ext, expected_ext)

    def is_number_of_properties_as_expected(self, expected_number):
        """It is not recommended to use this, because new properties could break a test case"""
        equals = len(self.bid_request) == expected_number
        if not equals:
            logging.error(
                f"The expected number of properties of request {expected_number} "
                f"and the actual value is {len(self.bid_request)}"
            )
        return equals

    def is_source_object_as_expected(self, expected_source):
        source = self.bid_request.get("source", None)
        assert source is not None
        assert source["fd"] == expected_source["fd"]
        assert isinstance(source["tid"], str)
        return self.__is_ext_objects_the_same(source["ext"], expected_source["ext"])

    def is_tmax_as_expected(self, expected_tmax):
        tmax = self.bid_request.get("tmax", None)
        return tmax == expected_tmax

    def is_at_as_expected(self, expected_at):
        at = self.bid_request.get("at", None)
        return at == expected_at

    def is_allimps_as_expected(self, expected_allimps):
        allimps = self.bid_request.get("allimps", None)
        return allimps == expected_allimps

    def is_cur_as_expected(self, expected_cur):
        cur = self.bid_request.get("cur", None)
        return cur == expected_cur

    def is_mimes_as_expected(self, expected_cur):
        impressions = self.bid_request["imp"]
        assert impressions is not None and len(impressions) > 0
        impression = impressions[0]
        mime_holder = impression["video"] or impression["banner"]
        assert mime_holder is not None
        mimes = mime_holder["mimes"]
        assert len(expected_cur) == len(mimes)
        assert all(elem in mimes for elem in expected_cur)

    def get_device_geo_object(self):
        device = self.bid_request.get("device", None)
        assert device is not None
        return device["geo"]

    def get_user_geo_object(self):
        user = self.bid_request.get("user", None)
        assert user is not None
        return user["geo"]

    def is_device_ip_not_available(self):
        device = self.bid_request.get("device", None)
        logging.info(device)
        assert device is not None
        assert "ip" not in device

    def is_inventory_partner_domain_as_expected_rtb26(
        self, expected_inventory_partner_domain
    ):
        app = self.bid_request["app"]
        assert app is not None
        inventory_partner_domain = app.get("inventorypartnerdomain", None)
        assert inventory_partner_domain is not None
        return expected_inventory_partner_domain == inventory_partner_domain

    def is_inventory_partner_domain_as_expected_rtb25(
        self, expected_inventory_partner_domain
    ):
        app = self.bid_request["app"]
        assert app is not None
        app_ext = app.get("ext", None)
        assert app_ext is not None

        inventory_partner_domain = app_ext.get("inventorypartnerdomain", None)
        assert inventory_partner_domain is not None
        return expected_inventory_partner_domain == inventory_partner_domain

    def is_ssai_as_expected_rtb26(self, expected_ssai):
        impressions = self.bid_request["imp"]
        assert impressions is not None and len(impressions) > 0
        impression = impressions[0]
        ssai = impression["ssai"]
        assert ssai is not None
        impression_ext = impression.get("ext", None)
        assert "ssai" not in impression_ext
        return expected_ssai == ssai

    def is_eid_as_expected(self, expected_source):
        user = self.bid_request.get("user", None)
        assert user is not None and len(user) > 0
        eids = user["eids"]
        return expected_source == eids[0]["uids"][0]["id"]

    def is_eid_empty(self):
        user = self.bid_request.get("user", None)
        assert user is not None and len(user) > 0
        return user.get("eids") is None

    def is_ssai_as_expected_rtb25(self, expected_ssai):
        impressions = self.bid_request["imp"]
        assert impressions is not None and len(impressions) > 0
        impression_ext = impressions[0].get("ext", None)
        ssai = impression_ext["ssai"]
        assert ssai is not None
        return expected_ssai == ssai

    def is_plcmt_expected(self, expected):
        impressions = self.bid_request["imp"]
        assert impressions is not None and len(impressions) > 0
        impression = impressions[0]
        video = impression["video"]
        assert video is not None
        assert video["plcmt"] == expected

    def is_device_dnt_as_expected(self, expected=0):
        device = self.bid_request.get("device", None)
        assert device is not None
        assert device["dnt"] == expected

    @staticmethod
    def __is_ext_objects_the_same(ext, expected_ext):
        expected_ext.get("schain", None).get("nodes", None)[0]["sid"] = ext.get(
            "schain", None
        ).get("nodes", None)[0]["sid"]
        expected_ext.get("schain", None).get("nodes", None)[0]["rid"] = ext.get(
            "schain", None
        ).get("nodes", None)[0]["rid"]
        equals = ext == expected_ext
        if not equals:
            logging.error(f"The expected ext {expected_ext} \n is not equal to {ext}")
        return equals
