import inspect
import logging

from core.configuration import Configuration
from core.utilResources import UtilResources


class Resource:
    """Represent a base resource class"""

    name = ""
    guid = ""

    def load_json_to_class_resource(self, json_resource):

        for member in inspect.getmembers(self):
            name_field_or_method = member[0]
            if not name_field_or_method.startswith("_") and not inspect.ismethod(
                member[1]
            ):
                setattr(
                    self,
                    name_field_or_method,
                    json_resource.get(name_field_or_method, None),
                )


class Publisher(Resource):
    adsTxtAccountId = ""


class Placement(Resource):
    pass


class Supply:
    def __init__(self, guid_placement, util_resources: type(UtilResources)):
        self.util_resources = util_resources
        self.publisher = Publisher()
        self.placement = Placement()

        self.__load_supply_data(guid_placement)

    def __load_supply_data(self, guid_placement):
        placements_json = self.util_resources.supply.find_placements_by_index()
        # reusing the placement from the index, because is enough data for this current use.
        placements_by_guid = self.util_resources.collection_resources_to_dict_by_guid(
            placements_json
        )
        placement_json = placements_by_guid.get(guid_placement, None)
        if placement_json is None:
            logging.error(
                f"The placement {guid_placement} was not found in the environment"
            )
            # Raising a fail test, because this should never happen
            assert False
        self.placement.load_json_to_class_resource(placement_json)
        publisher_id = placement_json.get("publisherId")
        publisher_json = self.util_resources.supply.find_publisher_by_id(publisher_id)
        self.publisher.load_json_to_class_resource(publisher_json)


class DataEnvironment:
    """Used to fetch data of an environment for an entity with fields
    like guid or others like that, that different always"""

    def __init__(self, guid_placement, configuration=Configuration()):
        self.util_resources = None
        self.configuration = configuration
        self.guid_placement = guid_placement
        self.__supply = None

    def supply(self):
        if self.__supply is None:
            self.util_resources = UtilResources(self.configuration)
            placement = self.guid_placement
            logging.info(
                f"Loading supply data for placement guid :{placement} "
                f"from dashboard {self.util_resources.configuration.dashboard_api}"
            )
            self.__supply = Supply(placement, self.util_resources)
        return self.__supply
