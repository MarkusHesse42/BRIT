'''
Created on 27.12.2017

@author: hesse
'''

import os
import fnmatch
from _ast import Continue

class Definition(object):
    '''
    Backup definition, i.e a mapping from file or directory to a backup place
    '''

    # List of possible backup types    
    BACKUP_TYPES= set(['dir', 'file'])

    def __init__(self, name='', backupType='dir', fromPlace='', toPlace='', includeFilePattern=[], excludeFilePattern=[], includeDirPattern=[], excludeDirPattern=[], class_name=''):
        '''
        Constructor
        class_name is actually not used. I add it to make fromJson very easy.
        '''
        assert backupType in self.BACKUP_TYPES
        
        self.name               = name
        self.backupType         = backupType 
        self.fromPlace          = fromPlace
        self.toPlace            = toPlace
        self.includeFilePattern = includeFilePattern
        self.excludeFilePattern = excludeFilePattern
        self.includeDirPattern  = includeDirPattern
        self.excludeDirPattern  = excludeDirPattern        
        
        
    def copy(self):
        return type(self)(**self.__dict__)
    
    
    def updateFrom(self, otherDefintion):
        self.name               = otherDefintion.name
        self.backupType         = otherDefintion.backupType 
        self.fromPlace          = otherDefintion.fromPlace
        self.toPlace            = otherDefintion.toPlace  
        self.includeFilePattern = otherDefintion.includeFilePattern  
        self.excludeFilePattern = otherDefintion.excludeFilePattern  
        self.includeDirPattern  = otherDefintion.includeDirPattern  
        self.excludeDirPattern  = otherDefintion.excludeDirPattern           
        
            
    @classmethod
    def fromJson(cls, jsonobj):
        return cls(**jsonobj)
           
    
    def toJson(self):
        values = self.__dict__
        values['class_name'] = 'Definition'
        
        return values
        
        
    def fileInfos(self):
        if self.backupType == 'file':
            infos = [{'source': self.fromPlace, 'target': self.toPlace}]
        elif self.backupType == 'dir':
            infos = []
            for folder, subfolders, files in os.walk(self.fromPlace):
                if self._dirIsIncluded(os.path.basename(folder)) and (not self._dirIsExcluded(os.path.basename(folder))):
                    for aFile in files:
                        if not self._fileIsIncluded(folder) or self._fileIsExcluded(folder):
                            Continue
                    
                        infos.append({'source': os.path.join(folder, aFile), 
                                      'target': os.path.join(self.toPlace, os.path.relpath(os.path.join(folder, aFile), os.path.dirname(self.fromPlace)))})
            
        return infos 
        
        
    def _dirIsIncluded(self, dirname):
        if self.includeDirPattern:
            return self._matchesOneOf(dirname, self.includeDirPattern)
        else:
            # If no pattern are given, I assume all dirs are included
            return True
    
    def _dirIsExcluded(self, dirname):
        return self._matchesOneOf(dirname, self.excludeDirPattern)
    
    def _fileIsIncluded(self, filename):
        if self.includeFilePattern:
            return self._matchesOneOf(filename, self.includeFilePattern)
        else:
            # If no pattern are given, I assume all files are included
            return True 
        
    def _fileIsExcluded(self, filename):
        return self._matchesOneOf(filename, self.excludeFilePattern)       
    
    def _matchesOneOf(self, name, patternList):
        for pattern in patternList:
            if fnmatch.fnmatch(name, pattern):
                return True
            
        return False
        
    
        
        
