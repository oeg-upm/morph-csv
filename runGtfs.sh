#!/bin/bash
dir="original"
for size in 1 10 100 1000
do 
	for query in $(seq 1 18)
	do
		for round in $(seq 1 5)
			do
			docker exec -w /morphcsv morphcsv bash /morphcsv/runGtfs.sh $size $round $query $dir
			echo "************************************************"
			echo "* GTFS Query: $query Size: $size Round: $round *"
			echo "* Hace referencia a la ejecución de arriba     *"
			echo "************************************************"
			done
	done
dir="vig"
done

