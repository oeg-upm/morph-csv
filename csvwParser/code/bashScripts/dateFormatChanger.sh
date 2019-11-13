params=$1
col=$2
delimiter=$3
file=$4
if [$delimiter != 'none'];
then
	echo "DELIMITER:$delimiter"
	cat ./tmp/$file | cut -d ',' -f $col | awk -F$delimiter "{print $params}"

else
	echo "No delimiter"
	#cat ./tmp/$file  | cut -d "," -f $col | awk 'BEGIN{FS=OFS=","} NR>1{cmd = "date -d \"" $1 "\" \"+%Y-%m-%d\""; cmd | getline out; $1=out; close("uuidgen")} 1'
	cat ./tmp/$file | cut -d "," -f $col | awk  -F '' '{print $1$2$3$4"-"$5$6"-"$7$8}' 
fi
