#!/bin/bash
#source=$1
#query=$2

#MotivatingExample
#cp evaluation/motivating-example/annotations.json tmp/annotations/
#cp evaluation/motivating-example/mapping.yaml tmp/annotations/
#cp evaluation/motivating-example/data/* tmp/csv/
#python3 morphcsv.py -c test/config.json -q evaluation/motivating-example/queries/query1.rq

#GTFS
#cp ~/Datasets/Gtfs/* tmp/csv/
#cp evaluation/gtfs/gtfs.csvw.json tmp/annotations/annotations.json
#cp evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
#python3 Test.py  -c evaluation/gtfs/config-gtfs.json -q evaluation/gtfs/queries/original/q9.rq

#GENEINFO
#cp evaluation/bio2rdf/ncbigene/ncbigene.annotations.json tmp/annotations/annotations.json
#cp evaluation/bio2rdf/ncbigene/ncbigene.mapping.yaml tmp/annotations/mapping.yaml
#cp evaluation/bio2rdf/ncbigene/gene_info.csv tmp/csv/
#python3 morphcsv.py -c test/config.json -q evaluation/bio2rdf/ncbigene/ncbigene.query.rq

#BIO2RDF:
#cp evaluation/bio2rdf/bio2rdf.csvw.json tmp/annotations/annotations.json
#cp evaluation/bio2rdf/bio2rdf.yml tmp/annotations/mapping.yaml
#cp ~/Datasets/bio2rdf/* tmp/csv/
#python3 Test.py  -c evaluation/bio2rdf/config-bio2rdf.json -q evaluation/bio2rdf/queries/query9.rq

#BSBM
cp evaluation/bsbm/bsbm.csv.yml tmp/annotations/mapping.yaml
cp evaluation/bsbm/bsbm.csvw.json tmp/annotations/annotations.json
#cp ~/Datasets/bsbm/scale100000/* tmp/csv/
python3 Test.py  -c evaluation/bio2rdf/config-bio2rdf.json -q evaluation/bsbm/queries/q7.rq
