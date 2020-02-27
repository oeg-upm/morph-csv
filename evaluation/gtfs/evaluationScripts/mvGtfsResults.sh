#!/bin/bash
qNumber=$1
gtfsSize=$2

mv /results/results.xml /results/gtfs-$gtfsSize-q$qNumber-morphrdb.xml
