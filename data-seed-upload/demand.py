import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from context import Context
from demandDefaultValues import (
    DEFAULT_ADVERTISER_BODY,
    DEFAULT_INSERTION_ORDER_BODY,
    DEFAULT_CAMPAIGN_BODY,
    DEFAULT_MEDIA_BODY,
)
from programmaticDemand import ProgrammaticDemand
from resourceUtil import ResourceUtil, sanitize
from trackers import change_old_id_to_new_id_for_trackers

ADVERTISERS = "/v2/manage/advtsrs"
AUDIENCES = "/v2/manage/audiences"
CAMPAIGNS = "/v2/manage/campaigns"
INSERTION_ORDERS = "/v2/manage/insertion-orders"
MEDIA = "/v2/manage/media"
MEDIA_DISPLAY = "/v2/manage/mediaAssets/display"
MEDIA_VIDEO = "/v2/manage/mediaAssets/video"

MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_DISPLAY = 6


class Demand:
    def __init__(self, context: type(Context)):
        self.context = context
        self.logger = logging.getLogger("upload")
        self.resource_util = ResourceUtil(context)
        self.api = context.configuration.dashboard_api
        self.programmatic_demand = ProgrammaticDemand(self.resource_util, self.api)

    def upload(self, resources, demand, trackers, directory_case):
        demand_resources = resources.get("demand")
        audiences = self.__upload_audiences(
            demand_resources, demand.get("audiences", [])
        )
        advertisers = self.__upload_advertiser(
            demand_resources, demand.get("advertisers")
        )
        insertion_orders = self.__upload_io(
            demand_resources,
            advertisers,
            demand.get("insertion_orders"),
        )
        campaigns = self.__upload_campaigns(
            demand_resources, insertion_orders, demand.get("campaigns")
        )
        media = self.__upload_media(
            demand_resources,
            campaigns,
            demand.get("media"),
            trackers,
            audiences,
            directory_case,
        )
        programmatic_demands_and_rtb_config = self.programmatic_demand.upload(
            demand_resources, demand, trackers
        )

        return {
            "advertisers": advertisers,
            "insertion_orders": insertion_orders,
            "campaigns": campaigns,
            "media": media,
            "rtb_bidder_conf": programmatic_demands_and_rtb_config.get(
                "rtb_bidder_conf"
            ),
            "programmatic_demands": programmatic_demands_and_rtb_config.get(
                "programmatic_demands"
            ),
        }

    def __upload_advertiser(self, resources, advertisers_serializations):
        url = self.api + ADVERTISERS
        advertisers_by_name = resources.get("advertisers")
        advertisers = {}

        for advertiser_serialization in advertisers_serializations:
            advertiser_serialization_id = advertiser_serialization.get("id")
            advertiser_request = sanitize(
                advertiser_serialization,
                ["insertionOrders", "contactName", "contactEmail"],
            )
            advertiser_response = self.resource_util.sync(
                url,
                advertiser_request,
                advertisers_by_name,
                DEFAULT_ADVERTISER_BODY,
                "advertiser",
            )

            advertisers[advertiser_serialization_id] = advertiser_response
        return advertisers

    def __upload_io(self, resources, advertisers, insertion_orders_serializations):
        url = self.api + INSERTION_ORDERS
        insertion_orders_by_name = resources.get("insertion-orders")
        insertion_orders_response = {}

        for insertion_order_serialization in insertion_orders_serializations:
            insertion_order_serialization_id = insertion_order_serialization.get("id")
            parent_advertiser = advertisers.get(
                insertion_order_serialization.get("advId")
            )

            insertion_order_request = sanitize(
                insertion_order_serialization,
                ["campaigns", "campaignTableList", "advName", "advId"],
            )

            insertion_order_request["advId"] = parent_advertiser.get("id")

            insertion_order_response = self.resource_util.sync(
                url,
                insertion_order_request,
                insertion_orders_by_name,
                DEFAULT_INSERTION_ORDER_BODY,
                "insertion-order",
            )
            insertion_orders_response[
                insertion_order_serialization_id
            ] = insertion_order_response

        return insertion_orders_response

    def __upload_campaigns(self, resources, insertion_orders, campaigns_serializations):
        url = self.api + CAMPAIGNS
        campaigns_by_name = resources.get("campaigns")
        campaigns_response = {}

        for campaign_serialization in campaigns_serializations:
            insertion_order_parent_serialization_id = campaign_serialization.get(
                "insertionOrderId"
            )

            campaign_request = sanitize(
                campaign_serialization,
                [
                    "insertionOrderId",
                    "insertionOrderName",
                    "advId",
                    "advName",
                    "media",
                    "empty",
                ],
            )
            self.cleanup_campaign_date(campaign_request)

            day_parting = campaign_request.get("dayParting", None)
            if day_parting is not None:
                day_parting_request = sanitize(day_parting, ["empty"])
                campaign_request["dayParting"] = day_parting_request

            insertion_order_parent = insertion_orders.get(
                insertion_order_parent_serialization_id
            )
            campaign_request["insertionOrderId"] = insertion_order_parent.get("id")

            campaign_response = self.resource_util.sync(
                url,
                campaign_request,
                campaigns_by_name,
                DEFAULT_CAMPAIGN_BODY,
                "campaign",
            )
            campaigns_response[campaign_serialization.get("id")] = campaign_response
        return campaigns_response

    @staticmethod
    def cleanup_campaign_date(campaign_data):
        # This is a method to handle of the end date, if is expired to put in the future
        end_date_string = campaign_data.get("endDate")
        if not (end_date_string is None):
            end_date = datetime.strptime(end_date_string, "%m/%d/%Y %H:%M %p")
            if end_date.date() < datetime.today().date():
                end_date = end_date + relativedelta(years=1)
                campaign_data["endDate"] = end_date.strftime("%m/%d/%Y %H:%M %p")

    def __upload_media(
        self,
        resources,
        campaigns,
        media_serializations,
        trackers,
        audiences,
        directory_case,
    ):
        url = self.api + MEDIA
        media_by_name = resources.get("media")
        media_response = {}

        for media_serialization in media_serializations:
            campaign_parent_serialization_id = media_serialization.get("campaignId")
            media_request = sanitize(
                media_serialization,
                [
                    "insertionOrderId",
                    "insertionOrderName",
                    "advId",
                    "advName",
                    "campaignId",
                    "campaignName",
                ],
            )
            parent = campaigns.get(campaign_parent_serialization_id)
            media_request["campaignId"] = parent.get("id")

            # Handle of the end date, if is expired to put the same of parent
            end_date_string = media_request.get("customEndDate")
            if not (end_date_string is None):
                end_date = datetime.strptime(end_date_string, "%m/%d/%Y %H:%M %p")
                if end_date.date() < datetime.today().date():
                    media_request["customEndDate"] = parent.get("endDate")

            self.__replace_media_url_in_media_request(
                media_by_name, media_serialization, media_request
            )

            media_type = media_request.get("mediaTypeId")

            if media_type == MEDIA_TYPE_VIDEO:
                self.__upload_a_video_media_file_and_replace_url_in_media_request(
                    media_by_name, media_serialization, media_request, directory_case
                )
            elif media_type == MEDIA_TYPE_DISPLAY:
                self.__upload_a_display_media_file_and_replace_url_in_media_request(
                    media_by_name, media_serialization, media_request, directory_case
                )
            else:
                raise RuntimeError(f"Unsupported media_type: {media_type}")

            self.update_media_audience(media_request, audiences)

            old_trackers_id = media_serialization.get("trackers")
            new_trackers_id = change_old_id_to_new_id_for_trackers(
                old_trackers_id, trackers
            )
            media_request["trackers"] = new_trackers_id

            media_create_updated = self.resource_util.sync(
                url,
                media_request,
                media_by_name,
                DEFAULT_MEDIA_BODY,
                "media",
            )
            media_response[media_create_updated.get("id")] = media_create_updated
        return media_response

    def __replace_media_url_in_media_request(
        self, media_by_name, current_media, media_request
    ):
        # Patching mediaUrl, the Media entity is not consistent in the filing of the dto in all controllers,
        # the index and get one are not equal
        url_base = f"{self.api}{MEDIA}"
        domain = self.context.configuration.domain
        media_server = self.context.configuration.media_server

        name = current_media.get("name")
        media_found = media_by_name.get(name, None)
        if media_found is None:
            media_urls = []
            for media_url in media_request.get("mediaUrls", []):
                media_url.pop("id")
                url = media_url.get("url", "")
                if url.startswith("https://media") and domain in url:
                    index = url.index(domain) + len(domain)
                    new_url = media_server + url[index::]
                    media_url["url"] = new_url

                media_urls.append(media_url)

        else:

            media_id = media_found.get("id")
            url = f"{url_base}/{media_id}"
            media_response = self.resource_util.get_resource_by_id(
                url, media_id, "media"
            )

            media_urls = media_response.get("mediaUrls", None)
            if not (media_urls is None):
                media_request["mediaUrls"] = media_urls

    def __upload_audiences(self, resources, audience_serializations):
        url = self.api + AUDIENCES
        audiences_by_name = resources.get("audiences", [])
        audiences = {}

        for audience_serialization in audience_serializations:
            audience_serialization_id = audience_serialization.get("id")
            audience_request = sanitize(
                audience_serialization,
                ["cpm"],
            )
            audience_response = self.resource_util.sync(
                url, audience_request, audiences_by_name, {}, "audience", "description"
            )

            audiences[audience_serialization_id] = audience_response
        return audiences

    def update_media_audience(self, media_request, audiences):
        media_audiences = media_request.get("audiences", [])
        if len(media_audiences) > 0:
            self.logger.info("Replacing audience targeting ids")
            audience_expression = media_request.get("audienceExpression", "")
            indices = [
                index
                for index in range(len(audience_expression))
                if audience_expression.startswith("audienceId", index)
            ]
            audience_id_serializations = []
            for index in indices:
                sub_data = audience_expression[index::]
                space = sub_data.index(" ")
                break_line = sub_data.index("\n")
                audience_id_serializations.append(sub_data[space:break_line])
            for audience_id_serialization in audience_id_serializations:
                audience_resource = audiences.get(int(audience_id_serialization))
                audience_resource_id = audience_resource.get("id")
                audience_expression = audience_expression.replace(
                    f" {audience_id_serialization}\n", f" {audience_resource_id}\n"
                )
            media_request["audienceExpression"] = audience_expression

            for media_audience in media_audiences:
                audience_resource = audiences.get(media_audience.get("id"))
                audience_resource_id = audience_resource.get("id")

                media_audience["id"] = audience_resource_id
                media_audience["guid"] = audience_resource.get("guid")
                media_audience["description"] = audience_resource.get("description")
                media_audience.pop("cpm", None)
            media_request["audiences"] = media_audiences

    def __upload_a_display_media_file_and_replace_url_in_media_request(
        self, media_by_name, current_media, media_request, directory_case
    ):
        name = current_media.get("name")
        url = self.api + MEDIA_DISPLAY
        media_found = media_by_name.get(name, None)

        if media_found is None:
            self.logger.debug("Media not found with name, and we have assets to upload")

            display_media_file = current_media["displayMediaFile"]
            media_file_id = display_media_file.get("id")
            media_file_extension = display_media_file.get("mimeType").split("/")[1]
            file_name_path = (
                f"{directory_case}/{name.replace(' ', '_')}_{media_file_id}"
            )

            # Dashboard API checks the file extension, so we override here to include it
            file = {
                "file": (
                    f"{file_name_path}.{media_file_extension}",
                    open(file_name_path, "rb"),
                )
            }
            data_media_file = {"mediaType": 6}

            media_file_response = self.resource_util.upload_file(
                file, data_media_file, url, "Media Asset File"
            )
            media_request["mediaFiles"] = [media_file_response]
            media_request["displayMediaFile"] = media_file_response
        else:
            media_id = media_found.get("id")
            url = f"{self.api}{MEDIA}/{media_id}"
            media_response = self.resource_util.get_resource_by_id(
                url, media_id, "media"
            )

            media_files = media_response.get("mediaFiles", [])
            media_request["mediaFiles"] = media_files
            media_request["displayMediaFile"] = media_files[0]

    def __upload_a_video_media_file_and_replace_url_in_media_request(
        self, media_by_name, current_media, media_request, directory_case
    ):
        url = self.api + MEDIA_VIDEO
        name = current_media.get("name")
        media_found = media_by_name.get(name, None)

        file_name_path_prefix = directory_case + "/" + name.replace(" ", "_")

        if media_found is None:
            self.logger.debug("Media not found with name, and we have assets to upload")
            media_file_responses = []
            for media_file in current_media.get("mediaFiles", []):
                data_media_fila = {
                    "uploadName": media_file.get("uploadName"),
                    "mimeType": media_file.get("mimeType"),
                    "height": media_file.get("height"),
                    "width": media_file.get("width"),
                    "bitRate": media_file.get("bitRate"),
                }
                media_file_id = media_file.get("id")
                file_name_path = f"{file_name_path_prefix}_{media_file_id}"
                file = {"file": open(file_name_path, "rb")}
                media_file_response = self.resource_util.upload_file(
                    file, data_media_fila, url, "Media Asset File"
                )
                media_file_responses.append(media_file_response)
            media_request["mediaFiles"] = media_file_responses

        else:
            media_id = media_found.get("id")
            url = f"{self.api}{MEDIA}/{media_id}"
            media_response = self.resource_util.get_resource_by_id(
                url, media_id, "media"
            )

            media_files = media_response.get("mediaFiles", [])
            media_request["mediaFiles"] = media_files
