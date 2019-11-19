#!/bin/bash
all='$0'
null=$1
col="$"$2
file=$3
#echo COL:$col NULL:$null FILE:$file
#cat ./tmp/$file | cut -d ',' -f$col | sed  -r -e "s/,$null,/,null,/"
#echo awk -F'\",\"' '{gsub(/\-/,"null",$5); print $0 }' tmp/gene_info
awk -F'\",\"' "{gsub(/\\$null/,\"null\",$col); print $all }" tmp/$file 