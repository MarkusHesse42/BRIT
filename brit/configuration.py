'''
Created on 28.12.2017

@author: hesse
'''

import json
import os

from datetime import timedelta
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder

from definition import Definition
from task import Task
from retain_strategy import RetainStrategy



class Encoder(JSONEncoder):
    def default(self, o):
        return o.toJson()

def decoder(jsonobj):
    if 'class_name' in jsonobj and jsonobj['class_name'] in CONFIG_CLASSES:
        return CONFIG_CLASSES[jsonobj['class_name']].fromJson(jsonobj)
    else:
        return jsonobj
    

class Configuration(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.backupDirectory  = ''
        self.tasks            = []
        self.definitions      = []
        self.retainStrategies = []
        
        
    @classmethod
    def fromJson(cls, jsonobj):
        new = cls()
        new.definitions      = jsonobj['definitions']
        new.retainStrategies = jsonobj['retainStrategies']
        
        if 'backupDirectory' in jsonobj:
            new.backupDirectory = jsonobj['backupDirectory']
        
        for task in jsonobj['tasks']:
            new.addTask(task)
        
        return new   
         
    
    def toJson(self):
        values = self.__dict__
        values['class_name'] = 'Configuration'
        
        return values
        
        
    def writeTo(self, fileName):
        with open(fileName, "w") as f:
            f.write(json.dumps(self, cls = Encoder, indent=4))
    
    
    @classmethod
    def readFrom(cls, fileName):
        if os.path.exists(fileName):
            with open(fileName) as f:
                lines = f.readlines()
            jsonstring = "\n".join(lines)
        else:
            return
            
        if jsonstring:
            return JSONDecoder(object_hook = decoder).decode(jsonstring)
        
    
    def addTask(self, task):
        self.tasks.append(task)
        task.configuration = self
        
    
    def addDefaultRetainStrategies(self):
        self.retainStrategies.append(RetainStrategy('Daily',   timedelta(days=1),    "day"  ))
        self.retainStrategies.append(RetainStrategy('Weekly',  timedelta(weeks = 1), "week" ))
        self.retainStrategies.append(RetainStrategy('Monthly', timedelta(days=31),   "month"))
        self.retainStrategies.append(RetainStrategy('Yearly',  timedelta(days=365),  "year" ))
        
        
CONFIG_CLASSES = {'Configuration':  Configuration,
                  'Task':           Task, 
                  'Definition':     Definition,
                  'RetainStrategy': RetainStrategy}