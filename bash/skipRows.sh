#!/bin/bash
#$1 = Number of SkipRows
#$2 = Path of the file
n=$1
fileName=$2
echo "SKIP: $n FILE $fileName"
awk "FNR > $n { print }" ./tmp/csv/$fileName > ./tmp/csv/$fileName
