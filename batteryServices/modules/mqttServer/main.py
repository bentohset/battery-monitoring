# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

""" 
Receives data through MQTT Port on the Edge Device and routes it to the next module
"""

import asyncio
import sys
import signal
import threading
import datetime
import multiprocessing
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message
from paho.mqtt import client as mqtt

# Event indicating client stop
stop_event = threading.Event()

# Constants for MQTT config
mqtt_broker = "192.168.0.104"
mqtt_port = 8883
mqtt_topic = "battery/telemetry"

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    return client

""" 
Main routine of this module
"""
async def run_sample(ioclient):
    # Customize this coroutine to do whatever tasks the module initiates
    
    # initialise mqtt client and message queue to receive data asynchronously in a synchronous channel
    mqtt_client = mqtt.Client()
    message_queue = multiprocessing.Queue()
    
    # mqtt connect event handlers
    def on_connect(client, user_data, flags, rc):
        print("Connected to MQTT Broker")
        mqtt_client.subscribe(mqtt_topic)

    def on_disconnect(client, user_data, rc):
        if rc != 0:
            print("Broker disconnected: Unexpected disconnection")
        else:
            print("Broker is disconnected...")
        print(rc)
    
    def on_message(client, user_data, msg):
        # when message is received update the timestamp with the current time and encapsulate it into a Message object
        payload = msg.payload.decode()
        print("Message received from MQTT Broker")
        print("Topic: {}".format(msg.topic))
        print("Payload: {}".format(payload))
        
        timestamp = str(datetime.datetime.now())
        payload_time = payload + "'timestamp': '" + timestamp + "'}"
        message = Message(payload_time)
        print("Message sent upstream {}".format(message))

        # input into message queue
        message_queue.put(message)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect

    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()

    # retrieves the first task from the message queue and sends to the output to next module
    while True:
        message = message_queue.get()
        print(message)
        print("Sending to output1..........")
        await ioclient.send_message_to_output(message, "output1")
        

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
