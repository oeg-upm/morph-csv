#!/bin/bash
date=$(date "+%F-%T")
file="logs/gtfs/gtfs$date.log.txt"
echo ''> $file
for i in $(seq 1 18)
do
echo "QUERY: $i" >> $file
cat  evaluation/gtfs/queries/original/q$i.rq >> $file
cp ~/Datasets/Gtfs/* tmp/csv/
cp evaluation/gtfs/gtfs.csvw.json tmp/annotations/annotations.json
cp evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
python3 Test.py  -c evaluation/gtfs/config-gtfs.json -q evaluation/gtfs/queries/original/q$i.rq >> $file
wait
echo "----------------------------------------------------" >> $file
done
