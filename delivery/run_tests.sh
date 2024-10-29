#!/bin/bash
#This is for python to know this is the root of the project'
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

#if command -v pyenv &> /dev/null
#then
# pyenv activate c6-autodelivery
#fi

echo "About to start to test in the directory $PYTHONPATH"

#This is for the project, it is similar to PYTHONPATH, but is only used for the project.
export AUTOMATION_PATH=$(pwd)

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
	echo "regression_ir - Run tests that are marked 'regression_ir' for inventory routers"
	echo "smoke - Run tests that are marked 'smoke'"
	echo "<custom> - Run tests that are marked <custom>"
	echo
	echo "Example: ./run_tests.sh regression"
}
# test_type is the run time input while calling the run_test.sh ,
# If there is no run time input then it will run the all the test cases
test_type=$1

rerun_config() {
	RERUN_FAILED_TESTS_NO_OF_TIMES=$DF_CONFIG_RERUN_FAILED_TESTS_NO_OF_TIMES
	RERUN_FAILED_TESTS_DELAY_TIME=$DF_CONFIG_RERUN_FAILED_TESTS_DELAY_TIME

	if test -z "$RERUN_FAILED_TESTS_NO_OF_TIMES"; then
		RERUN_FAILED_TESTS_NO_OF_TIMES=5
	fi

	if test -z "$RERUN_FAILED_TESTS_DELAY_TIME" ; then
		RERUN_FAILED_TESTS_DELAY_TIME=1
	fi
}

rerun_config

if [ -z "$DF_NUMBER_OF_PROCESS_OF_PYTEST" ]
then
      DF_NUMBER_OF_PROCESS_OF_PYTEST=3
fi

if [ -z "$test_type" ] || [ "$test_type" == "all" ]; then
	echo "Running all tests"
	pytest -n $DF_NUMBER_OF_PROCESS_OF_PYTEST --html=build/report.html --reruns $RERUN_FAILED_TESTS_NO_OF_TIMES --reruns-delay $RERUN_FAILED_TESTS_DELAY_TIME --self-contained-html --disable-warnings --durations=0 --durations-min=0
elif [ "$test_type" == "smoke" ] || [ "$test_type" == "regression" ]; then
	echo "We are performing $test_type Test "
	pytest -n $DF_NUMBER_OF_PROCESS_OF_PYTEST -m "$test_type" --reruns $RERUN_FAILED_TESTS_NO_OF_TIMES --reruns-delay $RERUN_FAILED_TESTS_DELAY_TIME --html=build/report.html --self-contained-html --disable-warnings --durations=0 --durations-min=0
else
	echo "We are performing $test_type Test "
	pytest -n $DF_NUMBER_OF_PROCESS_OF_PYTEST -m "$test_type" --html=build/report.html --self-contained-html --durations=0 --durations-min=0
fi
