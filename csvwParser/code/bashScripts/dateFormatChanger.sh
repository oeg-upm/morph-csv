#!/bin/bash
params=$1
col=$2
delimiter=$3
file=$4
#echo "PARAMS:$params COL:$col DELIMITER:$delimiter FILE:$file"
if [[ $delimiter == "none" ]] ;
then
	echo "No Delimiter"
	cat ./tmp/$file | cut -d "," -f $col | awk  -F '' '{print $1$2$3$4"-"$5$6"-"$7$8}' 


else
	echo "Delimiter"
	cat ./tmp/$file | cut -d ',' -f $col | awk -F$delimiter "{print $params}"

fi
