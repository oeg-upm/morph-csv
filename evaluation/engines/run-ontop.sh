#!/bin/bash
cd tmp/ontop/
./ontop query -m ../annotations/mapping.r2rml.ttl -p ../ontop.properties -q ../query.rq -o output.csv
cd ..