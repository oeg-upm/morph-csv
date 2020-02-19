#!/bin/bash
qNumber=$1
gtfsSize=$2
queryType=$3
round=$4
logFile="/results/gtfsEvaluation.log.txt"

cp /data/* /morphcsv/tmp/csv/
cp /morphcsv/evaluation/gtfs/gtfs.csvw.json tmp/annotations/annotations.json
cp /morphcsv/evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
echo "QUERY: $qNumber ROUND: $round" >> $logFile

start=$(date +%s.%N)
python3 Test.py -c /mappings/config-gtfs.json -q /queries/gtfs/$queryType/q$qNumber.rq >> $logFile
finish=$(date +%s.%N)
morphcsv=$(echo "$finish - $start" | bc)

start=$(date +%s.%N)
docker excec -w /morphcsv morphcsv bash ./tmp/run-morph-rdb.sh
finish=$(date +%s.%N)
morphrdb=$(echo "$finish - $start" | bc)

echo "gtfs-$gtfsSize,$qNumber,$round,$morphcsv,$morphrdb" >> /results/results-time.csv
rm /morphcsv/tmp/csv/*.csv
