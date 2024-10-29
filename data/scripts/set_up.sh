#!/bin/bash

echo Run of setup using the path $DATA_PATH

pytest -m "setup" --self-contained-html --html=build/set_up_report.html
