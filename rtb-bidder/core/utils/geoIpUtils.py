import csv

GEO_DATA_FILE = "data/data-file-geoip.csv"


def get_ip_for_geo(country="", region="", city="", postcode="", dma=""):
    with open(GEO_DATA_FILE, encoding="utf-8", newline="") as geo_file:
        geo_reader = csv.DictReader(geo_file)
        ip_address = ""

        for row in geo_reader:
            if (
                country in ("", row["country"])
                and region in ("", row["region"])
                and city in ("", row["city"])
                and postcode in ("", row["postcode"])
                and dma in ("", row["dma"])
            ):
                ip_address = row["ip_address"]
                break

        if not ip_address:
            raise Exception(
                f"No IP matching country={country}, region={city}, region={city}, postcode={postcode}, dma={dma}"
            )

        return ip_address


def get_ip_not_for_geo(country="", region="", city="", postcode="", dma=""):
    with open(GEO_DATA_FILE, encoding="utf-8", newline="") as geo_file:
        geo_reader = csv.DictReader(geo_file)
        ip_address = ""

        for row in geo_reader:
            if (
                (country == "" or country != row["country"])
                and (region == "" or region != row["region"])
                and (city == "" or city != row["city"])
                and (postcode == "" or postcode != row["postcode"])
                and (dma == "" or dma != row["dma"])
            ):
                ip_address = row["ip_address"]
                break

        if not ip_address:
            raise Exception(
                f"No IP NOT matching country={country}, region={region}, city={city}, postcode={postcode}, dma={dma}"
            )

        return ip_address


def get_geo_for_ip(ip_address):
    with open(GEO_DATA_FILE, encoding="utf-8", newline="") as geo_file:
        geo_reader = csv.DictReader(geo_file)
        geo_data = None

        for row in geo_reader:
            if row["ip_address"] == ip_address:
                geo_data = row
                connection_type = row["connection_type"]

                # app/app-web/app-web-delivery/src/main/java/com/altitude/app/web/auction/common/ConnectionTypeUtils.java
                if connection_type in ("Cable/DSL", "Corporate"):
                    geo_data["connection_type_code"] = 1
                elif connection_type == "Cellular":
                    geo_data["connection_type_code"] = 3
                else:
                    geo_data["connection_type_code"] = 0

                break

        if geo_data is None:
            raise Exception(f"No Geo Data found for ip_address={ip_address}")

        return geo_data
