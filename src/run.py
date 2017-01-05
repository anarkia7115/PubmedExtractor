#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import logging
import config
#from line_profiler import profile
logging.basicConfig(level=logging.DEBUG)

#@profile
def main(inputString=None, jobId=None):

    # connect db
    import connector
    #pubmed = connector.Mongo()
    #pubmed.setCollection('pubmed')

    pubmed = connector.Mysql()

    # query articles
    import query
    #articles = query.ArticlesMongo(pubmed)
    articles = query.ArticlesMysql(pubmed)
    if inputString is None:
        articleJsons = articles.testFifty()
    else:
        import ast
        # TODO: check pmid format
        pmids = ast.literal_eval(inputString)
        print "current working pmid size: {0}".format(len(pmids))
        articleJsons = articles.findPmids(pmids)
    if jobId is None:
        jobId = 0

    # save data in file

    # make data dir
    #articleOutput = "/home/shawn/git/PubmedExtractor/data/article/articleOut"
    import datetime
    today = str(datetime.date.today())

    articleOutputPath = config.file_path['article'].format(date_today=today,
                                                           job_id=jobId)
    articleDirPath = config.dir_path['article'].format(date_today=today,
                                                       job_id=jobId)

    inputFilePath   = config.file_path['article'].format(date_today=today,
                                                         job_id=jobId)
    inputDirPath    = config.dir_path['article'].format(date_today=today,
                                                        job_id=jobId)
    disOutputPath   = config.file_path['dis'].format(date_today=today,
                                                     job_id=jobId) # file
    chemOutputPath  = config.dir_path['chem_rst'].format(date_today=today,
                                                         job_id=jobId) # dir
    geneOutputPath  = config.dir_path['gene_rst'].format(date_today=today,
                                                         job_id=jobId) # dir
    todayDataDirPath = config.runtime_data_dir.format(date_today=today,
                                                      job_id=jobId)

    import shutil
    if os.path.isdir(todayDataDirPath):
        shutil.rmtree(todayDataDirPath)

    os.mkdir(todayDataDirPath)
    os.mkdir(articleDirPath)
    os.mkdir(chemOutputPath)
    os.mkdir(geneOutputPath)

    import render
    aSaver = render.AbstractSaver(articleJsons, articleOutputPath)
    aSaver.save()

    # execute word extractor
    import executor
    de = executor.DisExecutor( inputFilePath, disOutputPath)
    ce = executor.ChemExecutor(inputDirPath, chemOutputPath)
    ge = executor.GeneExecutor(inputDirPath, geneOutputPath)

    # run
    de.run(todayDataDirPath)
    ce.run(todayDataDirPath)
    ge.run(todayDataDirPath)

    # save word in file
    geneOutFile = config.file_path['gene'].format(date_today=today)
    geneWordOut = config.file_path['gene_word'].format(date_today=today)
    chemOutFile = config.file_path['chem'].format(date_today=today)
    chemWordOut = config.file_path['chem_word'].format(date_today=today)
    disOutFile =  config.file_path['dis'].format(date_today=today)
    disWordOut =  config.file_path['dis_word'].format(date_today=today)

    # run data render
    import render
    disWs =  render.WordSaver(disOutFile,  disWordOut,  render.disExtract)
    chemWs = render.WordSaver(chemOutFile, chemWordOut, render.chemExtract)
    geneWs = render.WordSaver(geneOutFile, geneWordOut, render.geneExtract)

    disWs.save()
    chemWs.save()
    geneWs.save()

    return str(dict(geneFilePath=geneWordOut, chemicalFilePath=chemWordOut, diseaseFilePath=disWordOut))

def test_DisExecutor():
    import datetime
    today = str(datetime.date.today())

    # strings
    articleOutputPath = config.file_path['article'].format(date_today=today)
    inputPath = articleOutputPath
    outputPath = config.file_path['dis'].format(date_today=today)

    # executor init
    import executor
    de = executor.DisExecutor(inputPath, outputPath)
    de.printCmd()

    print "de started! "
    # run
    de.run()
    print "de finished! "

def test_ChemExecutor():
    import datetime
    today = str(datetime.date.today())

    # strings
    inputPath = config.dir_path['article'].format(date_today=today)
    # mkdir outputPath
    outputPath = config.dir_path['chem_rst'].format(date_today=today)
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
    import datetime
    today = str(datetime.date.today())

    # strings
    inputPath = config.dir_path['article'].format(date_today=today)
    # mkdir outputPath
    outputPath = config.dir_path['gene_rst'].format(date_today=today)
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
    import datetime
    today = str(datetime.date.today())

    geneOutFile = config.file_path['gene'].format(date_today=today)
    geneWordOut = config.file_path['gene_word'].format(date_today=today)
    import render
    geneWs = render.WordSaver(geneOutFile, geneWordOut, render.geneExtract)
    geneWs.save()

def test_WordSaver_chem():
    import datetime
    today = str(datetime.date.today())

    #chemOutFile = "/home/shawn/git/PubmedExtractor/data/chemOut/articleOut.tmChem"
    chemOutFile = config.file_path['chem'].format(date_today=today)
    chemWordOut = config.file_path['chem_word'].format(date_today=today)
    import render
    chemWs = render.WordSaver(chemOutFile, chemWordOut, render.chemExtract)
    chemWs.save()

def test_WordSaver_dis():
    import datetime
    today = str(datetime.date.today())

    #disOutFile = "/home/shawn/git/PubmedExtractor/data/disOut"
    disOutFile = config.file_path['dis'].format(date_today=today)
    disWordOut = config.file_path['dis_word'].format(date_today=today)
    import render
    disWs = render.WordSaver(disOutFile, disWordOut, render.disExtract)
    disWs.save()

if __name__ == "__main__":
    #test_DisExecutor()
    #test_ChemExecutor()
    #test_GeneExecutor()
    #test_WordSaver_dis()
    main()
