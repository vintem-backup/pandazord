#!/bin/sh

echo "Waiting for DBs..."

#while ! nc -z $DB_HOST $DB_PORT; do
while ! nc -z postgres_dev $DB_PORT; do
    echo "DB not read"
    sleep 1
done

echo "DB started"

sleep 60 #Tempo para esperar as migrations do django
exec python listening_of_binance_assets_table.py binance_BT_assets_control