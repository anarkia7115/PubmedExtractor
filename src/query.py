#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import config
from pymongo import MongoClient

class Collection:

    """
        init connection
    """
    def __init__(self, collectionName):
        host    = config.mongodb['host']
        port    = config.mongodb['port']
        db      = "pubmed"

        client  = MongoClient(host=host, port=port)
        db      = client[db]

        self.collection = db[collectionName]

    """
        find one pmid
    """
    def findPmid(self, pmid):
        return self.collection.find_one({"pmid": pmid})

    """
        find [pmid1, pmid2, ... pmidN]
    """
    def findPmids(self, pmids):
        results = []

        # exec mongodb search (pmids.length) times
        for pmid in pmids:
            r = self.findPmid(pmid)
            results.append(r)

        return results

    def testOne(self):
        return self.findPmid(20423155)

    def testTwo(self):
        return self.findPmids([20423155, 20423156])
