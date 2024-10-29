import inspect
import json
import logging
import os
import uuid
from typing import List

import requests

from core.devices import DEVICE_CTV_ROKU
from core.environmentPlacements import environment_placements
from core.rtbResponse import RtbResponse
from core.utils.geoIpUtils import get_ip_not_for_geo


def get_source_extensions():
    return {
        "schain": {
            "ver": "1.0",
            "complete": 1,
            "nodes": [
                {
                    "asi": "altitude-arena.com",
                    "sid": "IF0J8IVKST2GP09K9FQEE58CF0",
                    "hp": 1,
                    "rid": "E2QN166Q948UR60S0F9A47MKT0",
                }
            ],
        }
    }


def default_parameters_values():
    return {
        "device.ip-v4": get_ip_not_for_geo(country="US", postcode="11219"),
        "device.ip-v6": None,
        "device.ua": DEVICE_CTV_ROKU.ua,
        "device.id": str(uuid.uuid4()),
        "device.lmt": 0,
        "content.episode": None,
        "content.title": None,
        "content.series": None,
        "content.genre": None,
        "content.cat": None,
        "content.prodq": None,
        "content.qagmediarating": None,
        "content.livestream": None,
        "content.len": None,
        "content.language": None,
        "content.id": None,
        "app.bundle": None,
        "app.name": None,
        "app.url": None,
        "site.page": None,
        "site.ref": None,
        "user.eid": None,
        "user.ext.eid": None,
    }


def _get_resolved_value(parameters, value):
    if not value.startswith("{") or not value.endswith("}"):
        return value
    else:
        try:
            return parameters.get(value[1:-1])  # Striping start and end { }
        except KeyError:  # The value is not in the dictionary so is not overriden
            return None


def resolve_placeholders(json_payload, parameters):
    """
    Resolves placeholders in a JSON payload (or dictionary) with their corresponding values from 'parameters'.

    Placeholders are identified by curly braces, for example: {placeholder}.
    If a placeholder key is found in 'parameters', it will be included in the resulting JSON.
    If a placeholder is not found in 'parameters' or is mapped to None, the corresponding key will be excluded.
    If the value is not a placeholder the corresponding key will be mapped as is.

    :param json_payload: A JSON payload (or dictionary) with keys possibly containing placeholders.
    :type json_payload: dict

    :param parameters: A dictionary containing parameter-value pairs.
    :type parameters: dict

    :return: A new dictionary with keys from 'payload' replaced with corresponding values from 'parameters'.
    :rtype: dict
    """
    result = {}
    for key, value in json_payload.items():
        new_value = _get_resolved_value(parameters, value)
        if new_value is not None:
            result[key] = new_value
    return result


class RtbRequestBuilder:
    def __init__(self, placement_id: str):
        self.__badv = []
        self.__request_id = str(uuid.uuid4())
        self.__placement_uid = placement_id
        self.__type = None
        self.__us_privacy = "1---"
        self.__impression = RtbImpression()
        self.__lat_long = (37.751, -97.822)
        self.__coppa = 0
        self.__source_extension_provider = lambda: get_source_extensions()
        self.__gpp = None
        self.__gpp_sid = []
        self.__ext_gpp = None
        self.__ext_gpp_sid = []

        self.__parameters = default_parameters_values()
        self.__headers = {"Content-Type": "application/json"}

    @staticmethod
    def mobile(placement_id: str = None) -> "RtbAppRequestBuilder":
        """
        Only works when called directly from the test itself.
        Assigns the placement uid taken from the corresponding
        data-file
        :return: a RtbAppRequestBuilder
        """
        if placement_id is None:
            caller_frame = inspect.stack()[1]
            key = caller_frame.function
            placement_id = environment_placements.get_for(key)
            assert placement_id is not None, f"Not placement uid found for test:{key}"
        return RtbAppRequestBuilder(placement_id)

    @staticmethod
    def web(placement_id: str = None) -> "RtbWebRequestBuilder":
        """
        Only works when called directly from the test itself.
        Assigns the placement uid taken from the corresponding
        data-file
        :return: a RtbWebRequestBuilder
        """
        if placement_id is None:
            caller_frame = inspect.stack()[1]
            key = caller_frame.function
            placement_id = environment_placements.get_for(key)
            assert placement_id is not None, f"Not placement uid found for test:{key}"
        return RtbWebRequestBuilder(placement_id)

    def us_privacy(self, value: str) -> "RtbRequestBuilder":
        self.__us_privacy = value
        return self

    def lat_long(self, lat: float, long: float) -> "RtbRequestBuilder":
        self.__lat_long = (lat, long)
        return self

    def with_header(self, name: str, value: str) -> "RtbRequestBuilder":
        self.__headers[name] = value
        return self

    def with_ipv4(self, ip: str) -> "RtbRequestBuilder":
        self.__parameters["device.ip-v4"] = ip
        self.__parameters["device.ip-v6"] = None
        return self

    def with_ipv6(self, ip: str) -> "RtbRequestBuilder":
        self.__parameters["device.ip-v4"] = None
        self.__parameters["device.ip-v6"] = ip
        return self

    def gpp(self, gpp: str) -> "RtbRequestBuilder":
        self.__gpp = gpp
        return self

    def ext_gpp(self, gpp: str) -> "RtbRequestBuilder":
        self.__ext_gpp = gpp
        return self

    def eid(self, eid: str) -> "RtbRequestBuilder":
        self.__parameters["user.eid"] = eid
        return self

    def ext_eid(self, eid: str) -> "RtbRequestBuilder":
        self.__parameters["user.ext.eid"] = eid
        return self

    def gpp_sid(self, gpp_sid: int) -> "RtbRequestBuilder":
        self.__gpp_sid = [gpp_sid]
        return self

    def ext_gpp_sid(self, gpp_sid: int) -> "RtbRequestBuilder":
        self.__ext_gpp_sid = [gpp_sid]
        return self

    def coppa(self, value: str) -> "RtbRequestBuilder":
        self.__coppa = value
        return self

    def ua(self, value: str) -> "RtbRequestBuilder":
        self.__parameters["device.ua"] = value
        return self

    def ifa(self, value: str) -> "RtbRequestBuilder":
        self.__parameters["device.id"] = value
        return self

    def did(self, value: str) -> "RtbRequestBuilder":
        self.__parameters["device.id"] = value
        return self

    def lmt(self, value: str) -> "RtbRequestBuilder":
        self.__parameters["device.lmt"] = value
        return self

    def content_id(self, value: str) -> "RtbRequestBuilder":
        self.__parameters["content.id"] = value
        return self

    def min_duration(self, value: float) -> "RtbRequestBuilder":
        self.__impression.min_duration = value
        return self

    def plcmt(self, value: float) -> "RtbRequestBuilder":
        self.__impression.plcmt = value
        return self

    def dnt(self, value: int) -> "RtbRequestBuilder":
        self.__impression.dnt = value
        return self

    def max_duration(self, value: float) -> "RtbRequestBuilder":
        self.__impression.max_duration = value
        return self

    def max_seq(self, value: int) -> "RtbRequestBuilder":
        self.__impression.max_seq = value
        return self

    def ssai(self, value: int) -> "RtbRequestBuilder":
        self.__impression.ssai = value
        return self

    def pod_dur(self, value: float) -> "RtbRequestBuilder":
        self.__impression.pod_dur = value
        return self

    def h(self, value: int) -> "RtbRequestBuilder":
        self.__impression.h = value
        return self

    def w(self, value: int) -> "RtbRequestBuilder":
        self.__impression.w = value
        return self

    def badv(self, value: list) -> "RtbRequestBuilder":
        self.__badv = value
        return self

    def private_auction(self, value: int):
        pmp = RTBPmp()
        pmp.private_auction = value
        self.__impression.pmp = pmp
        return self

    def deal_id(self, value: str):
        deal = self.__get_or_create_deal()
        deal.id = value
        return self

    def deal_bid_floor(self, value: float):
        deal = self.__get_or_create_deal()
        deal.bid_floor = value
        return self

    def __get_or_create_deal(self):
        deal = RTBDeal()
        if self.__impression.pmp.deals:
            deal = self.__impression.pmp.deals[0]
        else:
            self.__impression.pmp.deals.append(deal)
        return deal

    def bid_floor(self, value: float) -> "RtbRequestBuilder":
        self.__impression.bid_floor = value
        return self

    def mimes(self, value: str) -> "RtbRequestBuilder":
        self.__impression.mimes = value
        return self

    def set(self, key: str, value: object) -> "RtbRequestBuilder":
        self.__parameters[key] = value
        return self

    def _get_placement_uid(self):
        return self.__placement_uid

    def _get_parameters(self):
        return self.__parameters

    def __get_impression(self):
        return {**{"id": "1"}, **self.__impression.get_impression()}

    def __get_geo(self):
        return {"geo": {"lat": self.__lat_long[0], "lon": self.__lat_long[1]}}

    def __get_device(self):
        return {
            **resolve_placeholders(
                {
                    "ua": "{device.ua}",
                    "ip": "{ip.v4}",
                    "ipv6": "{ip.v6}",
                    "lmt": "{device.lmt}",
                    "ifa": "{device.id}",
                },
                self.__parameters,
            ),
            **self.__get_geo(),
        }

    def __get_user(self):
        return resolve_placeholders(
            {"eids": "{user.eid}", "ext": "{user.ext.eid}"},
            self.__parameters,
        )

    def get_content(self):
        return resolve_placeholders(
            {
                "episode": "{content.episode}",
                "title": "{content.title}",
                "series": "{content.series}",
                "genre": "{content.genre}",
                "cat": "{content.cat}",
                "prodq": "{content.prodq}",
                "qagmediarating": "{content.qagmediarating}",
                "livestream": "{content.livestream}",
                "len": "{content.len}",
                "language": "{content.language}",
                "id": "{content.id}",
            },
            self.__parameters,
        )

    def _get_type(self):
        raise NotImplementedError("Abstract method")

    def send(self) -> RtbResponse:
        """
        Performs the request to the rtb-service sending a bidRequest and expecting a bidResponse
        or an error.
        :return: An object capable of perform assertions to the BidResponse
        :rtype: RtbResponse
        """
        host = os.environ.get("RTBRT_RTB_BIDDER_HOST", "http://localhost:8030/")
        connect_to = os.environ.get("RTBRT_RTB_BIDDER_CONNECT_TO", 5000)
        read_to = os.environ.get("RTBRT_RTB_BIDDER_READ_TO", 1000)
        if not host.endswith("/"):
            host += "/"
        uid = self._get_parameters().get("uid")
        query_string = f"?uid={uid}" if uid is not None else ""

        url = host + "rtb" + query_string
        payload = json.dumps(self.__build_request(), indent=2)
        response = requests.request(
            "POST",
            url,
            headers=self.__headers,
            data=payload,
            timeout=(connect_to, read_to),
        )
        try:
            response_payload = json.dumps(response.json(), indent=2)
            logging.info(
                "****BidRequest sent to %s : %s *******returned status: %d response: %s",
                url,
                payload,
                response.status_code,
                response_payload,
            )
            return RtbResponse(self.__request_id, response)
        except ValueError as e:
            logging.info(
                "****BidRequest sent to %s : %s *******returned status: %d error: %s",
                url,
                payload,
                response.status_code,
                e,
            )
            return RtbResponse(self.__request_id, response)

    def __build_request(self):
        return {
            **{
                "id": str(self.__request_id),
                "imp": [self.__get_impression()],
                "device": self.__get_device(),
                "source": {"ext": self.__source_extension_provider()},
                "regs": {
                    "coppa": self.__coppa,
                    "gpp": self.__gpp,
                    "gpp_sid": self.__gpp_sid,
                    "ext": {
                        "us_privacy": self.__us_privacy,
                        "gpp": self.__ext_gpp,
                        "gpp_sid": self.__ext_gpp_sid,
                    },
                },
                "user": self.__get_user(),
                "badv": self.__badv,
            },
            **self._get_type(),
        }


class RtbImpression:
    def __init__(self):
        self.min_duration = 0
        self.max_duration = 0
        self.max_seq = 0
        self.ssai = 0
        self.eid = bytearray()
        self.pod_dur = 0
        self.h = 720
        self.w = 1080
        self.bid_floor = 0
        self.mimes = ["video/mp4", "video/3gpp", "video/webm"]
        self.pmp = RTBPmp()
        self.plcmt = 1
        self.dnt = 0

    def get_impression(self):
        assert self.bid_floor > 0, "BidFloor is a required parameter"
        return {
            "video": {
                "minduration": self.min_duration,
                "maxduration": self.max_duration,
                "maxseq": self.max_seq,
                "poddur": self.pod_dur,
                "h": self.h,
                "w": self.w,
                "plcmt": self.plcmt,
                "mimes": self.mimes,
            },
            "bidfloor": self.bid_floor,
            "ssai": self.ssai,
            "dnt": self.dnt,
            "pmp": self.pmp.get_pmp(),
        }


class RTBPmp:
    def __init__(self):
        self.private_auction = 0
        self.deals: List[RTBDeal] = []

    def get_pmp(self):
        return {"private_auction": self.private_auction, "deals": self.get_deals()}

    def get_deals(self):
        if not self.deals:
            return []
        return list(map(lambda d: d.get_deal(), self.deals))


class RTBDeal:
    def __init__(self):
        self.id = None
        self.bid_floor = 0

    def get_deal(self):
        if self.id is None:
            return None
        return {"id": self.id, "bidfloor": self.bid_floor}


class RtbAppRequestBuilder(RtbRequestBuilder):
    def url(self, url: str):
        self.set("app.url", url)
        return self

    def name(self, name: str):
        self.set("app.name", name)
        return self

    def bundle(self, bundle: str):
        self.set("app.bundle", bundle)
        return self

    def _get_type(self):
        data = {
            "app": resolve_placeholders(
                {
                    "id": self._get_placement_uid(),
                    "name": "{app.name}",
                    "bundle": "{app.bundle}",
                    "storeurl": "{app.url}",
                    "ver": "{app.ver}",
                },
                self._get_parameters(),
            )
        }
        data["app"]["content"] = self.get_content()
        return data


class RtbWebRequestBuilder(RtbRequestBuilder):
    def url(self, url: str):
        self.set("site.page", url)
        return self

    def ref(self, ref: str):
        self.set("site.ref", ref)
        return self

    def _get_type(self):
        return {
            "site": resolve_placeholders(
                {
                    "id": self._get_placement_uid(),
                    "page": "{site.page}",
                    "ref": "{site.ref}",
                },
                self._get_parameters(),
            )
        }
