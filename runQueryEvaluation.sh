#!/bin/bash 
qNumber=$1
size=$2
round=$3
qType=$4
resultPath="/results/log.txt"
cp /data/* /morphcsv/tmp/csv/
cp /morphcsv/evaluation/gtfs/gtfs.csvw.json tmp/annotations/annotations.json
cp /morphcsv/evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
echo "************************************" >> $resultPath
echo "QUERY:$qNumber ROUND:$round" >> $resultPath
cat /queries/gtfs/$qType/q$qNumber.rq >> $resultPath
start=$(date +%s.%N)
python3 Test.py -c /mappings/config-gtfs.json -q /queries/gtfs/$qType/q$qNumber.rq >> $resultPath
finish=$(date +%s.%N)
morphcsv=$(echo "$finish - $start" | bc)
start=$(date +%s.%N)
bash ./tmp/run-morph-rdb.sh
finish=$(date +%s.%N)
morphrdb=$(echo "$finish - $start" | bc)
echo "gtfs-$size,$qNumber,$round,$morphcsv,$morphrdb" >> /results/results-time.csv
