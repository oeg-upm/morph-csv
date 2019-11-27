awk_command = awk -F '\",\"' '{print $1"\" " "\""$2"\" "}'  examples/studentsport/SPORT.csv #SI USAMOS $1
awk_command = awk -F '\",\"' '{print  "\""$2"\" " "\""$3"\" "}'  examples/studentsport/SPORT.csv #SI NO USAMOS $1
