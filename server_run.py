#!/usr/bin/python3

#  Copyright (c) 2021. Ivan Zinin

# https://io.adafruit.com/i_sandwich/feeds/autoblinds1
#
# Data stored in adafruit IO is as follows:
# 0 - stop blinds | blinds stop
# 1 - blinds up
# 2 - blinds down
# // Not connected to IFTTT
# // 3 - left blinds up
# // 4 - left blinds down
# // 5 - right blinds up
# // 6 - right blinds down
# // 7 - setup mode to default
# // 8 - setup mode to quiet


# Need to fix this:
# Unexpected disconnection.
# Traceback (most recent call last):
#   File "./server_run.py", line 122, in <module>
#
#   File "./server_run.py", line 118, in main
#     # received.  Note there are other options for running the event loop like doing
#   File "/home/debian/.local/lib/python3.7/site-packages/Adafruit_IO/mqtt_client.py", line 187, in loop_blocking
#     self._client.loop_forever()
#   File "/home/debian/.local/lib/python3.7/site-packages/paho/mqtt/client.py", line 1779, in loop_forever
#     rc = self.loop(timeout, max_packets)
#   File "/home/debian/.local/lib/python3.7/site-packages/paho/mqtt/client.py", line 1181, in loop
#     rc = self.loop_read(max_packets)
#   File "/home/debian/.local/lib/python3.7/site-packages/paho/mqtt/client.py", line 1574, in loop_read
#     return self._loop_rc_handle(rc)
#   File "/home/debian/.local/lib/python3.7/site-packages/paho/mqtt/client.py", line 2227, in _loop_rc_handle
#     self._do_on_disconnect(rc, properties)
#   File "/home/debian/.local/lib/python3.7/site-packages/paho/mqtt/client.py", line 3360, in _do_on_disconnect
#     self.on_disconnect(self, self._userdata, rc)
#   File "/home/debian/.local/lib/python3.7/site-packages/Adafruit_IO/mqtt_client.py", line 101, in _mqtt_disconnect
#     raise MQTTError(rc)
# Adafruit_IO.errors.MQTTError: Incorrect protocol version

import time

from Adafruit_IO import MQTTClient

import blindsGateway
from blindsGateway import send_message

ADAFRUIT_IO_USERNAME = 'i_sandwich'
ADAFRUIT_IO_KEY = 'aio_fMAi58HKkhQeaEa8tlenXZkNwUD0'
FEED_ID = 'autoblinds1'

NUM_RETRIES = 3
RETRY_DELAY = 0.1  # seconds


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)


def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(FEED_ID, granted_qos[0]))


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    exit(1)


def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    value = int(payload)
    if value == 0:
        for r in range(NUM_RETRIES):
            send_message(0, blindsGateway.STOP, 0)
            send_message(1, blindsGateway.STOP, 0)
            time.sleep(RETRY_DELAY)
    elif value == 1:
        for r in range(NUM_RETRIES):
            send_message(0, blindsGateway.GO_UP, 0)
            send_message(1, blindsGateway.GO_UP, 0)
            time.sleep(RETRY_DELAY)
    elif value == 2:
        for r in range(NUM_RETRIES):
            send_message(0, blindsGateway.GO_DOWN, 0)
            send_message(1, blindsGateway.GO_DOWN, 0)
            time.sleep(RETRY_DELAY)
    elif value == 3:
        for r in range(NUM_RETRIES):
            send_message(0, blindsGateway.GO_UP, 0)
            time.sleep(RETRY_DELAY)
    elif value == 4:
        for r in range(NUM_RETRIES):
            send_message(0, blindsGateway.GO_DOWN, 0)
            time.sleep(RETRY_DELAY)
    elif value == 5:
        for r in range(NUM_RETRIES):
            send_message(1, blindsGateway.GO_UP, 0)
            time.sleep(RETRY_DELAY)
    elif value == 6:
        for r in range(NUM_RETRIES):
            send_message(1, blindsGateway.GO_DOWN, 0)
            time.sleep(RETRY_DELAY)
    elif value == 7:
        blindsGateway.setup()
    elif value == 8:
        blindsGateway.setup_quiet()
    else:
        print(f'Unrecognized command value: {value}')


def main():
    # Create an MQTT client instance.
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe

    # Connect to the Adafruit IO server.
    client.connect()

    # Setup motors on blinds:
    print('Setup...')
    blindsGateway.setup()

    # Start a message loop that blocks forever waiting for MQTT messages to be
    # received.  Note there are other options for running the event loop like doing
    # so in a background thread--see the mqtt_client.py example to learn more.
    client.loop_blocking()


if __name__ == '__main__':
    main()
