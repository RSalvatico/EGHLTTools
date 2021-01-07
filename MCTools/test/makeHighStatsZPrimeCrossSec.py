#!/usr/bin/env bash

def genZPrime(args,jobNr):
    
    nrJobs = (args.endMass-args.startMass)/args.massStep
    
    minMass=args.massStep*jobNr+args.startMass;
    maxMass=minMass+args.massStep;
    

    outputFilename=args.resultsDir.rstrip("/")+"/"+args.model+"_13TeV_M-"+str(args.mass)+"_"+str(minMass)+"to"+str(maxMass)+"_Inter"+args.inter+".root"
    cmsRunArgs=["cmsRun",args.configFile,"zPrimeModel="+args.model,"maxEvents="+str(args.nrEvents),
                "mass="+str(args.mass),"minMass="+str(minMass),"maxMass="+str(maxMass),
                "interferenceMode="+args.inter,
                "outFile="+outputFilename]
    ##runStr=""
   # print cmsRunArgs
    import subprocess
    output= subprocess.Popen(cmsRunArgs,stdout=subprocess.PIPE).communicate()[0].splitlines()
    

import threading
class JobThread (threading.Thread):
    def __init__(self, args,threadId):
        threading.Thread.__init__(self)
        self.args=args
        self.threadId=threadId
    def run(self):
        nrJobs = int((args.endMass-args.startMass)/args.massStep)
        for jobNr in range(0,nrJobs):
            if (jobNr+self.threadId)%self.args.nrThreads==0:
                genZPrime(self.args,jobNr)

import os
import argparse
parser = argparse.ArgumentParser(description='generates Z model cross-sections using pythia')

parser.add_argument('configFile',help='starting directory')
parser.add_argument('--startMass',default=200,type=int,help='start mass')
parser.add_argument('--endMass',default=5000,type=int,help='end mass')
parser.add_argument('--massStep',default=100,type=int,help='mass step')
parser.add_argument('--mass',default=3000,type=int,help='mass')
parser.add_argument('--model',required=True,help='Z\' model')
parser.add_argument('--inter',required=True,help='interference')
parser.add_argument('--nrEvents',default=50000,help='nrEvents to gen for each point')
parser.add_argument('--nrThreads',default=1,type=int,help='number of threads to run')
parser.add_argument('--resultsDir',default="./",help='results directory')
args = parser.parse_args()

if not os.path.exists(args.resultsDir):
    os.makedirs(args.resultsDir)
        
threads=[]
for threadId in range(0,args.nrThreads):
    threads.append(JobThread(args,threadId))
    
for thread in threads:
    thread.start()   




