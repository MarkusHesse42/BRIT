'''
Created on 29.12.2017

@author: hesse
'''
import unittest

import brit.tests.testconfiguration
import brit.tests.testtask
import brit.tests.testdefinition
import brit.tests.testretain_strategy


# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(brit.tests.testconfiguration))
suite.addTests(loader.loadTestsFromModule(brit.tests.testtask))
suite.addTests(loader.loadTestsFromModule(brit.tests.testdefinition))
suite.addTests(loader.loadTestsFromModule(brit.tests.testretain_strategy))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)


