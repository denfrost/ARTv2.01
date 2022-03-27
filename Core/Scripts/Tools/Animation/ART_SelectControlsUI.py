
import json
import os
from functools import partial

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_SelectControls(object):
    def __init__(self, animPickerUI, showUI, parent=None):

        super(ART_SelectControls, self).__init__()

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.pickerUI = animPickerUI
        self.showUI = showUI

        # build the UI or just go straight to selecting all controls
        if self.showUI:
            self.buildUI()
        else:
            self.selectControls()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):

        if cmds.window("pyART_SelectControlsWIN", exists=True):
            cmds.deleteUI("pyART_SelectControlsWIN", wnd=True)

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.pickerUI)

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("dark")
        self.mainWin.setCentralWidget(self.mainWidget)

        self.mainWin.closeEvent = self.closeEvent

        # create the mainLayout
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.mainWin.setStyleSheet(self.style)

        self.mainWin.setMinimumSize(QtCore.QSize(400, 250))
        self.mainWin.setMaximumSize(QtCore.QSize(400, 250))
        self.mainWin.resize(400, 250)

        # set qt object name
        self.mainWin.setObjectName("pyART_SelectControlsWIN")
        self.mainWin.setWindowTitle("Select Rig Controls")

        self.layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.layout)

        # LEFT SIDE
        # list of modules
        self.moduleList = QtWidgets.QListWidget()
        self.moduleList.setMinimumSize(QtCore.QSize(180, 230))
        self.moduleList.setMaximumSize(QtCore.QSize(180, 230))
        self.layout.addWidget(self.moduleList)
        self.moduleList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.moduleList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.moduleList.customContextMenuRequested.connect(self.createContextMenu)

        # RIGHT SIDE
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.rightLayout)

        # character combo
        self.characterCombo = QtWidgets.QComboBox()
        self.characterCombo.setObjectName("mid")
        self.rightLayout.addWidget(self.characterCombo)
        self.characterCombo.setMinimumSize(QtCore.QSize(180, 60))
        self.characterCombo.setMaximumSize(QtCore.QSize(180, 60))
        self.characterCombo.setIconSize(QtCore.QSize(50, 50))
        self.characterCombo.currentIndexChanged.connect(partial(self.findCharacterModules))

        # select options
        self.fkControlsCB = QtWidgets.QCheckBox("FK Controls")
        self.fkControlsCB.setChecked(True)
        self.fkControlsCB.setToolTip(
            "If this is checked, for the selected modules,\nall FK controls will be selected or added to the"
            "selection.")
        self.rightLayout.addWidget(self.fkControlsCB)

        self.ikControlsCB = QtWidgets.QCheckBox("IK Controls")
        self.ikControlsCB.setChecked(True)
        self.ikControlsCB.setToolTip(
            "If this is checked, for the selected modules,\nall IK controls will be selected or added to the"
            "selection.")
        self.rightLayout.addWidget(self.ikControlsCB)

        self.specialControlsCB = QtWidgets.QCheckBox("Special Controls")
        self.specialControlsCB.setChecked(True)
        self.specialControlsCB.setToolTip(
            "If this is checked, for the selected modules,\nany control that is not FK or IK (like dynamics for"
            "example),\nwill be selected or added to the selection.")
        self.rightLayout.addWidget(self.specialControlsCB)

        self.selectSettingsCB = QtWidgets.QCheckBox("Include Settings")
        self.selectSettingsCB.setChecked(True)
        self.selectSettingsCB.setToolTip(
            "If this is checked, for the selected modules,\nall settings nodes will be included in the selection.")
        self.rightLayout.addWidget(self.selectSettingsCB)

        self.selectSpacesCB = QtWidgets.QCheckBox("Include Spaces")
        self.selectSpacesCB.setChecked(True)
        self.selectSpacesCB.setToolTip(
            "If this is checked, for the selected modules,\nall space switching nodes will be included in the"
            "selection.")
        self.rightLayout.addWidget(self.selectSpacesCB)

        self.rightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        self.selectCtrlsBtn = QtWidgets.QPushButton("Select Controls")
        self.selectCtrlsBtn.setMinimumWidth(180)
        self.selectCtrlsBtn.setMaximumWidth(180)
        self.selectCtrlsBtn.setMinimumHeight(30)
        self.rightLayout.addWidget(self.selectCtrlsBtn)
        self.selectCtrlsBtn.setObjectName("settings")
        self.selectCtrlsBtn.clicked.connect(self.selectControls)

        # show window
        if self.showUI:
            self.mainWin.show()

        # populate UI
        self.findCharacters()
        self.findCharacterModules()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "SelectRigControls")
        self.mainWin.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "SelectRigControls")
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self.mainWin, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createContextMenu(self, point):

        self.contextMenu = QtWidgets.QMenu()

        selectIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select.png"))))

        self.contextMenu.addAction(selectIcon, "Select All", self.selectAllInList)
        self.contextMenu.addAction("Clear Selection", self.clearListSelection)

        self.contextMenu.exec_(self.moduleList.mapToGlobal(point))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectAllInList(self):

        self.moduleList.selectAll()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def clearListSelection(self):

        self.moduleList.clearSelection()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findCharacters(self):

        allNodes = cmds.ls(type="network")
        characterNodes = []
        for node in allNodes:
            attrs = cmds.listAttr(node)
            if "rigModules" in attrs:
                characterNodes.append(node)

        # go through each node, find the character name, the namespace on the node, and the picker attribute
        for node in characterNodes:
            try:
                namespace = cmds.getAttr(node + ".namespace")
            except:
                namespace = cmds.getAttr(node + ".name")

            # add the icon found on the node's icon path attribute to the tab
            iconPath = cmds.getAttr(node + ".iconPath")
            iconPath = utils.returnNicePath(self.projectPath, iconPath)
            icon = QtGui.QIcon(iconPath)

            self.characterCombo.addItem(icon, namespace)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findCharacterModules(self, *args):

        if self.showUI:
            self.moduleList.clear()

            # current character
            selectedChar = self.characterCombo.currentText()

            # get rig modules
            if cmds.objExists(selectedChar + ":" + "ART_RIG_ROOT"):
                modules = cmds.listConnections(selectedChar + ":" + "ART_RIG_ROOT.rigModules")

                for module in modules:
                    modName = cmds.getAttr(module + ".moduleName")
                    item = QtWidgets.QListWidgetItem(modName)
                    item.setData(QtCore.Qt.UserRole, module)
                    self.moduleList.addItem(item)

        else:
            index = self.pickerUI.characterTabs.currentIndex()
            selectedChar = self.pickerUI.characterTabs.tabToolTip(index)

            if cmds.objExists(selectedChar + ":" + "ART_RIG_ROOT"):
                modules = cmds.listConnections(selectedChar + ":" + "ART_RIG_ROOT.rigModules")

            return modules

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectControls(self, selectFK=True, selectIK=True, selectSpecial=True, includeSettings=True,
                       includeSpaces=True):

        # get selection settings
        if self.showUI:
            selectFK = self.fkControlsCB.isChecked()
            selectIK = self.ikControlsCB.isChecked()
            selectSpecial = self.specialControlsCB.isChecked()
            includeSettings = self.selectSettingsCB.isChecked()
            includeSpaces = self.selectSpacesCB.isChecked()

            selected = self.moduleList.selectedItems()
            selectedChar = self.characterCombo.currentText()

        else:
            selected = self.findCharacterModules()
            index = self.pickerUI.characterTabs.currentIndex()
            selectedChar = self.pickerUI.characterTabs.tabToolTip(index)

        # create list to store controls to select later
        controlsToSelect = []

        # go through each selected module, or all modules if not showing UI
        for each in selected:
            if self.showUI:
                module = each.data(QtCore.Qt.UserRole)
            else:
                module = each

            # get inst
            modType = cmds.getAttr(module + ".moduleType")
            modName = cmds.getAttr(module + ".moduleName")
            mod = __import__("RigModules." + modType, {}, {}, [modType])

            # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
            moduleClass = getattr(mod, mod.className)

            # find the instance of that module
            moduleInst = moduleClass(self, modName)

            # set namespace for instance
            moduleInst.namespace = selectedChar + ":"

            # get controls for module
            networkNode = moduleInst.returnRigNetworkNode
            controls = moduleInst.getControls()

            # SELECTION OPTIONS
            for data in controls:
                for control in data:
                    type = cmds.getAttr(control + ".controlType")
                    if type == "FK":
                        if selectFK:
                            controlsToSelect.append(control)

                    if type == "IK":
                        if selectIK:
                            controlsToSelect.append(control)

                    if type == "Special":
                        if selectSpecial:
                            controlsToSelect.append(control)

            if includeSettings:
                moduleName = cmds.getAttr(networkNode + ".moduleName")
                controlsToSelect.append(selectedChar + ":" + moduleName + "_settings")
                controlsToSelect.append(selectedChar + ":" + "rig_settings")

            if includeSpaces:
                for data in controls:
                    for control in data:
                        fullPath = cmds.listRelatives(control, fullPath=True)[0]
                        parents = fullPath.split("|")
                        for parent in parents:
                            if parent.find("space_switcher") != -1:
                                if parent.find("_follow") == -1:
                                    if cmds.getAttr(parent + ".sourceModule") == modName:
                                        if parent not in controlsToSelect:
                                            controlsToSelect.append(parent)

        # select all the things
        cmds.select(clear=True)
        for each in controlsToSelect:
            if cmds.objExists(each):
                cmds.select(each, add=True)

        print str(len(controlsToSelect)) + " objects selected"
