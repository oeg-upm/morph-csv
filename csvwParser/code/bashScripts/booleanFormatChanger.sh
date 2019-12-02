#!/bin/bash
$true=$1
$false=$2
$col=$3
$file=$4

cat ./tmp/$file | cut -d ',' -f$col | sed  -r -e "s/$true/true" -e "s/$false/false"
