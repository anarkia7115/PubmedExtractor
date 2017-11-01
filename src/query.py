#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from render import XmlTagRemover

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

class ArticlesFile(object):
  def __init__(self, input_stream):
    self.lines = input_stream

  def stream_to_dict(self, lines):
    results = []

    for line in lines:
      line = line.rstrip("\n")
      line_fields = line.split('\t')
      pmid = line_fields[0]
      title = line_fields[1].replace('|', ' ') 
      abst = line_fields[2].replace('|', ' ')
      single_json = {'articleTitle': title, 'pmid': pmid, 'abstractText':abst}
      results.append(single_json)

    return results

  def get_dict(self):

    return self.stream_to_dict(self.lines)

class ArticlesMysql(object):
  def __init__(self, mysql):
    self.cnx = mysql
    self.cursor = mysql.getCursor()
    self.abs_formatter = XmlTagRemover("AbstractText")

  def findPmids(self, pmids):

    results = []
    queryScript = """select pmid, article_title, abstract_text
    from medline_citation
    where pmid in ('{pmids}');
    """.format(pmids="', '".join([str(x) for x in pmids]))

    self.cursor.execute(queryScript)

    for line in self.cursor.fetchall():
      pmid = line[0]
      title = line[1].replace('|', ' ') 
      abst = self.abs_formatter.trim(line[1].replace('|', ' '))
      singleJson = {'articleTitle': title, 'pmid': pmid, 'abstractText':abst}
      results.append(singleJson)

    return results

  def testFifty(self):
    return self.findPmids(self.getPmids())

  def findExcludeTable(self, exclude_pmid_table, limit_lines):
    results = []
    if limit_lines > 1000:
      print "[WARNING] too many lines to query: {}".format(limit_lines)

    queryScript = """
    select a.pmid, a.article_title, a.abstract_text
    from pubmed.medline_citation a
    left outer join {} b
    on a.pmid = b.pmid
    where b.pmid is null
    limit {};""".format(exclude_pmid_table, limit_lines)

    self.cursor.execute(queryScript)

    for line in self.cursor.fetchall():
      pmid = line[0]
      title = line[1].replace('|', ' ') 
      abst = self.abs_formatter.trim(line[2].replace('|', ' '))
      singleJson = {'articleTitle': title, 'pmid': pmid, 'abstractText':abst}
      results.append(singleJson)

    return results

  def getPmids(self):

    queryScript = """select pmid
    from medline_citation 
    order by pmid desc 
    limit 100;"""

    self.cursor.execute(queryScript)

    return [str(x[0]) for x in self.cursor.fetchall()]


class TermMysql(object):

  def __init__(self, mysql):
    self.cnx = mysql
    self.cursor = mysql.getCursor()

  def insert_terms(self, term_list, out_table):

    insert_term_query = """
    INSERT INTO {}
    (pmid, mention_start, mention_end, mention, tag, term_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """.format(out_table)

    self.cursor.executemany(insert_term_query, term_list)

  def insert_pmids(self, pmids, uniq_pmids_table):
    insert_query = """
    INSERT INTO {}
    (pmid)
    VALUES (%(pmid)s)
    """.format(uniq_pmids_table)
    self.cursor.executemany(insert_query, pmids)


  def commit(self):
    self.cnx.commit()
