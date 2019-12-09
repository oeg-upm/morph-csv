#!/bin/bash


echo "gtfs-size,query,time,morphcsv,morphrdb,ontop" >> /results/results-time.csv
type="original"
for i in 1 #10 100 1000
do
  cp /data/gtfs/gtfs-$i/* /data/
  cp /data/gtfs/gtfs-$i/* /morphcsv/tmp/csv/
  for j in 1 #2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
  do
          for t in 1 #2 3 4 5
          do
            start=$(date +%s.%N)
            python3 morphcsv.py -c /mappings/config-gtfs.json -q /queries/gtfs/$type/q$j.rq
            finish=$(date +%s.%N)
            morphcsv=$(echo "$finish - $start" | bc)
            start=$(date +%s.%N)
            ./tmp/run-morph-rdb.sh
            finish=$(date +%s.%N)
            morphrdb=$(echo "$finish - $start" | bc)
            start=$(date +%s.%N)
            ./tmp/run-ontop.sh
            ontop=$(echo "$finish - $start" | bc)
            echo "gtfs-$i,$j,$t,$morphcsv,$morphrdb,$ontop" >> /results/results-time.csv
          done
          mv /results/results.xml /results/gtfs-$i-q$j.xml
  done
  type="vig"
done

rm /data/*.csv