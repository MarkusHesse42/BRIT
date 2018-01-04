'''
Created on 29.12.2017

@author: hesse
'''
import unittest

from brit.retain_strategy import RetainStrategy


class TestStrorageStrategy(unittest.TestCase):


    def testCreate(self):
        newSS = RetainStrategy('myName')
        self.assert_(newSS <> None, 'No task create')
        self.assert_(newSS.name == 'myName', 'Name not OK')   
        
        
    def testFromJson(self):
        newSS = RetainStrategy.fromJson({
            "name": "myName",  
            "class_name": "RetainStrategy", 
            })
        
        self.assert_(newSS <> None, 'No task created')
        self.assert_(newSS.name == 'myName', 'Name not OK')
        
        
    def testToJson(self):
        newSS = RetainStrategy('myName')
        
        json = newSS.toJson()
        
        self.assert_(json <> None, 'No json created')
        self.assert_(json['class_name'] == 'RetainStrategy',  'class_name not OK')
        self.assert_(json['name']       == 'myName',            'name not OK')             


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()