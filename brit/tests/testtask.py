'''
Created on 29.12.2017

@author: hesse


Note: I use testfixture here. T0 install, do
python -m pip install --trusted-host pypi.python.org testfixtures
'''

import unittest
from testfixtures import LogCapture
import logging
import os
import zipfile

from brit.task import Task
from brit.configuration import Configuration
from brit.definition import Definition
from brit.retain_strategy import RetainStrategy
from brit.tests.environment import Environment
from fileinput import filename

if os.name == 'nt':  
    import msvcrt


class TestTask(unittest.TestCase):


    def testCreate(self):
        newTask = Task('myName', ['config1', 'config2'], 'strategy', 'C:/Backup', True)
        self.assert_(newTask <> None, 'No task create')
        self.assert_(newTask.name == 'myName', 'Name not OK')
        self.assert_(newTask.definitionNames[0] == 'config1', 'Config 1 not OK')
        self.assert_(newTask.definitionNames[1] == 'config2', 'Config 2 not OK')
        self.assert_(newTask.strategyName == 'strategy', 'Strategy not OK')
        self.assert_(newTask.targetFolder == 'C:/Backup', 'targetFolder not OK')
        self.assert_(newTask.isActive, 'isActive not OK')
        
        
    def testCreateWithoutStrategy(self):
        newTask = Task('myName', ['config1', 'config2'])
        self.assert_(newTask <> None, 'No task create')
        self.assert_(newTask.name == 'myName', 'Name not OK')
        self.assert_(newTask.definitionNames[0] == 'config1', 'Config 1 not OK')
        self.assert_(newTask.definitionNames[1] == 'config2', 'Config 2 not OK')
        self.assert_(newTask.strategyName == '', 'Strategy not OK')
        self.assert_(newTask.targetFolder == '', 'targetFolder not OK')
        self.assert_(not newTask.isActive, 'isActive not OK')
        
        
    def testCopy(self):
        oldTask = Task('myName', ['config1', 'config2'], 'strategy', 'C:/Backup', True)
        newTask = oldTask.copy()
        
        self.assert_(newTask <> None, 'No task create')
        self.assert_(newTask.name == 'myName', 'Name not OK')
        self.assert_(newTask.definitionNames[0] == 'config1', 'Config 1 not OK')
        self.assert_(newTask.definitionNames[1] == 'config2', 'Config 2 not OK')
        self.assert_(newTask.strategyName == 'strategy', 'Strategy not OK')
        self.assert_(newTask.targetFolder == 'C:/Backup', 'targetFolder not OK')
        self.assert_(newTask.isActive, 'isActive not OK')
        
        
    def testUpdateFrom(self):
        oldTask = Task('myName', ['config1', 'config2'], 'strategy', 'C:/Backup', True)
        newTask = Task('myNameX', ['config1'], 'strategyX', 'C:/BackupX')
        
        newTask.updateFrom(oldTask)
        self.assert_(newTask <> None, 'No task create')
        self.assert_(newTask.name == 'myName', 'Name not OK')
        self.assert_(newTask.definitionNames[0] == 'config1', 'Config 1 not OK')
        self.assert_(newTask.definitionNames[1] == 'config2', 'Config 2 not OK')
        self.assert_(newTask.strategyName == 'strategy', 'Strategy not OK')
        self.assert_(newTask.targetFolder == 'C:/Backup', 'targetFolder not OK')
        self.assert_(newTask.isActive, 'isActive not OK')
        
        
    
    def testFromJson(self):
        newTask = Task.fromJson({
            "class_name": "Task",
            "name": "myName",  
            "strategyName": "strategy",
            "definitionNames": ["config1", "config2"],
            "targetFolder": "C:/Backup", 
            "isActive": True
            })
        
        self.assert_(newTask <> None, 'No task created')
        self.assert_(newTask.name == 'myName', 'Name not OK')
        self.assert_(newTask.definitionNames[0] == 'config1', 'Config 1 not OK')
        self.assert_(newTask.definitionNames[1] == 'config2', 'Config 2 not OK')
        self.assert_(newTask.strategyName == 'strategy', 'Strategy not OK')
        self.assert_(newTask.targetFolder == 'C:/Backup', 'targetFolder not OK')
        self.assert_(newTask.isActive, 'isActive not OK')
        
        
    def testToJson(self):
        newTask = Task('myName', ['config1', 'config2'], 'strategy', isActive=True)
        
        json = newTask.toJson()
        
        self.assert_(json <> None, 'No json created')
        self.assert_(json['class_name'] == 'Task',   'class_name not OK')
        self.assert_(json['name']       == 'myName', 'name not OK')
        self.assert_(newTask.definitionNames[0] == 'config1', 'Config 1 not OK')
        self.assert_(newTask.definitionNames[1] == 'config2', 'Config 2 not OK')
        self.assert_(not ('configuration' in json), 'Configuration not removes from json')
        self.assert_(json['strategyName'] == 'strategy', 'Strategy not OK')
        self.assert_(json['isActive'], 'isActive not OK')
        
        
    def testDefinitions(self):
        # Let's prepare a configuration
        newConfig = Configuration()
        newConfig.definitions.append(Definition('name1', 'dir', 'C:/temp1', './C/temp1'))
        newConfig.definitions.append(Definition('name2', 'dir', 'C:/temp2', './C/temp2'))
        newConfig.definitions.append(Definition('name3', 'dir', 'C:/temp3', './C/temp3'))
        
        # And now the task
        newTask = Task('myName', ['name1', 'name3', 'badConf'])
        newConfig.tasks.append(newTask)
        newTask.configuration = newConfig
        
        # Now the actual test
        defs = newTask.defintions()
        self.assert_(defs <> None, 'No defs returned')
        self.assert_(len(defs) == 2, 'Nb of found defs not OK')
        self.assert_(defs[0].name == 'name1', 'Name of first def not OK')
        self.assert_(defs[1].name == 'name3', 'Name of second def not OK')
        
        
    def testStrategy(self):
        # Let's prepare a configuration
        newConfig = Configuration()
        newConfig.retainStrategies.append(RetainStrategy('myStrategy')) 
        
        newTask = Task('myName', [], 'myStrategy')
        newConfig.tasks.append(newTask)
        newTask.configuration = newConfig
        
        strat = newTask.strategy()
        self.assert_(strat <> None, 'No Strategy returned')
        self.assert_(strat.name == 'myStrategy', 'Wrong Strategy returned')  
        
    
    def test_getTargetFolder(self):
        newTask = Task('myName', [], 'myStrategy')
        self.assert_(newTask._getTargetFolder() == 'c:/temp/Backup', 'fall back folder not OK')
        
        newConfig = Configuration()
        newConfig.backupDirectory = 'c:/temp/Backup2'
        newConfig.addTask(newTask)
        self.assert_(newTask._getTargetFolder() == 'c:/temp/Backup2', 'folder from configuration not taken')
        
        newConfig.backupDirectory = 'c:/temp/Backup3'
        self.assert_(newTask._getTargetFolder() == 'c:/temp/Backup3', 'folder from task not taken')
        
        
    def test_doArchiveFile(self):
        filename = Environment.setupExamplesDir()
        
        zipTargetFile = 'dir/example'
        config = Configuration()
        config.backupDirectory = Environment.targetFolder()
        definition = Definition('name1', 'file', filename, zipTargetFile)
        config.definitions.append(definition)
        
        task = Task('myName', ['name1'])
        config.addTask(task)
        
        task._prepareTargetFolder()
        targetfile  = task._getTargetFilename()
        archiveFile = task._prepareArchive(targetfile)
        
        # Now the actual test
        task._doArchiveFile(archiveFile, filename, zipTargetFile)
        archiveFile.close()
        
        self.assert_(self.fileIsZipped(zipTargetFile, targetfile), 'File not placed in zip file')
        
        Environment.cleanupTestFolder()


    def test_doArchiveFileFail(self):
        filename = Environment.setupExamplesDir()
        zipTargetFile = 'dir/example'
        config = Configuration()
        config.backupDirectory = Environment.targetFolder()
        definition = Definition('name1', 'file', filename, zipTargetFile)
        config.definitions.append(definition)
        
        task = Task('myName', ['name1'])
        config.addTask(task)
        
        task._prepareTargetFolder()
        targetfile  = task._getTargetFilename()
        archiveFile = task._prepareArchive(targetfile)
        
        # Now the actual test
        # I open and lock the example file to provoke an I/O error
        file_ = open(filename, 'a')
        if os.name == 'nt':
            msvcrt.locking(file_.fileno(), msvcrt.LK_LOCK, 0x7fffffff)
        
        with LogCapture(level=logging.WARNING) as l:    
            task._doArchiveFile(archiveFile, filename, zipTargetFile)
            l.check(('root', 
                     'WARNING', 
                     'File could not be read: C:\\ProgramData\\brit_test\\examples\\example.txt Reason: I/O error(13): Permission denied'))
                  
        archiveFile.close()
        
        # Unlock and close the file
        if os.name == 'nt':
            msvcrt.locking(file_.fileno(), msvcrt.LK_UNLCK, 0x7fffffff)
        file_.close()
        
        self.assert_(not self.fileIsZipped(zipTargetFile, targetfile), 'File placed in zip file even though it was locked')
        
        Environment.cleanupTestFolder()

        
    def fileIsZipped(self, file, archivename):
        '''I check, whether the file "file" is in the zip file'''
        if not zipfile.is_zipfile(archivename):
            return false
            
        archiveFile = zipfile.ZipFile(archivename, mode='r', allowZip64 = True)
        
        result = False
        for fileInfo in archiveFile.infolist():
            if fileInfo.filename == file:
                result = True
                break
        
        archiveFile.close()
        return result
        
        
    def testRun(self):
        Environment.cleanupTestFolder()
        Environment.setupExamplesDir() 
        
        newConfig = Configuration()
        newConfig.definitions.append(Definition('Name1', 'dir', Environment.examplesFolder(), './C/temp1'))

        newTask = Task('myName', ['Name1'], targetFolder=Environment.targetFolder())
        newConfig.addTask(newTask)
        
        filename = newTask.run()
        
        self.assert_(os.path.exists(Environment.targetFolder()), 'Target folder not created')
        self.assert_(filename <> None and filename <> '', 'No file name returned on run') 
        
        Environment.cleanupTestFolder()            
        
      
    def test_prepareTargetFolder(self):
        Environment.cleanupTestFolder()
        targetFolder = os.path.join(Environment.targetFolder(), 'sub')
        newTask      = Task('myName', ['Name1'], targetFolder=targetFolder)
        newTask._prepareTargetFolder()
        
        self.assert_(os.path.exists(targetFolder), 'Targtefolder not created')
        
        Environment.cleanupTestFolder()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()