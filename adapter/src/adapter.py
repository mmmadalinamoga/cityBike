# IDP - CITY BIKE
# MADALINA MOGA, 343C3

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import json
import time

client_db = None
client_mqtt = None

# Upon connecting to the mqtt broker, subscribe to all 
# its topics
def on_connect(client_mqtt, userdata, flags, rc):
	print("Connected with result code: " + str(rc))
	client_mqtt.subscribe("#")

# Upon receiving a message, write it to the
# influx database
def on_message(client_mqtt, userdata, msg):
    msg_decoded = str(msg.payload.decode())
    print("Message received", msg_decoded)
	
    #TODO: CHECK STATION AUTHENTICITY

	# Unpack received data in a dictionary:
    received_dict = json.loads(m_decode)

	# Add local timestamp if no timestamp was found	
	if "timestamp" in received_dict.keys() :
		timestamp = received_dict["timestamp"]
	else : 
		t = time.localtime()
		timestamp = time.strftime("%H:%M:%S", t)
	
	#TODO: Only write numeric data to database
	# for station in received_dict.keys() :


# Write received data to stdout
def on_log(client_mqtt, userdata, level, buf):
	print("log: ", buf)

 
if __name__ == '__main__':
	global client_mqtt
	global client_db
	
	# Instantiate a connection to the InfluxDB
	client_db = InfluxDBClient('influxdb', '8086', '', '', 'citybikedb')
	
	# Create an mqtt client and connect to broker
	client_mqtt = mqtt.Client("citybike")
	client_mqtt.connect('mosquitto', 1883)
	
	# Set callbacks for this client
	client_mqtt.on_connect = on_connect
	client_mqtt.on_message = on_message
	client_mqtt.on_log = on_log

	client_mqtt.loop_forever()

	# Drop database
	client_db.drop_database(dbname)

