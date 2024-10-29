#!/bin/bash

echo Running of assertions

pytest -m "regression" --self-contained-html --html=build/test_result.html
