##########################################################
# HASKi-CORE
#
# File Name: 	sonoff.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import paho.mqtt.client as mqtt
import time
from time import sleep
import sys, os
import threading
import database
from configparser import ConfigParser


config_object = ConfigParser()
config_object.read("config.ini")


mqtt_setup = config_object["MQTT"]

username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])



def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("SONOFF client connected to broker with result code {}".format(rc))
		client.subscribe("haski/stat/sonoff1/POWER")

	else:
		print("Connection failed")




def on_message_sonoff1(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'ON':
		database.insert_sonoff_status("SONOFF1", "On")

	if payload == 'OFF':
		database.insert_sonoff_status("SONOFF1", "Off")



def sonoff():
	client = mqtt.Client("SONOFF")
	client.username_pw_set(username, password)
	client.message_callback_add("haski/stat/sonoff1/POWER", on_message_sonoff1)
	client.on_connect = on_connect
	client.connect(broker_address, broker_port)
	client.loop_start()

	try:
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		os.system('clear')



if __name__ == '__main__':
	rel()
