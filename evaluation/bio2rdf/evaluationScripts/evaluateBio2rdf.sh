#!/bin/bash

#PREPARATION

sudo echo "MORPH-CSV+MORPH-RDB BIO2RDF EVALUATION" > results/results-time.csv
sudo echo "query,time,morphcsv,morphrdb" >> results/results-time.csv
docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
docker exec -w /morphcsv morphcsv bash loadBio2rdfData.sh
for j in 1 2 4 6 7 12 13 14 17
 do
    for t in 1 2 3 4 5
        do
            echo "QUERY: $j ROUND:$t"
            docker exec -w /morphcsv morphcsv bash runBio2rdfEvaluation.sh $j $t
            docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
	        docker restart postgres
            sleep 5
	        docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
	        sleep 5
        done
        docker exec -w /morphcsv morphcsv bash mvResults.sh $j
  done
