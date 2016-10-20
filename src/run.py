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
    articles = query.ArticlesMongo(pubmed)
    articleJsons = articles.testFifty()

    # save data in file
    #articleOut = "/home/shawn/git/PubmedExtractor/data/article/articleOut"
    articleOut = config.file_path['article']
    articleDir = config.dir_path['article']
    import shutil
    if os.path.isdir(articleDir):
        shutil.rmtree(articleDir)

    os.mkdir(articleDir)
    import render
    aSaver = render.AbstractSaver(articleJsons, articleOut)
    aSaver.save()

    # execute word extractor
    inputFilePath   = config.file_path['article']
    inputDirPath    = config.dir_path['article']
    disOutputPath   = config.file_path['dis']
    chemOutputPath  = config.dir_path['chem_rst']
    geneOutputPath  = config.dir_path['gene_rst']

    if os.path.isdir(chemOutputPath):
        shutil.rmtree(chemOutputPath)
    if os.path.isdir(geneOutputPath):
        shutil.rmtree(geneOutputPath)

    os.mkdir(chemOutputPath)
    os.mkdir(geneOutputPath)

    import executor
    de = executor.DisExecutor( inputFilePath, disOutputPath)
    ce = executor.ChemExecutor(inputDirPath, chemOutputPath)
    ge = executor.GeneExecutor(inputDirPath, geneOutputPath)

    # run
    de.run()
    ce.run()
    #ge.printCmd()
    ge.run()

    # save word in file
    geneOutFile = config.file_path['gene']
    geneWordOut = config.file_path['gene_word']
    chemOutFile = config.file_path['chem']
    chemWordOut = config.file_path['chem_word']
    disOutFile =  config.file_path['dis']
    disWordOut =  config.file_path['dis_word']

    # run data render
    import render
    disWs =  render.WordSaver(disOutFile,  disWordOut,  render.disExtract)
    chemWs = render.WordSaver(chemOutFile, chemWordOut, render.chemExtract)
    geneWs = render.WordSaver(geneOutFile, geneWordOut, render.geneExtract)

    disWs.save()
    chemWs.save()
    geneWs.save()

    return

def test_DisExecutor():
    # strings
    articleOut = config.file_path['article']
    inputPath = articleOut
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
    #test_DisExecutor()
    #test_ChemExecutor()
    #test_GeneExecutor()
    #test_WordSaver_dis()
    main()
