'''
Created on 27.12.2017

@author: hesse
'''
import unittest
import os

from brit.definition import Definition
from brit.tests.environment import Environment
from __builtin__ import len


class TestDefinition(unittest.TestCase):


    def testCreate(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp', ['*.txt'], ['old*', 'bad*'], ['wanted_dir*'], ['bad_dir*'] )
        
        self.assert_(myDef <> None, 'No definition created')
        self.assert_(myDef.name == 'myName', 'name not OK')
        self.assert_(myDef.backupType == 'dir', 'backupType not OK')
        self.assert_(myDef.fromPlace == 'C:/temp', 'fromPlace not OK')
        self.assert_(myDef.toPlace == './C/temp', 'toPlace not OK')
        self.assert_(myDef.includeFilePattern[0] == '*.txt', 'includeFilePattern not OK')
        self.assert_(myDef.excludeFilePattern[1] == 'bad*', 'excludeFilePattern not OK')
        self.assert_(myDef.includeDirPattern[0] == 'wanted_dir*', 'includeDirPattern not OK')
        self.assert_(myDef.excludeDirPattern[0] == 'bad_dir*', 'excludeDirPattern not OK')
        
    def testCopy(self):
        oldDef = Definition('myName', 'dir', 'C:/temp', './C/temp', ['*.txt'], ['old*', 'bad*'], [], ['unwanted'])
        newDef = oldDef.copy()
        
        self.assert_(newDef <> None, 'No definition created')
        self.assert_(newDef.name       == 'myName',   'name not OK')
        self.assert_(newDef.backupType == 'dir',      'backupType not OK')
        self.assert_(newDef.fromPlace  == 'C:/temp',  'fromPlace not OK')
        self.assert_(newDef.toPlace    == './C/temp', 'toPlace not OK')
         
        self.assert_(newDef.includeFilePattern[0] == '*.txt',    'includeFilePattern not OK')
        self.assert_(newDef.excludeFilePattern[1] == 'bad*',     'excludeFilePattern not OK')
        self.assert_(newDef.includeDirPattern     == [],         'includeDirPattern not OK')
        self.assert_(newDef.excludeDirPattern[0]  == 'unwanted', 'excludeDirPattern not OK')
        
        
    def testUpdateFrom(self):
        oldDef = Definition('myName', 'dir', 'C:/temp', './C/temp', ['*.txt'], ['old1*', '1bad*'])
        newDef = Definition('myNameNew', 'file', 'C:/tempNew', './C/tempNew', ['*.tyt'], ['old2*', '2bad*'], ['wanted'], ['unwanted'])
        oldDef.updateFrom(newDef)
        
        self.assert_(oldDef.name == 'myNameNew', 'name not OK')
        self.assert_(oldDef.backupType == 'file', 'backupType not OK')
        self.assert_(oldDef.fromPlace == 'C:/tempNew', 'fromPlace not OK')
        self.assert_(oldDef.toPlace == './C/tempNew', 'toPlace not OK')   
        self.assert_(oldDef.includeFilePattern[0] == '*.tyt', 'includeFilePattern not OK')
        self.assert_(oldDef.excludeFilePattern[1] == '2bad*', 'includePattern not OK')  
        self.assert_(oldDef.includeDirPattern     == ['wanted'],   'includeDirPattern not OK')
        self.assert_(oldDef.excludeDirPattern     == ['unwanted'], 'excludeDirPattern not OK')
        
        
    def testFromJson(self):
        myDef = Definition.fromJson({
            "name": "myName",
            "backupType": "dir",
            "fromPlace": "C:/temp1",
            "class_name": "Definition",
            "toPlace": "./C/temp1",
            "includeFilePattern": ['*.txt'],
            "excludeFilePattern": ['old*', 'bad*'],
            "includeDirPattern":  ['wanted'],
            "excludeDirPattern":  ['unwanted']
            })
        
        self.assert_(myDef <> None, 'No definition created')
        self.assert_(myDef.name == 'myName', 'name not OK')
        self.assert_(myDef.backupType == 'dir', 'backupType not OK')
        self.assert_(myDef.fromPlace == 'C:/temp1', 'fromPlace not OK')
        self.assert_(myDef.toPlace == './C/temp1', 'toPlace not OK')
        self.assert_(myDef.includeFilePattern[0] == '*.txt', 'includeFilePattern not OK')
        self.assert_(myDef.excludeFilePattern[1] == 'bad*', 'excludeFilePattern not OK')
        self.assert_(myDef.includeDirPattern     == ['wanted'],   'includeDirPattern not OK')
        self.assert_(myDef.excludeDirPattern     == ['unwanted'], 'excludeDirPattern not OK')
        
        
    def testToJson(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp', ['*.txt'], ['old*', 'bad*'], ['wanted'], ['unwanted'])
        
        json = myDef.toJson()
        
        self.assert_(json <> None, 'No json created')
        self.assert_(json['class_name'] == 'Definition', 'class_name not OK')
        self.assert_(json['name'] == 'myName', 'name not OK')
        self.assert_(json['backupType'] == 'dir', 'backupType not OK')
        self.assert_(json['fromPlace'] == 'C:/temp', 'fromPlace not OK')
        self.assert_(json['toPlace'] == './C/temp', 'toPlace not OK')
        self.assert_(json['includeFilePattern'] == ['*.txt'], 'includeFilePattern not OK')
        self.assert_(json['excludeFilePattern'] == ['old*', 'bad*'], 'excludeFilePattern not OK')
        self.assert_(json['includeDirPattern']  == ['wanted'],   'includeDirPattern not OK')
        self.assert_(json['excludeDirPattern']  == ['unwanted'], 'excludeDirPattern not OK')
        
        
    def testFileInfos_forFile(self): 
        Environment.cleanupTestFolder()
        exampleFile = Environment.setupExamplesDir()
        
        myDef = Definition('Name1', 'file', exampleFile, 'Test/example.txt')
        
        infos = []
        for info in myDef.fileInfos():
            infos.append(info)   
        
        self.assert_(len(infos) == 1, 'There should be exactly one fileInfo')
        self.assert_(infos[0]['source'] == exampleFile, 'Source not OK')
        self.assert_(infos[0]['target'] == 'Test/example.txt', 'Target not OK')
        
        Environment.cleanupTestFolder()

        
    def testfileInfos(self):
        Environment.cleanupTestFolder()
        exampleFile = Environment.setupExamplesDir()
        
        myDef = Definition('Name1', 'dir', Environment.examplesFolder(), 'Test/Dir')
        
        infos = []
        for info in myDef.fileInfos():
            infos.append(info)    
            
        self.assert_(infos <> None, 'No fileInfos created')
        self.assert_(infos[0]['source'] == os.path.join(Environment.examplesFolder(), 'example.txt'),
                     'Example source file not OK')
        self.assert_(infos[0]['target'] == os.path.join('Test/Dir', 'examples', 'example.txt'),
                     'Example source file not OK')        
        
        someFiles = Environment.extendExamplesDir()
        someFiles.append(exampleFile)
        
        infos = []
        for info in myDef.fileInfos():
            infos.append(info)  

        self.assert_(len(infos) == len(someFiles), 'Not all files found')
        
        myDef.includeDirPattern = ['subfolder']
        
        infos = []
        for info in myDef.fileInfos():
            infos.append(info)  
        # Note that I get all files of the base dir, independent if that matches included dirrs!
        self.assert_(len(infos) == 4, 'Nb of files not OK for include dirs')
        
        Environment.cleanupTestFolder()
        
    def testfilesSize(self):
        Environment.cleanupTestFolder()
        exampleFile = Environment.setupExamplesDir()
        someFiles = Environment.extendExamplesDir()
        someFiles.append(exampleFile)
        
        myDef = Definition('Name1', 'dir', Environment.examplesFolder(), 'Test/Dir')
        self.assert_(myDef.filesSize() == 514, 'FilesSize not OK')
                
        Environment.cleanupTestFolder()
        
            
    def test_dirIsIncluded(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp', [], [], [], [])
        self.assert_(myDef._dirIsIncluded('anydir'), 'Dir not included on empty include list')
        
        myDef.includeDirPattern = ['asd*', 'path']
        self.assert_(myDef._dirIsIncluded('path'), 'Dir not included that is in include list')
        self.assert_(myDef._dirIsIncluded('asd_whatEverDir'), 'Dir not included that is in include list2')
        self.assert_(not myDef._dirIsIncluded('anydir'), 'Dir included when not in include list')
        
        
    def test_dirIsExcluded(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp', [], [], [], [])
        self.assert_(not myDef._dirIsExcluded('c:/temp/anydir'), 'Dir excluded on empty exclude list')
        
        myDef.excludeDirPattern = ['*/asd*', '*/path/*']
        self.assert_(myDef._dirIsExcluded('c:/temp/path/anydir'), 'Dir not excluded that is in include list')
        self.assert_(myDef._dirIsExcluded('c:/temp/asd_whatEverDir'), 'Dir not excluded that is in include list2')
        self.assert_(not myDef._dirIsExcluded('c:/temp/anydir'), 'Dir excluded when not in include list')        
        
        
    def test_fileIsIncluded(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp', [], [], [], [])
        self.assert_(myDef._fileIsIncluded('Test.txt'), 'File not included on empty include list')
        
        myDef.includeFilePattern = ['*Test*', '*all*']
        self.assert_(myDef._fileIsIncluded('Test.txt'), 'File not included on matching include list')
        self.assert_(myDef._fileIsIncluded('fileOnCall.txt'), 'File not included on matching include list, item2')
        self.assert_(not myDef._fileIsIncluded('Bad.file'), 'File included on not matching include list')
        
        
    def test_fileIsExcluded(self):
        myDef = Definition('myName', 'dir', 'C:/temp', './C/temp', [], [], [], [])
        self.assert_(not myDef._fileIsExcluded('Test.txt'), 'File excluded on empty exclude list')
        
        myDef.excludeFilePattern = ['*Test*', '*all*']
        self.assert_(myDef._fileIsExcluded('Test.txt'), 'File not excluded on matching exclude list')
        self.assert_(myDef._fileIsExcluded('fileOnCall.txt'), 'File not excluded on matching exclude list, item2')
        self.assert_(not myDef._fileIsExcluded('Bad.file'), 'File excluded on not matching exclude list')
    

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
