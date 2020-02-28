#!/bin/bash
qNumber=$1
bsbmSize=$2
mv /results/results.xml /results/bsbm-$bsbmSize-q$qNumber-morphrdb.xml
mv /morphcsv/tmp/annotations/mapping.r2rml.ttl /results/bsbm-q$qNumber.r2rml.ttl
