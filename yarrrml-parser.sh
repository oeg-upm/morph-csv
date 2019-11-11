#!/bin/bash
cd examples
/usr/local/bin/yarrrml-parser -i ./mapping_aux.yml -o ./mapping.rml.ttl
rm mapping_aux.yml
