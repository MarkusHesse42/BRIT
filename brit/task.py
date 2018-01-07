'''
Created on 28.12.2017

@author: hesse
'''

import os
import zipfile
import logging
from logging_decorator import log
from datetime import datetime

from filemapping import FileMapping

class Task(object):
    '''
    classdocs
    '''


    def __init__(self, name, definitionNames, strategyName = '', targetFolder = '', isActive = False):
        '''
        Constructor
        '''
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
            
            
    @log('Task (%s)', 'name')
    def run(self):        
        self._prepareTargetFolder()
        filename = self._getTargetFilename()
        
        mapping     = FileMapping()
        archiveFile = self._prepareArchive(filename)
        
        for defintion in self.defintions():
            for fileInfo in defintion.fileInfos():
                self._doArchiveFile(archiveFile, fileInfo['source'], fileInfo['target'])
                mapping.addItem(fileInfo['source'], fileInfo['target'])
        
        self._archiveMapping(archiveFile, mapping)        
                
        archiveFile.close()
        
        return filename
            
            
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
        
        archiveFile.write(source, target,
                          compress_type = zipfile.ZIP_DEFLATED)
        
        
    def _archiveMapping(self, archiveFile, mapping):
        archiveFile.writestr(os.path.join('.meta', 'mapping.json'),
                            mapping.toString(),
                            compress_type = zipfile.ZIP_DEFLATED)
        

    
    