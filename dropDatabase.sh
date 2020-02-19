#!/bin/bash

sudo -u postgres -i psql -c "drop database if exists morphcsv;"
sudo systemctl restart postgresql
echo "DATA BASE RESTARTED"
