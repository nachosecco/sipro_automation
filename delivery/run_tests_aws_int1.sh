#!/bin/bash

export AEROSPIKE_HOST="aerospike71.int1.rowdy.cc"

export BIDDER_DATA_FILE="data/bidder-data-file-env-int1.dat"

export DATA_FILE="data/data-file-env-int1.csv"

export READ_LOG_STRATEGY="OPEN_SEARCH"

export DELIVERY_ROOT_URL="https://deliveryint1.siprocalads.com"

export READ_LOG_OPEN_SEARCH_HOST="kibana-os-int1.rowdy.cc"

export INVENTORY_ROUTERS_ROOT_URL="https://inventory-routersint1.siprocalads.com"

export INVENTORY_ROUTERS_DATA_FILE="data/data-file-routers-int1.csv"

export DF_MEDIA_SERVER_URL="https://mediaint1.siprocalads.com"

./run_tests.sh $1
