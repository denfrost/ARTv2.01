from ThirdParty.Qt import QtGui, QtCore, QtWidgets
from functools import partial
import maya.cmds as cmds
import os
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


class ART_PinModules():
    def __init__(self, mainUI):

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        self.buildUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):

        if cmds.window("ART_PinModulesWin", exists=True):
            cmds.deleteUI("ART_PinModulesWin", wnd=True)

        # launch a UI to get the name information
        self.window = QtWidgets.QMainWindow(self.mainUI)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.window.setWindowIcon(window_icon)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.window.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.mainWidget)

        # set qt object name
        self.window.setObjectName("ART_PinModulesWin")
        self.window.setWindowTitle("Pin Modules")

        # create the mainLayout for the rig creator UI
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.window.resize(400, 250)
        self.window.setSizePolicy(mainSizePolicy)
        self.window.setMinimumSize(QtCore.QSize(400, 250))
        self.window.setMaximumSize(QtCore.QSize(400, 250))

        # create the background image
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.widgetLayout = QtWidgets.QHBoxLayout(self.frame)
        self.widgetLayout.setContentsMargins(5, 5, 5, 5)

        # left side == list of modules in scene. for each item in list, will do something similar to aim mode,
        # where we will toggle an icon for pin state
        self.moduleList = QtWidgets.QListWidget()
        self.widgetLayout.addWidget(self.moduleList)
        self.moduleList.setMinimumSize(QtCore.QSize(265, 200))
        self.moduleList.setMaximumSize(QtCore.QSize(265, 200))
        self.moduleList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.moduleList.setSpacing(3)

        # right side layout == select all, clear selection, Pin Selected buttons
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.widgetLayout.addLayout(self.buttonLayout)
        self.buttonLayout.setContentsMargins(5, 20, 5, 20)

        # add the selection buttons
        self.selectAllButton = QtWidgets.QPushButton("Select All")
        self.selectAllButton.setMinimumSize(QtCore.QSize(115, 25))
        self.selectAllButton.setMaximumSize(QtCore.QSize(115, 25))
        self.buttonLayout.addWidget(self.selectAllButton)
        self.selectAllButton.clicked.connect(self.moduleList.selectAll)
        self.selectAllButton.setObjectName("settings")

        self.selectNoneButton = QtWidgets.QPushButton("Clear Selection")
        self.selectNoneButton.setMinimumSize(QtCore.QSize(115, 25))
        self.selectNoneButton.setMaximumSize(QtCore.QSize(115, 25))
        self.buttonLayout.addWidget(self.selectNoneButton)
        self.selectNoneButton.clicked.connect(self.moduleList.clearSelection)
        self.selectNoneButton.setObjectName("settings")

        # spacer
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.buttonLayout.addItem(spacerItem)

        # add the buttons for reset settings and reset transforms
        self.pinBtn = QtWidgets.QPushButton("Pin Selected")
        self.pinBtn.setMinimumSize(QtCore.QSize(115, 25))
        self.pinBtn.setMaximumSize(QtCore.QSize(115, 25))
        self.buttonLayout.addWidget(self.pinBtn)
        self.pinBtn.setToolTip(
            "Pin the selected modules so that parent module movements do not effect the pinned module")
        self.pinBtn.clicked.connect(partial(self.toggleLock, True))
        self.pinBtn.setObjectName("settings")

        self.unpinBtn = QtWidgets.QPushButton("Unpin Selected")
        self.unpinBtn.setMinimumSize(QtCore.QSize(115, 25))
        self.unpinBtn.setMaximumSize(QtCore.QSize(115, 25))
        self.buttonLayout.addWidget(self.unpinBtn)
        self.unpinBtn.setToolTip("Unpin modules to resume normal module behavior")
        self.unpinBtn.clicked.connect(partial(self.toggleLock, False))
        self.unpinBtn.setObjectName("settings")

        # populate the list widget
        modules = utils.returnRigModules()
        for module in modules:
            # get module name
            moduleName = cmds.getAttr(module + ".moduleName")

            # font
            headerFont = QtGui.QFont()
            headerFont.setPointSize(10)
            headerFont.setBold(True)

            # create the listWidgetItem
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/locked2.png"))
            iconOff = QtGui.QIcon(os.path.join(self.iconsPath, "System/unlocked.png"))

            item = QtWidgets.QListWidgetItem(iconOff, "    " + moduleName)
            item.setFont(headerFont)
            item.setData(QtCore.Qt.UserRole, [icon, iconOff])

            pinState = cmds.getAttr(module + ".pinned")
            if pinState:
                item.setIcon(icon)

            self.moduleList.addItem(item)

        # show the window
        self.window.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleLock(self, state):

        selected = self.moduleList.selectedItems()
        items = []

        for each in selected:
            items.append(each.text())

            if state:
                each.setIcon(each.data(QtCore.Qt.UserRole)[0])

                for inst in self.mainUI.moduleInstances:
                    name = inst.name
                    if each.text().strip() == name:
                        networkNode = inst.returnNetworkNode
                        inst.pinModule(True)
                        cmds.setAttr(networkNode + ".pinned", lock=False)
                        cmds.setAttr(networkNode + ".pinned", True, lock=True)

            if not state:
                each.setIcon(each.data(QtCore.Qt.UserRole)[1])

                for inst in self.mainUI.moduleInstances:
                    name = inst.name
                    if each.text().strip() == name:
                        networkNode = inst.returnNetworkNode
                        inst.pinModule(False)
                        cmds.setAttr(networkNode + ".pinned", lock=False)
                        cmds.setAttr(networkNode + ".pinned", False, lock=True)

        # clear selection
        self.moduleList.clearSelection()
