'''
Created on 28.12.2017

@author: hesse
'''
import os.path
from PyQt4 import QtGui
#QtCore, QtGui, uic

from brit.dialogs.definitiondialog import DefinitionDialog
from brit.definition import Definition

import unittest

class TestDefinitionDialog(unittest.TestCase):
    
    def setUp(self):
        self.app       = QtGui.QApplication([])
        self.definition = Definition('name', 'dir', 'from', 'to')
        self.dlg       = DefinitionDialog(None, self.definition)
        
        self.dlg.show()
        
        
    def tearDown(self):
        self.dlg.close()
        unittest.TestCase.tearDown(self)
        
    
    def testCreate(self):
        self.assert_(self.dlg <> None, 'dialog not created')
        self.assert_(self.dlg.definition == self.definition, 'Definition not set')        
        self.assert_(self.dlg.editName.text() == self.definition.name, 'Name set') 
        
        
    def test_DefinitionChanged(self):
        ''' I set a new definition to the dialog and check, that all GUI elements change their value accordingly'''
        newdefinition = Definition('new_name', 'file', 'new_from', 'new_to')
        self.dlg.definition = newdefinition
        self.dlg._definitionChanged()
        
        self.assert_(self.dlg.editName.text()   == newdefinition.name,      'Name not OK') 
        self.assert_(self.dlg.editSource.text() == newdefinition.fromPlace, 'fromPlace not OK')
        self.assert_(self.dlg.editTarget.text() == newdefinition.toPlace,   'toPlace not OK')
        self.assert_(self.dlg.cbbType.itemData(self.dlg.cbbType.currentIndex()) == 'file', 'Type not OK')
        
        
    def test_BackupTypeChanged(self):
        '''I change the GUI element for backup type and check, if the definition object changes accordingly'''
        self.assert_(self.dlg.cbbType.itemData(self.dlg.cbbType.currentIndex()) == 'dir', 'Initial type not OK')
        
        # Let's change the type in the GUI
        self.dlg.cbbType.setCurrentIndex(self.dlg.cbbType.findData('file'))
        
        # And now check, that the model has changed.
        self.assert_(self.definition.backupType == 'file', 'backupType not changed')
        
        
    def test_NameChanged(self):
        self.assert_(self.dlg.editName.text()   == self.definition.name,    'Initial name not OK')
        self.assert_(self.dlg.editTarget.text() == self.definition.toPlace, 'Initial toPlace not OK')
        
        self.definition.toPlace = ''
        
        self.dlg.editName.setText('new name')
        # Note, that setText does not emit editingFinished, thus I need to call that myself.
        self.dlg._nameChanged()
        
        # Now the name and toPlace of the definition should have changed
        self.assert_(self.definition.name    == 'new name', 'Name not OK')
        self.assert_(self.definition.toPlace == 'new name', 'toPlace not OK')
        
        # Let's change the value again. Now toPlace should not change, because it has already a value.
        self.dlg.editName.setText('new name2')
        self.dlg._nameChanged()        
        
        self.assert_(self.definition.name    == 'new name2', 'Name not OK after second change')
        self.assert_(self.definition.toPlace == 'new name',  'toPlace not OK after second change')  
        
    def test_FromPlaceChanged(self):  
        self.assert_(self.dlg.editSource.text() == self.definition.fromPlace, 'Initial fromPlace not OK')
        
        self.dlg.editSource.setText('new_from_place')
        self.dlg._fromPlaceChanged()
        
        self.assert_(self.definition.fromPlace == 'new_from_place', 'fromPlace not OK')   
        
        
    def test_ToPlaceChanged(self):  
        self.assert_(self.dlg.editTarget.text() == self.definition.toPlace, 'Initial toPlace not OK')
        
        self.dlg.editTarget.setText('new_to_place')
        self.dlg._toPlaceChanged()
        
        self.assert_(self.definition.toPlace == 'new_to_place', 'toPlace not OK')  


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
