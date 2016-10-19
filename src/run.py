#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import logging
import config
#from line_profiler import profile
logging.basicConfig(level=logging.DEBUG)

#@profile
def main():

    # connect db
    import connector
    pubmed = connector.Mongo()
    pubmed.setCollection('pubmed')

    # query articles
    import query
    articles = query.Articles(pubmed)
    articleJsons = articles.testFifty()

    # save data in file
    #artileOut = "/home/shawn/git/PubmedExtractor/data/article/articleOut"
    artileOut = file_path['article']
    import render
    aSaver = render.AbstractSaver(articleJsons, artileOut)
    aSaver.save()

    # execute word extractor
    # save word in file

    return

def test_DisExecutor():
    # strings
    artileOut = config.file_path['article']
    inputPath = artileOut
    outputPath = config.file_path['dis']

    # executor init
    import executor
    de = executor.DisExecutor(inputPath, outputPath)
    de.printCmd()

    print "de started! "
    # run
    de.run()
    print "de finished! "

def test_ChemExecutor():
    # strings
    inputPath = config.dir_path['article']
    # mkdir outputPath
    outputPath = config.dir_path['chem_rst']
    os.mkdir(outputPath)

    # executor init
    import executor
    ce = executor.ChemExecutor(inputPath, outputPath)
    ce.printCmd()

    print "ce started! "
    # run
    ce.run()
    print "ce finished! "

def test_GeneExecutor():
    # strings
    inputPath = config.dir_path['article']
    # mkdir outputPath
    outputPath = config.dir_path['gene_rst']
    os.mkdir(outputPath)

    # executor init
    import executor
    ge = executor.GeneExecutor(inputPath, outputPath)
    ge.printCmd()

    print "ge started! "
    # run
    ge.run()
    print "ge finished! "

def test_WordSaver_gene():
    geneOutFile = config.file_path['gene']
    geneWordOut = config.file_path['gene_word']
    import render
    geneWs = render.WordSaver(geneOutFile, geneWordOut, render.geneExtract)
    geneWs.save()

def test_WordSaver_chem():
    #chemOutFile = "/home/shawn/git/PubmedExtractor/data/chemOut/articleOut.tmChem"
    chemOutFile = config.file_path['chem']
    chemWordOut = config.file_path['chem_word']
    import render
    chemWs = render.WordSaver(chemOutFile, chemWordOut, render.chemExtract)
    chemWs.save()

def test_WordSaver_dis():
    #disOutFile = "/home/shawn/git/PubmedExtractor/data/disOut"
    disOutFile = config.file_path['dis']
    disWordOut = config.file_path['dis_word']
    import render
    disWs = render.WordSaver(disOutFile, disWordOut, render.disExtract)
    disWs.save()

if __name__ == "__main__":
    test_DisExecutor()
    #test_ChemExecutor()
    #test_GeneExecutor()
    test_WordSaver_dis()
    #main()
