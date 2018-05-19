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
#       +----+
#       |    |
#       |    |
#       +----+ broker (receiving from publisher client, forwarding to subscriber client)
#           \-     +----+
#             \-   |    |
#               \- |    |
#                 \+----+ subscriber (receiving from broker)


import paho.mqtt.client as mqtt #import the client1
import time

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

broker_address="broker.hivemq.com"

client = mqtt.Client("S1") #create new instance
print("connecting to broker")
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
client.loop_forever()
