'''
Created on 27.12.2017

@author: hesse
'''
import unittest
import os

from brit.definition import Definition
from brit.tests.environment import Environment


class TestDefinition(unittest.TestCase):


    def testCreate(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp')
        
        self.assert_(myDef <> None, 'No definition created')
        self.assert_(myDef.name       == 'myName',    'name not OK')
        self.assert_(myDef.backupType == 'dir',      'backupType not OK')
        self.assert_(myDef.fromPlace  == 'C:/temp',  'fromPlace not OK')
        self.assert_(myDef.toPlace    == './C/temp', 'toPlace not OK')
        
        
    def testCopy(self):
        oldDef = Definition('myName', 'dir', 'C:/temp', './C/temp')
        newDef = oldDef.copy()
        
        self.assert_(newDef <> None, 'No definition created')
        self.assert_(newDef.name       == 'myName',    'name not OK')
        self.assert_(newDef.backupType == 'dir',      'backupType not OK')
        self.assert_(newDef.fromPlace  == 'C:/temp',  'fromPlace not OK')
        self.assert_(newDef.toPlace    == './C/temp', 'toPlace not OK') 
        
        
    def testUpdateFrom(self):
        oldDef = Definition('myName',    'dir',  'C:/temp',    './C/temp')
        newDef = Definition('myNameNew', 'file', 'C:/tempNew', './C/tempNew')
        oldDef.updateFrom(newDef)
        
        self.assert_(oldDef.name       == 'myNameNew',   'name not OK')
        self.assert_(oldDef.backupType == 'file',        'backupType not OK')
        self.assert_(oldDef.fromPlace  == 'C:/tempNew',  'fromPlace not OK')
        self.assert_(oldDef.toPlace    == './C/tempNew', 'toPlace not OK')     
        
        
    def testFromJson(self):
        myDef = Definition.fromJson({
            "name": "myName",
            "backupType": "dir", 
            "fromPlace": "C:/temp1", 
            "class_name": "Definition", 
            "toPlace": "./C/temp1"
            })
        
        self.assert_(myDef <> None, 'No definition created')
        self.assert_(myDef.name       == 'myName',    'name not OK')
        self.assert_(myDef.backupType == 'dir',       'backupType not OK')
        self.assert_(myDef.fromPlace  == 'C:/temp1',  'fromPlace not OK')
        self.assert_(myDef.toPlace    == './C/temp1', 'toPlace not OK')
        
        
    def testToJson(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp')
        
        json = myDef.toJson()
        
        self.assert_(json <> None, 'No json created')
        self.assert_(json['class_name'] == 'Definition', 'class_name not OK')
        self.assert_(json['name']       == 'myName',     'name not OK')
        self.assert_(json['backupType'] == 'dir',        'backupType not OK')
        self.assert_(json['fromPlace']  == 'C:/temp',    'fromPlace not OK')
        self.assert_(json['toPlace']    == './C/temp',   'toPlace not OK')
        
        
    def testFileInfos(self):
        Environment.cleanupTestFolder()
        Environment.setupExamplesDir()
        
        myDef = Definition('Name1', 'dir', Environment.examplesFolder(), './C/temp1')
        infos = myDef.fileInfos()
        
        self.assert_(infos <> None, 'No fileInfos created')
        self.assert_(infos[0]['source'] == os.path.join(Environment.examplesFolder(), 'example.txt'),
                     'Example source file not OK')
        self.assert_(infos[0]['target'] == os.path.join('./C/temp1', 'examples', 'example.txt'),
                     'Example source file not OK')
        
        Environment.cleanupTestFolder()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()