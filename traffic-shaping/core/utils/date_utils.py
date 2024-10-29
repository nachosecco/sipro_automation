from datetime import timedelta, datetime


def get_past_hours(given_hour: str, hours: int = 24) -> [str]:
    date_format = "%Y%m%d_%H%M"
    given_date = datetime.strptime(given_hour, date_format)
    return [
        (given_date - timedelta(hours=i + 1)).strftime(date_format)
        for i in range(hours)
    ]
