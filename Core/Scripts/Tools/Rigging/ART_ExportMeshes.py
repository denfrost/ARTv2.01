"""
Author: Jeremy Ernst
"""

import json
import os
from functools import partial

import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_ExportMeshes(QtWidgets.QMainWindow):
    """
    This class is used to export skeletal meshes and skeletal mesh LODs.

    The UI has a robust suite of tools for managing LODs, bone removal for LODs, choosing
    which meshes are associated with a LOD, where weighting from removed bones will get transferred,
    and setting/viewing LOD poses (useful if you wanted to remove finger bones for a LOD, but not have
    "paddle hands"

        .. image:: /images/exportMeshes.png

    A look at the LOD tools for transferring weighting and managing LOD poses:

        .. image:: /images/lodTool.png

    """

    def __init__(self, mainUI, parent=None):
        """
        Instantiates the class, getting the QSettings, presenting a QMessageBox about saving the current file,
        creates a temporary file to do the export work out of (stripping out the rig and removing all connections
        from joints), set the model pose, then calls on the UI build.

        :param mainUI: Instance of the Rig Creator interface, from which this class was called.

        .. seealso:: ART_ExportMeshes.buildUI(), ART_ExportMeshes.populateUI()

        """

        super(ART_ExportMeshes, self).__init__(parent)

        if cmds.window("pyART_ExportMeshesWin", exists=True):
            cmds.deleteUI("pyART_ExportMeshesWin", wnd=True)

        # get settings
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")
        self.projectPath = settings.value("projectPath")

        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # class vars
        self.mainUI = mainUI
        self.lodPoseDict = {}

        # get current file
        self.saveFile = cmds.file(q=True, sceneName=True)

        # message box for confirming save action
        msgBax = QtWidgets.QMessageBox()
        msgBax.setText(
            "Please make sure any changes to the current file are saved before continuing. This process will be "
            "creating a temporary file to do all of the exporting from.")
        msgBax.setIcon(QtWidgets.QMessageBox.Warning)
        msgBax.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBax.setDefaultButton(QtWidgets.QMessageBox.Ok)
        ret = msgBax.exec_()

        if ret == QtWidgets.QMessageBox.Ok:

            # save file as a new temporary file
            self.tempFile = os.path.join(os.path.dirname(self.saveFile), "exportFile.ma")
            cmds.file(rename=self.tempFile)
            cmds.file(save=True)

            # remove all skeleton connections
            cmds.select("root", hi=True)
            selection = cmds.ls(sl=True)
            for each in selection:
                connT = cmds.connectionInfo(each + ".translate", sourceFromDestination=True)
                if connT != '':
                    cmds.disconnectAttr(connT, each + ".translate")
                connR = cmds.connectionInfo(each + ".rotate", sourceFromDestination=True)
                if connR != '':
                    cmds.disconnectAttr(connR, each + ".rotate")
                connS = cmds.connectionInfo(each + ".scale", sourceFromDestination=True)
                if connS != '':
                    cmds.disconnectAttr(connS, each + ".scale")

            # remove rig and driver skeleton
            cmds.select("rig_grp", hi=True)
            selection = cmds.ls(sl=True)

            for each in selection:
                cmds.lockNode(each, lock=False)

            cmds.delete("rig_grp")
            cmds.delete("driver_root")

            # show all joints
            cmds.select("root", hi=True)
            joints = cmds.ls(sl=True)
            for joint in joints:
                cmds.setAttr(joint + ".v", lock=False)
                cmds.setAttr(joint + ".v", 1)

            # build UI
            self.buildUI()

            # populate UI
            self.populateUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):
        """
        Gathers all information from the temp file (LOD meshes, bones to remove, etc), opens the export file,
        and applies that information to the network node in the export file. Lastly removes the temp file.

        """

        # save out data
        exportData = utils.findExportMeshData()

        # open original file
        cmds.file(self.saveFile, open=True, force=True)
        cmds.refresh(force=True)

        # apply data
        characterNode = utils.returnCharacterModule()

        lodData = ["_Pose", "_Bones", "_Meshes", "_FilePath"]

        for each in exportData:
            # path, meshes, removeBones, poseData, lodAttr
            for d in lodData:

                # if the attr does not exist, create it
                if not cmds.objExists(characterNode + "." + each[4] + d):
                    if d != "_Meshes":
                        cmds.addAttr(characterNode, ln=each[4] + d, dt="string")
                    else:
                        cmds.addAttr(characterNode, ln=each[4] + d, at="message")

            # set the attr data
            dataString = json.dumps(each[0])
            cmds.setAttr(characterNode + "." + each[4] + "_FilePath", dataString, type="string")

            dataString = json.dumps(each[2])
            cmds.setAttr(characterNode + "." + each[4] + "_Bones", dataString, type="string")

            dataString = json.dumps(each[3])
            cmds.setAttr(characterNode + "." + each[4] + "_Pose", dataString, type="string")

            # first remove all connections
            i = each[4].partition("_")[2]
            connections = cmds.listConnections(characterNode + "." + each[4] + "_Meshes")
            if connections is not None:
                for conn in connections:
                    cmds.disconnectAttr(characterNode + "." + each[4] + "_Meshes", conn + ".lodGroup" + str(i))

            # Add attrs to meshes to connect up to the characterNode LOD meshes attr
            for mesh in each[1]:
                if not cmds.objExists(mesh + ".lodGroup" + str(i)):
                    cmds.addAttr(mesh, sn="lodGroup" + str(i), at="message")
                cmds.connectAttr(characterNode + "." + each[4] + "_Meshes", mesh + ".lodGroup" + str(i))

        # remove temp file
        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)

        # message box for confirming save action
        msgBax = QtWidgets.QMessageBox()
        msgBax.setText("Save file to retain export data?")
        msgBax.setDetailedText("In order to retain the export data you just setup (export file paths, meshes,"
                               " bones to remove, LOD poses, etc), you must save your file.")
        msgBax.setIcon(QtWidgets.QMessageBox.Question)
        msgBax.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBax.setDefaultButton(QtWidgets.QMessageBox.Ok)
        ret = msgBax.exec_()

        QtWidgets.QMainWindow.closeEvent(self, event)

        if ret == QtWidgets.QMessageBox.Ok:
            # save the file
            try:
                cmds.file(save=True)
            except Exception, e:
                cmds.error("Could not save file. Error: " + str(e))
                return

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        """
        Builds the main interface for the tool, which allows additions of LODs, assignment of meshes to a given LOD,
        and assignment of bones to remove per LOD (which then opens another interface/tool).

        .. seealso:: ART_ExportMeshes.addBoneToList_UI(), ART_ExportMeshes.addMeshToList_UI()
        .. seealso:: ART_ExportMeshes.addMeshLOD(), ART_ExportMeshes.createLODpage()
        .. seealso:: ART_ExportMeshes.createExportMeshesPage(), ART_ExportMeshes.removeLodTab()
        .. seealso:: ART_ExportMeshes.export()

        Here is a breakdown image showing which UI elements call on which functions:

        .. image:: /images/exportMeshesBreakout.png

        """

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setStyleSheet(self.style)
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName("pyART_ExportMeshesWin")
        self.setWindowTitle("Export Skeletal Meshes")

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # set size policy
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.resize(600, 400)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(600, 400))
        self.setMaximumSize(QtCore.QSize(600, 400))

        # build pages
        self.createExportMeshesPage()

        # show window
        self.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createExportMeshesPage(self):
        """
        Creates the LOD0 Tab, which is a little bit unique from subsequent LOD tabs, as the Add/Remove LOD buttons
        are added, and the LOD0 tab can not be removed. It still calls on createLODpage to create the common
        elements, but this creates the framework for all of the LOD tabs.

        .. seealso:: ART_ExportMeshes.createLODpage()

        """

        # create the QFrame for this page
        self.exportMeshPage = QtWidgets.QFrame()
        self.exportMeshPage.setStyleSheet(self.style)
        self.exportMeshPage.setMinimumSize(560, 250)
        self.layout.addWidget(self.exportMeshPage)
        self.emPageMainLayout = QtWidgets.QVBoxLayout(self.exportMeshPage)
        self.exportMeshPage.setStyleSheet(self.style)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        # add Tab Widget
        # tab stylesheet (tab stylesheet via QSS doesn't seem to work for some reason
        self.tab_style = interfaceUtils.get_style_sheet("tabs")

        self.emPageTabs = QtWidgets.QTabWidget()
        self.emPageTabs.setStyleSheet(self.tab_style)
        self.emPageMainLayout.addWidget(self.emPageTabs)

        self.emPageTabBar = QtWidgets.QTabBar()
        self.emPageTabs.setTabBar(self.emPageTabBar)
        self.emPageTabBar.setContentsMargins(0, 0, 0, 0)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # LOD0 tab
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.createLODpage("LOD_0", False)

        cornerWidget = QtWidgets.QWidget()
        cornerLayout = QtWidgets.QHBoxLayout(cornerWidget)
        cornerLayout.setContentsMargins(0, 0, 0, 10)

        # remove lod button
        self.removeMeshLodBtn = QtWidgets.QPushButton("   -   ")
        self.removeMeshLodBtn.setObjectName("orange")
        self.removeMeshLodBtn.setMinimumHeight(20)
        self.removeMeshLodBtn.setToolTip("Remove Mesh LOD (current tab)")
        cornerLayout.addWidget(self.removeMeshLodBtn)
        self.removeMeshLodBtn.clicked.connect(self.removeLodTab)

        # add lod button
        self.addMeshLodBtn = QtWidgets.QPushButton("   +   ")
        self.addMeshLodBtn.setObjectName("orange")
        self.addMeshLodBtn.setMinimumHeight(20)
        self.addMeshLodBtn.setToolTip("Add Mesh LOD")
        cornerLayout.addWidget(self.addMeshLodBtn)
        self.addMeshLodBtn.clicked.connect(partial(self.addMeshLOD))

        self.emPageTabs.setCornerWidget(cornerWidget)

        # add continue/back buttons
        buttonlayout = QtWidgets.QHBoxLayout()
        self.emPageMainLayout.addLayout(buttonlayout)

        spacerItem = QtWidgets.QSpacerItem(300, 0)
        buttonlayout.addSpacerItem(spacerItem)

        self.emPage_continueButton = QtWidgets.QPushButton("Export")
        buttonlayout.addWidget(self.emPage_continueButton)
        self.emPage_continueButton.setFont(font)
        self.emPage_continueButton.setMinimumSize(250, 50)
        self.emPage_continueButton.setMaximumSize(250, 50)
        self.emPage_continueButton.clicked.connect(partial(self.export))
        self.emPage_continueButton.setObjectName("settings")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createLODpage(self, label, closeable):
        """
        Creates a tab (QFrame) for a new LOD, with the UI elements to set the output path for the FBX, to set the
        meshes assigned to the LOD, and to launch the bone removal tool for the LOD.

        :param label: The text label for the tab (LOD_#)
        :param closeable: Whether this LOD can be removed, thus removing the tab.

        """

        lodTab = QtWidgets.QFrame()
        lodTab.setObjectName("darkborder")
        lodTab.setStyleSheet(self.style)

        self.emPageTabs.addTab(lodTab, label)

        # horizontal layout
        mainLayout = QtWidgets.QHBoxLayout(lodTab)

        # left side column
        leftSide = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(leftSide)

        # label
        meshLayout = QtWidgets.QHBoxLayout()
        leftSide.addLayout(meshLayout)
        layoutLabel = QtWidgets.QLabel("Meshes For " + label + ":")
        meshLayout.addWidget(layoutLabel)
        layoutLabel.setStyleSheet('background: transparent')

        chooseBtn = QtWidgets.QPushButton("Choose Meshes")
        chooseBtn.setObjectName("settings")
        chooseBtn.setMinimumHeight(30)
        meshLayout.addWidget(chooseBtn)

        # render mesh list
        meshList = QtWidgets.QListWidget()
        meshList.setToolTip("Select the meshes you want to include in this mesh LOD.")
        meshList.setProperty("listType", "mesh")
        leftSide.addWidget(meshList)
        meshList.setToolTip("List of meshes to include for this LOD")
        meshList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        chooseBtn.clicked.connect(partial(self.addMeshToList_UI, self, label, meshList))

        # right side column
        rightLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(rightLayout)

        # horizontal layout for line edit and button
        pathLayout = QtWidgets.QHBoxLayout()
        rightLayout.addLayout(pathLayout)

        lineEdit = QtWidgets.QLineEdit()
        pathLayout.addWidget(lineEdit)
        lineEdit.setMinimumHeight(35)
        lineEdit.setMaximumHeight(35)
        lineEdit.setObjectName("light")
        lineEdit.setPlaceholderText("FBX Export Path...")
        lineEdit.setToolTip("Define the file name and file location for this LOD FBX file.")
        lineEdit.textChanged.connect(partial(self.saveFilePath, lineEdit, label))

        browseBtn = QtWidgets.QPushButton()
        browseBtn.setMinimumSize(35, 35)
        browseBtn.setMaximumSize(35, 35)
        browseBtn.setObjectName("settings")
        pathLayout.addWidget(browseBtn)
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/fileBrowse.png"))
        browseBtn.setIconSize(QtCore.QSize(30, 30))
        browseBtn.setIcon(icon)
        browseBtn.clicked.connect(partial(self.browseToFBX, lineEdit))

        # label + add button
        removeBonesLayout = QtWidgets.QHBoxLayout()
        rightLayout.addLayout(removeBonesLayout)

        layoutLabel = QtWidgets.QLabel("Bones to remove for " + label + ":")
        removeBonesLayout.addWidget(layoutLabel)
        layoutLabel.setStyleSheet('background: transparent;')

        removeBtn = QtWidgets.QPushButton("+")
        removeBtn.setMinimumSize(35, 35)
        removeBtn.setMaximumSize(35, 35)
        removeBonesLayout.addWidget(removeBtn)
        removeBtn.setObjectName("settings")

        # bone list
        boneList = QtWidgets.QListWidget()
        boneList.setProperty("listType", "bone")
        rightLayout.addWidget(boneList)
        boneList.setToolTip("List of joints to remove from this LOD")
        boneList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        boneList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # signals/slots
        removeBtn.clicked.connect(partial(self.addBoneToList_UI, self, label, boneList))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addBoneToList_UI(self, parent, label, listWidget):
        """
        Creates an interface to remove bones from a LOD, transfer weighting of those removed bones to the next viable
        parent, and handle LOD posing.

        :param parent: The instance of the main UI created by ART_ExportMeshes.buildUI()
        :param label: The label for the window title to show what LOD this interface represents.
        :param listWidget: The list widget on the main LOD page that lists all bones being removed.

        .. seealso::  ART_ExportMeshes.addBoneToList_Accept(), ART_ExportMeshes.addWeightingTransferEntry()
        .. seealso::  ART_ExportMeshes.viewLodPose(), ART_ExportMeshes.resetLodPose(), ART_ExportMeshes.resetLodPose()

        """

        # create the main window
        mainWin = QtWidgets.QMainWindow(parent)
        mainWin.setStyleSheet(self.style)

        # create the main widget
        mainWidget = QtWidgets.QFrame()
        mainWin.setCentralWidget(mainWidget)
        mainWin.setMinimumSize(725, 525)
        mainWin.setMaximumSize(725, 525)

        # set qt object name
        mainWin.setObjectName("ART_AddBoneToLODlistWin")
        mainWin.setWindowTitle(label)

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # create the mainLayout for the rig creator UI
        layout = QtWidgets.QVBoxLayout(mainWidget)
        mainLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(mainLayout)

        # treeWidget
        self.tree = QtWidgets.QTreeWidget()
        mainLayout.addWidget(self.tree)
        self.tree.headerItem().setText(0, "")
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree.setMinimumSize(QtCore.QSize(260, 470))
        self.tree.setMaximumSize(QtCore.QSize(260, 470))

        self.tree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tree.headerItem().setText(0, "Skeleton Tree")
        self.tree.setColumnWidth(0, 260)
        self.tree.setIndentation(10)

        # right side
        rightLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(rightLayout)

        # Weighting Transfer
        xferGroupBox = QtWidgets.QGroupBox("Weighting Transfer")
        rightLayout.addWidget(xferGroupBox)
        xferGroupBox.setMinimumSize(QtCore.QSize(425, 330))
        xferGroupBox.setMaximumSize(QtCore.QSize(425, 330))
        xferGroupBox.setObjectName("mid")

        # vboxLayout--hbox button layout for spacer/button, vboxlayout/scroll area for entries
        weightingXferLayout = QtWidgets.QVBoxLayout(xferGroupBox)
        rightLayout.addLayout(weightingXferLayout)

        buttonLayout = QtWidgets.QHBoxLayout()
        weightingXferLayout.addLayout(buttonLayout)
        buttonLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        addEntryButton = QtWidgets.QPushButton("  Add Entry  ")
        addEntryButton.setObjectName("settings")
        addEntryButton.setMinimumHeight(30)
        buttonLayout.addWidget(addEntryButton)

        # ScrollArea
        scrollLayout = QtWidgets.QVBoxLayout()
        weightingXferLayout.addLayout(scrollLayout)

        scrollArea = QtWidgets.QScrollArea()
        scrollLayout.addWidget(scrollArea)

        scrollContents = QtWidgets.QFrame()
        scrollContents.setObjectName("dark")
        scrollArea.setWidget(scrollContents)

        entriesLayout = QtWidgets.QVBoxLayout(scrollContents)
        scrollArea.setWidgetResizable(True)

        entriesLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # LOD Pose
        lodPoseGroupBox = QtWidgets.QGroupBox("LOD Posing")
        rightLayout.addWidget(lodPoseGroupBox)
        lodPoseGroupBox.setMinimumSize(QtCore.QSize(425, 75))
        lodPoseGroupBox.setMaximumSize(QtCore.QSize(425, 75))

        lodPoseLayout = QtWidgets.QHBoxLayout(lodPoseGroupBox)

        viewPoseBtn = QtWidgets.QPushButton("View LOD Pose")
        viewPoseBtn.setCheckable(True)
        viewPoseBtn.setObjectName("settings")
        viewPoseBtn.setMinimumHeight(30)
        lodPoseLayout.addWidget(viewPoseBtn)
        viewPoseBtn.clicked.connect(partial(self.viewLodPose, label, viewPoseBtn))

        resetPoseBtn = QtWidgets.QPushButton("Reset LOD Pose")
        lodPoseLayout.addWidget(resetPoseBtn)
        resetPoseBtn.setObjectName("settings")
        resetPoseBtn.setMinimumHeight(30)
        resetPoseBtn.clicked.connect(partial(self.resetLodPose, label))

        savePoseBtn = QtWidgets.QPushButton("Save LOD Pose")
        lodPoseLayout.addWidget(savePoseBtn)
        savePoseBtn.setMinimumHeight(30)
        savePoseBtn.setObjectName("settings")
        savePoseBtn.clicked.connect(partial(self.saveLodPose, label))

        # button
        addButton = QtWidgets.QPushButton("Save and Close")
        addButton.setMinimumHeight(40)
        addButton.setMaximumHeight(40)
        rightLayout.addWidget(addButton)
        addButton.clicked.connect(
            partial(self.addBoneToList_Accept, self.tree, listWidget, label, entriesLayout, viewPoseBtn))
        addButton.setObjectName("settings")

        addEntryButton.clicked.connect(partial(self.addWeightingTransferEntry, entriesLayout))

        # joints
        cmds.select("root", hi=True)
        joints = cmds.ls(sl=True, type="joint")

        for joint in joints:
            parent = cmds.listRelatives(joint, parent=True)

            if parent is None:
                item = QtWidgets.QTreeWidgetItem(self.tree)
                item.setText(0, joint)
                item.setBackground(0, QtCore.Qt.NoBrush)

                children = cmds.listRelatives(joint, children=True, type="joint")
                for child in children:
                    self.addBoneToListUI_addChildren(child, item)

        # show
        self.tree.expandAll()
        mainWin.show()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # populate ui automatically if the settings exist
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        characterNode = utils.returnCharacterModule()
        attrs = cmds.listAttr(characterNode, ud=True, string="LOD_*_Bones")
        lodAttrs = []

        if attrs is not None:
            for attr in attrs:
                lodAttrs.append(attr.partition("_Bones")[0])

        if lodAttrs is not None:

            # get json data from attribute
            lodData = ["_Bones"]
            boneValues = []

            for attr in lodAttrs:
                if attr == label:
                    for entry in lodData:
                        if cmds.objExists(characterNode + "." + attr + entry):
                            if entry == "_Bones":
                                boneValues = json.loads(cmds.getAttr(characterNode + "." + attr + entry))

            for item in boneValues:
                bones = item[1]
                xferBone = item[0]

                # create an entry (need to return back the layouts needed for the next part
                entryData = self.addWeightingTransferEntry(entriesLayout)
                self.tree.clearSelection()
                for each in bones:
                    item = self.tree.findItems(each, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
                    if item is not None:
                        item = item[0]
                        item.setSelected(True)
                self.addItemsToWeightXferList(entryData[0], entryData[1])

                self.tree.clearSelection()
                item = self.tree.findItems(xferBone, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
                if item is not None:
                    item = item[0]
                    item.setSelected(True)
                    self.addXferBoneToList(entryData[1], False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addWeightingTransferEntry(self, layout):
        """
        Adds a Groupbox with two QListWidgets, where the left shows bones to remove, and the right shows the next
        viable parent bone to transfer the weighting to. Both lists can then be edited as well.

        This is what that would like like:

            .. image:: /images/xferEntry.png

        :param layout: The QVboxLayout to add the QGroupbox to.

        :return: returns both QListWidgets (in memory)

        .. seealso:: ART_ExportMeshes.addItemsToWeightXferList(), ART_ExportMeshes.removeBonesFromList()

        """

        groupbox = QtWidgets.QGroupBox()
        layout.insertWidget(0, groupbox)
        groupbox.setMaximumSize(QtCore.QSize(370, 150))
        groupbox.setMaximumSize(QtCore.QSize(370, 150))
        groupbox.setCheckable(True)
        groupbox.setFlat(True)
        groupbox.setObjectName("mid")

        # load style sheet file
        style = interfaceUtils.get_style_sheet("artv2_style")
        groupbox.setStyleSheet(style)

        mainLayout = QtWidgets.QHBoxLayout(groupbox)

        groupbox.toggled.connect(partial(self.collapseBox, groupbox))

        removeBonesList = QtWidgets.QListWidget()
        mainLayout.addWidget(removeBonesList)
        removeBonesList.setMinimumSize(QtCore.QSize(135, 122))
        removeBonesList.setMaximumSize(QtCore.QSize(135, 122))
        removeBonesList.setProperty("list", "remove")
        removeBonesList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        removeBonesList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        removeBonesList.customContextMenuRequested.connect(partial(self.lodContextMenu, removeBonesList, groupbox))

        buttonLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(buttonLayout)

        addButton = QtWidgets.QPushButton(" + ")
        buttonLayout.addWidget(addButton)
        addButton.setObjectName("settings")
        addButton.setMinimumHeight(30)

        buttonLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        remButton = QtWidgets.QPushButton(" - ")
        buttonLayout.addWidget(remButton)
        remButton.setObjectName("settings")
        remButton.setMinimumHeight(30)

        xferBoneList = QtWidgets.QListWidget()
        mainLayout.addWidget(xferBoneList)
        xferBoneList.setMinimumSize(QtCore.QSize(135, 122))
        xferBoneList.setMaximumSize(QtCore.QSize(135, 122))
        xferBoneList.setProperty("list", "xfer")

        setButton = QtWidgets.QPushButton("<-")
        mainLayout.addWidget(setButton)
        setButton.setMinimumHeight(120)
        setButton.setObjectName("settings")
        setButton.clicked.connect(partial(self.addXferBoneToList, xferBoneList, False))

        addButton.clicked.connect(partial(self.addItemsToWeightXferList, removeBonesList, xferBoneList))
        remButton.clicked.connect(partial(self.removeBonesFromList, removeBonesList))

        return [removeBonesList, xferBoneList]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def collapseBox(self, groupBox, *args):
        """
        Collapses the given groupBox down to 16 pixel high, or restores its original height, given the state.

        :param groupBox: Which groupBox to operate on and manipulate the height.
        :param args: What the state is of the groupBox checkBox.

        """

        if args[0]:
            groupBox.setMaximumSize(QtCore.QSize(370, 140))
            groupBox.setMinimumSize(QtCore.QSize(370, 140))
        else:
            groupBox.setMaximumSize(QtCore.QSize(370, 16))
            groupBox.setMinimumSize(QtCore.QSize(370, 16))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addMeshLOD(self):
        """
        Finds the current number of LOD tabs, constructs a label for the new tab, iterating the count by 1,
        and calls on createLODpage, passing in that label.

        .. seealso:: ART_ExportMeshes.createLODpage()

        """

        # get current count of tabs
        numTabs = self.emPageTabs.count()
        label = "LOD_" + str(numTabs)

        self.createLODpage(label, True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addMeshToList_UI(self, parent, label, listWidget):
        """
        Creates a UI that lists all meshes for selection to assign meshes to a given LOD.

            .. image:: /images/addMeshesUI.png

        :param parent: The UI instance to parent this interface to
        :param label: The LOD text label for this interface's window title.
        :param listWidget: The listWidget on the main LOD page that will list the selected meshes

            .. image:: /images/meshList.png

        .. seealso:: ART_ExportMeshes.populateRenderMeshes(), ART_ExportMeshes.addMeshesToLodList()

        """

        # create the main window
        mainWin = QtWidgets.QMainWindow(parent)
        mainWin.setStyleSheet(self.style)

        # create the main widget
        mainWidget = QtWidgets.QFrame()
        mainWidget.setObjectName("mid")
        mainWin.setCentralWidget(mainWidget)
        mainWin.setMinimumSize(300, 525)
        mainWin.setMaximumSize(300, 525)

        # set qt object name
        mainWin.setObjectName("ART_AddMeshesToLODlistWin")
        mainWin.setWindowTitle(label)

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # create the mainLayout for the rig creator UI
        layout = QtWidgets.QVBoxLayout(mainWidget)
        mainLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(mainLayout)

        # treeWidget
        meshTree = QtWidgets.QTreeWidget()
        meshTree.setObjectName("light")
        mainLayout.addWidget(meshTree)
        meshTree.headerItem().setText(0, "")
        meshTree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        meshTree.setMinimumSize(QtCore.QSize(260, 470))
        meshTree.setMaximumSize(QtCore.QSize(260, 470))

        meshTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        meshTree.headerItem().setText(0, "Geometry")
        meshTree.setColumnWidth(0, 260)
        meshTree.setIndentation(10)

        chooseBtn = QtWidgets.QPushButton("Save and Close")
        chooseBtn.setObjectName("settings")
        chooseBtn.setMinimumHeight(30)
        layout.addWidget(chooseBtn)
        chooseBtn.clicked.connect(partial(self.addMeshesToLodList, listWidget, meshTree, mainWin, label))

        # populate tree
        self.populateRenderMeshes(meshTree)

        # if items in listWidget, select those items in the tree
        for i in range(listWidget.count()):
            item = listWidget.item(i).text()
            matches = meshTree.findItems(item, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
            for match in matches:
                match.setSelected(True)

        # show the window
        mainWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addMeshesToLodList(self, listWidget, meshTree, mainWin, label):
        """
        Finds the selected items in addMeshToList_UI's treeWidget, and adds them back to the main LOD page's
        listWidget for meshes associated with that LOD.

        :param listWidget: The list widget to add selected items in the treeWidget to.
        :param meshTree: The treeWidget from addMeshToList_UI(), whose selection will be queried.
        :param mainWin: The window instance from addMeshToList_UI()
        :param label: The name of the LOD tab

        .. seealso:: ART_ExportMeshes.saveMeshList()

        """

        # add to list widget
        selected = meshTree.selectedItems()
        listWidget.clear()
        for each in selected:
            icon = QtGui.QIcon(utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/mesh.png")))
            listWidgetItem = QtWidgets.QListWidgetItem(icon, each.text(0))
            listWidget.addItem(listWidgetItem)

        # hook up connections
        self.saveMeshList(listWidget, label)

        # close window
        mainWin.close()
        mainWin.deleteLater()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveLodPose(self, lod):
        """
        Queries the joints in the skeleton and get the attribute values to store for the given lod.

        :param lod: the text label of the LOD to operate on.

        .. todo:: Suggested feature request was to have this operate on the rig controls and not just joints. That
                  would mean storing both controls and joints. The desire behind this was to do all LOD posing in the
                  rig file, rather than the temp file that gets created for exporting.

        """

        # get all joints
        modules = utils.returnRigModules()

        # go through each one, and find the created bones for that modules
        createdJoints = []
        for module in modules:
            if module != "ART_Root_Module":
                joints = cmds.getAttr(module + ".Created_Bones")
                splitJoints = joints.split("::")

                for bone in splitJoints:
                    if bone != "":
                        createdJoints.append(bone)

        dataDict = {}
        for each in createdJoints:
            translateData = cmds.getAttr(each + ".translate")[0]
            translate = []
            for d in translateData:
                translate.append(float('{:.3f}'.format(d)))

            rotateData = cmds.getAttr(each + ".rotate")[0]
            rotate = []
            for r in rotateData:
                rotate.append(float('{:.3f}'.format(r)))

            scaleData = cmds.getAttr(each + ".scale")[0]
            scale = []
            for s in scaleData:
                scale.append(float('{:.3f}'.format(s)))

            dataDict[str(each)] = [translate, rotate, scale]

        self.lodPoseDict[lod] = dataDict

        for inst in self.mainUI.moduleInstances:
            try:
                # set the model pose again (un-altered)
                inst.setupForRigPose()
                inst.setReferencePose("modelPose")
                inst.cleanUpRigPose()
            except Exception, e:
                print e

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def viewLodPose(self, lod, button):
        """
        Gather LOD pose attribute data for the given LOD and set those values on the joints.

        :param lod: The text label for the LOD to operate on.
        :param button: the "View LOD Pose" button instance

        .. todo:: Suggested feature request was to have this operate on the rig controls and not just joints. That
                  would mean getting data for both controls and joints. The desire behind this was to do all LOD posing
                  in the rig file, rather than the temp file that gets created for exporting.

        """

        if button.isChecked():
            try:
                for key in self.lodPoseDict[lod]:
                    data = self.lodPoseDict[lod].get(key)
                    if cmds.objExists(key):
                        for each in data:
                            # translate, rotate, scale
                            if each == data[0]:
                                cmds.setAttr(key + ".translateX", each[0])
                                cmds.setAttr(key + ".translateY", each[1])
                                cmds.setAttr(key + ".translateZ", each[2])

                            if each == data[1]:
                                cmds.setAttr(key + ".rotateX", each[0])
                                cmds.setAttr(key + ".rotateY", each[1])
                                cmds.setAttr(key + ".rotateZ", each[2])

                            if each == data[2]:
                                cmds.setAttr(key + ".scaleX", each[0])
                                cmds.setAttr(key + ".scaleY", each[1])
                                cmds.setAttr(key + ".scaleZ", each[2])

            except:
                try:
                    characterNode = utils.returnCharacterModule()
                    if cmds.objExists(characterNode + "." + lod + "_Pose"):
                        dict = json.loads(cmds.getAttr(characterNode + "." + lod + "_Pose"))
                        for key in dict:
                            data = dict.get(key)
                            for each in data:
                                # translate, rotate, scale
                                if each == data[0]:
                                    cmds.setAttr(key + ".translateX", each[0])
                                    cmds.setAttr(key + ".translateY", each[1])
                                    cmds.setAttr(key + ".translateZ", each[2])

                                if each == data[1]:
                                    cmds.setAttr(key + ".rotateX", each[0])
                                    cmds.setAttr(key + ".rotateY", each[1])
                                    cmds.setAttr(key + ".rotateZ", each[2])

                                if each == data[2]:
                                    cmds.setAttr(key + ".scaleX", each[0])
                                    cmds.setAttr(key + ".scaleY", each[1])
                                    cmds.setAttr(key + ".scaleZ", each[2])
                except Exception, e:
                    print e

        else:

            for inst in self.mainUI.moduleInstances:
                try:
                    # call on the module's bakeOffsets method
                    inst.setupForRigPose()
                    inst.setReferencePose("modelPose")
                    inst.cleanUpRigPose()
                except Exception, e:
                    print e

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetLodPose(self, lod):
        """
        Resets the LOD pose for the given LOD to the model pose.

        :param lod: the LOD text label to operate on.

        """

        for inst in self.mainUI.moduleInstances:
            try:
                # call on the module's bakeOffsets method
                inst.setupForRigPose()
                inst.setReferencePose("modelPose")
                inst.cleanUpRigPose()
            except Exception, e:
                print e

        self.saveLodPose(lod)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def lodContextMenu(self, widget, groupBox, point):
        """
        Creates a right-click context menu for the weighting transfer entry widget:

            .. image:: /images/xferEntry.png

        :param widget: The parent widget the context menu will spawn from.
        :param groupBox: The parent groupBox for the weighting transfer entry.
        :param point: Where on the parent widget to spawn the context menu.

        """

        style = """
        QMenu {
                background-color: rgb(60,60,60);
                border: 1px solid black;
            }

        QMenu::item {
            background-color: transparent;
            }

        QMenu::item:selected {
                background-color: rgb(255,174,0);
                color: black;
            }
            """

        menu = QtWidgets.QMenu(widget)
        menu.setStyleSheet(style)
        menu.addAction("Clear Selection", widget.clearSelection)
        menu.addAction("Select All", widget.selectAll)
        menu.addAction("Remove This Entry", partial(self.removeTransferEntry, groupBox))

        menu.exec_(widget.mapToGlobal(point))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeTransferEntry(self, groupBox):
        """
        Removes the given groupBox, deleting a weighting transfer entry.

        :param groupBox: Which groupBox to remove.

        """

        groupBox.close()
        groupBox.deleteLater()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeLodTab(self):
        """
        Removes the current tab index from the tabWidget. Also removes and LOD attributes associated with this LOD
        from the character node.

        """

        currentTab = self.emPageTabs.currentIndex()
        tabText = self.emPageTabs.tabText(currentTab)

        if currentTab != 0:
            self.emPageTabs.removeTab(currentTab)

            # remove LOD attrs
            characterNode = utils.returnCharacterModule()
            attrs = cmds.listAttr(characterNode, ud=True, string=tabText + "*")
            if attrs is not None:
                for attr in attrs:
                    cmds.deleteAttr(characterNode, at=attr)

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Cannot remove LOD 0")
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.exec_()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def browseToFBX(self, lineEdit):
        """
        Calls on a fileDialog for the user to browse to an FBX file for saving. Either one that exists, or creating
        a new one.

        :param lineEdit: The QLineEdit whose text to set with the path to the FBX file.

        """

        fileName = cmds.fileDialog2(fm=0, dir=self.projectPath, ff="*.fbx")
        fileName = utils.returnFriendlyPath(fileName[0])
        lineEdit.setText(fileName)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addItemsToWeightXferList(self, widget, boneWidget):
        """
        Takes the items selected in the skeleton tree (pictured below) and auto-selects and children under the
        selected items, as removing the parent will also remove the children of those parents, and then adds all of
        those items to the given widget.

            .. image:: /images/boneTree.png

        :param widget: The QListWidget in the weighting transfer entry widget showing bones to remove.
        :param boneWidget: The QListWidget in the weighting transfer entry widget showing bone who will receive
                           weights from removed bones.

                            .. image:: /images/xferEntry.png

        .. seealso:: ART_ExportMeshes.addXferBoneToList()

        """

        # get selected items in self.tree
        selected = self.tree.selectedItems()

        fullList = []
        itemList = []
        for each in selected:
            self.findTreeChildren(fullList, itemList, each)

        for item in itemList:
            item.setSelected(True)

        for each in fullList:
            widget.addItem(each)

        self.addXferBoneToList(boneWidget)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findTreeChildren(self, fullList, itemList, item):
        """
        Finds any child items from selected items in the Skeleton Tree and appends them to the input lists.

        :param fullList: The full list of all items, including the original selected parent items and any child items
        :param itemList: The instances in memory of the selected items in the Skeleton Tree.
        :param item: The parent item in the Skeleton Tree to check for children

        .. seealso:: ART_ExportMeshes.addItemsToWeightXferList()

        """

        fullList.append(item.text(0))
        itemList.append(item)
        for i in range(item.childCount()):
            self.findTreeChildren(fullList, itemList, item.child(i))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addXferBoneToList(self, widget, autoFind=True):
        """
        Finds the selected items in the Skeleton Tree (for removal) and locates the next viable parent to transfer
        weighting to, then adds that bone to the passed in QListWidget.

        :param widget: The QListWidget to add the bone that will receive weights from removed bones.
        :param autoFind: Whether or not to auto-locate the next viable parent or use the currently selected item.

        """

        if autoFind:
            # find selected items, find the first item parent that is not selected
            selected = self.tree.selectedItems()

            viableParent = None
            for each in selected:
                if each.parent().isSelected() is False:
                    viableParent = each.parent().text(0)
            widget.clear()
            widget.addItem(viableParent)

        else:

            selected = self.tree.selectedItems()
            if len(selected) > 1:

                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Only 1 bone can be selected to transfer weighting to.")
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                msgBox.exec_()

            else:
                widget.clear()
                widget.addItem(selected[0].text(0))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeBonesFromList(self, widget):
        """
        Takes the selected items from the left QListWidget in a weighting transfer widget and attempts to remove
        them from the list.

        :param widget: The QListWidget to check for selected items in.

        """

        selected = widget.selectedItems()

        # find the text of each selected item and list items in the main skeleton tree that match that text
        for each in selected:
            text = each.text()
            match = self.tree.findItems(text, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)

            # check to make sure (if there was a match) that the parent of that item is not also being removed.
            if len(match) > 0:
                parent = match[0].parent()

                parentMatch = widget.findItems(parent.text(0), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
                if len(parentMatch) == 0:

                    row = widget.row(each)
                    widget.takeItem(row)

                else:
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setText(
                        "Parent of the joint is also being removed. Cannot complete request unless parent joint "
                        "is not removed.")
                    msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                    msgBox.exec_()

            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Was not able to find a matching entry in the skeleton tree.")
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                msgBox.exec_()

                return

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addBoneToListUI_addChildren(self, name, parent):
        """
        Populates the Skeleton Tree (self.tree) by recursively looking for relatives of the given name and making more
        QTreeWidgetItems using the passed in name, and parenting under the passed in parent.

        :param name: The bone name, which will be used to look for children, and also as the text for the treeWidgetItem
        :param parent: The parent treeWidgetItem that the created item will be a child of.

        """

        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, name)
        item.setBackground(0, QtCore.Qt.NoBrush)

        children = cmds.listRelatives(name, children=True, type="joint")
        if children:
            for child in children:
                self.addBoneToListUI_addChildren(child, item)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addBoneToList_Accept(self, tree, listWidget, lod, layout, viewBtn):
        """
        Called from the "Save and Close" button of the addBoneToList_UI, clears all items in the main listWidget,
        then populates that listWidget with the new bones to remove. Adds all LOD pose info to the character node as
        well as weighting transfer info for that lod.

        :param listWidget: The listWidget on the main LOD page on the bottom right that lists bones to remove.
        :param lod: The LOD text (LOD_#) to operate on.
        :param layout: The QVboxLayout to query for weighting transfer entries.
        :param viewBtn: The "View LOD Pose" button instance

        """

        # find items already in listWidget
        listWidget.clear()

        # get the character node
        characterNode = utils.returnCharacterModule()

        # add info to characterNode
        if not cmds.objExists(characterNode + "." + lod + "_Pose"):
            cmds.addAttr(characterNode, ln=lod + "_Pose", dt="string")

        if not cmds.objExists(characterNode + "." + lod + "_Bones"):
            cmds.addAttr(characterNode, ln=lod + "_Bones", dt="string")

        # gather weight transfer info and pose info
        lodXferList = []

        for i in range(layout.count()):
            if type(layout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                children = layout.itemAt(i).widget().children()
                data = []
                removeBones = []
                for each in children:
                    if type(each) == QtWidgets.QListWidget:

                        # [[list of bones], xferbone]
                        if each.property("list") == "remove":

                            for x in range(each.count()):
                                item = each.item(x)
                                if item.text() not in removeBones:
                                    removeBones.append(item.text())

                        elif each.property("list") == "xfer":
                            for y in range(each.count()):
                                item = each.item(y)
                                data.append(item.text())
                                data.append(removeBones)
                lodXferList.append(data)

        for item in lodXferList:
            bones = item[1]

            for bone in bones:
                icon = QtGui.QIcon(utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/boneDisplay.png")))
                listWidgetItem = QtWidgets.QListWidgetItem(icon, str(bone))
                listWidget.addItem(listWidgetItem)

        string = json.dumps(lodXferList)
        cmds.setAttr(characterNode + "." + lod + "_Bones", string, type="string")

        # Pose Info
        try:
            poseString = json.dumps(self.lodPoseDict[lod])
            cmds.setAttr(characterNode + "." + lod + "_Pose", poseString, type="string")
        except:
            print "no LOD pose given. Using model pose."

        # set viewPoseBtn to unchecked
        viewBtn.setChecked(False)
        self.viewLodPose(lod, viewBtn)

        # remove UI
        if cmds.window("ART_AddBoneToLODlistWin", exists=True):
            cmds.deleteUI("ART_AddBoneToLODlistWin", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateRenderMeshes(self, tree):
        """
        Finds all skinned meshes in the scene and adds them as items to the given TreeWidget.

        .. image:: /images/addMeshesUI.png

        :param tree: The QTreeWidget to add found meshes to

        """

        # find all skinned meshes in scene
        skinClusters = cmds.ls(type='skinCluster')
        renderMeshes = []

        for cluster in skinClusters:
            geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
            geoTransform = cmds.listRelatives(geometry, parent=True)[0]
            renderMeshes.append(geoTransform)

        geoParents = []
        worldGeo = []
        meshDict = {}

        for geo in renderMeshes:
            parent = cmds.listRelatives(geo, parent=True)
            if parent is not None:
                parent = parent[0]

                if parent not in geoParents:
                    geoParents.append(parent)

            else:
                worldGeo.append(geo)

        for each in geoParents:
            children = cmds.listRelatives(each)
            meshDict[each] = children

        for key in meshDict.keys():
            item = QtWidgets.QTreeWidgetItem(tree)
            item.setText(0, key)
            item.setBackground(0, QtCore.Qt.NoBrush)

            children = meshDict.get(key)
            for child in children:
                icon = QtGui.QIcon(utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/mesh.png")))
                childItem = QtWidgets.QTreeWidgetItem(item)
                childItem.setText(0, child)
                childItem.setBackground(0, QtCore.Qt.NoBrush)
                childItem.setIcon(0, icon)

        for geo in worldGeo:
            icon = QtGui.QIcon(utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/mesh.png")))
            geoItem = QtWidgets.QTreeWidgetItem(tree)
            geoItem.setText(0, geo)
            geoItem.setBackground(0, QtCore.Qt.NoBrush)
            geoItem.setIcon(0, icon)

        tree.expandAll()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateUI(self):
        """
        Checks to see if LOD attributes exist on the character node, and if so, builds and populates the UI based on
        those settings.

        """

        # get the character node
        characterNode = utils.returnCharacterModule()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # populate ui automatically if the settings exist
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        attrs = cmds.listAttr(characterNode, ud=True, string="LOD_*_FilePath")

        lodAttrs = []
        createdTabs = []
        if attrs is not None:
            for attr in attrs:
                lodAttrs.append(attr.partition("_FilePath")[0])

        if lodAttrs is not None:
            # get json data from attribute
            lodData = ["_Pose", "_Bones", "_Meshes", "_FilePath"]
            meshValue = None
            boneValue = None
            pathValue = None

            for attr in lodAttrs:
                for entry in lodData:
                    if cmds.objExists(characterNode + "." + attr + entry):
                        if entry == "_Bones":
                            boneValue = json.loads(cmds.getAttr(characterNode + "." + attr + entry))
                        if entry == "_Meshes":
                            meshValue = cmds.listConnections(characterNode + "." + attr + entry)
                        if entry == "_FilePath":
                            pathValue = json.loads(cmds.getAttr(characterNode + "." + attr + entry))

                # compare number of LOD attrs to number of current tabs. If needed, add more tabs for the lods
                numTabs = self.emPageTabs.count()

                if numTabs < len(lodAttrs):
                    for i in range(numTabs):
                        tab = self.emPageTabs.widget(i)
                        tabText = self.emPageTabs.tabText(i)

                        if attr != tabText:
                            if attr not in createdTabs:
                                self.createLODpage(attr, True)
                                createdTabs.append(attr)

                # find the associated tab and set the data
                for i in range(self.emPageTabs.count()):
                    tab = self.emPageTabs.widget(i)
                    tabText = self.emPageTabs.tabText(i)

                    if tabText == attr:
                        # tab children
                        lists = lineEdits = tab.findChildren(QtWidgets.QListWidget)
                        lineEdits = tab.findChildren(QtWidgets.QLineEdit)

                        # set meshes and bones for this tab
                        for list in lists:
                            property = list.property("listType")

                            if property == "mesh":
                                if meshValue is not None:
                                    for mesh in meshValue:
                                        icon = QtGui.QIcon(
                                            utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/mesh.png")))
                                        listWidgetItem = QtWidgets.QListWidgetItem(icon, mesh)
                                        list.addItem(listWidgetItem)

                            if property == "bone":
                                if boneValue is not None:
                                    for item in boneValue:
                                        bones = item[1]
                                        for bone in bones:
                                            icon = QtGui.QIcon(utils.returnFriendlyPath(
                                                os.path.join(self.iconsPath, "System/boneDisplay.png")))
                                            listWidgetItem = QtWidgets.QListWidgetItem(icon, bone)
                                            list.addItem(listWidgetItem)

                        # set file path
                        if os.path.exists(os.path.dirname(pathValue)):
                            lineEdits[0].setText(pathValue)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveFilePath(self, lineEdit, tabText, *args):
        """
        Gathers the FBX output path for the LOD and stores that information to the character node.

        :param lineEdit: The QLineEdit which stores the output path text.
        :param tabText: The LOD text to operate on (LOD_#)

        """

        characterNode = utils.returnCharacterModule()

        # get file path
        path = lineEdit.text()
        dataString = json.dumps(path)

        if not cmds.objExists(characterNode + "." + tabText + "_FilePath"):
            cmds.addAttr(characterNode, ln=tabText + "_FilePath", dt="string")

        cmds.setAttr(characterNode + "." + tabText + "_FilePath", dataString, type="string")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveMeshList(self, listWidget, tabText):
        """
        Gathers the associated meshes for an LOD and stores that information to the character node.

        :param listWidget: The QListWidget of the LOD tab to search for associated meshes.
        :param tabText: The LOD text to operate on (LOD_#)

        """

        characterNode = utils.returnCharacterModule()

        if not cmds.objExists(characterNode + "." + tabText + "_Meshes"):
            cmds.addAttr(characterNode, ln=tabText + "_Meshes", at="message")
        if not cmds.objExists(characterNode + "." + tabText + "_FilePath"):
            cmds.addAttr(characterNode, ln=tabText + "_FilePath", dt="string")

        i = tabText.partition("_")[2]

        # first remove all connections
        connections = cmds.listConnections(characterNode + "." + tabText + "_Meshes")
        if connections is not None:
            for conn in connections:
                cmds.disconnectAttr(characterNode + "." + tabText + "_Meshes", conn + ".lodGroup" + str(i))

        # Add attrs to meshes to connect up to the characterNode LOD meshes attr
        meshList = []
        for x in range(listWidget.count()):
            meshList.append(listWidget.item(x).text())

        for mesh in meshList:
            if not cmds.objExists(mesh + ".lodGroup" + str(i)):
                cmds.addAttr(mesh, sn="lodGroup" + str(i), at="message")

            cmds.connectAttr(characterNode + "." + tabText + "_Meshes", mesh + ".lodGroup" + str(i))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def export(self):
        """
        Gathers all export data by calling on utils.findExportMeshData, parses the information, and for each LOD in
        the list, calls on utils.ExportMesh(), passing in the appropriate data.

        .. seealso:: utils.ExportMesh(), utils.findExportMeshData()

        """

        exportData = utils.findExportMeshData()
        for each in exportData:
            if not os.path.exists(os.path.dirname(each[0])):
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("There are LODs with no valid file path to export to. Aborting.")
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                msgBox.exec_()
                return
            if each[1] is None:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("There are LODs that have no meshes associated with them. Aborting.")
                msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                msgBox.exec_()
                return

        # save the file
        saveFile = cmds.file(q=True, sceneName=True)
        try:
            cmds.file(save=True)
        except Exception, e:
            cmds.error("Could not save file. Error: " + str(e))
            return

        # export
        fileData = []
        for each in exportData:
            meshValue = each[1]
            pathValue = each[0]
            boneValue = each[2]
            poseData = each[3]

            utils.exportMesh(self.mainUI, meshValue, pathValue, boneValue, poseData)
            fileData.append(pathValue)

            # open the file
            cmds.file(saveFile, open=True, force=True)

        # report and close
        self.close()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Export Complete!")

        string = ""
        for each in fileData:
            string += each + "\n"
        msgBox.setDetailedText(string)
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.exec_()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    ART_ExportMeshes(self, parent=interfaceUtils.getMainWindow())