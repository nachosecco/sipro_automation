import logging
import uuid

from core.constants import REPLACE, AUTOMATION_FRAMEWORK_ID_DELIVERY
from core.utils.urlutils import get_delivery_url


class VPC:
    def __init__(self):
        self.uid: str = REPLACE
        self.player_width: str = "640"
        self.player_height: str = "480"
        self.ip_address = REPLACE
        self.latlng = REPLACE
        self.lat = REPLACE
        self.long = REPLACE
        self.ua = REPLACE
        self.app_name = REPLACE
        self.app_id = REPLACE
        self.app_uri = REPLACE
        self.app_ver = REPLACE
        self.schain = REPLACE
        self.did = REPLACE
        self.did_type = REPLACE
        self.us_privacy = REPLACE
        self.lmt = REPLACE
        self.coppa = REPLACE
        self.ssai = REPLACE
        self.eid = REPLACE
        self.content_episode = REPLACE
        self.content_title = REPLACE
        self.content_series = REPLACE
        self.content_genre = REPLACE
        self.content_cat = REPLACE
        self.content_prodq = REPLACE
        self.content_qagmediarating = REPLACE
        self.content_livestream = REPLACE
        self.content_len = REPLACE
        self.content_language = REPLACE
        self.content_id = REPLACE
        self.pod_size = REPLACE
        self.pod_max_dur = REPLACE
        self.pod_min_ad_dur = REPLACE
        self.pod_max_ad_dur = REPLACE
        self.pod_max_ad_dur = REPLACE
        self.gdpr = REPLACE
        self.gdpr_consent = REPLACE
        self.gdpr_pd = REPLACE
        self.page_domain = REPLACE
        self.page_url = REPLACE
        self.ref_page_domain = REPLACE
        self.ref_page_url = REPLACE
        self.channel_name = REPLACE
        self.network_name = REPLACE
        self.min_price = None
        self.use_dynamic_pricing = None
        self.__custom_param = {}
        self.gpp = REPLACE
        self.gpp_sid = REPLACE
        self.dnt = REPLACE
        self.plcmt = REPLACE

        # geo properties
        self.geo_co = REPLACE
        self.geo_dma = REPLACE
        self.geo_sub = REPLACE
        self.geo_sub = REPLACE
        self.geo_subname = REPLACE
        self.geo_code = REPLACE
        self.geo_conn_type = REPLACE
        self.geo_ip = REPLACE
        self.geo_lat = REPLACE
        self.geo_long = REPLACE
        self.geo_isp_name = REPLACE
        self.geo_latlng = REPLACE

        # Internal use, don't change the value
        self._automationFramework = str(uuid.uuid4())

    def add_custom_param(self, key: str, value: str):
        """Will add a custom param to a vpc call"""
        self.__custom_param[key] = value
        logging.info(f"Added custom param {key} with value {value}")

    def url(self):
        url = get_delivery_url() + "/vast?"
        fields = vars(self)
        for v in fields:
            if not v.startswith("_") and bool(fields[v]):
                if type(fields[v]) is dict:
                    for key in fields[v]:
                        url += key + "=" + fields[v][key] + "&"
                else:
                    url += v + "=" + fields[v] + "&"
        if len(self.__custom_param) > 0:
            for key_parm, value_param in self.__custom_param.items():
                url += key_parm + "=" + value_param + "&"
        url += f"{AUTOMATION_FRAMEWORK_ID_DELIVERY}={self._automationFramework}"

        return url

    def display_url(self):
        url = get_delivery_url() + "/" + self.uid + "?"
        url += f"us_privacy={self.us_privacy}&{AUTOMATION_FRAMEWORK_ID_DELIVERY}={self._automationFramework}"

        return url

    def regenerate_automation_framework(self):
        self._automationFramework = str(uuid.uuid4())
        self.__custom_param = {}
