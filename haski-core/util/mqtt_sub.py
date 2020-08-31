################################################################
# MQTT subscribe testing utility for Home Automation Starter Kit
#
# File Name: 	mqtt_sub.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
################################################################


import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
from time import sleep
import sys, os



username = 'haski'
password = 'mqtt_password'
broker_address = '192.168.1.XX'
broker_port = 1883



# MQTT On Conect function to subscribe to all available topics
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("TEST client connected to broker with result code {}".format(rc))
		client.subscribe("haski/stat/#")
		client.subscribe("haski/cmd/#")
		client.subscribe("haski/ack/#")
		client.subscribe("haski/tlm/#")
		client.subscribe("haski/stat/sonoff1/#")

	else:
		print("Connection failed")


# MQTT On Message function to print status of LED1
def on_message_led1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of LED2
def on_message_led2(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of LED3
def on_message_led3(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of REL1
def on_message_rel1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of REL2
def on_message_rel2(client, userdata, message):
	payload = message.payload.decode()
	print(payload)


# MQTT On Message function to print status of RELS
def on_message_rels(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of Zone1
def on_message_zone1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of Zone2
def on_message_zone2(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status RF Input1
def on_message_rf_inp1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status RF Output1
def on_message_rf_out1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status RF Output2
def on_message_rf_out2(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status RF Output3
def on_message_rf_out3(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of Wire Input1
def on_message_wire_inp1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of Wire Input2
def on_message_wire_inp2(client, userdata, message):
	payload = message.payload.decode()
	print(payload)


# MQTT On Message function to print status of Wire Input3
def on_message_wire_inp3(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print status of Wire Input4
def on_message_wire_inp4(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print SIM800 payloads in Acknowledgement topic
def on_message_sim800_ack(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print SIM800 payloads in Telemetry topic
def on_message_sim800_tlm(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print Zone1 payloads in Acknowledgement topic
def on_message_zone1_ack(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



# MQTT On Message function to print Zone2 payloads in Acknowledgement topic
def on_message_zone2_ack(client, userdata, message):
	payload = message.payload.decode()
	print(payload)


# MQTT On Message function to print Sonoff payloads in Status topic
def on_message_sonoff1(client, userdata, message):
	payload = message.payload.decode()
	print(payload)



def main():
	client = mqtt.Client("TEST")												# create name for MQTT client
	client.username_pw_set(username, password)									# setup uername and password

	client.message_callback_add("haski/ack/led1", on_message_led1)				# add message callbacks for MQTT topics
	client.message_callback_add("haski/ack/led2", on_message_led2)
	client.message_callback_add("haski/ack/led3", on_message_led3)

	client.message_callback_add("haski/ack/rel1", on_message_rel1)
	client.message_callback_add("haski/ack/rel2", on_message_rel2)
	client.message_callback_add("haski/ack/rels", on_message_rels)

	client.message_callback_add("haski/stat/zone1", on_message_zone1)
	client.message_callback_add("haski/stat/zone2", on_message_zone2)
	client.message_callback_add("haski/stat/rf_inp1", on_message_rf_inp1)

	client.message_callback_add("haski/ack/rf_out1", on_message_rf_out1)
	client.message_callback_add("haski/ack/rf_out2", on_message_rf_out2)
	client.message_callback_add("haski/ack/rf_out3", on_message_rf_out3)

	client.message_callback_add("haski/stat/wire_inp1", on_message_wire_inp1)
	client.message_callback_add("haski/stat/wire_inp2", on_message_wire_inp2)
	client.message_callback_add("haski/stat/wire_inp3", on_message_wire_inp3)
	client.message_callback_add("haski/stat/wire_inp4", on_message_wire_inp4)

	client.message_callback_add("haski/ack/sim800", on_message_sim800_ack)
	client.message_callback_add("haski/tlm/sim800", on_message_sim800_tlm)

	client.message_callback_add("haski/ack/zone1", on_message_zone1_ack)
	client.message_callback_add("haski/ack/zone2", on_message_zone2_ack)

	client.message_callback_add("haski/stat/sonoff1/POWER", on_message_sonoff1)


	client.on_connect = on_connect
	client.connect(broker_address, broker_port)
	client.loop_start()

	try:
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		GPIO.cleanup()
		os.system('clear')



if __name__ == '__main__':
	main()
