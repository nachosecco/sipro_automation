import io
import sys
from datetime import datetime

import boto3
import pandas as pd

from core.dashboard.authorization_context import AuthorizationContext
from core.dashboard.resource_util import ResourceUtil
from core.query import druid, athena
from core.query.druid import get_druid_url, get_druid_password


def read_mi_enabled_placements(context):
    # Read Multiple Impressions eanbled placements from Dashboard API. MI stands for multiple impressions.
    resource_util = ResourceUtil(context)
    pl = resource_util.get_resource_index("/v2/manage/placements", "placement")
    pl_guids = list(
        map(lambda p: p["guid"], filter(lambda p: p["usingMultipleImpObjects"], pl))
    )
    placements = pd.DataFrame(pl_guids, columns=["placement_guid"])
    return placements


def get_mi_disabled_rtb_opps(rtb_opps_df, mi_enabled_placements_df):
    rtb_opps_df = pd.merge(
        rtb_opps_df,
        mi_enabled_placements_df,
        on=["placement_guid"],
        how="outer",
        indicator=True,
    )
    rtb_opps_df = rtb_opps_df[rtb_opps_df["_merge"] == "left_only"]
    return int(rtb_opps_df["rtb_opps"].sum())


def get_mi_enabled_athena_rtb_opps(athena_rtb_opps_df, mi_enabled_placements_df):
    athena_rtb_opps_df = pd.merge(
        athena_rtb_opps_df, mi_enabled_placements_df, on=["placement_guid"], how="inner"
    )
    return int(athena_rtb_opps_df["imp_opps"].sum())


def get_mi_enabled_druid_rtb_opps(druid_rtb_opps_df, mi_enabled_placements_df):
    athena_rtb_opps_df = pd.merge(
        druid_rtb_opps_df, mi_enabled_placements_df, on=["placement_guid"], how="inner"
    )
    return int(athena_rtb_opps_df["rtb_opps"].sum())


def query_druid_rtb_opps(druid_datasource):
    query_json = {
        "query": f"select placement placement_guid, sum(rtb_opps) rtb_opps from {druid_datasource} where "
        f"company='{company_guid}' and __time=TIMESTAMP '{druid_hour}' group by "
        f"placement order by 1 limit 1000",
        "resultFormat": "csv",
        "header": True,
    }
    druid_query_results = druid.query(druid_url, DRUID_USER_NAME, password, query_json)
    return pd.read_csv(io.StringIO(druid_query_results))


def query_athena_rtb_opps(athena_database):
    rtb_opps_athena_df = pd.DataFrame(
        columns=["placement_guid", "imp_opps", "rtb_opps"]
    )
    athena_query_string = (
        f"select placement_guid, sum(json_array_length(json_extract(bidder, '$.impIdOpps'))) imp_opps, "
        f"count(bidder) rtb_opps from rtb cross join unnest(CAST(JSON_PARSE(regexp_replace(regexp_replace("
        f"regexp_replace(bidders, '\"\\w{{26,}}\":\\{{', '{{'), '^\\{{', '['), '\\}}$', ']')) AS "
        f"ARRAY<JSON>)) AS t(bidder) where hour='{athena_hour}' and "
        f"company_guid='{company_guid}' group by 1 order by 1 limit 1000;"
    )
    resp = athena.query(athena_database, athena_query_string)
    row_num = 0
    if resp is not None:
        rows = resp["ResultSet"]["Rows"]
        for row in rows:
            # Skip header
            if row_num > 0:
                rtb_opps_athena_df.loc[row_num] = [
                    row["Data"][0]["VarCharValue"],
                    int(row["Data"][1]["VarCharValue"]),
                    int(row["Data"][2]["VarCharValue"]),
                ]
            row_num += 1
    return rtb_opps_athena_df


def is_in_the_current_day(hour):
    return hour[:8] == datetime.utcnow().strftime("%Y%m%d")


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            f"Usage: python {sys.argv[0]} [prod|dev|qa1|qa2|int1] [Hour, e.g., 20230101_2300] "
            f"[Company GUID, e.g., LQPKO06JEH58HCQC039N9EK8KC] "
            f"[Dashborad API User, e.g., siprocal-delivery-automation@siprocal.com] "
            f"[Dashboard API Password]"
        )
        sys.exit(1)

    environment = sys.argv[1]
    athena_hour = sys.argv[2]
    company_guid = sys.argv[3]
    dashboard_api_user = sys.argv[4]
    dashboard_api_password = sys.argv[5]

    # Get Multiple Impression Object enabled placements
    secrets_manager = boto3.client("secretsmanager")
    dashboard_api_url = (
        f"https://manage{environment}.siprocalads.com"
        if environment != "prod"
        else "https://manage.siprocalads.com"
    )
    auth_context = AuthorizationContext(
        dashboard_api_url, dashboard_api_user, dashboard_api_password
    )
    placements_df = read_mi_enabled_placements(auth_context)

    # Query Athena Rtb Opps total
    rtb_opps_athena_df = query_athena_rtb_opps(environment)

    # Exclude MI enabled placements with no imp oops
    placements_df = placements_df.merge(
        rtb_opps_athena_df[rtb_opps_athena_df["imp_opps"] > 0],
        on=["placement_guid"],
        how="inner",
    )["placement_guid"]

    # Calculate Athena rtb opps
    athena_rtb_opps = get_mi_disabled_rtb_opps(rtb_opps_athena_df, placements_df)
    print(f"Athena Total Rtb Opps: {athena_rtb_opps}")
    athena_mi_enabled_rtb_opps = get_mi_enabled_athena_rtb_opps(
        rtb_opps_athena_df, placements_df
    )
    print(
        f"Athena Total Rtb Opps for placements with Multiple Impression Objects enabled: {athena_mi_enabled_rtb_opps}"
    )

    # Query Druid Rtb Opps total
    druid_url = get_druid_url(environment, secrets_manager)
    DRUID_USER_NAME = "admin"
    password = get_druid_password(environment, secrets_manager)
    druid_hour = druid.get_hour(athena_hour)
    rtb_opps_druid_df = query_druid_rtb_opps("rtb_v6")

    # Calculate Druid Rtb Opps total
    druid_rtb_opps = get_mi_disabled_rtb_opps(rtb_opps_druid_df, placements_df)
    print(f"Validating the hour {athena_hour}:")
    print(f"Druid Total Rtb Opps: {druid_rtb_opps}")
    druid_mi_enabled_rtb_opps = get_mi_enabled_druid_rtb_opps(
        rtb_opps_druid_df, placements_df
    )
    print(
        f"Druid Total Rtb Opps for placements with Multiple Impression Objects enabled: {druid_mi_enabled_rtb_opps}"
    )

    # Query Druid Rtb Daily Opps Total if the hour is in the current day
    if is_in_the_current_day(athena_hour):
        rtb_opps_druid_df = query_druid_rtb_opps("rtb_v6_daily")
        druid_rtb_opps_from_daily_ds = get_mi_disabled_rtb_opps(
            rtb_opps_athena_df, placements_df
        )
        print(f"Druid Total Rtb Opps From rtb_v6_daily: {druid_rtb_opps_from_daily_ds}")
        if druid_rtb_opps != druid_rtb_opps_from_daily_ds:
            print(
                "Total Rtb Opps count doesn't match between Druid rtb_v6 and rtb_v6_daily"
            )
            sys.exit(2)

    if druid_rtb_opps == athena_rtb_opps:
        print(
            "Total Rtb Opps count for placements with multiple impression object disabled matches"
        )
    else:
        print(
            "Total Rtb Opps count for placements with multiple impression object disabled doesn't match between Druid rtb_v6 and Athena"
        )
        sys.exit(1)

    if druid_mi_enabled_rtb_opps == athena_mi_enabled_rtb_opps:
        print(
            "Total Rtb Opps count for placements with multiple impression object enabled matches"
        )
    else:
        print(
            "Total Rtb Opps count for placements with multiple impression object enabled doesn't match between Druid rtb_v6 and Athena"
        )
        sys.exit(3)
