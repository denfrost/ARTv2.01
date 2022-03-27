# standard imports
import json
import os
from functools import partial
import copy

import maya.OpenMayaUI as mui
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken

# external imports
import Utilities.utils as utils
import Utilities.riggingUtils as riggingUtils
from RigModules.Base.ART_RigModule import ART_RigModule
from RigModules.ART_Root import ART_Root
import Utilities.interfaceUtils as interfaceUtils

windowTitle = "Rig_Creator"
windowObject = "pyArtRigCreatorUi"


class ART_RigCreator_UI(QtWidgets.QMainWindow):
    # Original Author: Jeremy Ernst

    def __init__(self, parent=None):

        super(ART_RigCreator_UI, self).__init__(parent)

        # clean up script jobs
        jobs = cmds.scriptJob(lj=True)
        for job in jobs:
            if job.find("ART_") != -1:
                jobNum = int(job.partition(":")[0])
                cmds.scriptJob(kill=jobNum, force=True)

        # get settings
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")

        # create a few lists/dicts to store info
        self.outlinerWidgets = {}
        self.outlinerControls = []

        # this list will store module instances created by this UI or by any sub-UIs (like addModuleUI)
        self.moduleInstances = []
        self.scriptJobs = []
        self.boneCounterInst = None

        # build the UI
        self.buildUI()

        # get up-axis of maya
        self.up = cmds.upAxis(q=True, ax=True)

        # check to see if the root of our rig network exists
        exists = False
        networkNodes = cmds.ls(type="network")
        for node in networkNodes:
            attrs = cmds.listAttr(node)

            if "rigModules" in attrs:
                exists = True

        # if the root of the rig network did not exist, create it now as well as our root module
        if exists is False:

            self.rigRootMod = ART_RigModule("ART_RIG_ROOT", None, None)
            self.rigRootMod.buildNetwork()

            # create a root module
            self.rootMod = ART_Root(self, "root")
            self.rootMod.buildNetwork()
            self.rootMod.skeletonSettings_UI("Root")
            if self.up == "z":
                self.rootMod.jointMover_Build("Core/JointMover/z_up/ART_Root.ma")
            if self.up == "y":
                self.rootMod.jointMover_Build("Core/JointMover/y_up/ART_Root.ma")
            self.rootMod.addJointMoverToOutliner()
            self.moduleInstances.append(self.rootMod)

            # lock the root mover down
            self.rootMod.lock_nodes()

        # if module node network existed, create UI elements and do not create any new network nodes
        else:
            modules = utils.returnRigModules()

            for module in modules:
                modType = cmds.getAttr(module + ".moduleType")
                modName = cmds.getAttr(module + ".moduleName")
                mod = __import__("RigModules." + modType, {}, {}, [modType])

                # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
                moduleClass = getattr(mod, mod.className)

                # find the instance of that module and call on the skeletonSettings_UI function
                moduleInst = moduleClass(self, modName)
                moduleInst.skeletonSettings_UI(modName)
                moduleInst.addJointMoverToOutliner()

                self.moduleInstances.append(moduleInst)

        # run toggleMoverVisibility
        self.setMoverVisibility()

        # clear selection
        cmds.select(clear=True)

        # unisolate selection if needed
        try:
            isoPnl = cmds.getPanel(wf=True)
            isoCrnt = cmds.isolateSelect(isoPnl, q=True, s=True)
            if isoCrnt:
                cmds.isolateSelect(isoPnl, s=False)
        except:
            pass

        utils.fitViewAndShade()

        # set the UI to the correct state
        if cmds.objExists("ART_RIG_ROOT.state"):
            state = cmds.getAttr("ART_RIG_ROOT.state")
            if state == 1:
                self.toolModeStack.setCurrentIndex(1)

                # remove outliner scriptJobs
                for job in self.scriptJobs:
                    cmds.scriptJob(kill=job, force=True)

                # build the scriptJob for the weight table
                self.scriptJobs.append(self.skinToolsInst.weightTable_scriptJob())

            if state == 2:
                self.toolModeStack.setCurrentIndex(2)

                # remove outliner scriptJobs
                for job in self.scriptJobs:
                    cmds.scriptJob(kill=job, force=True)

        self.populateNetworkList()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateNetworkList(self):

        self.nodeNetworkList.clear()

        # get network nodes and add to list widget
        modules = cmds.ls(type="network")
        returnMods = []
        for module in modules:
            attrs = cmds.listAttr(module)
            if "parent" in attrs:
                returnMods.append(module)

        mainNode = cmds.listConnections(returnMods[0] + ".parent")[0]
        self.nodeNetworkList.addItem(mainNode)

        for mod in returnMods:
            self.nodeNetworkList.addItem(mod)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        # Original Author: Jeremy Ernst

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.tab_style = interfaceUtils.get_style_sheet("tabs")
        self.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        scrollSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.setMinimumSize(QtCore.QSize(580, 400))
        self.setMaximumSize(QtCore.QSize(580, 900))

        self.resize(600, 450)

        # Create a stackedWidget
        self.toolModeStack = QtWidgets.QStackedWidget()
        self.layout.addWidget(self.toolModeStack)
        self.rigMode = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.rigMode)
        self.toolModeStack.addWidget(self.rigMode)

        # create the menu bar
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setMaximumHeight(25)
        self.mainLayout.addWidget(self.menuBar)

        # create the toolbar layout
        self.toolFrame = QtWidgets.QFrame()
        self.toolFrame.setMinimumHeight(50)
        self.toolFrame.setMaximumHeight(50)
        self.toolFrame.setObjectName("darkborder")
        self.mainLayout.addWidget(self.toolFrame)
        self.toolbarLayout = QtWidgets.QHBoxLayout(self.toolFrame)
        self.toolbarLayout.setDirection(QtWidgets.QBoxLayout.RightToLeft)
        self.toolbarLayout.addStretch(0)
        self.toolbarLayout.setSpacing(10)

        # toolbar buttons
        self.pinModulesBtn = QtWidgets.QPushButton()
        self.pinModulesBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.pinModulesBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/pin.png"))
        self.pinModulesBtn.setIconSize(QtCore.QSize(30, 30))
        self.pinModulesBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.pinModulesBtn)
        text = "Pin a module in place so that moving a parent does not effect the module."
        self.pinModulesBtn.setToolTip(text)
        self.pinModulesBtn.clicked.connect(self.pinModulesUI)
        self.pinModulesBtn.setObjectName("tool")

        self.bakeOffsetsBtn = QtWidgets.QPushButton()
        self.bakeOffsetsBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.bakeOffsetsBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/bakeOffsets.png"))
        self.bakeOffsetsBtn.setIconSize(QtCore.QSize(30, 30))
        self.bakeOffsetsBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.bakeOffsetsBtn)
        self.bakeOffsetsBtn.clicked.connect(self.bakeOffsetsUI)
        self.bakeOffsetsBtn.setObjectName("tool")
        text = "Bake the offset mover values up to the global movers."
        self.bakeOffsetsBtn.setToolTip(text)

        self.aimModeBtn = QtWidgets.QPushButton()
        self.aimModeBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.aimModeBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/aim.png"))
        self.aimModeBtn.setIconSize(QtCore.QSize(30, 30))
        self.aimModeBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.aimModeBtn)
        self.aimModeBtn.clicked.connect(self.aimModeUI)
        self.aimModeBtn.setObjectName("tool")
        text = "Toggle Aim mode for modules."
        self.aimModeBtn.setToolTip(text)

        self.boneCountBtn = QtWidgets.QPushButton()
        self.boneCountBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.boneCountBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/count.png"))
        self.boneCountBtn.setIconSize(QtCore.QSize(30, 30))
        self.boneCountBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.boneCountBtn)
        self.boneCountBtn.setCheckable(True)
        self.boneCountBtn.clicked.connect(self.boneCounterUI)
        self.boneCountBtn.setObjectName("tool")
        text = "Bring up a tool that allows you to track your current bone count given your module settings."
        self.boneCountBtn.setToolTip(text)

        self.resetBtn = QtWidgets.QPushButton()
        self.resetBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.resetBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/reset.png"))
        self.resetBtn.setIconSize(QtCore.QSize(30, 30))
        self.resetBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.resetBtn)
        self.resetBtn.setCheckable(True)
        self.resetBtn.clicked.connect(self.resetModeUI)
        self.resetBtn.setObjectName("tool")
        text = "Brings up a tool to allow you to reset multiple modules' settings or transforms."
        self.resetBtn.setToolTip(text)

        self.symmetryModeBtn = QtWidgets.QPushButton()
        self.symmetryModeBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.symmetryModeBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/symmetryMode.png"))
        self.symmetryModeBtn.setIconSize(QtCore.QSize(30, 30))
        self.symmetryModeBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.symmetryModeBtn)
        self.symmetryModeBtn.clicked.connect(self.symmetryModeUI)
        self.symmetryModeBtn.setObjectName("tool")
        text = "Brings up a new window to apply symmetry to the selected modules in the list."
        self.symmetryModeBtn.setToolTip(text)

        self.geoDisplayBtn = QtWidgets.QPushButton()
        self.geoDisplayBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.geoDisplayBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/geoDisplay_on.png"))
        self.geoDisplayBtn.setIconSize(QtCore.QSize(30, 30))
        self.geoDisplayBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.geoDisplayBtn)
        self.geoDisplayBtn.setCheckable(True)
        self.geoDisplayBtn.clicked.connect(partial(self.toggleMoverVisibility, "*_proxy_geo", self.geoDisplayBtn))
        self.geoDisplayBtn.clicked.connect(
            partial(self.toggleButtonIcon, self.geoDisplayBtn, "System/geoDisplay_on.png", "System/geoDisplay.png"))
        self.geoDisplayBtn.setChecked(True)
        self.geoDisplayBtn.setObjectName("tool")
        text = "Toggles the visibility of the proxy geometry."
        self.geoDisplayBtn.setToolTip(text)

        self.lraDisplayBtn = QtWidgets.QPushButton()
        self.lraDisplayBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.lraDisplayBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/lra_on.png"))
        self.lraDisplayBtn.setIconSize(QtCore.QSize(30, 30))
        self.lraDisplayBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.lraDisplayBtn)
        self.lraDisplayBtn.setCheckable(True)
        self.lraDisplayBtn.clicked.connect(partial(self.toggleMoverVisibility, "*_lra", self.lraDisplayBtn))
        self.lraDisplayBtn.clicked.connect(
            partial(self.toggleButtonIcon, self.lraDisplayBtn, "System/lra_on.png", "System/lra.png"))
        self.lraDisplayBtn.setChecked(True)
        self.lraDisplayBtn.setObjectName("tool")
        text = "Toggles the visibility of the local rotation axis geometry."
        self.lraDisplayBtn.setToolTip(text)

        self.boneDisplayBtn = QtWidgets.QPushButton()
        self.boneDisplayBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.boneDisplayBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/boneDisplay.png"))
        self.boneDisplayBtn.setIconSize(QtCore.QSize(30, 30))
        self.boneDisplayBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.boneDisplayBtn)
        self.boneDisplayBtn.setCheckable(True)
        self.boneDisplayBtn.clicked.connect(partial(self.toggleMoverVisibility, "*_bone_geo", self.boneDisplayBtn))
        self.boneDisplayBtn.clicked.connect(self.previewSkeleton)
        self.boneDisplayBtn.setChecked(False)
        self.boneDisplayBtn.setObjectName("tool")
        text = "Creates a preview skeleton based on current module positions."
        self.boneDisplayBtn.setToolTip(text)

        self.ctrlDisplayBtn = QtWidgets.QPushButton()
        self.ctrlDisplayBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.ctrlDisplayBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/rigCtrlDisplay.png"))
        self.ctrlDisplayBtn.setIconSize(QtCore.QSize(30, 30))
        self.ctrlDisplayBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.ctrlDisplayBtn)
        self.ctrlDisplayBtn.setCheckable(True)
        self.ctrlDisplayBtn.clicked.connect(self.editRigControls)
        self.ctrlDisplayBtn.setChecked(False)
        self.ctrlDisplayBtn.setObjectName("tool")
        text = "Toggles the visibility of the rig controls to allow editing. These controls will be used when the rig" \
               " is built.\n\nIf a module does not have separate rig controls to edit, its joint mover control will be" \
               " used."
        self.ctrlDisplayBtn.setToolTip(text)

        self.meshMoverBtn = QtWidgets.QPushButton()
        self.meshMoverBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.meshMoverBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/meshMover.png"))
        self.meshMoverBtn.setIconSize(QtCore.QSize(30, 30))
        self.meshMoverBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.meshMoverBtn)
        self.meshMoverBtn.setCheckable(True)
        self.meshMoverBtn.clicked.connect(partial(self.toggleMoverVisibility, "*_mover_geo", self.meshMoverBtn))
        self.meshMoverBtn.clicked.connect(
            partial(self.toggleButtonIcon, self.meshMoverBtn, "System/meshMover_on.png", "System/meshMover.png"))
        self.meshMoverBtn.setChecked(False)
        self.meshMoverBtn.setObjectName("tool")
        text = "Toggle the visibility of the mesh mover controls. Mesh movers have no affect on the joints and are only" \
               " used to edit the placement of the proxy geometry."
        self.meshMoverBtn.setToolTip(text)

        self.offsetMoverBtn = QtWidgets.QPushButton()
        self.offsetMoverBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.offsetMoverBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/offsetMover.png"))
        self.offsetMoverBtn.setIconSize(QtCore.QSize(30, 30))
        self.offsetMoverBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.offsetMoverBtn)
        self.offsetMoverBtn.setCheckable(True)
        self.offsetMoverBtn.clicked.connect(partial(self.toggleMoverVisibility, "*_mover_offset", self.offsetMoverBtn))
        self.offsetMoverBtn.clicked.connect(
            partial(self.toggleButtonIcon, self.offsetMoverBtn, "System/offsetMover_on.png", "System/offsetMover.png"))
        self.offsetMoverBtn.setChecked(False)
        self.offsetMoverBtn.setObjectName("tool")
        text = "Toggle the visibility of the offset mover controls. Offset movers move only the associated joint."
        self.meshMoverBtn.setToolTip(text)

        self.globalMoverBtn = QtWidgets.QPushButton()
        self.globalMoverBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.globalMoverBtn.setMaximumSize(QtCore.QSize(30, 30))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/globalMover_on.png"))
        self.globalMoverBtn.setIconSize(QtCore.QSize(30, 30))
        self.globalMoverBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.globalMoverBtn)
        self.globalMoverBtn.setCheckable(True)
        self.globalMoverBtn.clicked.connect(partial(self.toggleMoverVisibility, "*_mover", self.globalMoverBtn))
        self.globalMoverBtn.clicked.connect(
            partial(self.toggleButtonIcon, self.globalMoverBtn, "System/globalMover_on.png", "System/globalMover.png"))
        self.globalMoverBtn.setChecked(True)
        self.globalMoverBtn.setObjectName("tool")
        text = "Toggle the visibility of the global mover controls. Global movers move the associated joint and its" \
               " children."
        self.globalMoverBtn.setToolTip(text)

        self.saveTemplateBtn = QtWidgets.QPushButton()
        self.saveTemplateBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.saveTemplateBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/save.png"))
        self.saveTemplateBtn.setIconSize(QtCore.QSize(30, 30))
        self.saveTemplateBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.saveTemplateBtn)
        self.saveTemplateBtn.clicked.connect(self.saveTemplate)
        self.saveTemplateBtn.setObjectName("tool")
        text = "Saves current modules, their settings, and their positions, as a template file."
        self.saveTemplateBtn.setToolTip(text)

        self.loadTemplateBtn = QtWidgets.QPushButton()
        self.loadTemplateBtn.setMinimumSize(QtCore.QSize(32, 32))
        self.loadTemplateBtn.setMaximumSize(QtCore.QSize(32, 32))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/load.png"))
        self.loadTemplateBtn.setIconSize(QtCore.QSize(30, 30))
        self.loadTemplateBtn.setIcon(icon)
        self.toolbarLayout.addWidget(self.loadTemplateBtn)
        self.loadTemplateBtn.clicked.connect(self.loadTemplate)
        self.loadTemplateBtn.setObjectName("tool")
        text = "Load an existing template file."
        self.loadTemplateBtn.setToolTip(text)

        # Add Items to the Menu Bar
        # icons
        icon_saveTemplate = QtGui.QIcon(os.path.join(self.iconsPath, "System/save.png"))
        icon_loadTemplate = QtGui.QIcon(os.path.join(self.iconsPath, "System/load.png"))
        icon_exit = QtGui.QIcon(os.path.join(self.iconsPath, "System/exit.png"))
        icon_viewToolbar = QtGui.QIcon(os.path.join(self.iconsPath, "System/toggleVis.png"))
        icon_globalMover = QtGui.QIcon(os.path.join(self.iconsPath, "System/globalMover.png"))
        icon_offsetMover = QtGui.QIcon(os.path.join(self.iconsPath, "System/offsetMover.png"))
        icon_meshMover = QtGui.QIcon(os.path.join(self.iconsPath, "System/meshMover.png"))
        icon_boneDisplay = QtGui.QIcon(os.path.join(self.iconsPath, "System/boneDisplay.png"))
        icon_lraDisplay = QtGui.QIcon(os.path.join(self.iconsPath, "System/lra.png"))
        icon_proxyGeo = QtGui.QIcon(os.path.join(self.iconsPath, "System/geoDisplay.png"))
        icon_massMirrorMode = QtGui.QIcon(os.path.join(self.iconsPath, "System/symmetryMode.png"))
        icon_resetModules = QtGui.QIcon(os.path.join(self.iconsPath, "System/reset.png"))
        icon_boneCount = QtGui.QIcon(os.path.join(self.iconsPath, "System/count.png"))
        icon_physique = QtGui.QIcon(os.path.join(self.iconsPath, "System/modelPose.png"))

        # file
        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(icon_saveTemplate, "Save Template", self.saveTemplate)
        fileMenu.addAction(icon_loadTemplate, "Load Template", self.loadTemplate)
        fileMenu.addAction(icon_exit, "Exit")

        # view
        viewMenu = self.menuBar.addMenu("View")
        viewMenu.addAction(icon_viewToolbar, "Toggle Toolbar Visibility", self.setToolbarVisibility)
        viewMenu.addAction(icon_viewToolbar, "View Module Stats", self.moduleStatusUI)

        # display
        displayMenu = self.menuBar.addMenu("Display")
        displayMenu.addAction(icon_globalMover, "Toggle Global Movers",
                              partial(self.toggleMoverVisibility_FromMenu, "*_mover", self.globalMoverBtn,
                                      "System/globalMover_on.png", "System/globalMover.png"))
        displayMenu.addAction(icon_offsetMover, "Toggle Offset Movers",
                              partial(self.toggleMoverVisibility_FromMenu, "*_mover_offset", self.offsetMoverBtn,
                                      "System/offsetMover_on.png", "System/offsetMover.png"))
        displayMenu.addAction(icon_meshMover, "Toggle Mesh Movers",
                              partial(self.toggleMoverVisibility_FromMenu, "*_mover_geo", self.meshMoverBtn,
                                      "System/meshMover_on.png", "System/meshMover.png"))
        displayMenu.addAction(icon_boneDisplay, "Toggle Joint Display", self.previewSkeleton)
        displayMenu.addAction(icon_lraDisplay, "Toggle LRA Display",
                              partial(self.toggleMoverVisibility_FromMenu, "*_lra", self.lraDisplayBtn,
                                      "System/lra_on.png", "System/lra.png"))
        displayMenu.addAction(icon_proxyGeo, "Toggle Proxy Geo Display",
                              partial(self.toggleMoverVisibility_FromMenu, "*_proxy_geo", self.geoDisplayBtn,
                                      "System/geoDisplay_on.png", "System/geoDisplay.png"))

        # tools
        toolsMenu = self.menuBar.addMenu("Tools")
        toolsMenu.addAction(icon_massMirrorMode, "Mass Mirror Mode Tool", self.symmetryModeUI)
        toolsMenu.addAction(icon_resetModules, "Reset Modules Tool", self.resetModeUI)
        toolsMenu.addAction(icon_boneCount, "Bone Counter Tool", self.boneCounterUI)
        toolsMenu.addAction(icon_physique, "Physique Editor", self.editPhysique)

        # help
        helpMenu = self.menuBar.addMenu("Help")
        helpMenu.addAction("Documentation")
        helpMenu.addAction("About")

        # create the tabLayout (Skeleton Creation and Settings/Outliner)
        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(545, 400))
        self.tabWidget.setMaximumSize(QtCore.QSize(545, 900))
        self.tabWidget.setSizePolicy(scrollSizePolicy)
        self.tabWidget.setStyleSheet(self.tab_style)

        # Create our first tab
        self.tab1 = QtWidgets.QFrame()
        self.tab1.setObjectName("light")
        self.topLevelLayout = QtWidgets.QVBoxLayout(self.tab1)
        self.tabWidget.addTab(self.tab1, "Creation/Settings")

        # create the label layout
        self.labelLayout = QtWidgets.QHBoxLayout()
        self.topLevelLayout.addLayout(self.labelLayout)

        # create a label for  Modules and Installed Modules
        self.modLabel = QtWidgets.QLabel("Rig Modules:")
        self.modLabel.setObjectName("heading")
        self.modLabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.modLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.modLabel.setSizePolicy(mainSizePolicy)
        self.modLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.modLabel.setMaximumSize(QtCore.QSize(150, 30))
        self.labelLayout.addWidget(self.modLabel)

        # create the installed modules label
        self.installedModLabel = QtWidgets.QLabel("Installed Modules:")
        self.installedModLabel.setObjectName("heading")
        self.installedModLabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.installedModLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.installedModLabel.setSizePolicy(mainSizePolicy)
        self.installedModLabel.setMinimumSize(QtCore.QSize(360, 30))
        self.installedModLabel.setMaximumSize(QtCore.QSize(360, 30))
        self.labelLayout.addWidget(self.installedModLabel)

        # create the search layout
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.topLevelLayout.addLayout(self.searchLayout)

        # create the search bars for both sides
        self.moduleSearch = QtWidgets.QLineEdit()
        self.moduleSearch.setPlaceholderText("Search...")
        self.moduleSearch.setMinimumSize(QtCore.QSize(150, 20))
        self.moduleSearch.setMaximumSize(QtCore.QSize(150, 20))
        self.moduleSearch.setSizePolicy(mainSizePolicy)
        self.searchLayout.addWidget(self.moduleSearch)
        self.moduleSearch.textChanged.connect(self.searchModules)

        self.installedSearch = QtWidgets.QLineEdit()
        self.installedSearch.setPlaceholderText("Search...")
        self.installedSearch.setMinimumSize(QtCore.QSize(150, 20))
        self.installedSearch.setMaximumSize(QtCore.QSize(150, 20))
        self.installedSearch.setSizePolicy(mainSizePolicy)
        self.searchLayout.addWidget(self.installedSearch)
        self.installedSearch.textChanged.connect(self.searchInstalled)

        # add buttons (expand all, collapse all, sort by type, sort by ABC)
        self.installed_ExpandAll = QtWidgets.QPushButton()
        self.installed_ExpandAll.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.installed_ExpandAll.setMinimumSize(QtCore.QSize(40, 20))
        self.installed_ExpandAll.setMaximumSize(QtCore.QSize(40, 20))
        self.searchLayout.addWidget(self.installed_ExpandAll)
        self.installed_ExpandAll.clicked.connect(partial(self.expandAllSettings, True))
        self.installed_ExpandAll.setObjectName("expand")
        text = "Expand all module settings."
        self.installed_ExpandAll.setToolTip(text)

        self.installed_CollapseAll = QtWidgets.QPushButton()
        self.installed_CollapseAll.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.installed_CollapseAll.setMinimumSize(QtCore.QSize(40, 20))
        self.installed_CollapseAll.setMaximumSize(QtCore.QSize(40, 20))
        self.searchLayout.addWidget(self.installed_CollapseAll)
        self.installed_CollapseAll.clicked.connect(partial(self.expandAllSettings, False))
        self.installed_CollapseAll.setObjectName("collapse")
        text = "Collapse all module settings."
        self.installed_CollapseAll.setToolTip(text)

        self.installed_sortByType = QtWidgets.QPushButton("Type")
        self.installed_sortByType.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.installed_sortByType.setMinimumSize(QtCore.QSize(40, 20))
        self.installed_sortByType.setMaximumSize(QtCore.QSize(40, 20))
        self.searchLayout.addWidget(self.installed_sortByType)
        self.installed_sortByType.clicked.connect(partial(self.sortModules, "type"))
        self.installed_sortByType.setObjectName("settings")
        text = "Sort modules by module type."
        self.installed_sortByType.setToolTip(text)

        self.installed_sortByAlphabet = QtWidgets.QPushButton("ABC")
        self.installed_sortByAlphabet.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.installed_sortByAlphabet.setMinimumSize(QtCore.QSize(40, 20))
        self.installed_sortByAlphabet.setMaximumSize(QtCore.QSize(40, 20))
        self.searchLayout.addWidget(self.installed_sortByAlphabet)
        self.installed_sortByAlphabet.clicked.connect(partial(self.sortModules, "abc"))
        self.installed_sortByAlphabet.setObjectName("settings")
        text = "Sort modules by module alphabetical order."
        self.installed_sortByAlphabet.setToolTip(text)

        # create the layout for the main part of our UI
        self.main = QtWidgets.QHBoxLayout()
        self.topLevelLayout.addLayout(self.main)

        # create the module scroll area and add it to the main layout
        self.scrollAreaMods = QtWidgets.QScrollArea()
        self.main.addWidget(self.scrollAreaMods)
        self.scrollAreaMods.setSizePolicy(mainSizePolicy)
        self.scrollAreaMods.setMinimumSize(QtCore.QSize(150, 400))
        self.scrollAreaMods.setMaximumSize(QtCore.QSize(150, 60000))
        self.scrollAreaMods.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Module scroll area contents
        self.modScrollAreaContents = QtWidgets.QFrame()
        self.modScrollAreaContents.setObjectName("dark")
        self.modScrollAreaContents.setSizePolicy(scrollSizePolicy)
        self.modScrollAreaContents.setMinimumSize(QtCore.QSize(150, 800))
        self.modScrollAreaContents.setMaximumSize(QtCore.QSize(150, 60000))
        self.scrollAreaMods.setWidget(self.modScrollAreaContents)

        # add the vertical box layout for the module scroll area
        self.moduleLayout = QtWidgets.QVBoxLayout(self.modScrollAreaContents)
        self.moduleLayout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        self.moduleLayout.setContentsMargins(5, 5, 0, 5)
        self.moduleLayout.addStretch(2)
        self.moduleLayout.setSpacing(5)

        # create the scroll area for the module settings
        self.scrollAreaSettings = QtWidgets.QScrollArea()
        self.scrollAreaSettings.setWidgetResizable(True)
        self.main.addWidget(self.scrollAreaSettings)
        self.scrollAreaSettings.setSizePolicy(scrollSizePolicy)
        self.scrollAreaSettings.setMinimumSize(QtCore.QSize(360, 400))
        self.scrollAreaSettings.setMaximumSize(QtCore.QSize(360, 600000))
        self.scrollAreaSettings.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # create the module settings scroll area contents widget
        self.settingsScrollAreaContents = QtWidgets.QFrame()
        self.settingsScrollAreaContents.setObjectName("dark")
        self.settingsScrollAreaContents.setMinimumWidth(360)
        self.settingsScrollAreaContents.setMaximumWidth(360)
        self.settingsScrollAreaContents.setSizePolicy(scrollSizePolicy)
        self.scrollAreaSettings.setWidget(self.settingsScrollAreaContents)

        # add the vertical box layout for the module scroll area
        self.moduleSettingsLayout = QtWidgets.QVBoxLayout(self.settingsScrollAreaContents)
        self.moduleSettingsLayout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        self.moduleSettingsLayout.setContentsMargins(0, 5, 0, 5)
        self.moduleSettingsLayout.addStretch(2)
        self.moduleSettingsLayout.setSpacing(10)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # SECOND TAB #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # Create the 2nd tab
        self.tab2 = QtWidgets.QFrame(self.tabWidget)
        self.tab2Layout = QtWidgets.QHBoxLayout(self.tab2)
        self.tabWidget.addTab(self.tab2, "Outliner")

        # create the treeView representing the outliner
        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setIndentation(10)
        self.treeWidget.expandAll()

        self.tab2Layout.addWidget(self.treeWidget)
        self.treeWidget.setSizePolicy(mainSizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(320, 500))
        self.treeWidget.setMaximumSize(QtCore.QSize(320, 800))

        # create columns
        self.treeWidget.headerItem().setText(0, "Modules")
        self.treeWidget.headerItem().setText(1, "G")
        self.treeWidget.headerItem().setText(2, "O")
        self.treeWidget.headerItem().setText(3, "M")

        # set column widths
        self.treeWidget.setColumnWidth(0, 240)
        self.treeWidget.setColumnWidth(1, 20)
        self.treeWidget.setColumnWidth(2, 20)
        self.treeWidget.setColumnWidth(3, 20)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # CHANNEL BOX #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # add the channel box layout
        self.channelBoxLayout = QtWidgets.QFrame()

        # set dimensions
        self.channelBoxLayout.setSizePolicy(scrollSizePolicy)
        self.channelBoxLayout.setGeometry(0, 0, 250, 500)
        self.channelBoxLayout.setMinimumSize(QtCore.QSize(220, 500))
        self.channelBoxLayout.setMaximumSize(QtCore.QSize(220, 800))
        self.tab2Layout.addWidget(self.channelBoxLayout)

        # create a VBoxLayout for the channelBox Layout
        self.channelBoxVLayout = QtWidgets.QVBoxLayout(self.channelBoxLayout)

        # create the QWidget to house the channelBox
        self.channelBoxWidget = QtWidgets.QFrame()

        # set dimensions
        self.channelBoxWidget.setSizePolicy(mainSizePolicy)
        self.channelBoxWidget.setMinimumSize(QtCore.QSize(220, 470))
        self.channelBoxWidget.setMaximumSize(QtCore.QSize(220, 770))

        # add the channel box widget to the VBoxLayout
        self.channelBoxVLayout.addWidget(self.channelBoxWidget)

        # add the channel box VBoxLayout to the QFrame
        self.channelBox_mainLayout = QtWidgets.QVBoxLayout(self.channelBoxWidget)

        # add the channel box from Maya to the UI
        channelBoxWidget = cmds.channelBox()
        pointer = mui.MQtUtil.findControl(channelBoxWidget)
        self.channelBox = shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)
        self.channelBox_mainLayout.addWidget(self.channelBox)
        self.channelBox.setObjectName("dark")
        self.channelBox.show()

        # add network node info
        self.nodeNetworkList = QtWidgets.QListWidget()
        self.channelBox_mainLayout.addWidget(self.nodeNetworkList)
        self.nodeNetworkList.setMinimumHeight(200)
        self.nodeNetworkList.setMaximumHeight(200)
        self.nodeNetworkList.itemClicked.connect(self.selectNetworkNode)

        # add the "Finalize Setup" button
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.createSkeletonLayout = QtWidgets.QHBoxLayout()
        self.createSkeletonLayout.setContentsMargins(25, 0, 0, 0)
        self.createSkeletonBtn = QtWidgets.QPushButton("FINALIZE SETUP")
        self.createSkeletonBtn.setMinimumHeight(50)
        self.createSkeletonBtn.setMaximumHeight(50)
        self.createSkeletonBtn.setFont(font)
        text = "Move to the next phase of the build. The next phase will create a skeleton based on the current module" \
               " positions. This skeleton is used to bind weights."
        self.createSkeletonBtn.setToolTip(text)

        self.createSkeletonBtn.clicked.connect(self.finalizeSetup_UI)
        self.createSkeletonLayout.addWidget(self.createSkeletonBtn)
        self.mainLayout.addLayout(self.createSkeletonLayout)

        # build deformation UI
        self.buildDeformation_UI()

        # set the layout
        self.setLayout(self.mainLayout)

        # find and populate modules list
        self.findRigModules()

        # build lock page
        self.rigLockedPage = QtWidgets.QFrame()
        self.toolModeStack.addWidget(self.rigLockedPage)

        self.rigLockedPage.setMinimumSize(QtCore.QSize(550, 721))
        self.rigLockedPage.setMaximumSize(QtCore.QSize(550, 721))
        image = utils.returnNicePath(self.iconsPath, "System/backgrounds/rigLockPage.png")
        self.rigLockedPage.setStyleSheet("background-image: url(" + image + ");")

        # add the layout to the lock page
        self.lockLayout = QtWidgets.QVBoxLayout(self.rigLockedPage)
        self.lockLayout.setContentsMargins(20, 30, 20, 10)

        buttonLayout1 = QtWidgets.QHBoxLayout()
        self.lockLayout.addLayout(buttonLayout1)

        spacer = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.lockLayout.addItem(spacer)

        remove_rig_layout = QtWidgets.QHBoxLayout()
        self.lockLayout.addLayout(remove_rig_layout)

        # info text
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)

        label = QtWidgets.QLabel("The rig is locked.")
        label.setFont(font)
        label.setStyleSheet(self.style)
        self.lockLayout.addWidget(label)
        label.setAlignment(QtCore.Qt.AlignCenter)

        label2 = QtWidgets.QLabel("Remove rigging using the above button to edit modules.")
        label2.setFont(font)
        label2.setStyleSheet(self.style)
        self.lockLayout.addWidget(label2)
        label2.setAlignment(QtCore.Qt.AlignCenter)

        spacer = QtWidgets.QSpacerItem(55, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        remove_rig_layout.addItem(spacer)

        self.removeRigBtn = QtWidgets.QPushButton()
        self.removeRigBtn.setMinimumSize(QtCore.QSize(200, 200))
        self.removeRigBtn.setMaximumSize(QtCore.QSize(200, 200))
        self.removeRigBtn.setStyleSheet(self.style)
        self.removeRigBtn.clicked.connect(partial(self.removeRigging))
        self.removeRigBtn.setObjectName("riglock")
        remove_rig_layout.addWidget(self.removeRigBtn)

        spacer = QtWidgets.QSpacerItem(55, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        remove_rig_layout.addItem(spacer)

        spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.lockLayout.addItem(spacer)

        # add spacer and button

        rename_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_rename_joints.png"))
        paint_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_paint_weights.png"))
        export_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_export_mesh.png"))
        history_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/list.png"))
        create_space_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_create_space.png"))
        create_global_space_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_create_global_space.png"))
        rename_space_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_rename_space.png"))
        remove_space_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/edit_remove_space.png"))
        pick_walk_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/select_nodes.png"))

        joint_override_button = QtWidgets.QPushButton()
        joint_override_button.clicked.connect(partial(self.overrideJointNames_UI))
        joint_override_button.setMinimumSize(QtCore.QSize(40, 40))
        joint_override_button.setMaximumSize(QtCore.QSize(40, 40))
        joint_override_button.setStyleSheet(self.style)
        joint_override_button.setObjectName("settings")
        joint_override_button.setIconSize(QtCore.QSize(35, 35))
        joint_override_button.setIcon(rename_icon)
        joint_override_button.setToolTip("Override joint names on skeleton.")

        skin_tools_button = QtWidgets.QPushButton()
        skin_tools_button.clicked.connect(partial(self.deformationTools))
        skin_tools_button.setMinimumSize(QtCore.QSize(40, 40))
        skin_tools_button.setMaximumSize(QtCore.QSize(40, 40))
        skin_tools_button.setStyleSheet(self.style)
        skin_tools_button.setObjectName("settings")
        skin_tools_button.setIconSize(QtCore.QSize(35, 35))
        skin_tools_button.setIcon(paint_icon)
        skin_tools_button.setToolTip("Launch deformation tools.")

        export_meshes_button = QtWidgets.QPushButton()
        export_meshes_button.clicked.connect(partial(self.exportMeshes))
        export_meshes_button.setMinimumSize(QtCore.QSize(40, 40))
        export_meshes_button.setMaximumSize(QtCore.QSize(40, 40))
        export_meshes_button.setStyleSheet(self.style)
        export_meshes_button.setObjectName("settings")
        export_meshes_button.setIconSize(QtCore.QSize(35, 35))
        export_meshes_button.setIcon(export_icon)
        export_meshes_button.setToolTip("Export skeletal meshes to FBX.")

        rig_history_button = QtWidgets.QPushButton()
        rig_history_button.clicked.connect(partial(self.rigHistoryUI))
        rig_history_button.setMinimumSize(QtCore.QSize(40, 40))
        rig_history_button.setMaximumSize(QtCore.QSize(40, 40))
        rig_history_button.setStyleSheet(self.style)
        rig_history_button.setObjectName("settings")
        rig_history_button.setIconSize(QtCore.QSize(35, 35))
        rig_history_button.setIcon(history_icon)
        rig_history_button.setToolTip("View rig history.")

        create_space_button = QtWidgets.QPushButton()
        create_space_button.setMinimumSize(QtCore.QSize(40, 40))
        create_space_button.setMaximumSize(QtCore.QSize(40, 40))
        create_space_button.setStyleSheet(self.style)
        create_space_button.setObjectName("settings")
        create_space_button.setIconSize(QtCore.QSize(35, 35))
        create_space_button.setIcon(create_space_icon)
        create_space_button.setToolTip("Create a space for a control.")
        create_space_button.clicked.connect(self._create_space)

        create_global_space_button = QtWidgets.QPushButton()
        create_global_space_button.setMinimumSize(QtCore.QSize(40, 40))
        create_global_space_button.setMaximumSize(QtCore.QSize(40, 40))
        create_global_space_button.setStyleSheet(self.style)
        create_global_space_button.setObjectName("settings")
        create_global_space_button.setIconSize(QtCore.QSize(35, 35))
        create_global_space_button.setIcon(create_global_space_icon)
        create_global_space_button.setToolTip("Setup global spaces for all controls.")
        create_global_space_button.clicked.connect(self._create_global_spaces)

        rename_space_button = QtWidgets.QPushButton()
        rename_space_button.setMinimumSize(QtCore.QSize(40, 40))
        rename_space_button.setMaximumSize(QtCore.QSize(40, 40))
        rename_space_button.setStyleSheet(self.style)
        rename_space_button.setObjectName("settings")
        rename_space_button.setIconSize(QtCore.QSize(35, 35))
        rename_space_button.setIcon(rename_space_icon)
        rename_space_button.setToolTip("Rename a space.")
        rename_space_button.clicked.connect(self._rename_space)

        delete_space_button = QtWidgets.QPushButton()
        delete_space_button.setMinimumSize(QtCore.QSize(40, 40))
        delete_space_button.setMaximumSize(QtCore.QSize(40, 40))
        delete_space_button.setStyleSheet(self.style)
        delete_space_button.setObjectName("settings")
        delete_space_button.setIconSize(QtCore.QSize(35, 35))
        delete_space_button.setIcon(remove_space_icon)
        delete_space_button.setToolTip("Remove a space.")
        delete_space_button.clicked.connect(self._remove_space)

        setup_pickwalk_button = QtWidgets.QPushButton()
        setup_pickwalk_button.setMinimumSize(QtCore.QSize(40, 40))
        setup_pickwalk_button.setMaximumSize(QtCore.QSize(40, 40))
        setup_pickwalk_button.setStyleSheet(self.style)
        setup_pickwalk_button.setObjectName("settings")
        setup_pickwalk_button.setIconSize(QtCore.QSize(35, 35))
        setup_pickwalk_button.setIcon(pick_walk_icon)
        setup_pickwalk_button.setToolTip("Setup pick-walking between controls.")
        setup_pickwalk_button.clicked.connect(self._setup_pickwalks)

        buttonLayout1.addWidget(skin_tools_button)
        buttonLayout1.addWidget(export_meshes_button)
        buttonLayout1.addWidget(joint_override_button)
        buttonLayout1.addWidget(create_space_button)
        buttonLayout1.addWidget(create_global_space_button)
        buttonLayout1.addWidget(rename_space_button)
        buttonLayout1.addWidget(delete_space_button)
        buttonLayout1.addWidget(setup_pickwalk_button)
        buttonLayout1.addWidget(rig_history_button)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setToolbarVisibility(self):
        # Original Author: Jeremy Ernst
        state = self.toolFrame.isVisible()
        if state == True:
            self.toolFrame.setVisible(False)
        if state == False:
            self.toolFrame.setVisible(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setMoverVisibility(self):
        # Original Author: Jeremy Ernst

        movers = [["*_proxy_geo", self.geoDisplayBtn], ["*_lra", self.lraDisplayBtn],
                  ["*_bone_geo", self.boneDisplayBtn], ["*_mover_geo", self.meshMoverBtn],
                  ["*_mover_offset", self.offsetMoverBtn], ["*_mover", self.globalMoverBtn]]
        for mover in movers:
            self.toggleMoverVisibility(mover[0], mover[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def sortModules(self, sortMethod):
        # Original Author: Jeremy Ernst

        modules = utils.returnRigModules()
        modTypes = []
        modNames = []
        # get the module's type and name
        for module in modules:
            modType = cmds.getAttr(module + ".moduleType")
            modName = cmds.getAttr(module + ".moduleName")
            modTypes.append([modName, modType])
            modNames.append(str(modName))

        if sortMethod == "abc":
            # create a sorted list of that info
            modNames = sorted(modNames, key=str.lower)

            # create a list of the groupbox widgets sorted by alphabetical order
            groupBoxes = []
            for i in range(self.moduleSettingsLayout.count()):
                try:
                    groupBoxes.append([self.moduleSettingsLayout.itemAt(i).widget().title(),
                                       self.moduleSettingsLayout.itemAt(i).widget()])
                except:
                    pass

            # re-sort the groupboxes in the layout
            for each in modNames:
                for box in groupBoxes:
                    if box[0] == each:
                        self.moduleSettingsLayout.insertWidget(1, box[1])
                        self.moduleSettingsLayout.setDirection(QtWidgets.QBoxLayout.BottomToTop)

        if sortMethod == "type":
            # create a sorted list of that info
            sortedList = sorted(modTypes, key=lambda name: name[1])

            # create a list of the groupbox widgets sorted by module type
            groupBoxes = []
            for i in range(self.moduleSettingsLayout.count()):
                try:
                    groupBoxes.append([self.moduleSettingsLayout.itemAt(i).widget().title(),
                                       self.moduleSettingsLayout.itemAt(i).widget()])
                except:
                    pass
            # compare the sorted list to the list of groupboxes and make a new list that has those groupboxes in the
            # same order as the sorted list
            newList = []
            for item in sortedList:
                name = item[0]
                for box in groupBoxes:
                    title = box[0]
                    if title == name:
                        newList.append(box)

            # re-sort the groupboxes in the layout
            for i in range(len(newList)):
                self.moduleSettingsLayout.insertWidget(1, newList[i][1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def expandAllSettings(self, doExpand):
        # Original Author: Jeremy Ernst

        modules = utils.returnRigModules()

        for module in modules:
            modType = cmds.getAttr(module + ".moduleType")
            modName = cmds.getAttr(module + ".moduleName")
            mod = __import__("RigModules." + modType, {}, {}, [modType])

            # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
            moduleClass = getattr(mod, mod.className)

            # find the instance of that module and call on the skeletonSettings_UI function
            moduleInst = moduleClass(self, modName)

            if modType != "ART_Root":
                for i in range(self.moduleSettingsLayout.count()):
                    if type(self.moduleSettingsLayout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                        if self.moduleSettingsLayout.itemAt(i).widget().title() == modName:
                            self.moduleSettingsLayout.itemAt(i).widget().setChecked(doExpand)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addModule(self, baseName, className):
        # Original Author: Jeremy Ernst

        # This function gets called when a module button is pushed. It will grab some information from the user and
        # then add the network node, jointMover, and skelSettingsUI

        # delete the UI if it already exists
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        if cmds.window(mayaWindow + "|pyArtAddModuleUi", q=True, exists=True):
            cmds.deleteUI(mayaWindow + "|pyArtAddModuleUi")

        # run the user interface to gather information
        import Tools.Rigging.ART_AddModuleUI as ART_AddModuleUI
        inst = ART_AddModuleUI.ART_AddModule_UI(baseName, className, self, interfaceUtils.getMainWindow())
        inst.show()

        return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleButtonIcon(self, button, onIcon, offIcon):
        # Original Author: Jeremy Ernst

        state = button.isChecked()

        if state:
            icon = QtGui.QIcon(os.path.join(self.iconsPath, onIcon))
        else:
            icon = QtGui.QIcon(os.path.join(self.iconsPath, offIcon))

        button.setIcon(icon)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def previewSkeleton(self):
        """
        Builds a preview skeleton and constrains it to the joint mover. (or remove the preview skeleton)
        """

        # if the preview skeleton exists, set icon to off icon and delete skeleton
        if cmds.objExists("preview_root"):
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/boneDisplay.png"))
            self.boneDisplayBtn.setIcon(icon)
            cmds.delete("preview_root")

        # otherwise, build the skeleton, constrain to the LRAs, append a prefix, and change the button icon
        else:
            skeleton_data = riggingUtils.buildSkeleton()[0]
            for each in skeleton_data:
                cmds.parentConstraint(each[1], each[0])

            cmds.select("root", hi=True)
            selection = cmds.ls(sl=True)
            for each in selection:
                cmds.setAttr(each + ".overrideEnabled", 1)
                cmds.setAttr(each + ".overrideDisplayType", 2)
                cmds.rename(each, "preview_" + each)

            utils.xrayJoints()
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/boneDisplay_on.png"))
            self.boneDisplayBtn.setIcon(icon)

        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def editRigControls(self):

        state = self.ctrlDisplayBtn.isChecked()

        if state is True:
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/rigCtrlDisplay_On.png"))
            self.ctrlDisplayBtn.setIcon(icon)

            # get movers
            cmds.select("JointMover", hi=True)
            selection = cmds.ls(sl=True)

            # check for attrs
            attrs_to_check = ["fk_rig_control", "ik_rig_control"]

            for each in selection:
                for attr in attrs_to_check:
                    if cmds.objExists(each + "." + attr):

                        # if attrs exist, find connections
                        connection = cmds.listConnections(each + "." + attr)
                        if connection is not None:
                            # unlock vis and unhide connections
                            cmds.lockNode(connection[0], lock=False)
                            cmds.setAttr(connection[0] + ".visibility", lock=False)
                            cmds.setAttr(connection[0] + ".visibility", 1)


        else:
            icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/rigCtrlDisplay.png"))
            self.ctrlDisplayBtn.setIcon(icon)

            # get movers
            cmds.select("JointMover", hi=True)
            selection = cmds.ls(sl=True)

            # check for attrs
            attrs_to_check = ["fk_rig_control", "ik_rig_control"]

            for each in selection:
                for attr in attrs_to_check:
                    if cmds.objExists(each + "." + attr):

                        # if attrs exist, find connections
                        connection = cmds.listConnections(each + "." + attr)
                        if connection is not None:
                            # lock vis and hide connections
                            cmds.lockNode(connection[0], lock=False)
                            cmds.setAttr(connection[0] + ".visibility", lock=False)
                            cmds.setAttr(connection[0] + ".visibility", 0, lock=True)
                            cmds.lockNode(connection[0], lock=True)

        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleMoverVisibility_FromMenu(self, searchKey, button, onIcon, offIcon):
        # Original Author: Jeremy Ernst

        state = button.isChecked()
        if state:
            button.setChecked(False)
            icon = QtGui.QIcon(os.path.join(self.iconsPath, offIcon))
            button.setIcon(icon)

        else:
            button.setChecked(True)
            icon = QtGui.QIcon(os.path.join(self.iconsPath, onIcon))
            button.setIcon(icon)

        self.toggleMoverVisibility(searchKey, button)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleMoverVisibility(self, searchKey, button):
        # Original Author: Jeremy Ernst

        try:
            currentSelection = cmds.ls(sl=True)
            # get current checkbox state
            state = button.isChecked()

            # get the list of movers
            cmds.select(searchKey)
            movers = cmds.ls(sl=True)

            # find the mover shapes and set their visibility
            shapes = []
            for mover in movers:
                child = cmds.listRelatives(mover, children=True, shapes=True)
                if len(child) > 0:
                    shapes.append(mover + "|" + child[0])

            for shape in shapes:
                cmds.setAttr(shape + ".v", lock=False)
                cmds.setAttr(shape + ".v", state, lock=True)

            try:
                cmds.select(currentSelection)
            except:
                pass

        except:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveTemplate(self):

        # find all modules in the scene
        if cmds.objExists("ART_RIG_ROOT"):
            modules = cmds.listConnections("ART_RIG_ROOT.rigModules")
            module_data = {}

            # loop through each module, getting the required information
            for module in modules:

                attr_data = {}

                # get the module attributes and their values
                attrs = cmds.listAttr(module, ud=True, hd=True)
                for attr in attrs:
                    value = cmds.getAttr(module + "." + attr)
                    attr_data[str(attr)] = value

                # get all movers and their keyable values
                moduleName = cmds.getAttr(module + ".moduleName")
                moverTypes = ["_mover", "_mover_offset", "_mover_geo", "_mover_grp"]
                module_mover_data = {}

                for moverType in moverTypes:
                    try:
                        cmds.select(moduleName + "*" + moverType)
                        movers = cmds.ls(sl=True)
                        validMovers = []

                        # validate selection
                        for mover in movers:
                            moverGrp = moduleName + "_mover_grp"
                            validMovers.append(moverGrp)
                            children = cmds.listRelatives(moverGrp, ad=True)
                            if mover in children:
                                validMovers.append(str(mover))

                        # get mover values
                        for mover in validMovers:

                            attrs = cmds.listAttr(mover, keyable=True)

                            for attr in attrs:
                                value = cmds.getAttr(mover + "." + attr)
                                module_mover_data[str(mover + "." + attr)] = value

                    except Exception:
                        pass

                # add all of the mover data to the moduleData list
                module_data[str(module)] = [attr_data, module_mover_data]

            # ask for the file name to give the template
            startingDir = os.path.normcase(os.path.join(self.toolsPath, "Core/JointMover/Templates"))
            if not os.path.exists(startingDir):
                os.makedirs(startingDir)

            filename = cmds.fileDialog2(fm=0, okc="Save Template", dir=startingDir, ff="*.template")[0]

            # create the template file
            f = open(filename, 'w')

            # dump the data with json
            json.dump(module_data, f, indent=4, sort_keys=True)
            f.close()

            # print out confirmation
            print "Template has been saved"
            # inViewMessage only available in 2014 and up
            try:
                cmds.inViewMessage(amg=' <hl>Template has been saved.</hl>', pos='topCenter', fade=True)
            except:
                print "inViewMessage not supported"
                pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def loadTemplate(self):

        # make sure scene is new, and refresh UI
        if self.moduleSettingsLayout.count() > 2:
            self.unsavedChanges()
            return

        # turn renderer to default
        panels = cmds.getPanel(type='modelPanel')
        panelData = []
        for panel in panels:
            modelEditor = cmds.modelPanel(panel, q=True, modelEditor=True)
            renderSetting = cmds.modelEditor(modelEditor, q=True, rnm=True)
            panelData.append([modelEditor, renderSetting])
            cmds.modelEditor(modelEditor, edit=True, rnm="base_OpenGL_Renderer")

        # prompt for the file to load
        startingDir = os.path.normcase(os.path.join(self.toolsPath, "Core/JointMover/Templates"))
        if not os.path.exists:
            startingDir = self.toolsPath
        try:
            filename = cmds.fileDialog2(fm=1, okc="Load Template", dir=startingDir, ff="*.template")[0]
        except Exception:
            return

        if filename is not None:

            # load the data
            json_file = open(filename)
            data = json.load(json_file)
            json_file.close()

            # create a progress window
            progWindow = cmds.progressWindow(title='Loading Template', progress=0)
            amount = (100 / len(data))

            # go through the template data, adding the modules, the settings UI, and the joint mover
            completed = []
            to_do = copy.deepcopy(data)

            to_do.pop("ART_Root_Module")

            while len(to_do) > 0:
                for each in data:
                    if each not in completed:

                        module_info = data.get(each)
                        attr_data = module_info[0]
                        mover_data = module_info[1]
                        module_parent_bone = attr_data.get("parentModuleBone")
                        available_parents = utils.getViableParents()

                        if module_parent_bone in available_parents:
                            currentAmount = cmds.progressWindow(query=True, progress=True)
                            cmds.progressWindow(edit=True, progress=currentAmount + amount, status="Working on " + each)
                            self._load_template_data_for_module(attr_data, mover_data)
                            completed.append(each)
                            to_do.pop(each, None)

            # solve root mover last
            currentAmount = cmds.progressWindow(query=True, progress=True)
            cmds.progressWindow(edit=True, progress=currentAmount + amount)

            root_data = data.get("ART_Root_Module")
            mover_data = root_data[1]
            for mover in mover_data:
                value = mover_data.get(mover)
                try:
                    if ".visibility" not in mover:
                        cmds.setAttr(mover, value)
                except Exception:
                    pass

            cmds.progressWindow(endProgress=1)
            createUI()

        # set render settings back to what they were
        for each in panelData:
            cmds.modelEditor(each[0], edit=True, rnm=each[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_template_data_for_module(self, attr_data, mover_data):

        module_name = attr_data.get("moduleName")
        module_class = attr_data.get("moduleType")

        mod = __import__("RigModules." + module_class, {}, {}, [module_class])
        moduleClass = getattr(mod, mod.className)
        jmPath = mod.jointMover
        if self.up == "y":
            jmPath = jmPath.replace("z_up", "y_up")
        moduleInst = moduleClass(self, module_name)
        networkNode = moduleInst.buildNetwork()

        # set the attributes on the network node
        moduleInst.applyTemplate(attr_data, networkNode)

        # todo: this is some broken window shit. Nasty. Fix this!
        # arm/leg exceptions
        specialCaseModules = ["ART_Leg_Standard", "ART_Arm_Standard"]
        if module_class in specialCaseModules:
            side = cmds.getAttr(networkNode + ".side")
            jmPath = jmPath.partition(".ma")[0] + "_" + side + ".ma"

        # torso exception
        if module_class == "ART_Torso":
            numSpine = int(cmds.getAttr(networkNode + ".spineJoints"))
            jmPath = jmPath.partition(".ma")[0].rpartition("_")[0] + "_" + str(numSpine) + "Spine.ma"

        # head exception
        if module_class == "ART_Head":
            numNeck = int(cmds.getAttr(networkNode + ".neckJoints"))
            jmPath = jmPath.partition(".ma")[0].rpartition("_")[0] + "_" + str(numNeck) + "Neck.ma"

        # build settings UI/build JM/Add to Outliner
        moduleInst.skeletonSettings_UI(module_name)
        moduleInst.jointMover_Build(jmPath)
        moduleInst.addJointMoverToOutliner()
        moduleInst.applyModuleChanges(moduleInst)

        # copy, reset, and paste settings to update the UI/scene one last time
        skipModules = ["ART_Torso", "ART_Head"]
        if module_class not in skipModules:
            moduleInst.copySettings()
            moduleInst.resetSettings()
            moduleInst.pasteSettings()
        self.moduleInstances.append(moduleInst)

        # Apply the positional data
        for mover in mover_data:
            value = mover_data.get(mover)
            try:
                cmds.setAttr(mover, value)
            except Exception:
                pass

        # bake offsets
        moduleInst.bakeOffsets()

        parent = attr_data.get("parentModuleBone")
        mover = ""
        if parent == "root":
            mover = "root_mover"

        else:
            # find the parent mover name to parent to
            networkNodes = utils.returnRigModules()
            mover = utils.findMoverNodeFromJointName(networkNodes, parent, False, True)
            if mover is None:
                mover = utils.findMoverNodeFromJointName(networkNodes, parent, True, False)

        if mover is not None:
            cmds.parentConstraint(mover, module_name + "_mover_grp", mo=True)
            cmds.scaleConstraint(mover, module_name + "_mover_grp", mo=True)

        globalMover = utils.findGlobalMoverFromName(module_name)
        cmds.select(globalMover)
        cmds.setToolTo("moveSuperContext")
        utils.fitViewAndShade()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findRigModules(self):
        # Original Author: Jeremy Ernst

        # get rig module files
        modulesLocation = os.path.normcase(os.path.join(self.toolsPath, "Core/Scripts/RigModules"))
        files = os.listdir(modulesLocation)
        modules = []

        for f in files:
            if f.rpartition(".")[2] == "py":
                modules.append(f)

        for mod in modules:
            niceName = mod.rpartition(".")[0]
            if niceName != "__init__" and niceName != "ART_Root":
                # create the push button for the module and set the size
                button = QtWidgets.QPushButton()
                button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
                button.setMinimumSize(QtCore.QSize(125, 30))
                button.setMaximumSize(QtCore.QSize(125, 30))
                button.setObjectName("module")

                # get the icon path from the module and add the icon to the push button
                module = __import__("RigModules." + niceName, {}, {}, [niceName])

                searchTerm = module.search
                className = module.className
                baseName = module.baseName
                displayName = module.displayName
                tooltip_image = module.tooltip_image

                button.setText(displayName)
                interfaceUtils.setCustomToolTip(tooltip_image, button)

                # set properties for filtering later
                button.setProperty("name", searchTerm)
                self.moduleLayout.addWidget(button)

                # setup signal
                button.clicked.connect(partial(self.addModule, baseName, className))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def searchModules(self):
        # Original Author: Jeremy Ernst

        searchText = self.moduleSearch.text()

        for i in range(self.moduleLayout.count()):
            if type(self.moduleLayout.itemAt(i).widget()) == QtWidgets.QPushButton:
                self.moduleLayout.itemAt(i).widget().setVisible(False)
                moduleType = self.moduleLayout.itemAt(i).widget().property("name")
                searchKeys = moduleType.split(":")

                for key in searchKeys:
                    if key.find(searchText) != -1:
                        self.moduleLayout.itemAt(i).widget().setVisible(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def searchInstalled(self):
        # Original Author: Jeremy Ernst

        searchText = self.installedSearch.text()

        for i in range(self.moduleSettingsLayout.count()):
            if type(self.moduleSettingsLayout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                self.moduleSettingsLayout.itemAt(i).widget().setVisible(False)
                title = self.moduleSettingsLayout.itemAt(i).widget().title()

                if title.find(searchText) != -1:
                    self.moduleSettingsLayout.itemAt(i).widget().setVisible(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def editSetup(self):
        # Original Author: Jeremy Ernst

        # set model pose if exists
        for inst in self.moduleInstances:
            networkNode = inst.returnNetworkNode
            if cmds.objExists(networkNode + ".modelPose"):
                inst.setReferencePose("modelPose")

        # remove weight table script job
        cmds.scriptJob(kill=self.skinToolsInst.wtScriptJob)

        # show index 0 of stacked widget
        self.toolModeStack.setCurrentIndex(0)

        # change state in network node
        cmds.setAttr("ART_RIG_ROOT.state", 0)

        # find meshes that are weighted
        weightedMeshes = []
        skinClusters = cmds.ls(type='skinCluster')

        for cluster in skinClusters:
            geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
            geoTransform = cmds.listRelatives(geometry, parent=True, fullPath=True)[0]
            transform_name = geoTransform.rpartition("|")[2]
            if geoTransform.find("proxy_geo") == -1:
                weightedMeshes.append([geoTransform, cluster, transform_name])

        # save out weights of meshes
        for mesh in weightedMeshes:
            filePath = utils.returnFriendlyPath(os.path.join(cmds.internalVar(utd=True), mesh[2] + ".WEIGHTS"))
            print "saving out skin weights for " + mesh[2] + " at: " + filePath

            # export skin weights
            skin = riggingUtils.export_skin_weights(filePath, mesh[0])

            # delete history of meshes
            cmds.delete(mesh[0], ch=True)

        # delete skeleton
        cmds.delete("root")

        # delete proxy geo grp if it exists
        if cmds.objExists("skinned_proxy_geo"):
            cmds.delete("skinned_proxy_geo")

        # unhide/lock joint mover
        cmds.select("JointMover", hi=True)
        jmNodes = cmds.ls(sl=True)
        for node in jmNodes:
            cmds.lockNode(node, lock=False)

        lockNodes = cmds.listRelatives("JointMover", children=True)
        for node in lockNodes:
            cmds.setAttr(node + ".v", lock=False)
            cmds.setAttr(node + ".v", 1)

        for inst in self.moduleInstances:
            inst.lock_nodes()

        # clear selection
        cmds.select(clear=True)

        # recreate outliner scriptjobs
        self.scriptJobs = []
        for module in self.moduleInstances:
            module.createScriptJob()

    ##############################################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # EXTERNAL FILE CALLS
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ##############################################################################################################

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def overrideJointNames_UI(self):

        import Tools.Rigging.Interfaces.ART_OverrideJointNames_UI as ojn
        ojn.run()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildDeformation_UI(self):
        # Original Author: Jeremy Ernst

        import Tools.Rigging.ART_SkinTools as ART_SkinTools
        self.skinToolsInst = ART_SkinTools.ART_SkinTools(self, True, self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def deformationTools(self):
        # Original Author: Jeremy Ernst

        import Tools.Rigging.ART_SkinTools as ART_SkinTools
        self.skinToolsInst = ART_SkinTools.ART_SkinTools(self, False, interfaceUtils.getMainWindow())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def aimModeUI(self):
        # Original Author: Jeremy Ernst

        from Tools.Rigging import ART_AimModeUI
        ART_AimModeUI.ART_AimMode(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pinModulesUI(self):
        # Original Author: Jeremy Ernst
        import Tools.Rigging.ART_PinModules as ART_PinModules
        ART_PinModules.ART_PinModules(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def bakeOffsetsUI(self):
        # Original Author: Jeremy Ernst

        from Tools.Rigging import ART_BakeOffsetsUI
        ART_BakeOffsetsUI.ART_BakeOffsets(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boneCounterUI(self):
        # Original Author: Jeremy Ernst

        from Tools.Rigging import ART_BoneCounter
        inst = ART_BoneCounter.ART_BoneCounter(self)
        self.boneCounterInst = inst

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def editPhysique(self):
        # Original Author: Jeremy Ernst

        from Tools.Rigging import ART_PhysiqueEditorUI
        inst = ART_PhysiqueEditorUI.run(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetModeUI(self):

        from Tools.Rigging import ART_ResetModeUI
        ART_ResetModeUI.ART_ResetMode(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def symmetryModeUI(self):
        # Original Author: Jeremy Ernst

        from Tools.Rigging import ART_SymmetryModeUI
        ART_SymmetryModeUI.ART_SymmetryMode(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def finalizeSetup_UI(self):
        # Original Author: Jeremy Ernst

        if cmds.objExists("preview_root"):
            cmds.delete("preview_root")

        for module in utils.return_module_instances():
            network_node = module.returnNetworkNode
            module.pinModule(False)
            cmds.setAttr(network_node + ".pinned", lock=False)
            cmds.setAttr(network_node + ".pinned", False, lock=True)

            # If the module's joint positions have changed, remove the rig pose if it exists.
            if cmds.objExists(network_node + ".modelPose"):
                previous_pose = json.loads(cmds.getAttr(network_node + ".modelPose"))
                pose_data = module.getReferencePose("modelPose", zeroPose=False, return_only=True)
                pose_string = json.dumps(pose_data)
                current_pose = json.loads(pose_string)

                if previous_pose != current_pose:
                    if cmds.objExists(network_node + ".rigPose"):
                        cmds.deleteAttr(network_node + ".rigPose")
                    if cmds.objExists(network_node + ".rigPoseState"):
                        cmds.deleteAttr(network_node + ".rigPoseState")
                    print "deleted rig pose data for " + network_node

        from Tools.Rigging import ART_FinalizeSetup
        ART_FinalizeSetup.ART_FinalizeSetup(self, self.skinToolsInst)
        # need to also pass in deformation ui instance

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRig(self):
        # Original Author: Jeremy Ernst

        # run publish process
        from Tools.Rigging import ART_Publish
        ART_Publish.ART_Publish(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeRigging(self):
        # Original Author: Jeremy Ernst

        # reset scale if needed
        if cmds.objExists("master_anim.globalScale"):
            cmds.setAttr("master_anim.globalScale", 1)
        cmds.refresh()

        # disconnect main deformation hierarchy
        cmds.select("root", hi=True)
        joints = cmds.ls(sl=True, type="joint")

        for joint in joints:
            attrs = ["translate", "rotate", "scale"]
            for attr in attrs:
                try:
                    cmds.disconnectAttr("driver_" + joint + "." + attr, joint + "." + attr)
                except Exception, e:
                    print str(e)

        # unlock nodes
        cmds.select("rig_grp", hi=True)
        rigNodes = cmds.ls(sl=True)
        for node in rigNodes:
            cmds.lockNode(node, lock=False)

        # go through each rig and delete that module's rigging
        for module in self.moduleInstances:
            module.deleteRig()

        # set the state of the character
        self.toolModeStack.setCurrentIndex(1)
        if cmds.objExists("ART_RIG_ROOT.state"):
            cmds.setAttr("ART_RIG_ROOT.state", 1)

        # remove outliner scriptJobs
        for job in self.scriptJobs:
            cmds.scriptJob(kill=job, force=True)

        # build the scriptJob for the weight table
        self.scriptJobs.append(self.skinToolsInst.weightTable_scriptJob())

        # delete driver skeleton
        if cmds.objExists("driver_root"):
            cmds.delete("driver_root")

        # set model pose
        for inst in self.moduleInstances:
            networkNode = inst.returnNetworkNode

            # unlock network node
            if networkNode is not None:
                cmds.lockNode(networkNode, lock=False)

                if cmds.objExists(networkNode + ".modelPose"):
                    inst.setSkeletonPose("modelPose")

        # remove the skeletal constraints
        for inst in self.moduleInstances:
            networkNode = inst.returnNetworkNode
            if networkNode is not None:
                if cmds.objExists(networkNode + ".modelPose"):
                    inst.removeSkeletalConstraints()

        # unhide joints
        cmds.select("root", hi=True)
        joints = cmds.ls(sl=True)
        for joint in joints:
            cmds.setAttr(joint + ".v", lock=False)
            cmds.setAttr(joint + ".v", 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def rigHistoryUI(self):

        import Tools.Rigging.ART_RigHistoryUI as arh
        arh.ART_RigHistoryUI(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_space(self):

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
        ssui.create_space(None, None)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_global_spaces(self):

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
        ssui.create_global_spaces()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _rename_space(self):

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui

        control = None
        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            if cmds.objExists(selection[0] + ".follow"):
                control = selection[0]

        ssui.rename_space(control)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _remove_space(self):

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui

        control = None
        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            if cmds.objExists(selection[0] + ".follow"):
                control = selection[0]

        ssui.delete_space(control)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _setup_pickwalks(self):

        import Tools.Animation.Interfaces.ART_PickWalkSetupUI as ART_PickWalkSetupUI
        ART_PickWalkSetupUI.run()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def moduleStatusUI(self):

        import Tools.Rigging.ART_ModuleStatus as ART_ModuleStatus
        ART_ModuleStatus.run(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def unsavedChanges(self):
        # Original Author: Jeremy Ernst

        # message box for letting user know current file has unsaved changes
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Current File Has Unsaved Changes!")
        msgBox.setDetailedText("To load a template, please create a new file and re-launch the tool.")
        ret = msgBox.exec_()

        return ret

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def exportMeshes(self):
        # Original Author: Jeremy Ernst

        # run publish process
        from Tools.Rigging import ART_ExportMeshes
        inst = ART_ExportMeshes.ART_ExportMeshes(self, parent=interfaceUtils.getMainWindow())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectNetworkNode(self):

        selection = self.nodeNetworkList.currentItem()
        cmds.select(selection.text())


##############################################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NON-CLASS FUNCTIONS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##############################################################################################################


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createUI():
    # Original Author: Jeremy Ernst

    global parent
    global gui

    try:

        gui.close()
        gui.deleteLater()

    except:
        pass

    # if the rigCreatorUI exists delete UI
    if cmds.dockControl("pyArtRigCreatorDock", q=True, exists=True):
        cmds.deleteUI(windowObject)
        cmds.deleteUI("pyArtRigCreatorDock", control=True)

    # create an instance of the UI and add it to a Maya dock
    gui = ART_RigCreator_UI(interfaceUtils.getMainWindow())
    allowedAreas = ["left", "right"]
    dockControl = cmds.dockControl("pyArtRigCreatorDock", area="right", content=windowObject, allowedArea=allowedAreas,
                                   label=windowTitle, w=450, h=500)
    cmds.refresh(force=True)
    cmds.dockControl("pyArtRigCreatorDock", e=True, r=True)
    return gui
