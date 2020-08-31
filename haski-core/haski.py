##########################################################
# HASKi-CORE
#
# File Name: 	haski.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

from multiprocessing import Process
import paho.mqtt.client as mqtt
import sys, os
import time
from time import sleep
import init
import led, relay, wire_input, srx882, stx882, sim800, sonoff, controler




def main():

	try:
		init.database_setup()
		sleep(3)

		process_led = Process(target = led.led)
		process_led.start()

		process_rel = Process(target = relay.rel)
		process_rel.start()

		process_srx882 = Process(target = srx882.rf_inp)
		process_srx882.start()

		process_stx882 = Process(target = stx882.rf_out)
		process_stx882.start()

		process_wire_inp = Process(target = wire_input.wire_inp)
		process_wire_inp.start()

		process_sim800 = Process(target = sim800.sim800)
		process_sim800.start()

		process_sonoff = Process(target = sonoff.sonoff)
		process_sonoff.start()

		process_controler = Process(target = controler.controler)
		process_controler.start()

		sleep(1)

		# init.led_test()
		# init.relay_test()
		init.sim800_test()
		init.siren_beep()


		process_led1_blick = Process(target = led.led1_blick)
		process_led1_blick.start()


	except (KeyboardInterrupt):
		# os.system('clear')
		led.join()
		rel.join()
		rf_inp.join()
		rf_out.join()
		wire_inp.join()
		sim800.join()
		sonoff.join()
		controler.join()


	# finally:
	# 	os.system('clear')



if __name__ == '__main__':
	main()
