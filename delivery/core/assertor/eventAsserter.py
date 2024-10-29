import logging

from core.assertor.bidderAssertor import BidderAssertor, parse_bidders_log
from core.constants import ComparisonType as CT
from core.constants import IP_ADDRESS_VALIDATION_REGEX
from core.dto.event import Event, EventType
from core.utils.validationUtils import compare_result, compare_result_without_quotes
from core.vpc import VPC


class EventAsserter:
    def __init__(self, delivery_saved_logs, vpc: VPC):
        self.event = None
        self.delivery_logs = delivery_saved_logs
        self.log_found = False
        self.log = ""
        self.vpc = vpc

    def __find_log_entry(self, logs, event_type: EventType):
        for log in logs:
            if log.find(f"{event_type.value}") != -1:
                return log
        return ""

    def assert_expected_event_in_the_log(self, event: Event):
        self.event = event
        self.log = self.__find_log_entry(self.delivery_logs, event.event_type).strip()
        self.log_found = len(self.log) != 0
        self.validate_event()

    def validate_event(self):

        event = self.event
        vpc = self.vpc
        log = self.log
        if not self.log_found:
            logging.error(
                f"The log message related to event {event.event_type} was not found in the logs"
            )
            assert False

        logging.info(
            f"Asserting that the expected event values are : ${self.event.__dict__}"
        )
        compare_result_without_quotes("beaconEventType: ", event.beacon_event_type, log)
        compare_result('placementGuid: "', event.placement_guid, log)
        compare_result('siteGuid: "', event.site_guid, log)
        compare_result('publisherGuid: "', event.publisher_guid, log)
        compare_result('companyGuid: "', event.company_guid, log)
        compare_result('ipAddress: "', IP_ADDRESS_VALIDATION_REGEX, log, CT.Pattern)
        compare_result('ipAddressOverride: "', event.ipAddressOverride, log, CT.Pattern)
        compare_result('schain: "', event.schain, log)
        compare_result('userTrackerId: "', event.user_tracker_id, log)
        compare_result_without_quotes(
            "beaconEventPlacementPosition: ", event.placement_position, log
        )
        compare_result('partnerGuid: "', event.partner_guid, log)
        compare_result_without_quotes(
            "beaconEventPlacementSizeType: ", event.placement_size_type, log
        )
        compare_result('userAgent: "', event.user_agent, log, CT.Startswith)
        compare_result('appName: "', vpc.app_name, log)
        compare_result('appBundleId: "', vpc.app_id, log)
        # geo details
        compare_result('countryCode: "', vpc.geo_co, log)
        compare_result('subCode: "', vpc.geo_sub, log)
        compare_result('subName: "', vpc.geo_subname, log)
        compare_result('postalCode: "', vpc.geo_code, log)
        compare_result('dma: "', vpc.geo_dma, log)
        compare_result('ISPName: "', vpc.geo_isp_name, log)
        compare_result_without_quotes("longitude: ", vpc.geo_long, log)
        compare_result_without_quotes("latitude: ", vpc.geo_lat, log)
        compare_result('connectionType: "', vpc.geo_conn_type, log)
        # Meta Details
        compare_result('mediaGuid: "', event.media_guid, log)
        compare_result_without_quotes("deviceType: ", event.device_type, log)
        compare_result_without_quotes("vpaidType: ", event.vpaid_type, log)
        compare_result_without_quotes("deviceOS: ", event.device_os, log)
        compare_result_without_quotes("os: ", event.os, log)
        compare_result_without_quotes(
            "userTrackingType: ", event.user_tracking_type, log
        )
        compare_result_without_quotes(
            "isUsingUserTrackerIdSessionUUID: ",
            event.is_using_user_tracker_id_session_UUID,
            log,
        )
        compare_result_without_quotes("filterReasonsV2: ", event.filter_reasons_v2, log)
        compare_result_without_quotes("filterReasons: ", event.filter_reasons, log)
        compare_result_without_quotes("filterReason: ", event.filter_reason, log)
        compare_result_without_quotes("result: ", event.result, log)

        if event.event_type == EventType.RTB_EVENT:
            compare_result("win: ", event.bid_win, log)
            compare_result_without_quotes(
                "lossReasonCode: ", event.loss_reason_code, log
            )
            compare_result_without_quotes(
                "\ncpm: ", event.cpm, log
            )  # add next line char to avoid getting searched as part of wcpm
            compare_result_without_quotes("floor: ", event.floor, log)
            compare_result_without_quotes("wcpm: ", event.wcpm, log)
            compare_result('dimension: "', event.placement_size, log)
            compare_result_without_quotes("placementType: ", event.placement_type, log)
            for blocked_bidder_guid in event.blocked_bidders_guids:
                compare_result(
                    'blockedBiddersGuids: "',
                    blocked_bidder_guid,
                    log,
                )

        else:
            compare_result('cpm: "', event.cpm, log)
            compare_result('floor: "', event.floor, log)
            compare_result('placementSize: "', event.placement_size, log)
            compare_result_without_quotes(
                "beaconEventPlacementType: ", event.placement_type, log
            )

        compare_result_without_quotes(
            "partnerDemandFeePercentage: ", event.partner_demand_fee_percentage, log
        )
        compare_result('winnerId: "', event.winner_id, log)
        compare_result('episode: "', event.episode, log)
        compare_result('title: "', event.title, log)
        compare_result('series: "', event.series, log)
        compare_result('genre: "', event.genre, log)
        compare_result('categories: "', event.categories, log)
        compare_result('productionQuality: "', event.productionQuality, log)
        compare_result('mediaRating: "', event.mediaRating, log)
        compare_result('liveStream: "', event.liveStream, log)
        compare_result('length: "', event.length, log)
        compare_result('language: "', event.language, log)
        # validate bidders if they exist
        bidder_asserter = BidderAssertor(parse_bidders_log(log))
        bidder_asserter.assert_expected_bidders_in_logs(
            event.winnerBidder, event.loserBidders
        )
