#!/bin/bash
for size in 45 90 180 360
do 
	for query in $(seq 1 12)
	do
		for round in $(seq 1 5)
			do
			docker exec -w /morphcsv morphcsv bash /morphcsv/runBsbm.sh $size $round $query 
                        echo "************************************************"
                        echo "* BSBM Query: $query Size: $size Round: $round *"
                        echo "************************************************"
                        echo "Hace referencia a la ejecución de arriba"
			done
	done
done

