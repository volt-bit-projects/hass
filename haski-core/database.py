##########################################################
# HASKi-CORE
#
# File Name: 	database.py
# Author:    	David Janoušek
# Copyright:	© 2020 David Janoušek, All Rights Reserved
# Website:   	www.volt-bit-projects.com
# License:		MIT License
# Version:  	1.0.0
##########################################################

import pymysql
from configparser import ConfigParser


config_object = ConfigParser()
config_object.read("config.ini")


db_setup = config_object["MARIADB"]
db_address = db_setup["db_address"]
db_name = db_setup["db_name"]
root_user = db_setup["root_user"]
root_password = db_setup["root_password"]
haski_user = db_setup["haski_user"]
haski_password = db_setup["haski_password"]




# check if database haski exists on the MariaDB server
def check_db_exists():
	try:
		db = pymysql.connect(db_address, root_user, root_password, db_name)
		db.close()
		db_exists = True

	except:
		db_exists = False

	finally:
		return db_exists



def check_user_exists():
	db = pymysql.connect(db_address, root_user, root_password)								# open connection to haski database
	cursor = db.cursor()

	try:
		cursor.execute("SELECT User FROM mysql.user")											# execute the SQL command
		results = cursor.fetchall()

		if 'haski' in str(results):
			user_exists = True
		else:
			user_exists = False

	except:
		user_exists = False

	finally:
		db.close()
		return user_exists



# delete database haski from MariaDB server
def delete_db():
	db = pymysql.connect(db_address, root_user, root_password)
	print("Deleting %s database ..." % (db_name))

	try:
		cursor = db.cursor()
		cursor.execute('DROP DATABASE %s'%(db_name))
		print("%s database deleted sucessfully.\n" % (db_name))

	except:
		print("%s database doesn't exist.\n" % (db_name))

	finally:
		db.close



# create database haski at MariaDB server
def create_db():
	print("Creating new %s database ..." % (db_name))

	db = pymysql.connect(db_address, root_user, root_password)

	try:
		cursor = db.cursor()
		cursor.execute("CREATE DATABASE %s CHARACTER SET UTF8"%(db_name))

	finally:
		db.close
		print("%s database created sucessfully.\n" % (db_name))

	print("Creating %s tables ..." % (db_name))

	try:
		db = pymysql.connect(db_address, root_user, root_password, db_name)
		cursor = db.cursor()

		# Create table SensorActivity
		sql = """CREATE TABLE SensorActivity (
			id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			SensorName CHAR(50) NOT NULL,
			ConnectionType CHAR(10) NOT NULL,
			BatteryLevel CHAR(10) NOT NULL,
			Status CHAR(50) NOT NULL)"""
		cursor.execute(sql)
		print ("Table SensorActivity created successfully.")


		# Create table RfOutStatus
		sql = """CREATE TABLE RfOutStatus (
			id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			RfOutName CHAR(50) NOT NULL,
			Status CHAR(50) NOT NULL)"""
		cursor.execute(sql)
		print ("Table RfOutStatus created successfully.")


		# Create table RelayStatus
		sql = """CREATE TABLE RelayStatus (
			id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			RelayName CHAR(50) NOT NULL,
			Status CHAR(50) NOT NULL)"""
		cursor.execute(sql)
		print ("Table RelayStatus created successfully.")


		# Create table SonoffStatus
		sql = """CREATE TABLE SonoffStatus (
			id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			SonoffName CHAR(50) NOT NULL,
			Status CHAR(50) NOT NULL)"""
		cursor.execute(sql)
		print ("Table SonoffStatus created successfully.")


		# Create table AlarmEvent
		sql = """CREATE TABLE AlarmEvent (
			id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			SensorName CHAR(50) NOT NULL)"""
		cursor.execute(sql)
		print ("Table AlarmEvent created successfully.")


		# Create table Zone1Log
		sql = """CREATE TABLE LogZone1
			(id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			Name CHAR(50) NOT NULL,
			Status CHAR(10) NOT NULL)"""
		cursor.execute(sql)
		print ("Table LogZone1 created successfully.")


		# Create table ZoneLog
		sql = """CREATE TABLE LogZone2
			(id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Time DATETIME NOT NULL,
			Name CHAR(50) NOT NULL,
			Status CHAR(10) NOT NULL)"""
		cursor.execute(sql)
		print ("Table LogZone2 created successfully.")


		# Create table Zone1
		sql = """CREATE TABLE StatusZone1
			(id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Status BOOL NOT NULL)"""
		cursor.execute(sql)
		print ("Table Zone1 created successfully")


		# Create table Zone2
		sql = """CREATE TABLE StatusZone2
			(id INTEGER PRIMARY KEY AUTO_INCREMENT,
			Status BOOL NOT NULL)"""
		cursor.execute(sql)
		print ("Table Zone2 created successfully.")

	finally:
		db.close

		print("Database %s ready to use.\n" % (db_name))


	# enter default values to StatusZone1 and StatusZone2 tables
	try:
		db = pymysql.connect(db_address, root_user, root_password, db_name)
		print("Entering DB default values ...")
		cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO StatusZone1 (Status) VALUES (false)"""
		cursor.execute(sql)
		db.commit()

		# Prepare SQL query to INSERT a record into the database.
		sql = """INSERT INTO StatusZone2 (Status) VALUES (false)"""
		cursor.execute(sql)
		db.commit()

	except:
		db.rollback()

	finally:
		db.close()
		print("All tables created successfully.\n")



def delete_user():
	db = pymysql.connect(db_address, root_user, root_password)
	print("Deleting %s user from database ..." % (db_name))

	try:
		cursor = db.cursor()
		cursor.execute("DROP USER '%s'@'localhost';"%(haski_user));
		print("User %s deleted sucessfully.\n" % (haski_user))

	except:
		print("User %s doesn't exist.\n" % (haski_user))

	finally:
		db.close



def create_user():
	db = pymysql.connect(db_address, root_user, root_password, db_name)
	print("Creating new user %s ..." % haski_user)

	try:
		cursor = db.cursor()
		cursor.execute("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';"%(haski_user, haski_password));
		cursor.execute("GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost';"%(haski_user, haski_user));
		cursor.execute("FLUSH PRIVILEGES")

	finally:
		db.close
		print("New user %s created sucessfully.\n" % (haski_user))




# insert sensor activity
def insert_sensor_activity(sensor_name, connection_type, battery_level, status):
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO SensorActivity (Time, SensorName, ConnectionType, BatteryLevel, Status) VALUES (NOW(), %s, %s, %s, %s)", (sensor_name, connection_type, battery_level, status))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()


# insert RF Output Status
def insert_rf_out_status(rf_out_name, status):
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO RfOutStatus (Time, RfOutName, Status) VALUES (NOW(), %s, %s)", (rf_out_name, status))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()


# insert RelayStatus
def insert_relay_status(relay_name, status):
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO RelayStatus (Time, RelayName, Status) VALUES (NOW(), %s, %s)", (relay_name, status))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()



# insert SonoffStatus
def insert_sonoff_status(sonoff_name, status):
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO SonoffStatus (Time, SonoffName, Status) VALUES (NOW(), %s, %s)", (sonoff_name, status))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()




# insert alarm event
def insert_alarm_event(sensor_name):
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO AlarmEvent (Time, SensorName) VALUES (NOW(), %s)", (sensor_name))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()



# insert logZone1
def insert_log_zone1(status):
	zone1_name = "Byt"
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO LogZone1 (Time, Name, Status) VALUES (NOW(), %s, %s)", (zone1_name, status))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()



# insert logZone2
def insert_log_zone2(status):
	zone2_name = "Sklep"
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("INSERT INTO LogZone2 (Time, Name, Status) VALUES (NOW(), %s, %s)", (zone2_name, status))
		db.commit()

	except:
	   db.rollback()

	finally:
		db.close()



# get StatusZone1
def get_status_zone1():
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("SELECT id, Status FROM StatusZone1")
		results = cursor.fetchall()
		for row in results:
			status_zone1 = row[1]

	except:
		print ("Error: unable to fetch data")

	finally:
		db.close()

	return status_zone1



# get StatusZone1
def get_status_zone2():
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("SELECT id, Status FROM StatusZone2")
		results = cursor.fetchall()
		for row in results:
			status_zone2 = row[1]

	except:
		print ("Error: unable to fetch data")

	finally:
		db.close()

	return status_zone2



# change StatusZone1
def change_status_zone1():
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("SELECT id, Status FROM StatusZone1")
		results = cursor.fetchall()
		for row in results:
			status_zone1 = row[1]

		if status_zone1 == False:
			cursor.execute("UPDATE StatusZone1 SET Status = true WHERE ID = 1")
		elif status_zone1 == True:
			cursor.execute("UPDATE StatusZone1 SET Status = false WHERE ID = 1")
		db.commit()

	except:
		db.rollback()

	finally:
		db.close()


# change StatusZone2
def change_status_zone2():
	db = pymysql.connect(db_address, haski_user, haski_password, db_name)
	cursor = db.cursor()

	try:
		cursor.execute("SELECT id, Status FROM StatusZone2")
		results = cursor.fetchall()
		for row in results:
			status_zone2 = row[1]

		if status_zone2 == False:
			cursor.execute("UPDATE StatusZone2 SET Status = true WHERE ID = 1")
		elif status_zone2 == True:
			cursor.execute("UPDATE StatusZone2 SET Status = false WHERE ID = 1")
		db.commit()

	except:
		db.rollback()

	finally:
		db.close()



# main program start
def main():
	pass
	# create_db()
	# create_user()
	# delete_user()
	# delete_db()


if __name__ == '__main__':
	main()
