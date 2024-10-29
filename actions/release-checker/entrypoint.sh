#!/bin/sh -l



git config --system --add safe.directory '*'
python /release-checker.py $1