#!/usr/bin/python3

'''
PASSWORD AND PHONE MANAGEMENT SYSTEM.
GUYEN GN.
THIS UTILITY REQUIRES MYSQL SERVER RUNNING ON CONFIG_MYSQL_IP
'''

def printBarDouble():
	print("=================================================")

def printBarSingle():
	print("-------------------------------------------------")

import os
import sys
import re
import mysql.connector

from cmnLib3 import *
presenceDb = None
presenceTable = None

os.system("clear")

#	Initialize variables.

dbNamePws=os.environ["MYSQL_DB_PWS"]
dbNamePwsTbl=os.environ["MYSQL_DB_PWS_TABLE"]
dbNameUser=os.environ["MYSQL_DB_USER"]
mySqlServerIp=os.environ["MYSQL_SERVER_IP"]
print("database name: ", dbNamePws)

#	connect to mysql server.

mydb = mysql.connector.connect(
  host=mySqlServerIp,
  user=dbNameUser,
  passwd="",
)

if not mydb:
	print("Connection failure to db")
	sys.exit(1)

#	init cursor.

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

for x in mycursor:
	print(x)

	if re.search(dbNamePws, str(x)):
		print("Found database.")
		presenceDb = 1	

print(type(mycursor))

if presenceDb:
	print("Database exists, connecting...")
	try:
		mydb = mysql.connector.connect(
  		host=mySqlServerIp,
  		user=dbNameUser,
  		passwd="",
  		database=dbNamePws
		)
	except Exception as msg:
		print("Failed to connect to database: ", dbNamePws)
		print(msg)
		exit(1)
	print("OK")
else:
	print("Database does not exist, creating...")
	mycursor.execute("CREATE DATABASE " + dbNamePws)

# 	Check if table exists.

mycursor = mydb.cursor()
mycursor.execute("use " + dbNamePws)
mycursor.execute("SHOW TABLES")

for x in mycursor:
	print(x)	

	if re.search(dbNamePwsTbl, str(x)):
		print("Table", x, " is found.")
		break

if not presenceTable:
	try:
		print("Table does not exist. Creating a table with primary keys.")
		mycursor.execute("CREATE TABLE " + dbNamePwsTbl + " (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255), entry VARCHAR(255), password VARCHAR (255), misc1 VARCHAR(255), misc2 VARCHAR(255))")
	except Exception as msg:
		print(msg)
#else:
#	print("Table exists. Creating a primary key.")
#	mycursor.execute("ALTER TABLE " + dbNamePws + " ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

#	Insert a record

mydb.commit()

print(mycursor.rowcount, "record inserted.")

#	Selecting record from table and showing all.

print("Selecting records and displaying tables from ", dbNamePwsTbl)
mycursor.execute("SELECT * FROM " + dbNamePwsTbl + "")
myresult = mycursor.fetchall()

for x in myresult:
 	print(x)

#	Insert a record.

sql = "INSERT INTO " + str(dbNamePwsTbl) + " (category, entry, password, misc1, misc2) VALUES (%s, %s, %s, %s, %s)"
val = ("none", "www.example.com", "8981555aaa", "none", "none")
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")			

#	Re-displaying records from table.

mycursor = mydb.cursor()
print("Selecting records and displaying tables from ", dbNamePwsTbl)
mycursor.execute("SELECT * FROM " + dbNamePwsTbl + "")
myresult = mycursor.fetchall()

for x in myresult:
 	print(x)
