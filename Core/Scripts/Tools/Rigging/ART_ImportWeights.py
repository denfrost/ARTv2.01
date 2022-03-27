"""
Author: Jeremy Ernst

    This class builds the interface for importing skin weights from a .weights file.

===============
Class
===============
"""

import os
import traceback
from functools import partial

import maya.cmds as cmds

import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_ImportSkinWeights():
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
        self.buildImportWeightsUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # USER INTERFACE
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildImportWeightsUI(self):
        """
        Build the interface for importing skin weights. The interface will create an entry for every piece of selected
        geometry.

        The interface will look like this:

        .. image:: /images/importWeights.png

        """
        if cmds.window("ART_importSkinWeightsUI", exists=True):
            cmds.deleteUI("ART_importSkinWeightsUI", wnd=True)

        # launch a UI to get the name information
        self.importSkinWeights_Win = QtWidgets.QMainWindow(self.mainUI)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.importSkinWeights_Win.setStyleSheet(self.style)

        # create the main widget
        self.importSkinWeights_mainWidget = QtWidgets.QWidget()
        self.importSkinWeights_Win.setCentralWidget(self.importSkinWeights_mainWidget)

        # set qt object name
        self.importSkinWeights_Win.setObjectName("ART_importSkinWeightsUI")
        self.importSkinWeights_Win.setWindowTitle("Import Skin Weights")

        # create the mainLayout for the ui
        self.importSkinWeights_mainLayout = QtWidgets.QVBoxLayout(self.importSkinWeights_mainWidget)
        self.importSkinWeights_mainLayout.setContentsMargins(5, 5, 5, 5)

        self.importSkinWeights_Win.resize(450, 400)
        # self.importSkinWeights_Win.setSizePolicy(mainSizePolicy)
        self.importSkinWeights_Win.setMinimumSize(QtCore.QSize(450, 400))
        self.importSkinWeights_Win.setMaximumSize(QtCore.QSize(450, 400))

        # create the background image
        self.importSkinWeights_frame = QtWidgets.QFrame()
        self.importSkinWeights_mainLayout.addWidget(self.importSkinWeights_frame)
        self.importSkinWeights_frame.setObjectName("dark")

        # create widgetLayout
        self.importSkinWeights_widgetLayout = QtWidgets.QVBoxLayout(self.importSkinWeights_frame)

        # import skin weights method
        # self.importSkinWeights_methodForm = QtWidgets.QHBoxLayout()
        # self.importSkinWeights_widgetLayout.addLayout(self.importSkinWeights_methodForm)
        #
        # label = QtWidgets.QLabel("Import Method:  ")
        # label.setStyleSheet("background: transparent;")
        # self.importSkinWeights_methodForm.addWidget(label)

        # self.importSkinWeights_importMethod = QtWidgets.QComboBox()
        # self.importSkinWeights_methodForm.addWidget(self.importSkinWeights_importMethod)
        # self.importSkinWeights_importMethod.addItem("Vertex Order")
        # self.importSkinWeights_importMethod.addItem("World Position")
        # self.importSkinWeights_importMethod.addItem("Local Position")
        # self.importSkinWeights_importMethod.addItem("UV Position")

        # scroll area contents
        self.importSkinWeights_scrollContents = QtWidgets.QFrame()
        self.importSkinWeights_scrollContents.setObjectName("light")

        # Layout of Container Widget
        self.importSkinWeights_VLayout = QtWidgets.QVBoxLayout()
        self.importSkinWeights_VLayout.setSpacing(5)

        # find selected geometry and populate scroll area
        self.importSkinWeights_populate()

        # add scrollArea for selected geo, skinFileName, and checkbox for importing
        self.importSkinWeights_scrollLayout = QtWidgets.QScrollArea()
        self.importSkinWeights_widgetLayout.addWidget(self.importSkinWeights_scrollLayout)
        self.importSkinWeights_scrollLayout.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.importSkinWeights_scrollLayout.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.importSkinWeights_scrollLayout.setWidgetResizable(False)
        self.importSkinWeights_scrollLayout.setWidget(self.importSkinWeights_scrollContents)

        # refresh and import button
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)

        self.importSkinWeights_BtnLayout = QtWidgets.QHBoxLayout()
        self.importSkinWeights_widgetLayout.addLayout(self.importSkinWeights_BtnLayout)

        self.importSkinWeights_RefreshBtn = QtWidgets.QPushButton("Refresh")
        self.importSkinWeights_BtnLayout.addWidget(self.importSkinWeights_RefreshBtn)
        self.importSkinWeights_RefreshBtn.setMinimumSize(QtCore.QSize(70, 50))
        self.importSkinWeights_RefreshBtn.setMaximumSize(QtCore.QSize(70, 50))
        self.importSkinWeights_RefreshBtn.setFont(font)
        self.importSkinWeights_RefreshBtn.clicked.connect(partial(self.buildImportWeightsUI))
        self.importSkinWeights_RefreshBtn.setObjectName("settings")

        self.importSkinWeights_ImportBtn = QtWidgets.QPushButton("IMPORT WEIGHTS")
        self.importSkinWeights_BtnLayout.addWidget(self.importSkinWeights_ImportBtn)
        self.importSkinWeights_ImportBtn.setMinimumSize(QtCore.QSize(330, 50))
        self.importSkinWeights_ImportBtn.setMaximumSize(QtCore.QSize(330, 50))
        self.importSkinWeights_ImportBtn.setFont(font)
        self.importSkinWeights_ImportBtn.clicked.connect(partial(self.importSkinWeights_DoImport))
        self.importSkinWeights_ImportBtn.setObjectName("settings")

        # lastly, progress bar
        self.importSkinWeights_progBarTotal = QtWidgets.QProgressBar()
        self.importSkinWeights_widgetLayout.addWidget(self.importSkinWeights_progBarTotal)
        self.importSkinWeights_progBarTotal.setRange(0, self.importSkinWeights_VLayout.count() - 1)
        self.importSkinWeights_progBarTotal.setValue(0)

        self.importSkinWeights_progBarCurrent = QtWidgets.QProgressBar()
        self.importSkinWeights_widgetLayout.addWidget(self.importSkinWeights_progBarCurrent)
        self.importSkinWeights_progBarCurrent.setRange(0, 100)
        self.importSkinWeights_progBarCurrent.setValue(0)

        # show window
        self.importSkinWeights_Win.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importSkinWeights_populate(self):
        """
        Populate the interface with an entry for each piece of selected geometry. Each entry will have the geometry
        name and allow the user to point to the geometry's .weight file.
        """

        # get current selection
        selection = cmds.ls(sl=True)
        if len(selection) > 0:

            # Create headers
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)

            headerLayout = QtWidgets.QHBoxLayout()
            self.importSkinWeights_VLayout.addLayout(headerLayout)
            headerExport = QtWidgets.QLabel(" ")
            headerExport.setStyleSheet("background: transparent;")
            headerLayout.addWidget(headerExport)

            headerGeo = QtWidgets.QLabel("Mesh")
            headerGeo.setStyleSheet("background: transparent;")
            headerGeo.setMinimumSize(QtCore.QSize(180, 20))
            headerGeo.setMaximumSize(QtCore.QSize(180, 20))
            headerLayout.addWidget(headerGeo)
            headerGeo.setFont(font)

            headerFileName = QtWidgets.QLabel("Weight File")
            headerFileName.setStyleSheet("background: transparent;")
            headerLayout.addWidget(headerFileName)
            headerFileName.setMinimumSize(QtCore.QSize(180, 20))
            headerFileName.setMaximumSize(QtCore.QSize(180, 20))
            headerFileName.setFont(font)

            # get a list of weight files
            weightFiles = []
            for root, subFolders, files in os.walk(self.toolsPath):
                for file in files:
                    if file.rpartition(".")[2] == "weights":
                        fullPath = utils.returnFriendlyPath(os.path.join(root, file))

                        weightFiles.append(fullPath)
            print weightFiles
            # loop through selection, checking selection is valid and has skinCluster
            for each in selection:

                try:
                    # get dagPath and shape and create a nice display name
                    dagPath = cmds.ls(each, long=True)[0]
                    shapeNode = cmds.listRelatives(dagPath, children=True)
                    nicename = each.rpartition("|")[2]
                except Exception, e:
                    traceback.format_exc()

                try:
                    if cmds.nodeType(dagPath + "|" + shapeNode[0]) == "mesh":
                        # create HBoxLayout
                        layout = QtWidgets.QHBoxLayout()
                        layout.setSpacing(10)
                        self.importSkinWeights_VLayout.addLayout(layout)

                        # create checkbox
                        checkBox = QtWidgets.QCheckBox()
                        layout.addWidget(checkBox)
                        checkBox.setChecked(True)

                        # create non editable line edit
                        geoName = QtWidgets.QLabel(nicename + " : ")
                        geoName.setStyleSheet("background: transparent;")
                        geoName.setProperty("dag", dagPath)
                        layout.addWidget(geoName)
                        geoName.setMinimumSize(QtCore.QSize(100, 30))
                        geoName.setMaximumSize(QtCore.QSize(100, 30))

                        # create editable line edit
                        skinFileName = QtWidgets.QLineEdit()
                        layout.addWidget(skinFileName)
                        skinFileName.setMinimumSize(QtCore.QSize(205, 30))
                        skinFileName.setMaximumSize(QtCore.QSize(205, 30))

                        # try to find a matching weight file
                        for file in weightFiles:
                            compareString = file.rpartition("/")[2].partition(".")[0]
                            if nicename.lower() == compareString.lower():
                                skinFileName.setText(file)

                        # check if geometry has weights file associated already
                        if cmds.objExists(dagPath + ".weightFile"):
                            path = cmds.getAttr(dagPath + ".weightFile")
                            path = utils.returnFriendlyPath(path)
                            if os.path.exists(path):
                                skinFileName.setText(path)

                        # browse button
                        browseBtn = QtWidgets.QPushButton()
                        layout.addWidget(browseBtn)
                        browseBtn.setMinimumSize(35, 35)
                        browseBtn.setMaximumSize(35, 35)
                        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/fileBrowse.png"))
                        browseBtn.setIconSize(QtCore.QSize(30, 30))
                        browseBtn.setIcon(icon)
                        browseBtn.clicked.connect(partial(self.importSkinWeights_fileBrowse, skinFileName))
                except Exception, e:
                    print traceback.format_exc()

            # add spacer
            self.importSkinWeights_scrollContents.setLayout(self.importSkinWeights_VLayout)

        else:
            label = QtWidgets.QLabel("No Geometry Selected For Import. Select Geometry and Relaunch.")
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.importSkinWeights_VLayout.addWidget(label)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importSkinWeights_fileBrowse(self, lineEdit):
        """
        Open a file dialog that the user can use to browse to the .weight file, then set the text of the passed-in
        line edit to be the path to the .weights file.

        :param lineEdit: QLineEdit to set path text to.
        """

        # Need support for defaulting to current project character was last published to and creating character
        # skin weights folder

        try:
            path = cmds.fileDialog2(fm=1, dir=self.toolsPath)[0]
            nicePath = utils.returnFriendlyPath(path)
            lineEdit.setText(nicePath)
        except:
            pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importSkinWeights_DoImport(self):
        """
        Gather the information from the interface and import the skin weights with that information.

        For each piece of geometry, get the associated .weight file on disk, then call on import_skin_weights
        from riggingUtils, passing in the .weight file path and the mesh.

        """
        # which method?
        # method = self.importSkinWeights_importMethod.currentText()

        # error report messages
        errorMessages = []

        # weight files
        weightFiles = []

        # find each lineEdit in the scrollArea and get the entered text
        for i in range(self.importSkinWeights_VLayout.count()):
            hboxLayout = self.importSkinWeights_VLayout.itemAt(i)
            value, fileName, mesh = None, None, None
            for x in range(hboxLayout.count()):
                widget = hboxLayout.itemAt(x)
                # go through each widget in the hboxLayout, and get values
                if type(widget.widget()) == QtWidgets.QLabel:
                    geoName = widget.widget().text()
                    geoName = geoName.partition(" :")[0]
                    if cmds.objExists(geoName):
                        mesh = cmds.ls(geoName, long=True)[0]

                # see if the user wants to export the weights for this entry
                if type(widget.widget()) == QtWidgets.QCheckBox:
                    value = widget.widget().isChecked()

                # get the fileName
                if type(widget.widget()) == QtWidgets.QLineEdit:
                    fileName = widget.widget().text()

                    # if the box is checked for import, do the import
            if (value and mesh and fileName):
                ###############################
                # BEGIN WEIGHT IMPORT

                # try to load the given file
                if os.path.exists(fileName):
                    weightFiles.append(fileName)
                else:
                    cmds.error('ART_ImportWeights: Skin file does not exist: ' + fileName)
                    return False
                if not mesh:
                    cmds.error('ART_ImportWeights: Mesh does not exist!')
                    return False
                # update the total progress bar
                incrementValue = self.importSkinWeights_progBarTotal.value() + 1
                self.importSkinWeights_progBarTotal.setValue(incrementValue)

                # create a skinWeights class with the skin file
                if fileName:
                    print 'Loading skinWeights from ', str(fileName)
                    riggingUtils.import_skin_weights(fileName, mesh, True)

        # ask if user wants to delete weight files
        file_string = ""
        for file in weightFiles:
            file_name = os.path.basename(file)
            file_string += file_name + "\n"

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Would you like to delete the following weight files?")
        msgBox.setDetailedText(file_string)
        msgBox.addButton("Yes", QtWidgets.QMessageBox.YesRole)
        msgBox.addButton("No", QtWidgets.QMessageBox.NoRole)
        ret = msgBox.exec_()

        if ret == 0:
            for file in weightFiles:
                try:
                    os.remove(file)
                except:
                    cmds.warning("Unable to delete file: " + str(file))
        if ret == 1:
            return
