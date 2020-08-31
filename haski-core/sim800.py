##########################################################
# HASKi-CORE
#
# File Name: 	sim800.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import paho.mqtt.client as mqtt
import time
from time import sleep
from datetime import datetime
import json
import serial
from serial import SerialException, SerialTimeoutException
import sys, os
import re
from configparser import ConfigParser



config_object = ConfigParser()
config_object.read("config.ini")

mqtt_setup = config_object["MQTT"]
username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])


# SIM800 init function
def sim800_init():
	reply = "OK"																				# define "OK" as expected reply from SIM800L module

	sim800 = serial.Serial("/dev/serial0",  115200, timeout = 2)								# open serial port

	try:
		sim800.write(b'AT\n')																	# check communication with SIM800 module
		rec = sim800.read(8).decode("ascii")
		if reply in rec:
			print("SIM800 ready.")
		else:
			print("ERROR")
			return 0
		sleep(0.5)

		sim800.write(b'AT+CMGF=1\n')															# set SMS mode to text
		rec = sim800.read(15).decode("ascii")
		if reply in rec:
			print("SMS set to text mode.")
		else:
			print("ERROR")
			return 0
		sleep(0.5)

		sim800.write(b'AT+CNMI=2,2,0,0,0\n')													# enable new SMS indication to avoid pooling for a new message
		rec = sim800.read(21).decode("ascii")
		if reply in rec:
			print("New SMS indication enabled.")
		else:
			print("ERROR")
			return 0
		sleep(0.5)

		ack = 1

	except Exception as e:
		print("SIM800 module communication error: " + str(e))
		ack = 0

	finally:
		sim800.close()

	return ack


# get remaining credit info for prepaid SIM card
def get_credit(operator_name):
	sim800 = serial.Serial("/dev/serial0",  115200, timeout = 1)

	if operator_name == "O2":
		sim800.write(b'AT+CUSD=1,"*104*#"\r')		# check credit code for O2
	elif operator_name == "T-Mobile":
		sim800.write(b'AT+CUSD=1,"*101#"\r')		# check credit code for T-Mobile (add specific code to get credit for your operator)

	while True:
		rec = sim800.readline().decode("ascii")

		if rec:
			if ", 15" in rec:
				sim800.close
				break

	credit_string = re.search('je(.+?)Kc', rec)		# parse your operator's string containing credit info

	if credit_string:
	    credit = (credit_string.group(1))[1:]

	return credit


# send SMS message
def send_sms(sms_message, phone_number):
	# global ack

	reply = "OK"																				# set expected reply
	sim800 = serial.Serial("/dev/serial0",  115200, timeout = 5)								# open serial port

	try:
		sim800.write(b'AT+CMGS="' + phone_number.encode() + b'"\n')								# send phone number to SIM800 module
		time.sleep(0.5)																			# wait 500ms
		sim800.write(sms_message.encode() + b"\n")												# send message to SIM800 module
		time.sleep(0.5)																			# wait 500ms
		sim800.write(bytes([26]))																# send ctrl-Z

		while True:
			rec = sim800.readline().decode("ascii")												# wait for reply from SIM800 module

			if rec:																				# check OK in reply
				if reply in rec:
					#print ("Message sent.\n\n")
					sim800.close																# close serial port
					break																		# exit while loop
		ack = 1

	except Exception as e:
		print("Cannot send SMS message: " + str(e))
		ack = 0

	finally:
		sim800.close

	return ack



def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("SIM800 client connected to broker with result code {}".format(rc))
		client.subscribe("haski/cmd/sim800")
	else:
		print("Connection failed")



def on_message_sim800(client, userdata, message):
	payload = json.loads(message.payload) 									# use json.loads to convert string to json
	command = (payload['command'])

	if command == 'init':
		ack = sim800_init()
		if ack == 1:
			payload = json.dumps({"init": "OK"})
			client.publish("haski/ack/sim800", payload, qos=1)
		elif ack == 0:
			payload = json.dumps({"init": "ERROR"})
			client.publish("haski/ack/sim800", payload, qos=1)


	if command == 'credit':
		operator = (payload['operator'])
		credit = get_credit(operator)
		payload = json.dumps({"credit": credit})
		client.publish("haski/tlm/sim800", payload, qos=1)


	if command == 'sms':
		sms_message = (payload['sms_message'])
		phone_number = (payload['phone_number'])
		ack = send_sms(sms_message, phone_number)

		if ack == 1:
			payload = json.dumps({"sms": "OK"})
			client.publish("haski/ack/sim800", payload, qos=1)
		if ack == 0:
			payload = json.dumps({"sms": "ERROR"})
			client.publish("haski/ack/sim800", payload, qos=1)



def sim800():
	client = mqtt.Client("SIM800")
	client.username_pw_set(username, password)
	client.message_callback_add("haski/cmd/sim800", on_message_sim800)



	client.on_connect = on_connect
	client.connect(broker_address, broker_port)
	client.loop_start()

	try:
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		# GPIO.cleanup()
		os.system('clear')



if __name__ == '__main__':
	sim800()
