import os

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

def displayMenu(pMenu, pMenuTitle):
    os.system("clear")

    printBarSingle()

    if pMenuTitle:
        print("---", pMenuTitle.upper(), "---")

    printBarSingle()

    counter = 0

    for x in pMenu:
        print(counter, ". ", x)
        counter += 1
    printBarSingle()
    

