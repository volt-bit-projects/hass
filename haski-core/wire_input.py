##########################################################
# HASKi-CORE
#
# File Name: 	wire_input.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from time import sleep
import database
import sys, os
from configparser import ConfigParser

INP1 = 22
INP2 = 23
INP3 = 24
INP4 = 25


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
GPIO.setup(INP1, GPIO.IN)
GPIO.setup(INP2, GPIO.IN)
GPIO.setup(INP3, GPIO.IN)
GPIO.setup(INP4, GPIO.IN)



def mqtt_pub(topic, payload):
	client = mqtt.Client()
	client.username_pw_set(username, password)
	client.connect(broker_address, broker_port)
	client.publish(topic, payload, qos=1)
	client.disconnect()



def read_inp1(INP1):
	if GPIO.input(INP1):
		mqtt_pub("haski/stat/wire_inp1", "stat_wire_inp1_opened")
		database.insert_sensor_activity("input1", "wire", "N/A", "opened")
	else:
		mqtt_pub("haski/stat/wire_inp1", "stat_wire_inp1_closed")
		database.insert_sensor_activity("input1", "wire", "N/A", "closed")



def read_inp2(INP2):
	if GPIO.input(INP2):
		mqtt_pub("haski/stat/wire_inp2", "stat_wire_inp2_opened")
		database.insert_sensor_activity("input2", "wire", "N/A", "opened")
	else:
		mqtt_pub("haski/stat/wire_inp2", "stat_wire_inp2_closed")
		database.insert_sensor_activity("input2", "wire", "N/A", "closed")



def read_inp3(INP3):
	if GPIO.input(INP3):
		mqtt_pub("haski/stat/wire_inp3", "stat_wire_inp3_opened")
		database.insert_sensor_activity("input3", "wire", "N/A", "opened")
	else:
		mqtt_pub("haski/stat/wire_inp3", "stat_wire_inp3_closed")
		database.insert_sensor_activity("input3", "wire", "N/A", "closed")



def read_inp4(INP4):
	if GPIO.input(INP4):
		mqtt_pub("haski/stat/wire_inp4", "stat_wire_inp4_opened")
		database.insert_sensor_activity("input4", "wire", "N/A", "opened")
	else:
		mqtt_pub("haski/stat/wire_inp4", "stat_wire_inp4_closed")
		database.insert_sensor_activity("input4", "wire", "N/A", "closed")



def wire_inp():

	GPIO.add_event_detect(INP1, GPIO.BOTH, callback = read_inp1, bouncetime = 300)
	GPIO.add_event_detect(INP2, GPIO.BOTH, callback = read_inp2, bouncetime = 300)
	GPIO.add_event_detect(INP3, GPIO.BOTH, callback = read_inp3, bouncetime = 300)
	GPIO.add_event_detect(INP4, GPIO.BOTH, callback = read_inp4, bouncetime = 300)

	try:
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		# client.disconnect()
		# client.loop_stop()
		GPIO.cleanup()
		os.system('clear')


if __name__ == '__main__':
	wire_inp()
