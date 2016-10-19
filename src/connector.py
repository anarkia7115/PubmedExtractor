#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import config
from pymongo import MongoClient

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
        dbName      = "pubmed"

        client  = MongoClient(host=host, port=port)
        self.db      = client[dbName]

    """ Set Collection Name
    """
    def setCollection(self, collectionName):
        #self.collectionName = collectionName
        self.collection = self.db[collectionName]

    def getCollection(self):
        return self.collection

