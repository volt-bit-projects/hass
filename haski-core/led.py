##########################################################
# HASKi-CORE
#
# File Name: 	led.py
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
from configparser import ConfigParser


LED1 = 4
LED2 = 5
LED3 = 6


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
GPIO.setup(LED1, GPIO.OUT)
GPIO.output(LED1, GPIO.LOW)

GPIO.setup(LED2, GPIO.OUT)
GPIO.output(LED2, GPIO.LOW)

GPIO.setup(LED3, GPIO.OUT)
GPIO.output(LED3, GPIO.LOW)



# process - blick LED1
def led1_blick():

	try:
		while True:
			GPIO.output(LED1, GPIO.HIGH)
			sleep(1)
			GPIO.output(LED1, GPIO.LOW)
			sleep(1)

	except KeyboardInterrupt:
		GPIO.cleanup()



def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("LED client connected to broker with result code {}".format(rc))
		client.subscribe("haski/cmd/led1")
		client.subscribe("haski/cmd/led2")
		client.subscribe("haski/cmd/led3")
	else:
		print("Connection failed")



def on_message_led1(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'cmd_led1_on':
		GPIO.output(LED1, GPIO.HIGH)
		client.publish("haski/ack/led1", "ack_led1_on", qos=1)
	elif payload == 'cmd_led1_off':
		GPIO.output(LED1, GPIO.LOW)
		client.publish("haski/ack/led1", "ack_led1_off", qos=1)



def on_message_led2(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'cmd_led2_on':
		GPIO.output(LED2, GPIO.HIGH)
		client.publish("haski/ack/led2", "ack_led2_on", qos=1)
	elif payload == 'cmd_led2_off':
		GPIO.output(LED2, GPIO.LOW)
		client.publish("haski/ack/led2", "ack_led2_off", qos=1)



def on_message_led3(client, userdata, message):
	payload = message.payload.decode()

	if payload == 'cmd_led3_on':
		GPIO.output(LED3, GPIO.HIGH)
		client.publish("haski/ack/led3", "ack_led3_on", qos=1)
	elif payload == 'cmd_led3_off':
		client.publish("haski/ack/led3", "ack_led3_off", qos=1)
		GPIO.output(LED3, GPIO.LOW)



def led():
	client = mqtt.Client("LED")
	client.username_pw_set(username, password)
	client.message_callback_add("haski/cmd/led1", on_message_led1)
	client.message_callback_add("haski/cmd/led2", on_message_led2)
	client.message_callback_add("haski/cmd/led3", on_message_led3)

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
	led()
