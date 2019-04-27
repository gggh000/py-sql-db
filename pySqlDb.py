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
import time
from pySqlDbApi import *

prompt = 1

if __name__ == "__main__":
    from cmnLib3 import *
#   from pySqlDbApi import *

    pwManager = mysqlManager()
    
    dispatchMapMenu = {\
    1: pwManager.mainMenuDispTbls, \
    2: pwManager.mainMenuSelectTbl \
    }
    
    
    while prompt:
        os.system("clear")
    
        printBarDouble()
        print("MAIN MENU")
        pwManager.displayMenu(['Display tables','Select table','Quit'],'Main menu')
        printBarDouble()
        
        try:
            prompt = int(input("Select from menu above...\n"))
    
            if int(prompt) == 3:
                print("Exiting...")
                exit(0)
        except Exception as msg:
            print("Error interpreting input...")
            print(msg)
            time.sleep(5)
    
        print(dispatchMapMenu)

        a = dispatchMapMenu[prompt]
        a()
        input("Press a key to continue.")
    
