#!/bin/bash
date=$(date "+%F-%T")
file="logs/bio2rdf/bio2rdf$date.log.txt"
echo ''> $file
for i in $(seq 1 10)
do
echo "QUERY: $i" >> $file
cat evaluation/bio2rdf/queries/query$i.rq >> $file
cp evaluation/bio2rdf/bio2rdf.csvw.json tmp/annotations/annotations.json
cp evaluation/bio2rdf/bio2rdf.yml tmp/annotations/mapping.yaml
cp ~/Datasets/bio2rdf/* tmp/csv/
time python3 Test.py  -c evaluation/bio2rdf/config-bio2rdf.json -q evaluation/bio2rdf/queries/query$i.rq >> $file
echo "----------------------------------------------------" >> $file
done
