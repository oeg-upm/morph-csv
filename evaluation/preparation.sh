#!/bin/bash
cd ..
cp -r /morphcsv/evaluation/engines/* /morphcsv/tmp/
chmod +x /morphcsv/tmp/*.sh
cd /morphcsv/tmp/
wget https://github.com/ontop/ontop/releases/download/ontop-3.0.0/ontop-cli-3.0.0.zip
unzip ontop-cli-3.0.0.zip -d ontop
mv /morphcsv/tmp/run-ontop.sh /morphcsv/tmp/ontop/
cd /morphcsv/tmp/ontop/jdbc/
wget https://jdbc.postgresql.org/download/postgresql-42.2.9.jar
cd ../../
wget -O morph-rdb.jar https://github.com/oeg-upm/morph-rdb/releases/download/v3.12.5/morph-rdb-dist-3.12.5-jar-with-dependencies.jar
cd /
#gtfs
cp /morphcsv/evaluation/gtfs/gtfs.csvw.json /mappings/
cp /morphcsv/evaluation/gtfs/gtfs-csv.yaml /mappings/
cp /morphcsv/evaluation/gtfs/config-gtfs.json /mappings/
mkdir /queries/gtfs
cp -r /morphcsv/evaluation/gtfs/queries/* /queries/gtfs/
cp /morphcsv/evaluation/gtfs/evaluate.sh /evaluate-gtfs.sh

#bio2rdf
cp /morphcsv/evaluation/bio2rdf/bio2rdf.csvw.json /mappings/
cp /morphcsv/evaluation/bio2rdf/bio2rdf.yml /mappings/
cp /morphcsv/evaluation/bio2rdf/config-bio2rdf.json /mappings/
mkdir /queries/bio2rdf
cp -r /morphcsv/evaluation/bio2rdf/queries/* /queries/bio2rdf/
cp /morphcsv/evaluation/bio2rdf/evaluate.sh /evaluate-bio2rdf.sh
#data
#use the csv with links inside the evaluation folders to download the data manually