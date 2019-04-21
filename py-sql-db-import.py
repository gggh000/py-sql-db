#!/usr/bin/python3

'''
PASSWORD AND PHONE MANAGEMENT SYSTEM.
GUYEN GN.
THIS UTILITY REQUIRES MYSQL SERVER RUNNING ON CONFIG_MYSQL_IP
If repeatedly run this will re-import the xlsx without checking over and over again.
If you need to reimport it, then it is advisabae to remove the table first by:

mysql -i root -p
show databases;
use passwds
show tables;
drop table <MY_SQL_DB_PWS_TABLE>;
exit

'''

#   Helper functions.

def printBarDouble():
    print("=================================================")

def printBarSingle():
    print("-------------------------------------------------")

#   Import statements. 

import os
import sys
import re
import mysql.connector
import time
from openpyxl import *
from cmnLib3 import *

presenceDb = None
presenceTable = None
insertErrors = {}

os.system("clear")

#    Initialize variables.

dbNamePws=os.environ["MYSQL_DB_PWS"]
dbNamePwsTbl=os.environ["MYSQL_DB_PWS_TABLE"]
dbNameUser=os.environ["MYSQL_DB_USER"]
mySqlServerIp=os.environ["MYSQL_SERVER_IP"]
print("database name: ", dbNamePws)
fileNameExcel='NUMBERS2010-97.xlsx'

#    Connect to mysql server, root without password.

mydb = mysql.connector.connect(
  host=mySqlServerIp,
  user=dbNameUser,
  passwd="",
)

if not mydb:
    print("Connection failure to db")
    sys.exit(1)

#    Init cursor.

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)

    if re.search(dbNamePws, str(x)):
        print("Found database.")
        presenceDb = 1    

print(type(mycursor))

#   If db exists, connect, otherwise create one.

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

#     Check if table exists.

mycursor = mydb.cursor()
mycursor.execute("use " + dbNamePws)
mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)    

    if re.search(dbNamePwsTbl, str(x)):
        print("Table", x, " is found.")
        break

#   Create the table if it does not exist.

if not presenceTable:
    try:
        print("Table does not exist. Creating a table with primary keys.")
        mycursor.execute("CREATE TABLE " + dbNamePwsTbl + " (id INT AUTO_INCREMENT PRIMARY KEY, \
            index INT, \
            category VARCHAR(255), \
            entry VARCHAR(255), \
            password VARCHAR (255), \
            misc1 VARCHAR(255), \
            misc2 VARCHAR(255), \
            misc3 VARCHAR(255))")
    except Exception as msg:
        print(msg)

''' Commented out because of logic issues.

#else:
#    print("Table exists. Creating a primary key.")
#    mycursor.execute("ALTER TABLE " + dbNamePws + " ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#print(mycursor.rowcount, "record inserted.")

mydb.commit()
'''
'''
#    Insert a record. This snipped was initially used for testing purpose. It is retained here as a code referenec.

#    Selecting record from table and showing all.

print("Selecting records and displaying tables from ", dbNamePwsTbl)
mycursor.execute("SELECT * FROM " + dbNamePwsTbl + "")
myresult = mycursor.fetchall()

for x in myresult:
     print(x)

#    Insert a record by defining the columns.

sql = "INSERT INTO " + str(dbNamePwsTbl) + " (category, index, entry, password, misc1, misc2, misc3) VALUES (%s, %s, %s, %s, %s, %s)"
val = ("none", "none", "www.example.com", "8981555aaa", "none", "none", "none")
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record inserted.")            

#    Re-displaying records from table.

mycursor = mydb.cursor()
print("Selecting records and displaying tables from ", dbNamePwsTbl)
mycursor.execute("SELECT * FROM " + dbNamePwsTbl + "")
myresult = mycursor.fetchall()

for x in myresult:
     print(x)
'''

''' NEW WORK BOOK creation. It is kept here only used as a code reference.
wb = Workbook()
# grab the active worksheet
ws = wb.active
'''

#   Deleting all record first.

mycursor = mydb.cursor()
print("Selecting records and displaying tables from ", dbNamePwsTbl)

try:
    mycursor.execute("DELETE FROM " + dbNamePwsTbl + "")
except Exception as msg:
    print(msg)
    time.sleep(3)

#   Load the xlsx file and load the worksheet and start importing.

wb = load_workbook(filename = fileNameExcel)
sheet_ranges = wb['number']
col_ranges=['A','B','C','D','E','F','G']
row_ranges=range(1, 1112)
fp = open("importErrors.log",'w')

counter = 0;

for i in row_ranges:
    printBarSingle()
    val = []
    for j in col_ranges:
        print("reading cell: i/j: ", str(j), "/",  str(i))

        cellContent = (str(sheet_ranges[str(j) + str(i)].value))

        if j == 0:
            cellContent = counter
        
        val.append(cellContent.strip())

    counter += 1

    print("val: ")
    print(val)

    try:
        sql = "INSERT INTO " + str(dbNamePwsTbl) + " (index, category, entry, password, misc1, misc2, misc3) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as msg:
        print(msg)
        msg = str(msg).strip()
        msg = re.sub("\"|\'", "", msg)
        fp.write(str(i) + str(j) + ": " + str(msg) + '\n')
        insertErrors[str(i) + str(j)] =  msg

print("Insertion errors: ")

for i in insertErrors:
    print(i)

fp.close()

