# IDP - CITY BIKE
# MADALINA MOGA, 343C3

import paho.mqtt.client as paho
import json
import time
import random

broker = "mosquitto"
port = 1883
mqtt_topic = "station_data"

iterations = 10

battery = 100
battery_level = "safe"
maximum_bikes = 30
maximum_docks = 30

def on_publish_romana(client, userdata, result):
    print("Sensor Piata Romana : Data published.")
    pass

def on_publish_unirii(client, userdata, result):
    print("Sensor Unirii : Data published.")
    pass

def on_publish_eroilor(client, userdata, result):
    print("Sensor Eroilor : Data published.")
    pass

client_romana = paho.Client("romana")
client_romana.on_publish = on_publish_romana
client_romana.connect(broker, port)

client_unirii = paho.Client("unirii")
client_unirii.on_publish = on_publish_unirii
client_unirii.connect(broker, port)

client_eroilor = paho.Client("eroilor")
client_eroilor.on_publish = on_publish_eroilor
client_eroilor.connect(broker, port)

stations_dict = {"piata_romana" : (12345, "true", client_romana), "unirii" : (2342, "false", client_unirii), "eroilor" : (988, "false", client_eroilor)}
battery_dict = {"piata_romana" : 150, "unirii" : 70, "eroilor" : 40}

for i in range(1, iterations):
    for s in stations_dict.keys():
        battery = battery_dict[s]

        if battery > 70 :
            battery_level = "safe"
        elif battery > 30 and battery < 70 :
            battery_level = "alert"
        else : 
            battery_level = "critical"

        battery_dict[s] = battery - 1;

        if battery < 0:
            continue

        t = time.localtime()
        timestamp = time.strftime("%H:%M:%S", t)

        bikes = random.randint(0, maximum_bikes)
        ubikes = random.randint(0, maximum_bikes)

        docks = random.randint(0, maximum_docks)
        udocks = random.randint(0, maximum_docks)

        if random.randint(0, 300) % 5 :
            message = json.dumps({"dispenser": stations_dict[s][1], "keys": "false", "id" : str(stations_dict[s][0]), "name" : s,
                        "battery" : battery_level, "bikes": bikes, "docks": docks, "ubikes": ubikes, "udocks": udocks})
        else :
            message = json.dumps({"dispenser": stations_dict[s][1], "keys": "false", "id" : str(stations_dict[s][0]), "name" : s,
                        "battery" : battery_level, "timestamp": timestamp, "bikes": bikes, "docks": docks, "ubikes": ubikes, "udocks": udocks})

        d = random.randint(1, 30)
        time.sleep(d)

        ret = stations_dict[s][2].publish(mqtt_topic, message)
        stations_dict[s][2].loop()

print("Sensors Stopped")
