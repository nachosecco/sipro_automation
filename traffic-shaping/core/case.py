from core.traffic_shaping import TrafficShaping

from core.configuration import Configuration


class Case:
    """Representation of case to test"""

    def __init__(self, name, configuration=Configuration()):
        self.name = name
        self.configuration = configuration

    def get_traffic_shaping_and_load_data(
        self,
        hourly_records: dict,
        current_hour: str,
        placement_guid: str,
        app_bundle_id: str,
    ):
        traffic_shaping = TrafficShaping.init_from_records(
            hourly_records,
            current_hour,
            self.configuration,
            placement_guid,
            app_bundle_id,
        )
        # Clean up records before validation
        traffic_shaping.cleanup_records(self.name)
        # Seed data to Athena Tables
        traffic_shaping.seed_data()
        return traffic_shaping
