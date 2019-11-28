#!/bin/bash
#source=$1
#query=$2 
#python3 morphcsv.py -c test/config.json -q test/query.rq
cp csvwParser/data/madridGtfs/* tmp/csv/
cp test/gtfs.csvw.json tmp/annotations/annotations.json
cp test/gtfs.mapping.yml tmp/annotations/mapping.yml
python3 morphcsv.py  -c test/configGtfs.json -q test/queryGtfs.rq

#cp utils/parser/oldStuff/tests/gene_info tmp/csv/gene_info.csv
#cp test/ncbigene.annotations.json tmp/annotations/annotations.json
#cp test/ncbigene.mapping.yaml tmp/annotations/mapping.yaml
#python3 morphcsv.py -c test/config.json -q test/ncbigene.query.rq
