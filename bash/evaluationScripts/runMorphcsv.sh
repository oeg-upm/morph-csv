#!/bin/bash 

echo "***********************INICIO GTFS*****************************"
bash runGtfs.sh
echo "***********************FIN GTFS*****************************"

echo "***********************INICIO BSBM*****************************"
bash runBsbm.sh 
echo "***********************FIN BSBM*****************************"

