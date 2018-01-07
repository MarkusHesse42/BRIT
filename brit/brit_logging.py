'''
Created on 07.01.2018

@author: hesse
'''

import logging
import os

# Log to the file %HOME%/.brit.log
logging.basicConfig(filename=os.path.join(os.path.expanduser("~"), '.brit.log'),
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s: %(message)s')