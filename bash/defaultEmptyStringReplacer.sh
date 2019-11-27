#!/bin/bash

value=$1
col=$2
file=$3

echo VALUE:$value COL:$col FILE:$file
cat ./tmp/csv/$file | cut -d ',' -f $col | sed -r -e "s/$value//"
