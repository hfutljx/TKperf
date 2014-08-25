'''
Created on Aug 6, 2014

@author: gschoenb
'''

from abc import ABCMeta, abstractmethod
import logging
import subprocess

class Device(object):
    '''
    Representing the tested device.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, devtype, devname):
        '''
        Constructor
        '''
        ## The type of the device
        self.__devtype = devtype
        ## The path name of the device
        self.__devname = devname
        try:
            ## The size of the device in bytes
            self.__devsizeb = self.calcDevSizeB()
            ## The size of the device in kilo bytes
            self.__devsizekb = self.calcDevSizeKB()
        except RuntimeError:
            logging.error("error getting size of " + self.__devname)

    def getDevSizeKB(self): return self.__devsizekb
    def getDevSizeB(self): return self.__devsizeb

    def calcDevSizeKB(self):
        '''
        Get the device size in KByte.
        The function calls 'blockdev' to determine device sector size
        and sector count.
        @return Size on success
        @exception RuntimeError if blockdev fails
        '''
        out = subprocess.Popen(['blockdev','--getss',self.__devname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout,stderr) = out.communicate()
        if stderr != '':
            logging.error("blockdev --getss encountered an error: " + stderr)
            raise RuntimeError, "blockdev error"
        else:
            sectorSize = int(stdout)
            out = subprocess.Popen(['blockdev','--getsz',self.__devname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (stdout,stderr) = out.communicate()
            if stderr != '':
                logging.error("blockdev --getsz encountered an error: " + stderr)
                raise RuntimeError, "blockdev error"
            else:
                sectorCount = long(stdout)
                if ((sectorCount * sectorSize) % 1024) != 0:
                        logging.error("blockdev sector count cannot be divided by 1024")
                        raise RuntimeError, "blockdev error"
                devSzKB = (sectorCount * sectorSize) / 1024
                logging.info("#Device" + self.__devname + " sector count: " + str(sectorCount))
                logging.info("#Device" + self.__devname + " sector size: " + str(sectorSize))
                logging.info("#Device" + self.__devname + " size in KB: " + str(devSzKB))
                return devSzKB

    def calcDevSizeB(self):
        '''
        Get the device size in Byte.
        The function calls 'blockdev' to determine device sector size
        and sector count.
        @return Size on success
        @exception RuntimeError if blockdev fails
        '''
        out = subprocess.Popen(['blockdev','--getsize64',self.__devname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout,stderr) = out.communicate()
        if stderr != '':
            logging.error("blockdev --getss encountered an error: " + stderr)
            raise RuntimeError, "blockdev error"
        else:
            byteSize = long(stdout)
            if byteSize == 0:
                logging.error("blockdev --getsize64 returned zero.")
                raise RuntimeError, "blockdev error"
            return byteSize

    @abstractmethod
    def secureErase(self):
        ''' Erase a device. '''
        
class SSD(Device):
    '''
    Representing a SSD.
    '''
    def secureErase(self):
        return True