#!/bin/bash
qNumber=$1
round=$2
logFile="/results/bio2rdfEvaluation.log.txt"

cp /data/* /morphcsv/tmp/csv/
cp /morphcsv/evaluation/bio2rdf/bio2rdf.csvw.json tmp/annotations/annotations.json
cp /morphcsv/evaluation/bio2rdf/bio2rdf.yml tmp/annotations/mapping.yaml

echo "QUERY: $qNumber ROUND: $round" >> $logFile
start=$(date +%s.%N)
python3 Test.py -c /mappings/config-bio2rdf.json -q /queries/bio2rdf/query$qNumber.rq >> $logFile
finish=$(date +%s.%N)
morphcsv=$(echo "$finish - $start" | bc)

start=$(date +%s.%N)
bash ./tmp/run-morph-rdb.sh
finish=$(date +%s.%N)
morphrdb=$(echo "$finish - $start" | bc)

echo "$qNumber,$round,$morphcsv,$morphrdb" >> /results/results-time.csv
rm /morphcsv/tmp/csv/*.csv
