#!/bin/bash
q=$1
cd /morphcsv
python3 /morphcsv/morphcsv.py -d -c /server/tmp/config.json $q 
wait
sleep 5
rm -r /results/*
cp -r /morphcsv/tmp/annotations/ /results/annotations/ 
cp -r /morphcsv/tmp/csv/processeds/ /results/csv/ 
wait
sleep 5
