"""
Author: Jeremy Ernst
"""

import json
import os
import socket
from functools import partial

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
import maya.mel as mel
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


class ART_HotkeyEditor(QtWidgets.QMainWindow):
    """
    This class is used to create an interface to setup and manage hotkeys specific to ARTv2.

    """

    def __init__(self, parent=None):
        """
        Instantiates the class, gets settings values from QSettings. Calls on building the interface.

        """

        super(ART_HotkeyEditor, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")

        # create a dictionary of all hotkey widgets that get created (label, lineEdit, checkbox)
        self.widgets = {}

        # build the interface
        self.buildInterface()

        # get hotkey files and parse data
        self.hotkeyData = self.findHotkeys()

        # populate the interface with the hotkeyData
        # first, populate the combo box with the categories
        for key in self.hotkeyData:
            self.categoryCombobox.addItem(key)

            # next, add listWidgetItems for each key in the group dict
            groups = self.hotkeyData.get(key)
            for group in groups:
                self.categoryList.addItem(group)

                # then, create a stackWidget for each group item
                entries = groups.get(group)
                self.addHotkeyWidgets(key, group, entries)

        # select the first entry in the list
        if self.categoryList.count() > 0:
            self.categoryList.setCurrentRow(0)

            # set the proper QFrame to display
            self.changeCategory()

        # store the pre-ARTv2 hotkeySet
        self.originalHotkeySet = cmds.hotkeySet(q=True, current=True)

        allKeys = settings.allKeys()
        if "hotkeySetOriginal" not in allKeys:
            settings.setValue("hotkeySetOriginal", self.originalHotkeySet)

        # populate the keyset combo box
        self.populateComboBox()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # check for hotkey file and populate UI with that data
        host = socket.gethostname()
        keysetName = "ARTv2_" + host

        prefs = cmds.internalVar(upd=True)
        hkeyDir = utils.returnNicePath(prefs, "hotkeys")
        filename = utils.returnNicePath(hkeyDir, keysetName + ".hkeys")

        if os.path.exists(filename):
            # open and read the file contents
            json_file = open(filename)
            data = json.load(json_file)
            json_file.close()

            # populate the UI based on data
            self.populateUI(data)



    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findHotkeys(self):

        returnDict = {}
        groupDict = {}

        # get hotkey script files
        files = os.listdir(utils.returnNicePath(self.scriptPath, "Hotkeys"))
        for each in files:
            script = each.partition(".")[0]
            if script != "__init__":
                # import the module in order to grab variables
                mod = __import__('Hotkeys.' + script, globals(), locals(), [script])

                # get file variables that determine name in UI, category, and group
                label = mod.label
                cat = mod.cat
                grp = mod.grp

                if cat not in returnDict:
                    returnDict[cat] = groupDict

                if grp not in groupDict:
                    groupDict[grp] = []

                entryData = groupDict.get(grp)
                if [label, script] not in entryData:
                    groupDict[grp].append([label, script])

        return returnDict

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildInterface(self):
        """
        build the interface to setup and manage hotkeys in ARTv2.

        """
        # set the window size
        self.setMinimumSize(QtCore.QSize(750, 450))
        self.setMaximumSize(QtCore.QSize(750, 450))

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.setCentralWidget(self.mainWidget)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)

        # set qt object name
        self.setObjectName("ART_HotkeyEditorUI")
        self.setWindowTitle("ARTv2 Hotkey Editor")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # create the mainLayout
        self.mainLayout = QtWidgets.QHBoxLayout(self.mainWidget)

        # load the stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)
        self.mainWidget.setStyleSheet(self.style)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create the first column, which has a group box with a Tools title, and a list widget of hotkey categories
        self.columnA = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.columnA)

        # add hboxlayout for current keyset
        self.keysetLayout = QtWidgets.QHBoxLayout()
        self.columnA.addLayout(self.keysetLayout)

        label = QtWidgets.QLabel("Hotkey Set:")
        label.setStyleSheet("background: transparent;")
        self.keysetLayout.addWidget(label)

        self.keyComboBox = QtWidgets.QComboBox()
        self.keyComboBox.setObjectName("light")
        self.keysetLayout.addWidget(self.keyComboBox)
        self.keyComboBox.currentIndexChanged.connect(self.changeKeySet)

        # add the groupbox
        self.groupBox = QtWidgets.QGroupBox("Tools")
        self.columnA.addWidget(self.groupBox)
        self.groupBox.setMinimumSize(QtCore.QSize(190, 400))
        self.groupBox.setMaximumSize(QtCore.QSize(190, 400))

        # add a layout to sit inside the groupbox
        self.groupBoxLayout = QtWidgets.QVBoxLayout(self.groupBox)

        # add the combo box for tools categories
        self.categoryCombobox = QtWidgets.QComboBox()
        self.categoryCombobox.setObjectName("light")
        self.groupBoxLayout.addWidget(self.categoryCombobox)

        # add the list widget that lists each categories hotkey sub-categories
        self.categoryList = QtWidgets.QListWidget()
        self.categoryList.setObjectName("dark")
        self.groupBoxLayout.addWidget(self.categoryList)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create the second column, which holds all the possible hotkey bindings
        self.columnB = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.columnB)

        headerLayout = QtWidgets.QHBoxLayout()
        self.columnB.addLayout(headerLayout)

        labelA = QtWidgets.QLabel("  Function")
        labelA.setMinimumWidth(250)
        labelA.setStyleSheet("background: transparent")

        labelB = QtWidgets.QLabel("Key Modifiers")
        labelB.setMinimumWidth(130)
        labelB.setStyleSheet("background: transparent")

        labelC = QtWidgets.QLabel("Key Binding")
        labelC.setMinimumWidth(120)
        labelC.setStyleSheet("background: transparent")

        headerLayout.addWidget(labelA)
        headerLayout.addWidget(labelB)
        headerLayout.addWidget(labelC)

        # create groupbox to house keybind settings
        self.entriesGroupBox = QtWidgets.QFrame()
        self.entriesGroupBox.setObjectName("darkborder")
        self.columnB.addWidget(self.entriesGroupBox)
        self.entriesGroupBox.setMinimumSize(QtCore.QSize(490, 330))
        self.entriesGroupBox.setMaximumSize(QtCore.QSize(490, 330))

        # add a stack widget
        self.stackLayout = QtWidgets.QStackedWidget(self.entriesGroupBox)
        self.stackLayout.setMinimumSize(QtCore.QSize(480, 320))
        self.stackLayout.setMaximumSize(QtCore.QSize(480, 320))
        self.stackLayout.setObjectName("dark")
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create the bottom button layout
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.columnB.addLayout(self.buttonLayout)

        # create the different buttons and spacers
        self.loadButton = QtWidgets.QPushButton("Load")
        self.loadButton.setMinimumSize(QtCore.QSize(124, 40))
        self.loadButton.setMaximumSize(QtCore.QSize(124, 40))
        self.buttonLayout.addWidget(self.loadButton)
        self.loadButton.setObjectName("settings")
        self.loadButton.clicked.connect(self.loadHotkeys)

        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setMinimumSize(QtCore.QSize(124, 40))
        self.saveButton.setMaximumSize(QtCore.QSize(124, 40))
        self.buttonLayout.addWidget(self.saveButton)
        self.saveButton.setObjectName("settings")
        self.saveButton.clicked.connect(self.saveHotkeys)

        self.closeButton = QtWidgets.QPushButton("Save and Close")
        self.closeButton.setMinimumSize(QtCore.QSize(124, 40))
        self.closeButton.setMaximumSize(QtCore.QSize(124, 40))
        self.buttonLayout.addWidget(self.closeButton)
        self.closeButton.setObjectName("settings")
        self.closeButton.clicked.connect(self.saveAndClose)

        # setup signals and slots
        self.categoryCombobox.currentIndexChanged.connect(partial(self.changeCategory))
        self.categoryList.currentItemChanged.connect(partial(self.changeCategory))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addHotkeyWidgets(self, category, groupName, entries):

        # first create a widget to add to the stackedLayout
        widget = QtWidgets.QFrame()
        widget.setMinimumSize(QtCore.QSize(490, 330))
        widget.setMaximumSize(QtCore.QSize(490, 330))
        widget.setObjectName("darkborder")
        widget.setProperty("Category", [category, groupName])
        self.stackLayout.addWidget(widget)
        self.stackLayout.setCurrentWidget(widget)

        # add the layout to the widget to hold the entries
        layout = QtWidgets.QVBoxLayout(widget)

        # add the entries to the layout
        self.addCategoryEntries(entries, layout, category, groupName)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def hotkey_check(self, label, ctl, alt, sht, key, *args):
        """
        Checks to see if the hotkey has changed during this UI session. If it has, it clears the original hotkey
        assignment.
        """

        currentKeySet = self.keyComboBox.currentText()
        prefs = cmds.internalVar(upd=True)
        hkeyDir = utils.returnNicePath(prefs, "hotkeys")
        filename = utils.returnNicePath(hkeyDir, currentKeySet + ".hkeys")

        if os.path.exists(filename):
            # open and read the file contents
            json_file = open(filename)
            originalData = json.load(json_file)
            json_file.close()

            hasChanged = False
            query_command = ""
            nameCommand = ""
            command_string = ""

            for data in originalData:
                if data[1] == label.text():
                    nameCommand = label.property("script")
                    query_command = "hotkey -q"
                    command_string = "hotkey -k \"" + data[5] + "\""

                    if data[5] != key.currentText():
                        hasChanged = True

                    if data[2] != ctl.isChecked():
                        hasChanged = True
                        query_command += " -ctl"
                        command_string += " -ctl"

                    if data[3] != alt.isChecked():
                        hasChanged = True
                        query_command += " -alt"
                        command_string += " -alt"

                    if data[4] != sht.isChecked():
                        hasChanged = True
                        query_command += " -sht"
                        command_string += " -sht"

                    query_command += " -name \"" + data[5] + "\";"

            if hasChanged is True:
                try:
                    result = mel.eval(query_command)
                    if result == nameCommand:
                        command_string += " -name \"\";"
                        mel.eval(command_string)
                        cmds.savePrefs()
                except Exception, e:
                    pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addCategoryEntries(self, entries, parent, category, groupName, *args):

        # take the passed in entries (things like: ["Toggle Animation UI", "toggleAnimUI"] and create UI widgets
        # that will allow the user to actually set hotkeys for things.
        for entry in entries:
            label = QtWidgets.QLabel(entry[0])
            label.setMinimumWidth(200)
            label.setMaximumWidth(200)
            label.setStyleSheet("background: transparent")
            label.setProperty("script", entry[1])

            # create buttons for ctrl, alt and shift (checkable)
            ctrlBtn = QtWidgets.QPushButton("ctrl")
            ctrlBtn.setMinimumWidth(40)
            ctrlBtn.setMaximumWidth(40)
            ctrlBtn.setCheckable(True)
            ctrlBtn.setChecked(False)
            ctrlBtn.setObjectName("hotkey")

            altBtn = QtWidgets.QPushButton("alt")
            altBtn.setMinimumWidth(40)
            altBtn.setMaximumWidth(40)
            altBtn.setCheckable(True)
            altBtn.setChecked(False)
            altBtn.setObjectName("hotkey")

            shiftBtn = QtWidgets.QPushButton("shift")
            shiftBtn.setMinimumWidth(40)
            shiftBtn.setMaximumWidth(40)
            shiftBtn.setCheckable(True)
            shiftBtn.setChecked(False)
            shiftBtn.setObjectName("hotkey")

            # create combo box for keys
            comboBox = QtWidgets.QComboBox()
            comboBox.setObjectName("light")
            comboBox.setMinimumWidth(100)
            comboBox.setMaximumWidth(100)
            self.addKeys(comboBox)

            self.widgets[entry[0]] = [label, ctrlBtn, altBtn, shiftBtn, comboBox, category, groupName]

            layout = QtWidgets.QHBoxLayout()
            parent.addLayout(layout)
            layout.addWidget(label)
            layout.addWidget(ctrlBtn)
            layout.addWidget(altBtn)
            layout.addWidget(shiftBtn)
            layout.addWidget(comboBox)

            ctrlBtn.clicked.connect(partial(self.hotkey_check, label, ctrlBtn, altBtn, shiftBtn, comboBox))
            altBtn.clicked.connect(partial(self.hotkey_check, label, ctrlBtn, altBtn, shiftBtn, comboBox))
            shiftBtn.clicked.connect(partial(self.hotkey_check, label, ctrlBtn, altBtn, shiftBtn, comboBox))
            comboBox.currentIndexChanged.connect(partial(self.hotkey_check, label, ctrlBtn, altBtn, shiftBtn, comboBox))

        # add spacer
        spacerItem = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        parent.addItem(spacerItem)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleAllCheckboxes(self, checckBox, *args):

        # get all entries in the entires layout
        children = self.stackLayout.children()

        for child in children:
            if type(child) == QtWidgets.QFrame:
                # get the vboxlayout for each frame
                groupChildren = child.children()
                for groupChild in groupChildren:
                    if type(groupChild) == QtWidgets.QVBoxLayout:
                        for i in range(groupChild.count()):
                            if type(groupChild.itemAt(i)) == QtWidgets.QHBoxLayout:

                                # get the children of the hbox layout
                                hboxLayout = groupChild.itemAt(i).layout()

                                # get the label text
                                for index in range(hboxLayout.count()):
                                    if type(hboxLayout.itemAt(index).widget()) == QtWidgets.QLabel:
                                        text = hboxLayout.itemAt(index).widget().text()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveHotkeys(self):

        # get hotkey keybind data on current entires page
        # [entry[1], label.text(), ctrlBtn, altBtn, shiftBtn, comboBox])  <- data
        data = self.gatherHotkeyData()

        # create nameCommands and set keybind
        for each in data:
            # look in keybind for modifiers
            ctl = each[2]
            alt = each[3]
            sht = each[4]
            key = each[5].lower()

            # build the python command
            commandString = "python(\"import Hotkeys." + each[0] + "; Hotkeys." + each[0] + ".run()\")"
            cmds.nameCommand(str(each[0]), ann=each[1], c=commandString)

            # check if hotkey assignment currently exists. If so, remove assignment
            mapping = cmds.hotkeyCheck(keyString=key, ctl=ctl, alt=alt)

            if len(mapping) > 0:
                # unset the command
                cmds.hotkey(k=key, ctl=ctl, alt=alt, sht=sht, name='')
                # cmds.savePrefs(hotkeys=True)

            # set the new hotkey
            cmds.hotkey(k=key, ctl=ctl, alt=alt, sht=sht, name=str(each[0]))

        cmds.savePrefs(hotkeys=True)
        self.saveHotkeyData()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveAndClose(self):

        self.saveHotkeys()
        if cmds.window("ART_HotkeyEditorUI", exists=True):
            cmds.deleteUI("ART_HotkeyEditorUI", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def gatherHotkeyData(self, save=False):

        returnData = []

        # get all entries in the stack widget
        children = self.stackLayout.children()

        for child in children:
            if type(child) == QtWidgets.QFrame:
                # get the vboxlayout for each frame
                groupChildren = child.children()
                for groupChild in groupChildren:
                    if type(groupChild) == QtWidgets.QVBoxLayout:
                        for i in range(groupChild.count()):
                            if type(groupChild.itemAt(i)) == QtWidgets.QHBoxLayout:

                                # get the children of the hbox layout
                                hboxLayout = groupChild.itemAt(i).layout()

                                # get the label text
                                for index in range(hboxLayout.count()):
                                    if type(hboxLayout.itemAt(index).widget()) == QtWidgets.QLabel:
                                        text = hboxLayout.itemAt(index).widget().text()

                                        # get the info from each entry
                                        data = self.widgets.get(text)
                                        label = data[0]  # annotation
                                        ctrlBtn = data[1]
                                        altBtn = data[2]
                                        shiftBtn = data[3]
                                        comboBox = data[4]
                                        cat = data[5]
                                        grp = data[6]

                                        # compare the label to the entries
                                        categories = self.hotkeyData.get(cat)
                                        for category in categories:
                                            entries = categories.get(category)
                                            for entry in entries:
                                                if label.text() == entry[0]:
                                                    if save is False:
                                                        if comboBox.currentText() != "":
                                                            returnData.append([entry[1], label.text(),
                                                                               ctrlBtn.isChecked(), altBtn.isChecked(),
                                                                               shiftBtn.isChecked(),
                                                                               comboBox.currentText()])
                                                        else:
                                                            cmds.hotkey(k=str(comboBox.currentText().lower()),
                                                                        ctl=ctrlBtn.isChecked(),
                                                                        alt=altBtn.isChecked(),
                                                                        sht=shiftBtn.isChecked(), name="")
                                                    if save is True:
                                                        returnData.append([category, label.text(), ctrlBtn.isChecked(),
                                                                           altBtn.isChecked(), shiftBtn.isChecked(),
                                                                           comboBox.currentText()])

        return returnData
        # self.widgets[entry[0]] = [label, ctrlBtn, altBtn, shiftBtn, comboBox, checkbox, category, groupName]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveHotkeyData(self):

        # save out a json file that will be used for populating the UI.
        # (label, keybind, checked) per entry
        data = self.gatherHotkeyData(save=True)

        # get user pref dir
        prefs = cmds.internalVar(upd=True)

        # write data to json
        keysetName = self.keyComboBox.currentText()

        hkeyDir = utils.returnNicePath(prefs, "hotkeys")
        filename = utils.returnNicePath(hkeyDir, keysetName + ".hkeys")
        f = open(filename, 'w')

        # dump the data with json
        json.dump(data, f)
        f.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateUI(self, data):

        # take incoming data, compare to QLabels, fill in corresponding keybind and set checkbox

        # get all entries in the entires layout
        children = self.stackLayout.children()

        for child in children:
            if type(child) == QtWidgets.QFrame:
                # get the vboxlayout for each frame
                groupChildren = child.children()
                for groupChild in groupChildren:
                    if type(groupChild) == QtWidgets.QVBoxLayout:
                        for i in range(groupChild.count()):
                            if type(groupChild.itemAt(i)) == QtWidgets.QHBoxLayout:

                                # get the children of the hbox layout
                                hboxLayout = groupChild.itemAt(i).layout()
                                # get the label text
                                for index in range(hboxLayout.count()):
                                    if type(hboxLayout.itemAt(index).widget()) == QtWidgets.QLabel:
                                        text = hboxLayout.itemAt(index).widget().text()

                                        # get the info from each entry
                                        info = self.widgets.get(text)
                                        label = info[0]  # annotation
                                        ctrlBtn = info[1]
                                        altBtn = info[2]
                                        shiftBtn = info[3]
                                        comboBox = info[4]

                                        for each in data:
                                            if each[1] == text:
                                                ctrl = each[2]
                                                alt = each[3]
                                                shift = each[4]
                                                key = each[5]

                                                ctrlBtn.setChecked(ctrl)
                                                altBtn.setChecked(alt)
                                                shiftBtn.setChecked(shift)

                                                index = comboBox.findText(key, QtCore.Qt.MatchExactly)
                                                comboBox.setCurrentIndex(index)

    # self.widgets[entry[0]] = [label, ctrlBtn, altBtn, shiftBtn, comboBox, checkbox, category, groupName]
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeKeySet(self):

        # create file name from working keyset
        keyset = self.keyComboBox.currentText()
        prefs = cmds.internalVar(upd=True)
        prefs = utils.returnNicePath(prefs, "hotkeys")
        filename = utils.returnNicePath(prefs, keyset + ".hkeys")

        if os.path.exists(filename):
            json_file = open(filename, 'r')
            data = json.load(json_file)
            json_file.close()

            # set combo box to new keyset
            hkeyBase = os.path.basename(filename)
            hkeyBase = hkeyBase.rpartition(".")[0]

            index = self.keyComboBox.findText(hkeyBase, QtCore.Qt.MatchExactly)
            self.keyComboBox.setCurrentIndex(index)

            # populate the UI based on data
            self.populateUI(data)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def loadHotkeys(self):

        # get user prefs directory and open a file dialog
        prefs = cmds.internalVar(upd=True)
        prefs = utils.returnNicePath(prefs, "hotkeys")

        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Select Hotkeys", prefs, "*.hkeys")

        # open and read the file contents
        json_file = open(filename[0])
        data = json.load(json_file)
        json_file.close()

        # add item to the keyset combo box if it doesn't exist
        keysets = []
        for i in range(self.keyComboBox.count()):
            text = self.keyComboBox.itemText(i)
            keysets.append(text)

        hkeyBase = os.path.basename(filename[0])
        hkeyBase = hkeyBase.rpartition(".")[0]

        if hkeyBase not in keysets:
            self.keyComboBox.addItem(hkeyBase)

        # set comobo box to new keyset
        index = self.keyComboBox.findText(hkeyBase, QtCore.Qt.MatchExactly)
        self.keyComboBox.setCurrentIndex(index)

        # populate the UI based on data
        self.populateUI(data)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateComboBox(self):

        # get user prefs directory and list hkeys files in directory
        prefs = cmds.internalVar(upd=True)
        prefs = utils.returnNicePath(prefs, "hotkeys")

        hkeys = []
        files = os.listdir(prefs)
        for f in files:
            if f.rpartition(".")[2] == "hkeys":
                hkeys.append(f)

        # get default keyset name
        host = socket.gethostname()
        keysetName = "ARTv2_" + host

        # if no keyset files found, add default.
        if len(hkeys) == 0:
            self.keyComboBox.addItem(keysetName)

        # otherwise, add keyset files found
        if len(hkeys) > 0:
            for each in hkeys:
                self.keyComboBox.addItem(each.rpartition(".")[0])

        # select the hotkey set that matches host name by default
        index = self.keyComboBox.findText(keysetName, QtCore.Qt.MatchExactly)
        self.keyComboBox.setCurrentIndex(index)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeCategory(self, *args):

        # get the selected category and group
        category = self.categoryCombobox.currentText()
        try:
            section = self.categoryList.currentItem().text()
        except AttributeError:
            return

        # set the proper QFrame to display
        frames = self.stackLayout.children()
        for frame in frames:
            info = frame.property("Category")
            if info is not None:
                if info[0] == category:
                    if info[1] == section:
                        self.stackLayout.setCurrentWidget(frame)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addKeys(self, comboBox, *args):

        keys = ["", "PgUp", "PgDown", "Ins", "Home", "End", "/", "*", "-", "+", "1", "2", "3", "4", "5", "6", "7", "8",
                "9", "0", ".", ",", "Up", "Down", "Left", "Right", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
                "F10", "F11", "F12", "`", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                "O", "P", "Q", "R", "S", "T", "U", "V", "W", "U", "X", "Y", "Z", ";", "'", "[", "]", "\\"]

        for key in keys:
            comboBox.addItem(key)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    if cmds.window("ART_HotkeyEditorUI", exists=True):
        cmds.deleteUI("ART_HotkeyEditorUI", wnd=True)

    # check current maya hotkeyset to make sure it is not Maya Default
    try:
        current = cmds.hotkeySet(q=True, current=True)
        if current == "Maya_Default":
            cmds.warning("You must use a valid hotkey set for this tool to work. Please create a new hotkey set in"
                         " Maya's hotkey editor.")
            return
    except Exception:
        pass

    gui = ART_HotkeyEditor(interfaceUtils.getMainWindow())
    gui.show()
