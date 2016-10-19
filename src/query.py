#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

class Articles(object):
    """ init db info
    """
    def __init__(self, mongo):
        self.collection = mongo.getCollection()

    """ find one pmid
    """
    def findPmid(self, pmid):
        return self.collection.find_one({"pmid": pmid})

    """ find [pmid1, pmid2, ... pmidN]
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

    def getPmids(self):
        cursor = self.collection.find(
            {}, {'pmid':1, '_id':0}).sort("pmid",-1).limit(50)
        pmids = []

        for pmid in cursor:
            if 'pmid' in pmid:
                pmids.append(pmid['pmid'])

        return pmids

    def testFifty(self):
        return self.findPmids(self.getPmids())
