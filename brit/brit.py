import sys
import os
import json

from functools import partial
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication

from configuration import Configuration
from task import Task
from definition import Definition
from dialogs.taskdialog import TaskDialog
from dialogs.definitiondialog import DefinitionDialog

import brit_logging
from logging_decorator import log

# Define function to import external files when using PyInstaller.
def resource_base_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return base_path

qtCreatorFile = os.path.join(resource_base_path(), 'ui', 'britMainForm.ui') 
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BritApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.configuration  = None
        self.configFilename = self._getConfigFilenameFromBrit()
        
        if not self.configuration:
            self.configuration = Configuration()
            self.configuration.addDefaultRetainStrategies()
       
        self.editBackupFolder.editingFinished.connect(self._backupFolderChanged)
        self.pbSelectBackupFolder.pressed.connect(self.selectBackupFolder)
        self.pbSelectBackupFolder.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton))
        
        self.actionOpen.triggered.connect(self.openConfiguration)
        self.actionSave.triggered.connect(self.saveConfiguration)
        self.actionSave_As.triggered.connect(self.saveConfigurationAs)
        self.actionRun.triggered.connect(self.runActiveTasks)
        
        self.editConfigFilename.editingFinished.connect(self._configFilenameChanged)
        self.pbOpenConfigFile.pressed.connect(self.openConfiguration)
        self.pbOpenConfigFile.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton))
        
        
        self.actionRunSelectedJob.triggered.connect(self.runActiveTasks)
        self.actionRunSelectedJob.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        
        self.tvJobs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tvJobs.customContextMenuRequested.connect(self._showJobsContextMenu)
        self.tvJobs.itemDoubleClicked.connect(self.editTaskItem)
        
        
        self.tvDefinitions.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tvDefinitions.customContextMenuRequested.connect(self._showDefinitionsContextMenu)
        self.tvDefinitions.itemDoubleClicked.connect(self.editDefinitionItem)
        
        self.statusbar   = self.statusBar()
        self.progressBar = QtGui.QProgressBar()
        
        self.statusbar.addPermanentWidget(self.progressBar)

        # This is simply to show the bar
        self.progressBar.setGeometry(30, 40, 200, 25)
        self.progressBar.setValue(0)
                
        
    def _getBritConfigFilename(self):
        """Basic configuration file"""
        return os.path.join(os.path.expanduser("~"), '.brit')
    
    def _getConfigFilenameFromBrit(self):
        filename = self._getBritConfigFilename()
        
        if os.path.isfile(filename):
            with open(filename) as json_data_file:
                data = json.load(json_data_file)
                return data['configFilename']
        else:
            return ''
        
    def _setConfigFilenameToBrit(self, configFilename):
        filename = self._getBritConfigFilename()
        
        data = {'configFilename': unicode(configFilename)}
        
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        
    
    def _getBackupDirectory(self):
        if self.configuration:
            return self.configuration.backupDirectory
        else:
            return ''
    
    def _setBackupDirectory(self, folderName):
        self.configuration.backupDirectory = folderName
        self.editBackupFolder.setText(folderName)
        
    backupDirectory = property(_getBackupDirectory, _setBackupDirectory)    
        
        
    def _getConfigFilename(self):
        return self._configFilename
    
    def _setConfigFilename(self, filename):
        if os.path.isfile(filename):
            # FIXME: Error handling!
            self.configuration   = Configuration.readFrom(filename)
            
            # If the config file was empty, I should at least create an empty configuration.
            if not self.configuration:
                self.configuration = Configuration()
            
            self._configFilename = filename
            self.editConfigFilename.setText(filename)
            self._setConfigFilenameToBrit(filename)
            self.editBackupFolder.setText(self.backupDirectory)
        else:
            self._configFilename = ''
            
    
    def _getConfiguration(self):
        return self._configuration
    
    def _setConfiguration(self, configuration):
        self._configuration = configuration
        self._configurationChanged()
        
    
    configFilename  = property(_getConfigFilename,  _setConfigFilename )
    configuration   = property(_getConfiguration,   _setConfiguration  )
    
    
    def selectBackupFolder(self):
        if self.backupDirectory <> '':
            StartDir = self.backupDirectory
        else:
            StartDir = ''     
            
        self.backupDirectory = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                                                                              caption   = 'Select backup folder',
                                                                              directory = StartDir))   
        
    
    def openConfiguration(self):
        if self.configFilename <> '':
            StartDir = os.path.dirname(unicode(self.configFilename))
        else:
            StartDir = ''
            
        self.configFilename = unicode(QtGui.QFileDialog.getOpenFileName(self, 
                                                                        caption   = 'Select configuration file',
                                                                        directory = StartDir,
                                                                        filter    = "BRIT Configuration (*.brit)"))
                                                                  
    
    def saveConfiguration(self):
        if self.configuration:
            if self.configFilename:
                self.configuration.writeTo(self.configFilename)
            else:
                self.saveConfigurationAs()
        
    
    def saveConfigurationAs(self):
        if self.configFilename <> '':
            StartDir = os.path.dirname(unicode(self.configFilename))
        else:
            StartDir = ''
                    
        filename = QtGui.QFileDialog.getSaveFileName(self, 
                                                    caption   = 'Select configuration file',
                                                    directory = StartDir,
                                                    filter    = "BRIT Configuration (*.brit)") 
        
        if filename:
            self.configuration.writeTo(filename)
            self._configFilename = filename
            self.editConfigFilename.setText(filename)
        
    
    def _configFilenameChanged(self):
        if self.configFilename <> self.editConfigFilename.text():
            self.configFilename = self.editConfigFilename.text()
        
    def _backupFolderChanged(self):
        self.configuration.backupDirectory = unicode(self.editBackupFolder.text())
        
    def _configurationChanged(self):
        self._fillJobsListview()
        self._fillDefinitionsList()
        self._fillStrategieList()
        
    def _fillJobsListview(self):
        self.tvJobs.clear()
        
        if self.configuration:
            for task in self.configuration.tasks:
                self.tvJobs.addTopLevelItem(JobsTreeItem(self, task))
                
                
    def _fillDefinitionsList(self):
        self.tvDefinitions.clear()
        
        if self.configuration:
            for definition in self.configuration.definitions:
                self.tvDefinitions.addTopLevelItem(DefinitionsTreeItem(self, definition))
                
                
    def _fillStrategieList(self):
        self.tvRetainStrategies.clear()
        
        if self.configuration:
            for strategy in self.configuration.retainStrategies:
                self.tvRetainStrategies.addTopLevelItem(RetainTreeItem(self, strategy))
            
    
    @log('Run all active tasks', param=-1)    
    def runActiveTasks(self, checked):
        self.runTasks([task for task in self.configuration.tasks if task.isActive])
                    
        
    def _showJobsContextMenu(self, point):
        item = self.tvJobs.currentItem()
        
        if item:
            self.menu = item.menu()
        else:
            self.menu = QtGui.QMenu()
            newAction = QtGui.QAction("Create new job", self.menu)
            newAction.triggered.connect(self.createNewTask)
            self.menu.addAction(newAction)
            
        point = self.tvJobs.mapToGlobal(point)
        self.menu.popup(point)
            
        
    def _showDefinitionsContextMenu(self, point):
        item = self.tvDefinitions.currentItem()
        
        if item:
            self.menu = item.menu()
        else:
            self.menu = QtGui.QMenu()
        
            newAction = QtGui.QAction("Create definition", self.menu)
            newAction.triggered.connect(self.createDefinition)
            self.menu.addAction(newAction)
        
        point = self.tvDefinitions.mapToGlobal(point)
        self.menu.popup(point)
        
        return self.menu
    
    
    def createNewTask(self):
        # I open the task dialog with a new, empty task
        dlg = TaskDialog(self, Task('enter name', []))
        dlg.show()
        result = dlg.exec_()
        
        if result and dlg.task:
            self.addTask(dlg.task)
            
            
    def editTaskItem(self, taskItem, clumnNumber):
        self.editTask(taskItem.task)
    
    def editTask(self, task):
        dlg = TaskDialog(self, task.copy())
        result = dlg.exec_()
                
        if result:
            task.updateFrom(dlg.task)
            self._configurationChanged()
    
    def deleteTask(self, task):
        # FIXME: How about a question to the user?
        self.configuration.tasks.remove(task)
        self._configurationChanged()
    
    def runTask(self, task):
        self.runTasks([task])
        
    def runTasks(self, tasks):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        self.statusbar.showMessage('Starting')
        self.progressBar.setValue(0)
        
        filesSize = 0
        for task in tasks:
            filesSize = filesSize + task.filesSize()
            
        self.progressBar.setMaximum(filesSize)
            
        for task in tasks:
            task.progressChanged.connect(self.on_progress)
            task.run()
            
        self.progressBar.setValue(0);
        QApplication.restoreOverrideCursor()
        self.statusbar.showMessage('Done', 2000)
                
    
    def on_progress(self, progressAddValue, progressString):
        # If a negative value is given, I leave the progress as it is.
        # Nice feature, if I only want to change the label text.
        if not (progressAddValue < 0):
            self.progressBar.setValue(self.progressBar.value() + progressAddValue) 

        self.statusbar.showMessage(progressString)
        
    
    def addTask(self, task):
        self.configuration.tasks.append(task)
        task.configuration = self.configuration
        self._configurationChanged()
        
    
    def createDefinition(self):
        dlg = DefinitionDialog(self, Definition('enter name', 'dir', '', ''))
        dlg.show()
        result = dlg.exec_()
        
        if result and dlg.definition:
            self.configuration.definitions.append(dlg.definition)
            self._configurationChanged()
            
            
    def editDefinitionItem(self, definitionItem, clumnNumber):
        self.editDefinition(definitionItem.definition)
        
    
    def editDefinition(self, definition):
        dlg = DefinitionDialog(self, definition.copy())
        dlg.show()
        result = dlg.exec_()
                    
        if result:
            definition.updateFrom(dlg.definition)
            self._configurationChanged()    
    
    def deleteDefinition(self, definition):
        # FIXME: How about a question to the user?
        self.configuration.definitions.remove(definition)
        self._configurationChanged()
    
    
#############################################################################################################
#
# Jobs tree elements
#

class JobsTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, owner, task):
        QtGui.QTreeWidgetItem.__init__(self)
        self.owner = owner
        self.task  = task
        self.setText(0, task.name)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsUserCheckable)
        if task.isActive:
            self.setCheckState(0, QtCore.Qt.Checked)
        else:
            self.setCheckState(0, QtCore.Qt.Unchecked)
        
    def menu(self):
        menu = QtGui.QMenu()
        
        newAction = QtGui.QAction("Create new job", menu)
        newAction.triggered.connect(self.owner.createNewTask)
        menu.addAction(newAction)
        
        newAction = QtGui.QAction("Edit job", menu)
        newAction.triggered.connect(partial(self.owner.editTask, self.task))
        menu.addAction(newAction)
        
        newAction = QtGui.QAction("Delete job", menu)
        newAction.triggered.connect(partial(self.owner.deleteTask, self.task))
        menu.addAction(newAction)  
        
        newAction = QtGui.QAction("Run job", menu)
        newAction.triggered.connect(partial(self.owner.runTask, self.task))
        menu.addAction(newAction)              
        
        return menu
    
    def setData(self, column, role, value):
        if column == 0 and role == QtCore.Qt.CheckStateRole:
            self.task.isActive = value.toBool()

        super(JobsTreeItem, self).setData(column, role, value)

#############################################################################################################
#
# Definitions tree elements
#

class DefinitionsTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, owner, definition):
        QtGui.QTreeWidgetItem.__init__(self)
        self.owner = owner
        self.definition = definition
        self.setText(0, definition.name)
        
    def menu(self):
        menu = QtGui.QMenu()
        
        newAction = QtGui.QAction("Create new definition", menu)
        newAction.triggered.connect(self.owner.createDefinition)
        menu.addAction(newAction)
        
        newAction = QtGui.QAction("Edit definition", menu)
        newAction.triggered.connect(partial(self.owner.editDefinition, self.definition))
        menu.addAction(newAction)
        
        newAction = QtGui.QAction("Delete definition", menu)
        newAction.triggered.connect(partial(self.owner.deleteDefinition, self.definition))
        menu.addAction(newAction)  
                
        return menu
        
#############################################################################################################
#
# Retain strategy tree elements
#

class RetainTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, owner, strategy):
        QtGui.QTreeWidgetItem.__init__(self)
        self.strategy = strategy
        self.setText(0, strategy.name)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = BritApp()
    window.show()
    sys.exit(app.exec_())
    