#!/bin/bash
cd tmp/
java -cp .:morph-rdb.jar:lib/*:dependency/* es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner ./ morph-rdb.properties || flag=1
cd ..