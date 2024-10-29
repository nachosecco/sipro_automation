#!/usr/bin/env python3
import argparse
import json
import os

import requests

company_id = os.getenv("RTBRT_COMPANY_ID")
dashboard_server = os.getenv("DSE_DASHBOARD_API")
user = os.getenv("DSE_API_USER")
password = os.getenv("DSE_API_PWD")
env = os.getenv("DSE_ENVIRONMENT")

# Step 1: Set up command-line arguments
parser = argparse.ArgumentParser(
    description="Process JSON test cases files and creates JSON data file."
)
parser.add_argument("--company_id", default=company_id, help="Rtb test Company id")
parser.add_argument("--username", default=user, help="Username for authentication")
parser.add_argument("--password", default=password, help="Password for authentication")
parser.add_argument(
    "--dashboard_server", default=dashboard_server, help="Dashboard server URL"
)
parser.add_argument("--env", default=env, help="target environment JSON data file")

args = parser.parse_args()

# Step 1: Authenticate and get token
url_auth = f"{args.dashboard_server}/v2/auth"
auth_data = {"username": f"{args.username}", "password": f"{args.password}"}
response = requests.post(url_auth, json=auth_data)
response.raise_for_status()
token = response.json()["authorization"]

# Step 2: Get placements
url_placements = f"{args.dashboard_server}/v2/manage/placements"
headers = {"Authorization": f"{token}"}
response = requests.get(url_placements, headers=headers)
response.raise_for_status()
placements_data = response.json()

# Store placements by name in a dictionary
placements_dict = {placement["name"]: placement for placement in placements_data}

# Step 3: Read and process JSON files in 'case' directory and subdirectories
case_dir = "cases"
result = {}
for root, dirs, files in os.walk(case_dir):
    for filename in files:
        if filename.endswith(".json"):
            with open(os.path.join(root, filename), "r") as file:
                json_data = json.load(file)

                # Check if placement name exists in placements_dict
                placement_name = json_data["supply"]["placement"]["name"]
                if placement_name in placements_dict:
                    placement_guid = placements_dict[placement_name]["guid"]
                    test_case_name = os.path.splitext(filename)[0]
                    result[test_case_name] = placement_guid
                    # Associate data
                    print(
                        f"File Name: {test_case_name}, Placement Name: {placement_name}, GUID: {placement_guid}"
                    )

output_file = f"data/data-file-env-{args.env}.json"
with open(output_file, "w") as output_json:
    json.dump(result, output_json)
