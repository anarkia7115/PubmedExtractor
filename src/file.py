#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

class AbstractSaver:

    """
        1. read json data
        2. get pmid
        3. get abstract
        4. save to file as format:

            26116688|t|Syphilis and gonorrhoea increase sharply in England.
            26116688|a|-No abstract-

    """
    def __init__(self, jsonData, outputPath):

        self.article    = jsonData
        self.outputPath = outputPath

    def parse(self, singleJson):

        abstract = singleJson['abstractText']
        title    = singleJson['articleTitle']
        pmid     = singleJson['pmid']

        if abstract == '':
            abstract = '-No abstract-'

        return (abstract, title, pmid)

class WordSaver:

    """
    """
    def __init__(self, inputPath, outputPath):
        pass
