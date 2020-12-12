# rand.py

import sqlite3
import os

currentDirectory = os.getcwd()
pathToDB =os.path.join(currentDirectory ,'extensions.db')   #Create path to database
database = sqlite3.connect(pathToDB)                        #Connect to database
cur = database.cursor()

####
query = 'select * from Extensions where Description like "%html%"'
####

obj = cur.execute(query)
data = obj.fetchall()

for i in data:
    print(i)
