import requests


def query(url, user_name, password, query_json):
    resp = requests.post(url, auth=(user_name, password), json=query_json, verify=False)
    result = resp.text.rstrip()
    # Druid query returns "" if there is no data in the query result after Imply 2023.09
    result = "0" if result == '""' else result
    return result


def query_sql(url, user_name, password, sql):
    query_json = {
        "query": sql,
        "resultFormat": "array",
    }

    return query(url, user_name, password, query_json)


def get_hour(input_hour):
    # Input hour format: YYYYMMdd_HHmm. Druid hour: YYYY-MM-dd HH:mm:00
    druid_hour = (
        input_hour[0:4]
        + "-"
        + input_hour[4:6]
        + "-"
        + input_hour[6:8]
        + " "
        + input_hour[9:11]
        + ":"
        + input_hour[11:13]
        + ":00"
    )
    return druid_hour


def get_druid_url(env, secrets_manager):
    response = secrets_manager.get_secret_value(
        SecretId=f"/{env}/imply_monitoring/DRUID_URL"
    )
    druid_host = response["SecretString"]
    return f"https://{druid_host}/druid/v2/sql/"


def get_druid_password(env, secrets_manager):
    response = secrets_manager.get_secret_value(
        SecretId=f"/{env}/imply_monitoring/DRUID_AUTH_PASSWORD"
    )
    return response["SecretString"]


def to_iso_date(event_time_date: str, min_hour):
    year = event_time_date[0:4]
    month = event_time_date[5:7]
    day = event_time_date[8:10]
    hour = event_time_date[11:13]
    if min_hour:
        minute = "00"
    else:
        minute = "59"

    return f"{year}-{month}-{day}T{hour}:{minute}:00.000Z"
