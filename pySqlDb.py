#!/usr/bin/python3

'''
PASSWORD AND PHONE NO. MANAGEMENT SYSTEM.
GUYEN GN.
THIS UTILITY REQUIRES MYSQL SERVER RUNNING ON CONFIG_MYSQL_IP
'''

def printBarDouble():
	print("=================================================")

def printBarSingle():
	print("-------------------------------------------------")

import os
import sys
import time
from pySqlDbApi import *
prompt = 1
EXIT_MENU = 3

if __name__ == "__main__":
    from cmnLib3 import *
    pwManager = mysqlManager()
    
    dispatchMapMenu = {\
    1: pwManager.mainMenuDispTbls, \
    2: pwManager.mainMenuSelectTbl \
    }

    while prompt:
        os.system("clear")
        printBarDouble()
        print("MAIN MENU")

        if not pwManager.tableToUse:
            pwManager.displayMenu(['Display tables','Select table','Quit'],'Main menu')
        else:
            pwManager.displayMenu(['Display tables','Select table', 'Search for an entry', 'Input new entry', 'Quit'],'Main menu')

        dispatchMapMenu[3] = pwManager.mainMenuSearchForEntry
        dispatchMapMenu[4] = pwManager.mainMenuInputNewEntry
        printBarDouble()
        EXIT_MENU = 5
        
        try:
            prompt = int(input("Select from menu above...\n"))
    
            if int(prompt) == EXIT_MENU:
                print("Exiting...")
                exit(0)
        except Exception as msg:
            print("Error interpreting input, try again...")
            print(msg)
    
        print(dispatchMapMenu)

        a = dispatchMapMenu[prompt]
        a()
        input("Press a key to continue.")
    
