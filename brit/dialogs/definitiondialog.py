'''
Created on 01.01.2018

@author: hesse
'''

import os
from PyQt4 import QtCore, QtGui, uic

pluginPath = os.path.dirname(os.path.dirname(__file__))

Ui_Dialog, QtBaseClass = uic.loadUiType(os.path.join(pluginPath, 'ui', 'definitionDialog.ui'))

class DefinitionDialog(Ui_Dialog, QtBaseClass):
    '''
    classdocs
    '''


    def __init__(self, parent, definition):
        '''
        Constructor
        '''
        super(DefinitionDialog, self).__init__(parent,
                               QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)        
        self.setupUi(self)
        
        self.cbbType.addItem('Directory', 'dir' )
        self.cbbType.addItem('File',      'file')
        
        self.cbbType.currentIndexChanged.connect(self._backupTypeChanged)
        
        self.editName.editingFinished.connect(self._nameChanged)
        self.editSource.editingFinished.connect(self._fromPlaceChanged)
        self.pbSelectSoruce.pressed.connect(self._selectSourceFolder)
        self.pbSelectSoruce.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton))
        self.editTarget.editingFinished.connect(self._toPlaceChanged)
        
        self.definition = definition
        self._definitionChanged()
        
        
    def _definitionChanged(self):
        self.editName.setText(self.definition.name) 
        self.cbbType.setCurrentIndex(self.cbbType.findData(self.definition.backupType))
        self.editSource.setText(self.definition.fromPlace)
        self.editTarget.setText(self.definition.toPlace)
        
    def _backupTypeChanged(self):
        self.definition.backupType = self.ccbType.itemData(self.cbbType.currentIndex())
    
    def _nameChanged(self):
        self.definition.name = unicode(self.editName.text())
        
        if not self.definition.toPlace:
            self.definition.toPlace = self.definition.name
            self.editTarget.setText(self.definition.toPlace)
    
    def _fromPlaceChanged(self):
        self.definition.fromPlace = unicode(self.editSource.text())
    
    def _toPlaceChanged(self):
        self.definition.toPlace = unicode(self.editTarget.text())
    
    def _selectSourceFolder(self):
        if self.definition.fromPlace <> '':
            if self.definition.backupType == 'dir':
                StartDir = self.definition.fromPlace
            else:
                StartDir = os.path.dirname(self.definition.fromPlace)
        else:
            StartDir = ''  
            
        if self.definition.backupType == 'dir':
            newFromPlace = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                                                                      caption   = 'Select folder to backup',
                                                                      directory = StartDir))
        else:
            newFromPlace = unicode(QtGui.QFileDialog.getOpenFileName(self, 
                                                                 caption   = 'Select file to backup',
                                                                 directory = StartDir))
            
        self.definition.fromPlace = newFromPlace
        self.editSource.setText(newFromPlace)
                                                                  
    