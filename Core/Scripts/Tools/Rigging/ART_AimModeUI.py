"""
Author: Jeremy Ernst
"""

from functools import partial
import os
import maya.cmds as cmds

import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_AimMode():
    """
    This class creates a tool that allows a rigger to toggle aim mode for a given selection of modules. Aim mode
    ensures that the parent joints in a joint mover are always aiming at their children.

    This tool can be called from the toolbar on the Rig Creator UI from the following button:
        .. image:: /images/aimModeButton.png

    The full interface looks like this:
        .. image:: /images/aimMode.png

    """

    def __init__(self, mainUI):
        """
        Instantiates the class, getting the QSettings for the tool, and building the Aim Mode interface.

        :param mainUI: The instance of the Rig Creator UI this tool was called from.

        """

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        self.buildAimModeUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildAimModeUI(self):
        """
        Builds the Aim Mode interface, finding all modules that have the ability to aim, and listing those modules
        as well as their current aim status.

        """

        if cmds.window("ART_AimModeWin", exists=True):
            cmds.deleteUI("ART_AimModeWin", wnd=True)

        # launch a UI to get the name information
        self.aimModeWin = QtWidgets.QMainWindow(self.mainUI)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.aimModeWin.setWindowIcon(window_icon)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.aimModeWin.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.aimModeWin_mainWidget = QtWidgets.QWidget()
        self.aimModeWin.setCentralWidget(self.aimModeWin_mainWidget)

        # set qt object name
        self.aimModeWin.setObjectName("ART_AimModeWin")
        self.aimModeWin.setWindowTitle("Aim Mode")

        # create the mainLayout for the rig creator UI
        self.aimModeWin_mainLayout = QtWidgets.QVBoxLayout(self.aimModeWin_mainWidget)
        self.aimModeWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.aimModeWin.resize(400, 250)
        self.aimModeWin.setSizePolicy(mainSizePolicy)
        self.aimModeWin.setMinimumSize(QtCore.QSize(400, 250))
        self.aimModeWin.setMaximumSize(QtCore.QSize(400, 250))

        # create the background image
        self.aimModeWin_frame = QtWidgets.QFrame()
        self.aimModeWin_mainLayout.addWidget(self.aimModeWin_frame)

        # create the layout for the widgets
        self.aimModeWin_widgetLayout = QtWidgets.QHBoxLayout(self.aimModeWin_frame)
        self.aimModeWin_widgetLayout.setContentsMargins(5, 5, 5, 5)

        # add the QListWidget Frame
        self.aimModeWin_moduleListFrame = QtWidgets.QFrame()
        self.aimModeWin_moduleListFrame.setMinimumSize(QtCore.QSize(275, 200))
        self.aimModeWin_moduleListFrame.setMaximumSize(QtCore.QSize(275, 200))
        self.aimModeWin_moduleListFrame.setContentsMargins(20, 0, 20, 0)

        # create the list widget
        self.aimModeWin_moduleList = QtWidgets.QListWidget(self.aimModeWin_moduleListFrame)
        self.aimModeWin_widgetLayout.addWidget(self.aimModeWin_moduleListFrame)
        self.aimModeWin_moduleList.setMinimumSize(QtCore.QSize(265, 200))
        self.aimModeWin_moduleList.setMaximumSize(QtCore.QSize(265, 200))
        self.aimModeWin_moduleList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.aimModeWin_moduleList.setSpacing(3)

        # add the layout for the buttons
        self.aimModeWin_buttonLayoutAll = QtWidgets.QVBoxLayout()
        self.aimModeWin_widgetLayout.addLayout(self.aimModeWin_buttonLayoutAll)
        self.aimModeWin_buttonLayoutAll.setContentsMargins(5, 20, 5, 20)

        # add the selection buttons
        self.aimModeWin_selectionButtonLayout = QtWidgets.QVBoxLayout()
        self.aimModeWin_buttonLayoutAll.addLayout(self.aimModeWin_selectionButtonLayout)
        self.aimModeWin_selectAllButton = QtWidgets.QPushButton("Select All")
        self.aimModeWin_selectAllButton.setMinimumSize(QtCore.QSize(115, 25))
        self.aimModeWin_selectAllButton.setMaximumSize(QtCore.QSize(115, 25))
        self.aimModeWin_selectionButtonLayout.addWidget(self.aimModeWin_selectAllButton)
        self.aimModeWin_selectAllButton.clicked.connect(self.aimModeWin_moduleList.selectAll)
        self.aimModeWin_selectAllButton.setObjectName("settings")

        self.aimModeWin_selectNoneButton = QtWidgets.QPushButton("Clear Selection")
        self.aimModeWin_selectNoneButton.setMinimumSize(QtCore.QSize(115, 25))
        self.aimModeWin_selectNoneButton.setMaximumSize(QtCore.QSize(115, 25))
        self.aimModeWin_selectionButtonLayout.addWidget(self.aimModeWin_selectNoneButton)
        self.aimModeWin_selectNoneButton.clicked.connect(self.aimModeWin_moduleList.clearSelection)
        self.aimModeWin_selectNoneButton.setObjectName("settings")

        # spacer
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.aimModeWin_selectionButtonLayout.addItem(spacerItem)

        # add the buttons for reset settings and reset transforms
        self.aimModeWin_turnOnAim = QtWidgets.QPushButton("On")
        self.aimModeWin_turnOnAim.setMinimumSize(QtCore.QSize(115, 25))
        self.aimModeWin_turnOnAim.setMaximumSize(QtCore.QSize(115, 25))
        self.aimModeWin_selectionButtonLayout.addWidget(self.aimModeWin_turnOnAim)
        self.aimModeWin_turnOnAim.setToolTip("Turn on Aim Mode for selected modules.")
        self.aimModeWin_turnOnAim.clicked.connect(partial(self.aimModeUI_Toggle, True))
        self.aimModeWin_turnOnAim.setObjectName("settings")

        self.aimModeWin_turnOffAim = QtWidgets.QPushButton("Off")
        self.aimModeWin_turnOffAim.setMinimumSize(QtCore.QSize(115, 25))
        self.aimModeWin_turnOffAim.setMaximumSize(QtCore.QSize(115, 25))
        self.aimModeWin_selectionButtonLayout.addWidget(self.aimModeWin_turnOffAim)
        self.aimModeWin_turnOffAim.setToolTip("Turn off Aim Mode for selected modules.")
        self.aimModeWin_turnOffAim.clicked.connect(partial(self.aimModeUI_Toggle, False))
        self.aimModeWin_turnOffAim.setObjectName("settings")

        # populate the list widget
        modules = utils.returnRigModules()
        for module in modules:
            # get module name
            moduleName = cmds.getAttr(module + ".moduleName")

            # figure out if the module supports aimMode
            canAim = False
            if cmds.objExists(module + ".canAim"):
                canAim = cmds.getAttr(module + ".canAim")

                # see if it is currently in aimMode
                aimMode = cmds.getAttr(module + ".aimMode")

            # if it does, add it to the listwidget
            if canAim:

                # font
                headerFont = QtGui.QFont()
                headerFont.setPointSize(10)
                headerFont.setBold(True)

                # create the listWidgetItem
                pixmap = QtGui.QPixmap(10, 10)
                pixmap.fill(QtGui.QColor(67, 155, 98))
                icon = QtGui.QIcon(pixmap)

                pixmapOff = QtGui.QPixmap(10, 10)
                pixmapOff.fill(QtGui.QColor(155, 74, 67))
                iconOff = QtGui.QIcon(pixmapOff)

                item = QtWidgets.QListWidgetItem(iconOff, moduleName)
                item.setFont(headerFont)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setData(QtCore.Qt.UserRole, [icon, iconOff])

                if aimMode:
                    item.setIcon(icon)

                self.aimModeWin_moduleList.addItem(item)

        # show the window
        self.aimModeWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def aimModeUI_Toggle(self, state):
        """
        Calls on each selected module's aimMode function and sets the aimMode based on the passed in state.

        :param state: Whether to turn aim mode on or off.

        """

        selected = self.aimModeWin_moduleList.selectedItems()
        items = []

        for each in selected:
            items.append(each.text())
            if state:
                each.setIcon(each.data(QtCore.Qt.UserRole)[0])
            if not state:
                each.setIcon(each.data(QtCore.Qt.UserRole)[1])

        # call on each selected module's aimMode function
        for each in self.mainUI.moduleInstances:
            name = each.name
            if name in items:
                each.aimMode(state)

        # clear selection
        self.aimModeWin_moduleList.clearSelection()
