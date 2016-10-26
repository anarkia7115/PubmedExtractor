#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import re

class AbstractSaver:

    """
        1. read json data
        2. get pmid
        3. get abstract
        4. save to file as format:

            26116688|t|Syphilis and gonorrhoea increase sharply in England.
            26116688|a|-No abstract-

    """
    def __init__(self, jsonDatas, outputPath):

        self.articles    = jsonDatas
        self.outputPath = outputPath

    def parse(self, singleJson):

        if 'abstractText' in singleJson:
            abstract = singleJson['abstractText']
            if abstract == '':
                abstract = '-No abstract-'

        else:
            abstract = '-No abstract-'

        if 'articleTitle' in singleJson:
            title    = singleJson['articleTitle']
            if title == '':
                title = '-No title-'
        else:
            title = '-No title-'

        pmid     = singleJson['pmid']

        return (abstract, title, pmid)

    def save(self):

        with open(self.outputPath, 'w') as fw:
            import sys
            for a in self.articles:
                # parse from json
                ab, ti, pmid = self.parse(a)

                # write to file (3 lines per json)
                line1 = "{0}|t|{1}\n".format(pmid, ti)
                try:
                    line2 = "{0}|a|{1}\n".format(pmid, ab.encode('utf-8'))
                except UnboundLocalError as err:
                    print ab
                    print pmid
                    print ("UnboundLocal error: {0}".format(err))
                    raise
                except UnicodeDecodeError as uniErr:
                    print ab
                    print pmid
                    print ("UnicodeDecode error: {0}".format(uniErr))
                    raise
                except:
                    print pmid
                    print ("Unexpected error:", sys.exc_info()[0])
                    raise


                fw.write(line1)
                fw.write(line2)
                fw.write('\n')
        

def geneExtract(line):
    factors = line.split('\t')
    wordType = factors[4]
    if wordType != 'Gene':
        return 'NO-PMID', 'NO-WORD'
    pmid = factors[0]
    wordName = factors[3]
    return pmid, wordName
    #return "{pmid},{word_name}".format(pmid=pmid, word_name=wordName)

def chemExtract(line):
    factors = line.split('\t')
    wordType = factors[4]
    if wordType != 'Chemical':
        return 'NO-PMID', 'NO-WORD'
    pmid = factors[0]
    wordName = factors[3]
    mesh = factors[5].rstrip()
    return pmid, mesh
    #return "{pmid},{mesh_id},{word_name}".format(pmid=pmid, mesh_id=mesh, word_name=wordName)

def disExtract(line):
    factors = line.split('\t')
    wordType = factors[4]
    if wordType != 'Disease':
        return 'NO-PMID', 'NO-WORD'
    pmid = factors[0]
    wordName = factors[3]
    mesh = factors[5].rstrip()
    return pmid, mesh
    #return "{pmid},{mesh_id},{word_name}".format(pmid=pmid, mesh_id=mesh, word_name=wordName)

class WordSaver:

    """
    """
    def __init__(self, inputPath, outputPath, extractFunc):
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.extractFunc = extractFunc
        self.pmid = 'NO-PMID'
        self.wordSet = set()
        pass

    def parse(self, line):

        if re.match(r"\d+\t", line):
            pmid, word = self.extractFunc(line)
            if pmid == 'NO-PMID':
                status = 'PASS'
            else:
                self.pmid = pmid
                self.wordSet.add(word)
                status = 'LOADING'

        elif re.match(r"^$", line):
            status = 'END'
        else:
            status = 'PASS'

        return status

    def save(self):

        with open(self.inputPath) as fi, open(self.outputPath, 'w') as fw:
            for line in fi:
                status = self.parse(line)

                if status == 'LOADING':
                    """ Add word to set """
                    pass
                elif status == 'END' and self.pmid != 'NO-PMID':
                    for word in self.wordSet:
                        outLine = "{pmid},{word}".format(
                            pmid=self.pmid, word=word)
                        fw.write(outLine)
                        fw.write('\n')
                    self.wordSet.clear()
                else:
                    """ Nothing meaningful """
                    pass
