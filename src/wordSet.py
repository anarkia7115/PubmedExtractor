#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

def loadGeneSymbolList(symbolTxtPath):
    with open(symbolTxtPath) as infile:
        wordSet = set(line.strip() for line in infile)

    return wordSet

def loadGeneDict(geneidSymbolTsvPath):
    wordDict = dict()
    with open(geneidSymbolTsvPath) as infile:
        for line in infile:
            fields = line.strip().split()
            geneId = fields[0]
            symbol = fields[1]
            wordDict[geneId] = symbol

    return wordDict

def main():

    symbolTxtPath = "../DICTIONARY/gene_id_symbol.tsv"
    wordSet = loadGeneDict(symbolTxtPath)

    for i in range(0, 10):
        key = wordSet.keys()[i]
        val = wordSet.values()[i]
        print "{}: {}".format(key, val)


if __name__ == "__main__":
    main()
