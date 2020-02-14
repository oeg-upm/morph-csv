#!/bin/bash
file=$1
col=$2
dataCol=""
numberOfRows=$(awk -F ',' "{print $col}" $file | wc -l)
numberOfValues=$(awk -F ',' "{print $col}" $file | sort -u | wc -l)
selectivity="$(bc <<< "scale=2; $numberOfValues/$numberOfRows")"
echo $selectivity > tmp/selectivity.tmp.txt
echo "Number of Values:$numberOfValues NumberOfRows:$numberOfRows Selectivity:$selectivity"
