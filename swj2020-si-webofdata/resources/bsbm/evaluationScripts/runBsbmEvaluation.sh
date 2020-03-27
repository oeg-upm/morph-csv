#!/bin/bash
qNumber=$1
bsbmSize=$2
round=$3
logFile="/results/bsbmEvaluation.log.txt"

cp /data/* /morphcsv/tmp/csv/
cp /morphcsv/evaluation/bsbm/bsbm.csvw.json /morphcsv/tmp/annotations/annotations.json
cp /morphcsv/evaluation/bsbm/bsbm.csv.yml /morphcsv/tmp/annotations/mapping.yaml
echo "QUERY: $qNumber ROUND: $round" >> $logFile

start=$(date +%s.%N)
python3 Test.py -c /mappings/config-bsbm.json -q /queries/bsbm/q$qNumber.rq >> $logFile
finish=$(date +%s.%N)
morphcsv=$(echo "$finish - $start" | bc)

start=$(date +%s.%N)
docker excec -w /morphcsv morphcsv bash ./tmp/run-morph-rdb.sh
finish=$(date +%s.%N)
morphrdb=$(echo "$finish - $start" | bc)

echo "bsbm-$bsbmSize,$qNumber,$round,$morphcsv,$morphrdb" >> /results/results-time.csv
rm /morphcsv/tmp/csv/*.csv
