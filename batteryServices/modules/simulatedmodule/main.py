# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import signal
import threading
import datetime
import random
import json
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message


# Event indicating client stop
stop_event = threading.Event()

MAX_MESSAGE = 200
count = 0

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    global count
    while count < MAX_MESSAGE:
        battery_id = random.randint(1, 20)
        ble_uuid = "abcdefg"
        humidity = random.uniform(20,80)
        temperature = random.uniform(15, 35)
        internal_series_resistance = random.uniform(1, 10)
        internal_impedance = random.uniform(100, 1000)
        timestamp = str(datetime.datetime.now())

        payload = {
            "battery_id": battery_id,
            "ble_uuid": ble_uuid,
            "humidity": humidity,
            "temperature": temperature,
            "internal_series_resistance": internal_series_resistance,
            "internal_impedance": internal_impedance,
            "timestamp": timestamp,
        }

        payload_str = json.dumps(payload)
        print(payload_str)
        message = Message(payload_str)
        
        await client.send_message_to_output(message, "output1")
        count += 1
        print(f"Count: {count}")

        await asyncio.sleep(1)


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
