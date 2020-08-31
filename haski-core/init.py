##########################################################
# HASKi-CORE
#
# File Name: 	init.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import paho.mqtt.client as mqtt
import sys, os
import database
import time
from time import sleep
import json
from configparser import ConfigParser


config_object = ConfigParser()
config_object.read("config.ini")


mqtt_setup = config_object["MQTT"]

username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])




def mqtt_pub(topic, payload):
	client = mqtt.Client()
	client.username_pw_set(username, password)
	client.connect(broker_address, broker_port)
	client.publish(topic, payload, qos=1)
	client.disconnect()




def led_test():
	mqtt_pub("haski/cmd/led1", "cmd_led1_off")
	mqtt_pub("haski/cmd/led2", "cmdled2_off")
	mqtt_pub("haski/cmd/led3", "cmdled3_off")
	sleep(1)

	for i in range(3):
		mqtt_pub("haski/cmd/led1", "cmd_led1_on")
		sleep(0.2)
		mqtt_pub("haski/cmd/led2", "cmd_led2_on")
		sleep(0.2)
		mqtt_pub("haski/cmd/led3", "cmd_led3_on")
		sleep(0.2)

		mqtt_pub("haski/cmd/led3", "cmd_led3_off")
		sleep(0.2)
		mqtt_pub("haski/cmd/led2", "cmd_led2_off")
		sleep(0.2)
		mqtt_pub("haski/cmd/led1", "cmd_led1_off")
		sleep(0.2)




def relay_test():
	mqtt_pub("haski/cmd/rel1", "cmd_rel1_on")
	sleep(1)
	mqtt_pub("haski/cmd/rel1", "cmd_rel1_off")
	sleep(1)
	mqtt_pub("haski/cmd/rel2", "cmd_rel2_on")
	sleep(1)
	mqtt_pub("haski/cmd/rel2", "cmd_rel2_off")
	sleep(1)


	for i in range(2):
		mqtt_pub("haski/cmd/rels", "cmd_rels_on")
		sleep(0.1)
		mqtt_pub("haski/cmd/rels", "cmd_rels_off")
		sleep(0.1)



def siren_beep():
	for i in range(2):
		mqtt_pub("haski/cmd/rels", "cmd_rels_on")
		sleep(0.1)
		mqtt_pub("haski/cmd/rels", "cmd_rels_off")
		sleep(0.1)



def sim800_test():
	payload_dict = {
	  "command": "init"
	}

	payload = json.dumps(payload_dict)
	mqtt_pub("haski/cmd/sim800", payload)



def database_setup():
	db_exists = database.check_db_exists()													# check if rhss database exists
	if db_exists == False:																	# if not, create it
		database.delete_user()
		database.create_db()

	user_exists = database.check_user_exists()
	if user_exists == False:
		database.create_user()

	status_zone1 = database.get_status_zone1()												# check ARM1 status
	status_zone2 = database.get_status_zone2()												# check ARM2 status

	if status_zone1 == True:																# if ARM1 is ON, set ARM1 OFF as a default after setup
		database.change_status_zone1()
		database.insert_log_zone1("OFF")
	if status_zone2 == True:																# if ARM2 is ON, set ARM2 OFF as a default after setup
		database.change_status_zone2()
		database.insert_log_zone2("OFF")



if __name__ == '__main__':
	led_test()
