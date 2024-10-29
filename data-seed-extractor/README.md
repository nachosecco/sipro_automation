# Data Seed Extractor

### Required Environment Variables with examples

- export DSE_DASHBOARD_API=https://managedev.siprocalads.com
- export DSE_INVENTORY_ROUTER_API=https://routerdev.siprocalads.com
- export DSE_API_USER=c6-ui-automation@column6.tv
- export DSE_API_PWD=change_me
- export DSE_ENVIRONMENT=dev
- export DSE_MEDIA_SERVER_URL=https://mediadev.siprocalads.com

### Usage

```
usage: extract.py [-h] [--override-company-name [OVERRIDE_COMPANY_NAME]] {delivery,inventory_routers} case_name uid folder

A tool used to serialize data for our integration tests

positional arguments:
  {delivery,inventory_routers}
                        Which app type we are extracting
  case_name             Name of the test case
  uid                   UID of the Placement or Inventory Router to be extracted
  folder                Folder to write the output file

optional arguments:
  -h, --help            show this help message and exit
  --override-company-name [OVERRIDE_COMPANY_NAME]
                        Name of company to use when uploading the data instead of the default
```

Delivery Example

`./extract.py delivery test_delivery_example 62PKC8MDTP029CQ64B6UT414NO /tmp/`

Inventory Routers Example

`./extract.py inventory_routers test_routers_example 6d9f4fac-fc4d-4c58-adad-b74c6becdbdd /tmp/`
