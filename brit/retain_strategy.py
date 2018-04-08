'''
Created on 28.12.2017

@author: hesse
'''

from datetime import timedelta

class RetainStrategy(object):
    '''
    Class to manage the retain strategy of a backup task.
    If a strategy is attached to a backup task, all backup files not matching the strategy will be deleted.
    '''
    
    # List of possible retain intervals    
    RETAIN_INTERVALS= set(['year', 'month', 'week', 'day'])


    def __init__(self, name="", retainDuration=timedelta(microseconds=0), retainInterval="year"):
        '''
        Constructor
        '''
        if retainDuration == None:
            retainDuration = timedelta(microseconds=0)
            
        if retainInterval == None:
            retainInterval = "year"
        
        assert retainInterval in self.RETAIN_INTERVALS
        
        self.name           = name
        # Any backup file not older than this will be retained.
        self.retainDuration = retainDuration
        
        # The last backup of each interval in the past will be retained.
        self.retainInterval = retainInterval
        
    
    @classmethod
    def fromJson(cls, jsonobj):
        if 'retainDuration' in jsonobj:
            duration = timedelta(seconds=jsonobj['retainDuration'])
        else:    
            duration = None
            
        if 'retainInterval' in jsonobj:
            interval = jsonobj['retainInterval']
        else:
            interval = None
            
        return cls(jsonobj['name'], duration, interval)
           
    
    def toJson(self):
        values = self.__dict__.copy()
        values.pop('retainDuration', None)
        values['retainDuration'] = self.retainDuration.total_seconds()
        values['class_name']     = 'RetainStrategy'
        
        return values