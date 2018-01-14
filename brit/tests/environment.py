'''
Created on 30.12.2017

@author: hesse
'''

import os
import shutil

class Environment(object):
    '''
    Class to provide some common environment and helper methods for tests of BRIT
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    @classmethod
    def baseTestFolder(cls):
        return os.path.join(os.getenv('PROGRAMDATA'), 'brit_test')
    
    @classmethod
    def cleanupTestFolder(cls):
        if os.path.exists(cls.baseTestFolder()):
            shutil.rmtree(cls.baseTestFolder())
        
    @classmethod
    def targetFolder(cls):
        return os.path.join(cls.baseTestFolder(), 'target')
    
    @classmethod
    def examplesFolder(cls):
        return os.path.join(cls.baseTestFolder(), 'examples') 
    
    
    @classmethod
    def setupExamplesDir(cls):
        if not os.path.exists(cls.examplesFolder()):
            os.makedirs(cls.examplesFolder())
            
        filename = os.path.join(cls.examplesFolder(),'example.txt')
            
        with open(filename, 'w') as f:
            f.write('Simple test file for BRIT')
            
        return filename
    
     
    
    