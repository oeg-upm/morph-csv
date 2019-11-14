#!/bin/bash
$null=$1
$col=$2
$file=$3

cat ./tmp/$file | cut -d ',' -f$col | sed  -r -e "s/$true/null"
