'''
Created on 28.12.2017

@author: hesse
'''
import os.path

import unittest
from brit.task import Task
from brit.configuration import Configuration
from brit.definition import Definition
from brit.retain_strategy import RetainStrategy
from brit.tests.environment import Environment

class TestConfiguration(unittest.TestCase):
    
    def testCreate(self):
        newConfig = Configuration()
        self.assert_(newConfig <> None, 'No configuration created')
        
    
    def testWriteToReadFrom(self):
        newConfig = Configuration()
        newConfig.addTask(Task('TestTest1', ['config1', 'config2']))
        newConfig.addTask(Task('TestTest2', ['config1', 'config2']))
        newConfig.definitions.append(Definition('name1', 'dir', 'C:/temp1', './C/temp1'))
        newConfig.definitions.append(Definition('name2', 'dir', 'C:/temp2', './C/temp2'))
        newConfig.definitions.append(Definition('name3', 'dir', 'C:/temp3', './C/temp3'))
        newConfig.retainStrategies.append(RetainStrategy('reatinDefault'))
        newConfig.backupDirectory = 'c:/temp/backup'
        
        Environment.cleanupTestFolder()
        Environment.setupExamplesDir()
        testFile = os.path.join(Environment.examplesFolder(), 'test_config.brit')
        
            
        newConfig.writeTo(testFile)
        self.assert_(os.path.isfile(testFile), 'No config file written')
        
        newConfig2 = Configuration.readFrom(testFile)
        
        self.assert_(newConfig2 <> None, 'No configuration has been read from Json')
        self.assert_(len(newConfig2.tasks)    == 2,           'Length of list of tasks not OK')
        self.assert_(newConfig2.tasks[0].name == 'TestTest1', 'Name of first task not OK')
        self.assert_(newConfig2.tasks[0].configuration == newConfig2, 'Configuration of task not set')
        
        self.assert_(len(newConfig2.definitions) == 3, 'Length of list of Definitions not OK')
        self.assert_(len(newConfig2.retainStrategies) == 1, 'Length of list of RetainStrategies not OK')
        
        self.assert_(newConfig2.backupDirectory == 'c:/temp/backup', 'backupDirectory not OK')
        
        Environment.cleanupTestFolder()
        
        
    def testReadFrom_WithNotExistingFile(self):
        newConfig2 = Configuration.readFrom('C:/temp/no_such_file.xyz')
        self.assert_(newConfig2 == None, 'Config should not be created, if there is no config file')
        
    def testAddTask(self):
        newConfig = Configuration()
        newTask = Task('TestTest1', ['config1', 'config2'])
        
        newConfig.addTask(newTask)
        self.assert_(newTask in newConfig.tasks, 'Task not added to list')
        self.assert_(newTask.configuration == newConfig, 'Configuration not set')
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()