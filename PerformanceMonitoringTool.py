#-*- coding: utf-8 -*-
#This Python file uses the following encoding: utf-8

import os
import subprocess
import json
#import psutil
import tempfile
import xml.etree.cElementTree as ET
import time
import threading
import argparse
import psutil
import codecs
import json
import urllib2

class ProcessPerformance:
    #processname=r"Adobe Photoshop CC 2019"
    cpulist=[]
    rsslist=[]
    vmslist=[]
    savedjsonpath=r""
    hostname=r""


    def parseargs(self):
        parser = argparse.ArgumentParser(description='Process Performance Monitoring Tool')
        parser.add_argument('--processname', '-p', required=True, type=str, help='processname')
        parser.add_argument('--identifier', '-i', required=False, type=str, help='unique identifier')
        parser.add_argument('--hostname', '-r', required=False, type=str, help='hostname to send data to remote server/ REST End Point')
        self.args = parser.parse_args()
        self.processname = self.args.processname
        self.identifier = self.args.identifier
        self.hostname = self.args.hostname


    def start(self):
        print ("start")
        while 1:
            if self.isprocessrunning(self.processname):
                print ("process found.")
                print ("process ID : ",self.pid)
                print ("process name : ",self.name)
                self.t1=time.time()
                self.getstats()
                break

    def getstats(self):
        print ("getstats")
        process=psutil.Process(self.pid)
        while self.isprocessrunning(self.processname):
            try:
                #mem=float(process.memory_info().rss)/(2**20)
                self.rsslist.append(float(process.memory_info().rss)/(2**20))
                self.cpulist.append(process.cpu_percent(interval=1)/psutil.cpu_count())
                self.vmslist.append(float(process.memory_info().vms)/(2**20))
            except:
                print ("process terminated...,\n exception : ")
                #self.t2=time.time()
                #self.hddf=self.gethddsize()
                #self.printstats()
                break
        print ("process terminated")


    def isprocessrunning(self,processname):
        check=0
        try:
            for proc in psutil.process_iter():
                pinfo = proc.as_dict(attrs=['pid', 'name'])
                #print(pinfo['name'])
                if processname==pinfo['name']:
                    self.name=pinfo['name']
                    self.pid=pinfo['pid']
                    return 1
            return 0
        except :
            return 0


    def cleanup(self):
        self.rsslist=[]
        self.vmslist=[]
        self.cpulist=[]


    def printall(self):
        print(self.rsslist)
        print(self.vmslist)
        print(self.cpulist)
        pass


    def writetojson(self):
        import json
        self.data={"data":{},"meta":{}}
        self.data["data"]["rsslist"]=self.rsslist
        self.data["data"]["vmslist"]=self.vmslist
        self.data["data"]["cpulist"]=self.cpulist
        self.data["meta"]["identifier"]=self.identifier
        self.data["meta"]["processname"]=self.processname
        self.data["meta"]["timestamp"]=self.ts
        with open(os.path.join(self.savedjsonpath,'data.json'), 'w') as outfile:
            json.dump(self.data, outfile)


    def setvariables(self):
        #print(type(self.identifier))
        if self.identifier is None:
            self.identifier=r""
        else:
            pass
        self.ts=str(time.time())
        if os.name=="nt":
            self.savedjsonpath=os.path.join(tempfile.gettempdir(),"PerformanceData",self.identifier,self.ts)
            if ".exe" in self.processname:
                pass
            else:
                self.processname+=".exe"
        else:
            self.savedjsonpath=os.path.join("temp","PerformanceData",self.identifier,self.ts)
        try:
            os.makedirs(self.savedjsonpath)
        except:
            pass

    def wf(self):
        self.parseargs()
        self.setvariables()
        self.start()
        self.printall()
        self.writetojson()

    def sendpostcall(self):

        try:
            if self.hostname is None:
                self.hostname=""
            req = urllib2.Request(self.hostname)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps(self.data))
        except Exception,e:
            print(e)


if __name__=="__main__":
    y=ProcessPerformance()
    y.wf()



