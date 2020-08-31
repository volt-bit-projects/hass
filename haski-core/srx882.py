##########################################################
# HASKi-CORE
#
# File Name: 	srx882.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

from rpi_rf import RFDevice
import paho.mqtt.client as mqtt
import time
from time import sleep
from datetime import datetime
import database
import sys, os
from configparser import ConfigParser



config_object = ConfigParser()
config_object.read("config.ini")


mqtt_setup = config_object["MQTT"]

username = mqtt_setup["username"]
password = mqtt_setup["password"]
broker_address = mqtt_setup["broker_address"]
broker_port = int(mqtt_setup["broker_port"])



RC_ZONE1 = 4128768										# assign control code to switch ON/OFF Zone1
RC_ZONE2 = 983040										# assign control code to switch ON/OFF Zone2

RF_INP1_OPENED_NV = 5895475								# assign control code for wirelsess magnetic door contact - open (normal voltage)
RF_INP1_CLOSED_NV = 5895954								# assign control code for wirelsess magnetic door contact - closed (normal voltage)
RF_INP1_OPENED_LV = 5895489								# assign control code for wirelsess magnetic door contact - open (low voltage)
RF_INP1_CLOSED_LV = 5895987								# assign control code for wirelsess magnetic door contact - closed (low voltage)




def mqtt_pub(topic, payload):
	client = mqtt.Client()
	client.username_pw_set(username, password)
	client.connect(broker_address, broker_port)
	client.publish(topic, payload, qos=1)
	client.disconnect()


def rf_inp():

	rfdevice = RFDevice(27)
	rfdevice.enable_rx()
	timestamp = None
	code_inp1_opened_nv = False
	code_inp1_closed_nv = False
	code_inp1_opened_lv = False
	code_inp1_closed_lv = False


	try:
		while True:
			if rfdevice.rx_code_timestamp != timestamp:
				timestamp = rfdevice.rx_code_timestamp
				code = rfdevice.rx_code

				if code == RC_ZONE1:
					print("Received code: ", code)
					mqtt_pub("haski/cnt/zone1", "cnt_zone1_change")



				if code == RC_ZONE2:
					print("Received code: ", code)
					mqtt_pub("haski/cnt/zone2", "cnt_zone2_change")


				if code == RF_INP1_OPENED_NV:
					if code_inp1_opened_nv == False:
						print("Received code: ", code)
						mqtt_pub("haski/stat/rf_inp1", "stat_rf_inp1_opened_nv")
						database.insert_sensor_activity("input1", "rf", "normal", "opened")
						code_inp1_opened_nv = True

					code_inp1_closed_nv = False


				if code == RF_INP1_CLOSED_NV:
					if code_inp1_closed_nv == False:
						print("Received code: ", code)
						mqtt_pub("haski/stat/rf_inp1", "stat_rf_inp1_closed_nv")
						database.insert_sensor_activity("input1", "rf", "normal", "closed")
						code_inp1_closed_nv = True

					code_inp1_opened_nv = False


				if code == RF_INP1_OPENED_LV:
					if code_inp1_opened_lv == False:
						print("Received code: ", code)
						mqtt_pub("haski/stat/rf_inp1", "stat_rf_inp1_opened_lv")
						database.insert_sensor_activity("input1", "rf", "low", "opened")
						code_inp1_opened_lv = True

					code_inp1_closed_lv = False


				if code == RF_INP1_CLOSED_LV:
					if code_inp1_closed_lv == False:
						print("Received code: ", code)
						mqtt_pub("haski/stat/rf_inp1", "stat_rf_inp1_closed_lv")
						database.insert_sensor_activity("input1", "rf", "low", "closed")
						code_inp1_closed_lv = True

					code_inp1_opened_lv = False


			time.sleep(0.5)

	except KeyboardInterrupt:
		# client.disconnect()
		# client.loop_stop()
		rfdevice.cleanup()
		os.system('clear')


if __name__ == '__main__':
	rf_inp()
