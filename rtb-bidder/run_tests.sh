#!/bin/bash
#This is for python to know this is the root of the project'
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

help() {
	echo "Types of tests you can run:"
	echo
	echo "all - Run all tests (this is the default)"
	echo "mark:regression - Run tests that are marked 'regression'"
	echo "mark:<custom> - Run tests that are marked <custom>"
	echo "file:<file name> - Run all tests in <file name> (don't include an extension)"
	echo
	echo "Examples: "
	echo "./run_tests.sh mark:regression"
	echo
}

# to use env configuration or default values to re-run execution
rerun_config() {
	RERUN_FAILED_TESTS_NO_OF_TIMES=$DF_CONFIG_RERUN_FAILED_TESTS_NO_OF_TIMES
	RERUN_FAILED_TESTS_DELAY_TIME=$DF_CONFIG_RERUN_FAILED_TESTS_DELAY_TIME

	if test -z "$RERUN_FAILED_TESTS_NO_OF_TIMES"; then
		RERUN_FAILED_TESTS_NO_OF_TIMES=3
	fi

	if test -z "$RERUN_FAILED_TESTS_DELAY_TIME" ; then
		RERUN_FAILED_TESTS_DELAY_TIME=1
	fi
}

run_pytest() {
	rerun_config
	
	DF_NUMBER_OF_PROCESS=$DF_NUMBER_OF_PROCESS_OF_PYTEST

	if [ -z "$DF_NUMBER_OF_PROCESS" ]
		then
			DF_NUMBER_OF_PROCESS=3
	fi

	pytest_static_args="-W ignore::DeprecationWarning:invoke.loader -n $DF_NUMBER_OF_PROCESS  --html=build/report.html --self-contained-html"
	pytest_rerun_args=" --reruns $RERUN_FAILED_TESTS_NO_OF_TIMES --reruns-delay $RERUN_FAILED_TESTS_DELAY_TIME"
	pytest_optional_args="$1"
	echo "Command: pytest $pytest_static_args $pytest_rerun_args $pytest_optional_args"
	pytest $pytest_static_args $pytest_rerun_args $pytest_optional_args
}

input_arg=$1
test_type="$(cut -d ':' -f1 <<< "$input_arg")"

if [ "$input_arg" == "help" ]; then
	help
elif [ -z "$input_arg" ] || [ "$input_arg" == "all" ]; then
	echo "Running all tests"
	run_pytest
elif [ "$test_type" == "mark" ]; then
	mark_name="$(cut -d ':' -f2 <<< "$input_arg")"
	echo "Running tests marked $mark_name"
	run_pytest "-m $mark_name"
elif [ "$test_type" == "file" ]; then
	file_name="$(cut -d ':' -f2 <<< "$input_arg")"
	echo "Running tests in $file_name file"
	run_pytest "-k $file_name"
else
	echo "Not sure what to do with input: [$input_arg]"
	echo
	help
fi
