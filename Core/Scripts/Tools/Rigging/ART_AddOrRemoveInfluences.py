"""
Author: Jeremy Ernst
"""

from functools import partial
import os
import maya.cmds as cmds
import maya.mel as mel

import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_AddOrRemoveInfluences():
    """
    This class is used to list influences in or out of the current skinCluster, and then remove or add said
    influences given current selection.

    It is called from this button, found after finalizing your setup:
      .. image:: /images/addRemoveInfsButton.png

    This is what the full interface looks like:
      .. image:: /images/addRemoveInfs.png

    """

    def __init__(self, mainUI):
        """
        Instantiates the class, taking in the instance of the rig creator skin tools interface. Get settings values
        from QSettings. Build the interface.

        :param mainUI: Instance of the skin tools interface.

        """

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        self.buildInterface()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildInterface(self):
        """
        Builds the interface for the tool, finding all joints that compose the asset, comparing them to joints in the
        skinCluster, then separating the initial list into joints in the cluster, and joints not in the cluster.

        """

        if cmds.window("ART_addRemoveInfsWin", exists=True):
            cmds.deleteUI("ART_addRemoveInfsWin", wnd=True)

        # launch a UI to get the name information
        self.addRemoveInfsWin = QtWidgets.QMainWindow(self.mainUI)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.addRemoveInfsWin_mainWidget = QtWidgets.QWidget()
        self.addRemoveInfsWin.setCentralWidget(self.addRemoveInfsWin_mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.addRemoveInfsWin.setWindowIcon(window_icon)

        # set qt object name
        self.addRemoveInfsWin.setObjectName("ART_addRemoveInfsWin")
        self.addRemoveInfsWin.setWindowTitle("Add/Remove Influences")

        # create the mainLayout for the ui
        self.addRemoveInfsWin_mainLayout = QtWidgets.QVBoxLayout(self.addRemoveInfsWin_mainWidget)
        self.addRemoveInfsWin_mainLayout.setContentsMargins(5, 5, 5, 5)

        self.addRemoveInfsWin.resize(300, 450)
        self.addRemoveInfsWin.setSizePolicy(mainSizePolicy)
        self.addRemoveInfsWin.setMinimumSize(QtCore.QSize(300, 450))
        self.addRemoveInfsWin.setMaximumSize(QtCore.QSize(300, 450))

        # create the background image
        self.addRemoveInfsWin_frame = QtWidgets.QFrame()
        self.addRemoveInfsWin_mainLayout.addWidget(self.addRemoveInfsWin_frame)
        self.addRemoveInfsWin_frame.setObjectName("dark")

        # create the main layout for the widgets
        self.addRemoveInfsWin_widgetLayout = QtWidgets.QHBoxLayout(self.addRemoveInfsWin_frame)

        # two layouts needed for the widget layout. left side = vertical layout for filters,
        # search, and list. right layout = vertical layout for buttons
        self.addRemoveInfsWin_leftSideLayout = QtWidgets.QVBoxLayout()
        self.addRemoveInfsWin_widgetLayout.addLayout(self.addRemoveInfsWin_leftSideLayout)

        self.addRemoveInfsWin_rightSideLayout = QtWidgets.QVBoxLayout()
        self.addRemoveInfsWin_widgetLayout.addLayout(self.addRemoveInfsWin_rightSideLayout)

        # left side: filters, search, list
        self.addRemoveInfsWin_filters = QtWidgets.QComboBox()
        self.addRemoveInfsWin_leftSideLayout.addWidget(self.addRemoveInfsWin_filters)
        self.addRemoveInfsWin_filters.addItem("Show Influences In Skin")
        self.addRemoveInfsWin_filters.addItem("Show Influences Not In Skin")
        self.addRemoveInfsWin_filters.currentIndexChanged.connect(partial(self.addOrRemoveInfs_ShowInfsFilter))

        self.addRemoveInfsWin_search = QtWidgets.QLineEdit()
        self.addRemoveInfsWin_leftSideLayout.addWidget(self.addRemoveInfsWin_search)
        self.addRemoveInfsWin_search.setPlaceholderText("Search...")
        self.addRemoveInfsWin_search.setObjectName("light")
        self.addRemoveInfsWin_search.textChanged.connect(partial(self.addOrRemoveInfs_Search))

        self.addRemoveInfsWin_infList = QtWidgets.QListWidget()
        self.addRemoveInfsWin_leftSideLayout.addWidget(self.addRemoveInfsWin_infList)
        self.addRemoveInfsWin_infList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # right side: add button, remove button, prune weights, remove unused button
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)

        self.addRemoveInfsWin_refreshSelBtn = QtWidgets.QPushButton("Refresh")
        self.addRemoveInfsWin_rightSideLayout.addWidget(self.addRemoveInfsWin_refreshSelBtn)
        self.addRemoveInfsWin_refreshSelBtn.setMinimumSize(110, 35)
        self.addRemoveInfsWin_refreshSelBtn.setMaximumSize(110, 35)
        self.addRemoveInfsWin_refreshSelBtn.setFont(font)
        self.addRemoveInfsWin_refreshSelBtn.clicked.connect(partial(self.addOrRemoveInfs_RefreshSelection))
        self.addRemoveInfsWin_refreshSelBtn.setObjectName("settings")
        self.addRemoveInfsWin_rightSideLayout.addSpacerItem(
            QtWidgets.QSpacerItem(100, 300, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        self.addRemoveInfsWin_addInfBtn = QtWidgets.QPushButton("Add")
        self.addRemoveInfsWin_rightSideLayout.addWidget(self.addRemoveInfsWin_addInfBtn)
        self.addRemoveInfsWin_addInfBtn.setMinimumSize(110, 35)
        self.addRemoveInfsWin_addInfBtn.setMaximumSize(110, 35)
        self.addRemoveInfsWin_addInfBtn.setFont(font)
        self.addRemoveInfsWin_addInfBtn.clicked.connect(partial(self.addOrRemoveInfs_addInf, True, False))
        self.addRemoveInfsWin_addInfBtn.setObjectName("settings")

        self.addRemoveInfsWin_removeInfBtn = QtWidgets.QPushButton("Remove")
        self.addRemoveInfsWin_rightSideLayout.addWidget(self.addRemoveInfsWin_removeInfBtn)
        self.addRemoveInfsWin_removeInfBtn.setMinimumSize(110, 35)
        self.addRemoveInfsWin_removeInfBtn.setMaximumSize(110, 35)
        self.addRemoveInfsWin_removeInfBtn.setFont(font)
        self.addRemoveInfsWin_removeInfBtn.clicked.connect(partial(self.addOrRemoveInfs_addInf, False, False))
        self.addRemoveInfsWin_removeInfBtn.setObjectName("settings")

        self.addRemoveInfsWin_removeUnusedInfBtn = QtWidgets.QPushButton("Remove Unused")
        self.addRemoveInfsWin_rightSideLayout.addWidget(self.addRemoveInfsWin_removeUnusedInfBtn)
        self.addRemoveInfsWin_removeUnusedInfBtn.setMinimumSize(110, 35)
        self.addRemoveInfsWin_removeUnusedInfBtn.setMaximumSize(110, 35)
        self.addRemoveInfsWin_removeUnusedInfBtn.setFont(font)
        self.addRemoveInfsWin_removeUnusedInfBtn.clicked.connect(partial(self.addOrRemoveInfs_addInf, False, True))
        self.addRemoveInfsWin_removeUnusedInfBtn.setObjectName("settings")

        self.addRemoveInfsWin_pruneBtn = QtWidgets.QPushButton("Prune Weights")
        self.addRemoveInfsWin_rightSideLayout.addWidget(self.addRemoveInfsWin_pruneBtn)
        self.addRemoveInfsWin_pruneBtn.setMinimumSize(110, 35)
        self.addRemoveInfsWin_pruneBtn.setMaximumSize(110, 35)
        self.addRemoveInfsWin_pruneBtn.setFont(font)
        self.addRemoveInfsWin_pruneBtn.clicked.connect(partial(self.addOrRemoveInfs_prune))
        self.addRemoveInfsWin_pruneBtn.setObjectName("settings")

        # populate infList
        self.addOrRemoveInfs_RefreshSelection()

        # show window
        self.addRemoveInfsWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addOrRemoveInfs_RefreshSelection(self):
        """
        Regenerate the lists comparing all joints of the rig to joints in the skin cluster and joints not in the
        skinCluster. Clear the listWidgets and refresh with new data.

        """

        self.addRemoveInfsWin_infList.clear()

        # get selection, find skin cluster, find influences in skinCluster, and populate listWidget
        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            skinCluster = riggingUtils.findRelatedSkinCluster(selection[0])

            if skinCluster is not None:
                skinInfs = cmds.skinCluster(skinCluster, q=True, inf=True)

                for inf in skinInfs:
                    self.addRemoveInfsWin_infList.addItem(inf)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addOrRemoveInfs_ShowInfsFilter(self, *args):
        """
        Change what is displayed in the QListWidget based on the QComboBox setting of which joints to show: those in
        the skinCluster, or those not in the skinCluster.

        """

        self.addRemoveInfsWin_infList.clear()
        currentIndex = self.addRemoveInfsWin_filters.currentIndex()

        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            skinCluster = riggingUtils.findRelatedSkinCluster(selection[0])

            if skinCluster is not None:
                skinInfs = cmds.skinCluster(skinCluster, q=True, inf=True)
                # if filter set to show infs in cluster:
                if currentIndex == 0:
                    for each in skinInfs:
                        self.addRemoveInfsWin_infList.addItem(each)

                # if filter set to show non-skinned infs
                if currentIndex == 1:
                    # get full path
                    dagPath = cmds.ls(skinInfs[0], long=True)[0]
                    rootJoint = dagPath.partition("|")[2].partition("|")[0]
                    currentSelection = cmds.ls(sl=True)[0]

                    # get all joints
                    cmds.select(rootJoint, hi=True)
                    skeleton = cmds.ls(sl=True)
                    cmds.select(currentSelection)

                    # compare all joints to infs list
                    for each in skeleton:
                        if each not in skinInfs:
                            self.addRemoveInfsWin_infList.addItem(each)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def addOrRemoveInfs_Search(self):
        """
        Hides all items in the QListWidget, then compares the QLineEdit search text with each item in the QListWidget,
        and if the search text is found in the text of an item, show that QListWidgetItem.

        """

        searchKey = self.addRemoveInfsWin_search.text()

        # get all items in the joint list
        allItems = []
        for i in range(self.addRemoveInfsWin_infList.count()):
            item = self.addRemoveInfsWin_infList.item(i)
            itemName = item.text()
            allItems.append([item, itemName])

        # hide all items in list
        for item in allItems:
            item[0].setHidden(True)
            item[0].setSelected(False)

        # find items in list with search key and show item
        if searchKey.find("*") == 0:
            matchedItems = self.addRemoveInfsWin_infList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchWildcard)
            for item in matchedItems:
                item.setHidden(False)
                item.setSelected(True)

        else:
            matchedItems = self.addRemoveInfsWin_infList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchContains)
            for item in matchedItems:
                item.setHidden(False)
                item.setSelected(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def addOrRemoveInfs_addInf(self, add, removeUnused):
        """
        Either add, or remove, selected influences from the QListWidget to/from the skinCluster. (the main function)

        :param add: Whether or not to add or remove.
        :param removeUnused: If this flag is set, remove any unweighted influences in the skinCluster.

        """

        # get current selection in scene
        currentSelection = cmds.ls(sl=True)

        # get selected items in infList
        selectedItems = self.addRemoveInfsWin_infList.selectedItems()

        # find the skinCluster
        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            skinCluster = riggingUtils.findRelatedSkinCluster(selection[0])

            # removed unused influences
            if removeUnused:
                weightedInfs = cmds.skinCluster(skinCluster, q=True, weightedInfluence=True)
                allInfs = cmds.skinCluster(skinCluster, q=True, inf=True)

                for inf in allInfs:
                    if inf not in weightedInfs:
                        cmds.skinCluster(skinCluster, edit=True, ri=inf)

                cmds.select(currentSelection)
                self.addOrRemoveInfs_RefreshSelection()
                self.addOrRemoveInfs_ShowInfsFilter()
                return

            # add selectedItems to the skinCluster
            for item in selectedItems:
                if add:
                    cmds.skinCluster(skinCluster, edit=True, ai=item.text(), wt=0, lw=True)
                if not add:
                    cmds.skinCluster(skinCluster, edit=True, ri=item.text())

        # refresh list
        cmds.select(currentSelection)
        self.addOrRemoveInfs_RefreshSelection()
        self.addOrRemoveInfs_ShowInfsFilter()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addOrRemoveInfs_prune(self):
        """
        Calls on Maya's built in prune skin weights tool.

        """

        mel.eval("PruneSmallWeightsOptions;")

        # get current selection in scene
        currentSelection = cmds.ls(sl=True)

        # refresh lists
        cmds.select(currentSelection)
        self.addOrRemoveInfs_RefreshSelection()
        self.addOrRemoveInfs_ShowInfsFilter()
