#!/bin/sh -l


git config --system --add safe.directory '*'
python /release-notification.py $1