#ª/bin/bash
results="/results/annotations"
cd /morph-rdb
cp ${results}/query.rq ./data/
cp ${results}/mapping.r2rml.ttl ./data/
timeout -s SIGKILL 120m java -XX:-UseGCOverheadLimit  -cp .:morph-rdb.jar:lib/*:dependency/* es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner ./ morph-rdb.properties 
python3 xmlToJson.py
