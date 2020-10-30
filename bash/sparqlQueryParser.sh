#!/bin/bash
file=$1
cp $file /morphcsv/tmp/annotations/query.rq	
sparqljs $file > /morphcsv/tmp/annotations/sparql.json
wait
