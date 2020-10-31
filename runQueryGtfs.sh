#!/bin/bash
size=$1
round=$2
query=$3
dir=$4
annotations="/morphcsv/tmp/annotations/"
cp /data/gtfs/gtfs_$size/*.csv tmp/csv/
python3 morphcsv.py -c /data/gtfs/gtfsconfig_${size}.json -q /data/gtfs/$dir/q${query}.rq
bash moveResults.sh "gtfs" $size $round $query
