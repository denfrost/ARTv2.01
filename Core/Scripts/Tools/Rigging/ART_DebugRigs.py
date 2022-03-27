"""
Author: Jeremy Ernst
"""

import os
from functools import partial

import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_DebugRigs():
    """
    This class is used in developing rigs for modules and quickly testing them without having to go
    through the entire build/publish process.

        .. image:: /images/debugRigs.png

    """

    def __init__(self, mainUI):
        """
        Instantiate the class, getting the QSettings, and building the interface.

        :param mainUI: The instance of the Rig Creator UI from which this class was called.

        """

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.projectPath = settings.value("projectPath")

        self.mainUI = mainUI

        # build the UI
        if cmds.window("ART_DebugRigsWin", exists=True):
            cmds.deleteUI("ART_DebugRigsWin", wnd=True)

        self.buildUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        """
        Build the UI, listing all modules in the scene that make up the asset for the user to select and build rigs
        for the selected.

        """

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.mainUI)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.mainWin.setWindowIcon(window_icon)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.mainWin.setStyleSheet(self.style)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # set qt object name
        self.mainWin.setObjectName("ART_DebugRigsWin")
        self.mainWin.setWindowTitle("Build Rigs")

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # set size policy
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.mainWin.resize(400, 300)
        self.mainWin.setSizePolicy(mainSizePolicy)
        self.mainWin.setMinimumSize(QtCore.QSize(400, 300))
        self.mainWin.setMaximumSize(QtCore.QSize(400, 300))

        # create the QFrame for this page
        self.background = QtWidgets.QFrame()
        self.background.setObjectName("mid")
        self.layout.addWidget(self.background)
        self.mainLayout = QtWidgets.QHBoxLayout(self.background)

        # create the list on the left and add the modules to the list
        self.moduleList = QtWidgets.QListWidget()
        self.mainLayout.addWidget(self.moduleList)

        for mod in self.mainUI.moduleInstances:
            item = QtWidgets.QListWidgetItem(mod.name)
            item.setData(QtCore.Qt.UserRole, mod)
            self.moduleList.addItem(item)

        # create our buttons on the right
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.rightLayout)

        infoText = "This tool is only for testing rigs in development. "
        infoText += "It will leave behind nodes in your scene that you do NOT want to publish with. "
        infoText += "When using this tool, it is advised to open a clean scene to publish your final asset."

        self.info = QtWidgets.QLabel()
        self.rightLayout.addWidget(self.info)
        self.info.setWordWrap(True)
        self.info.setMinimumSize(150, 125)
        self.info.setMaximumSize(150, 125)
        self.info.setText(infoText)

        self.rightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 200, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        self.buildButton = QtWidgets.QPushButton("Build Rigs For Selected")
        self.buildButton.setObjectName("settings")
        self.rightLayout.addWidget(self.buildButton)
        self.buildButton.setMinimumSize(150, 40)
        self.buildButton.setMaximumSize(150, 40)
        self.buildButton.clicked.connect(partial(self.buildRigs))

        self.deleteButton = QtWidgets.QPushButton("Remove Selected Rigs")
        self.deleteButton.setObjectName("settings")
        self.rightLayout.addWidget(self.deleteButton)
        self.deleteButton.setMinimumSize(150, 40)
        self.deleteButton.setMaximumSize(150, 40)
        self.deleteButton.clicked.connect(partial(self.deleteRig))

        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.setObjectName("settings")
        self.rightLayout.addWidget(self.closeButton)
        self.closeButton.setMinimumSize(150, 40)
        self.closeButton.setMaximumSize(150, 40)
        self.closeButton.clicked.connect(partial(self.close))

        self.mainWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRigs(self):
        """
        Builds the rigs for the selected module by calling on that module's buildRig function.

        """

        data = self.moduleList.currentItem().data(QtCore.Qt.UserRole)

        # call on inst build rigs functions
        if not cmds.objExists("driver_root"):
            riggingUtils.createDriverSkeleton()
        data.buildRig(None, self.mainUI)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def deleteRig(self):
        """
        Deletes the rigs for the selected module by calling on that module's deleteRig function.

        """

        data = self.moduleList.currentItem().data(QtCore.Qt.UserRole)
        data.deleteRig()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def close(self):
        """
        Close the interface and delete the window.

        """

        if cmds.window("ART_DebugRigsWin", exists=True):
            cmds.deleteUI("ART_DebugRigsWin", wnd=True)
