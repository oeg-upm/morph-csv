#!/bin/bash
#source=$1
#query=$2 

#python3 morphcsv.py -c test/config.json -q test/query.rq
# cp csvwParser/data/madridGtfs/* tmp/csv/
# cp  evaluation/gtfs/annotations-csvw.json tmp/annotations/annotations.json
# cp  evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
time python3 morphcsv.py  -c test/configGtfs.json -q test/gtfs.query.rq

#cp utils/parser/oldStuff/tests/gene_info tmp/csv/gene_info.csv
#cp test/ncbigene.annotations.json tmp/annotations/annotations.json
#cp test/ncbigene.mapping.yaml tmp/annotations/mapping.yaml
#python3 morphcsv.py -c test/config.json -q test/query.rq
#python3 morphcsv.py -c test/config.json -q test/query.rq
#python3 morphcsv.py -c test/config.json -q test/query.rq

#cp csvwParser/data/madridGtfs/* tmp/csv/
#cp evaluation/gtfs/annotations-csvw.json tmp/annotations/annotations.json
#cp evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
#python3 morphcsv.py  -c test/configGtfs.json -q test/queryGtfs.rq
