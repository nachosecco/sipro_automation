# Data Seed Uploader

### Required Environment Variables with examples

- export DSE_DASHBOARD_API=https://managedev.siprocalads.com
- export DSE_INVENTORY_ROUTER_API=https://routerdev.siprocalads.com
- export DSE_API_USER=c6-ui-automation@column6.tv
- export DSE_API_PWD=change_me-
- export DSE_MEDIA_SERVER_URL=https://mediadev.siprocalads.com

### Usage

```
usage: upload.py [-h] [--upload-all] {delivery,inventory_routers} path

A tool used to upload data serialized by data-seed-extractor

positional arguments:
  {delivery,inventory_routers}
                        Which app type we are uploading
  path                  Path to file or folder to be uploaded

optional arguments:
  -h, --help            show this help message and exit
  --upload-all          Upload all data even if the placement already exists
```

Delivery Example

`./upload.py delivery path_to_file_or_directory`

Inventory Routers Example

`./upload.py inventory_routers path_to_file_or_directory`

