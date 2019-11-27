#!/bin/bash
delimiter=$1
arg=$2
filename=$3
#echo " Delimiter:$delimiter File:$filename"

#time sed -i -r -e "s/$delimiter/\t/g" ./tmp/$filename
echo DELIMTER:$delimiter ARG:$arg FILE:$filename
awk -F$delimiter "{print $arg}" tmp/$filename > tmp/tmp.txt
mv tmp/tmp.txt tmp/$filename
