docker exec postgres psql -U user -d postgres -c "DROP DATABASE IF EXISTS morphcsv"
docker restart postgres
sleep 5
docker exec postgres psql -U user -d postgres -c "CREATE DATABASE morphcsv"
sleep 5
cp tmp/data/gtfs/*.csv tmp/csv/
sed -i 's/\s*$//g' tmp/csv/*.csv
python3 morphcsv.py -c config.json -q naive.rq
