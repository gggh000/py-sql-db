import os

#    Initialize variables.

import mysql.connector
dbNamePws=os.environ["MYSQL_DB_PWS"]
dbNamePwsTbl=os.environ["MYSQL_DB_PWS_TABLE"]
dbNameUser=os.environ["MYSQL_DB_USER"]
mySqlServerIp=os.environ["MYSQL_SERVER_IP"]
print("database name: ", dbNamePws)

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

    if pMenuTitle:
        print("---", pMenuTitle.upper(), "---")

    printBarSingle()

    counter = 1

    for x in pMenu:
        print(counter, ". ", x)
        counter += 1
    printBarSingle()

    print("Connecting to database...")

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

    mycursor = mydb.cursor()
    mycursor.execute("use " + dbNamePws)
    mycursor.execute("SHOW TABLES")
    
    for x in mycursor:
        print(x)

    return 0;
        
def waitInput(pPrompt, pTimeout, pRange):
    input = raw_input(pPrompt)
    return input

def mainMenuDispTbls():
    os.system("clear")
    print("Display Tables")

def mainMenuSelectTbl():
    os.system("clear")
    print("Select Table")


