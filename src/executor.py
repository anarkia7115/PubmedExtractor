#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import config
import subprocess
import string
sleepTime = "2"

def runCmd(execCmd, jobName, runtimeDataDir):
    # redirect stdout, stderr
    p = subprocess.Popen(execCmd, 
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

    (sout, serr) = p.communicate()

    if p.returncode != 0:
        print "[{JOB_NAME}:STDOUT] ".format(JOB_NAME=jobName.upper())
        print sout
        print "[{JOB_NAME}:STDERR] ".format(JOB_NAME=jobName.upper())
        print serr

        print "{Job_name} Failed!".format(Job_name=jobName.capitalize())

    else:
        import datetime
        today = str(datetime.date.today())
        fo = open("{run_dir}/{job_name}.stdout".format(
            run_dir=runtimeDataDir, 
            job_name=jobName), 'w')
        fe = open("{run_dir}/{job_name}.stderr".format(
            run_dir=runtimeDataDir, 
            job_name=jobName), 'w')
        fo.write(sout)
        fe.write(serr)
        fo.close()
        fe.close()

        print "{Job_name} Extractor Finished Successfully!".format(
            Job_name=jobName.capitalize())

class DisExecutor:
    def __init__(self, inputPath, outputPath):
        execPath = config.exec_cmd['dis']
        self.execCmd = string.split(execPath.format(in_path = inputPath, 
                                                 out_path = outputPath))

    def printCmd(self):
        print self.execCmd

    def run(self, runtimeDataDir):
        #self.execCmd = ["sleep", sleepTime]
        print "running dis..."
        os.chdir(config.exec_dir['dis'])

        runCmd(self.execCmd, 'dis', runtimeDataDir)


class ChemExecutor:
    def __init__(self, inputPath, outputPath):
        execPath = config.exec_cmd['chem']
        self.execCmd = string.split(execPath.format(in_path = inputPath, 
                                                 out_path = outputPath))

    def printCmd(self):
        print self.execCmd

    def run(self, runtimeDataDir):
        #self.execCmd = ["sleep", sleepTime]
        print "running chem..."
        os.chdir(config.exec_dir['chem'])

        runCmd(self.execCmd, 'chem', runtimeDataDir)


class GeneExecutor:
    def __init__(self, inputPath, outputPath):
        execPath = config.exec_cmd['gene']
        self.execCmd = string.split(execPath.format(
            in_path=inputPath, 
            out_path=outputPath))

    def printCmd(self):
        print self.execCmd

    def run(self, runtimeDataDir):
        #self.execCmd = ["sleep", sleepTime]
        print "running gene..."
        os.chdir(config.exec_dir['gene'])

        runCmd(self.execCmd, 'gene', runtimeDataDir)
