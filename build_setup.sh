#!/bin/bash

sudo useradd -rs /bin/false influxdb

sudo mkdir -p /etc/influxdb

sudo docker run --rm influxdb influxd config | sudo tee /etc/influxdb/influxdb.conf > /dev/null

sudo chown influxdb:influxdb /etc/influxdb/

# Create folder for InfluxDB's data, metadata and WAL
sudo mkdir -p /var/lib/influxdb

sudo chown influxdb:influxdb /var/lib/influxdb

# Use init script
sudo docker run --rm -e INFLUXDB_HTTP_AUTH_ENABLED=true \
         -e INFLUXDB_ADMIN_USER=admin \
         -e INFLUXDB_ADMIN_PASSWORD=admin123 \
         -v /var/lib/influxdb:/var/lib/influxdb \
         -v /home/madalinamoga/Desktop/cityBike/influxdb:/docker-entrypoint-initdb.d \
         influxdb /init-influxdb.sh

sudo docker run -d -p 8086:8086 --user 997:997 --name=influxdb -v /etc/influxdb/influxdb.conf:/etc/influxdb/influxdb.conf -v /var/lib/influxdb:/var/lib/influxdb influxdb -config /etc/influxdb/influxdb.conf

# to test, run: curl -G http://localhost:8086/query --data-urlencode "q=SHOW DATABASES"
