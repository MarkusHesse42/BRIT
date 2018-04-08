'''
Created on 29.12.2017

@author: hesse
'''
import unittest

from datetime import timedelta
from brit.retain_strategy import RetainStrategy


class TestStrorageStrategy(unittest.TestCase):


    def testCreate(self):
        newSS = RetainStrategy('myName')
        self.assert_(newSS <> None, 'No task create')
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()