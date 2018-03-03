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
    
    
    @classmethod
    def extendExamplesDir(cls):
        someFiles = []
          
        folder = cls.examplesFolder()
          
        subFolder = os.path.join(cls.examplesFolder(), 'subfolder')
        if not os.path.exists(subFolder):
            os.makedirs(subFolder)
              
        someFiles.append(cls.makeFile(os.path.join(subFolder, 'test1.txt')))
        someFiles.append(cls.makeFile(os.path.join(subFolder, 'test2.txt')))
        someFiles.append(cls.makeFile(os.path.join(subFolder, 'test1.pdf')))
                       
        subFolder = os.path.join(cls.examplesFolder(), 'newfolder')
        if not os.path.exists(subFolder):
            os.makedirs(subFolder)        
              
        someFiles.append(cls.makeFile(os.path.join(subFolder, 'newtest1.txt')))
        someFiles.append(cls.makeFile(os.path.join(subFolder, 'newtest1.xml')))
        someFiles.append(cls.makeFile(os.path.join(subFolder, 'newtest1.pdf')))        
                       
        return someFiles
     
    
    @classmethod
    def makeFile(cls, filename):
        with open(filename, 'w') as f:
            f.write(filename + ': Simple test file for BRIT')
            
        return filename
                 
     
    
    