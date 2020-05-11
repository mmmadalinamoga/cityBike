# IDP - CITY BIKE
# MADALINA MOGA, 343C3
#
# This emulates sensor data

import paho.mqtt.client as paho
import json
import time
import datetime
import random

# MQTT settings
broker = "mosquitto"
port = 1883
mqtt_topic = "station_data"

# Sensor initial values
battery = 100
battery_level = "safe"
maximum_bikes = 30
maximum_docks = 30

# Used for debugging
def on_publish_romana(client, userdata, result):
    print("Sensor Piata Romana : Data published.")
    pass

def on_publish_unirii(client, userdata, result):
    print("Sensor Unirii : Data published.")
    pass

def on_publish_eroilor(client, userdata, result):
    print("Sensor Eroilor : Data published.")
    pass

# Init mqtt clients
client_romana = paho.Client("romana")
client_romana.on_publish = on_publish_romana
client_romana.connect(broker, port)

client_unirii = paho.Client("unirii")
client_unirii.on_publish = on_publish_unirii
client_unirii.connect(broker, port)

client_eroilor = paho.Client("eroilor")
client_eroilor.on_publish = on_publish_eroilor
client_eroilor.connect(broker, port)

stations_dict = {"piata_romana" : (12345, "true", client_romana), "unirii" : (2342, "true", client_unirii), "eroilor" : (988, "false", client_eroilor)}
battery_dict = {"piata_romana" : 80, "unirii" : 65, "eroilor" : 50}

# Generate sensor data and publish it using mqtt
while True:
    for s in stations_dict.keys():

        bikes = random.randint(0, maximum_bikes)
        ubikes = random.randint(0, maximum_bikes)

        docks = random.randint(0, maximum_docks)
        udocks = random.randint(0, maximum_docks)

        battery = battery_dict[s]

        h = datetime.datetime.now().hour
        if h >= 4 and h <= 10 :
            battery = battery + 0.1 * h
        elif h > 10 and h <= 16 :
            battery = battery + 0.2 * h
        elif h > 16 and h < 21 :
            battery = battery - 0.1 * h
        else : 
            if h < 4 :
                bikes = random.randint(20, maximum_bikes)
                docks = random.randint(0, 5)
            battery = battery - 0.02  

        if battery > 70 :
            battery_level = "safe"
        elif battery > 30 and battery < 70 :
            battery_level = "alert"
        else : 
            battery_level = "critical"

        battery_dict[s] = battery

        if battery < 0:
            continue

        t = time.localtime()
        timestamp = time.strftime("%H:%M:%S", t)

        if bikes % 2 == 0:
            available_keys = "true"
        else:
            available_keys = "false"

        if random.randint(0, 300) % 5 :
            message = json.dumps({"dispenser": stations_dict[s][1], "keys": available_keys, "id" : str(stations_dict[s][0]), "name" : s,
                        "battery" : battery_level, "bikes": bikes, "docks": docks, "battery_value": battery, "ubikes": ubikes, "udocks": udocks})
        else :
            message = json.dumps({"dispenser": stations_dict[s][1], "keys": available_keys, "id" : str(stations_dict[s][0]), "name" : s,
                        "battery" : battery_level, "timestamp": timestamp, "bikes": bikes, "docks": docks, "battery_value": battery, "ubikes": ubikes, "udocks": udocks})

        d = random.randint(1, 30)
        time.sleep(d)

        ret = stations_dict[s][2].publish(mqtt_topic, message)
        stations_dict[s][2].loop()

print("Sensors Stopped")
