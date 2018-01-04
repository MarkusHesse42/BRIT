'''
Created on 31.12.2017

@author: hesse
'''

#import sys
import os
from PyQt4 import QtCore, QtGui, uic

#from brit.task import Task

pluginPath = os.path.dirname(os.path.dirname(__file__))

Ui_Dialog, QtBaseClass = uic.loadUiType(os.path.join(pluginPath, 'ui', 'taskDialog.ui'))


class TaskDialog(Ui_Dialog, QtBaseClass):
    '''
    classdocs
    '''


    def __init__(self, parent, task):
        '''
        Constructor
        '''
        super(TaskDialog, self).__init__(parent,
                               QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)        
        self.setupUi(self)
        
        #if task:
        self.task = task
        #else:
        #    self.task = self.newTask()
            
        self._taskChanged()
        
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        
        self.editName.editingFinished.connect(self._taskNameChanged)
        
        self.pbAdd.clicked.connect(self.addSelectedDefintion)
        self.pbRemove.clicked.connect(self.removeSelectedDefintion)
        
    
    def _taskChanged(self):
        self._fillPossibleDefinitions()
        self._fillSelectedDefinitions()
        self.editName.setText(self.task.name)
        
    def _taskNameChanged(self):
        self.task.name = unicode(self.editName.text())
        
    def configuration(self):
        return self.parent().configuration
    
    def _fillPossibleDefinitions(self):
        self.tvPossibleDefinitions.clear()
        
        for definition in self.configuration().definitions:
            if not definition.name in self.task.definitionNames:
                self.tvPossibleDefinitions.addTopLevelItem(DefinitionsTreeItem(self.tvPossibleDefinitions, definition))
                
    def _fillSelectedDefinitions(self):
        self.tvSelectedDefinitions.clear()
        
        for definition in self.configuration().definitions:
            if definition.name in self.task.definitionNames:
                self.tvSelectedDefinitions.addTopLevelItem(DefinitionsTreeItem(self.tvSelectedDefinitions, definition))


    def addSelectedDefintion(self):
        if self.tvPossibleDefinitions.selectedItems():
            for item in self.tvPossibleDefinitions.selectedItems():
                self.task.definitionNames.append(item.definition.name)
                
        self._taskChanged()
        
    def removeSelectedDefintion(self):
        if self.tvSelectedDefinitions.selectedItems():
            for item in self.tvSelectedDefinitions.selectedItems():
                if item.definition.name in self.task.definitionNames:
                    self.task.definitionNames.remove(item.definition.name)
                
        self._taskChanged()
        
        
#############################################################################################################
#
# Definitions tree elements
#

class DefinitionsTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, owner, definition):
        QtGui.QTreeWidgetItem.__init__(self)
        self.definition = definition
        self.setText(0, definition.name)        
        
        
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     window = TaskDialog(app)
#     window.show()
#     sys.exit(app.exec_())

