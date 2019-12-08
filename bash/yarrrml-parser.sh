#!/bin/bash
cd ./tmp/annotations
/usr/local/bin/yarrrml-parser -i ./mapping_aux.yml -o ./mapping.r2rml.ttl -F R2RML
