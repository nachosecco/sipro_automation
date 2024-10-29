import logging

from context import Context
from extractorDelivery import ExtractorDelivery
from resourceUtil import ResourceUtil
from extractorWriter import ExtractorWriter


class ExtractorInventoryRouter(ExtractorWriter):
    def __init__(
        self,
        router_uid: str,
        context: Context
    ):
        self.router_uid = router_uid
        ExtractorWriter.__init__(self, context)
        self.logger = logging.getLogger("extractor")
        self.resource_util = ResourceUtil(self.context.authorization_context)
        self.api = self.context.configuration.inventory_router_api

    def extract(self):
        routers = self.__load_index()
        router_found = self.__load_router(routers)
        placements_by_demand_source = self.__load_placements(router_found)
        return {
            "router": router_found,
            "placementsByDemandSource": placements_by_demand_source,
        }

    def __load_router(self, routers):
        for router in routers:
            if router.get("guid") == self.router_uid:
                router["name"] = self.context.case_name
                return router

        raise Exception(
            f"error the router with uid [{self.router_uid}] was not found in the index"
        )

    def __load_index(self):

        company_id = self.context.authorization_context.company_id

        url = f"{self.api}/api/v1/model/company/{company_id}/routers"
        return self.resource_util.get_resource_index("router", url)

    def __load_placements(self, router):
        demand_sources = router.get("demandSources")
        placements_by_demand_source = []
        placement_number = 1
        for demand_source in demand_sources:
            placement_id = demand_source.get("placementId")
            if not (placement_id is None):
                context = Context(f"{self.context.case_name}_[{placement_number}]", self.context.folder_to_write, self.context.override_options)
                extractor = ExtractorDelivery(
                    {"id": placement_id},
                    context
                )
                placement = extractor.extract()
                data = {"id": demand_source.get("id"), "placement": placement}
                placements_by_demand_source.append(data)
                placement_number += 1

        return placements_by_demand_source
