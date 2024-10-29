from collections.abc import Iterator
import csv
import ipaddress
import logging
import sys
import geoip2.database

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
log = logging.getLogger()


GEO_DATA_FILE = "data/data-file-geoip.csv"
GEO_DATA_FILE_OUT = "data/NEW-data-file-geoip.csv"

GEO_CITY_NETWORK_BLOCKS_FILE = "scripts/GeoIP2-City-Blocks-IPv4.csv"
GEO_CITY_LOCATIONS_FILE = "scripts/GeoIP2-City-Locations-en.csv"
GEO_ISP_MMDB = "scripts/GeoIP2-ISP.mmdb"
GEO_CONNECTION_TYPE_MMDB = "scripts/GeoIP2-Connection-Type.mmdb"


def read_current_geo_data_file():
    """Return a List of Dict. Each Dict is a row in the current geo data file"""
    with open(GEO_DATA_FILE, encoding="utf-8", newline="") as geo_data_file:
        geo_data_reader = csv.DictReader(geo_data_file)
        return list(geo_data_reader)


def read_city_locations_file():
    """Return a Dict of geoname_id -> Dict. Each Dict is a row in the city locations file"""
    city_locations = {}
    with open(
        GEO_CITY_LOCATIONS_FILE, encoding="utf-8", newline=""
    ) as city_locations_file:
        city_locations_reader = csv.DictReader(city_locations_file)

        log.info("Beginning read of city_locations_file: %s", GEO_CITY_LOCATIONS_FILE)
        for row in city_locations_reader:
            city_locations[row["geoname_id"]] = row

        log.info("Done reading city_locations_file")

    return city_locations


def read_isp_mmdb(ip_addresses):
    """Return a Dict of ip_address -> Dict. Each Dict is data from the ISP db

    The ISP CSV doesn't have all the same data that is in the MMDB (not sure why).
    So we pull this data from MMDB for each IP we will output
    """
    isp_geo_data = {}
    with geoip2.database.Reader(GEO_ISP_MMDB) as reader:
        for ip_address in ip_addresses:
            try:
                isp_geo_data[ip_address] = reader.isp(ip_address)
            except geoip2.errors.AddressNotFoundError:
                pass

    return isp_geo_data


def read_connection_type_mmdb(ip_addresses):
    """Return a Dict of ip_address -> Dict. Each Dict is data from the Connection Type db

    The Connection Type CSV doesn't have all the same data that is in the MMDB (not sure why).
    So we pull this data from MMDB for each IP we will output
    """
    connection_type_geo_data = {}
    with geoip2.database.Reader(GEO_CONNECTION_TYPE_MMDB) as reader:
        for ip_address in ip_addresses:
            try:
                connection_type_geo_data[ip_address] = reader.connection_type(
                    ip_address
                )
            except geoip2.errors.AddressNotFoundError:
                pass

    return connection_type_geo_data


def read_city_network_blocks_file(current_geo_data, city_locations):
    """Return a Dict of ip -> Dict. Each Dict is a row in the city network blocks file

    IPs returned are either existing IPs from the current geo data file or are suitable replacements
    if one of the current IPs can no longer be used.

    The idea is to use the existing IP if possible to reduce churn, but if it no longer meets the
    criteria then we need a replacement.

    The City Network Blocks file is ~500MB, so we want to avoid putting it in memory or iterating
    over it multiple times. This makes the logic a little more complicated.

    The general idea is this:
    Iterate over the City Network Blocks file
        Iterate over the current geo data
            If the IP from the current geo data matches -> Save the City Block data for this IP
            Else If the location data matches -> Save the City Block data as a suitable replacement
    """
    for data in current_geo_data:
        # This is expensive, so convert once here rather than on every use
        data["ip_object"] = ipaddress.ip_address(data["ip_address"])

    city_network_blocks = {}

    with open(
        GEO_CITY_NETWORK_BLOCKS_FILE, encoding="utf-8", newline=""
    ) as city_network_file:
        city_network_reader = csv.DictReader(city_network_file)

        log.info(
            "Beginning read of city_network_blocks_file: %s",
            GEO_CITY_NETWORK_BLOCKS_FILE,
        )
        for city_network_row in city_network_reader:
            geoname_id = city_network_row["geoname_id"]
            if geoname_id == "":
                continue

            network = ipaddress.ip_network(city_network_row["network"])
            location = city_locations[geoname_id]

            for data in current_geo_data:
                # Is the IP address from the current data file within the network range
                if data["ip_object"] in network:
                    city_network_blocks[data["ip_address"]] = city_network_row
                    log.debug("NETWORK MATCH: ip_address: %s", data["ip_address"])
                # If we don't already have a replacement option and this one works then save it
                elif "replacement_ip_option" not in data and location_data_matches(
                    data, city_network_row, location
                ):
                    replacement_ip_option = get_ip_within_network(network)
                    city_network_blocks[replacement_ip_option] = city_network_row
                    data["replacement_ip_option"] = replacement_ip_option
                    log.debug(
                        "NETWORK REPLACEMENT FOUND: ip_address: %s, %s",
                        data["ip_address"],
                        replacement_ip_option,
                    )

        log.info("Done reading city_network_blocks_file")

    return city_network_blocks


def location_data_matches(current_geo_data_row, city_network_row, city_location):
    """Returns True if the location data matches otherwise False"""
    return (
        current_geo_data_row["postcode"] in (city_network_row["postal_code"], "")
        and current_geo_data_row["country"] in (city_location["country_iso_code"], "")
        and current_geo_data_row["region"] in (city_location["subdivision_1_name"], "")
        and current_geo_data_row["city"] in (city_location["city_name"], "")
        and current_geo_data_row["dma"] in (city_location["metro_code"], "")
    )


def get_ip_within_network(network):
    """Return a string representation of an IP that is within the given network"""
    if isinstance(network.hosts(), Iterator):
        return str(next(network.hosts()))

    return str(network.hosts()[0])


def determine_ips_to_output(current_geo_data, city_locations, city_network_blocks):
    """Returns a List of ips that should be written to the output file

    Includes ips that had no change in their location data, so are being reused and
    replacement ips for any that did have a change in location data.
    """
    ips_to_output = []

    for row in current_geo_data:
        ip_address = row["ip_address"]
        (change_found, change_reason) = check_for_data_change(
            row, city_locations, city_network_blocks
        )

        if change_found:
            if "replacement_ip_option" in row:
                replacement_ip = row["replacement_ip_option"]
                log.info(
                    "CHANGE FOUND for IP: %s - (%s). Using replacement %s",
                    ip_address,
                    change_reason,
                    replacement_ip,
                )
                ips_to_output.append(replacement_ip)
            else:
                log.error(
                    "ERROR: CHANGE FOUND for IP: %s - (%s). No replacement IP found",
                    ip_address,
                    change_reason,
                )
        else:
            ips_to_output.append(ip_address)

    return ips_to_output


def check_for_data_change(data, city_locations, city_network_blocks):
    """Returns a 2 element Tuple: 1st (bool): change found or not, 2nd (string): change reason"""
    ip_address = data["ip_address"]
    postcode = data["postcode"]
    country = data["country"]
    region = data["region"]
    city = data["city"]
    dma = data["dma"]

    if ip_address not in city_network_blocks:
        return (True, "Not found in Network Geo Data.")

    city_network_block = city_network_blocks[ip_address]
    geoname_id = city_network_block["geoname_id"]

    if geoname_id not in city_locations:
        return (True, "Not found in Location Geo Data.")

    city_location = city_locations[geoname_id]

    if postcode not in (city_network_block["postal_code"], ""):
        return (
            True,
            f"Postcode different: {postcode} -> {city_network_block['postal_code']}",
        )

    if country not in (city_location["country_iso_code"], ""):
        return (
            True,
            f"Country different: {country} -> {city_location['country_iso_code']}",
        )

    if region not in (city_location["subdivision_1_name"], ""):
        return (
            True,
            f"Region different: {region} -> {city_location['subdivision_1_name']}",
        )

    if city not in (city_location["city_name"], ""):
        return (True, f"City different: {city} -> {city_location['city_name']}")

    if dma not in (city_location["metro_code"], ""):
        return (True, f"DMA different: {dma} -> {city_location['metro_code']}")

    return (False, "")


def generate_output_file(
    ips_to_output,
    city_network_blocks,
    city_locations,
    isp_data,
    connection_type_data,
):
    """Write a file with the updated set of ips and location data"""
    output_data = []
    for ip_address in ips_to_output:
        geoname_id = ""
        data_row = {"ip_address": ip_address}

        if ip_address in city_network_blocks:
            city_network_block = city_network_blocks[ip_address]
            data_row["postcode"] = city_network_block["postal_code"]
            data_row["lat"] = city_network_block["latitude"]
            data_row["lon"] = city_network_block["longitude"]
            geoname_id = city_network_block["geoname_id"]

        if geoname_id != "" and geoname_id in city_locations:
            city_location = city_locations[geoname_id]
            data_row["country"] = city_location["country_iso_code"]
            data_row["region"] = city_location["subdivision_1_name"]
            data_row["region_iso_code"] = city_location["subdivision_1_iso_code"]
            data_row["city"] = city_location["city_name"]
            data_row["dma"] = city_location["metro_code"]

        if ip_address in isp_data:
            data_row["carrier"] = isp_data[ip_address].organization

        if ip_address in connection_type_data:
            data_row["connection_type"] = connection_type_data[
                ip_address
            ].connection_type

        output_data.append(data_row)

    output_data = sorted(output_data, key=lambda d: d["ip_address"])

    with open(
        GEO_DATA_FILE_OUT, "w", encoding="utf-8", newline=""
    ) as geo_data_file_out:
        out_keys = [
            "ip_address",
            "country",
            "region",
            "region_iso_code",
            "city",
            "postcode",
            "dma",
            "lat",
            "lon",
            "carrier",
            "connection_type",
        ]
        geo_data_writer = csv.DictWriter(geo_data_file_out, out_keys)
        geo_data_writer.writeheader()
        geo_data_writer.writerows(output_data)


def main():
    """Main method of the program"""
    current_geo_data = read_current_geo_data_file()
    city_locations = read_city_locations_file()
    city_network_blocks = read_city_network_blocks_file(
        current_geo_data, city_locations
    )

    ips_to_output = determine_ips_to_output(
        current_geo_data, city_locations, city_network_blocks
    )

    isp_data = read_isp_mmdb(ips_to_output)
    connection_type_data = read_connection_type_mmdb(ips_to_output)

    generate_output_file(
        ips_to_output,
        city_network_blocks,
        city_locations,
        isp_data,
        connection_type_data,
    )


if __name__ == "__main__":
    main()
