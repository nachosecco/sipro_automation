#!/bin/bash

export AEROSPIKE_HOST="aerospike71.qa1.rowdy.cc"

export BIDDER_DATA_FILE="data/bidder-data-file-env-qa1.dat"

export DATA_FILE="data/data-file-env-qa1.csv"

export READ_LOG_STRATEGY="OPEN_SEARCH"

export DELIVERY_ROOT_URL="https://deliveryqa1.siprocalads.com"

export READ_LOG_OPEN_SEARCH_HOST="kibana-os-qa1.rowdy.cc"

export INVENTORY_ROUTERS_ROOT_URL="https://routerqa1.siprocalads.com"

export INVENTORY_ROUTERS_DATA_FILE="data/data-file-routers-qa1.csv"

export DF_MEDIA_SERVER_URL="https://mediaqa1.siprocalads.com"

export DSE_DASHBOARD_API="https://manageqa1.siprocalads.com"



./run_tests.sh $1
