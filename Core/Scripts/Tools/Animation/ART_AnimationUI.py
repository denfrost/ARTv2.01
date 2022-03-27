"""
Author: Jeremy Ernst
"""

# import statements
import json
import os
import weakref
from functools import partial

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import ART_PoseLibrary as apl

reload(interfaceUtils)

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


def getMainWindow():
    """
    Get Maya's window as a QWidget and return the item in memory.

    :return: a QWidget of Maya's window

    """

    # get maya's window as QWidget
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    # pyside QMainWindow takes in a QWidget rather than QObject
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


class ART_AnimationUI(QtWidgets.QMainWindow):
    """
    This class creates the main animation interface that houses the control picker and the buttons for the animation
    tools. This is the main interface that animators will interact with.

        .. image:: /images/animationUI.png

    """
    _instances = []

    def __init__(self, parent=None):
        """
        Instantiates the class, getting the QSettings, writing the stylesheets, and calling on the method to build
        the interface.

        """

        self.__class__._instances.append(weakref.proxy(self))

        super(ART_AnimationUI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.center = QtCore.QPointF(210.000000, 287.500000)
        self.scale = 1.0
        self.selectionScriptJobs = []

        # assign close event
        self.closeEvent = self.closeEvent

        # build the UI
        self.buildUI()

        # if more than 1 character, darken inactive character tabs
        self.changeTabImage()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        """
        Builds the animation UI that houses the area for control pickers and a sidebar for animation tools.

        """

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("mid")
        self.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        # load stylesheets
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.tabStyle = interfaceUtils.get_style_sheet("small_tabs")

        self.setStyleSheet(self.style)

        self.setMinimumSize(QtCore.QSize(520, 400))
        self.setMaximumSize(QtCore.QSize(520, 750))
        self.resize(520, 750)

        # set qt object name
        self.setObjectName("pyART_AnimTools_Win")
        self.setWindowTitle("Animation Tools")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # =======================================================================
        # #create the menu bar
        # =======================================================================
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setMaximumHeight(20)
        self.layout.addWidget(self.menuBar)

        # =======================================================================
        # #create the picker toolbar layout
        # =======================================================================
        self.toolFrame = QtWidgets.QFrame()
        self.toolFrame.setObjectName("light")
        self.toolFrame.setMinimumHeight(50)
        self.toolFrame.setMaximumHeight(50)

        self.layout.addWidget(self.toolFrame)
        self.toolbarLayout = QtWidgets.QHBoxLayout(self.toolFrame)
        self.toolbarLayout.setDirection(QtWidgets.QBoxLayout.RightToLeft)
        self.toolbarLayout.addStretch(0)
        self.toolbarLayout.setSpacing(4)

        # =======================================================================
        # #picker toolbar buttons
        # =======================================================================

        self.editPickerBtn = QtWidgets.QPushButton("Edit")
        self.editPickerBtn.setMinimumSize(QtCore.QSize(70, 30))
        self.editPickerBtn.setMaximumSize(QtCore.QSize(70, 30))
        self.toolbarLayout.addWidget(self.editPickerBtn)
        self.editPickerBtn.setEnabled(False)
        self.editPickerBtn.setObjectName("settings")
        self.editPickerBtn.clicked.connect(self.editPicker)
        self.editPickerBtn.setToolTip("Make module pickers editable (move, scale, rotate)")

        self.createPickerBtn = QtWidgets.QPushButton("Create")
        self.createPickerBtn.setMinimumSize(QtCore.QSize(70, 30))
        self.createPickerBtn.setMaximumSize(QtCore.QSize(70, 30))
        self.createPickerBtn.setObjectName("settings")
        self.createPickerBtn.setToolTip("Create a new picker for the given character.")

        self.toolbarLayout.addWidget(self.createPickerBtn)
        self.createPickerBtn.clicked.connect(self.createNewPicker)

        self.removeModBtn = QtWidgets.QPushButton()
        self.removeModBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.removeModBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/removeModule.png"))
        self.removeModBtn.setIconSize(QtCore.QSize(30, 30))
        self.removeModBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.removeModBtn)
        self.removeModBtn.setEnabled(False)
        self.removeModBtn.setObjectName("tool")
        self.removeModBtn.clicked.connect(partial(self.removeModuleFromPickerUI))
        self.removeModBtn.setToolTip("Remove a module's picker from the canvas.")

        self.moveModBtn = QtWidgets.QPushButton()
        self.moveModBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.moveModBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/movePicker.png"))
        self.moveModBtn.setIconSize(QtCore.QSize(30, 30))
        self.moveModBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.moveModBtn)
        self.moveModBtn.setEnabled(False)
        self.moveModBtn.setObjectName("tool")
        self.moveModBtn.clicked.connect(partial(self.movePickerToTab))
        self.moveModBtn.setToolTip("Move a picker from one tab to another.")

        self.moduleListBtn = QtWidgets.QPushButton()
        self.moduleListBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.moduleListBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/moduleList.png"))
        self.moduleListBtn.setIconSize(QtCore.QSize(30, 30))
        self.moduleListBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.moduleListBtn)
        self.moduleListBtn.setEnabled(False)
        self.moduleListBtn.setObjectName("tool")
        self.moduleListBtn.clicked.connect(partial(self.addModuleToPickerUI))
        self.moduleListBtn.setToolTip("Add a module's picker to the current canvas.")

        # background image button
        self.backgroundImgBtn = QtWidgets.QPushButton()
        self.backgroundImgBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.backgroundImgBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/background.png"))
        self.backgroundImgBtn.setIconSize(QtCore.QSize(30, 30))
        self.backgroundImgBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.backgroundImgBtn)
        self.backgroundImgBtn.setEnabled(False)
        self.backgroundImgBtn.setObjectName("tool")
        self.backgroundImgBtn.setToolTip("Change the background of the current picker tab.")
        self.backgroundImgBtn.clicked.connect(partial(self.changeBackground))

        # background image button
        self.miscButton = QtWidgets.QPushButton()
        self.miscButton.setMinimumSize(QtCore.QSize(30, 30))
        self.miscButton.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/add.png"))
        self.miscButton.setIconSize(QtCore.QSize(30, 30))
        self.miscButton.setIcon(icon)
        self.toolbarLayout.addWidget(self.miscButton)
        self.miscButton.setEnabled(False)
        self.miscButton.setObjectName("tool")
        self.miscButton.setToolTip("Add a custom button or label to the picker.")
        self.miscButton.clicked.connect(partial(self.addCustomObjectToPicker))

        buttonGrp = QtWidgets.QButtonGroup(self.toolbarLayout)
        buttonGrp.setExclusive(True)

        self.normalSelectButton = QtWidgets.QPushButton()
        self.normalSelectButton.setMinimumSize(QtCore.QSize(30, 30))
        self.normalSelectButton.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/normalSelect_On.png"))
        self.normalSelectButton.setIconSize(QtCore.QSize(30, 30))
        self.normalSelectButton.setIcon(icon)
        self.toolbarLayout.addWidget(self.normalSelectButton)
        self.normalSelectButton.setCheckable(True)
        self.normalSelectButton.setObjectName("tool")
        self.normalSelectButton.setChecked(True)
        self.normalSelectButton.setToolTip("Change picker selection mode to normal selection")
        self.normalSelectButton.clicked.connect(self.toggleDragState)

        self.dragSelectButton = QtWidgets.QPushButton()
        self.dragSelectButton.setMinimumSize(QtCore.QSize(30, 30))
        self.dragSelectButton.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/dragSelect.png"))
        self.dragSelectButton.setIconSize(QtCore.QSize(30, 30))
        self.dragSelectButton.setIcon(icon)
        self.toolbarLayout.addWidget(self.dragSelectButton)
        self.dragSelectButton.setCheckable(True)
        self.dragSelectButton.setObjectName("tool")
        self.dragSelectButton.setToolTip("Change picker selection mode to drag selection")
        self.dragSelectButton.clicked.connect(self.toggleDragState)

        self.commentButton = QtWidgets.QPushButton()
        self.commentButton.setMinimumSize(QtCore.QSize(30, 30))
        self.commentButton.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/commentMode.png"))
        self.commentButton.setIconSize(QtCore.QSize(30, 30))
        self.commentButton.setIcon(icon)
        self.toolbarLayout.addWidget(self.commentButton)
        self.commentButton.setCheckable(True)
        self.commentButton.setObjectName("tool")
        self.commentButton.setToolTip("Add Comment Box Mode")
        self.commentButton.clicked.connect(self.toggleDragState)

        buttonGrp.addButton(self.normalSelectButton)
        buttonGrp.addButton(self.dragSelectButton)
        buttonGrp.addButton(self.commentButton)

        # self.toolbarLayout.addSpacerItem(QtWidgets.QSpacerItem(20, 0))

        self.saveTemplateBtn = QtWidgets.QPushButton()
        self.saveTemplateBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.saveTemplateBtn.setMaximumSize(QtCore.QSize(30, 30))
        self.toolbarLayout.addWidget(self.saveTemplateBtn)
        self.saveTemplateBtn.setObjectName("save")
        self.saveTemplateBtn.clicked.connect(self.savePicker)
        self.saveTemplateBtn.setToolTip("Save a picker file")

        self.loadTemplateBtn = QtWidgets.QPushButton()
        self.loadTemplateBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.loadTemplateBtn.setMaximumSize(QtCore.QSize(30, 30))
        self.toolbarLayout.addWidget(self.loadTemplateBtn)
        self.loadTemplateBtn.setObjectName("load")
        self.loadTemplateBtn.clicked.connect(self.loadPicker)
        self.loadTemplateBtn.setToolTip("Load a picker file")

        # =======================================================================
        # #create the horizontal layout, with the left column giving us the picker canvas area,
        # and the right a toolbar for animation tools
        # =======================================================================
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.mainLayout)

        self.mainLeftColumnLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.mainLeftColumnLayout)

        self.mainRightColumnLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.mainRightColumnLayout)

        # =======================================================================
        # #left column - picker canvas
        # =======================================================================

        """
        the picker canvas will consist of a tab layout at the top, one per character in scene,
        and in each of those tabs, another tab layout to hold the pages of the picker
        """

        self.pickerMainWidget = QtWidgets.QFrame()
        self.mainLeftColumnLayout.addWidget(self.pickerMainWidget)

        self.pickerMainWidget.setMinimumSize(470, 700)
        self.pickerMainWidget.setMaximumSize(470, 700)

        self.characterTabs = QtWidgets.QTabWidget(self.pickerMainWidget)
        self.characterTabs.setObjectName("border")
        self.characterTabs.setMinimumSize(440, 670)
        self.characterTabs.setMaximumSize(440, 670)
        self.characterTabs.setIconSize(QtCore.QSize(60, 60))

        # look for characters in scene to create character tabs
        charactersFound = self.findCharacters()
        self.characterTabs.currentChanged.connect(partial(self.changeTabImage))

        if not charactersFound:
            cmds.warning("No characters found in scene.")

        # =======================================================================
        # #right column - toolbar
        # =======================================================================

        self.mainRightColumnLayout.addSpacerItem(QtWidgets.QSpacerItem(45, 68))

        self.animToolsFrame = QtWidgets.QFrame()
        self.animToolsFrame.setObjectName("light")
        self.mainRightColumnLayout.addWidget(self.animToolsFrame)
        self.animToolsFrame.setMinimumSize(50, 601)
        self.animToolsFrame.setMaximumSize(50, 601)

        self.animToolsLayout = QtWidgets.QVBoxLayout(self.animToolsFrame)
        self.animToolsLayout.setContentsMargins(3, 0, 10, 0)

        self.animToolsLayout.addSpacerItem(QtWidgets.QSpacerItem(45, 10))

        # Select Controls
        self.selectCtrlBtn = QtWidgets.QPushButton()
        self.selectCtrlBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.selectCtrlBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.selectCtrlBtn)
        self.selectCtrlBtn.setObjectName("animselect")
        self.selectCtrlBtn.clicked.connect(self.selectAllCtrls)

        image = utils.returnNicePath(self.iconsPath, "Help/tooltips/select_rig_controls.png")
        tooltip = "<img src = \"" + image + "\">"
        self.selectCtrlBtn.setToolTip(tooltip)

        # Selection Set
        self.selectSetBtn = QtWidgets.QPushButton()
        self.selectSetBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.selectSetBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.selectSetBtn)
        self.selectSetBtn.setObjectName("animselectset")
        self.selectSetBtn.clicked.connect(self.selectionSets)
        text = "Selection Sets Tool. Create, modify, and use selection sets. Shift + LMB on a selection set will" \
               " append the selection."
        self.selectSetBtn.setToolTip(text)

        # Reset Module
        self.resetModuleBtn = QtWidgets.QPushButton()
        self.resetModuleBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.resetModuleBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.resetModuleBtn)
        self.resetModuleBtn.setObjectName("animreset")
        self.resetModuleBtn.clicked.connect(self.resetRigCtrls)
        text = "Launches the reset rig controls tool. Reset multiple modules' rig control transformations quickly" \
               " with this tool."
        self.resetModuleBtn.setToolTip(text)

        # Export Motion
        self.exportMotionBtn = QtWidgets.QPushButton()
        self.exportMotionBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.exportMotionBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.exportMotionBtn)
        self.exportMotionBtn.setObjectName("animexport")
        self.exportMotionBtn.clicked.connect(self.exportMotion)
        text = "Launches the export motion tool. Use this to export your animation into game-engine ready FBX data."
        self.exportMotionBtn.setToolTip(text)

        # Import Motion
        self.importMotionBtn = QtWidgets.QPushButton()
        self.importMotionBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.importMotionBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.importMotionBtn)
        self.importMotionBtn.setObjectName("animimport")
        self.importMotionBtn.clicked.connect(self.importMotion)
        text = "Launches the import motion tool. Imports FBX data onto the rig controls. Useful for working with mocap."
        self.importMotionBtn.setToolTip(text)

        # Match Over Frame Range
        self.matchRangeBtn = QtWidgets.QPushButton()
        self.matchRangeBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.matchRangeBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.matchRangeBtn)
        self.matchRangeBtn.setObjectName("animmatch")
        self.matchRangeBtn.clicked.connect(self.matchOverRange)
        text = "Launches the match over frame range tool. Allows you to match rigs (FK, IK) to each other over a" \
               " frame range."
        self.matchRangeBtn.setToolTip(text)

        # Space Switcher
        self.spaceSwitcherBtn = QtWidgets.QPushButton()
        self.spaceSwitcherBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.spaceSwitcherBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.spaceSwitcherBtn)
        self.spaceSwitcherBtn.setObjectName("animspace")
        self.spaceSwitcherBtn.clicked.connect(self.spaceSwitcher)
        text = "Launches the space switcher tool. Create new spaces, switch to spaces, and bake spaces using this tool."
        self.spaceSwitcherBtn.setToolTip(text)

        # Pose Library
        self.poseLibBtn = QtWidgets.QPushButton()
        self.poseLibBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.poseLibBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.poseLibBtn)
        self.poseLibBtn.setObjectName("animpose")
        self.poseLibBtn.clicked.connect(self.poseLibrary)
        self.poseLibBtn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.poseLibBtn.customContextMenuRequested.connect(partial(self._mirror_context_menu, self.poseLibBtn))
        image = utils.returnNicePath(self.iconsPath, "Help/tooltips/launch_pose_library.png")
        tooltip = "<img src = \"" + image + "\">"
        self.poseLibBtn.setToolTip(tooltip)

        # Rig Settings
        self.rigSettingsBtn = QtWidgets.QPushButton()
        self.rigSettingsBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.rigSettingsBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.animToolsLayout.addWidget(self.rigSettingsBtn)
        self.rigSettingsBtn.setObjectName("animsettings")
        self.rigSettingsBtn.clicked.connect(self.rigSettings)
        text = "Launches a UI for managing rig settings. There are hotkeys available for selecting rig settings and" \
               " toggling the rig settings UI."
        self.rigSettingsBtn.setToolTip(text)

        self.animToolsLayout.addSpacerItem(QtWidgets.QSpacerItem(75, 600))

        # restore window position
        settings = QtCore.QSettings("ARTv2", "AnimationUI")
        self.restoreGeometry(settings.value("geometry"))

        return

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "AnimationUI")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setButtonIcon(self, movie, *args):
        """
        Sets the icon of the matchRangeBtn to the next frame in the passed in movie. Note: This was a test function
        to see if animated gifs could be used as buttons.

        :param movie: The movie whose frame to change.

        """

        self.matchRangeBtn.setIcon(QtGui.QIcon(movie.currentPixmap()))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findCharacters(self):
        """
        Finds all assets in the scene built with ARTv2, and creates a picker tab for each one in the animation UI.

        """

        allNodes = cmds.ls(type="network")
        characterNodes = []
        for node in allNodes:
            attrs = cmds.listAttr(node)
            if "rigModules" in attrs:
                characterNodes.append(node)

        if len(characterNodes) == 0:
            return False

        else:
            # go through each node, find the character name, the namespace on the node, and the picker attribute
            for node in characterNodes:
                try:
                    namespace = cmds.getAttr(node + ".namespace")
                except:
                    namespace = cmds.getAttr(node + ".name")

                picker = False

                if cmds.objExists(node + ".pickerFile"):
                    pickerFile = cmds.getAttr(node + ".pickerFile")
                    picker = True

                # create the tab for the given namespace
                characterWidget = QtWidgets.QFrame()
                characterWidget.setObjectName("dark")
                characterWidget.setProperty("charNode", node)
                characterWidget.setMinimumSize(442, 720)
                characterWidget.setMaximumSize(442, 720)
                characterWidget.setProperty("namespace", namespace)

                # add the icon found on the node's icon path attribute to the tab
                iconPath = cmds.getAttr(node + ".iconPath")
                iconPath = utils.returnNicePath(self.projectPath, iconPath)
                icon = QtGui.QIcon(iconPath)

                self.characterTabs.addTab(characterWidget, icon, "")
                index = self.characterTabs.indexOf(characterWidget)
                self.characterTabs.setTabToolTip(index, namespace)
                self.characterTabs.setProperty("tab_" + str(index), icon)

                # if a picker file existed, load it. Otherwise, display an image telling the user to either
                # load a file or create a picker
                frame = QtWidgets.QFrame(characterWidget)
                frame.setMinimumSize(442, 720)
                frame.setMaximumSize(442, 720)
                frame.setStyleSheet(
                    "background-image: url(" + utils.returnNicePath(self.iconsPath, "System/backgrounds/noPicker.png") + ");")

                layout = QtWidgets.QVBoxLayout(frame)
                layout.setContentsMargins(20, 150, 20, 241)

                # add help gif
                movie_screen = QtWidgets.QLabel(frame)
                movie_screen.setStyleSheet("background: transparent;")
                layout.addWidget(movie_screen)
                moviePath = utils.returnNicePath(self.iconsPath, "Help/createPicker.gif")
                movie = QtGui.QMovie(moviePath, QtCore.QByteArray())
                movie.setCacheMode(QtGui.QMovie.CacheAll)
                movie.setSpeed(100)
                movie_screen.setMovie(movie)

                movie.start()

                if picker:
                    self.characterTabs.setCurrentIndex(index)
                    self.loadPicker(utils.returnFriendlyPath(pickerFile))

            return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createNewPicker(self, bypass=False):
        """
        Create a new control picker for the given character tab. This will remove the help gif and replace it with a
        blank canvas that module pickers can be added to (using ART_AddModuleToCanvas).

        :param bypass:  Whether or not to bypass the QMessageBox confirming the creation of a new picker.
                        This is used when loading a picker from file. bypass will be set to True.

        :return: returns the QTabWidget for this character's picker.

        .. seealso:: ART_AddModuleToCanvas

        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        closeWidget = widget.children()

        # get the tab text
        character = self.characterTabs.tabToolTip(index)

        if not bypass:
            # display a message confirming new picker creation for given character
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Create a New Picker for " + str(character) + " ?")
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            msgBox.addButton("Cancel", QtWidgets.QMessageBox.NoRole)
            ret = msgBox.exec_()

            # if the user selected "Yes", delete the old widget
            if ret == 0:
                for each in closeWidget:
                    each.setParent(None)
                    each.close()
                    self.update()

            if ret == 1:
                return

        else:
            for each in closeWidget:
                each.setParent(None)
                each.close()
                self.update()

        # now add a new tab widget to our character tabs, with a new tab named "Main"
        pickerTabs = QtWidgets.QTabWidget(widget)
        pickerTabs.setStyleSheet(self.tabStyle)
        pickerTabs.currentChanged.connect(self.pickerTabChange)

        # add 'add tab' button
        addTabBtn = QtWidgets.QPushButton()
        addTabBtn.setText("+")
        addTabBtn.setMinimumSize(QtCore.QSize(25, 30))
        addTabBtn.setMaximumSize(QtCore.QSize(25, 30))
        addTabBtn.setObjectName("settings")
        addTabBtn.setToolTip("Add Picker Tab")
        addTabBtn.clicked.connect(partial(self.addTab, pickerTabs))
        pickerTabs.setCornerWidget(addTabBtn, QtCore.Qt.TopRightCorner)

        # create the qWidget for this tab of the picker
        pickerCanvas = QtWidgets.QWidget()
        pickerTabs.addTab(pickerCanvas, "Main")

        # create the layout for this page
        pageLayout = QtWidgets.QVBoxLayout(pickerCanvas)

        # create the graphicsView
        gfxView = QtWidgets.QGraphicsView()
        pageLayout.addWidget(gfxView)

        # create the qgraphicsScene
        gfxScene = QtWidgets.QGraphicsScene()
        gfxScene.setSceneRect(0, 0, 418, 540)
        gfxView.setScene(gfxScene)
        gfxView.setDragMode(QtWidgets.QGraphicsView.NoDrag)

        # set background image
        pixmap = QtGui.QPixmap(utils.returnNicePath(self.iconsPath, "System/backgrounds/canvas.png"))
        gfxItem = gfxScene.addPixmap(pixmap)
        gfxItem.setZValue(-20)

        # show the picker tabs
        pickerTabs.show()

        # enable module list button
        self.backgroundImgBtn.setEnabled(True)
        self.moduleListBtn.setEnabled(True)
        self.removeModBtn.setEnabled(True)
        self.miscButton.setEnabled(True)
        self.moveModBtn.setEnabled(True)
        self.normalSelectButton.setEnabled(False)
        self.dragSelectButton.setEnabled(False)

        if not bypass:
            self.addModuleToPickerUI()

        # =======================================================
        # #enable edit button
        # =======================================================
        self.editPickerBtn.setEnabled(True)

        return pickerTabs

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleDragState(self):
        """
        Toggles selection interaction modes within the QGraphicsScene. The three different modes are normal select,
        drag select, and comment box mode. This will set the dragMode of the QGraphicsView to the currently selected
        state, along with switching icons to show selection status.

        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        views = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                selectedTab = tab.currentIndex()

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            views.append(view)

                tab.setCurrentIndex(selectedTab)

        for view in views:
            view.mousePressEvent = partial(self.gfxViewMousePress, view)
            view.mouseMoveEvent = partial(self.gfxViewMouseMove, view)
            view.mouseReleaseEvent = partial(self.gfxViewMouseRelease, view)

        # normal singular select mode
        if self.normalSelectButton.isChecked():
            for view in views:
                view.setDragMode(QtWidgets.QGraphicsView.NoDrag)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/normalSelect_On.png"))
            self.normalSelectButton.setIconSize(QtCore.QSize(30, 30))
            self.normalSelectButton.setIcon(icon)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/dragSelect.png"))
            self.dragSelectButton.setIconSize(QtCore.QSize(30, 30))
            self.dragSelectButton.setIcon(icon)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/commentMode.png"))
            self.commentButton.setIconSize(QtCore.QSize(30, 30))
            self.commentButton.setIcon(icon)

        # drag select mode
        if self.dragSelectButton.isChecked():
            for view in views:
                view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/normalSelect.png"))
            self.normalSelectButton.setIconSize(QtCore.QSize(30, 30))
            self.normalSelectButton.setIcon(icon)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/dragSelect_On.png"))
            self.dragSelectButton.setIconSize(QtCore.QSize(30, 30))
            self.dragSelectButton.setIcon(icon)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/commentMode.png"))
            self.commentButton.setIconSize(QtCore.QSize(30, 30))
            self.commentButton.setIcon(icon)

        # create UE4-style comment box mode
        if self.commentButton.isChecked():
            for view in views:
                view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/normalSelect.png"))
            self.normalSelectButton.setIconSize(QtCore.QSize(30, 30))
            self.normalSelectButton.setIcon(icon)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/dragSelect.png"))
            self.dragSelectButton.setIconSize(QtCore.QSize(30, 30))
            self.dragSelectButton.setIcon(icon)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/commentMode_on.png"))
            self.commentButton.setIconSize(QtCore.QSize(30, 30))
            self.commentButton.setIcon(icon)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def gfxViewMousePress(self, view, event):
        """
        Override event that captures a mouse press when in the passed in QGraphicsView and displays the QRubberBand
        if in drag select or comment box mode.

        :param view: the QGraphicsView to detect mouse press events in.

        """

        if self.dragSelectButton.isChecked():
            self.origin = event.pos()
            self.rubberband = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, view)
            self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rubberband.show()

        if self.commentButton.isChecked():
            self.origin = event.pos()
            self.rubberband = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, view)
            self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rubberband.show()

        QtWidgets.QGraphicsView.mousePressEvent(view, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def gfxViewMouseMove(self, view, event):
        """
        Override event that captures a mouse move when in the passed in QGraphicsView and changes the
        displayed size of the QRubberBand based on the origin position and the current position, drawing a QRect (if
        in drag select or comment box mode.). It also finds any items inside of that QRect (picker buttons, etc).

        :param view: the QGraphicsView to detect mouse move events in and check for items in.

        """

        if self.dragSelectButton.isChecked():
            try:
                self.rubberband.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
                self.itemsInRect = view.items(QtCore.QRect(self.origin, event.pos()).normalized())
            except Exception, e:
                pass

        if self.commentButton.isChecked():
            try:
                self.rubberband.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
                self.itemsInRect = view.items(QtCore.QRect(self.origin, event.pos()).normalized())
            except Exception, e:
                pass
        QtWidgets.QGraphicsView.mouseMoveEvent(view, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def gfxViewMouseRelease(self, view, event):
        """
        Override event that captures a mouse release when in the passed in QGraphicsView and hides the QRubberBand
        if it was visible. If in comment box mode, this release event will also create the comment box with the
        dimensions and position of the start point of the mouse press, and the QRect from the mouse move.

        :param view: the QGraphicsView to detect mouse release events and to add comment boxes to.

        """

        if self.dragSelectButton.isChecked():
            self.rubberband.hide()
            try:
                for item in self.itemsInRect:
                    try:
                        if item.classType == "pickerButton":
                            item.mousePressEventCustom(event)

                    except:
                        pass
            except:
                pass

        if self.commentButton.isChecked():
            self.rubberband.hide()

            geo = self.rubberband.geometry()
            scene = view.scene()
            if geo.width() > 20:
                if geo.height() > 20:
                    box = interfaceUtils.commentBoxItem(geo.x(), geo.y(), geo.width(), geo.height(), scene, view, self)
                    scene.addItem(box)
                    box.setZValue(0)

            self.normalSelectButton.setChecked(True)
            self.toggleDragState()

        QtWidgets.QGraphicsView.mouseReleaseEvent(view, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addTab(self, tabWidget, bypass=False, tabName=None):
        """
        Adds a tab to the QTabWidget for a given character to add more module control pickers to. These are sometimes
        referred to as "canvases".

        :param tabWidget: The QTabWidget to add a tab to.
        :param bypass: If not creating the "Main" tab or loading a picker from file, a tab name must be entered.
        :param tabName: If creating the "Main" tab or loading a picker from file, the name given to the tab that
                        will be created.

        :return: Index of the created tab in the QTabWidget.
        """

        if not bypass:
            tabName, ok = QtWidgets.QInputDialog.getText(self, "Tab Name", "Enter Tab Name:")
        else:
            ok = True
            tabName = tabName
        if ok:
            if tabName != "":
                # create the qWidget for this tab of the picker
                pickerCanvas = QtWidgets.QWidget()
                tabWidget.addTab(pickerCanvas, str(tabName))
                index = tabWidget.indexOf(pickerCanvas)

                # create the layout for this page
                pageLayout = QtWidgets.QVBoxLayout(pickerCanvas)

                # create the graphicsView
                gfxView = QtWidgets.QGraphicsView()
                pageLayout.addWidget(gfxView)

                # create the qgraphicsScene
                gfxScene = QtWidgets.QGraphicsScene()
                gfxScene.setSceneRect(0, 0, 418, 540)
                gfxView.setScene(gfxScene)

                # set background image
                pixmap = QtGui.QPixmap(utils.returnNicePath(self.iconsPath, "System/backgrounds/canvas.png"))
                gfxScene.addPixmap(pixmap)

                return index
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def closeEvent(self, event):
        """
        Closes the interface.
        """

        for instance in self.__class__._instances:
            if cmds.dockControl("pyART_animToolsDock", q=True, exists=True):
                instance.close()

            else:
                if cmds.window("pyART_AnimTools_Win", exists=True):
                    try:
                        instance.close()
                    except ReferenceError:
                        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addCustomObjectToPicker(self):
        import Tools.Animation.ART_AddCustomButton as acb
        acb.run(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addModuleToPickerUI(self):
        """
        Creates an instance of ART_AddModuleToCanvas to bring up that tool, passing in modules valid to add.

        """

        modulesToAdd = self.comparePickerToRig(True, False)
        import Tools.Animation.ART_AddModuleToCanvas as am2c
        am2c.ART_AddModuleToCanvas(self, modulesToAdd)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeModuleFromPickerUI(self):
        """
        Creates an instance of the ART_RemoveModuleFromCanvas tool, passing in modules valid to remove.

        """

        modulesToAdd = self.comparePickerToRig(False, True)
        import Tools.Animation.ART_RemoveModuleFromCanvas as arfc
        arfc.ART_RemoveModuleFromCanvas(self, modulesToAdd)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def movePickerToTab(self):
        """
        Creates an instance of the ART_MovePickerToTabUI tool, passing in all valid module pickers that could be moved.

        """

        modulesToAdd = self.findAllPickerItems()
        import Tools.Animation.ART_MovePickerToTabUI as mp2t
        mp2t.ART_MovePickerToTab(self, modulesToAdd)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pickerTabChange(self):
        """
        Called on when a tab is changed on a given character's picker, if the remove modules from canvas UI is open,
        it will be closed.

        .. todo:: This function could eventually be changed to simply refresh that UI with the new information.

        """

        if cmds.window("pyART_AddToCanvasWIN", exists=True):
            title = cmds.window("pyART_AddToCanvasWIN", q=True, title=True)
            if title == "Remove Module From Canvas":
                cmds.deleteUI("pyART_AddToCanvasWIN", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def editPicker(self):
        """
        Makes all picker items editable again, making them selectable, movable, scalable, and rotatable.

        """

        data = self.getPickerTabs(False)
        comments = self.getComments()
        custom_buttons = self.getCustomButtons()

        self.backgroundImgBtn.setEnabled(True)
        self.moduleListBtn.setEnabled(True)
        self.removeModBtn.setEnabled(True)
        self.moveModBtn.setEnabled(True)
        self.miscButton.setEnabled(True)
        self.normalSelectButton.setEnabled(False)
        self.dragSelectButton.setEnabled(False)

        for each in data:
            item = each.get("item")
            if item is not None:
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
                item.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

        for comment in comments:
            item = comment.get("item")
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

        for custom in custom_buttons:
            item = custom.get("item")
            self.refresh_customData(custom, item)
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
            item.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def refresh_customData(self, data, item):

        child_items = item.childItems()
        for each in child_items:

            if data.get("buttonType") == "selection":
                each.setData(5, data.get("selection"))
                each.setData(7, data.get("style"))
                each.setData(9, data.get("hasLabel"))
                each.setData(10, data.get("labelText"))
                each.setData(11, data.get("labelPosition"))
                if each.data(7) == 0:
                    each.setData(6, data.get("color"))

                if each.data(7) == 1:
                    each.setData(8, data.get("image"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def savePicker(self):
        """
        Save the picker data to a .picker file. The main picker data is actually gathered by self.getPickerTabs,
        self.getComments, and self.getButtonColors.

        .. seealso:: ART_AnimationUI.getPickerTabs, ART_AnimationUI.getComments, ART_AnimationUI.getButtonColors

        """

        # get info from current character tab
        pickerData = self.getPickerTabs(True)
        commentData = self.getComments(True)
        customData = self.getCustomButtons(True)
        buttonData = self.getButtonColors()

        jsonData = {}
        jsonData["pickerData"] = pickerData
        jsonData["commentData"] = commentData
        jsonData["customData"] = customData
        jsonData["buttonData"] = buttonData

        # character name
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        characterNode = widget.property("charNode")

        if not cmds.objExists(characterNode + ".pickerFile"):
            cmds.addAttr(characterNode, ln="pickerFile", dt="string")

        # ask for the file name to give the picker
        startingDir = utils.returnNicePath(self.toolsPath, "Core/Pickers")
        if not os.path.exists(startingDir):
            os.makedirs(startingDir)

        filename = cmds.fileDialog2(fm=0, okc="Save Picker", dir=startingDir, ff="*.picker")
        if filename is not None:
            # create the picker file
            f = open(filename[0], 'w')

            # dump the data with json
            json.dump(jsonData, f, sort_keys=True, indent=4)
            f.close()

            # write picker file location to character node
            pickerFile = utils.returnFriendlyPath(filename[0])
            cmds.setAttr(characterNode + ":.pickerFile", pickerFile, type="string")

            # disable module list button
            self.backgroundImgBtn.setEnabled(False)
            self.moduleListBtn.setEnabled(False)
            self.removeModBtn.setEnabled(False)
            self.miscButton.setEnabled(False)
            self.moveModBtn.setEnabled(False)
            self.normalSelectButton.setEnabled(True)
            self.dragSelectButton.setEnabled(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def comparePickerToRig(self, unused, used):
        """
        Compares the modules that are on the picker to all modules that make up the character.

        :param unused: Whether or not we want a list returned of modules that are not on the picker yet.
        :param used: Whether or not we want a list returned of modules that are on the picker.
        :return: Returns a list of the modules based on either used or unused args.

        """

        # get info from current character tab
        jsonData = self.getPickerTabs(False)

        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        characterNode = widget.property("charNode")

        rigModules = cmds.listConnections(characterNode + ".rigModules")
        returnModules = []
        pickerModules = []

        for data in jsonData:
            pickerModules.append(data.get("module"))

        if unused:
            for module in rigModules:
                if module not in pickerModules:
                    returnModules.append(module)

        if used:
            returnModules = list(set(pickerModules))

        return returnModules

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findAllPickerItems(self):
        """
        Finds all modules on the picker. Used mostly be the load picker function.
        :return: Returns a list of picker data that includes for each item, the module the picker is for, the item in
        memory, and the nice name.

        .. seealso:: ART_AnimationUI.loadPicker
        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        returnData = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            # get all items in the gfxScene
                            itemsInScene = scene.items()

                            for item in itemsInScene:
                                # if we find our top level picker item (the borderItem), get it's data
                                if type(item) == interfaceUtils.pickerBorderItem or item.type() == 3:
                                    module = item.data(QtCore.Qt.UserRole)
                                    niceName = item.data(2)
                                    returnData.append([module, item, niceName])

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def loadPicker(self, filename=None):
        """
        Loads a .picker file and builds the picker according to the file data.
        :param filename: The path of the picker file to gather data from.

        """

        if filename is None:
            startingDir = utils.returnNicePath(self.toolsPath, "Core/Pickers")
            if os.path.exists(startingDir):

                filename = cmds.fileDialog2(fm=1, okc="Load Picker", dir=startingDir, ff="*.picker")
                if filename is not None:
                    filename = filename[0]
        borderItems = []

        print filename
        if os.path.exists(filename):
            # ===============================================================
            # #load the data
            # ===============================================================
            try:
                json_file = open(filename)
                data = json.load(json_file)
                json_file.close()
            except:
                pass

            # ===============================================================
            # #get character node
            # ===============================================================
            tabIndex = self.characterTabs.currentIndex()
            characterWidget = self.characterTabs.widget(tabIndex)
            characterNode = characterWidget.property("charNode")
            characterNodeModules = cmds.listConnections(characterNode + ".rigModules")

            if cmds.objExists(characterNode + ".namespace"):
                namespace = cmds.getAttr(characterNode + ".namespace") + ":"
            else:
                namespace = cmds.getAttr(characterNode + ".name")

            # create new picker
            tabWidget = self.createNewPicker(True)

            # ===============================================================
            # #create all tabs
            # ===============================================================
            existingTabs = []
            subPickers = []
            for i in range(tabWidget.count()):
                tabName = tabWidget.tabText(i)
                existingTabs.append(tabName)

            # ===============================================================
            # #go through data
            # ===============================================================
            subPickers = []
            pickerData = data["pickerData"]

            for item in pickerData:
                module = item.get("module")
                moduleNiceName = item.get("module")
                tab = item.get("tab")
                transforms = item.get("transforms")
                subPicker = item.get("subPicker")
                mirrored = item.get("mirrored")
                path = item.get("path")

                if module is not None:
                    # if there is a namespace (if the add character for animation tool was used):
                    if namespace + module in characterNodeModules:
                        module = namespace + module
                    else:
                        namespace = ""

                if subPicker is True:
                    subPickers.append([module, tab, transforms, mirrored, moduleNiceName])

                if tab not in existingTabs:
                    self.addTab(tabWidget, True, tab)
                    existingTabs.append(tab)

                # ===========================================================
                # #add the picker to the correct tab
                # ===========================================================
                buildPicker = False
                tabChildren = tabWidget.children()

                # get a list of the tabs with their names and index
                tabInfo = {}
                for i in range(len(tabChildren)):
                    tabName = tabWidget.tabText(i)
                    tabInfo[tabName] = i

                # now find a matching entry in that list to our tab variable
                index = tabInfo.get(tab)
                if index is None:
                    index = 0
                # set out tab widget to that index
                tabWidget.setCurrentIndex(index)
                if subPicker is False:
                    buildPicker = True

                # ===========================================================
                # #now that the tab is correct, build the picker for the module
                # ===========================================================
                if buildPicker:
                    scene = self.getCurrentScene()

                    try:
                        # create picker for the given module
                        inst = self.getModuleInst(module)
                        pickerData = inst.pickerUI(self.center, self, module, namespace)
                        picker = pickerData[0]
                        scene.addItem(picker)
                        self.selectionScriptJobs.append(pickerData[2])
                        borderItems.append([picker, moduleNiceName, module])

                        # mirror the module's pickerBorderItem if needed
                        if pickerData[1] is True:
                            picker.setTransformOriginPoint(picker.boundingRect().center())
                            picker.setTransform(
                                QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, picker.boundingRect().width() * 2, 0.0))

                            children = picker.childItems()
                            if children is not None:
                                self.mirrorChildTextItems(children)

                        # set transformations on the picker
                        picker.setTransformOriginPoint(picker.boundingRect().center())
                        picker.setScale(transforms[2])

                        # when loading a picker, set data(1) to be the scale factor that was possibly saved out.
                        picker.setData(1, transforms[2])

                        picker.setTransformOriginPoint(picker.boundingRect().center())
                        picker.setRotation(transforms[1])

                        picker.setPos(QtCore.QPointF(transforms[0][0], transforms[0][1]))

                        picker.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                        picker.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                        picker.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                        picker.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False)

                        # =======================================================
                        # #enable edit button
                        # =======================================================
                        self.editPickerBtn.setEnabled(True)

                        # =======================================================
                        # #disable canvas, move, and remove buttons
                        # =======================================================
                        self.backgroundImgBtn.setEnabled(False)
                        self.moduleListBtn.setEnabled(False)
                        self.removeModBtn.setEnabled(False)
                        self.miscButton.setEnabled(False)
                        self.moveModBtn.setEnabled(False)
                        self.normalSelectButton.setEnabled(True)
                        self.dragSelectButton.setEnabled(True)

                    except Exception, e:
                        cmds.warning(str(e))

                try:
                    if path is not None:

                        widget = tabWidget.widget(index)
                        widgetChildren = widget.children()
                        for child in widgetChildren:
                            if type(child) == QtWidgets.QGraphicsView:
                                gfxView = child

                                if os.path.exists(utils.returnFriendlyPath(path)):

                                    # set background image
                                    pixmap = QtGui.QPixmap()
                                    pixmap.load(utils.returnFriendlyPath(path))
                                    scene = gfxView.scene()
                                    gfxItem = scene.addPixmap(pixmap)
                                    gfxItem.setZValue(-10)
                                    scene.setProperty("customImg", gfxItem)
                                    scene.setProperty("filePath", filename)
                                else:
                                    cmds.warning("Tried to load custom background image: " + str(
                                        path) + ", but file not found on disk.")

                except Exception, e:
                    print e

            # ===============================================================
            # #Handle Sub-Pickers
            # ===============================================================
            if len(subPickers) > 0:
                for info in subPickers:

                    module = info[4]
                    tab = info[1]
                    transforms = info[2]
                    mirrored = info[3]
                    pickerItems = self.findAllPickerItems()

                    # each item in pickerItems has module, item, niceName. use niceName to see if we have a winner

                    for each in pickerItems:
                        pickerModule = each[0]
                        pickerItem = each[1]
                        pickerNiceName = each[2]

                        if pickerModule == module:
                            if pickerNiceName is not None:
                                # now find a matching entry in that list to our tab variable
                                index = tabInfo.get(tab)

                                # set our tab widget to that index
                                tabWidget.setCurrentIndex(index)

                                # find current scene
                                scene = self.getCurrentScene()
                                scene.addItem(pickerItem)

                                # set transformations on the picker
                                pickerItem.setTransformOriginPoint(pickerItem.boundingRect().center())
                                pickerItem.setScale(transforms[2])

                                # when loading a picker, set data(1) to be the scale factor that was possibly saved out.
                                pickerItem.setData(1, transforms[2])

                                pickerItem.setTransformOriginPoint(pickerItem.boundingRect().center())
                                pickerItem.setRotation(transforms[1])

                                pickerItem.setPos(QtCore.QPointF(transforms[0][0], transforms[0][1]))

                                if mirrored == -1:
                                    pickerItem.setTransformOriginPoint(pickerItem.boundingRect().center())
                                    pickerItem.setTransform(
                                        QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, scene.sceneRect().width(), 0.0))
                                    pickerItem.setTransformOriginPoint(pickerItem.boundingRect().center())

                                # lock down pickers
                                pickerItem.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                                pickerItem.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                                pickerItem.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                                pickerItem.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False)

            # ===============================================================
            # #Add Comment data
            # ===============================================================
            commentData = data["commentData"]

            for item in commentData:
                rect = item.get("rect")
                color = item.get("color")
                label = item.get("label")
                tab = item.get("tab")

                tabChildren = tabWidget.children()

                # get a list of the tabs with their names and index
                tabInfo = {}
                for i in range(len(tabChildren)):
                    tabName = tabWidget.tabText(i)
                    tabInfo[tabName] = i

                # now find a matching entry in that list to our tab variable
                index = tabInfo.get(tab)
                if index is None:
                    index = 0
                # set out tab widget to that index
                tabWidget.setCurrentIndex(index)

                view = self.getCurrentView()
                scene = self.getCurrentScene()

                box = interfaceUtils.commentBoxItem(rect[0], rect[1], rect[2], rect[3], scene, view, self)
                box.brush.setColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))
                box.textLabel.setPlainText(label)
                scene.addItem(box)

                box.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                box.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                box.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                box.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False)

            #
            # ===============================================================
            # #Add Custom data
            # ===============================================================
            if "customData" in data.keys():

                import Tools.Animation.ART_AddCustomButton as acb

                customData = data["customData"]

                clearBrush = QtGui.QBrush(QtCore.Qt.black)
                clearBrush.setStyle(QtCore.Qt.NoBrush)

                for item in customData:
                    button_type = item.get("buttonType")
                    tab = item.get("tab")
                    style = item.get("style")
                    transforms = item.get("transforms")
                    hasLabel = item.get("hasLabel")

                    tabChildren = tabWidget.children()

                    # get a list of the tabs with their names and index
                    tabInfo = {}
                    for i in range(len(tabChildren)):
                        tabName = tabWidget.tabText(i)
                        tabInfo[tabName] = i

                    # now find a matching entry in that list to our tab variable
                    index = tabInfo.get(tab)
                    if index is None:
                        index = 0
                    # set our tab widget to that index
                    tabWidget.setCurrentIndex(index)

                    # get scene/view info
                    view = self.getCurrentView()
                    scene = self.getCurrentScene()

                    # create the instance of the custom button
                    custom_border = interfaceUtils.customBorderItem(10, 10, 48, 48, clearBrush, None)

                    if button_type == "selection":
                        selection = item.get("selection")
                        color = item.get("color")

                        if style == 0:
                            brush = QtGui.QColor(color[0], color[1], color[2])
                            button = acb.SelectionButton_Color(28, 28, [10, 10], selection, brush, color, custom_border)
                            scene.addItem(custom_border)

                        if style == 1:
                            path = item.get("image")
                            image = QtGui.QPixmap(path)
                            button = acb.SelectionButton_Icon(28, 28, [10, 10], selection, path, image, custom_border)
                            scene.addItem(custom_border)

                        if hasLabel is True:
                            text = item.get("labelText")
                            position = item.get("labelPosition")
                            acb.Custom_Text_Item(text, position, customColor=None, parent=button)

                            # set data for notifying that the button has a label associated with it
                            button.setData(9, True)
                            button.setData(10, text)
                            button.setData(11, position)

                    if button_type == "script":
                        path = item.get("image")
                        scriptType = item.get("scriptType")
                        scriptContents = item.get("scriptContents")
                        image = QtGui.QPixmap(path)
                        button = acb.ScriptButton_Icon(28, 28, [10, 10], scriptContents, scriptType, path, image,
                                                       custom_border)
                        scene.addItem(custom_border)

                        if hasLabel is True:
                            text = item.get("labelText")
                            position = item.get("labelPosition")
                            acb.Custom_Text_Item(text, position, customColor=None, parent=button)

                            # set data for notifying that the button has a label associated with it
                            button.setData(9, True)
                            button.setData(10, text)
                            button.setData(11, position)

                    if button_type == "label":
                        label_text = item.get("labelText")
                        color = item.get("color")
                        label = acb.Custom_Text_Item(label_text, "center", color, custom_border, True)
                        label.setData(99, "label")
                        label.setData(6, color)
                        label.setData(10, label_text)

                        scene.addItem(custom_border)

                    # set transformations on the custom button object
                    custom_border.setTransformOriginPoint(custom_border.boundingRect().center())
                    custom_border.setScale(transforms[2])

                    # when loading a picker, set data(1) to be the scale factor that was possibly saved out.
                    custom_border.setData(1, transforms[2])
                    custom_border.setTransformOriginPoint(custom_border.boundingRect().center())
                    custom_border.setRotation(transforms[1])
                    custom_border.setPos(QtCore.QPointF(transforms[0][0], transforms[0][1]))

                    custom_border.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                    custom_border.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                    custom_border.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                    custom_border.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False)

            # ===============================================================
            # #Find button color data
            # ===============================================================
            try:
                buttonData = data["buttonData"]

                for border in borderItems:
                    pickerModule = border[1]
                    picker = border[0]
                    networkNode = border[2]

                    for button in buttonData:
                        module = button.get("module")
                        color = button.get("color")
                        control = button.get("control")

                        if pickerModule == module:

                            # then we have the correct border item parent and now need to get its button
                            childItems = picker.childItems()
                            for child in childItems:
                                if type(child) == interfaceUtils.pickerButton:

                                    # delete the existing scriptJob
                                    scriptJob = picker.data(5)
                                    cmds.scriptJob(kill=scriptJob)
                                    self.selectionScriptJobs.remove(scriptJob)

                                    # set the button color
                                    child.brush.setColor(QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3]))

                                    inst = self.getModuleInst(networkNode)

                                    # create the new scriptJob
                                    newColor = QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3])
                                    scriptJob = cmds.scriptJob(event=["SelectionChanged",
                                                                      partial(inst.selectionScriptJob_animUI,
                                                                              [[child, control, newColor]])],
                                                               kws=True)
                                    picker.setData(5, scriptJob)
                                    self.selectionScriptJobs.append(scriptJob)

            except Exception, e:
                print e

            # ===============================================================
            # #write picker file location to character node
            # ===============================================================
            if not cmds.objExists(characterNode + ".pickerFile"):
                cmds.addAttr(characterNode, ln="pickerFile", dt="string")

            pickerFile = utils.returnFriendlyPath(filename)
            cmds.setAttr(characterNode + ".pickerFile", pickerFile, type="string")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorChildTextItems(self, children):
        """
        Mirrors any QGraphicsSimpleTextItems text if the parent picker was mirrored, so that the text is correct.
        :param children: List of child items (QGraphicsSimpleTextItems) of a pickerBorderItem or a pickerButton.

        """

        # for mirroring text on any child items of a pickerBorderItem or a pickerButton
        for child in children:
            if type(child) == QtWidgets.QGraphicsSimpleTextItem:
                child.setTransformOriginPoint(child.boundingRect().center())
                child.setTransform(QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, child.boundingRect().width(), 0.0))

            children = child.childItems()
            if children is not None:
                self.mirrorChildTextItems(children)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getCurrentScene(self):
        """
        Gets the QGraphicsScene of the current QGraphicsView, which is gotten by calling on self.getCurrentView.

        :return: Returns the QGraphicsScene under the current QGraphicsView.

        .. seealso:: ART_AnimationUI.getCurrentView

        """

        view = self.getCurrentView()
        scene = view.scene()
        return scene

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def getCurrentView(self):
        """
        Gets the current QGraphicsView based on the currently selected character tab, and the currently selected
        picker tab of said character.

        :return: Returns the QGraphicsView that is currently active.

        """
        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)

        # search through the children of the widget until we find the gfxScene
        children = widget.children()
        for child in children:
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                canvasIndex = tab.currentIndex()
                canvasWidget = tab.widget(canvasIndex)

                canvasChildren = canvasWidget.children()
                for canvasChild in canvasChildren:
                    if type(canvasChild) == QtWidgets.QGraphicsView:
                        view = canvasChild

                        return view

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getPickerTabs(self, saving):
        """
        Finds and returns all picker item data, like transforms, scale, x/y coordinates, mirrored status, parent tab,
        and controlled module.

        :param saving: Whether or not this function is being called by savePicker, in which case if it is, it will then
                        make sure that the picker items are no longer editable.

        :rtype: A list of lists, where each inner list has the following data for a picker item:
        :return [0]: Name of tab the picker item belongs to
        :return [1]: Picker item transforms
        :return [2]: Name of module picker belongs to (which module controls it interfaces with)
        :return [3]: Whether or not the picker item is mirrored.
        :return [4]: Whether or not the picker is a sub-picker, like fingers or toes.
        :return [5]: And if not saving, the memory address of the picker item.

        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        returnData = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                selectedTab = tab.currentIndex()

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            # get all items in the gfxScene
                            itemsInScene = scene.items()

                            for item in itemsInScene:
                                # if we find our top level picker item (the borderItem), get it's data
                                if type(item) == interfaceUtils.pickerBorderItem or item.type() == 3:
                                    if item.data(99) != "custom":

                                        # item.data(1)could have data that is the scale factor, however, if this is
                                        # a fresh picker, it will not.
                                        scaleFactor = item.data(1)
                                        if scaleFactor is None:
                                            scaleFactor = item.scale

                                        # get position, rotation, and find out if the pickerBorderItem has been mirrored
                                        position = item.pos()
                                        position = [position.x(), position.y()]
                                        rotation = item.rotation()
                                        mirrored = item.transform().m11()
                                        itemData = {}

                                        # add data to dictionary
                                        itemData["tab"] = tab.tabText(canvasIndex)
                                        itemData["transforms"] = [position, rotation, scaleFactor]
                                        itemData["module"] = item.data(QtCore.Qt.UserRole)
                                        itemData["mirrored"] = mirrored

                                        if item.data(2) is None:
                                            itemData["subPicker"] = False
                                        else:
                                            itemData["subPicker"] = True

                                        if not saving:
                                            itemData["item"] = item

                                        if saving:
                                            # set flags to False so borderItem is no longer moveable, selectable, etc.
                                            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                                            item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                                            item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                                            item.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False)

                                        returnData.append(itemData)

                                if type(item) == QtWidgets.QGraphicsPixmapItem:
                                    customImg = scene.property("customImg")
                                    if item == customImg:
                                        filePath = scene.property("filePath")
                                        itemData = {}

                                        itemData["tab"] = tab.tabText(canvasIndex)
                                        itemData["path"] = filePath

                                        returnData.append(itemData)

                tab.setCurrentIndex(selectedTab)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getComments(self, saving=False):
        """
        Gets any comment boxes that were created on any picker tabs and returns a list of those items.
        :param saving: Whether or not this function is being called from savePicker, in which case, it will disable
        edits.

        :rtype: A list of lists where the inner list contains the following data for each comment box found:
        :return [0]: The QRect of the comment box, which contains the box dimensions and the x/y coordinates.
        :return [1]: The color of the comment box
        :return [2]: The name of the tab the comment box is under.
        :return [3]: The text label of the comment box.

        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        returnData = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                selectedTab = tab.currentIndex()

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            # get all items in the gfxScene
                            itemsInScene = scene.items()

                            for item in itemsInScene:

                                if type(item) == interfaceUtils.commentBoxItem:

                                    itemData = {}
                                    if not saving:
                                        itemData["item"] = item

                                    # get comment box position and color
                                    geo = item.boundingRect()
                                    color = item.brush.color().getRgb()
                                    itemData["rect"] = [geo.x(), geo.y(), geo.width(), geo.height()]
                                    itemData["color"] = color
                                    itemData["tab"] = tab.tabText(canvasIndex)

                                    # get comment box text
                                    children = item.childItems()
                                    for each in children:
                                        if type(each) == QtWidgets.QGraphicsTextItem:
                                            label = each.toPlainText()
                                            itemData["label"] = label

                                    returnData.append(itemData)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getCustomButtons(self, saving=False):
        """
        Gets custom picker data which includes custom selection buttons, custom script buttons, and custom labels.

        :param saving: Whether or not this data is being saved to a file or simply gathered and returned

        :return: Dictionary of item data (color, icon, image, selection, script, etc)
        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        returnData = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:
            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                selectedTab = tab.currentIndex()

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            # get all items in the gfxScene
                            itemsInScene = scene.items()

                            for item in itemsInScene:
                                # if the item is a customBorderItem
                                if item.data(99) == "custom":

                                    # item.data(1)could have data that is the scale factor, however, if this is
                                    # a fresh picker, it will not.
                                    scaleFactor = item.data(1)
                                    if scaleFactor is None:
                                        scaleFactor = item.scale

                                    # get position, rotation, and find out if the pickerBorderItem has been mirrored
                                    position = item.pos()
                                    position = [position.x(), position.y()]
                                    rotation = item.rotation()
                                    itemData = {}

                                    child_items = item.childItems()
                                    for each in child_items:
                                        # determine type of button (script, selection)
                                        if each.data(99) == "script":
                                            # DATA TYPES
                                            # 8 = image path for icon
                                            # 9 = has label (True/False)
                                            # 10 = label text
                                            # 11 = label position
                                            # 20 = script type
                                            # 21 = script
                                            itemData["buttonType"] = "script"
                                            itemData["style"] = 1
                                            itemData["hasLabel"] = each.data(9)
                                            itemData["labelText"] = each.data(10)
                                            itemData["labelPosition"] = each.data(11)
                                            itemData["scriptType"] = each.data(20)
                                            itemData["scriptContents"] = each.data(21)
                                            itemData["image"] = each.data(8)

                                        if each.data(99) == "selection":
                                            # DATA TYPES
                                            # 5 = selection objects
                                            # 6 = button color
                                            # 7 = style (color or icon)
                                            # 8 = image path for icon
                                            # 9 = has label (True/False)
                                            # 10 = label text
                                            # 11 = label position

                                            itemData["buttonType"] = "selection"
                                            itemData["selection"] = each.data(5)
                                            itemData["style"] = each.data(7)
                                            itemData["hasLabel"] = each.data(9)
                                            itemData["labelText"] = each.data(10)
                                            itemData["labelPosition"] = each.data(11)

                                            # button style (color or icon)
                                            if each.data(7) == 0:
                                                itemData["color"] = each.data(6)

                                            if each.data(7) == 1:
                                                itemData["image"] = each.data(8)

                                        if each.data(99) == "label":
                                            itemData["buttonType"] = "label"
                                            itemData["color"] = each.data(6)
                                            itemData["labelText"] = each.data(10)

                                    # add data to dictionary
                                    itemData["tab"] = tab.tabText(canvasIndex)
                                    itemData["transforms"] = [position, rotation, scaleFactor]

                                    if not saving:
                                        itemData["item"] = item

                                    if saving:
                                        # set flags to False so borderItem is no longer moveable, selectable, etc.
                                        item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                                        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
                                        item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)
                                        item.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, False)

                                    returnData.append(itemData)

                tab.setCurrentIndex(selectedTab)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getButtonColors(self):
        """
        Gets joint module picker button colors, which can be edited by the user.

        .. note:: Currently, only the joint module supports users being able to change the button color.

        :rtype: A list of lists where the inner list contains the following data for each joint module found:
        :return [0]: The name of the module this picker interfaces with.
        :return [1]: The color of the picker button.
        :return [2]: The name of the control this button selects.

        """

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)
        returnData = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                selectedTab = tab.currentIndex()

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            # get all items in the gfxScene
                            itemsInScene = scene.items()

                            for item in itemsInScene:
                                if type(item) == interfaceUtils.pickerBorderItem or item.type() == 3:
                                    childButtons = item.childItems()

                                    # if the picker button is from a leaf module, get color data (only leaf for now)
                                    for child in childButtons:
                                        if type(child) == interfaceUtils.pickerButton:
                                            moduleType = item.data(QtCore.Qt.UserRole)
                                            if "ART_Leaf_Module" in moduleType:

                                                # get button color
                                                color = child.brush.color().getRgb()

                                                # store module name, button color
                                                itemData = {}
                                                itemData["module"] = moduleType
                                                itemData["color"] = color
                                                itemData["control"] = child.object

                                                returnData.append(itemData)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getModuleInst(self, module):
        """
        Takes the given module and instantiates it, returning the memory address for the created instance.

        :param module: The name of the module to instantiate.

        :return: The instance of the instantiated module in memory.

        """

        modType = cmds.getAttr(module + ".moduleType")
        modName = cmds.getAttr(module + ".moduleName")
        mod = __import__("RigModules." + modType, {}, {}, [modType])

        # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
        moduleClass = getattr(mod, mod.className)

        # find the instance of that module
        moduleInst = moduleClass(self, modName)

        return moduleInst

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeBackground(self):
        """
        Creates an interface allowing a user to change the background image of a picker with these dimensions: (442 x
        600)

        """

        if cmds.window("pyART_changeBackgroundImg_Win", exists=True):
            cmds.deleteUI("pyART_changeBackgroundImg_Win", wnd=True)

        mainWin = QtWidgets.QMainWindow(self.mainWidget)
        mainWin.setStyleSheet(self.style)

        mainWin.setMinimumSize(QtCore.QSize(400, 200))
        mainWin.setMaximumSize(QtCore.QSize(400, 200))

        # set qt object name
        mainWin.setObjectName("pyART_changeBackgroundImg_Win")
        mainWin.setWindowTitle("Change Background")

        # create the main layout
        mainWidget = QtWidgets.QFrame()
        mainWin.setCentralWidget(mainWidget)
        mainLayout = QtWidgets.QVBoxLayout(mainWidget)

        # scroll area contents
        scrollContents = QtWidgets.QFrame()
        scrollContents.setStyleSheet("background: transparent;")
        scrollLayout = QtWidgets.QVBoxLayout()
        scrollLayout.setSpacing(5)

        # find tabs. for each tab, create widget for changing background
        tabs = []
        index = self.characterTabs.currentIndex()
        widget = self.characterTabs.widget(index)

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, get tab name and item
            if type(child) == QtWidgets.QTabWidget:
                tab = child

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)

                    # find tab's graphics view
                    canvas = tab.widget(i)
                    canvasChildren = canvas.children()
                    for child in canvasChildren:
                        if type(child) == QtWidgets.QGraphicsView:
                            gfxView = child
                            tabs.append([tab, tab.tabText(i), gfxView])

        for i in range(len(tabs)):
            # create the widget for each tab background
            layout = QtWidgets.QHBoxLayout()
            scrollLayout.addLayout(layout)

            # which tab combo box
            tabComboBox = QtWidgets.QComboBox()
            tabComboBox.setMinimumWidth(100)
            tabComboBox.setFixedHeight(35)
            layout.addWidget(tabComboBox)
            tabComboBox.setStyleSheet(self.style)

            tabComboBox.addItem(tabs[i][1])

            # path location
            pathField = QtWidgets.QLineEdit()
            layout.addWidget(pathField)
            pathField.setReadOnly(True)
            pathField.setFixedHeight(35)
            pathField.setStyleSheet(self.style)
            pathField.setMinimumWidth(160)
            pathField.setPlaceholderText("418 x 525 PNG image file..")

            # browse button
            button = QtWidgets.QPushButton()
            layout.addWidget(button)
            button.setMinimumSize(35, 35)
            button.setMaximumSize(35, 35)
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/load.png"))
            button.setIconSize(QtCore.QSize(30, 30))
            button.setIcon(icon)
            button.setStyleSheet(self.style)
            button.clicked.connect(partial(self.backgroundBrowse, pathField, tabs[i][2]))

            # clear button
            button = QtWidgets.QPushButton()
            layout.addWidget(button)
            button.setMinimumSize(35, 35)
            button.setMaximumSize(35, 35)
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/removeModule.png"))
            button.setIconSize(QtCore.QSize(30, 30))
            button.setIcon(icon)
            button.setToolTip("Clear custom background image, resetting back to default.")
            button.setStyleSheet(self.style)
            button.clicked.connect(partial(self.clearBackground, tabs[i][2]))

        # add everything to the scroll Layout
        scrollContents.setLayout(scrollLayout)
        scrollArea = QtWidgets.QScrollArea()
        mainLayout.addWidget(scrollArea)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrollArea.setWidgetResizable(False)
        scrollArea.setWidget(scrollContents)

        # show
        mainWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def backgroundBrowse(self, field, gfxView):
        """
        Opens a file browser to select a valid .png background image and then apply it to the specified QGraphicsScene.

        :param field: QLineEdit for the path name to be displayed.
        :param gfxView: QGraphicsView to add the background image to.

        """

        startingDir = utils.returnNicePath(self.toolsPath, "Core/Icons")
        if os.path.exists(startingDir):

            filename = cmds.fileDialog2(fm=1, okc="Load Picker", dir=startingDir, ff="*.png")
            if filename is not None:
                filename = filename[0]
                field.setText(utils.returnFriendlyPath(filename))

                # set background image
                pixmap = QtGui.QPixmap()
                pixmap.load(utils.returnFriendlyPath(filename))
                scene = gfxView.scene()
                gfxItem = scene.addPixmap(pixmap)
                gfxItem.setZValue(-10)
                scene.setProperty("customImg", gfxItem)
                scene.setProperty("filePath", filename)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def clearBackground(self, gfxView):
        """
        Removes the background image from the given QGraphicsView.

        :param gfxView: The QGraphicsView whose background image to remove.

        .. seealso:: ART_AnimationUI.changeBackground

        """

        scene = gfxView.scene()
        items = scene.items()
        customImg = scene.property("customImg")

        for item in items:
            if item == customImg:
                scene.removeItem(item)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def exportMotion(self):
        """
        Instantiates ART_ExportMotionUI to bring up the tool for exporting animation out to various file formats.

        """

        import Tools.Animation.ART_ExportMotionUI as ART_ExportMotionUI
        ART_ExportMotionUI.ART_ExportMotion(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importMotion(self):
        """
        Instantiates ART_ImportMotionUI to bring up the tool for importing FBX animation onto the rig.

        """

        import Tools.Animation.ART_ImportMotionUI as ART_ImportMotionUI
        ART_ImportMotionUI.ART_ImportMotion(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetRigCtrls(self):
        """
        Instantiates ART_ResetModulesUI to bring up the tool for resetting transformations on a selected modules.
        Also known as "zeroing out".

        """

        import Tools.Animation.ART_ResetModulesUI as ART_ResetModulesUI
        ART_ResetModulesUI.ART_ResetModules(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def poseLibrary(self):
        import Tools.Animation.ART_PoseLibrary as apl
        apl.run()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectionSets(self):
        """
        Instantiates ART_SelectionSetsUI to bring up the tool for creating and managing selection sets.
        """
        import Tools.Animation.ART_SelectionSetsUI as selectionSets
        reload(selectionSets)
        selectionSets.run()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectAllCtrls(self):
        """
        Instantiates ART_SelectControlsUI to bring up the tool for selecting specified rig controls for selected
        modules.

        """

        show = True
        mods = cmds.getModifiers()
        if (mods & 4) > 0:
            show = False

        import Tools.Animation.ART_SelectControlsUI as ART_SelectControlsUI
        ART_SelectControlsUI.ART_SelectControls(self, show)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def matchOverRange(self):
        """
        Instantiates ART_MatchOverRangeUI to bring up the tool for matching different rig type over a frame range for
        selected modules.

        :Example:

        Matching the IK leg rig controls to the Fk leg rig controls over a frame range of 0-30.

        """

        import Tools.Animation.ART_MatchOverRangeUI as ART_MatchOverRangeUI
        ART_MatchOverRangeUI.ART_MatchOverRange(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def rigSettings(self):
        """
        Instantiates ART_RigSettingsUI to bring up the tool for managing various settings on the rig.
        """

        import Tools.Animation.ART_RigSettingsUI as rigSettings
        rigSettings.run(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def spaceSwitcher(self):
        """
        Instantiates ART_SpaceSwitcherUI to bring up the tool for creating spaces, managing and switching spaces, and
        baking spaces down.

        """

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
        ssui.run()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeTabImage(self, *args):

        tabs = self.characterTabs.count()
        current = self.characterTabs.currentIndex()

        for i in range(tabs):

            # restore the current tab to the original icon image (from disk)
            if i == current:
                original_icon = self.characterTabs.property("tab_" + str(i))
                self.characterTabs.setTabIcon(i, original_icon)

            # for any other tab, create a new image from the original icon and darken it, then reapply
            else:
                # get the icon and convert it to a pixmap. Then create a new QImage
                icon = self.characterTabs.tabIcon(i)
                pixmap = icon.pixmap(60, 60)
                tmp = pixmap.toImage()

                # loop through the pixels of the image
                for y in range(0, tmp.height() + 1):
                    for x in range(0, tmp.width() + 1):

                        # get the rgb value of the pixel
                        colorAtPixel = tmp.pixel(x, y)
                        pixelColor = QtGui.QColor(colorAtPixel).getRgb()[:-1]
                        newColor = QtGui.QColor(pixelColor[0], pixelColor[1], pixelColor[2])

                        # darken that pixel by double
                        finalColor = newColor.darker(300)

                        # set the pixel on the temp image to this new color
                        tmp.setPixel(x, y, finalColor.rgb())

                # set the icon of the tab to the new, darkened, image.
                newIcon = QtGui.QPixmap.fromImage(tmp)
                self.characterTabs.setTabIcon(i, newIcon)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _mirror_context_menu(self, btn, pos):

        index = self.characterTabs.currentIndex()
        character = self.characterTabs.tabToolTip(index)

        menu_style = interfaceUtils.get_style_sheet("menu")
        menu = QtWidgets.QMenu()
        menu.setStyleSheet(menu_style)

        mirror_local_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/mirror.png"))

        pose_location = self._capture_current_pose()

        local_menu = menu.addMenu(mirror_local_icon, "Mirror Current Pose (Local)")
        local_menu.addAction("X", partial(self._mirror_current_pose, pose_location, "Local Space", character, "X"))
        local_menu.addAction("Y", partial(self._mirror_current_pose, pose_location, "Local Space", character, "Y"))
        local_menu.addAction("Z", partial(self._mirror_current_pose, pose_location, "Local Space", character, "Z"))

        world_menu = menu.addMenu(mirror_local_icon, "Mirror Current Pose (World)")
        world_menu.addAction("X", partial(self._mirror_current_pose, pose_location, "World Space", character, "X"))
        world_menu.addAction("Y", partial(self._mirror_current_pose, pose_location, "World Space", character, "Y"))
        world_menu.addAction("Z", partial(self._mirror_current_pose, pose_location, "World Space", character, "Z"))

        selected_menu = menu.addMenu(mirror_local_icon, "Mirror Current Pose (Selected)")
        selected_menu.addAction("X", partial(self._mirror_current_pose, pose_location, "Local Space", character, "X",
                                             True))
        selected_menu.addAction("Y", partial(self._mirror_current_pose, pose_location, "Local Space", character, "Y",
                                             True))
        selected_menu.addAction("Z", partial(self._mirror_current_pose, pose_location, "Local Space", character, "Z",
                                             True))

        menu.exec_(btn.mapToGlobal(pos))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _mirror_current_pose(self, pose_location, space, namespace, axis, selected=False):

        if selected is True:
            apl.ART_LoadPose(pose_location, "Mirror Selected", space, namespace, axis)
        else:
            apl.ART_LoadPose(pose_location, "Mirror", space, namespace, axis)

        try:
            os.remove(pose_location)
        except IOError:
            pass
        except WindowsError:
            pass
        except OSError:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _capture_current_pose(self):

        controls = self._get_controls()
        temp_dir = utils.returnFriendlyPath(cmds.internalVar(userTmpDir=True))
        apl.ART_CreatePose("temp", temp_dir, controls, viewport=None, image="test")
        full_path = utils.returnNicePath(temp_dir, "temp.v2pose")
        return full_path

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_controls(self):

        return_controls = []
        character_controls = []

        # get the current tab index and the widget
        index = self.characterTabs.currentIndex()
        character = self.characterTabs.tabToolTip(index)

        if cmds.objExists(character + ":" + "ART_RIG_ROOT"):
            modules = cmds.listConnections(character + ":ART_RIG_ROOT.rigModules")

            if modules is not None:
                for module in modules:
                    controls = cmds.listConnections(module + ".controls")

                    if controls is not None:
                        for control in controls:
                            # get all attrs on the controlNode
                            attrs = cmds.listAttr(control, ud=True)

                            # loop through attrs, getting connections
                            for attr in attrs:
                                connections = cmds.listConnections(control + "." + attr, source=False)
                                if connections is not None:
                                    character_controls.extend(connections)

            for each in character_controls:
                return_controls.append(each)

        return_controls.append(character + ":" + "rig_settings")

        return return_controls

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """
    Instantiate the ART_AnimationUI class to build the main interface the animators will interact with.

    :return: instance of the ART_AnimationUI in memory.

    """

    for instance in ART_AnimationUI._instances:
        del instance

    print ART_AnimationUI._instances

    # create new instance of ART_AnimationUI
    gui = ART_AnimationUI(getMainWindow())

    # Dock Control
    allowedAreas = ["left", "right"]

    try:
        if cmds.dockControl("pyArtv2AnimToolsDock", q=True, exists=True):
            cmds.deleteUI("pyART_AnimTools_Win")
            cmds.deleteUI("pyArtv2AnimToolsDock", control=True)

        dock = cmds.dockControl("pyArtv2AnimToolsDock", area="right", content="pyART_AnimTools_Win",
                                allowedArea=allowedAreas, label="Animation Tools", w=450, h=500)
        cmds.refresh(force=True)
        cmds.dockControl(dock, edit=True, r=True)

    except Exception, e:
        cmds.warning("UI failed to launch.")
        print e

    return gui
