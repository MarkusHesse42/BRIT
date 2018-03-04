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
        
        self.editIncludeDirs.editingFinished.connect(self._includeDirsChanged)
        self.editExcludeDirs.editingFinished.connect(self._excludeDirsChanged)
        self.editIncludeFiles.editingFinished.connect(self._includeFilesChanged)
        self.editExcludeFiles.editingFinished.connect(self._excludeFilesChanged)
        
        self.definition = definition
        self._definitionChanged()
        
        
    def _definitionChanged(self):
        self.editName.setText(self.definition.name) 
        self.cbbType.setCurrentIndex(self.cbbType.findData(self.definition.backupType))
        self.editSource.setText(self.definition.fromPlace)
        self.editTarget.setText(self.definition.toPlace)
        
        self.editIncludeDirs.setText(",".join(self.definition.includeDirPattern))
        self.editExcludeDirs.setText(",".join(self.definition.excludeDirPattern))
        self.editIncludeFiles.setText(",".join(self.definition.includeFilePattern))
        self.editExcludeFiles.setText(",".join(self.definition.excludeFilePattern))
        
        
    def _backupTypeChanged(self):
        self.definition.backupType = unicode(self.cbbType.itemData(self.cbbType.currentIndex()).toString())
    
    def _nameChanged(self):
        self.definition.name = unicode(self.editName.text())
        
        if not self.definition.toPlace:
            self.definition.toPlace = self.definition.name
            self.editTarget.setText(self.definition.toPlace)
    
    def _fromPlaceChanged(self):
        self.definition.fromPlace = unicode(self.editSource.text())
    
    def _toPlaceChanged(self):
        self.definition.toPlace = unicode(self.editTarget.text())
        
    def _includeDirsChanged(self):
        if self.editIncludeDirs.text():
            self.definition.includeDirPattern = unicode(self.editIncludeDirs.text()).split(",")
        else:
            self.definition.includeDirPattern = []
            
    
    def _excludeDirsChanged(self):
        if self.editExcludeDirs.text():
            self.definition.excludeDirPattern = unicode(self.editExcludeDirs.text()).split(",")
        else:
            self.definition.excludeDirPattern = []
            
    
    def _includeFilesChanged(self):
        if self.editIncludeFiles.text():
            self.definition.includeFilePattern = unicode(self.editIncludeFiles.text()).split(",")
        else:
            self.definition.includeFilePattern = []
            
    
    def _excludeFilesChanged(self):
        if self.editExcludeFiles.text():
            self.definition.excludeFilePattern = unicode(self.editExcludeFiles.text()).split(",")
        else:
            self.definition.excludeFilePattern = [] 
            
    
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
                                                                  
    