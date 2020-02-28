#!/bin/bash
cd tmp/
timeout -s SIGKILL 120m java -XX:-UseGCOverheadLimit  -cp .:morph-rdb.jar:lib/*:dependency/* es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner ./ morph-rdb.properties 
cd ..
