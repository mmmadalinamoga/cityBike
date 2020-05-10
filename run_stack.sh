#!/bin/bash

sudo docker-compose -f stack.yml build

sudo docker-compose -f stack.yml up -d

sudo docker-compose -f stack.yml ps

sudo docker-compose -f stack.yml down --volumes

sudo docker stack deploy  --compose-file stack.yml citybike

sudo docker stack services citybike

#sudo docker stack rm citybike

# if swarm not init (address from ifconfig, also used for grafana)
# sudo docker swarm init --advertise-addr 192.168.100.10
