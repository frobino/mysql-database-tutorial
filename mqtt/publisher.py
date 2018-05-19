# Requires Eclipse Paho MQTT Python client library, which implements the MQTT protocol.
# The MQTT protocol is a machine-to-machine (M2M)/Internet of Things connectivity protocol.
# Designed as an extremely lightweight publish/subscribe messaging transport,
# it is useful for connections with remote locations where a small code footprint is required
# and/or network bandwidth is at a premium.
#
# pip install paho-mqtt
#
# This code provides a client class which enable applications to connect to an MQTT broker
# to publish messages, and to subscribe to topics and receive published messages.
# 
#                +----+
#                |    |
#                |    |
#               /+----+ broker (receiving from publisher client)
#      +----+  /
#      |    | /
#      |    |/
#      +----+ publisher (sending to broker)

import paho.mqtt.client as mqtt #import the client1
import time

broker_address="broker.hivemq.com"

client = mqtt.Client("P1") #create new instance
print("Connecting to broker")
client.connect(broker_address) #connect to broker
print("Publishing message to topic","house/bulbs/bulb1")
i=0
while i<100:
    client.publish("house/bulbs/bulb1","OFF")
    time.sleep(10) # wait
    i=i+1
