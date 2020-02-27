date=$(date "+%F-%T")
file="logs/bsbm/bsbm.$date.log.txt"
echo "LOG BSBM-1 DATE:$date" > $file
for i in 1 #2 3 4 5 7 8 10 11
do
echo "QUERY: $i" >> $file
cat evaluation/bsbm/queries/q$i.rq >> $file
cp evaluation/bsbm/bsbm.csv.yml tmp/annotations/mapping.yaml
cp evaluation/bsbm/bsbm.csvw.json tmp/annotations/annotations.json
cp ~/Datasets/bsbm/scale100000/* tmp/csv/
python3 Test.py  -c evaluation/bio2rdf/config-bio2rdf.json -q evaluation/bsbm/queries/q$i.rq >> $file
echo '------------------------------------------------------------------' >> $file
done
