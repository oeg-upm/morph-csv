#!/bin/bash

delimiter= $1
fileName= $(echo "$2")
echo "Delimiter: $delimiter, File: $fileName"
#sed -i -r "s/$delimiter/,/g" ./tmp/$fileName
