#!/bin/bash
#Use Riot to migrate data from one redis server to another
#Run Riot as docker and mount the folder as a volume and run this script
echo "Migration Started"
set +e

riot replicate redis://ec-1.internal.example.com:6379/0    redis://ec-2.internal.example.com:6379/80

set -e
echo "Migration Completed"