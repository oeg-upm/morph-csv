#!/bin/bash
#source=$1
#query=$2 
#python3 morphcsv.py -c test/config.json -q test/query.rq
rm -r tmp/ results/
python3 morphcsv.py  -c test/configGtfs.json -q test/queryGtfs.rq

