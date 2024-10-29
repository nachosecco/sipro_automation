import logging
import os

from core.RoutersConstants import REPLACE


class Routers:
    def __init__(self, external_config):
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
        self.__external_config = external_config

    def url(self):
        root_url_router = os.getenv("RS_URL", None)
        if root_url_router is None:
            logging.error("The variable [RS_URL] is not set in the environment")
            raise Exception("The variable [RS_URL] is not set in the environment")

        url = root_url_router + "/vast?"
        fields = vars(self)
        for v in fields:
            if not v.startswith("_") and bool(fields[v]):
                url += v + "=" + fields[v] + "&"

        return url
