#!/bin/bash


echo "dataset,query,time,morphcsv,morphrdb,ontop" >> /results/results-time.csv

cp -r /data/bio2rdf/* /data/

for j in 1 2 3 4 5 6 7 8 9 10
do
  for t in 1 2 3 4 5
  do
    cp -r /data/* /morphcsv/tmp/csv
    start=$(date +%s.%N)
    python3 morphcsv.py -c /mappings/config-bio2rdf.json -q /queries/bio2rdf/q$j.rq
    finish=$(date +%s.%N)
    morphcsv=$(echo "$finish - $start" | bc)
    start=$(date +%s.%N)
    ./tmp/run-morph-rdb.sh
    finish=$(date +%s.%N)
    morphrdb=$(echo "$finish - $start" | bc)
    start=$(date +%s.%N)
    ./tmp/ontop/run-ontop.sh
    ontop=$(echo "$finish - $start" | bc)
    echo "bio2rdf,$i,$j,$t,$morphcsv,$morphrdb,$ontop" >> /results/results-time.csv
  done
  mv /results/results.xml /results/bio2rdf-q$j-morphrdb.xml
  mv /morphcsv/tmp/ontop/output.csv /results/bio2rdf-q$j-ontop.csv
done
