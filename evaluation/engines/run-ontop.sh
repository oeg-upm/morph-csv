#!/bin/bash
cd tmp/ontop/
./ontop mapping to-obda -i ../annotations/mapping.r2rml.ttl -o ../annotations/mapping.obda
sed -i "s/a \"\(http.*\)\"^^xsd:string/a <\1>/g" ../annotations/mapping.obda
./ontop query -m ../annotations/mapping.obda -p ../ontop.properties -q ../query.rq -o output.csv
cd ..