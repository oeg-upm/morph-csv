#!/bin/bash
file=$1
sparqljs $file > tmp/annotations/sparql.json
wait
