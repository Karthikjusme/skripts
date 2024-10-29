#!/bin/bash

DEV_HOST=<dev_host>
PROD_HOST=<prod_host>
PROD_PASSWORD=<password>
DEV_PASSWORD=<password>
set -e
mysqldump -h $PROD_HOST -u root -p$PROD_PASSWORD db_name $1  > $1.sql

sleep 10

mysql -h $DEV_HOST -u db_name -p$DEV_PASSWORD db_name < $1.sql

set +e