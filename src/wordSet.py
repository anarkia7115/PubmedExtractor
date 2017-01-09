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

    symbolTxtPath = "../DICTIONARY/symbol_list.txt"
    wordSet = loadGeneSymbolList(symbolTxtPath)

    aWord = "NAT1"
    if aWord in wordSet:
        print "found word: {}".format(aWord)
    else:
        print "word not found"

if __name__ == "__main__":
    main()
