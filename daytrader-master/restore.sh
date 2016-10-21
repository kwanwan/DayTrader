#!/bin/bash

username=$1
password=$2
idDomain=$3
jcsInstance=$4
backupId=$5

echo "Restoring backup: $backupId"

curl -s -i -X POST -H Content-Type:application/json -u $username:$password --data {"'"backupId"'":"'"$backupId"'"} -H X-ID-TENANT-NAME:$idDomain https://jaas.oraclecloud.com/jaas/api/v1.1/instances/$idDomain/$jcsInstance/restoredbackups -o response.json

cat response.json

jobId=`cat response.json | grep job_id | awk -F, {'print $2'} | awk -F: {'gsub(/"/, "", $2); print $2'}`
if [ -z "$jobId" ]; then
    echo "Restore Job ID not identified"
    exit 1
else
    echo "Restore Job ID $jobId"
fi

status=Unknown
while [ "$status" != "Completed" ]
do
    echo "Checking job status..."
    sleep 90s
    curl -s -i -X GET -u $username:$password -H X-ID-TENANT-NAME:$idDomain https://jaas.oraclecloud.com/jaas/api/v1.1/instances/$idDomain/$jcsInstance/restoredbackups/$jobId -o response.json
    status=`cat response.json | grep status | awk -F, {'print $6'} | awk -F: {'gsub(/"/, "", $2); print $2'}`
done

echo "Restore successfully completed!"