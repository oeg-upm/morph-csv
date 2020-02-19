#!/bin/bash
echo "gtfs-size,query,time,morphcsv,morphrdb" > /results/results-time.csv
type="original"
for i in 1 #10 100 1000
do
  cp /data/gtfs/gtfs$i/* /data/
  echo "EVALUATING GTFS-$i" > tmp/log.txt
  for j in $(seq 1 18)
  do
	    echo "QUERY: $j" >> tmp/log.txt
	    cat  /queries/gtfs/$type/q$j.rq >> tmp/log.txt
          for t in 1 #2 3 4 5 6
          do
	    echo "ROUND: $t" >> tmp/log.txt
        docker excec morphcsv cp /data/* /morphcsv/tmp/csv/
	    docker excec morphcsv  cp /morphcsv/evaluation/gtfs/gtfs.csvw.json tmp/annotations/annotations.json
	    docker excec morphcsv cp /morphcsv/evaluation/gtfs/gtfs-csv.yaml tmp/annotations/mapping.yaml
            start=$(date +%s.%N)
            docker excec -w /morphcsv morphcsv python3 Test.py -c /mappings/config-gtfs.json -q /queries/gtfs/$type/q$j.rq >> tmp/log.txt
            finish=$(date +%s.%N)
            morphcsv=$(echo "$finish - $start" | bc)
            start=$(date +%s.%N)
            docker excec -w /morphcsv morphcsv bash ./tmp/run-morph-rdb.sh
            finish=$(date +%s.%N)
            morphrdb=$(echo "$finish - $start" | bc)
            echo "gtfs-$i,$j,$t,$morphcsv,$morphrdb" >> /results/results-time.csv
            docker exec -w / postgres bash dropDataBase.sh
            sleep 5
          done
        docker excec morphcsv mv /results/results.xml /results/gtfs-$i-q$j-morphrdb.xml
  	    docker excec morphcsv mv tmp/log.txt /results/gtfs-$i.log.txt
          #mv /morphcsv/tmp/ontop/output.csv /results/gtfs-$i-q$j-ontop.csv
  done
  type="vig"
done

docker excec morphcsv rm /data/*.csv
