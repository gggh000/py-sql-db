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
from pySqlDbApi import *
from cmnLib3 import *

os.system("clear")

printBarDouble()
print("MAIN MENU")
displayMenu(['Display tables','Select table','Quit'],'Main menu')
printBarDouble()

