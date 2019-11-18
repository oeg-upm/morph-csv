#!/bin/bash

null=$1
col=$2
file=$3
#echo COL:$col NULL:$null FILE:$file
cat ./tmp/$file | cut -d ',' -f$col | sed  -r -e "s/,$null,/,null,/"
