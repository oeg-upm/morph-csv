#!/bin/bash
size=$1
round=$2
query=$3
dir=$4
annotations="/morphcsv/tmp/annotations/"
cp /data/bsbm/${size}k/*.csv tmp/csv/
python3 morphcsv.py -c /data/bsbm/bsbmconfig.json -q /data/bsbm/queries/q${query}.rq
bash moveResults.sh "bsbm" $size $round $query
