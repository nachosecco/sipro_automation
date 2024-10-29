import logging

from demand import Demand
from supply import Supply
from context import Context
from tracker import Tracker
from extractorWriter import ExtractorWriter


class ExtractorDelivery(ExtractorWriter):
    def __init__(
        self, placement, context: Context
    ):
        self.context_placement = placement
        ExtractorWriter.__init__(self, context)
        self.__setup_logger()

    def __setup_logger(self):
        logging.basicConfig(format="%(asctime)s [%(levelname)8.8s] %(message)s")

        logger = logging.getLogger("extractor")
        logger.setLevel(logging.DEBUG)

        self.logger = logger

    def extract(self):
        self.logger.info(f"Placement :[{self.context_placement}]")
        self.logger.info(f"Case :[{self.context.case_name}]")

        supply = Supply(self.context, self.context_placement).extract()

        placement = supply.get("placement")

        demand = Demand(self.context, placement.get("id")).extract()

        trackers_supply = supply.get("trackers") or []
        trackers_demand = demand.get("trackers") or []

        trackers = Tracker(self.context, list(set(trackers_supply + trackers_demand))).extract()

        result = {
            "supply": supply,
            "demand": demand,
            "trackers": trackers,
        }

        if self.context.override_options is not None:
            result['override_options'] = self.context.override_options

        return result
