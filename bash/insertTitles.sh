#!/bin/bash
#echo "inserting $1 on $2"
#head -2 ./tmp/csv/$2
ex -sc "1i|$1" -cx ./tmp/csv/$2
#head -2 ./tmp/csv/$2
