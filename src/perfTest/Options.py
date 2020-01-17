'''
Created on Aug 26, 2014

@author: gschoenb
'''

import logging
import json
from lxml import etree

class Options(object):
    '''
    A class holding user defined options on command line.
    '''

    def __init__(self, nj=1, iod=1, runtime=60, ioengine="libaio", xargs=None):
        '''
        Constructor
        @param nj Number of jobs
        @param iod Number for io depth
        @param xargs Further argument as list for all fio jobs in tests
        '''
        ## Number of jobs for fio.
        self.__nj = nj
        ## Number of iodepth for fio.
        self.__iod = iod
        ## Runtime of one test round for fio.
        self.__runtime = runtime
        ## IOEngine of one test round for fio.
        self.__ioengine = ioengine
        ## polled IO completions for fio.
        self.__hipri = None
        ## pre map IO buffers for fio.
        self.__sqthread_poll = None
        ## offload submission/completion to kernel thread for fio.
        self.__fixedbufs = None
        ## what CPU to run SQ thread polling on for poll.
        self.__sqthread_poll_cpu = None
        ## Further single arguments as list for fio.
        self.__xargs = xargs

    def getNj(self): return self.__nj
    def getIod(self): return self.__iod
    def getRuntime(self): return self.__runtime
    def getIOEngine(self): return self.__ioengine
    def getHipri(self): return self.__hipri
    def getSqthread_poll(self): return self.__sqthread_poll
    def getFixedbufs(self): return self.__fixedbufs
    def getSqthread_poll_cpu(self): return self.__sqthread_poll_cpu
    def getXargs(self): return self.__xargs
    def setNj(self,nj): self.__nj = nj
    def setIod(self,iod): self.__iod = iod
    def setRuntime(self,rt): self.__runtime = rt
    def setIOEngine(self,ioe): self.__ioengine = ioe
    def setHipri(self,hipri): self.__hipri = hipri
    def setSqthread_poll(self,sqthread_poll): self.__sqthread_poll = sqthread_poll
    def setFixedbufs(self,fixedbufs): self.__fixedbufs = fixedbufs
    def setSqthread_poll_cpu(self,sqthread_poll_cpu): self.__sqthread_poll_cpu = sqthread_poll_cpu
    def setXargs(self,xargs): self.__xargs = xargs
    
    def appendXml(self,r):
        '''
        Append the information about options to a XML node. 
        @param root The xml root tag to append the new elements to
        ''' 
        data = json.dumps(self.__nj)
        e = etree.SubElement(r,'numjobs')
        e.text = data
        
        data = json.dumps(self.__iod)
        e = etree.SubElement(r,'iodepth')
        e.text = data
        
        data = json.dumps(self.__runtime)
        e = etree.SubElement(r,'runtime')
        e.text = data

        data = json.dumps(self.__ioengine)
        e = etree.SubElement(r,'ioengine')
        e.text = data

        data = json.dumps(self.__hipri)
        e = etree.SubElement(r,'hipri')
        e.text = data

        data = json.dumps(self.__sqthread_poll)
        e = etree.SubElement(r,'sqthread_poll')
        e.text = data

        data = json.dumps(self.__fixedbufs)
        e = etree.SubElement(r,'fixedbufs')
        e.text = data

        data = json.dumps(self.__sqthread_poll_cpu)
        e = etree.SubElement(r,'sqthread_poll_cpu')
        e.text = data
        
        if self.__xargs != None:
            data = json.dumps(list(self.__xargs))
            e = etree.SubElement(r,'xargs')
            e.text = data

    def fromXml(self,root):
        '''
        Loads the information about options from XML.
        @param root The given element containing the information about
        the object to be initialized.
        '''
        if root.findtext('numjobs'):
            self.__nj = json.loads(root.findtext('numjobs'))
        if root.findtext('iodepth'):
            self.__iod = json.loads(root.findtext('iodepth'))
        if root.findtext('runtime'):
            self.__runtime = json.loads(root.findtext('runtime'))
        if root.findtext('ioengine'):
            self.__ioengine = json.loads(root.findtext('ioengine'))
        if root.findtext('hipri'):
            self.__hipri = json.loads(root.findtext('hipri'))
        if root.findtext('sqthread_poll'):
            self.__sqthread_poll = json.loads(root.findtext('sqthread_poll'))
        if root.findtext('fixedbufs'):
            self.__fixedbufs = json.loads(root.findtext('fixedbufs'))
        if root.findtext('sqthread_poll_cpu'):
            self.__sqthread_poll_cpu = json.loads(root.findtext('sqthread_poll_cpu'))
        if root.findtext('xargs'):
                self.__xargs = json.loads(root.findtext('xargs'))
        logging.info("# Loading options from xml")
        logging.info("# Options nj:"+str(self.__nj))
        logging.info("# Options iod: "+str(self.__iod))
        if self.__xargs != None:
            logging.info("# Options xargs:")
            logging.info(self.__xargs)