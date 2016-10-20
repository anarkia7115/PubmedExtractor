#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import config

class Mongo(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print "new db connection."
            cls.instance = super(Mongo, cls).__new__(cls)
        else: 
            print "load previous db connection."
        return cls.instance

    """ init connection
    """
    def __init__(self):
        host    = config.mongodb['host']
        port    = config.mongodb['port']
        dbName  = "pubmed"

        from pymongo import MongoClient
        client  = MongoClient(host=host, port=port)
        self.db      = client[dbName]

    """ Set Collection Name
    """
    def setCollection(self, collectionName):
        #self.collectionName = collectionName
        self.collection = self.db[collectionName]

    def getCollection(self):
        return self.collection

class Mysql(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print "new db connection."
            cls.instance = super(Mysql, cls).__new__(cls)
        else: 
            print "load previous db connection."
        return cls.instance

    def __init__(self):
        host = config.mysql['host']
        user = config.mysql['user']
        passwd = config.mysql['passwd']
        db = config.mysql['db']
        import MySQLdb
        db = MySQLdb.connect(
            host=host,
            user=user,
            passwd=passwd,
            db=db
        )
        self.cur = db.cursor()

    def getCursor(self):
        return self.cur

