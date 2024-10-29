#!/bin/bash

# USAGE: bash test.sh <db-name> <custom-psql-url>
set +e

#CHange Password.
OLD_PSQL_URL=<old-rds-psql-url>
NEW_PSQL_URL=<new-rds-psql-url>
export PGPASSWORD=<password>

pg_dump -h $OLD_PSQL_URL -p 5432 -U postgres -d $1 -F c -b -v -f $1.dump

pg_restore -h $NEW_PSQL_URL -p 5432 -U postgres -d $1 -v -c -1 $1.dump

# Define the filename
FILENAME="$1.json"

# Create the file and write JSON content into it
cat <<EOL > $FILENAME
{
    "Comment": "Updating CNAME record for $2",
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "$2",
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "$NEW_PSQL_URL"
                    }
                ]
            }
        }
    ]
}
EOL

aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch file:///data/psql/$1.json

# Display a message
echo "$2 has been successfully updated"

set -e