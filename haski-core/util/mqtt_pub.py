##############################################################
# MQTT publish testing utility for Home Automation Starter Kit
#
# File Name: 	mqtt_pub.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##############################################################

import paho.mqtt.client as mqtt
import time
from time import sleep
import json


username = 'haski'
password = 'mqtt_password'
broker_address = '192.168.1.XX'
broker_port = 1883


def mqtt_pub(topic, payload):
	client = mqtt.Client()
	client.username_pw_set(username, password)
	client.connect(broker_address, broker_port)
	client.publish(topic, payload, qos=1)
	client.disconnect()



def main():

	# Test on-board LEDs
	# mqtt_pub("haski/cmd/led1", "cmd_led1_on")
	# sleep(1)
	# mqtt_pub("haski/cmd/led1", "cmd_led1_off")
	# sleep(1)
	#
	# mqtt_pub("haski/cmd/led2", "cmd_led2_on")
	# sleep(1)
	# mqtt_pub("haski/cmd/led2", "cmd_led2_off")
	# sleep(1)
	#
	# mqtt_pub("haski/cmd/led3", "cmd_led3_on")
	# sleep(1)
	# mqtt_pub("haski/cmd/led3", "cmd_led3_off")
	# sleep(1)



	# Test on-board relays
	mqtt_pub("haski/cmd/rel1", "cmd_rel1_on")
	sleep(1)
	mqtt_pub("haski/cmd/rel1", "cmd_rel1_off")
	sleep(1)

	mqtt_pub("haski/cmd/rel2", "cmd_rel2_on")
	sleep(1)
	mqtt_pub("haski/cmd/rel2", "cmd_rel2_off")
	sleep(1)

	mqtt_pub("haski/cmd/rels", "cmd_rels_on")
	sleep(1)
	mqtt_pub("haski/cmd/rels", "cmd_rels_off")
	sleep(1)



	# Test RF outputs - sockets
	# mqtt_pub("haski/cmd/rf_out1", "cmd_rf_out1_on")
	# sleep(1)
	# mqtt_pub("haski/cmd/rf_out1", "cmd_rf_out1_off")
	# sleep(1)
	#
	# mqtt_pub("haski/cmd/rf_out2", "cmd_rf_out2_on")
	# sleep(1)
	# mqtt_pub("haski/cmd/rf_out2", "cmd_rf_out2_off")
	# sleep(1)
	#
	# mqtt_pub("haski/cmd/rf_out3", "cmd_rf_out3_on")
	# sleep(1)
	# mqtt_pub("haski/cmd/rf_out3", "cmd_rf_out3_off")
	# sleep(1)



	# Test RF inputs
	# mqtt_pub("haski/stat/rf_inp1", "stat_rf_inp1_opened_nv")
	# sleep(1)
	# mqtt_pub("haski/stat/rf_inp1", "stat_rf_inp1_closed_nv")
	# sleep(1)



	# Test zone 1 ARM/DISARM
	# mqtt_pub("haski/cnt/zone1", "cnt_zone1_change")
	# sleep(1)
	# mqtt_pub("haski/cnt/zone1", "cnt_zone1_change")
	# sleep(1)



	# Test zone 2 ARM/DISARM
	# mqtt_pub("haski/cnt/zone2", "cnt_zone2_change")
	# sleep(1)
	# mqtt_pub("haski/cnt/zone2", "cnt_zone2_change")
	# sleep(1)



	# Test SIM800L initialization sequence
	# payload_dict = {
	#   "command": "init"
	# }
	#
	# payload = json.dumps(payload_dict)
	# mqtt_pub("haski/cmd/sim800", payload)



	# Test check credit command
	# payload_dict = {
	#   "command": "credit",
	#   "operator": "Operator name"
	# }
	#
	# payload = json.dumps(payload_dict)
	# mqtt_pub("haski/cmd/sim800", payload)



	# Test send SMS command
	# payload_dict = {
	# 	"command": "sms",
	# 	"sms_message": "Test message",
	# 	"phone_number": "+XXXXXXXXXXXX"
	# }
	#
	# payload = json.dumps(payload_dict)
	# mqtt_pub("haski/cmd/sim800", payload)



if __name__ == '__main__':
	main()
