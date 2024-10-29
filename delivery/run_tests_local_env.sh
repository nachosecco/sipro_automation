#!/bin/bash

echo "Please configure delivery & event application to redirect logs to a file."
echo "You can set LOG_PATH_DELIVERY and LOG_PATH_EVENT environment variables to avoid prompt"

if [[ -z "${LOG_PATH_DELIVERY}" ]]; then
  read -rp 'delivery log file:' READ_LOG_PATH_DELIVERY
else
  export READ_LOG_PATH_DELIVERY="${LOG_PATH_DELIVERY}"
fi

if [[ -z "${LOG_PATH_EVENT}" ]]; then
  read  -rp 'event log file:' READ_LOG_PATH_EVENT
else
  export READ_LOG_PATH_EVENT="${LOG_PATH_EVENT}"
fi

export READ_LOG_STRATEGY="LOCAL"

export AEROSPIKE_HOST="localhost"

export BIDDER_DATA_FILE="data/bidder-data-file-env-local.dat"

export DATA_FILE="data/data-file-env-local.csv"

export DELIVERY_ROOT_URL="http://localhost:8050"

export INVENTORY_ROUTERS_ROOT_URL="http://localhost:8111"

./run_tests.sh $1
