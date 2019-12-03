#!/bin/bash
#source=$1
#query=$2 
#python3 morphcsv.py -c test/config.json -q test/query.rq
#python3 morphcsv.py -c test/config.json -q test/query.rq

cp csvwParser/data/madridGtfs/* tmp/csv/
cp evaluation/gtfs/annotations-csvw.json tmp/annotations/annotations.json
cp evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
python3 morphcsv.py  -c test/configGtfs.json -q test/queryGtfs.rq

