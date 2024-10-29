import logging

from context import Context
from resourceUtil import ResourceUtil


class Demand:
    def __init__(self, context: type(Context), id_placement: int):

        self.id_placement = id_placement
        self.context = context
        self.logger = logging.getLogger("extractor")
        self.resource_util = ResourceUtil(context.authorization_context)
        self.api = context.configuration.dashboard_api
        self.case_name = context.case_name

    def extract(self):
        media_align = self.__load_alignment_media_and_programmatic_demands()
        media = self.__load_media(media_align.get("media"))
        campaigns = self.__load_campaign_from_media(media)
        insertion_orders = self.__load_io_from_campaign(campaigns)
        advertisers = self.__load_advertiser_from_io(insertion_orders)
        programmatic_demand = media_align.get("programmatic_demand")
        rtb_bidder_conf = self.__load_rtb_bidder_from_programmatic(programmatic_demand)
        audiences = self.__load_audiences(media, programmatic_demand)
        trackers = self.__trackers_from_medias(media + programmatic_demand)
        return {
            "advertisers": advertisers,
            "insertion_orders": insertion_orders,
            "campaigns": campaigns,
            "media": media,
            "programmatic_demands": programmatic_demand,
            "rtb_bidder_conf": rtb_bidder_conf,
            "audiences": audiences,
            "trackers": trackers,
        }

    def __load_alignment_media_and_programmatic_demands(self):

        placement_id = self.id_placement

        url = f"{self.api}/v2/manage/placements/{placement_id}/alignments"

        alignments = self.resource_util.get_resource_index("alignments", url)

        media_aligned = self.resource_util.resource_name_for_collection(
            self.case_name, "media", alignments.get("media")
        )
        programmatic_demands_aligned = []
        programmatic_demands_aligned_raw = alignments.get("programmaticDemands")
        self.logger.info(
            f"Fetched programmatic from alignment for placement with id [{placement_id}] "
        )
        # we have to fetch more details for programmatic that are not in the alignments collection
        base_url = f"{self.api}/v2/manage/programmatic-demand/"
        for pd in programmatic_demands_aligned_raw:
            id_programmatic_demand = pd.get("id")
            url = f"{base_url}{id_programmatic_demand}"

            programmatic_demand = self.resource_util.get_resource_with_test_case_naming(
                id_programmatic_demand,
                "programmatic demand",
                url,
                self.case_name,
            )

            programmatic_demands_aligned.append(programmatic_demand)

        programmatic_demands_aligned = self.resource_util.resource_name_for_collection(
            self.case_name, "programmatic demand", programmatic_demands_aligned
        )
        return {
            "media": media_aligned,
            "programmatic_demand": programmatic_demands_aligned,
        }

    @staticmethod
    def __trackers_from_medias(medias):
        trackers_to_return = set()
        for media in medias:
            trackers = media.get("trackers")
            if trackers is not None:
                for tracker in trackers:
                    trackers_to_return.add(tracker)

        return list(trackers_to_return)

    @staticmethod
    def __is_already_added(id_resource, collection):
        for value in collection:
            if value.get("id") == id_resource:
                return True
        return False

    def __load_resource_from_collection(
        self, collection, parent_key, resource_name_log, url
    ):
        data_resources = []
        for resource in collection or []:
            resource_id = resource.get(parent_key)

            if self.__is_already_added(resource_id, data_resources):
                continue
            url_suffix = url.format(str(resource_id))
            url_api = f"{self.api}{url_suffix}"
            resource = self.resource_util.get_resource_with_test_case_naming(
                resource_id, resource_name_log, url_api, self.case_name
            )

            data_resources.append(resource)

        self.resource_util.resource_name_for_collection(
            self.case_name, resource_name_log, data_resources
        )

        return data_resources

    def __load_campaign_from_media(self, media):

        return self.__load_resource_from_collection(
            media, "campaignId", "campaign from media", "/v2/manage/campaigns/{}"
        )

    def __load_io_from_campaign(self, campaigns):

        return self.__load_resource_from_collection(
            campaigns,
            "insertionOrderId",
            "io from campaign",
            "/v2/manage/insertion-orders/{}",
        )

    def __load_advertiser_from_io(self, insertion_orders):
        return self.__load_resource_from_collection(
            insertion_orders, "advId", "advertiser from io", "/v2/manage/advtsrs/{}"
        )

    def __load_rtb_bidder_from_programmatic(self, programmatic_demands):
        """creating a list of a bidders from to align programmatic_demands"""
        self.logger.debug("Loading rtb bidders")
        rtb_bidders = []
        base_url = f"{self.api}/v2/manage/rtb-bidders/"
        rtb_bidder_ids = {}
        for programmatic in programmatic_demands:
            programmatic_bidder_configs = programmatic.get("programmaticBidderConfigs")
            for bidder_configs in programmatic_bidder_configs:
                rtb_bidder_id = bidder_configs.get("rtbBidderId")
                rtb_bidder_ids[rtb_bidder_id] = rtb_bidder_id

        for rtb_bidder_id in rtb_bidder_ids:
            url_api = f"{base_url}{rtb_bidder_id}"
            rtb_bidder = self.resource_util.get_resource_json(
                rtb_bidder_id, "rtb bidder", url_api
            )
            rtb_bidders.append(rtb_bidder)

        return self.resource_util.resource_name_for_collection(
            self.case_name, "rtb bidder", rtb_bidders
        )

    def __load_media(self, media):
        api_url = f"{self.api}/v2/manage/media/"
        media_responses = []
        for media_request in media:
            media_id = media_request.get("id")
            media_responses.append(
                self.resource_util.get_resource_with_test_case_naming(
                    media_id, "media", f"{api_url}{media_id}", self.case_name
                )
            )
        media_responses = self.resource_util.resource_name_for_collection(
            self.case_name, "media", media_responses
        )
        for media_response in media_responses:
            if media_response.get("mediaSource") == "asset":
                self.__load_and_write_asset(media_response)

        return media_responses

    def __load_audiences(self, media, programmatic_demands):
        api_url_prefix = f"{self.api}/v2/manage/audiences/"
        audiences = {}
        for current_media in media:
            media_audiences = current_media.get("audiences", [])
            self.audience_from_demand_source(api_url_prefix, audiences, media_audiences)
        for programmatic_demand in programmatic_demands:
            programmatic_demand_audiences = programmatic_demand.get("audiences", [])
            self.audience_from_demand_source(
                api_url_prefix, audiences, programmatic_demand_audiences
            )
        return self.resource_util.resource_name_for_collection(
            self.case_name, "Audience", list(audiences.values()), "description"
        )

    def audience_from_demand_source(
        self, api_url_prefix, audiences, demand_sources_audiences
    ):
        for demand_sources_audience in demand_sources_audiences:
            audience_id = demand_sources_audience.get("id")
            api_url = f"{api_url_prefix}{audience_id}"
            audience = self.resource_util.get_resource_json(
                audience_id, "Audience", api_url
            )
            audiences[audience.get("id")] = audience

    def __load_and_write_asset(self, media_response):
        media_id = media_response.get("id")
        name_file_prefix = media_response.get("name").replace(" ", "_")

        self.logger.info(f"Loading asset from media with id {media_id}")
        for media_file in media_response.get("mediaFiles", []):
            self.write_asset(media_file, name_file_prefix, "previewURL")

    def write_asset(self, media_file, name_file_prefix, key_to_download):
        media_asset_id = media_file.get("id")
        name_file = f"{self.context.folder_to_write}{name_file_prefix}_{media_asset_id}"
        response = self.resource_util.get_resource(
            media_asset_id, "media asset", media_file.get(key_to_download)
        )
        with open(name_file, "wb") as f:
            f.write(response.content)
