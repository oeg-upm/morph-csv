#!/bin/bash
delimiter=$1
filename=$2
#echo " Delimiter:$delimiter File:$filename"
sed -i -r "s/$delimiter/,/g" ./tmp/$filename
