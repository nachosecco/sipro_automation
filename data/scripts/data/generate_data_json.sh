ENV=$1
DASHBOARD_USER=$2
DASHBOARD_PSW=$3
DASHBOARD_API=$4
EXECUTION_ID=$5

DATA_PATH=$(pwd)
UPLOAD_PATH="$(dirname "$DATA_PATH")/data-seed-upload/"

export PYTHON_PATH="$DATA_PATH"

echo "Copying test case json files to build/data/cases/"
python scripts/data/data_generator.py --execution_id="$EXECUTION_ID" --origin_path="cases" --destination_path="build/data/cases/"

echo "Copy of placeholder json file to build/data/placeholder/"
python scripts/data/data_generator.py --execution_id="$EXECUTION_ID" --origin_path="resources/placeholder" --destination_path="build/data/placeholder/"


echo "Preparing to upload all json files"

export DSE_DASHBOARD_API=$DASHBOARD_API
export DSE_API_USER=$DASHBOARD_USER
export DSE_API_PWD=$DASHBOARD_PSW
export DSE_MEDIA_SERVER_URL=https://media$ENV.siprocalads.com
export PYTHON_PATH="$UPLOAD_PATH"

cd $UPLOAD_PATH

echo "we are going to upload all json files (cases & placeholder)"
python upload.py delivery "$DATA_PATH/build/data/"
