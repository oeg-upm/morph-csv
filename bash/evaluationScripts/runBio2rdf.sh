#!/bin/bash
docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
sleep 5
docker restart postgres
sleep 5
docker restart morphcsv
sleep 5
docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
sleep 5
	for query in $(seq 1 11)
	do
		for round in $(seq 1 5)
			do
			docker exec -w /morphcsv morphcsv bash /morphcsv/runQueryBio2rdf.sh $query $round  
			echo "***********************************************************"
			echo "* 	BIO2RDF  Query: $query  Round: $round		*"
			echo "* 	Hace referencia a la ejecución de arriba     	*"
			echo "***********************************************************"
        		
			docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
		        docker restart postgres
		        sleep 5
		        docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
		        sleep 5

			done
	done

