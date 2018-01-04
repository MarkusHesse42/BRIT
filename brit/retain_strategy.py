'''
Created on 28.12.2017

@author: hesse
'''

class RetainStrategy(object):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        
    
    @classmethod
    def fromJson(cls, jsonobj):
        return cls(jsonobj['name'])
           
    
    def toJson(self):
        values = self.__dict__
        values['class_name'] = 'RetainStrategy'
        
        return values