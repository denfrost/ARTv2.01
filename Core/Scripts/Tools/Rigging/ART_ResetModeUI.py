from ThirdParty.Qt import QtGui, QtCore, QtWidgets
from functools import partial
import maya.cmds as cmds
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
import os

class ART_ResetMode():
    def __init__(self, mainUI):

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        self.buildResetModeUI(mainUI)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildResetModeUI(self, mainUI):

        if cmds.window("ART_ResetModeWin", exists=True):
            cmds.deleteUI("ART_ResetModeWin", wnd=True)

        # launch a UI to get the name information
        self.resetModeWin = QtWidgets.QMainWindow(mainUI)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.resetModeWin.setWindowIcon(window_icon)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.resetModeWin.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.resetModeWin_mainWidget = QtWidgets.QWidget()
        self.resetModeWin.setCentralWidget(self.resetModeWin_mainWidget)

        # set qt object name
        self.resetModeWin.setObjectName("ART_ResetModeWin")
        self.resetModeWin.setWindowTitle("Reset Modules")

        # create the mainLayout for the rig creator UI
        self.resetModeWin_mainLayout = QtWidgets.QVBoxLayout(self.resetModeWin_mainWidget)
        self.resetModeWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.resetModeWin.resize(400, 250)
        self.resetModeWin.setSizePolicy(mainSizePolicy)
        self.resetModeWin.setMinimumSize(QtCore.QSize(400, 250))
        self.resetModeWin.setMaximumSize(QtCore.QSize(400, 250))

        # create the background image
        self.resetModeWin_frame = QtWidgets.QFrame()
        self.resetModeWin_mainLayout.addWidget(self.resetModeWin_frame)

        # create the layout for the widgets
        self.resetModeWin_widgetLayout = QtWidgets.QHBoxLayout(self.resetModeWin_frame)
        self.resetModeWin_widgetLayout.setContentsMargins(5, 5, 5, 5)

        # add the QListWidget Frame
        self.resetModeWin_moduleListFrame = QtWidgets.QFrame()
        self.resetModeWin_moduleListFrame.setMinimumSize(QtCore.QSize(275, 200))
        self.resetModeWin_moduleListFrame.setMaximumSize(QtCore.QSize(275, 200))
        self.resetModeWin_moduleListFrame.setContentsMargins(20, 0, 20, 0)

        # create the list widget
        self.resetModeWin_moduleList = QtWidgets.QListWidget(self.resetModeWin_moduleListFrame)
        self.resetModeWin_widgetLayout.addWidget(self.resetModeWin_moduleListFrame)
        self.resetModeWin_moduleList.setMinimumSize(QtCore.QSize(265, 200))
        self.resetModeWin_moduleList.setMaximumSize(QtCore.QSize(265, 200))
        self.resetModeWin_moduleList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.resetModeWin_moduleList.setSpacing(3)

        # add the layout for the buttons
        self.resetModeWin_buttonLayoutAll = QtWidgets.QVBoxLayout()
        self.resetModeWin_widgetLayout.addLayout(self.resetModeWin_buttonLayoutAll)
        self.resetModeWin_buttonLayoutAll.setContentsMargins(5, 20, 5, 20)

        # add the selection buttons
        self.resetModeWin_selectionButtonLayout = QtWidgets.QVBoxLayout()
        self.resetModeWin_buttonLayoutAll.addLayout(self.resetModeWin_selectionButtonLayout)
        self.resetModeWin_selectAllButton = QtWidgets.QPushButton("Select All")
        self.resetModeWin_selectAllButton.setMinimumSize(QtCore.QSize(115, 25))
        self.resetModeWin_selectAllButton.setMaximumSize(QtCore.QSize(115, 25))
        self.resetModeWin_selectionButtonLayout.addWidget(self.resetModeWin_selectAllButton)
        self.resetModeWin_selectAllButton.clicked.connect(self.resetModeWin_moduleList.selectAll)
        self.resetModeWin_selectAllButton.setObjectName("settings")

        self.resetModeWin_selectNoneButton = QtWidgets.QPushButton("Clear Selection")
        self.resetModeWin_selectNoneButton.setMinimumSize(QtCore.QSize(115, 25))
        self.resetModeWin_selectNoneButton.setMaximumSize(QtCore.QSize(115, 25))
        self.resetModeWin_selectionButtonLayout.addWidget(self.resetModeWin_selectNoneButton)
        self.resetModeWin_selectNoneButton.clicked.connect(self.resetModeWin_moduleList.clearSelection)
        self.resetModeWin_selectNoneButton.setObjectName("settings")

        # spacer
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.resetModeWin_selectionButtonLayout.addItem(spacerItem)

        # add the buttons for reset settings and reset transforms
        self.resetModeWin_resetSettings = QtWidgets.QPushButton("Reset Settings")
        self.resetModeWin_resetSettings.setMinimumSize(QtCore.QSize(115, 25))
        self.resetModeWin_resetSettings.setMaximumSize(QtCore.QSize(115, 25))
        self.resetModeWin_selectionButtonLayout.addWidget(self.resetModeWin_resetSettings)
        self.resetModeWin_resetSettings.clicked.connect(partial(self.resetMode_resetSettings))
        self.resetModeWin_resetSettings.setObjectName("settings")

        self.resetModeWin_resetXforms = QtWidgets.QPushButton("Reset Xforms")
        self.resetModeWin_resetXforms.setMinimumSize(QtCore.QSize(115, 25))
        self.resetModeWin_resetXforms.setMaximumSize(QtCore.QSize(115, 25))
        self.resetModeWin_selectionButtonLayout.addWidget(self.resetModeWin_resetXforms)
        self.resetModeWin_resetXforms.clicked.connect(partial(self.resetMode_resetXformsUI))
        self.resetModeWin_resetXforms.setObjectName("settings")

        # populate the list widget
        modules = utils.returnRigModules()
        for module in modules:
            moduleName = cmds.getAttr(module + ".moduleName")
            self.resetModeWin_moduleList.addItem(moduleName)

        # show the window
        self.resetModeWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetMode_resetSettings(self):

        selected = self.resetModeWin_moduleList.selectedItems()
        items = []
        for each in selected:
            items.append(each.text())
        for each in self.mainUI.moduleInstances:
            name = each.name
            if name in items:
                each.resetSettings()

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def resetMode_resetXformsUI(self):

        # if nothing in the list is selected, return
        if self.resetModeWin_moduleList.selectedItems() == []:
            return

        # if window exists, delete first
        if cmds.window("ART_ResetXformsModeWin", exists=True):
            cmds.deleteUI("ART_ResetXformsModeWin", wnd=True)

        # launch a UI to get the name information
        self.resetXformsWin = QtWidgets.QMainWindow(self.mainUI)

        self.resetXformsWin.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.resetXformsWin_mainWidget = QtWidgets.QWidget()
        self.resetXformsWin.setCentralWidget(self.resetXformsWin_mainWidget)

        # set qt object name
        self.resetXformsWin.setObjectName("ART_ResetXformsModeWin")
        self.resetXformsWin.setWindowTitle("Reset Transformations")

        # create the mainLayout for the rig creator UI
        self.resetXformsWin_mainLayout = QtWidgets.QVBoxLayout(self.resetXformsWin_mainWidget)
        self.resetXformsWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.resetXformsWin.resize(300, 100)
        self.resetXformsWin.setSizePolicy(mainSizePolicy)
        self.resetXformsWin.setMinimumSize(QtCore.QSize(300, 100))
        self.resetXformsWin.setMaximumSize(QtCore.QSize(300, 100))

        # create the background
        self.resetXformsWin_frame = QtWidgets.QFrame()
        self.resetXformsWin_mainLayout.addWidget(self.resetXformsWin_frame)

        # create the layout for the widgets
        self.resetXformsWin_widgetLayout = QtWidgets.QVBoxLayout(self.resetXformsWin_frame)
        self.resetXformsWin_widgetLayout.setContentsMargins(5, 5, 5, 5)
        self.resetXformsWin_widgetLayoutRow = QtWidgets.QHBoxLayout(self.resetXformsWin_frame)
        self.resetXformsWin_widgetLayout.addLayout(self.resetXformsWin_widgetLayoutRow)

        # add the 3 buttons for translate, rotate, scale



        self.resetXformsWin_transCB = QtWidgets.QPushButton("Translate")
        self.resetXformsWin_widgetLayoutRow.addWidget(self.resetXformsWin_transCB)
        self.resetXformsWin_transCB.setCheckable(True)
        self.resetXformsWin_transCB.setChecked(True)

        self.resetXformsWin_rotCB = QtWidgets.QPushButton("Rotate")
        self.resetXformsWin_widgetLayoutRow.addWidget(self.resetXformsWin_rotCB)
        self.resetXformsWin_rotCB.setCheckable(True)
        self.resetXformsWin_rotCB.setChecked(True)

        self.resetXformsWin_scaleCB = QtWidgets.QPushButton("Scale")
        self.resetXformsWin_widgetLayoutRow.addWidget(self.resetXformsWin_scaleCB)
        self.resetXformsWin_scaleCB.setCheckable(True)
        self.resetXformsWin_scaleCB.setChecked(True)

        # Create the Reset Transforms button
        self.resetXformsWin_resetXformButton = QtWidgets.QPushButton("Reset Transformations")
        self.resetXformsWin_widgetLayout.addWidget(self.resetXformsWin_resetXformButton)
        self.resetXformsWin_resetXformButton.setMinimumSize(QtCore.QSize(290, 40))
        self.resetXformsWin_resetXformButton.setMaximumSize(QtCore.QSize(290, 40))
        self.resetXformsWin_resetXformButton.clicked.connect(self.resetMode_resetXforms)
        self.resetXformsWin_resetXformButton.setProperty("boldFont", True)

        # show window
        self.resetXformsWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetMode_resetXforms(self):

        translate = self.resetXformsWin_transCB.isChecked()
        rotate = self.resetXformsWin_rotCB.isChecked()
        scale = self.resetXformsWin_scaleCB.isChecked()

        selected = self.resetModeWin_moduleList.selectedItems()
        items = []
        for each in selected:
            items.append(each.text())
        for each in self.mainUI.moduleInstances:
            name = each.name
            if name in items:
                each.resetTransforms(translate, rotate, scale, name)
