#!/bin/bash
#source=$1
#query=$2 

#MotivatingExample
#python3 morphcsv.py -c test/config.json -q test/query.rq

#GTFS
#python3 morphcsv.py  -c evaluation/gtfs/config-gtfs.json -q test/queries/query4.rq

#GENEINFO
#cp evaluation/bio2rdf/ncbigene/ncbigene.annotations.json tmp/annotations/annotations.json
#cp evaluation/bio2rdf/ncbigene/ncbigene.mapping.yaml tmp/annotations/mapping.yaml
#cp evaluation/bio2rdf/ncbigene/gene_info.csv tmp/csv/
#python3 morphcsv.py -c test/config.json -q evaluation/bio2rdf/ncbigene/ncbigene.query.rq

#BIO2RDF:
cp evaluation/bio2rdf/bio2rdf.csvw.json tmp/annotations/annotations.json
cp evaluation/bio2rdf/bio2rdf.yml tmp/annotations/mapping.yaml
python3 morphcsv.py  -c evaluation/bio2rdf/config-bio2rdf.json -q evaluation/bio2rdf/queries/query4.rq

