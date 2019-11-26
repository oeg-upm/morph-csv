#!/bin/bash
params=$1
col="$"$2
delimiter=$3
file=$4
#echo "PARAMS:$params COL:$col DELIMITER:$delimiter FILE:$file"
awk -F '\t' '{print $col=$(colFormatter)}' ./tmp/$file > tmpFile 
#mv tmp ./tmp/$file
function colFormatter {
	if [[ $delimiter == "none" ]] ;
	then
		echo "No Delimiter"
		cat ./tmp/csv/$file | awk -F '\",\"' '{print $col}' | awk  -F '' '{print $1$2$3$4"-"$5$6"-"$7$8}' 


	else
		echo "Delimiter"
		cat ./tmp/csv/$file | awk -F '\",\"' '{print $col}' | awk -F$delimiter "{print $params}"

	fi
}
