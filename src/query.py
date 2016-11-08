#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

class ArticlesMongo(object):
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


class ArticlesMysql(object):
    def __init__(self, mysql):
        self.cursor = mysql.getCursor()

    def findPmids(self, pmids):

        results = []
        queryScript = """select pmid, abstract_text
        from medline_citation
        where pmid in ('{pmids}');
        """.format(pmids="', '".join([str(x) for x in pmids]))

        self.cursor.execute(queryScript)

        for line in self.cursor.fetchall():
            pmid = line[0]
            abst = line[1].replace('|', ' ')
            singleJson = {'pmid': pmid, 'abstractText':abst}
            results.append(singleJson)

        return results

    def testFifty(self):
        return self.findPmids(self.getPmids())

    def getPmids(self):

        queryScript = """select pmid
        from medline_citation 
        order by pmid desc 
        limit 100;"""

        self.cursor.execute(queryScript)

        return [str(x[0]) for x in self.cursor.fetchall()]
