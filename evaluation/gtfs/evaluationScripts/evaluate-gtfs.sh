#!/bin/bash
queryType="original"

#PREPARATION
sudo rm results/*
sudo echo "gtfs-size,query,time,morphcsv,morphrdb" > results/results-time.csv
docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"

for i in 1 10 100 1000
do
  docker exec -w /morphcsv morphcsv bash loadData.sh $i
  for j in 1 2 4 6 7 12 13 14 17
  do
          for t in 1 2 3 4 5 
          do
            docker exec -w /morphcsv morphcsv bash runEvaluation.sh $j $i $queryType $t
            docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv" 
	    docker restart postgres
            sleep 5
	    docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
	    sleep 5
          done
        docker exec -w /morphcsv morphcsv bash mvResults.sh $j $i
  done
  queryType="vig"
done

