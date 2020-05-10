# IDP - CITY BIKE
# MADALINA MOGA, 343C3

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import json
import time


# Upon connecting to the mqtt broker, subscribe to all 
# its topics
def on_connect(client_mqtt, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client_mqtt.subscribe("station_data")

# Upon receiving a message, write it to the
# influx database
def on_message(client_mqtt, userdata, msg):
    msg_decoded = str(msg.payload.decode())
    print("Message received", msg_decoded)
    
    # Unpack received data in a dictionary:
    received_dict = json.loads(msg_decoded)
    print("Dict received", received_dict)

    # Add local timestamp if no timestamp was found    
    if "timestamp" in received_dict.keys():
        timestamp = received_dict["timestamp"]
    else: 
        t = time.localtime()
        timestamp = time.strftime("%H:%M:%S", t)

    message_body = [{"measurement":"station_data",
    				 "tags" : { "bike_key_dispenser": received_dict["dispenser"],
                				"bike_keys_available": received_dict["keys"],
    				 			"id" : received_dict["id"],
    				 			"name" : received_dict["name"],
    				 			"battery" : received_dict["battery"],
    				},
    				"timestamp" : timestamp,
    				"fields" : {
    							"available_bikes": received_dict["bikes"],
                				"available_docks": received_dict["docks"],
                				"unavailable_bikes": received_dict["ubikes"],
                				"unavailable_docks": received_dict["udocks"]
    				}
    				}]

    client_db.write_points(message_body);
    #result = client_db.query("SELECT available_bikes from station_data;")
    result = client_db.query(query='select available_bikes from station_data where "name"=$name;', bind_params={"name": 'unirii'})
    print("Result: {0}".format(result))


# Write received data to stdout
def on_log(client_mqtt, userdata, level, buf):
    print("Adapter log: ", buf)

 
if __name__ == '__main__':
    # Instantiate a connection to the InfluxDB
    client_db = InfluxDBClient(host='influxdb', port='8086', username='', password='', database='iotdb')
    
    # Create an mqtt client and connect to broker
    client_mqtt = mqtt.Client("adapter")
    client_mqtt.connect('mosquitto', 1883)
    
    # Set callbacks for this client
    client_mqtt.on_connect = on_connect
    client_mqtt.on_message = on_message
    client_mqtt.on_log = on_log

    client_mqtt.loop_forever()

    # Drop database
    client_db.drop_database(dbname)

