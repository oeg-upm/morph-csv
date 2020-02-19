#!/bin/bash
docker exec -w /morphcsv morphcsv bash loadHeaders.sh
type="original"
for i in 1 #10 100 1000
do
  docker exec -w /morphcsv morphcsv bash loadData.sh
  for j in $(seq 1 18)
  do
          for t in 1 #2 3 4 5 6
          do
            docker exec -w /morphcsv morphcsv bash runEvaluation.sh
            docker exec -w / postgres bash dropDataBase.sh
            sleep 5
          done
        docker exec -w /morphcsv morphcsv bash mvResults.sh
  done
  type="vig"
done

