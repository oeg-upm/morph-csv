#!/bin/bash
cd tmp/
java -jar morph-rdb.jar es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner csv morph-rdb.properties
cd ..