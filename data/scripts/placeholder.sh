#!/bin/bash

echo Running placeholder

pytest -m "placeholder" --self-contained-html --html=build/placeholder_report.html
