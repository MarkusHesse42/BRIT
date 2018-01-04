'''
Created on 28.12.2017

@author: hesse
'''
import os.path

import unittest
from json.decoder import JSONDecoder

from brit.filemapping import FileMapping
from brit.tests.environment import Environment

class TestFileMapping(unittest.TestCase):
    
    def testCreate(self):
        newMapping = FileMapping()
        self.assert_(newMapping <> None, 'No mapping created')
        
        
    def testAddItem(self):
        newMapping = FileMapping()
        newMapping.addItem(u'c:/temp/x1.txt', u'Temp/x1.txt')
        self.assert_(newMapping.itemMappings[u'c:/temp/x1.txt'] == u'Temp/x1.txt', 'Mapping item not added')
        
        
    def testSaveToReadFrom(self):
        newMapping = FileMapping()
        newMapping.addItem(u'c:/temp/x1.txt', u'Temp/x1.txt')
        newMapping.addItem(u'c:/temp/x2.txt', u'Temp/x2.txt')
        
        Environment.cleanupTestFolder()
        Environment.setupExamplesDir()
        testFile = os.path.join(Environment.examplesFolder(), 'test_mapping.json')
        
        newMapping.saveTo(testFile)
        
        self.assert_(os.path.isfile(testFile), 'No mapping file written')
        newMapping2 = FileMapping.readFrom(testFile)
        
        self.assert_(newMapping2 <> None, 'No mapping read')
        self.assert_(len(newMapping2.itemMappings) == 2, 'Nb of items mappings not OK')
        self.assert_(newMapping2.itemMappings[u'c:/temp/x1.txt'] == u'Temp/x1.txt', 'Mapping item not added')
        
        Environment.cleanupTestFolder()
        
        
    def testToString(self):
        newMapping = FileMapping()
        newMapping.addItem(u'c:/temp/x1.txt', u'Temp/x1.txt')
        newMapping.addItem(u'c:/temp/x2.txt', u'Temp/x2.txt')
        
        str = newMapping.toString()
        self.assert_(str <> None, 'No string returned')   
        items = JSONDecoder().decode(str) 
        self.assert_(items <> None, 'String could not be decoded by JSON')
        self.assert_(len(items) == 2, 'Nb of items mappings not OK')  
        self.assert_(items[u'c:/temp/x1.txt'] == u'Temp/x1.txt', 'Mapping item not OK')   
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()