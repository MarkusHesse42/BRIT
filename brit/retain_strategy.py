'''
Created on 28.12.2017

@author: hesse
'''

import os
from datetime import timedelta, datetime
from PyInstaller.loader.pyimod01_os_path import caseOk

class RetainStrategy(object):
    '''
    Class to manage the retain strategy of a backup task.
    If a strategy is attached to a backup task, all backup files not matching the strategy will be deleted.
    '''
    
    # List of possible retain intervals    
    RETAIN_INTERVALS = set(['year', 'month', 'week', 'day'])
    DEFAULT_INTERVAL = "year"
    DEFAULT_DURATION = timedelta(microseconds=0)


    def __init__(self, name="", retainDuration=timedelta(microseconds=0), retainInterval="year"):
        '''
        Constructor
        '''
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
            duration = cls.DEFAULT_DURATION
            
        if 'retainInterval' in jsonobj:
            interval = jsonobj['retainInterval']
        else:
            interval = cls.DEFAULT_INTERVAL
            
        return cls(jsonobj['name'], duration, interval)
           
    
    def toJson(self):
        values = self.__dict__.copy()
        values.pop('retainDuration', None)
        values['retainDuration'] = self.retainDuration.total_seconds()
        values['class_name']     = 'RetainStrategy'
        
        return values
    
    def apply(self, Task):
        self.applyOnFiles(Task.storedFiles())

    
    def applyOnFiles(self, files):
        files2check = []
        retainAllTime = datetime.now() - self.retainDuration
        
        # Retrieve all files that are older than retainAllTime 
        for file in files:
            if datetime.fromtimestamp(os.path.getctime(file)) < retainAllTime:
                files2check.append(file)
                
        # Retrieve the latest file in each interval. That one I want to kkep.
        file2keep = {}
        for file in files2check:
            ctime = datetime.fromtimestamp(os.path.getctime(file))
            nb = self.intervalNumber(ctime)
            
            if nb in file2keep:
                if ctime > file2keep[nb]["time"]:
                    file2keep[nb] = {"filename": file, "time": ctime}
            else:
                file2keep[nb] = {"filename": file, "time": ctime}
        
        # Now I remove all files to keep from thefiles2check   
        for nb, info in file2keep.iteritems():
            files2check.remove(info["filename"])
            
        # Eventually I delete the remaining files2check
        for file in files2check:
            os.remove(file)
            
    def intervalNumber(self, time):
        switcher = {
            "day":   self._intervalNumberDay,
            "week":  self._intervalNumberWeek,
            "month": self._intervalNumberMonth,
            "year":  self._intervalNumberYear
            }
        
        return switcher.get(self.retainInterval)(time)
        
    def _intervalNumberDay(self, time):
        return (time.year * 365) + time.timetuple().tm_yday
    
    def _intervalNumberWeek(self, time):
        return (time.year * 60) + time.isocalendar()[1]
            
    def _intervalNumberMonth(self, time):
        return (time.year * 12) + time.month
    
    def _intervalNumberYear(self, time):
        return time.year       
        
        