#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import logging
import config
import config
import io
#from line_profiler import profile
#logging.basicConfig(level=logging.DEBUG)

def mysql_based_main(job_id=0):

  # connect db
  import connector
  #pubmed = connector.Mongo()
  #pubmed.setCollection('pubmed')

  pubmed = connector.Mysql()

  # query articles
  import query
  #articles = query.ArticlesMongo(pubmed)
  articles = query.ArticlesMysql(pubmed)

  uniq_pmids_table   = "pubminer.uniq_pmids"
  exclude_pmid_table = uniq_pmids_table
  limit_lines = 300
  articleJsons = articles.findExcludeTable(exclude_pmid_table,
                       limit_lines)

  print "current working pmid size: {0}".format(limit_lines)
  # save data in file

  # make data dir
  #articleOutput = "/home/shawn/git/PubmedExtractor/data/article/articleOut"
  import datetime
  today = str(datetime.date.today())

  todayDataDirPath = config.runtime_data_dir.format(
                date_today=today,
                job_id=job_id)

  articleOutputPath = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  articleDirPath = config.dir_path['article'].format(
                data_dir=todayDataDirPath)

  inputFilePath   = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  inputDirPath  = config.dir_path['article'].format(
                data_dir=todayDataDirPath)
  disOutputPath   = config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  chemOutputPath  = config.dir_path['chem_rst'].format(
                data_dir=todayDataDirPath)
  geneOutputPath  = config.dir_path['gene_rst'].format(
                data_dir=todayDataDirPath)

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
  geneOutFile = config.file_path['gene'].format(
                data_dir=todayDataDirPath)
  geneWordOut = config.file_path['gene_word'].format(
                data_dir=todayDataDirPath)
  chemOutFile = config.file_path['chem'].format(
                data_dir=todayDataDirPath)
  chemWordOut = config.file_path['chem_word'].format(
                data_dir=todayDataDirPath)
  disOutFile =  config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  disWordOut =  config.file_path['dis_word'].format(
                data_dir=todayDataDirPath)

  # run data render
  import render
  rp = render.ResultParser()

  dis_result_set  = rp.getlines(disOutFile)
  chem_result_set = rp.getlines(chemOutFile)
  gene_result_set = rp.getlines(geneOutFile)

  tm = query.TermMysql(pubmed)
  dis_out_table  = "pubminer.pubmed_extracted_dis"
  chem_out_table = "pubminer.pubmed_extracted_chem"
  gene_out_table = "pubminer.pubmed_extracted_gene"

  tm.insert_terms(dis_result_set, dis_out_table)
  tm.insert_terms(chem_result_set, chem_out_table)
  tm.insert_terms(gene_result_set, gene_out_table)
  tm.insert_pmids( articleJsons, uniq_pmids_table)

  tm.commit()

  return str(dict(geneFilePath=geneWordOut, chemicalFilePath=chemWordOut, diseaseFilePath=disWordOut))

def streaming_based_main(input_stream=None, job_id=0):

  if input_stream is None:
    raise ValueError("No input stream")
  else:
    # TODO: check pmid format
    print "current working articles size: {0}".format(len(input_stream))

  # save data in file

  # make data dir
  #articleOutput = "/home/shawn/git/PubmedExtractor/data/article/articleOut"
  import datetime
  today = str(datetime.date.today())

  todayDataDirPath = config.runtime_data_dir.format(
                date_today=today,
                job_id=job_id)

  articleOutputPath = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  articleDirPath = config.dir_path['article'].format(
                data_dir=todayDataDirPath)

  inputFilePath   = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  inputDirPath  = config.dir_path['article'].format(
                data_dir=todayDataDirPath)
  disOutputPath   = config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  chemOutputPath  = config.dir_path['chem_rst'].format(
                data_dir=todayDataDirPath)
  geneOutputPath  = config.dir_path['gene_rst'].format(
                data_dir=todayDataDirPath)

  import shutil
  if os.path.isdir(todayDataDirPath):
    shutil.rmtree(todayDataDirPath)

  os.mkdir(todayDataDirPath)
  os.mkdir(articleDirPath)
  os.mkdir(chemOutputPath)
  os.mkdir(geneOutputPath)

  import query
  af = query.ArticlesFile(input_stream)
  article_dict = af.get_dict()

  import render
  aSaver = render.AbstractSaver(article_dict, articleOutputPath)
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
  geneOutFile = config.file_path['gene'].format(
                data_dir=todayDataDirPath)
  geneWordOut = config.file_path['gene_word'].format(
                data_dir=todayDataDirPath)
  chemOutFile = config.file_path['chem'].format(
                data_dir=todayDataDirPath)
  chemWordOut = config.file_path['chem_word'].format(
                data_dir=todayDataDirPath)
  disOutFile =  config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  disWordOut =  config.file_path['dis_word'].format(
                data_dir=todayDataDirPath)

  # run data render
  import render
  disWs =  render.WordSaver(disOutFile,  disWordOut,  "dis")
  chemWs = render.WordSaver(chemOutFile, chemWordOut, "chem")
  geneWs = render.WordSaver(geneOutFile, geneWordOut, "gene")

  disWs.save()
  chemWs.save()
  geneWs.save()

  return str(dict(geneFilePath=geneWordOut, chemicalFilePath=chemWordOut, diseaseFilePath=disWordOut))


#@profile
def file_based_main(inputString=None, job_id=0):

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

  # save data in file

  # make data dir
  #articleOutput = "/home/shawn/git/PubmedExtractor/data/article/articleOut"
  import datetime
  today = str(datetime.date.today())

  todayDataDirPath = config.runtime_data_dir.format(
                date_today=today,
                job_id=job_id)

  articleOutputPath = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  articleDirPath = config.dir_path['article'].format(
                data_dir=todayDataDirPath)

  inputFilePath   = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  inputDirPath  = config.dir_path['article'].format(
                data_dir=todayDataDirPath)
  disOutputPath   = config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  chemOutputPath  = config.dir_path['chem_rst'].format(
                data_dir=todayDataDirPath)
  geneOutputPath  = config.dir_path['gene_rst'].format(
                data_dir=todayDataDirPath)

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
  geneOutFile = config.file_path['gene'].format(
                data_dir=todayDataDirPath)
  geneWordOut = config.file_path['gene_word'].format(
                data_dir=todayDataDirPath)
  chemOutFile = config.file_path['chem'].format(
                data_dir=todayDataDirPath)
  chemWordOut = config.file_path['chem_word'].format(
                data_dir=todayDataDirPath)
  disOutFile =  config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  disWordOut =  config.file_path['dis_word'].format(
                data_dir=todayDataDirPath)

  # run data render
  import render
  disWs =  render.WordSaver(disOutFile,  disWordOut,  "dis")
  chemWs = render.WordSaver(chemOutFile, chemWordOut, "chem")
  geneWs = render.WordSaver(geneOutFile, geneWordOut, "gene")

  disWs.save()
  chemWs.save()
  geneWs.save()

  return str(dict(geneFilePath=geneWordOut, chemicalFilePath=chemWordOut, diseaseFilePath=disWordOut))

def test_DisExecutor():
  import datetime
  today = str(datetime.date.today())

  # strings
  articleOutputPath = config.file_path['article'].format(
                data_dir=todayDataDirPath)
  inputPath = articleOutputPath
  outputPath = config.file_path['dis'].format(
                data_dir=todayDataDirPath)

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
  inputPath = config.dir_path['article'].format(
                data_dir=todayDataDirPath)
  # mkdir outputPath
  outputPath = config.dir_path['chem_rst'].format(
                data_dir=todayDataDirPath)
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
  inputPath = config.dir_path['article'].format(
                data_dir=todayDataDirPath)
  # mkdir outputPath
  outputPath = config.dir_path['gene_rst'].format(
                data_dir=todayDataDirPath)
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
  #import datetime
  #today = str(datetime.date.today())

  geneOutFile = "../geneData/geneOut/articleOut"
  #geneOutFile = config.file_path['gene'].format(
  #              data_dir=todayDataDirPath)
  #geneWordOut = config.file_path['gene_word'].format(
  #              data_dir=todayDataDirPath)
  geneWordOut = "./geneWordOut"
  import render
  geneWs = render.WordSaver(geneOutFile, geneWordOut, "gene")
  geneWs.save()

def test_WordSaver_chem():
  import datetime
  today = str(datetime.date.today())

  #chemOutFile = "/home/shawn/git/PubmedExtractor/data/chemOut/articleOut.tmChem"
  chemOutFile = config.file_path['chem'].format(
                data_dir=todayDataDirPath)
  chemWordOut = config.file_path['chem_word'].format(
                data_dir=todayDataDirPath)
  import render
  chemWs = render.WordSaver(chemOutFile, chemWordOut, render.chemExtract)
  chemWs.save()

def test_WordSaver_dis():
  import datetime
  today = str(datetime.date.today())

  #disOutFile = "/home/shawn/git/PubmedExtractor/data/disOut"
  disOutFile = config.file_path['dis'].format(
                data_dir=todayDataDirPath)
  disWordOut = config.file_path['dis_word'].format(
                data_dir=todayDataDirPath)
  import render
  disWs = render.WordSaver(disOutFile, disWordOut, render.disExtract)
  disWs.save()

def test_AbstractFile():
  with io.open("/gcbi/storage/similarPubmed/input/cbd778ac624f417494ff9f748c6db82d",
       "r", encoding="utf-8") as input_stream:
    cleaned_lines = []
    for l in input_stream:
      if len(l.split("\t")) == 3:
        cleaned_lines.append(l)

  import query
  af = query.ArticlesFile(cleaned_lines)
  article_dict = af.get_dict()

  import render
  articleOutputPath = "/home/gcbi/PubmedExtractor/result/article"
  aSaver = render.AbstractSaver(article_dict, articleOutputPath)
  aSaver.save()


if __name__ == "__main__":
  #test_DisExecutor()
  #test_ChemExecutor()
  #test_GeneExecutor()
  #test_WordSaver_gene()
  #mysql_based_main()
  test_AbstractFile()
