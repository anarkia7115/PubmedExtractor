#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import config
import subprocess
import string
sleepTime = "2"


class DisExecutor:
    def __init__(self, inputPath, outputPath):
        execPath = config.exec_cmd['dis']
        self.execCmd = string.split(execPath.format(in_path = inputPath, 
                                                 out_path = outputPath))

    def printCmd(self):
        print self.execCmd

    def run(self):
        #self.execCmd = ["sleep", sleepTime]
        print "running dis..."
        #print self.execCmd
        os.chdir(config.exec_dir['dis'])
        subprocess.call(self.execCmd)


class ChemExecutor:
    def __init__(self, inputPath, outputPath):
        execPath = config.exec_cmd['chem']
        self.execCmd = string.split(execPath.format(in_path = inputPath, 
                                                 out_path = outputPath))

    def printCmd(self):
        print self.execCmd

    def run(self):
        #self.execCmd = ["sleep", sleepTime]
        print "running chem..."
        os.chdir(config.exec_dir['chem'])
        subprocess.call(self.execCmd)


class GeneExecutor:
    def __init__(self, inputPath, outputPath):
        execPath = config.exec_cmd['gene']
        self.execCmd = string.split(execPath.format(in_path = inputPath, 
                                                 out_path = outputPath))

    def printCmd(self):
        print self.execCmd

    def run(self):
        #self.execCmd = ["sleep", sleepTime]
        print "running gene..."
        os.chdir(config.exec_dir['gene'])
        subprocess.call(self.execCmd)
