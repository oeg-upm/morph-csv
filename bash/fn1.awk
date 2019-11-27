#!bin/awk
#EJECUTAR DESDE utils/parser
#awk -f bashScripts/fn1.awk  oldStuff/tests/FN1normalizationExample

BEGIN{
	system("echo \"\\\"id\\\",\\\"value\\\"\" > testing");
}
{
	FS="";
	len=split($0,value,"|");
	if($0 != "null"){
		n="";
		for(i=1;i<=len;++i){
			n=n "\\\"" NR "\\\",\\\"" value[i] "\\\"";
			if(i <=len - 1){
				n= n"\n";
				}
			}
		system("echo \"" n "\" >> testing");
	}# oldStuff/tests/FN1normalizationExample
	if($0 == "null"){
		system("echo \"\\\"" NR "\\\",\\\"Null\\\"\" >> testing")
		}
	$0=NR
	print $0

}
END{
	
	}

