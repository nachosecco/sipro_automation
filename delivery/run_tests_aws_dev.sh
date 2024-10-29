#!/bin/bash

export AEROSPIKE_HOST="aerospike71.dev.rowdy.cc"

export BIDDER_DATA_FILE="data/bidder-data-file-env-dev.dat"

export DATA_FILE="data/data-file-env-dev.csv"

export READ_LOG_STRATEGY="OPEN_SEARCH"

export DELIVERY_ROOT_URL="https://deliverydev.siprocalads.com"

export READ_LOG_OPEN_SEARCH_HOST="kibana-os-dev.rowdy.cc"

export INVENTORY_ROUTERS_ROOT_URL="https://routerdev.siprocalads.com"

export INVENTORY_ROUTERS_DATA_FILE="data/data-file-routers-dev.csv"

export DF_MEDIA_SERVER_URL="https://mediadev.siprocalads.com"

./run_tests.sh $1
