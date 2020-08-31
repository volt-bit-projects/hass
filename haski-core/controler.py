##########################################################
# HASKi-CORE
#
# File Name: 	controler.py
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
import database
import json
from configparser import ConfigParser



config_object = ConfigParser()
config_object.read("config.ini")

mqtt_setup = config_object["MQTT"]

username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])


sim800_setup = config_object["SIM800"]
phone_number1 = sim800_setup["phone_number1"]


def create_payload(sms_message, phone_number):
	payload_dict = {
		"command": "sms",
		"sms_message": sms_message,
		"phone_number": phone_number
	}

	payload = json.dumps(payload_dict)

	return payload



def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("CONTROLER client connected to broker with result code {}".format(rc))
		client.subscribe("haski/stat/wire_inp1")
		client.subscribe("haski/stat/wire_inp2")
		client.subscribe("haski/stat/wire_inp3")
		client.subscribe("haski/stat/wire_inp4")
		client.subscribe("haski/stat/rf_inp1")
		client.subscribe("haski/cnt/zone1")
		client.subscribe("haski/cnt/zone2")
		client.subscribe("haski/ack/rel1")
		client.subscribe("haski/ack/rel2")
	else:
		print("Connection failed")



def on_message_zone1(client, userdata, message):
	payload = message.payload.decode()

	if payload == "cnt_zone1_change":
		database.change_status_zone1()
		zone1_status = database.get_status_zone1()
		if zone1_status == 1:
			client.publish("haski/cmd/led2", "cmd_led2_on", qos=1)
			client.publish("haski/cmd/rels", "cmd_rels_zone_on", qos=1)
			client.publish("haski/ack/zone1", "ack_zone1_on", qos=1)
			database.insert_log_zone1("ON")
		elif zone1_status == 0:
			client.publish("haski/cmd/led2", "cmd_led2_off", qos=1)
			client.publish("haski/cmd/rels", "cmd_rels_zone_off", qos=1)
			client.publish("haski/ack/zone1", "ack_zone1_off", qos=1)
			database.insert_log_zone1("OFF")



def on_message_zone2(client, userdata, message):
	payload = message.payload.decode()

	if payload == "cnt_zone2_change":
		database.change_status_zone2()
		zone2_status = database.get_status_zone2()
		if zone2_status == 1:
			client.publish("haski/cmd/led3", "cmd_led3_on", qos=1)
			client.publish("haski/cmd/rels", "cmd_rels_zone_on", qos=1)
			client.publish("haski/ack/zone2", "ack_zone2_on", qos=1)
			database.insert_log_zone2("ON")
		elif zone2_status == 0:
			client.publish("haski/cmd/led3", "cmd_led3_off", qos=1)
			client.publish("haski/cmd/rels", "cmd_rels_zone_off", qos=1)
			client.publish("haski/ack/zone2", "ack_zone2_off", qos=1)
			database.insert_log_zone2("OFF")



def on_message_wire_inp1(client, userdata, message):
	payload = message.payload.decode()
	zone1_status = database.get_status_zone1()

	if zone1_status == 1:
		client.publish("haski/cmd/rels", "cmd_rels_alarm_on", qos=1)
		database.insert_alarm_event("Wire input1")
		payload = create_payload("Wire input1 activated", phone_number1)
		client.publish("haski/cmd/sim800", payload, qos=1)


def on_message_wire_inp2(client, userdata, message):
	payload = message.payload.decode()
	zone1_status = database.get_status_zone1()

	if zone1_status == 1:
		client.publish("haski/cmd/rels", "cmd_rels_alarm_on", qos=1)
		database.insert_alarm_event("Wire input2")
		payload = create_payload("Wire input2 activated", phone_number1)



def on_message_wire_inp3(client, userdata, message):
	payload = message.payload.decode()
	zone1_status = database.get_status_zone1()

	if zone1_status == 1:
		client.publish("haski/cmd/rels", "cmd_rels_alarm_on", qos=1)
		database.insert_alarm_event("Wire input3")
		payload = create_payload("Wire input3 activated", phone_number1)



def on_message_wire_inp4(client, userdata, message):
	payload = message.payload.decode()
	zone1_status = database.get_status_zone1()

	if zone1_status == 1:
		client.publish("haski/cmd/rels", "cmd_rels_alarm_on", qos=1)
		database.insert_alarm_event("Wire input4")
		payload = create_payload("Wire input4 activated", phone_number1)



def on_message_rf_inp1(client, userdata, message):
	payload = message.payload.decode()
	zone2_status = database.get_status_zone2()

	if zone2_status == 1:
		client.publish("haski/cmd/rels", "cmd_rels_alarm_on", qos=1)
		database.insert_alarm_event("RF input1")
		payload = create_payload("RF input1 activated", phone_number1)
		client.publish("haski/cmd/sim800", payload, qos=1)



def on_message_rel1(client, userdata, message):
	payload = message.payload.decode()



def on_message_rel2(client, userdata, message):
	payload = message.payload.decode()



def controler():

	client = mqtt.Client("CONTROLER")
	client.username_pw_set(username, password)

	client.message_callback_add("haski/cnt/zone1", on_message_zone1)
	client.message_callback_add("haski/cnt/zone2", on_message_zone2)
	client.message_callback_add("haski/stat/wire_inp1", on_message_wire_inp1)
	client.message_callback_add("haski/stat/wire_inp2", on_message_wire_inp2)
	client.message_callback_add("haski/stat/wire_inp3", on_message_wire_inp3)
	client.message_callback_add("haski/stat/wire_inp4", on_message_wire_inp4)
	client.message_callback_add("haski/stat/rf_inp1", on_message_rf_inp1)
	client.message_callback_add("haski/ack/rel1", on_message_rel1)
	client.message_callback_add("haski/ack/rel2", on_message_rel2)

	client.on_connect = on_connect
	client.connect(broker_address, broker_port)
	client.loop_start()

	try:
		while True:
			time.sleep(0.1)

	except KeyboardInterrupt:
		os.system('clear')



if __name__ == '__main__':
	controler()
