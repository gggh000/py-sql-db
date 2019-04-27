import os
import re
import time

#    Initialize variables.

import mysql.connector

def printBarDouble():
    print("=================================================")

def printBarSingle():
    print("-------------------------------------------------")

class mysqlManager:

    tableToUse = None
    dbNamePws= None
    dbNamePwsTbl= None
    dbNameUser=None
    mySqlServerIp=None
    tableToUse=None
    debug = 1
    mydb = None

    def __init__(self):
        if self.debug:
            print("mySqlManager.__init__ entered...")

        self.dbNamePws=os.environ["MYSQL_DB_PWS"]
        self.dbNamePwsTbl=os.environ["MYSQL_DB_PWS_TABLE"]
        self.dbNameUser=os.environ["MYSQL_DB_USER"]
        self.mySqlServerIp=os.environ["MYSQL_SERVER_IP"]
        print("database name: ", self.dbNamePws)
        self.tableToUse=None

        try:
            self.mydb = mysql.connector.connect(
              host=self.mySqlServerIp,
              user=self.dbNameUser,
              passwd="",
              database=self.dbNamePws
            )

        except Exception as msg:
            print("Failed to connect to database: ", self.dbNamePws)
            print(msg)
            exit(1)

        print("OK, connected to database...")
        print(self.mydb)
        time.sleep(2)

    def displayTable(pCursor, pDb, pTable):
	    print("Selecting records and displaying tables from ", pDb)
	    pCursor.execute("SELECT * FROM " + pDb + "")
	    myresult = pCursor.fetchall()
	    
	    for x in myresult:
        	    print(x)
    
    '''
        Display a menu. 
        INPUT:  
        pMenu - menu to be display in string array format.
        pMenuTitle - Title of the menu to be displayed.
    
        RETURN:
        None
    '''
    
    def waitInput(self, pPrompt, pTimeout, pRange):
        input = raw_input(pPrompt)
        return input
    
    def mainMenuDispTbls(self):
        os.system("clear")
        print("Display Tables")
        mycursor = mydb.cursor()
        mycursor.execute("use " + self.dbNamePws)
        mycursor.execute("SHOW TABLES")
        
        for x in mycursor:
            print(x)
    
    def mainMenuSelectTbl(self):
        os.system("clear")
        print("Display Tables")
        mycursor = self.mydb.cursor()
        mycursor.execute("use " + self.dbNamePws)
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
    
        mycursor.execute("use " + self.dbNamePws)
        mycursor.execute("SHOW TABLES")
    
        for x in mycursor:
            if counter == select:
                print("Matchin table is found. Selecting this table...")
                x = re.sub("'|\(|\)|,","", str(x)).strip()
                print("use", str(x))
                self.tableToUse = x
                break
    
    def displayMenu(self, pMenu, pMenuTitle):
        os.system("clear")
    
        printBarSingle()
    
        if self.tableToUse:
            print("Table selected: ", self.tableToUse)
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
            
    
            
        
                     
    
    
    
