#!/bin/bash
i=$1
cp /data/bio2rdf/*.csv tmp/csv/
python3 morphcsv.py -c /data/bio2rdf/bio2rdfconfig.json -q /morphcsv/testNormalization.rq
mv /morphcsv/tmp/execution_times.csv /results/execution_times_bio2rdf_$i.csv
