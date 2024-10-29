import logging

from demandDefaultValues import DEFAULT_RTB_BIDDER, DEFAULT_PROGRAMMATIC_DEMAND
from resourceUtil import ResourceUtil, sanitize
from trackers import change_old_id_to_new_id_for_trackers

RTB_BIDDERS = "/v2/manage/rtb-bidders"

PROGRAMMATIC_DEMAND = "/v2/manage/programmatic-demand"


class ProgrammaticDemand:
    def __init__(self, resource_util: type(ResourceUtil), api):
        self.logger = logging.getLogger("upload")
        self.resource_util = resource_util
        self.api = api

    def upload(self, demand_resources, demand, trackers):
        programmatic_demands_serializations = demand.get("programmatic_demands")
        rtb_bidder_conf = self.upload_bidder_conf(
            demand_resources,
            demand.get("rtb_bidder_conf"),
            programmatic_demands_serializations,
        )

        programmatic_demands = self.__sync_programmatic_demands(
            demand_resources,
            rtb_bidder_conf,
            programmatic_demands_serializations,
            trackers,
        )

        return {
            "rtb_bidder_conf": rtb_bidder_conf,
            "programmatic_demands": programmatic_demands,
        }

    def upload_bidder_conf(
        self, resources, rtb_bidders_serializations, programmatic_demands_serializations
    ):
        url = self.api + RTB_BIDDERS
        rtb_bidders_by_name = resources.get("rtb_bidders")

        seats_by_bidder = self.get_seats_by_programmatic_demands(
            programmatic_demands_serializations
        )

        rtb_bidders_response = {}
        for rtb_bidder_serialization in rtb_bidders_serializations:
            bidder_id = rtb_bidder_serialization.get("id")
            bidder_name = rtb_bidder_serialization.get("name")
            rtb_bidder_seats_serialized = rtb_bidder_serialization.get("rtbBidderSeats")
            existing_bidder = rtb_bidders_by_name.get(bidder_name, None)

            rtb_bidder_seats = self.rtb_bidder_seat_to_bidder(
                bidder_id,
                existing_bidder,
                seats_by_bidder,
                rtb_bidder_seats_serialized,
            )

            rtb_bidder_request = sanitize(rtb_bidder_serialization, ["rtbBidderSeats"])
            # Trusting existing urls, because of deals ids
            if existing_bidder is not None:
                id_existing_bidder = existing_bidder.get("id")
                # Reloading to have the urls
                existing_bidder = self.resource_util.get_resource_by_id(
                    f"{url}{id_existing_bidder}", id_existing_bidder, "Bidder"
                )
                rtb_bidder_request["rtbUrls"] = existing_bidder.get("rtbUrls")

            rtb_bidder_request["rtbBidderSeats"] = rtb_bidder_seats

            rtb_bidder_response = self.resource_util.sync(
                url,
                rtb_bidder_request,
                rtb_bidders_by_name,
                DEFAULT_RTB_BIDDER,
                "rtb_bidder",
            )
            rtb_bidders_response[
                rtb_bidder_serialization.get("id")
            ] = rtb_bidder_response

            rtb_bidders_by_name[rtb_bidder_response.get("name")] = rtb_bidder_response

        return rtb_bidders_response

    @staticmethod
    def rtb_bidder_seat_to_bidder(
        bidder_id,
        existing_bidder,
        seats_by_bidder,
        rtb_bidder_seats_serialized,
    ):

        rtb_bidder_seats = []
        if existing_bidder is None:
            for seat_tmp in seats_by_bidder.get(bidder_id, {}).values():
                rtb_bidder_seats.append(sanitize(seat_tmp, ["bidderId"]))
        else:
            rtb_bidder_seats = existing_bidder.get("rtbBidderSeats")

        rtb_bidder_seats_to_return = []
        for rtb_bidder_seat_serialized in rtb_bidder_seats_serialized:
            seat_name_serialized = rtb_bidder_seat_serialized.get("seatName")
            found_seat = False
            for rtb_bidder_seat in rtb_bidder_seats:
                if rtb_bidder_seat.get("seatName") == seat_name_serialized:
                    found_seat = True
                    rtb_bidder_seats_to_return.append(rtb_bidder_seat)
                    break
            if not found_seat:
                rtb_bidder_seat_new = sanitize(rtb_bidder_seat_serialized, ["bidderId"])
                if existing_bidder is not None:
                    rtb_bidder_seat_new["bidderId"] = existing_bidder.get("id")
                rtb_bidder_seats_to_return.append(rtb_bidder_seat_new)

        return rtb_bidder_seats_to_return

    @staticmethod
    def get_seats_by_programmatic_demands(programmatic_demands_serializations):
        seats_by_bidder = {}
        for programmatic_demand_serialization in programmatic_demands_serializations:

            bidder_configs = programmatic_demand_serialization.get(
                "programmaticBidderConfigs"
            )
            for bidder_config in bidder_configs:
                bidder_id = bidder_config.get("rtbBidderId")
                seats_serializations = bidder_config.get("rtbBidderSeats")
                seats = seats_by_bidder.get(bidder_id, {})
                for seat_serialization in seats_serializations:
                    seat_name = seat_serialization.get("seatName")
                    used_seat = seats.get(seat_name, None)
                    if used_seat is None:
                        seats[seat_name] = seat_serialization

                seats_by_bidder[bidder_id] = seats
        return seats_by_bidder

    def delete_existing_programmatic_demand_with_same_deal_id(
        self,
        url_base,
        programmatic_demands_serializations,
        deals,
    ):
        for programmatic_demand_serialization in programmatic_demands_serializations:
            deal_id = programmatic_demand_serialization.get("dealId", "")
            name = programmatic_demand_serialization.get("name")
            programmatic_demand_deal = deals.get(deal_id, None)
            if len(deal_id) > 0 and programmatic_demand_deal is not None:

                db_name = programmatic_demand_deal.get("name")
                if name != db_name:
                    programmatic_demand_id = programmatic_demand_deal.get("id")
                    self.logger.debug(
                        f"We are going to delete a existing programmatic demand with id {programmatic_demand_id}"
                    )
                    url = f"{url_base}/{programmatic_demand_id}"
                    programmatic_demand = self.resource_util.get_resource_by_id(
                        url, programmatic_demand_id, "programmatic demand"
                    )
                    programmatic_demand_request = sanitize(
                        programmatic_demand, ["placements", "inheritedValues"]
                    )
                    programmatic_demand_request["id"] = programmatic_demand.get("id")

                    self.resource_util.create_update_delete_resource(
                        programmatic_demand_request,
                        "programmatic demand",
                        url,
                        "DELETE",
                    )

                    self.logger.debug(
                        f"Deleted programmatic demand with id {programmatic_demand_id}"
                    )

    def update_bidder_url_with_deal(
        self, programmatic_bidder_configs, new_deal_id, old_deals_id
    ):

        for bidder_config in programmatic_bidder_configs:
            bidder_id = bidder_config.get("rtbBidderId")
            self.logger.info(
                f"Updating Bidder with id {bidder_id} to new {new_deal_id}"
            )
            url = f"{self.api}{RTB_BIDDERS}/{bidder_id}"
            rtb_bidder = self.resource_util.get_resource_by_id(url, bidder_id, "Bidder")
            new_rtb_bidder = []
            for url_bidder in rtb_bidder.get("rtbUrls"):
                url_of_bidder = url_bidder.get("url")
                for old_deal_id in old_deals_id:
                    find_deal = f"dealId={old_deal_id}"
                    replace_deal = f"dealId={new_deal_id}"
                    if url_of_bidder in f"{find_deal}&":
                        replace_deal = f"{replace_deal}&"
                        find_deal = f"{find_deal}&"
                    elif url_of_bidder in f'{find_deal}"':
                        find_deal = f'{find_deal}"'
                        replace_deal = f'{replace_deal}"'

                    url_bidder["url"] = url_of_bidder.replace(find_deal, replace_deal)
                    new_rtb_bidder.append(url_bidder)
                    break
            rtb_bidder["rtbUrls"] = new_rtb_bidder

            rtb_bidder_request = sanitize(rtb_bidder, [])

            self.resource_util.create_update_delete_resource(
                rtb_bidder_request, "Bidder", url, "PUT"
            )
            self.logger.info(f"Updated Bidder with id {bidder_id} to new {new_deal_id}")

    def __sync_programmatic_demands(
        self, resources, rtb_bidder_confs, programmatic_demands_serializations, trackers
    ):
        url = self.api + PROGRAMMATIC_DEMAND

        programmatic_demands_by_name = resources.get("programmatic_demands")

        programmatic_demands_response = {}

        for programmatic_demand_serialization in programmatic_demands_serializations:
            pds_name = programmatic_demand_serialization.get("name")
            existing_programmatic_demand = programmatic_demands_by_name.get(
                pds_name, None
            )

            bidder_confs_serializations = programmatic_demand_serialization.get(
                "programmaticBidderConfigs"
            )
            seats_serializations = []
            for bidder_confs_serialization in bidder_confs_serializations:

                seats_serializations.extend(
                    bidder_confs_serialization.get("rtbBidderSeats", [])
                )

            programmatic_demand_request = sanitize(
                programmatic_demand_serialization,
                ["programmaticBidderConfigs", "placements"],
            )

            old_tracker_ids = programmatic_demand_request.get("trackers")
            new_tracker_ids = change_old_id_to_new_id_for_trackers(
                old_tracker_ids, trackers
            )
            programmatic_demand_request["trackers"] = new_tracker_ids

            programmatic_bidder_configs = self.get_programmatic_bidder_configs(
                programmatic_demand_serialization,
                rtb_bidder_confs,
                seats_serializations,
            )

            programmatic_demand_request[
                "programmaticBidderConfigs"
            ] = programmatic_bidder_configs
            programmatic_demand_response = None

            day_parting = programmatic_demand_request.get("dayParting", None)
            if day_parting is not None:
                day_parting_request = sanitize(day_parting, [])
                programmatic_demand_request["dayParting"] = day_parting_request

            # Using existing programmatic demand with a deal id,  we are going to use it.
            if (
                existing_programmatic_demand is not None
                and len(existing_programmatic_demand.get("dealId", "")) > 0
            ):
                programmatic_demand_request[
                    "dealId"
                ] = existing_programmatic_demand.get("dealId")

            old_deals_id = {}

            if len(programmatic_demand_serialization.get("dealId", "")) > 0:
                deal_id = programmatic_demand_serialization.get("dealId")
                old_deals_id[deal_id] = deal_id

            need_to_update_bidder_with_deal = False
            deal_id = programmatic_demand_request.get("dealId", None)

            while programmatic_demand_response is None:
                deal_id = programmatic_demand_request.get("dealId", None)
                old_deals_id[deal_id] = deal_id
                try:
                    programmatic_demand_response = self.resource_util.sync(
                        url,
                        programmatic_demand_request,
                        programmatic_demands_by_name,
                        DEFAULT_PROGRAMMATIC_DEMAND,
                        "programmatic-demand",
                    )
                except Exception as e:
                    if deal_id is not None and str(e).find("Deal ID already exists"):
                        deal_id = self.deal_name_change_to_number(deal_id)
                        programmatic_demand_request["dealId"] = deal_id
                        need_to_update_bidder_with_deal = True
                    else:
                        raise Exception(str(e))

            programmatic_demands_response[
                programmatic_demand_serialization.get("id")
            ] = programmatic_demand_response
            if need_to_update_bidder_with_deal:
                self.update_bidder_url_with_deal(
                    programmatic_demand_response.get("programmaticBidderConfigs"),
                    deal_id,
                    old_deals_id,
                )
        return programmatic_demands_response

    @staticmethod
    def get_programmatic_bidder_configs(
        programmatic_demand_serialization, rtb_bidder_confs, seats_serializations
    ):
        programmatic_bidder_configs = []
        for bidder_config in programmatic_demand_serialization.get(
            "programmaticBidderConfigs"
        ):
            rtb_bidder = rtb_bidder_confs.get(bidder_config.get("rtbBidderId"))
            seats_in_conf = rtb_bidder.get("rtbBidderSeats")
            seats = []
            for seat_serialization in seats_serializations:
                for seat_in_conf in seats_in_conf:
                    if seat_in_conf.get("seatName") == seat_serialization.get(
                        "seatName"
                    ):
                        seats.append(seat_in_conf)

            programmatic_bidder_configs.append(
                {"rtbBidderId": rtb_bidder.get("id"), "rtbBidderSeats": seats}
            )
        return programmatic_bidder_configs

    @staticmethod
    def deal_name_change_to_number(deal_id):
        """Will wrap up the name of the"""
        if len(deal_id) > 7 and deal_id[-6:].startswith("DA_"):
            deal_number = int(deal_id[-3:]) + 1
            return deal_id[0 : len(deal_id) - 6] + f"DA_{deal_number:003}"
        else:
            return f"{deal_id}DA_001"
