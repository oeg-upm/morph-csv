#!/bin/bash
qNumber=$1
gtfsSize=$2

mv /results/results.xml /results/bio2rdf-query$qNumber-morphrdb.xml
mv /morphcsv/tmp/annotations/mapping.r2rml.ttl /results/bio2rdf-query$qNumber.r2rml.ttl
