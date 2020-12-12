# catBD.py

import sqlite3

database = sqlite3.connect('extensions.db')
cur = database.cursor()

f = open('c.txt', 'r')
cont = f.read().splitlines()

for i in cont:
    d = i.split(':')
    cat = d[0] + ' Files'
    exts = d[1].split()
    # print(cat, exts)
    for j in exts:
        query = "update Extensions set Category = '{0}' where Name = '{1}';".format(cat,j) 
        cur.execute(query)
        # print(query)
    database.commit()

cur.close()
database.close()