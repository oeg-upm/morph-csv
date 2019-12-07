#!/bin/bash
#source=$1
#query=$2 

#MotivatingExample
#python3 morphcsv.py -c test/config.json -q test/query.rq

#GTFS
#python3 morphcsv.py  -c test/configGtfs.json -q test/queryGtfs.rq

#GENEINFO
cp evaluation/bio2rdf/ncbigene/ncbigene.annotations.json tmp/annotations/annotations.json
cp evaluation/bio2rdf/ncbigene/ncbigene.mapping.yaml tmp/annotations/mapping.yaml
python3 morphcsv.py -c test/config.json -q evaluation/bio2rdf/ncbigene/ncbigene.query.rq
