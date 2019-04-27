import os
import re

#    Initialize variables.

import mysql.connector

dbNamePws=os.environ["MYSQL_DB_PWS"]
dbNamePwsTbl=os.environ["MYSQL_DB_PWS_TABLE"]
dbNameUser=os.environ["MYSQL_DB_USER"]
mySqlServerIp=os.environ["MYSQL_SERVER_IP"]
print("database name: ", dbNamePws)
tableToUse=None

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

def displayTable(pCursor, pDb, pTable):
	print("Selecting records and displaying tables from ", pDb)
	pCursor.execute("SELECT * FROM " + pDb + "")
	myresult = pCursor.fetchall()
	
	for x in myresult:
        	print(x)

def printBarDouble():
    print("=================================================")

def printBarSingle():
    print("-------------------------------------------------")

'''
    Display a menu. 
    INPUT:  
    pMenu - menu to be display in string array format.
    pMenuTitle - Title of the menu to be displayed.

    RETURN:
    None
'''

def displayMenu(pMenu, pMenuTitle):
    os.system("clear")

    printBarSingle()

    if tableToUse:
        print("Table selected: ", tableToUse)
    else:
        print("No table selected.")

    printBarSingle()
    
    if pMenuTitle:
        print("---", pMenuTitle.upper(), "---")

    printBarSingle()

    counter = 1

    for x in pMenu:
        print(counter, ". ", x)
        counter += 1
    printBarSingle()

    print("Connecting to database...")

    return 0;
        
def waitInput(pPrompt, pTimeout, pRange):
    input = raw_input(pPrompt)
    return input

def mainMenuDispTbls():
    os.system("clear")
    print("Display Tables")
    mycursor = mydb.cursor()
    mycursor.execute("use " + dbNamePws)
    mycursor.execute("SHOW TABLES")
    
    for x in mycursor:
        print(x)

def mainMenuSelectTbl():
    os.system("clear")
    print("Display Tables")
    mycursor = mydb.cursor()
    mycursor.execute("use " + dbNamePws)
    mycursor.execute("SHOW TABLES")

    counter = 1    

    for x in mycursor:
        print(counter, ": ", x)
        
    print("Select Table by entering an index: ")

    for i in range(0, 10):
        try:
            select = int(input())
        except Exception as msg:
            print("Invalid input: ", select)
            continue

        if select > counter and select < 1:
           print("Invalid choice, try again: ")
        else:
            break
        
    if select > counter and select < 1:
        print("Invalid choice entered more than 10 times. Giving up...")
        return None

    print("You entered: ", select)
    counter = 1

    mycursor.execute("use " + dbNamePws)
    mycursor.execute("SHOW TABLES")

    for x in mycursor:
        if counter == select:
            print("Matchin table is found. Selecting this table...")
            x = re.sub("'|\(|\)|,","", str(x)).strip()
            print("use", str(x))
            tableToUse = x
            break

    
    
                 



