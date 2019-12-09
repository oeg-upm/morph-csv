#!/bin/bash
cd ./tmp/annotations
yarrrml-parser -i ./mapping.yaml -o ./mapping.r2rml.ttl -f R2RML
wait
