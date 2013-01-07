'''
Created on Jan 6, 2013

@author: pixo
'''
import os
import couchdb

def getDataBase():
    serveradress=os.getenv("HK_DB_SERVER")
    databasename=os.getenv("HK_DB")
    server = couchdb.Server(serveradress)
    return server[databasename]