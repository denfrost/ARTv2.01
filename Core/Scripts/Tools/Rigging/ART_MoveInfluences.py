from ThirdParty.Qt import QtGui, QtCore, QtWidgets
from functools import partial
import maya.cmds as cmds
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
import os


class ART_MoveInfluences():
    def __init__(self, mainUI):

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI
        self.skinCluster = None

        # build the UI
        self.buildMoveInfsUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildMoveInfsUI(self):

        if cmds.window("ART_MoveInfluencesWin", exists=True):
            cmds.deleteUI("ART_MoveInfluencesWin", wnd=True)

        # launch a UI to get the name information
        self.moveInfsWin = QtWidgets.QMainWindow(self.mainUI)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.moveInfsWin.setWindowIcon(window_icon)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.moveInfsWin.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.moveInfsWin_mainWidget = QtWidgets.QWidget()
        self.moveInfsWin.setCentralWidget(self.moveInfsWin_mainWidget)

        # set qt object name
        self.moveInfsWin.setObjectName("ART_MoveInfluencesWin")
        self.moveInfsWin.setWindowTitle("Move Influences")

        # create the mainLayout for the rig creator UI
        self.moveInfsWin_mainLayout = QtWidgets.QVBoxLayout(self.moveInfsWin_mainWidget)
        self.moveInfsWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.moveInfsWin.resize(300, 100)
        self.moveInfsWin.setSizePolicy(mainSizePolicy)
        self.moveInfsWin.setMinimumSize(QtCore.QSize(300, 100))
        self.moveInfsWin.setMaximumSize(QtCore.QSize(300, 100))

        # create the background image
        self.moveInfsWin_frame = QtWidgets.QFrame()
        self.moveInfsWin_mainLayout.addWidget(self.moveInfsWin_frame)

        # layout for the widgets
        self.moveInfsWin_widgetLayout = QtWidgets.QVBoxLayout(self.moveInfsWin_frame)

        # layout for the combo boxes
        self.moveInfsWin_comboBoxLayout = QtWidgets.QHBoxLayout()
        self.moveInfsWin_widgetLayout.addLayout(self.moveInfsWin_comboBoxLayout)

        # combo boxes
        self.moveFromComboBox = QtWidgets.QComboBox()
        self.moveInfsWin_comboBoxLayout.addWidget(self.moveFromComboBox)

        label = QtWidgets.QLabel("  -------->  ")
        label.setMaximumWidth(40)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.moveInfsWin_comboBoxLayout.addWidget(label)

        self.moveToComboBox = QtWidgets.QComboBox()
        self.moveInfsWin_comboBoxLayout.addWidget(self.moveToComboBox)

        # process button
        self.moveInfsGoBtn = QtWidgets.QPushButton("Move Influences")
        self.moveInfsGoBtn.setObjectName("settings")
        self.moveInfsWin_widgetLayout.addWidget(self.moveInfsGoBtn)
        self.moveInfsGoBtn.setMinimumHeight(40)
        self.moveInfsGoBtn.clicked.connect(partial(self.moveInfluences))

        # populate the lists
        status = self.findInfluencesOnSelection()
        if not status:
            return

        # show the window
        self.moveInfsWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findInfluencesOnSelection(self):

        # find the selected mesh
        selection = cmds.ls(sl=True)

        influences = []

        # check if valid selection
        if len(selection) >= 1:
            if selection[0].find(".vtx") != -1:
                mesh = selection[0].partition(".vtx")[0]

                if cmds.nodeType(mesh) == "transform":

                    # check for skinCluster
                    skinClusters = cmds.ls(type='skinCluster')

                    # go through each found skin cluster, and if we find a skin cluster whose geometry matches our
                    # selection, get influences
                    for cluster in skinClusters:
                        geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
                        geoTransform = cmds.listRelatives(geometry, parent=True)[0]
                        if geoTransform == mesh:
                            self.skinCluster = cluster
                            influences = cmds.skinCluster(cluster, q=True, inf=True)

            else:
                cmds.warning("please select the vertices you want to operate on.")
                return False

        # populate combo boxes
        for inf in influences:
            self.moveFromComboBox.addItem(inf)
            self.moveToComboBox.addItem(inf)

        return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def moveInfluences(self):

        # make sure there is still a valid selection
        selection = cmds.ls(sl=True)
        valid = False
        if len(selection) >= 1:
            if selection[0].find(".vtx") != -1:
                valid = True

        if valid:
            # make sure the combo boxes don't have the same values
            moveFrom = self.moveFromComboBox.currentText()
            moveTo = self.moveToComboBox.currentText()

            if moveFrom == moveTo:
                cmds.warning("Target influence cannot be the same as the source influence.")

            else:
                cmds.skinPercent(self.skinCluster, tmw=[moveFrom, moveTo])
                cmds.deleteUI("ART_MoveInfluencesWin", wnd=True)
                selection = cmds.ls(sl=True, flatten=True)
                cmds.select(clear=True)
                cmds.select(selection)

        if not valid:
            cmds.warning("No vertices selected to operate on.")
