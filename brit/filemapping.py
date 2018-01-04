'''
Created on 27.12.2017

@author: hesse
'''

import json
import os
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder


class FileMapping(object):
    '''
    Class to hold the mapping from source files and position in the zip file.
    
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.itemMappings = {}
        
    
    def addItem(self, sourceFile, targetPlace):
        self.itemMappings[sourceFile] = targetPlace
        
    
    def saveTo(self, filename):
        with open(filename, "w") as f:
            f.write(json.dumps(self.itemMappings, indent=4))
            
    
    @classmethod
    def readFrom(cls, filename):
        if os.path.exists(filename):
            with open(filename) as f:
                lines = f.readlines()
            jsonstring = "\n".join(lines)
        else:
            return
            
        if jsonstring:
            newMapping = cls()
            newMapping.itemMappings = JSONDecoder().decode(jsonstring)
            return newMapping
    
    
    def toString(self):
        return json.dumps(self.itemMappings, indent=4)
    
    
    