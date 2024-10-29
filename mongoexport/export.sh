#!/bin/bash

set -e

# Set the current date for the output filename
current_date=$(date +"%d-%m-%Y")

# MongoDB export command
mongoexport --username "$MONGO_PS_USERNAME" --password "$MONGO_PS_PASSWORD" --collection=karthick --out=karthik.json mongodb://mongo.v1.example.com:27017,mongo.v1.example.com:27017,mongo.v1.example.com:27017/db-name?replicaSet=app-v1&readPreference=secondary 

sleep 300
# Compress the output file

# cat karthik.json

gzip karthik.json
sleep 60

# Upload to AWS S3
aws s3 cp karthik.json.gz s3://devops-backups/mongo/karthik/$current_date.gz
sleep 60

set +e