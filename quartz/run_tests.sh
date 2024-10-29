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
	echo "./run_tests.sh file:test_liveramp_cookie_and_segment_v1_job"
	echo
}

run_pytest() {
	pytest_static_args="-W ignore::DeprecationWarning:invoke.loader --html=build/report.html --self-contained-html"
	pytest_optional_args="$1"
	echo "Command: pytest $pytest_static_args $pytest_optional_args"
	pytest $pytest_static_args $pytest_optional_args
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
