#!/bin/bash

# Change directory to the script location and then the git repository root
# This allows us to run the script from any location and still use paths relative to the repository root
cd "$(dirname "$0")"
cd "$(git rev-parse --show-toplevel)/traffic-shaping"

export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export AWS_DEFAULT_REGION=us-west-2

# Default value
env_name="dev"
test_type="regression"

# get environment name and marker from command line arguments
while [[ "$#" -gt 0 ]]; do
	case $1 in
	-env)
		env_name="$2"
		shift
		;;
	-m)
		test_type="$2"
		shift
		;;
	esac
	shift
done

if [ -f "./config/$env_name.env" ]; then
	source ./config/$env_name.env
else
	echo "Environment file ./config/$env_name.env not found!"
	exit 1
fi

echo "Running against environment: $env_name"

if [ -z "$RS_NUMBER_OF_PROCESS_OF_PYTEST" ]; then
	RS_NUMBER_OF_PROCESS_OF_PYTEST=3
fi

if [ -z "$test_type" ] || [ "$test_type" == "all" ]; then
	echo "Running all tests"
	pytest -n $RS_NUMBER_OF_PROCESS_OF_PYTEST --html=build/report.html --self-contained-html --disable-warnings
elif [ "$test_type" == "smoke" ] || [ "$test_type" == "regression" ]; then
	echo "We are performing $test_type Test "
	pytest -n $RS_NUMBER_OF_PROCESS_OF_PYTEST -m "$test_type" --html=build/report.html --self-contained-html --disable-warnings
else
	echo "We are performing $test_type Test "
	pytest -n $RS_NUMBER_OF_PROCESS_OF_PYTEST -m "$test_type" --html=build/report.html --self-contained-html
fi
