'''
Created on 07.01.2018

@author: hesse
'''

import logging
from datetime import datetime

def log(message, attrib=None, param=-1):
    '''Decorator to log an action including duration log
    
    If attrib is given, I retrieve the that attribute from the first argument to f (normally self).
    If param (an integer) is given, I retrieve that argument from the args list.
    Both values are added to the message via % operator (i.e. add %s statements to message as needed). 
    '''
    def wrap(f):
        def wrapped_f(*args):
            if attrib is not None:
                value = getattr(args[0], attrib)
                
                if param > -1:
                    actual_message = message % (value, args[param])
                else:
                    actual_message = message % (value)  
            else:
                if param > -1:
                    actual_message = message % (args[param])
                else:
                    actual_message = message
                
                
                
            logging.info('Starting: %s', actual_message)
            starttime = datetime.now()
            f(*args)
            duration = datetime.now() - starttime
            logging.info('Done: %s  Duration: %s', actual_message, duration)
        return wrapped_f
    return wrap
