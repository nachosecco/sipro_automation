#!/bin/bash
#This is for python to know this is the root of the project'
if [ -z "$RS_ROUTER_PATH" ]
then
      DELIVERY_PATH=$(dirname "$(pwd)")/delivery
      ROUTER_PATH="$(pwd)"
      RS_ROUTER_PATH="$ROUTER_PATH:$DELIVERY_PATH"
fi

export PYTHONPATH="${PYTHONPATH}:$RS_ROUTER_PATH"


echo "About to start to test in the directory $PYTHONPATH"

#This is for the project, it is similar to PYTHONPATH, but is only used for the project.
AUTOMATION_PATH=$(pwd)
export AUTOMATION_PATH

echo "About to launch tests..."

python -m black .

# NOTE:
# Use -m myTest to run only tests marked as myTest
# Use -rP to get log output for every test case
# Use --log-level=DEBUG to get DEBUG logs

help() {
	echo "Types of tests you can run:"
	echo
	echo "all - Run all tests (this is the default)"
	echo "regression - Run tests that are marked 'regression' for delivery"
	echo "smoke - Run tests that are marked 'smoke'"
	echo "<custom> - Run tests that are marked <custom>"
	echo
	echo "Example: ./run_tests.sh regression"
}
# test_type is the run time input while calling the run_test.sh ,
# If there is no run time input then it will run the all the test cases
test_type=$1


if [ -z "$RS_NUMBER_OF_PROCESS_OF_PYTEST" ]
then
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
