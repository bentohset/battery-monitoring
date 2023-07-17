# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

"""
Receives data from mqtt module and inserts into local database
"""

import asyncio
import sys
import ast
import signal
import threading
import json
import psycopg2
from azure.iot.device.aio import IoTHubModuleClient

# Event indicating client stop
stop_event = threading.Event()

pg_connection_string = "host=192.168.0.104 user=postgres password=3logytech! dbname=temperature_sensor"

# global counters
TEMPERATURE_THRESHOLD = 25
TWIN_CALLBACKS = 0
RECEIVED_MESSAGES = 0

# function to insert JSON into PostgreSQL DB
def insert_psql(message_json):
    try:
        # opens a connection
        conn = psycopg2.connect(
            database="temperature_sensor",
            user="postgres",
            host="192.168.0.104",
            password="3logytech!"
        )
        cursor = conn.cursor()
    except Exception as e:
        print("Error connecting to DB: ", str(e))

    try:
        # constructs query and executes it
        query = """
        INSERT INTO readings (battery_id, ble_uuid, humidity, temperature, internal_series_resistance, internal_impedance, timestamp)
        VALUES (%(battery_id)s, %(ble_uuid)s, %(humidity)s, %(temperature)s, %(internal_series_resistance)s, %(internal_impedance)s, %(timestamp)s)
        """
    
        values = {
            "battery_id": message_json["battery_id"],
            "ble_uuid": message_json["ble_uuid"],
            "humidity": message_json["humidity"],
            "temperature": message_json["temperature"],
            "internal_series_resistance": message_json["internal_series_resistance"],
            "internal_impedance": message_json["internal_impedance"],
            "timestamp": message_json["timestamp"]
        }
        
        cursor.execute(query, values)
        conn.commit()
        print("Inserted into PSQL DB successfully")
    except psycopg2.Error as e:
        print("real Error occurred while inserting data into PostgreSQL:", str(e))
        conn.rollback()
        
    finally:
        # Close the database connection
        cursor.close()
        conn.close()

""" 
Main routine of this module:
creates the client with respective event handlers
"""
def create_client():
    print("creating client")
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        global RECEIVED_MESSAGES
        print("Message received")
        size = len(message.data)
        message_text = message.data.decode('utf-8')


        print("    Data: <<<{data}>>> & Size={size}".format(data=message.data, size=size))
        print("    Properties: {}".format(message.custom_properties))
        RECEIVED_MESSAGES += 1
        print("Total messages received: {}".format(RECEIVED_MESSAGES))

        # checks if messages are received from the correct input and converts into JSON
        if message.input_name == "input1":
            message_format = str(message_text).replace("'", '"')
            message_json = json.loads(message_format)
            insert_psql(message_json)

            # sends "useless" data to the output (purpose already fulfilled above when inserted into DB)
            await client.send_message_to_output(message, "output1")

    # Define function for handling received twin patches (aka exact same data)
    # NOTE: should not be running, to be repurposed for future
    async def receive_twin_patch_handler(twin_patch):
        # code here is from sample taken online
        global TEMPERATURE_THRESHOLD
        global TWIN_CALLBACKS
        print("Twin Patch received")
        print("     {}".format(twin_patch))
        if "TemperatureThreshold" in twin_patch:
            TEMPERATURE_THRESHOLD = twin_patch["TemperatureThreshold"]
        TWIN_CALLBACKS += 1
        print("Total calls confirmed: {}".format(TWIN_CALLBACKS))

    try:
        # Set handler on the client
        print("client created")
        client.on_message_received = receive_message_handler
        # client.on_twin_desired_properties_patch_received = receive_twin_patch_handler
    except:
        # Cleanup if failure occurs
        print("error creating client")
        client.shutdown()
        raise

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages

    while True:
        await asyncio.sleep(100)


def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
