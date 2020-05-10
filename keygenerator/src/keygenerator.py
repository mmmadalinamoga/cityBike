# IDP - CITY BIKE
# MADALINA MOGA, 343C3
#
# Gets a key from a station

from influxdb import InfluxDBClient
import json
import time
import random
import sys
import string


if __name__ == '__main__':
    # Instantiate a connection to the iotdb database
    client_db = InfluxDBClient(host='influxdb', port='8086', username='', password='', database='iotdb')

    while True:
        station_name = sys.stdin.readline().rstrip()

        if station_name :

            print("You requested key for station: ", station_name)

            result = client_db.query(query='SELECT * from station_data where "name"=$name limit 1;', bind_params={"name": station_name})
            res = result.get_points(measurement='station_data')
            print(res)

            if res["bike_keys_available"] == 'true' and res["bike_key_dispenser"] == 'true':

                gen = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                print(gen)

            # Drop database
            #client_db.drop_database('iotdb')


