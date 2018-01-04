'''
Created on 27.12.2017

@author: hesse
'''

import os

class Definition(object):
    '''
    Backup definition, i.e a mapping from file or directory to a backup place
    '''

    # List of possible backup types    
    BACKUP_TYPES= set(['dir', 'file'])

    def __init__(self, name, backupType, fromPlace, toPlace):
        '''
        Constructor
        '''
        assert backupType in self.BACKUP_TYPES
        
        self.name       = name
        self.backupType = backupType 
        self.fromPlace  = fromPlace
        self.toPlace    = toPlace
        
        
    def copy(self):
        return type(self)(self.name, self.backupType, self.fromPlace, self.toPlace)
    
    
    def updateFrom(self, otherDefintion):
        self.name       = otherDefintion.name
        self.backupType = otherDefintion.backupType 
        self.fromPlace  = otherDefintion.fromPlace
        self.toPlace    = otherDefintion.toPlace        
        
            
    @classmethod
    def fromJson(cls, jsonobj):
        return cls(jsonobj['name'], jsonobj['backupType'], jsonobj['fromPlace'], jsonobj['toPlace'])
           
    
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
                for aFile in files:
                    infos.append({'source': os.path.join(folder, aFile), 
                                  'target': os.path.join(self.toPlace, os.path.relpath(os.path.join(folder, aFile), os.path.dirname(self.fromPlace)))})
            
        return infos 
        
        
    
        
        