#!/bin/bash
#source=$1
#query=$2 

#MotivatingExample
#python3 morphcsv.py -c test/config.json -q test/query.rq

#GTFS
python3 morphcsv.py  -c evaluation/gtfs/configGtfs.json -q evaluation/gtfs/query6.rq

#GENEINFO
#cp evaluation/bio2rdf/ncbigene/ncbigene.annotations.json tmp/annotations/annotations.json
#cp evaluation/bio2rdf/ncbigene/ncbigene.mapping.yaml tmp/annotations/mapping.yaml
#cp evaluation/bio2rdf/ncbigene/gene_info.csv tmp/csv/
#python3 morphcsv.py -c test/config.json -q evaluation/bio2rdf/ncbigene/ncbigene.query.rq

#BIO2RDF:
#python3 morphcsv.py  -c evaluation/bio2rdf/config.json -q evaluation/bio2rdf/queries/query11.rq

