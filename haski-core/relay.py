##########################################################
# HASKi-CORE
#
# File Name: 	relay.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
from time import sleep
import sys, os
import threading
import database
from configparser import ConfigParser


REL1 = 19
REL2 = 20
RELS = 21


config_object = ConfigParser()
config_object.read("config.ini")


mqtt_setup = config_object["MQTT"]

username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])



# configure GPIO pins numbering as BCM
GPIO.setmode(GPIO.BCM)

# set up the GPIO pin for output
GPIO.setup(REL1, GPIO.OUT)
GPIO.output(REL1, GPIO.LOW)

GPIO.setup(REL2, GPIO.OUT)
GPIO.output(REL2, GPIO.LOW)

GPIO.setup(RELS, GPIO.OUT)
GPIO.output(RELS, GPIO.LOW)



def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("REL client connected to broker with result code {}".format(rc))
		client.subscribe("haski/cmd/rel1")
		client.subscribe("haski/cmd/rel2")
		client.subscribe("haski/cmd/rels")

	else:
		print("Connection failed")


def alarm_timer():

	username = 'haski'
	password = '1xV8gTm1J4bALrTm'
	broker_address = '192.168.1.18'
	broker_port = 1883

	client = mqtt.Client()
	client.username_pw_set(username, password)
	client.connect(broker_address, broker_port)

	GPIO.output(RELS, GPIO.HIGH)
	client.publish("haski/ack/rels", "ack_rels_on", qos=1)
	sleep(10)
	GPIO.output(RELS, GPIO.LOW)
	client.publish("haski/ack/rels", "ack_rels_off", qos=1)

	client.disconnect()



def on_message_rel1(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'cmd_rel1_on':
		GPIO.output(REL1, GPIO.HIGH)
		client.publish("haski/ack/rel1", "ack_rel1_on", qos=1)
		database.insert_relay_status("Rel1", "On")

	elif payload == 'cmd_rel1_off':
		GPIO.output(REL1, GPIO.LOW)
		client.publish("haski/ack/rel1", "ack_rel1_off", qos=1)
		database.insert_relay_status("Rel1", "Off")



def on_message_rel2(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'cmd_rel2_on':
		GPIO.output(REL2, GPIO.HIGH)
		client.publish("haski/ack/rel2", "ack_rel2_on", qos=1)
		database.insert_relay_status("Rel2", "On")
	elif payload == 'cmd_rel2_off':
		GPIO.output(REL2, GPIO.LOW)
		client.publish("haski/ack/rel2", "ack_rel2_off", qos=1)
		database.insert_relay_status("Rel2", "Off")



def on_message_rels(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'cmd_rels_on':
		GPIO.output(RELS, GPIO.HIGH)
		client.publish("haski/ack/rels", "ack_rels_on", qos=1)
	elif payload == 'cmd_rels_off':
		GPIO.output(RELS, GPIO.LOW)
		client.publish("haski/ack/rels", "ack_rels_off", qos=1)

	if payload == 'cmd_rels_zone_on':
		GPIO.output(RELS, GPIO.HIGH)
		sleep(0.1)
		GPIO.output(RELS, GPIO.LOW)
		sleep(0.2)

	elif payload == 'cmd_rels_zone_off':

		for i in range(2):
			GPIO.output(RELS, GPIO.HIGH)
			sleep(0.1)
			GPIO.output(RELS, GPIO.LOW)
			sleep(0.2)
			client.publish("haski/ack/rels", "ack_rels_off", qos=1)

	elif payload == "cmd_rels_alarm_on":

		# Define threading and start thread
		thread_alarm_timer = threading.Thread(target=alarm_timer)
		thread_alarm_timer.start()




def rel():
	client = mqtt.Client("REL")
	client.username_pw_set(username, password)
	client.message_callback_add("haski/cmd/rel1", on_message_rel1)
	client.message_callback_add("haski/cmd/rel2", on_message_rel2)
	client.message_callback_add("haski/cmd/rels", on_message_rels)
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
	rel()
