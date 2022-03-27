'''
Created on Aug 26, 2015

@author: jeremy.ernst
'''

from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import maya.cmds as cmds
import os, json
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


class ART_RigHistoryUI():
    # Original Author: Jeremy Ernst

    def __init__(self, mainUI):

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.mainUI = mainUI
        self.rigData = []
        self.warnings = 0
        self.errors = 0

        # build the UI
        if cmds.window("ART_RigHistWin", exists=True):
            cmds.deleteUI("ART_RigHistWin", wnd=True)

        self.buildUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        # Original Author: Jeremy Ernst

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.mainUI)

        self.style = interfaceUtils.get_style_sheet("artv2_style")

        self.mainWin.setStyleSheet(self.style)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # set qt object name
        self.mainWin.setObjectName("ART_RigHistWin")
        self.mainWin.setWindowTitle("Rig History")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.mainWin.setWindowIcon(window_icon)

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # set size policy
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.mainWin.resize(400, 240)
        self.mainWin.setSizePolicy(mainSizePolicy)
        self.mainWin.setMinimumSize(QtCore.QSize(400, 240))
        self.mainWin.setMaximumSize(QtCore.QSize(400, 240))

        # create the QFrame for this page
        self.background = QtWidgets.QFrame()
        self.layout.addWidget(self.background)
        self.mainLayout = QtWidgets.QVBoxLayout(self.background)

        # detailed information
        self.infoText = QtWidgets.QTextEdit()
        self.mainLayout.addWidget(self.infoText)
        self.infoText.setMinimumSize(QtCore.QSize(360, 200))
        self.infoText.setMaximumSize(QtCore.QSize(360, 200))
        self.infoText.setReadOnly(True)
        self.infoText.setWordWrapMode(QtGui.QTextOption.WordWrap)

        # show the window
        self.mainWin.show()

        self.getHistory()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getHistory(self):

        characterNode = "ART_RIG_ROOT"
        data = json.loads(cmds.getAttr(characterNode + ".versionNote"))

        for each in data:
            version = each[0]
            info = each[1]
            user = each[2]

            self.infoText.setTextColor(QtGui.QColor(236, 217, 0))
            self.infoText.append("Version #: " + str(version))
            self.infoText.setTextColor(QtGui.QColor(255, 255, 255))
            self.infoText.append("Description: " + info)
            self.infoText.setTextColor(QtGui.QColor(0, 255, 0))
            self.infoText.append("User: " + user + "\n\n")
