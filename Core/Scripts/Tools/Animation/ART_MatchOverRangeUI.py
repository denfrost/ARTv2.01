"""
Module for matching rigs over a frame range. Contains classes for the front-end interface, and the actual matching
functionality
"""
from functools import partial

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class Match(object):
    """
    Class for matching over frame range functionality.
    """

    def __init__(self, character, module_match_info, start_frame, end_frame):
        """
        :param character: which character namespace to operate on
        :param module_match_info: a list containing lists of modules and their match method
        :param start_frame: start frame to begin matching
        :param end_frame: end frame to stop matching
        """

        self.character = character
        self.module_match_info = module_match_info
        self.start_frame = int(start_frame)
        self.end_frame = int(end_frame)

        self.execute_match()

    def execute_match(self):
        """
        Executes the match over frame range functionality, going through each entry in the module_match_info list,
        and executing that modules match method on each frame during the frame range.
        """

        currentMode = cmds.evaluationManager(q=True, mode=True)[0]
        cmds.evaluationManager(mode="off")

        # loop through frame range, calling each module's match function given the match method
        if len(self.module_match_info) > 0:
            for i in range(self.start_frame, self.end_frame + 1):
                cmds.currentTime(i)
                for each in self.module_match_info:
                    # get inst
                    modType = cmds.getAttr(each[0] + ".moduleType")
                    modName = cmds.getAttr(each[0] + ".moduleName")
                    mod = __import__("RigModules." + modType, {}, {}, [modType])

                    # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
                    moduleClass = getattr(mod, mod.className)

                    # find the instance of that module
                    moduleInst = moduleClass(self, modName)

                    # set namespace for instance
                    moduleInst.namespace = self.character + ":"

                    # call on module's match function (method, checkbox, match over range)
                    moduleInst.switchMode(each[1], None, True)

        cmds.evaluationManager(mode=currentMode)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_MatchOverRange(object):
    """
    Class that provides front-end interface for setting up matching over frame range. Lists all modules in the scene
    that have multiple rigs, and their match methods, as well as providing start and end frame entries.
    """

    def __init__(self, animPickerUI):
        super(ART_MatchOverRange, self).__init__()

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.pickerUI = animPickerUI

        # build the UI
        self._build_interface()

    def _build_interface(self):
        if cmds.window("pyART_MatchOverRangeWIN", exists=True):
            cmds.deleteUI("pyART_MatchOverRangeWIN", wnd=True)

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.pickerUI)

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("dark")
        self.mainWin.setCentralWidget(self.mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.mainWin.setStyleSheet(self.style)

        # set window size
        self.mainWin.setMinimumSize(QtCore.QSize(600, 350))
        self.mainWin.setMaximumSize(QtCore.QSize(600, 350))
        self.mainWin.resize(600, 350)

        # set qt object name
        self.mainWin.setObjectName("pyART_MatchOverRangeWIN")
        self.mainWin.setWindowTitle("Match Over Frame Range")
        self.mainWin.closeEvent = self.closeEvent

        # horizontal layout
        self.mainLayout = QtWidgets.QHBoxLayout(self.mainWidget)

        # LEFT SIDE
        # module list widget
        self.moduleList = QtWidgets.QListWidget()
        self.mainLayout.addWidget(self.moduleList)
        self.moduleList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.moduleList.setSpacing(20)

        # RIGHT SIDE
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.rightLayout)

        self.rightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.characterCombo = QtWidgets.QComboBox()
        self.characterCombo.setObjectName("mid")
        self.rightLayout.addWidget(self.characterCombo)
        self.characterCombo.setMinimumHeight(50)
        self.characterCombo.setMaximumHeight(50)
        self.characterCombo.setIconSize(QtCore.QSize(40, 40))
        self.characterCombo.currentIndexChanged.connect(partial(self._find_character_modules))

        # frame ranges

        # SPACER!
        self.rightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))

        self.rangeLayout = QtWidgets.QHBoxLayout()
        self.rightLayout.addLayout(self.rangeLayout)

        label1 = QtWidgets.QLabel("Start:")
        label1.setStyleSheet("background: transparent;")
        self.rangeLayout.addWidget(label1)

        self.startFrame = QtWidgets.QSpinBox()
        self.startFrame.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rangeLayout.addWidget(self.startFrame)
        self.startFrame.setRange(-10000, 10000)

        label2 = QtWidgets.QLabel("End:")
        label2.setStyleSheet("background: transparent;")
        self.rangeLayout.addWidget(label2)

        self.endFrame = QtWidgets.QSpinBox()
        self.endFrame.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rangeLayout.addWidget(self.endFrame)
        self.endFrame.setRange(-10000, 10000)

        # SPACER!
        self.rightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # Button
        self.matchButton = QtWidgets.QPushButton("Match")
        self.rightLayout.addWidget(self.matchButton)
        self.matchButton.setObjectName("settings")
        self.matchButton.setMinimumHeight(50)
        self.matchButton.clicked.connect(self._match)

        # SPACER!
        self.rightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))

        # show the window
        self.mainWin.show()

        # populate UI
        self._find_characters()
        self._find_character_modules()

        startFrame = cmds.playbackOptions(q=True, min=True)
        endFrame = cmds.playbackOptions(q=True, max=True)

        self.startFrame.setValue(startFrame)
        self.endFrame.setValue(endFrame)

        # restore window position
        settings = QtCore.QSettings("ARTv2", "MatchOverRange")
        self.mainWin.restoreGeometry(settings.value("geometry"))

    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):
        self.settings = QtCore.QSettings("ARTv2", "MatchOverRange")
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self.mainWin, event)

    def _find_characters(self):
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
            except StandardError:
                namespace = cmds.getAttr(node + ".name")

            # add the icon found on the node's icon path attribute to the tab
            iconPath = cmds.getAttr(node + ".iconPath")
            iconPath = utils.returnNicePath(self.projectPath, iconPath)
            icon = QtGui.QIcon(iconPath)

            self.characterCombo.addItem(icon, namespace)

    def _find_character_modules(self, *args):
        print args
        self.moduleList.clear()

        # current character
        selectedChar = self.characterCombo.currentText()

        # get rig modules
        if cmds.objExists(selectedChar + ":" + "ART_RIG_ROOT"):
            modules = cmds.listConnections(selectedChar + ":" + "ART_RIG_ROOT.rigModules")

            for module in modules:
                niceName = cmds.getAttr(module + ".moduleName")
                moduleType = cmds.getAttr(module + ".moduleType")

                # create widget
                item = QtWidgets.QListWidgetItem()

                widgetItem = QtWidgets.QGroupBox()
                widgetItem.setMinimumHeight(50)
                widgetItem.setProperty("module", module)
                widgetItem.setObjectName("light")

                layout = QtWidgets.QHBoxLayout(widgetItem)

                checkBox = QtWidgets.QCheckBox(niceName)
                checkBox.setChecked(False)
                layout.addWidget(checkBox)

                comboBox = QtWidgets.QComboBox()
                layout.addWidget(comboBox)

                # add items to combo box bases on module class var
                mod = __import__("RigModules." + moduleType, {}, {}, [moduleType])
                matchData = mod.matchData

                if matchData[0] is True:
                    for each in matchData[1]:
                        comboBox.addItem(each)

                    comboBox.setCurrentIndex(1)

                    self.moduleList.addItem(item)
                    self.moduleList.setItemWidget(item, widgetItem)

    def _match(self):
        # get the current character
        character = self.characterCombo.currentText()

        # go through each module in list, find import method, and setup constraints accordingly
        moduleItems = []
        for i in range(self.moduleList.count()):
            item = self.moduleList.item(i)
            itemWidget = self.moduleList.itemWidget(item)
            itemModule = itemWidget.property("module")

            children = itemWidget.children()
            for child in children:

                if type(child) == QtWidgets.QCheckBox:
                    value = child.isChecked()
                    if value is False:
                        break

                if type(child) == QtWidgets.QComboBox:
                    matchMethod = child.currentText()
                    moduleItems.append([itemModule, matchMethod])

        # get frame range
        start = self.startFrame.value()
        end = self.endFrame.value()

        Match(character, moduleItems, start, end)
