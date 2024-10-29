import time
import boto3
from pandas import DataFrame
from botocore.exceptions import NoRegionError


# Execute multiple queries in a single transaction
def execute_queries(database, query_strings):
    for query_string in query_strings:
        query(database, query_string)


# Execute a single query and return the results
def query(database, query_string):
    client = boto3.client("athena")
    try:
        resp = client.start_query_execution(
            QueryString=query_string,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={
                "OutputLocation": f"s3://c6-{database}-s3-uw2-devops-athena-query-results/",
            },
            WorkGroup="primary",
        )
        query_execution_id = resp["QueryExecutionId"]
        query_time = 0
        while query_time < 1800:
            resp = client.get_query_execution(QueryExecutionId=query_execution_id)
            state = resp["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                # For more information on get_query_results including Response Syntax, see:
                # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/get_query_results.html
                resp = client.get_query_results(
                    QueryExecutionId=query_execution_id, MaxResults=1000
                )
                return resp
            if state == "FAILED":
                print(
                    f'Athena query failed: {resp["QueryExecution"]["Status"]["StateChangeReason"]}'
                )
                return None
            time.sleep(10)
            query_time += 10
    except NoRegionError:
        print("No AWS region specified. Please specify a region.")
    # If the query fails, return None
    return None


def get_traffic_shaping_hourly_blocklist_for_hour(db, hour):
    # Query the traffic_shaping_hourly_blocklist table to verify that the blocked bidder is present
    query_string = (
        f"SELECT * FROM {db}.traffic_shaping_hourly_blocklist WHERE etl_hour='{hour}'"
    )
    result = query(db, query_string)
    return result


# Get the rows from an athena query result
def get_rows(result):
    return result["ResultSet"]["Rows"]


# Get the number of rows from an athena query result
def get_rows_count(result):
    return len(get_rows(result))


def get_column_value_for_row(result, column_name, row_index):
    # Find the index of the partner_guid column in the header row
    header_row_df = DataFrame(result["ResultSet"]["Rows"][0]["Data"])
    column_index = header_row_df.index[
        header_row_df["VarCharValue"] == column_name
    ].tolist()[0]
    row = result["ResultSet"]["Rows"][row_index]
    return row["Data"][column_index]["VarCharValue"]
