#!/bin/bash


echo "dataset,query,time,morphcsv,morphrdb,ontop" >> /results/results-time.csv

for j in 1 2 3 4 5 6 7 8 9 11 12
do
  for t in 1 2 3 4 5
  do
    cp -r /data/*.csv /morphcsv/tmp/csv
    start=$(date +%s.%N)
    python3 morphcsv.py -c /mappings/config-bio2rdf.json -q /queries/bio2rdf/query$j.rq
    finish=$(date +%s.%N)
    morphcsv=$(echo "$finish - $start" | bc)
    start=$(date +%s.%N)
    ./tmp/run-morph-rdb.sh
    finish=$(date +%s.%N)
    morphrdb=$(echo "$finish - $start" | bc)
    start=$(date +%s.%N)
    ./tmp/ontop/run-ontop.sh
    finish=$(date +%s.%N)
    ontop=$(echo "$finish - $start" | git pullbc)
    echo "bio2rdf,$j,$t,$morphcsv,$morphrdb,$ontop" >> /results/results-time.csv
  done
  mv /results/results.xml /results/bio2rdf-q$j-morphrdb.xml
  mv /morphcsv/tmp/ontop/output.csv /results/bio2rdf-q$j-ontop.csv
done