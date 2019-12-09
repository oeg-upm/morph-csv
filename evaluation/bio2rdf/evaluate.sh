#!/bin/bash


echo "dataset,query,time,morphcsv,morphrdb,ontop" >> /results/results-time.csv

cp -r /data/bio2rdf/* /data/
cp -r /data/bio2rdf/* /morphcsv/tmp/csv
for j in 1 2 3 4 5 6 7 8 9 10
do
  for t in 1 2 3 4 5
  do
    start=$(date +%s.%N)
    python3 /morphcsv/morphcsv.py -c /mappings/config-bio2rdf.json -q /queries/bio2rdf/q$j.rq
    finish=$(date +%s.%N)
    morphcsv=$(echo "$finish - $start" | bc)
    cd /morphcsv/tmp/
    start=$(date +%s.%N)
    ./run-morph-rdb.sh
    finish=$(date +%s.%N)
    morphrdb=$(echo "$finish - $start" | bc)
    start=$(date +%s.%N)
    ./run-ontop.sh
    ontop=$(echo "$finish - $start" | bc)
    echo "bio2rdf,$i,$j,$t,$morphcsv,$morphrdb,$ontop" >> /results/results-time.csv
    cd /
  done
  mv /results/results.xml /results/bio2rdf-q$j.xml
done
