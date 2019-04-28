import os
import re
import time
from prettytable import *
from tableWrapper import *

#    Initialize variables.

import mysql.connector

def printBarDouble():
    print("=================================================")

def printBarSingle():
    print("-------------------------------------------------")

#   class for managing the all aspects of mySql interaction from python. This class
#   heavily uses and depends on the mysql.connector but also adds additional layer of 
#   API which mainly for processing menu item choices. 

class mysqlManager:

    #   Class member variable definitions.

    tableToUse = None
    dbNamePws= None
    dbNamePwsTbl= None
    dbNameUser=None
    mySqlServerIp=None
    debug = 1
    mydb = None
    mycursor = None

    #   Class constructor, initialize member variables.

    def __init__(self):
        if self.debug:
            print("mySqlManager.__init__ entered...")

        self.dbNamePws=os.environ["MYSQL_DB_PWS"]
        self.dbNamePwsTbl=os.environ["MYSQL_DB_PWS_TABLE"]
        self.dbNameUser=os.environ["MYSQL_DB_USER"]
        self.mySqlServerIp=os.environ["MYSQL_SERVER_IP"]
        print("database name: ", self.dbNamePws)
        self.tableToUse=None

        #   Connect to database as part of initialization. If connection fails, quit immediately.

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
        time.sleep(1)

    '''
    Display selected table. The tables to display under pDb database.
    If no tables are present, it will quit silently.
    INPUT:
        pCursor - mysql database cursor object.
        pDb - database from which the tables are to be displayed.
        pTable - unnecessary input, delete after a while! 
    OUTPUT:
        None
    '''

    def displayTable(pCursor, pDb, pTable):
	    print("Selecting records and displaying tables from ", pDb)
	    pCursor.execute("SELECT * FROM " + pDb + "")
	    myresult = pCursor.fetchall()
	    
	    for x in myresult:
        	    print(x)
    
    '''
    Waits for input from user.
    INPUT:  
        pPrompt - tells user what input is expected
        pTimeOut - timeout of wait (not implemented yet)
        pRange - accepted range of values (not implemeted yet)    
    OUTPUT:
        input - user's input that are entered.
    '''
    
    def waitInput(self, pPrompt, pTimeout, pRange):
        input = raw_input(pPrompt)
        return input
    
    '''
    Display all tables in database. Database selected is defined in self.dbNamePws.
    INPUT:
        None
    OUTPUT:
        None
    '''

    def mainMenuDispTbls(self):
        os.system("clear")
        print("Display Tables")
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("use " + self.dbNamePws)
        self.mycursor.execute("SHOW TABLES")
        
        for x in self.mycursor:
            print(x)
    
    '''
    Selects one of the table as active, as a result, self.tableToUse is updated with active, selected table. 
    INPUT:
        None
    OUTPUT:
        None
    '''

    def mainMenuSelectTbl(self):
        os.system("clear")
        print("Display Tables")
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("use " + self.dbNamePws)
        self.mycursor.execute("SHOW TABLES")
        INPUT_RETRY_MAX = 10

        counter = 1    
    
        for x in self.mycursor:
            print(counter, ": ", x)
            
        print("Select Table by entering an index: ")

        #   Prompt use for INPUT_RETRY_MAX times. After that give up.
    
        for i in range(0, INPUT_RETRY_MAX):
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
            print("Invalid choice entered more than ", INPUT_RETRY_MAX, " times. Giving up...")
            return None
    
        print("You entered: ", select)
        counter = 1

        #   Iterate through the tables for matching index and if matches, update the tableToUse.
    
        self.mycursor.execute("use " + self.dbNamePws)
        self.mycursor.execute("SHOW TABLES")
    
        for x in self.mycursor:
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
        return 0
            
    def mainMenuSearchForEntry(self):
        searchPattern = None
        counter = 0

        while searchPattern == None:
            if counter > 5:
                print("Empty search value entered too many times. Giving up.")
                return None                

            searchPattern = input("Input your pattern to search (all columns are searched):").strip()
            if searchPattern == None:
                print("Nothing is entered. Try again:")

            counter += 1

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("use " + self.dbNamePws)
        print("select * from " + str(self.tableToUse) + " where CONCAT(category,entry,password,misc1,misc2,misc3) like '%" + searchPattern + "%';")
        time.sleep(3)
        self.mycursor.execute("select * from " + str(self.tableToUse) + " where CONCAT(category,entry,password,misc1,misc2,misc3) like '%" + searchPattern + "%';")

        printBarSingle()
        print("Search result for " + str(searchPattern))
        printBarSingle()

        t = PrettyTable(['id','idx','category','entry','password','misc1','misc2','misc3'])
        t.max_width = 15

        for x in self.mycursor:
            t.add_row(x)                        
       
        print(t)

        '''
        labels = (['id','idx','category','entry','password','misc1','misc2','misc3'])
        tableData=[]

        COL_WIDTH = 15

        for x in self.mycursor:
            x = list(x)
            printBarSingle()
            print(x)
            print(type(x))
        
            for i in range(0, len(str(max(x, key=len))) - 1 / COL_WIDTH + 1, COL_WIDTH):
                tableData.append(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
        
        for i in tableData:
            print(i)

        '''
        printBarSingle()
        input("Press a key to continue.")
        return 1

    def mainMenuInputNewEntry(self):
        inputFields = ["idx", "category", "entry", "password", "misc1", "misc2", "misc3"]
        inputFieldValues = len(inputFields) * [None]
        inputFieldValues[0] = -1

        for i in range(1, len(inputFields)):
            inputFieldValues[i] = input("Enter " + str(inputFields[i]) + " value: ")

        sql = "INSERT INTO " + str(self.dbNamePwsTbl) + \
            " (idx, category, entry, password, misc1, misc2, misc3) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.execute(sql, inputFieldValues)
        self.mydb.commit()
        return 0
    
#select * from raw where CONCAT(<col1>, <col2>, .... <colN>) like '%<pattern>%';
