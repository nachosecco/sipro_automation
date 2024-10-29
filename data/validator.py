import sys
import boto3


from core.query import druid, athena
from core.query.druid import get_druid_url, get_druid_password

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            f"Usage: python {sys.argv[0]} [prod|dev|qa1|qa2|int1] [Hour, e.g., 20230101_2300] "
            f"[Company GUID, e.g., LQPKO06JEH58HCQC039N9EK8KC]"
        )
        exit(1)

    environment = sys.argv[1]
    athena_hour = sys.argv[2]
    company_guid = sys.argv[3]

    # Query Druid Impression count
    secrets_manager = boto3.client("secretsmanager")
    druid_url = get_druid_url(environment, secrets_manager)
    druid_user_name = "admin"
    password = get_druid_password(environment, secrets_manager)
    druid_hour = druid.get_hour(athena_hour)
    query_json = {
        "query": f"select sum(impression) from network_v1 where company='{company_guid}' "
        f"and __time=TIMESTAMP '{druid_hour}'",
        "resultFormat": "csv",
    }
    druid_impression_count = druid.query(
        druid_url, druid_user_name, password, query_json
    )
    print(f"Validating the hour {athena_hour}:")
    print(f"Druid impression count: {druid_impression_count}")

    # Query Athena Impression count
    athena_database = environment
    athena_query_string = f"select count(*) from impression where hour='{athena_hour}' and company_guid='{company_guid}';"
    resp = athena.query(athena_database, athena_query_string)
    if resp is not None:
        rows = resp["ResultSet"]["Rows"]
        row = rows[1]
        athena_impression_count = row["Data"][0]["VarCharValue"]
        print(f"Athena impression count: {athena_impression_count}\n")
        if int(druid_impression_count) == int(athena_impression_count):
            print("Impression count matches")
            exit(0)
    print("Impression count doesn't match")
    exit(1)
