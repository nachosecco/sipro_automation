from dashboardApiEnvironmentResources import DashboardApiEnvironmentResources
from UploaderReader import UploaderReader
from align import Align
from context import Context
from demand import Demand
from supply import Supply
from trackers import Trackers

DEFAULT_COMPANY_NAME = "_DEFAULT_COMPANY_NAME"


class UploadDashboardApi(UploaderReader):
    def __init__(self, only_new_changes: False):
        super().__init__()
        self.only_new_changes = only_new_changes
        self.resource_cache = {}

    def __get_resources(self, context):
        company_name = context.override_options.get(
            "company_name", DEFAULT_COMPANY_NAME
        )

        if company_name not in self.resource_cache:
            self.resource_cache[
                company_name
            ] = DashboardApiEnvironmentResources().load_resources(context)

        return self.resource_cache[company_name]

    def upload(
        self,
        data,
        context: type(Context),
        directory_case,
    ):
        resources = self.__get_resources(context)
        self.logger.debug("starting to upload dashboard data")

        # if we have flag to only new changes, we only check for placement is there
        if self.only_new_changes:
            placements_by_name_resources = resources.get("supply").get("placements")
            placement_name_serialized = data.get("supply").get("placement").get("name")
            placement_found = placements_by_name_resources.get(
                placement_name_serialized, None
            )
            if placement_found is not None:
                self.logger.debug(
                    f"placement {placement_name_serialized} found in env, continue"
                )
                return {"supply": {"placement": placement_found}}

        trackers = Trackers(context).upload(resources, data.get("trackers") or [])

        supply = Supply(context).upload(resources, data.get("supply"), trackers)

        demand = Demand(context).upload(
            resources, data.get("demand"), trackers, directory_case
        )

        Align(context).align(
            resources,
            supply.get("placement"),
            demand.get("media"),
            demand.get("programmatic_demands"),
        )
        return {"supply": supply, "demand": demand, "trackers": trackers}
