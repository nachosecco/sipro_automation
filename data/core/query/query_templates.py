from core.query.druid import to_iso_date


def create_druid_count_query(
    table: str, min_date: str, max_date: str, placement_guid: str
):

    iso_min_date = to_iso_date(min_date, True)
    iso_max_date = to_iso_date(max_date, False)

    sql = "SLECT COUNT(*)"
    sql += f"\nFROM {table}"
    sql += f"\nWHERE __time >= '{iso_min_date}' AND __time <= '{iso_max_date}'"
    sql += f"\nAND placement = '{placement_guid}'"


def create_druid_query(
    table: str,
    metrics: list,
    dimensions: list,
    filters: list,
    min_date: str,
    max_date: str,
    sorting=None,
    max_rows=None,
) -> str:
    sql = "SELECT "

    # Dimension as columns
    dimensions_len = len(dimensions)
    if dimensions_len > 0:
        for idx, d in enumerate(dimensions):
            sql += d
            if idx + 1 < dimensions_len:
                sql += ", "

    # Metrics
    metrics_len = len(metrics)
    if metrics_len > 0:
        if dimensions_len > 0:
            sql += ", "

        for idx, m in enumerate(metrics):
            sql += "COALESCE(SUM(" + m + "), 0)"
            if idx + 1 < metrics_len:
                sql += ", "

    sql += "\nFROM " + table

    # Filters
    sql += (
        "\nWHERE __time >= '"
        + to_iso_date(min_date, True)
        + "' AND __time <= '"
        + to_iso_date(max_date, False)
        + "'"
    )
    for idx, f in enumerate(filters):
        sql += " AND " + f["dimension"] + " = '" + f["value"] + "'"

    # Dimensions as GROUP BY
    if dimensions_len > 0:
        sql += "\nGROUP BY "
        for idx, d in enumerate(dimensions):
            sql += d
            if idx + 1 < dimensions_len:
                sql += ", "

    # Sorting
    if sorting is not None:
        sorting_len = len(sorting)
        if sorting_len > 0:
            sql += "\nORDER BY "
            for idx, f in enumerate(sorting):
                sql += f["column"] + " " + f["direction"] + ""
                if idx + 1 < sorting_len:
                    sql += ", "

    # Limit
    if max_rows is not None:
        sql += f"\nLIMIT {max_rows}"

    return sql
