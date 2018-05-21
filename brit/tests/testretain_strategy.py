'''
Created on 29.12.2017

@author: hesse
'''
import unittest
import os
import win32file

from datetime import timedelta, datetime
from brit.retain_strategy import RetainStrategy
from brit.tests.environment import Environment
from calendar import week


class TestStrorageStrategy(unittest.TestCase):


    def testCreate(self):
        newSS = RetainStrategy('myName')
        self.assert_(newSS <> None, 'No strategy create')
        self.assert_(newSS.name == 'myName', 'Name not OK') 
        self.assert_(newSS.retainDuration == timedelta(microseconds=0), "Default retain duration not OK")  
        
        newSS = RetainStrategy('myName', timedelta(days=7))
        self.assert_(newSS.retainDuration == timedelta(days=7), "Given retain duration not taken")
        
        newSS = RetainStrategy('myName', timedelta(days=7), "week")
        self.assert_(newSS.retainInterval == "week", "Given retain interval not taken")
        
        
    def testFromJson(self):
        newSS = RetainStrategy.fromJson({
            "name": "myName",  
            "class_name": "RetainStrategy"
            })
        
        self.assert_(newSS <> None, 'No task created')
        self.assert_(newSS.name == 'myName', 'Name not OK')
        self.assert_(newSS.retainDuration == timedelta(seconds=0), "Default retain duration not taken")
        self.assert_(newSS.retainInterval == "year", "Default retain interval not taken")
        
        newSS = RetainStrategy.fromJson({
            "name": "myName",  
            "class_name": "RetainStrategy", 
            "retainInterval": "week",
            "retainDuration": timedelta(days=7).total_seconds()
            })
        
        self.assert_(newSS <> None, 'No task created')
        self.assert_(newSS.name == 'myName', 'Name not OK')
        self.assert_(newSS.retainDuration == timedelta(days=7), "Given retain duration not taken")
        self.assert_(newSS.retainInterval == "week", "Given retain interval not taken")
        
    def testToJson(self):
        newSS = RetainStrategy('myName')
        
        json = newSS.toJson()
        
        self.assert_(json <> None, 'No json created')
        self.assert_(json['class_name'] == 'RetainStrategy',  'class_name not OK')
        self.assert_(json['name']       == 'myName',            'name not OK')  
        
        newSS = RetainStrategy('myName', timedelta(days=7), "week")
        
        json = newSS.toJson()
        
        self.assert_(json <> None, 'No json created')
        self.assert_(json['class_name']     == 'RetainStrategy', 'class_name not OK')
        self.assert_(json['name']           == 'myName',         'name not OK')  
        self.assert_(json['retainInterval'] == 'week',           'Given retain interval not taken')  
        self.assert_(json['retainDuration'] == timedelta(days=7).total_seconds(), 'Given retain duration not taken')   
        
        
    def testapplyOnFiles(self):
        Environment.cleanupTestFolder()
        
        targetFolder = Environment.targetFolder()
            
        filename1 = os.path.join(targetFolder,'myName_1.zip')
        filename2 = os.path.join(targetFolder,'myName_2.zip')
        filename3 = os.path.join(targetFolder,'myName_3.zip')
        filename4 = os.path.join(targetFolder,'myName_4.zip')
        
        files = [filename1, filename2, filename3, filename4]
    
        time_now = datetime.now()

        # Let's do a test with days
        self.createFiles(files)
        self.setFileTime(filename1, time_now - timedelta(minutes = 1))
        self.setFileTime(filename2, time_now - timedelta(days = 1))
        self.setFileTime(filename3, time_now - timedelta(days = 1, minutes = 5))
        self.setFileTime(filename4, time_now - timedelta(days = 3))
        
        RS = RetainStrategy('aStrat', timedelta(days=1), "day")
        RS.applyOnFiles(files)
        
        self.assert_(os.path.isfile(filename1), "File 1 should not be deleted")
        self.assert_(os.path.isfile(filename2), "File 2 should not be deleted")
        self.assert_(not os.path.isfile(filename3), "File 3 should be deleted")
        self.assert_(os.path.isfile(filename4), "File 4 should not be deleted")
  
        Environment.cleanupTestFolder()

        # Let's do a test with weeks
        self.createFiles(files)
        self.setFileTime(filename1, time_now - timedelta(minutes = 1))
        self.setFileTime(filename2, time_now - timedelta(weeks = 1))
        self.setFileTime(filename3, time_now - timedelta(weeks = 1, minutes = 5))
        self.setFileTime(filename4, time_now - timedelta(weeks = 3))
        
        RS = RetainStrategy('aStrat', timedelta(weeks = 1), "week")
        RS.applyOnFiles(files)
        
        self.assert_(os.path.isfile(filename1), "File 1 should not be deleted")
        self.assert_(os.path.isfile(filename2), "File 2 should not be deleted")
        self.assert_(not os.path.isfile(filename3), "File 3 should be deleted")
        self.assert_(os.path.isfile(filename4), "File 4 should not be deleted")
  
        Environment.cleanupTestFolder()
        
        # Let's do a test with months
        self.createFiles(files)
        self.setFileTime(filename1, time_now - timedelta(minutes = 1))
        self.setFileTime(filename2, time_now - timedelta(days = 31))
        self.setFileTime(filename3, time_now - timedelta(days = 31, minutes = 5))
        self.setFileTime(filename4, time_now - timedelta(days = 31 * 3))
        
        RS = RetainStrategy('aStrat', timedelta(days = 31), "month")
        RS.applyOnFiles(files)
        
        self.assert_(os.path.isfile(filename1), "File 1 should not be deleted")
        self.assert_(os.path.isfile(filename2), "File 2 should not be deleted")
        self.assert_(not os.path.isfile(filename3), "File 3 should be deleted")
        self.assert_(os.path.isfile(filename4), "File 4 should not be deleted")
  
        Environment.cleanupTestFolder()       
        
        # Finally let's do a test with years
        self.createFiles(files)
        self.setFileTime(filename1, time_now - timedelta(minutes = 1))
        self.setFileTime(filename2, time_now - timedelta(days = 365))
        self.setFileTime(filename3, time_now - timedelta(days = 365, minutes = 5))
        self.setFileTime(filename4, time_now - timedelta(days = 365 * 3))
        
        RS = RetainStrategy('aStrat', timedelta(days = 365), "year")
        RS.applyOnFiles(files)
        
        self.assert_(os.path.isfile(filename1), "File 1 should not be deleted")
        self.assert_(os.path.isfile(filename2), "File 2 should not be deleted")
        self.assert_(not os.path.isfile(filename3), "File 3 should be deleted")
        self.assert_(os.path.isfile(filename4), "File 4 should not be deleted")
  
        Environment.cleanupTestFolder()  
        

    def setFileTime(self, filename, time):
        '''I set the values for creation time, modify time and last access time of the file the given time'''
        f = win32file.CreateFile(filename,
                                 win32file.GENERIC_READ|win32file.GENERIC_WRITE,
                                 0, None, win32file.OPEN_EXISTING, 0, 0)
        win32file.SetFileTime(f, time, time, time)
        
        
    def createFiles(self, files):
        # Make sure, target folder exists
        if not os.path.exists(Environment.targetFolder()):
            os.makedirs(Environment.targetFolder())
            
        for file in files:
            with open(file, 'w') as f:
                f.write('Simple test file for BRIT')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()