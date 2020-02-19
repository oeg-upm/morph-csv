sudo -u postgres -i psql -c "drop database if exists GTFS;"
sudo systemctl restart postgresql
echo "DATA BASE RESTARTED"
