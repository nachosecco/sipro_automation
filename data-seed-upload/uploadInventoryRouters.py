from UploaderReader import UploaderReader

from resourceUtil import sanitize, ResourceUtil
from uploadDashboardApi import UploadDashboardApi


class UploadInventoryRouters(UploaderReader):
    def __init__(
        self,
    ):
        super().__init__()
        # Use a single instance since UploadDashboardApi does resource caching
        self.upload_dashboard_api = UploadDashboardApi(False)

    def upload(
        self,
        data_read,
        context,
        directory_case,
    ):

        url = (
            context.configuration.inventory_router_api
            + "/api/v1/model/company/1/routers"
        )

        placements_response = self.upload_placements(
            data_read.get("placementsByDemandSource"),
            context,
            directory_case,
        )

        router_serialization = data_read.get("router")
        router_request = sanitize(router_serialization, ["requests"])
        demand_sources_request = []
        for demand_source in router_request.get("demandSources"):
            demand_source_request = sanitize(demand_source, [])
            if demand_source_request.get("type") == "PLACEMENT":
                demand_source_request["placementId"] = placements_response[
                    demand_source_request.get("placementId")
                ]
                demand_sources_request.append(demand_source_request)
        router_request["demandSources"] = demand_sources_request
        resource_util = ResourceUtil(context)
        routers_index = resource_util.load_index(url, "Router")
        routers_resources = {}
        for router in routers_index:
            routers_resources[router.get("name")] = router
        resource_util.sync(url, router_request, routers_resources, {}, "Router")

    def upload_placements(
        self,
        placements_serializations,
        context,
        directory_case,
    ):
        self.logger.info("Starting the upload of dashboard(domain) api resources")
        placements = {}
        for placement_serialization in placements_serializations:
            placement_serialization_dashboard = placement_serialization.get("placement")
            upload_response = self.upload_dashboard_api.upload(
                placement_serialization_dashboard,
                context,
                directory_case,
            )
            supply_serialization = placement_serialization_dashboard.get("supply")
            placement_serialization = supply_serialization.get("placement")

            supply_response = upload_response.get("supply")
            placement_response = supply_response.get("placement")

            placements[placement_serialization.get("id")] = placement_response.get("id")
        return placements
