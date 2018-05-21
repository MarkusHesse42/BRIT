'''
Created on 28.12.2017

@author: hesse
'''

import os
import zipfile
import logging
from logging_decorator import log
from datetime import datetime
from PyQt4.QtCore import pyqtSignal, QObject

from filemapping import FileMapping
from glob import iglob

class Task(QObject):
    '''
    classdocs
    '''
    progressChanged = pyqtSignal(int, str)


    def __init__(self, name, definitionNames, strategyName = '', targetFolder = '', isActive = False):
        '''
        Constructor
        '''
        QObject.__init__(self)
        
        self.name            = name
        self.definitionNames = definitionNames
        self.strategyName    = strategyName
        self.targetFolder    = targetFolder
        self.configuration   = None
        self.isActive        = isActive
        
    
    def copy(self):
        ''' Create a copy of self.
        
        Note, that the relation to the configuration is NOT set up!
        '''
        return type(self)(self.name, self.definitionNames[:], self.strategyName, self.targetFolder, self.isActive)
    
    
    def updateFrom(self, otherTask):
        self.name            = otherTask.name
        self.definitionNames = otherTask.definitionNames
        self.strategyName    = otherTask.strategyName
        self.targetFolder    = otherTask.targetFolder
        self.isActive        = otherTask.isActive        
    
        
    def toJson(self):
        values = self.__dict__.copy()
        values.pop('configuration', None)
        values['class_name'] = 'Task'
        
        return values
    
    @classmethod
    def fromJson(cls, jsonobj):
        if 'isActive' in jsonobj:
            active = jsonobj['isActive']
        else:
            active = False
            
        return cls(jsonobj['name'], jsonobj['definitionNames'], jsonobj['strategyName'], jsonobj['targetFolder'], active)
    
    
    def defintions(self):
        return [aDef for aDef in self.configuration.definitions if aDef.name in self.definitionNames]
    
    
    def strategy(self):
        for aStrategy in self.configuration.retainStrategies:
            if aStrategy.name == self.strategyName:
                return aStrategy
            
    def filesSize(self):
        size = 0
        for defintion in self.defintions():
            size = size + defintion.filesSize()

        return size
            
            
    @log('Task (%s)', 'name')
    def run(self):        
        self._prepareTargetFolder()
        filename = self._getTargetFilename()
        
        mapping     = FileMapping()
        archiveFile = self._prepareArchive(filename)
        
        for defintion in self.defintions():
            for fileInfo in defintion.fileInfos():
                self.progressChanged.emit(0, "Archiving file: " + fileInfo['source'])
                self._doArchiveFile(archiveFile, fileInfo['source'], fileInfo['target'])
                mapping.addItem(fileInfo['source'], fileInfo['target'])
                self.progressChanged.emit(os.path.getsize(fileInfo['source']), "Archiving file: " + fileInfo['source'])
        
        self._archiveMapping(archiveFile, mapping)        
                
        archiveFile.close()
        
        if self.strategy():
            self.strategy().apply(self)
        
        return filename
    
    
    def storedFiles(self):
        '''I return an iterator of all files in the target directory that were created by me'''
        targetPath = self._getTargetFolder()
        for fileName in iglob(os.path.join(targetPath, self.name + '_*')):
            yield fileName 
        
            
            
    def _getTargetFolder(self):
        if self.targetFolder:
            return self.targetFolder
        elif self.configuration and self.configuration.backupDirectory:
            return self.configuration.backupDirectory
        else:
            # FIXME: In the future I want to get a default from the configuration
            return 'c:/temp/Backup'
        
    
    def _getTargetFilename(self):
        return os.path.join(self._getTargetFolder(), self.name + '_' + self._dateTimePostfix() + '.zip')
    
    def _dateTimePostfix(self):
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    

    def _prepareTargetFolder(self):
        folder = self._getTargetFolder()
        if not os.path.exists(folder):
            os.makedirs(folder)
            
            
    def _prepareArchive(self, filename):
        """I create the zip file"""
        return zipfile.ZipFile(filename, mode='w', allowZip64 = True)
    
    @log('Task (%s): File: %s', attrib='name', param=2)
    def _doArchiveFile(self, archiveFile, source, target):
        """Archive the given source file to the given target position in the archive
        
        If the file does not exists, it is skipped"""
        
        if not os.path.exists(source):
            logging.warn('No such file %s' % source)
            return         
        
        try:
            archiveFile.write(source, target,
                              compress_type = zipfile.ZIP_DEFLATED)
        except IOError as (errno, strerror):
            logging.warn('File could not be read: {0} Reason: I/O error({1}): {2}'.format(source, errno, strerror))
            
        
        
    def _archiveMapping(self, archiveFile, mapping):
        archiveFile.writestr(os.path.join('.meta', 'mapping.json'),
                            mapping.toString(),
                            compress_type = zipfile.ZIP_DEFLATED)
        

    
    