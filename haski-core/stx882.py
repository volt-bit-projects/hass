##########################################################
# HASKi-CORE
#
# File Name: 	stx882.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import paho.mqtt.client as mqtt
import time
from time import sleep
import database
from rpi_rf import RFDevice
import sys, os
from configparser import ConfigParser



config_object = ConfigParser()
config_object.read("config.ini")


mqtt_setup = config_object["MQTT"]

username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])




rfdevice = RFDevice(17)																			# gpio pin to send data to RF TX module
rfdevice.enable_tx()



def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("STX882 client connected to broker with result code {}".format(rc))
		client.subscribe("haski/cmd/rf_out1")
		client.subscribe("haski/cmd/rf_out2")
		client.subscribe("haski/cmd/rf_out3")

	else:
		print("Connection failed")




def on_message_rf_out1(client, userdata, message):

	payload = message.payload.decode()

	if payload == "cmd_rf_out1_on":
		database.insert_rf_out_status("RF Socket1", "On")
		rfdevice.tx_code(16106836, 1, 200)
		client.publish("haski/ack/rf_out1", "ack_rf_out1_on", qos=1)

	elif payload == "cmd_rf_out1_off":
		database.insert_rf_out_status("RF Socket1", "Off")
		rfdevice.tx_code(16106833, 1, 200)
		client.publish("haski/ack/rf_out1", "ack_rf_out1_off", qos=1)



def on_message_rf_out2(client, userdata, message):

	payload = message.payload.decode()

	if payload == "cmd_rf_out2_on":
		database.insert_rf_out_status("RF Socket2", "On")
		rfdevice.tx_code(16109908, 1, 200)
		client.publish("haski/ack/rf_out2", "ack_rf_out2_on", qos=1)

	elif payload == "cmd_rf_out2_off":
		database.insert_rf_out_status("RF Socket2", "Off")
		rfdevice.tx_code(16109905, 1, 200)
		client.publish("haski/ack/rf_out2", "ack_rf_out2_off", qos=1)



def on_message_rf_out3(client, userdata, message):

	payload = message.payload.decode()

	if payload == "cmd_rf_out3_on":
		database.insert_rf_out_status("RF Socket3", "On")
		rfdevice.tx_code(16110676, 1, 200)										# code, protocol=1, pulsLenght=350, Length=24, repeat=10
		client.publish("haski/ack/rf_out3", "ack_rf_out3_on", qos=1)

	elif payload == "cmd_rf_out3_off":
		database.insert_rf_out_status("RF Socket3", "Off")
		rfdevice.tx_code(16110673, 1, 200)
		client.publish("haski/ack/rf_out3", "ack_rf_out3_off", qos=1)



def rf_out():

	client = mqtt.Client("stx882")
	client.username_pw_set(username, password)

	client.message_callback_add("haski/cmd/rf_out1", on_message_rf_out1)
	client.message_callback_add("haski/cmd/rf_out2", on_message_rf_out2)
	client.message_callback_add("haski/cmd/rf_out3", on_message_rf_out3)


	# create event handler on_connect
	client.on_connect= on_connect
	client.connect(broker_address, broker_port)
	client.loop_start()


	try:
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		client.disconnect()
		client.loop_stop()
		# GPIO.cleanup()
		rfdevice.cleanup()
		os.system('clear')



if __name__ == '__main__':
	rf_out()
