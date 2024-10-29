#!/bin/bash

export DATA_FILE="data/data-file-env-qa2.csv"

export READ_LOG_STRATEGY="OPEN_SEARCH"

export DELIVERY_ROOT_URL="https://deliveryqa2.siprocalads.com"

export READ_LOG_OPEN_SEARCH_HOST="kibana-os-qa2.rowdy.cc"

export INVENTORY_ROUTERS_ROOT_URL="https://routerqa2.siprocalads.com"

export INVENTORY_ROUTERS_DATA_FILE="data/data-file-routers-qa2.csv"

export DF_MEDIA_SERVER_URL="https://mediaqa2.siprocalads.com"

export DSE_DASHBOARD_API="https://manageqa2.siprocalads.com"

export AEROSPIKE_HOST="aerospike71.qa2.rowdy.cc"

#export DSE_API_USER="user"
#export DSE_API_PWD="changeme"

./run_tests.sh $1
