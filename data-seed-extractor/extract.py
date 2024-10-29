#!python
import argparse

from context import Context
from extractorDelivery import ExtractorDelivery
from extractorInventoryRouter import ExtractorInventoryRouter

parser = argparse.ArgumentParser(
    prog="extract.py",
    description="A tool used to serialize data for our integration tests"
)
parser.add_argument("app_to_extract", choices=['delivery', 'inventory_routers'], help="Which app type we are extracting")
parser.add_argument("case_name", help="Name of the test case")
parser.add_argument("uid", help="UID of the Placement or Inventory Router to be extracted")
parser.add_argument("folder", help="Folder to write the output file")
parser.add_argument("--override-company-name", type=str, nargs='?', default="", const="", help="Name of company to use when uploading the data instead of the default")

args = parser.parse_args()
print(f"Parsed Arguments are: ${vars(args)}")

override_options = None
if 'override_company_name' in args and args.override_company_name != "":
    override_options = {
        'company_name': args.override_company_name
    }

context = Context(args.case_name, args.folder, override_options)

if args.app_to_extract == "delivery":
    print("About to launch extract information for delivery")
    ExtractorDelivery({"uid": args.uid}, context).write_to_folder()

if args.app_to_extract == "inventory_routers":
    print("About to launch extract information for inventory routers")
    ExtractorInventoryRouter(args.uid, context).write_to_folder()
