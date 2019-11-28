#!bin/bash
delimiter=$1
separator=$2
col="\$$3"
newFile=$4
file=$5
echo ''> tmp/csv/$newFile
#awk -F "$delimiter" "{len=split($col,value,\"$separator\");n=\"\";for(i=1;i<=len;++i){n=n \"\\\"\" NR \"\\\",\\\"\" value[i] \"\\\"\";if(i<=len-1){n=n\"\n\";}system(\"echo \"\" n \"\" >> tmp/csv/$newFile\");}$col=NR}" $file
awk -F "$delimiter" "{len=split($col,value,\"$separator\");n=\"\";for(i=1;i<=len;++i){n=n \"\\\"\" NR \"\\\"$delimiter\\\"\" value[i] \"\\\"\";system(\"echo \\\"\" n \"\\\" >> tmp/csv/$newFile\");n=\"\"}$col=NR}" $file
