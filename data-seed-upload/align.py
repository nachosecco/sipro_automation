import logging

from context import Context
from resourceUtil import ResourceUtil


class Align:
    """Class that has the logic to the align a placement with the media"""

    def __init__(self, context: type(Context)):
        self.logger = logging.getLogger("upload")
        self.auth_token = context.authorization_context.token
        self.resource_util = ResourceUtil(context)
        self.api = context.configuration.dashboard_api

    def align(self, cache_resources, placement, media, programmatic_demands):
        cache_alignments = cache_resources.get("alignments")

        placement_id = placement.get("id")
        placement_name = placement.get("name")
        dashboard_api = self.api

        self.logger.info(
            f"Start to was align placement with name {placement_name} and id {placement_id}"
        )

        alignment_options_cache = cache_alignments.get(placement_id, {"media": []}).get(
            "media"
        )

        if not self.__check_if_necessary_align(
            alignment_options_cache, programmatic_demands, media
        ):
            logging.info("Skipping alignment, as it is already align")
            return

        media_align = []
        programmatic_demands_align = []

        url_alignment_options = f"{dashboard_api}/v2/manage/alignment-options/demand?placementId={placement_id}"
        alignment_options = self.resource_util.load_index(
            url_alignment_options, "alignment-options"
        )

        for media_option in alignment_options.get("media"):
            for media_dto in media.values():
                if media_dto.get("id") == media_option.get("id"):
                    media_align.append(media_option)

        for programmatic_demand_option in alignment_options.get("programmaticDemands"):
            for programmatic_demand in programmatic_demands.values():
                if programmatic_demand.get("id") == programmatic_demand_option.get(
                    "id"
                ):
                    programmatic_demands_align.append(programmatic_demand_option)

        programmatic_demands_len = len(programmatic_demands)
        if not len(programmatic_demands_align) == programmatic_demands_len:
            logging.warning(
                "programmatic_demands align is not the same that is in the seed data, check if something is not enabled"
            )

        media_len = len(media)
        media_align_len = len(media_align)
        if media_align_len != media_len:
            logging.warning(
                "Media align is not the same that is in the seed data, check if something is not enabled"
            )

        align_data = {
            "id": placement_id,
            "media": media_align,
            "programmaticDemands": programmatic_demands_align,
            "allowRon": False,
        }
        url = f"{dashboard_api}/v2/manage/placements/{placement_id}/alignments"
        self.resource_util.create_update_delete_resource(
            align_data, "alignments", url, "PUT", None
        )

        self.logger.info(
            f"It was aligned [{media_len}] media and [{programmatic_demands_len}] programmatic demands to the "
            f"placement with name {placement_name} and id {placement_id}"
        )

    @staticmethod
    def __check_if_necessary_align(
        alignment_options_cache, programmatic_demands, media
    ):
        # If for some reason the cache is not populated, it will always be necessary to align
        if len(alignment_options_cache) == 0:
            return True

        media_align = []
        programmatic_demands_align = []
        # If for some reason the cache is not populated, it will always be necessary to align
        if len(alignment_options_cache) == 0:
            return True

        for media_option in alignment_options_cache:
            if media_option.get("programmaticDemands"):
                for programmatic_demand in programmatic_demands.values():
                    if programmatic_demand.get("id") == media_option.get("id"):
                        programmatic_demands_align.append(media_option)
            else:
                for media_dto in media.values():
                    if media_dto.get("id") == media_option.get("id"):
                        media_align.append(media_option)

        return len(media_align) + len(programmatic_demands_align) != len(
            alignment_options_cache
        )
