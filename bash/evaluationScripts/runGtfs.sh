#!/bin/bash
dir="original"
docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
sleep 5
docker restart postgres
sleep 5
docker restart morphcsv
sleep 5
docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
sleep 5
for size in 1 #10 100 1000
do 
	for query in $(seq 1 18)
	do
		for round in $(seq 1 5)
			do
			docker exec -w /morphcsv morphcsv bash /morphcsv/runQueryGtfs.sh $size $round $query $dir
			echo "************************************************"
			echo "* GTFS Query: $query Size: $size Round: $round *"
			echo "* Hace referencia a la ejecución de arriba     *"
			echo "************************************************"
        		
			docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
		        docker restart postgres
		        sleep 5
		        docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
		        sleep 5

			done
	done
dir="vig"
done

