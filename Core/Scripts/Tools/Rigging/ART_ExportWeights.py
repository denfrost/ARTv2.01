"""
Author: Jeremy Ernst

    This class builds the interface for exporting skin weights for each piece of selected geometry.

===============
Class
===============
"""

import os
from functools import partial

import maya.cmds as cmds

import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_ExportSkinWeights():
    def __init__(self, mainUI):
        """
        Instantiate the class, getting the settings from QSettings, then build the interface.

        :param mainUI: instance of the rig creator interface
        """

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        self.buildExportWeightsUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildExportWeightsUI(self):
        """
        Build the interface for exporting the skin weights. An entry is added for each piece of selected geometry.
        The user then has the ability to specify a .weight file name for the associated geometry.
        The user also specifies where they would like the weight files saved to.

        .. image:: /images/exportWeights.png

        """

        if cmds.window("ART_exportSkinWeightsUI", exists=True):
            cmds.deleteUI("ART_exportSkinWeightsUI", wnd=True)

        # launch a UI to get the name information
        self.exportSkinWeights_Win = QtWidgets.QMainWindow(self.mainUI)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")

        # create the main widget
        self.exportSkinWeights_mainWidget = QtWidgets.QWidget()
        self.exportSkinWeights_Win.setCentralWidget(self.exportSkinWeights_mainWidget)

        # set qt object name
        self.exportSkinWeights_Win.setObjectName("ART_exportSkinWeightsUI")
        self.exportSkinWeights_Win.setWindowTitle("Export Skin Weights")

        # create the mainLayout for the ui
        self.exportSkinWeights_mainLayout = QtWidgets.QVBoxLayout(self.exportSkinWeights_mainWidget)
        self.exportSkinWeights_mainLayout.setContentsMargins(5, 5, 5, 5)

        self.exportSkinWeights_Win.resize(450, 600)
        self.exportSkinWeights_Win.setSizePolicy(mainSizePolicy)
        self.exportSkinWeights_Win.setMinimumSize(QtCore.QSize(450, 600))
        self.exportSkinWeights_Win.setMaximumSize(QtCore.QSize(450, 600))

        # create the background image
        self.exportSkinWeights_frame = QtWidgets.QFrame()
        self.exportSkinWeights_mainLayout.addWidget(self.exportSkinWeights_frame)
        self.exportSkinWeights_frame.setObjectName("dark")

        # create widgetLayout
        self.exportSkinWeights_widgetLayout = QtWidgets.QVBoxLayout(self.exportSkinWeights_frame)

        # create the hboxLayout for lineEdit and browser button
        self.exportSkinWeights_browseLayout = QtWidgets.QHBoxLayout()
        self.exportSkinWeights_widgetLayout.addLayout(self.exportSkinWeights_browseLayout)

        # create the line edit for the export path
        self.exportSkinWeights_lineEdit = QtWidgets.QLineEdit(utils.returnFriendlyPath(self.toolsPath))
        self.exportSkinWeights_browseLayout.addWidget(self.exportSkinWeights_lineEdit)

        self.exportSkinWeights_browseBtn = QtWidgets.QPushButton()
        self.exportSkinWeights_browseLayout.addWidget(self.exportSkinWeights_browseBtn)
        self.exportSkinWeights_browseBtn.setMinimumSize(35, 35)
        self.exportSkinWeights_browseBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/fileBrowse.png"))
        self.exportSkinWeights_browseBtn.setIconSize(QtCore.QSize(30, 30))
        self.exportSkinWeights_browseBtn.setIcon(icon)
        self.exportSkinWeights_browseBtn.clicked.connect(partial(self.exportSkinWeights_fileBrowse))

        # scroll area contents
        self.exportSkinWeights_scrollContents = QtWidgets.QFrame()
        self.exportSkinWeights_scrollContents.setObjectName("light")

        # Layout of Container Widget
        self.exportSkinWeights_VLayout = QtWidgets.QVBoxLayout()

        # find selected geometry and populate scroll area
        self.exportSkinWeights_populate()

        # add scrollArea for selected geo, skinFileName, and checkbox for exporting
        self.exportSkinWeights_scrollLayout = QtWidgets.QScrollArea()
        self.exportSkinWeights_widgetLayout.addWidget(self.exportSkinWeights_scrollLayout)
        self.exportSkinWeights_scrollLayout.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.exportSkinWeights_scrollLayout.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.exportSkinWeights_scrollLayout.setWidgetResizable(False)
        self.exportSkinWeights_scrollLayout.setWidget(self.exportSkinWeights_scrollContents)

        # lastly, export button
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)

        self.exportSkinWeights_exportBtnLayout = QtWidgets.QHBoxLayout()
        self.exportSkinWeights_widgetLayout.addLayout(self.exportSkinWeights_exportBtnLayout)

        self.exportSkinWeights_RefreshBtn = QtWidgets.QPushButton("Refresh")
        self.exportSkinWeights_exportBtnLayout.addWidget(self.exportSkinWeights_RefreshBtn)
        self.exportSkinWeights_RefreshBtn.setMinimumSize(QtCore.QSize(70, 50))
        self.exportSkinWeights_RefreshBtn.setMaximumSize(QtCore.QSize(70, 50))
        self.exportSkinWeights_RefreshBtn.setFont(font)
        self.exportSkinWeights_RefreshBtn.clicked.connect(partial(self.buildExportWeightsUI))
        self.exportSkinWeights_RefreshBtn.setObjectName("settings")

        self.exportSkinWeights_ExportBtn = QtWidgets.QPushButton("EXPORT WEIGHTS")
        self.exportSkinWeights_exportBtnLayout.addWidget(self.exportSkinWeights_ExportBtn)
        self.exportSkinWeights_ExportBtn.setMinimumSize(QtCore.QSize(330, 50))
        self.exportSkinWeights_ExportBtn.setMaximumSize(QtCore.QSize(330, 50))
        self.exportSkinWeights_ExportBtn.setFont(font)
        self.exportSkinWeights_ExportBtn.clicked.connect(partial(self.exportSkinWeights_doExport))
        self.exportSkinWeights_ExportBtn.setObjectName("settings")

        # show window
        self.exportSkinWeights_Win.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def exportSkinWeights_populate(self):
        """
        Populate the interface with an entry for each mesh the user has selected.

        This entry includes the mesh name, an QLineEdit to specify a file name for the .weight file, and a checkbox
        as to whether or not the user wants to export weights for that mesh.

        """

        # get current selection
        selection = cmds.ls(sl=True)
        if len(selection) > 0:

            # Create headers
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)

            headerLayout = QtWidgets.QHBoxLayout()
            self.exportSkinWeights_VLayout.addLayout(headerLayout)
            headerExport = QtWidgets.QLabel(" ")
            headerLayout.addWidget(headerExport)
            headerExport.setStyleSheet("background: transparent;")

            headerGeo = QtWidgets.QLabel("Mesh")
            headerGeo.setMinimumSize(QtCore.QSize(180, 20))
            headerGeo.setMaximumSize(QtCore.QSize(180, 20))
            headerLayout.addWidget(headerGeo)
            headerGeo.setFont(font)
            headerGeo.setStyleSheet("background: transparent;")

            headerFileName = QtWidgets.QLabel("FileName")
            headerLayout.addWidget(headerFileName)
            headerFileName.setMinimumSize(QtCore.QSize(180, 20))
            headerFileName.setMaximumSize(QtCore.QSize(180, 20))
            headerFileName.setFont(font)
            headerFileName.setStyleSheet("background: transparent;")

            # loop through selection, checking selection is valid and has skinCluster
            for each in selection:

                # get dagPath of each
                dagPath = cmds.ls(each, long=True)[0]
                skinCluster = riggingUtils.findRelatedSkinCluster(dagPath)

                if skinCluster is not None:
                    # create HBoxLayout
                    layout = QtWidgets.QHBoxLayout()
                    layout.setSpacing(10)
                    self.exportSkinWeights_VLayout.addLayout(layout)

                    # create checkbox
                    checkBox = QtWidgets.QCheckBox()
                    layout.addWidget(checkBox)
                    checkBox.setChecked(True)

                    # create non editable line edit
                    niceName = each.rpartition("|")[2]
                    geoName = QtWidgets.QLabel(niceName + " : ")
                    geoName.setProperty("dag", dagPath)
                    layout.addWidget(geoName)
                    geoName.setMinimumSize(QtCore.QSize(180, 30))
                    geoName.setMaximumSize(QtCore.QSize(180, 30))

                    # create editable line edit
                    if cmds.objExists(dagPath + ".weightFile"):
                        path = cmds.getAttr(dagPath + ".weightFile")
                        niceName = path.rpartition("/")[2].partition(".")[0]
                        dirPath = path.rpartition("/")[0]
                        dirPath = utils.returnFriendlyPath(dirPath)
                        self.exportSkinWeights_lineEdit.setText(dirPath)

                    skinFileName = QtWidgets.QLineEdit(niceName)
                    layout.addWidget(skinFileName)
                    skinFileName.setMinimumSize(QtCore.QSize(170, 30))
                    skinFileName.setMaximumSize(QtCore.QSize(170, 30))

            # add spacer
            self.exportSkinWeights_scrollContents.setLayout(self.exportSkinWeights_VLayout)

        else:
            label = QtWidgets.QLabel("No Geometry Selected For Export. Select Geometry and Relaunch.")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.exportSkinWeights_VLayout.addWidget(label)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def exportSkinWeights_fileBrowse(self):
        """
        Open a file dialog that the user can use to browse to the output directory of their choice for saving the
        .weight files to.

        """

        # Need support for defaulting to current project character was last published to and creating character skin
        # weights folder

        try:
            path = cmds.fileDialog2(fm=3, dir=self.toolsPath)[0]
            nicePath = utils.returnFriendlyPath(path)
            self.exportSkinWeights_lineEdit.setText(nicePath)
        except:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def exportSkinWeights_doExport(self):
        """
        Gather the information from the interface and export the skin weights with that information.

        For each piece of geometry, built the path of the .weight file by joining the output path and the .weight
        file name, then call on export_skin_weights from riggingUtils, passing in the .weight file path and the mesh.

        """

        # get the export path
        exportPath = self.exportSkinWeights_lineEdit.text()
        value = False

        # find each lineEdit in the scrollArea and get the entered text
        for i in range(self.exportSkinWeights_VLayout.count()):
            hboxLayout = self.exportSkinWeights_VLayout.itemAt(i)
            for x in range(hboxLayout.count()):
                widget = hboxLayout.itemAt(x)

                # go through each widget in the hboxLayout, and get values
                if type(widget.widget()) == QtWidgets.QLabel:
                    geoName = widget.widget().text().partition(" :")[0]
                    dagname = widget.widget().property("dag")

                # see if the user wants to export the weights for this entry
                if type(widget.widget()) == QtWidgets.QCheckBox:
                    value = widget.widget().isChecked()

                # get the fileName
                if type(widget.widget()) == QtWidgets.QLineEdit:
                    fileName = widget.widget().text()

                    if fileName.find(":") is not -1:
                        # name contains invalid characters for file name.
                        cmds.warning("file name contains invalid characters: ':'")
                        return

                    # create the full path
                    fullPath = utils.returnNicePath(exportPath, fileName + ".weights")
                    if value:
                        # if the checkbox is checked, export skin weights

                        # export the skin data
                        riggingUtils.export_skin_weights(fullPath, dagname)

                        # add exportPath attribute to geometry if it doesn't exist
                        if not cmds.objExists(dagname + ".weightFile"):
                            cmds.addAttr(dagname, longName="weightFile", dt="string", keyable=True)
                        cmds.setAttr(dagname + ".weightFile", fullPath, type="string")

        # close the UI
        self.exportSkinWeights_Win.close()

        # notify user
        try:
            cmds.inViewMessage(amg='<hl>All Weights Have Been Exported</hl>.', pos='midCenter', fade=True)
        except:
            print("All Weights Have Been Exported.")
