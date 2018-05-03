import paho.mqtt.client as mqtt #import the client1
import time

broker_address="broker.hivemq.com"

client = mqtt.Client("P1") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker
print("Publishing message to topic","house/bulbs/bulb1")
i=0
while i<100:
    client.publish("house/bulbs/bulb1","OFF")
    time.sleep(10) # wait
    i=i+1
