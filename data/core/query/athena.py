import time

import boto3


def query(database, query_string):
    client = boto3.client("athena")
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
    return None


def count_query(table: str, min_date: str, max_date: str, placement_guid: str) -> str:

    sql = "SELECT COUNT(*)"
    sql += f"\nFROM {table}"
    sql += f"\nWHERE hour >= '{min_date}' AND hour <= '{max_date}'"
    sql += f"\nAND placement_guid = '{placement_guid}'"
    return sql


def sum_query(
    table: str,
    metrics: list,
    dimensions: list,
    min_date: str,
    max_date: str,
    placement_guid: str,
) -> str:

    sql = f"SELECT "

    # Dimension as columns
    dimensions_len = len(dimensions)
    if dimensions_len > 0:
        for idx, d in enumerate(dimensions):
            sql += d
            if idx + 1 < dimensions_len:
                sql += ", "

    # Metrics
    fields_len = len(metrics)
    if fields_len > 0:
        if dimensions_len > 0:
            sql += ", "
        for idx, field in enumerate(metrics):
            sql += f"SUM(try_cast({field} as double))"
            if idx + 1 < fields_len:
                sql += ", "

    sql += f"\nFROM {table}"

    # Filters
    sql += f"\nWHERE hour >= '{min_date}' AND hour <= '{max_date}'"
    sql += f"\nAND "
    for idx, field in enumerate(metrics):
        sql += f"{field} IS NOT NULL and {field} != ''"
        if idx + 1 < fields_len:
            sql += " AND "

    sql += f"\nAND placement_guid = '{placement_guid}'"

    # Dimensions as GROUP BY
    if dimensions_len > 0:
        sql += f"\nGROUP BY "
        for idx, dimension in enumerate(dimensions):
            sql += f"{dimension}"
            if idx + 1 < dimensions_len:
                sql += ", "

    return sql
