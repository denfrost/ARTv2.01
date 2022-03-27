import math
import os
from functools import partial

import maya.OpenMayaUI as mui
import maya.cmds as cmds
import maya.mel as mel
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken

import Utilities.utils as utils
import Utilities.riggingUtils as riggingUtils
import Utilities.interfaceUtils as interfaceUtils


def getMainWindow():
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    # pyside QMainWindow takes in a QWidget rather than QObject
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


class ART_SkinTools(QtWidgets.QMainWindow):
    def __init__(self, mainUI, attachToRigInterface, parent):

        super(ART_SkinTools, self).__init__(parent=None)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)
        self.setWindowTitle("Deformation Tools")

        # build the UI
        self.buildSkinToolsUI(attachToRigInterface)

        # UI Skin Cluster
        self.skinCluster = None

        # how to run the UI
        if attachToRigInterface:
            self.mainUI.toolModeStack.addWidget(self.deformationTabWidget)

        # standalone (WORK IN PROGRESS)
        else:
            self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
            self.setMinimumSize(QtCore.QSize(580, 600))
            self.setMaximumSize(QtCore.QSize(580, 900))
            self.setContentsMargins(0, 0, 0, 0)
            self.resize(580, 900)
            self.setCentralWidget(self.deformationTabWidget)

            self.show()
            self.weightTable_scriptJob()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildSkinToolsUI(self, attachToRigInterface):

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # add the widget to the stacked widget
        self.deformationTabWidget = QtWidgets.QWidget()
        self.deformation_mainLayout = QtWidgets.QVBoxLayout(self.deformationTabWidget)

        # create the menu bar
        if attachToRigInterface:
            self.deformation_menuBar = QtWidgets.QMenuBar()
            self.deformation_menuBar.setMaximumHeight(20)
            self.deformation_mainLayout.addWidget(self.deformation_menuBar)

            # add items to menu bar
            debugMenu = self.deformation_menuBar.addMenu("Development Tools")
            debugMenu.addAction("Test Building Rigs", self.debugRigs)

        # create the toolbar layout
        self.deformation_toolFrame = QtWidgets.QFrame()
        self.deformation_toolFrame.setObjectName("darkborder")
        self.deformation_toolFrame.setMaximumHeight(52)

        self.deformation_mainLayout.addWidget(self.deformation_toolFrame)

        self.deformation_toolbarLayout = QtWidgets.QHBoxLayout(self.deformation_toolFrame)
        self.deformation_toolbarLayout.setDirection(QtWidgets.QBoxLayout.LeftToRight)
        self.deformation_toolbarLayout.setSpacing(10)

        # toolbar buttons

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/paintWeights.png")
        self.weightTable_paintWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_paintWeightsBtn)
        self.weightTable_paintWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_paintWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_paintWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_paintWeightsBtn.setIcon(icon)
        self.weightTable_paintWeightsBtn.clicked.connect(self.weightTable_paintWeightsMode)
        text = "Enter \'Paint Skin Weights\' tool."
        self.weightTable_paintWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/addRemove.png")
        self.weightTable_addRemoveInfsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_addRemoveInfsBtn)
        self.weightTable_addRemoveInfsBtn.setMinimumSize(35, 35)
        self.weightTable_addRemoveInfsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_addRemoveInfsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_addRemoveInfsBtn.setIcon(icon)
        self.weightTable_addRemoveInfsBtn.clicked.connect(self.addOrRemoveInfs_UI)
        text = "Opens a tool to add or remove influences."
        self.weightTable_addRemoveInfsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/mirrorWeights.png")
        self.weightTable_mirrorWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_mirrorWeightsBtn)
        self.weightTable_mirrorWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_mirrorWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_mirrorWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_mirrorWeightsBtn.setIcon(icon)
        self.weightTable_mirrorWeightsBtn.clicked.connect(self.paintSkinWeights_mirrorSkinWeights)
        text = "Mirror Skin Weights."
        self.weightTable_mirrorWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/importSkin.png")
        self.weightTable_importSkinWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_importSkinWeightsBtn)
        self.weightTable_importSkinWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_importSkinWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_importSkinWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_importSkinWeightsBtn.setIcon(icon)
        self.weightTable_importSkinWeightsBtn.setFont(headerFont)
        self.weightTable_importSkinWeightsBtn.clicked.connect(self.paintSkinWeights_importSkinWeights)
        text = "Import Skin Weights."
        self.weightTable_importSkinWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/exportSkin.png")
        self.weightTable_exportSkinWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_exportSkinWeightsBtn)
        self.weightTable_exportSkinWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_exportSkinWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_exportSkinWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_exportSkinWeightsBtn.setIcon(icon)
        self.weightTable_exportSkinWeightsBtn.clicked.connect(self.paintSkinWeights_exportSkinWeights)
        text = "Export Skin Weights."
        self.weightTable_exportSkinWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/smartCopy.png")
        self.weightTable_smartCopyWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_smartCopyWeightsBtn)
        self.weightTable_smartCopyWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_smartCopyWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_smartCopyWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_smartCopyWeightsBtn.setIcon(icon)
        self.weightTable_smartCopyWeightsBtn.clicked.connect(self.paintSkinWeights_copySkinWeights)
        text = "Copy Skin Weights. Select the source object first, then the target object."
        self.weightTable_smartCopyWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/moveInfs.png")
        self.weightTable_moveInfsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_moveInfsBtn)
        self.weightTable_moveInfsBtn.setMinimumSize(35, 35)
        self.weightTable_moveInfsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_moveInfsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_moveInfsBtn.setIcon(icon)
        self.weightTable_moveInfsBtn.clicked.connect(partial(self.moveInfluences_UI))
        text = "Move Weights Tool. Move the weights from one influence to another influence."
        self.weightTable_moveInfsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/fixWeights.png")
        self.weightTable_fixWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_fixWeightsBtn)
        self.weightTable_fixWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_fixWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_fixWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_fixWeightsBtn.setIcon(icon)
        self.weightTable_fixWeightsBtn.setFont(headerFont)
        self.weightTable_fixWeightsBtn.clicked.connect(riggingUtils.fixSkinWeights)
        text = "Fix Skin Weights Tool. Copies the mesh, deletes history, and transfers the weights to the mesh."
        self.weightTable_fixWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/hammer.png")
        self.weightTable_hammerWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_hammerWeightsBtn)
        self.weightTable_hammerWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_hammerWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_hammerWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_hammerWeightsBtn.setIcon(icon)
        self.weightTable_hammerWeightsBtn.clicked.connect(self.paintSkinWeights_hammerSkinWeights)
        text = "Hammer Skin Weights."
        self.weightTable_hammerWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/wizard.png")
        self.weightTable_weightWizardBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_weightWizardBtn)
        self.weightTable_weightWizardBtn.setMinimumSize(35, 35)
        self.weightTable_weightWizardBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_weightWizardBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_weightWizardBtn.setIcon(icon)
        self.weightTable_weightWizardBtn.clicked.connect(self.paintSkinWeights_deformationWizardLaunch)
        self.weightTable_weightWizardBtn.setToolTip("Launch Skinning Wizard")
        text = "Open Skinning Wizard."
        self.weightTable_weightWizardBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/bindTool.png")
        self.weightTable_bindWeightsBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_bindWeightsBtn)
        self.weightTable_bindWeightsBtn.setMinimumSize(35, 35)
        self.weightTable_bindWeightsBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_bindWeightsBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_bindWeightsBtn.setIcon(icon)
        self.weightTable_bindWeightsBtn.clicked.connect(self.paintSkinWeights_smoothSkinUI)
        self.weightTable_bindWeightsBtn.setToolTip("Smooth Bind Tool")
        text = "Open Smooth Bind Tool."
        self.weightTable_bindWeightsBtn.setToolTip(text)

        buttonBkrd = utils.returnNicePath(self.iconsPath, "System/rename.png")
        self.weightTable_overrideJointNamesBtn = QtWidgets.QPushButton()
        self.deformation_toolbarLayout.addWidget(self.weightTable_overrideJointNamesBtn)
        self.weightTable_overrideJointNamesBtn.setMinimumSize(35, 35)
        self.weightTable_overrideJointNamesBtn.setMaximumSize(35, 35)
        icon = QtGui.QIcon(buttonBkrd)
        self.weightTable_overrideJointNamesBtn.setIconSize(QtCore.QSize(30, 30))
        self.weightTable_overrideJointNamesBtn.setIcon(icon)
        self.weightTable_overrideJointNamesBtn.clicked.connect(self.overrideJointNames_UI)
        text = "Override Joint Names."
        self.weightTable_overrideJointNamesBtn.setToolTip(text)

        self.deformation_toolbarLayout.addSpacerItem(
            QtWidgets.QSpacerItem(500, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        # Add Items to the Menu Bar

        # Add the main widget that will house all of the main UI components
        self.defomation_mainWidget = QtWidgets.QStackedWidget()
        self.defomation_mainWidget.setMinimumSize(QtCore.QSize(560, 400))
        self.defomation_mainWidget.setMaximumSize(QtCore.QSize(560, 900))
        self.deformation_mainLayout.addWidget(self.defomation_mainWidget)

        # add pages to the stackedwidget
        self.defomation_subWidget = QtWidgets.QWidget()
        self.defomation_mainWidget.addWidget(self.defomation_subWidget)
        self.deformationPaintWeightsWidget = QtWidgets.QWidget()
        self.defomation_mainWidget.addWidget(self.deformationPaintWeightsWidget)

        # add hbox layout that splits tools and channel box
        self.deformation_hBoxLayout = QtWidgets.QHBoxLayout(self.defomation_subWidget)
        self.defomation_mainWidget.setCurrentIndex(0)

        # tools layout scroll layout
        self.weightTableScrollArea = QtWidgets.QScrollArea()
        self.weightTableScrollArea.setMinimumSize(QtCore.QSize(310, 500))
        self.weightTableScrollArea.setMaximumSize(QtCore.QSize(310, 6000))
        self.weightTableScrollArea.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))
        self.weightTableScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.deformation_hBoxLayout.addWidget(self.weightTableScrollArea)

        # frame
        self.deformation_toolsLayout = QtWidgets.QFrame()
        self.deformation_toolsLayout.setMinimumSize(QtCore.QSize(290, 850))
        self.deformation_toolsLayout.setMaximumSize(QtCore.QSize(290, 6000))
        self.weightTableScrollArea.setWidget(self.deformation_toolsLayout)

        self.weightTableMainLayout = QtWidgets.QVBoxLayout(self.deformation_toolsLayout)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # weight table
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # weight table selection
        self.weightTableSelectionFrame = QtWidgets.QGroupBox("Selection")
        self.weightTableSelectionFrame.setFont(headerFont)
        self.weightTableSelectionFrame.setObjectName("light")
        self.weightTableSelectionFrame.setMinimumSize(QtCore.QSize(275, 100))
        self.weightTableSelectionFrame.setMaximumSize(QtCore.QSize(275, 100))
        self.weightTableSelectionMain = QtWidgets.QVBoxLayout(self.weightTableSelectionFrame)
        self.weightTableSelection = QtWidgets.QHBoxLayout()
        self.weightTableSelectionMain.addLayout(self.weightTableSelection)
        self.weightTableMainLayout.addWidget(self.weightTableSelectionFrame)

        self.growSelection = QtWidgets.QPushButton("Grow")
        self.growSelection.setMinimumHeight(30)
        self.weightTableSelection.addWidget(self.growSelection)
        self.growSelection.clicked.connect(partial(self.weightTable_growOrShrink, 1))
        self.growSelection.setToolTip("Grow Selection")
        self.growSelection.setObjectName("settings")

        self.shrinkSelection = QtWidgets.QPushButton("Shrink")
        self.shrinkSelection.setMinimumHeight(30)
        self.weightTableSelection.addWidget(self.shrinkSelection)
        self.shrinkSelection.clicked.connect(partial(self.weightTable_growOrShrink, 2))
        self.shrinkSelection.setToolTip("Shrink Selection")
        self.shrinkSelection.setObjectName("settings")

        self.selectLoop = QtWidgets.QPushButton("Loop")
        self.selectLoop.setMinimumHeight(30)
        self.weightTableSelection.addWidget(self.selectLoop)
        self.selectLoop.clicked.connect(partial(self.weightTable_loopOrRing, "loop"))
        self.selectLoop.setToolTip("Select Edge Loop from Selection")
        self.selectLoop.setObjectName("settings")

        self.selectRing = QtWidgets.QPushButton("Ring")
        self.selectRing.setMinimumHeight(30)
        self.weightTableSelection.addWidget(self.selectRing)
        self.selectRing.clicked.connect(partial(self.weightTable_loopOrRing, "ring"))
        self.selectRing.setToolTip("Select Edge Ring from Selection")
        self.selectRing.setObjectName("settings")

        self.selectShell = QtWidgets.QPushButton("Shell")
        self.selectShell.setMinimumHeight(30)
        self.weightTableSelection.addWidget(self.selectShell)
        self.selectShell.clicked.connect(self.weightTable_shell)
        self.selectShell.setToolTip("Select Element")
        self.selectShell.setObjectName("settings")

        self.weightTableIsoLayout = QtWidgets.QHBoxLayout()
        self.weightTableSelectionMain.addLayout(self.weightTableIsoLayout)

        self.isolateSelection = QtWidgets.QPushButton("Isolate Selection")
        self.isolateSelection.setMinimumHeight(30)
        self.weightTableIsoLayout.addWidget(self.isolateSelection)
        self.isolateSelection.setCheckable(True)
        self.isolateSelection.clicked.connect(self.weightTable_isolate)
        self.isolateSelection.setToolTip("Isolate Selection")
        self.isolateSelection.setObjectName("settings")

        # preset weight values
        self.weightTablePresetsFrame = QtWidgets.QGroupBox("Preset Weight Values")
        self.weightTablePresetsFrame.setFont(headerFont)
        self.weightTablePresetsFrame.setObjectName("light")
        self.weightTablePresetsFrame.setMinimumSize(QtCore.QSize(275, 60))
        self.weightTablePresetsFrame.setMaximumSize(QtCore.QSize(275, 60))
        self.weightTablePresets = QtWidgets.QHBoxLayout(self.weightTablePresetsFrame)
        self.weightTableMainLayout.addWidget(self.weightTablePresetsFrame)

        self.weightPreset1 = QtWidgets.QPushButton("0")
        self.weightPreset1.setMinimumHeight(30)
        self.weightTablePresets.addWidget(self.weightPreset1)
        self.weightPreset1.clicked.connect(partial(self.weightTable_addWeight, 0.0))
        self.weightPreset1.setObjectName("orange")

        self.weightPreset2 = QtWidgets.QPushButton(".1")
        self.weightPreset2.setMinimumHeight(30)
        self.weightTablePresets.addWidget(self.weightPreset2)
        self.weightPreset2.clicked.connect(partial(self.weightTable_addWeight, 0.1))
        self.weightPreset2.setObjectName("orange")

        self.weightPreset3 = QtWidgets.QPushButton(".25")
        self.weightPreset3.setMinimumHeight(30)
        self.weightTablePresets.addWidget(self.weightPreset3)
        self.weightPreset3.clicked.connect(partial(self.weightTable_addWeight, 0.25))
        self.weightPreset3.setObjectName("orange")

        self.weightPreset4 = QtWidgets.QPushButton(".5")
        self.weightPreset4.setMinimumHeight(30)
        self.weightTablePresets.addWidget(self.weightPreset4)
        self.weightPreset4.clicked.connect(partial(self.weightTable_addWeight, 0.5))
        self.weightPreset4.setObjectName("orange")

        self.weightPreset5 = QtWidgets.QPushButton(".75")
        self.weightPreset5.setMinimumHeight(30)
        self.weightTablePresets.addWidget(self.weightPreset5)
        self.weightPreset5.clicked.connect(partial(self.weightTable_addWeight, 0.75))
        self.weightPreset5.setObjectName("orange")

        self.weightPreset6 = QtWidgets.QPushButton("1.0")
        self.weightPreset6.setMinimumHeight(30)
        self.weightTablePresets.addWidget(self.weightPreset6)
        self.weightPreset6.clicked.connect(partial(self.weightTable_addWeight, 1.0))
        self.weightPreset6.setObjectName("orange")

        # custom weight values
        self.weightTableCustomFrame = QtWidgets.QGroupBox("Custom Weight Values")
        self.weightTableCustomFrame.setFont(headerFont)
        self.weightTableCustomFrame.setObjectName("light")
        self.weightTableCustomFrame.setMinimumSize(QtCore.QSize(275, 80))
        self.weightTableCustomFrame.setMaximumSize(QtCore.QSize(275, 80))
        self.weightTableCustom = QtWidgets.QVBoxLayout(self.weightTableCustomFrame)
        self.weightTableMainLayout.addWidget(self.weightTableCustomFrame)

        self.setCustomWeightLayout = QtWidgets.QHBoxLayout()
        self.weightTableCustom.addLayout(self.setCustomWeightLayout)

        self.scaleCustomWeightLayout = QtWidgets.QHBoxLayout()
        self.weightTableCustom.addLayout(self.scaleCustomWeightLayout)

        # set weight
        self.setCustomWeight = QtWidgets.QPushButton("Set Weight")
        self.setCustomWeightLayout.addWidget(self.setCustomWeight)
        self.setCustomWeight.clicked.connect(partial(self.weightTable_addWeight, None))
        self.customWeightField = QtWidgets.QDoubleSpinBox()
        self.setCustomWeightLayout.addWidget(self.customWeightField)
        self.customWeightField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setCustomWeight.setObjectName("settings")
        self.setCustomWeight.setMinimumHeight(25)

        self.customWeightField.setRange(0.0, 1.0)
        self.customWeightField.setValue(0.1)
        self.customWeightField.setSingleStep(.01)

        self.setCustomWeightIncrease = QtWidgets.QPushButton("+")
        self.setCustomWeightLayout.addWidget(self.setCustomWeightIncrease)
        self.setCustomWeightIncrease.setMinimumWidth(30)
        self.setCustomWeightIncrease.setMaximumWidth(30)
        self.setCustomWeightIncrease.clicked.connect(partial(self.weightTable_inrementWeight, "up"))
        self.setCustomWeightIncrease.setObjectName("orange")
        self.setCustomWeightIncrease.setMinimumHeight(25)

        self.setCustomWeightDecrease = QtWidgets.QPushButton("-")
        self.setCustomWeightLayout.addWidget(self.setCustomWeightDecrease)
        self.setCustomWeightDecrease.setMinimumWidth(30)
        self.setCustomWeightDecrease.setMaximumWidth(30)
        self.setCustomWeightDecrease.clicked.connect(partial(self.weightTable_inrementWeight, "down"))
        self.setCustomWeightDecrease.setObjectName("orange")
        self.setCustomWeightDecrease.setMinimumHeight(25)

        # scale weight
        self.scaleCustomWeight = QtWidgets.QPushButton("Scale Weight")
        self.scaleCustomWeightLayout.addWidget(self.scaleCustomWeight)
        self.scaleCustomWeight.clicked.connect(partial(self.weightTable_scaleWeight, None))
        self.scaleCustomWeight.setObjectName("settings")
        self.scaleCustomWeight.setMinimumHeight(25)

        self.scaleCustomWeightField = QtWidgets.QDoubleSpinBox()
        self.scaleCustomWeightLayout.addWidget(self.scaleCustomWeightField)
        self.scaleCustomWeightField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.scaleCustomWeightField.setRange(0.0, 1.0)
        self.scaleCustomWeightField.setValue(0.9)
        self.scaleCustomWeightField.setSingleStep(.01)

        self.scaleCustomWeightIncrease = QtWidgets.QPushButton("+")
        self.scaleCustomWeightLayout.addWidget(self.scaleCustomWeightIncrease)
        self.scaleCustomWeightIncrease.setMinimumWidth(30)
        self.scaleCustomWeightIncrease.setMaximumWidth(30)
        self.scaleCustomWeightIncrease.clicked.connect(partial(self.weightTable_scaleWeight, "up"))
        self.scaleCustomWeightIncrease.setObjectName("orange")
        self.scaleCustomWeightIncrease.setMinimumHeight(25)

        self.scaleCustomWeightDecrease = QtWidgets.QPushButton("-")
        self.scaleCustomWeightLayout.addWidget(self.scaleCustomWeightDecrease)
        self.scaleCustomWeightDecrease.setMinimumWidth(30)
        self.scaleCustomWeightDecrease.setMaximumWidth(30)
        self.scaleCustomWeightDecrease.clicked.connect(partial(self.weightTable_scaleWeight, "down"))
        self.scaleCustomWeightDecrease.setObjectName("orange")
        self.scaleCustomWeightDecrease.setMinimumHeight(25)

        # Value Transfer
        self.weightTablevalueXferFrame = QtWidgets.QGroupBox("Value Transfer")
        self.weightTablevalueXferFrame.setFont(headerFont)
        self.weightTablevalueXferFrame.setObjectName("light")
        self.weightTablevalueXferFrame.setMinimumSize(QtCore.QSize(275, 60))
        self.weightTablevalueXferFrame.setMaximumSize(QtCore.QSize(275, 60))
        self.weightTableXferLayout = QtWidgets.QHBoxLayout(self.weightTablevalueXferFrame)
        self.weightTableMainLayout.addWidget(self.weightTablevalueXferFrame)

        self.weightTable_copyValues = QtWidgets.QPushButton("Copy")
        self.weightTable_copyValues.setMinimumHeight(30)
        self.weightTableXferLayout.addWidget(self.weightTable_copyValues)
        self.weightTable_copyValues.clicked.connect(self.weightTable_copyWeight)
        self.weightTable_copyValues.setObjectName("settings")

        self.weightTable_pasteValues = QtWidgets.QPushButton("Paste")
        self.weightTable_pasteValues.setMinimumHeight(30)
        self.weightTableXferLayout.addWidget(self.weightTable_pasteValues)
        self.weightTable_pasteValues.clicked.connect(self.weightTable_pasteWeight)
        self.weightTable_pasteValues.setObjectName("settings")

        self.weightTable_blendValues = QtWidgets.QPushButton("Blend")
        self.weightTable_blendValues.setMinimumHeight(30)
        self.weightTableXferLayout.addWidget(self.weightTable_blendValues)
        self.weightTable_blendValues.clicked.connect(self.weightTable_blendWeight)
        self.weightTable_blendValues.setObjectName("settings")

        # vertex buffer
        self.vertexBufferLayout = QtWidgets.QLineEdit()
        self.vertexBufferLayout.setReadOnly(True)
        self.weightTableMainLayout.addWidget(self.vertexBufferLayout)
        self.vertexBufferLayout.setPlaceholderText("No vertex data copied...")

        # List of skin joints
        self.weightTablevalueskinJointsFrame = QtWidgets.QGroupBox("Skin Joints")
        self.weightTablevalueskinJointsFrame.setFont(headerFont)
        self.weightTablevalueskinJointsFrame.setObjectName("light")
        self.weightTablevalueskinJointsFrame.setMinimumSize(QtCore.QSize(275, 200))
        self.weightTablevalueskinJointsFrame.setMaximumSize(QtCore.QSize(275, 200))
        self.weightTablevalueskinJointsLayout = QtWidgets.QHBoxLayout(self.weightTablevalueskinJointsFrame)
        self.weightTableMainLayout.addWidget(self.weightTablevalueskinJointsFrame)

        self.weightTable_skinJoints = QtWidgets.QListWidget()
        self.weightTablevalueskinJointsLayout.addWidget(self.weightTable_skinJoints)
        self.weightTable_skinJoints.itemClicked.connect(partial(self.weightTable_connectInfluenceLists, True, False))

        # button layout
        self.weightTableSkinJointsButtons = QtWidgets.QVBoxLayout()
        self.weightTablevalueskinJointsLayout.addLayout(self.weightTableSkinJointsButtons)

        # add show influenced verts button
        self.weightTableShowInfVerts = QtWidgets.QPushButton()
        self.weightTableShowInfVerts.setObjectName("settings")
        self.weightTableSkinJointsButtons.addWidget(self.weightTableShowInfVerts)
        self.weightTableShowInfVerts.setMinimumSize(QtCore.QSize(32, 32))
        self.weightTableShowInfVerts.setMaximumSize(QtCore.QSize(32, 32))
        self.weightTableShowInfVerts.setToolTip("Show vertices influenced by selected joint in list.")
        self.weightTableShowInfVerts.clicked.connect(partial(self.weightTable_showInfluencedVerts, False))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/showVerts.png"))
        self.weightTableShowInfVerts.setIconSize(QtCore.QSize(30, 30))
        self.weightTableShowInfVerts.setIcon(icon)

        # show influenced verts in selection button
        self.weightTableShowInfVertsSel = QtWidgets.QPushButton()
        self.weightTableShowInfVertsSel.setObjectName("settings")
        self.weightTableSkinJointsButtons.addWidget(self.weightTableShowInfVertsSel)
        self.weightTableShowInfVertsSel.setMinimumSize(QtCore.QSize(32, 32))
        self.weightTableShowInfVertsSel.setMaximumSize(QtCore.QSize(32, 32))
        self.weightTableShowInfVertsSel.setToolTip("Show vertices influenced by selected joint in current selection.")
        self.weightTableShowInfVertsSel.clicked.connect(partial(self.weightTable_showInfluencedVerts, True))
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/showVertsInSel.png"))
        self.weightTableShowInfVertsSel.setIconSize(QtCore.QSize(30, 30))
        self.weightTableShowInfVertsSel.setIcon(icon)

        # toggle joint selection filter
        self.weightTableJointSel = QtWidgets.QPushButton()
        self.weightTableJointSel.setObjectName("settings")
        self.weightTableSkinJointsButtons.addWidget(self.weightTableJointSel)
        self.weightTableJointSel.setMinimumSize(QtCore.QSize(32, 32))
        self.weightTableJointSel.setMaximumSize(QtCore.QSize(32, 32))
        self.weightTableJointSel.setToolTip("Toggle Joint Selection Filter.")
        self.weightTableJointSel.setCheckable(True)
        self.weightTableJointSel.clicked.connect(self.weightTable_toggleJointSelectMode)
        icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/jointFilter.png"))
        self.weightTableJointSel.setIconSize(QtCore.QSize(30, 30))
        self.weightTableJointSel.setIcon(icon)

        # list of vertices' joints/influence amounts
        self.weightTablevalueVertsFrame = QtWidgets.QGroupBox("Vertex Skin Info")
        self.weightTablevalueVertsFrame.setObjectName("light")
        self.weightTablevalueVertsFrame.setFont(headerFont)
        self.weightTablevalueVertsFrame.setMinimumSize(QtCore.QSize(275, 200))
        self.weightTablevalueVertsFrame.setMaximumSize(QtCore.QSize(275, 200))
        self.weightTablevalueVertsLayout = QtWidgets.QHBoxLayout(self.weightTablevalueVertsFrame)
        self.weightTableMainLayout.addWidget(self.weightTablevalueVertsFrame)
        self.weightTableSplitter = QtWidgets.QSplitter()
        self.weightTablevalueVertsLayout.addWidget(self.weightTableSplitter)

        # vertex list
        self.weightTableVertList = QtWidgets.QListWidget()
        self.weightTableSplitter.addWidget(self.weightTableVertList)
        self.weightTableVertList.itemClicked.connect(partial(self.weightTable_connectInfluenceLists, False, True))

        # set context menu policy on groupbox
        self.weightTableVertList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.weightTableVertList.customContextMenuRequested.connect(self.createContextMenuWeightTable)

        # create the header
        customColor = QtGui.QColor(25, 175, 255)
        labelItem = QtWidgets.QListWidgetItem("Joint")
        labelItem.setFont(headerFont)
        labelItem.setFlags(QtCore.Qt.NoItemFlags)
        labelItem.setForeground(customColor)
        labelItem.setBackground(QtCore.Qt.black)
        labelItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.weightTableVertList.addItem(labelItem)

        # influence list
        self.weightTableInfList = QtWidgets.QListWidget()
        self.weightTableSplitter.addWidget(self.weightTableInfList)

        # create the header
        labelValue = QtWidgets.QListWidgetItem("Avg. Weight")
        labelValue.setFont(headerFont)
        labelValue.setFlags(QtCore.Qt.NoItemFlags)
        labelValue.setForeground(customColor)
        labelValue.setBackground(QtCore.Qt.black)
        labelValue.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.weightTableInfList.addItem(labelValue)

        # space
        self.weightTableMainLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # channel box layout frame
        self.deformation_cbLayout = QtWidgets.QFrame()
        self.deformation_cbLayout.setObjectName("darkborder")

        # set dimensions of channel box frame
        self.deformation_cbLayout.setMinimumSize(QtCore.QSize(220, 600))
        self.deformation_cbLayout.setMaximumSize(QtCore.QSize(220, 600))
        self.deformation_hBoxLayout.addWidget(self.deformation_cbLayout)

        # add channel box layout
        self.deformation_channelBoxLayout = QtWidgets.QVBoxLayout(self.deformation_cbLayout)

        # add the channel box from Maya to the UI
        channelBoxWidget = cmds.channelBox(w=150, h=570)
        pointer = mui.MQtUtil.findControl(channelBoxWidget)
        self.channelBox = shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)
        self.deformation_channelBoxLayout.addWidget(self.channelBox)
        self.channelBox.show()

        self.deformation_channelBoxLayout.addSpacerItem(
            QtWidgets.QSpacerItem(220, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # add the bottom buttons for Edit Setup and Build Rig
        self.deformation_bottomButtonLayout = QtWidgets.QHBoxLayout()
        self.deformation_bottomButtonLayout.setContentsMargins(25, 0, 0, 0)

        if attachToRigInterface:
            # edit setup

            font = QtGui.QFont()
            font.setBold(True)
            font.setPointSize(20)

            self.deformation_editSetupBtn = QtWidgets.QPushButton("Edit Setup")
            self.deformation_editSetupBtn.setMinimumHeight(50)
            self.deformation_editSetupBtn.setMaximumHeight(50)
            self.deformation_bottomButtonLayout.addWidget(self.deformation_editSetupBtn)
            self.deformation_mainLayout.addLayout(self.deformation_bottomButtonLayout)
            self.deformation_editSetupBtn.clicked.connect(self.mainUI.editSetup)
            self.deformation_editSetupBtn.setProperty("boldFont", True)
            self.deformation_editSetupBtn.setFont(font)
            text = "Go back to the previous phase to edit/add modules, adjust settings, or adjust placement."
            self.deformation_editSetupBtn.setToolTip(text)

            # build rig
            self.deformation_buildRigBtn = QtWidgets.QPushButton("Build Rig")
            self.deformation_buildRigBtn.setMinimumHeight(50)
            self.deformation_buildRigBtn.setMaximumHeight(50)
            self.deformation_bottomButtonLayout.addWidget(self.deformation_buildRigBtn)
            self.deformation_mainLayout.addLayout(self.deformation_bottomButtonLayout)
            self.deformation_buildRigBtn.clicked.connect(self.mainUI.buildRig)
            self.deformation_buildRigBtn.setProperty("boldFont", True)
            self.deformation_buildRigBtn.setFont(font)
            text = "Launch the rig building process. A wizard will walk you through the necessary steps to publish" \
                   " your rig."
            self.deformation_buildRigBtn.setToolTip(text)

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # PAINT SKIN WEIGHTS                               #
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create the vertical layout
        self.psw_topLevelLayout = QtWidgets.QVBoxLayout(self.deformationPaintWeightsWidget)

        # create the scrollLayout
        self.psw_paintWeightsScroll = QtWidgets.QScrollArea()
        self.psw_topLevelLayout.addWidget(self.psw_paintWeightsScroll)
        self.psw_paintWeightsScroll.setMinimumSize(QtCore.QSize(500, 500))
        self.psw_paintWeightsScroll.setMaximumSize(QtCore.QSize(500, 6000))
        self.psw_paintWeightsScroll.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.psw_paintWeightsScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.psw_paintWeightsScrollFrame = QtWidgets.QFrame(self.psw_paintWeightsScroll)
        self.psw_paintWeightsScrollFrame.setObjectName("dark")
        self.psw_paintWeightsScrollFrame.setMinimumSize(QtCore.QSize(500, 1100))
        self.psw_paintWeightsScrollFrame.setMaximumSize(QtCore.QSize(500, 6000))
        self.psw_paintWeightsScrollFrame.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        self.psw_paintWeightsScroll.setWidget(self.psw_paintWeightsScrollFrame)
        self.psw_mainLayout = QtWidgets.QVBoxLayout(self.psw_paintWeightsScrollFrame)

        # create the groupbox for influences
        self.psw_groupBox = QtWidgets.QGroupBox("Influences")
        self.psw_groupBox.setMinimumSize(QtCore.QSize(470, 650))
        self.psw_groupBox.setMaximumSize(QtCore.QSize(470, 650))
        self.psw_groupBox.setFont(headerFont)
        self.psw_mainLayout.addWidget(self.psw_groupBox)
        self.psw_influenceLayout = QtWidgets.QVBoxLayout(self.psw_groupBox)

        # # # influence searches # # #
        self.psw_influenceSearchesLayout = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_influenceSearchesLayout)

        self.psw_modSearchBar = QtWidgets.QLineEdit()
        self.psw_modSearchBar.setPlaceholderText("Search Modules...")
        self.psw_influenceSearchesLayout.addWidget(self.psw_modSearchBar)
        self.psw_modSearchBar.textChanged.connect(self.paintSkinWeights_searchModules)

        self.psw_infSearchBar = QtWidgets.QLineEdit()
        self.psw_infSearchBar.setPlaceholderText("Search Influences...")
        self.psw_influenceSearchesLayout.addWidget(self.psw_infSearchBar)
        self.psw_infSearchBar.textChanged.connect(self.paintSkinWeights_searchInfluences)

        # # # INFLUENCES # # #
        self.psw_influenceListsLayout = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_influenceListsLayout)

        # module list
        self.psw_moduleInfluenceList = QtWidgets.QListWidget()
        self.psw_moduleInfluenceList.setObjectName("dark")
        self.psw_influenceListsLayout.addWidget(self.psw_moduleInfluenceList)
        self.psw_moduleInfluenceList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.psw_moduleInfluenceList.itemSelectionChanged.connect(self.paintSkinWeights_populateInfs)

        # influence list
        self.psw_influenceList = QtWidgets.QListWidget()
        self.psw_influenceList.setObjectName("dark")
        self.psw_influenceListsLayout.addWidget(self.psw_influenceList)
        self.psw_influenceList.itemClicked.connect(self.paintSkinWeights_changeInf)

        # set context menu policy on influence list
        self.psw_influenceList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.psw_influenceList.customContextMenuRequested.connect(self.paintSkinWeights_createContextMenu)

        # paint mode
        self.psw_paintModeLayout = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_paintModeLayout)
        modeLabel = QtWidgets.QLabel("Mode: ")
        modeLabel.setStyleSheet("background: transparent;")
        modeLabel.setFont(headerFont)
        self.psw_paintModeLayout.addWidget(modeLabel)

        self.psw_paintModeButtonGrp = QtWidgets.QButtonGroup()

        self.psw_paintMode_paint = QtWidgets.QRadioButton("Paint")
        self.psw_paintModeLayout.addWidget(self.psw_paintMode_paint)
        self.psw_paintMode_paint.setChecked(True)
        self.psw_paintMode_paint.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "skinPaintMode", str(1), self.psw_paintMode_paint))

        self.psw_paintMode_select = QtWidgets.QRadioButton("Select")
        self.psw_paintModeLayout.addWidget(self.psw_paintMode_select)
        self.psw_paintMode_select.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "skinPaintMode", str(0), self.psw_paintMode_select))

        self.psw_paintMode_paintSelect = QtWidgets.QRadioButton("Paint Select")
        self.psw_paintModeLayout.addWidget(self.psw_paintMode_paintSelect)
        self.psw_paintMode_paintSelect.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "skinPaintMode", str(2), self.psw_paintMode_paintSelect))

        self.psw_paintModeButtonGrp.addButton(self.psw_paintMode_paint, 1)
        self.psw_paintModeButtonGrp.addButton(self.psw_paintMode_select, 2)
        self.psw_paintModeButtonGrp.addButton(self.psw_paintMode_paintSelect, 3)

        # paint select
        self.psw_paintSelectLayout = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_paintSelectLayout)
        paintSelectLabel = QtWidgets.QLabel("Paint Select: ")
        paintSelectLabel.setStyleSheet("background: transparent;")
        paintSelectLabel.setFont(headerFont)
        self.psw_paintSelectLayout.addWidget(paintSelectLabel)

        self.psw_paintSelectButtonGrp = QtWidgets.QButtonGroup()

        self.psw_paintSelect_Add = QtWidgets.QRadioButton("Add")
        self.psw_paintSelectLayout.addWidget(self.psw_paintSelect_Add)
        self.psw_paintSelect_Add.setChecked(True)
        self.psw_paintSelect_Add.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "paintSelectMode", str(1), self.psw_paintSelect_Add))

        self.psw_paintSelect_Remove = QtWidgets.QRadioButton("Remove")
        self.psw_paintSelectLayout.addWidget(self.psw_paintSelect_Remove)
        self.psw_paintSelect_Remove.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "paintSelectMode", str(2), self.psw_paintSelect_Remove))

        self.psw_paintSelect_Toggle = QtWidgets.QRadioButton("Toggle")
        self.psw_paintSelectLayout.addWidget(self.psw_paintSelect_Toggle)
        self.psw_paintSelect_Toggle.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "paintSelectMode", str(3), self.psw_paintSelect_Toggle))

        self.psw_paintSelectButtonGrp.addButton(self.psw_paintSelect_Add, 1)
        self.psw_paintSelectButtonGrp.addButton(self.psw_paintSelect_Remove, 2)
        self.psw_paintSelectButtonGrp.addButton(self.psw_paintSelect_Toggle, 3)

        # paint operation
        self.psw_paintOperationLayout = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_paintOperationLayout)
        paintOperationLabel = QtWidgets.QLabel("Paint Operation: ")
        paintOperationLabel.setStyleSheet("background: transparent;")
        paintOperationLabel.setFont(headerFont)
        self.psw_paintOperationLayout.addWidget(paintOperationLabel)

        self.psw_paintOperation = QtWidgets.QComboBox()
        self.psw_paintOperationLayout.addWidget(self.psw_paintOperation)
        self.psw_paintOperation.currentIndexChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "selectedattroper", "paintOp", self.psw_paintOperation))

        self.psw_paintOperation.addItem("Add")
        self.psw_paintOperation.addItem("Replace")
        self.psw_paintOperation.addItem("Scale")
        self.psw_paintOperation.addItem("Smooth")

        # paint profile
        self.paintProfileButtons = []
        self.psw_paintProfileLayout = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_paintProfileLayout)
        paintProfileLabel = QtWidgets.QLabel("Profile: ")
        paintProfileLabel.setStyleSheet("background: transparent;")
        paintProfileLabel.setFont(headerFont)
        self.psw_paintProfileLayout.addWidget(paintProfileLabel)

        self.paintProfile_buttonGrp = QtWidgets.QButtonGroup()

        self.psw_paintProfile_Gaussian = QtWidgets.QPushButton()
        self.psw_paintProfile_Gaussian.setObjectName("gaussian")
        self.psw_paintProfile_Gaussian.setToolTip("gaussian")
        self.psw_paintProfile_Gaussian.setMinimumSize(QtCore.QSize(30, 30))
        self.psw_paintProfile_Gaussian.setMaximumSize(QtCore.QSize(30, 30))
        self.psw_paintProfileLayout.addWidget(self.psw_paintProfile_Gaussian)
        self.psw_paintProfile_Gaussian.setCheckable(True)
        self.psw_paintProfile_Gaussian.setChecked(True)
        self.psw_paintProfile_Gaussian.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "stampProfile", "\"" + "gaussian" + "\"",
                    self.psw_paintProfile_Gaussian))

        self.psw_paintProfile_Soft = QtWidgets.QPushButton()
        self.psw_paintProfile_Soft.setObjectName("soft")
        self.psw_paintProfile_Soft.setToolTip("soft")
        self.psw_paintProfile_Soft.setMinimumSize(QtCore.QSize(30, 30))
        self.psw_paintProfile_Soft.setMaximumSize(QtCore.QSize(30, 30))
        self.psw_paintProfileLayout.addWidget(self.psw_paintProfile_Soft)
        self.psw_paintProfile_Soft.setCheckable(True)
        self.psw_paintProfile_Soft.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "stampProfile", "\"" + "poly" + "\"", self.psw_paintProfile_Soft))

        self.psw_paintProfile_Solid = QtWidgets.QPushButton()
        self.psw_paintProfile_Solid.setObjectName("solid")
        self.psw_paintProfile_Solid.setToolTip("solid")
        self.psw_paintProfile_Solid.setMinimumSize(QtCore.QSize(30, 30))
        self.psw_paintProfile_Solid.setMaximumSize(QtCore.QSize(30, 30))
        self.psw_paintProfileLayout.addWidget(self.psw_paintProfile_Solid)
        self.psw_paintProfile_Solid.setCheckable(True)
        self.psw_paintProfile_Solid.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "stampProfile", "\"" + "solid" + "\"",
                    self.psw_paintProfile_Solid))

        self.psw_paintProfile_Square = QtWidgets.QPushButton()
        self.psw_paintProfile_Square.setObjectName("square")
        self.psw_paintProfile_Square.setToolTip("square")
        self.psw_paintProfile_Square.setMinimumSize(QtCore.QSize(30, 30))
        self.psw_paintProfile_Square.setMaximumSize(QtCore.QSize(30, 30))
        self.psw_paintProfileLayout.addWidget(self.psw_paintProfile_Square)
        self.psw_paintProfile_Square.setCheckable(True)
        self.psw_paintProfile_Square.clicked.connect(
            partial(self.paintSkinWeights_updateCTX, "stampProfile", "\"" + "square" + "\"",
                    self.psw_paintProfile_Square))

        self.paintProfile_buttonGrp.addButton(self.psw_paintProfile_Gaussian, 1)
        self.paintProfile_buttonGrp.addButton(self.psw_paintProfile_Soft, 2)
        self.paintProfile_buttonGrp.addButton(self.psw_paintProfile_Solid, 3)
        self.paintProfile_buttonGrp.addButton(self.psw_paintProfile_Square, 4)

        # opacity
        line = QtWidgets.QFrame()
        line.setMinimumSize(400, 3)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.psw_influenceLayout.addWidget(line)

        self.psw_opacityLayoutTop = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_opacityLayoutTop)

        opacLabel = QtWidgets.QLabel("Opacity: ")
        opacLabel.setStyleSheet("background: transparent;")
        opacLabel.setFont(headerFont)
        self.psw_opacityLayoutTop.addWidget(opacLabel)

        # # # opacity slider # # #
        self.psw_opacitySlider = QtWidgets.QSlider()
        self.psw_opacityLayoutTop.addWidget(self.psw_opacitySlider)
        self.psw_opacitySlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.psw_opacitySlider.setRange(0, 100)
        self.psw_opacitySlider.setValue(100)
        self.psw_opacitySlider.setSingleStep(1)
        self.psw_opacitySlider.setPageStep(1)
        self.psw_opacitySlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.psw_opacitySlider.setTickInterval(20)

        # # # opacity field # # #
        self.psw_opacityField = QtWidgets.QDoubleSpinBox()
        self.psw_opacityLayoutTop.addWidget(self.psw_opacityField)
        self.psw_opacityField.setValue(1.00)
        self.psw_opacityField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.psw_opacityField.setReadOnly(True)

        # # # opacity signals/slots # # #
        self.psw_opacitySlider.valueChanged.connect(
            partial(self.paintSkinWeights_UpdateSliders, self.psw_opacitySlider, self.psw_opacityField, True))
        self.psw_opacitySlider.valueChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "opacity", "sliderEdit", self.psw_opacitySlider))

        # # # opacity presets # # #
        self.psw_opacityLayoutBottom = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_opacityLayoutBottom)

        label = QtWidgets.QLabel("Presets: ")
        label.setStyleSheet("background: transparent;")
        label.setFont(headerFont)
        self.psw_opacityLayoutBottom.addWidget(label)

        self.psw_opacPreset1 = QtWidgets.QPushButton("0.00")
        self.psw_opacPreset1.setMaximumSize(40, 20)
        self.psw_opacPreset1.setMinimumSize(40, 20)
        self.psw_opacityLayoutBottom.addWidget(self.psw_opacPreset1)
        self.psw_opacPreset1.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_opacitySlider, 0))
        self.psw_opacPreset1.setObjectName("orange")
        self.psw_opacPreset1.setMinimumHeight(25)

        self.psw_opacPreset2 = QtWidgets.QPushButton("0.10")
        self.psw_opacPreset2.setMaximumSize(40, 20)
        self.psw_opacPreset2.setMinimumSize(40, 20)
        self.psw_opacityLayoutBottom.addWidget(self.psw_opacPreset2)
        self.psw_opacPreset2.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_opacitySlider, 10))
        self.psw_opacPreset2.setObjectName("orange")
        self.psw_opacPreset2.setMinimumHeight(25)

        self.psw_opacPreset3 = QtWidgets.QPushButton("0.25")
        self.psw_opacPreset3.setMaximumSize(40, 20)
        self.psw_opacPreset3.setMinimumSize(40, 20)
        self.psw_opacityLayoutBottom.addWidget(self.psw_opacPreset3)
        self.psw_opacPreset3.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_opacitySlider, 25))
        self.psw_opacPreset3.setObjectName("orange")
        self.psw_opacPreset3.setMinimumHeight(25)

        self.psw_opacPreset4 = QtWidgets.QPushButton("0.50")
        self.psw_opacPreset4.setMaximumSize(40, 20)
        self.psw_opacPreset4.setMinimumSize(40, 20)
        self.psw_opacityLayoutBottom.addWidget(self.psw_opacPreset4)
        self.psw_opacPreset4.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_opacitySlider, 50))
        self.psw_opacPreset4.setObjectName("orange")
        self.psw_opacPreset4.setMinimumHeight(25)

        self.psw_opacPreset5 = QtWidgets.QPushButton("0.75")
        self.psw_opacPreset5.setMaximumSize(40, 20)
        self.psw_opacPreset5.setMinimumSize(40, 20)
        self.psw_opacityLayoutBottom.addWidget(self.psw_opacPreset5)
        self.psw_opacPreset5.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_opacitySlider, 75))
        self.psw_opacPreset5.setObjectName("orange")
        self.psw_opacPreset5.setMinimumHeight(25)

        self.psw_opacPreset6 = QtWidgets.QPushButton("1.00")
        self.psw_opacPreset6.setMaximumSize(40, 20)
        self.psw_opacPreset6.setMinimumSize(40, 20)
        self.psw_opacityLayoutBottom.addWidget(self.psw_opacPreset6)
        self.psw_opacPreset6.clicked.connect(
            partial(self.paintSkinWeights_SetSliderValues, self.psw_opacitySlider, 100))
        self.psw_opacPreset6.setObjectName("orange")
        self.psw_opacPreset6.setMinimumHeight(25)

        self.psw_opacityLayoutBottom.setSpacing(20)
        self.psw_opacityLayoutBottom.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        # value
        line = QtWidgets.QFrame()
        line.setMinimumSize(400, 3)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.psw_influenceLayout.addWidget(line)

        self.psw_valueLayoutTop = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_valueLayoutTop)

        valueLabel = QtWidgets.QLabel("Value:    ")
        valueLabel.setStyleSheet("background: transparent;")
        valueLabel.setFont(headerFont)
        self.psw_valueLayoutTop.addWidget(valueLabel)

        # # # value slider # # #
        self.psw_valueSlider = QtWidgets.QSlider()
        self.psw_valueLayoutTop.addWidget(self.psw_valueSlider)
        self.psw_valueSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.psw_valueSlider.setRange(0, 100)
        self.psw_valueSlider.setValue(100)
        self.psw_valueSlider.setSingleStep(1)
        self.psw_valueSlider.setPageStep(1)
        self.psw_valueSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.psw_valueSlider.setTickInterval(20)

        # # # value field # # #
        self.psw_valueField = QtWidgets.QDoubleSpinBox()
        self.psw_valueLayoutTop.addWidget(self.psw_valueField)
        self.psw_valueField.setValue(1.00)
        self.psw_valueField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.psw_valueField.setReadOnly(True)

        # # # value signals/slots # # #
        self.psw_valueSlider.valueChanged.connect(
            partial(self.paintSkinWeights_UpdateSliders, self.psw_valueSlider, self.psw_valueField, True))
        self.psw_valueSlider.valueChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "value", "sliderEdit", self.psw_valueSlider))

        # # # value presets # # #
        self.psw_valueLayoutBottom = QtWidgets.QHBoxLayout()
        self.psw_influenceLayout.addLayout(self.psw_valueLayoutBottom)

        label = QtWidgets.QLabel("Presets: ")
        label.setStyleSheet("background: transparent;")
        label.setFont(headerFont)
        self.psw_valueLayoutBottom.addWidget(label)

        self.psw_valuePreset1 = QtWidgets.QPushButton("0.00")
        self.psw_valuePreset1.setMaximumSize(40, 20)
        self.psw_valuePreset1.setMinimumSize(40, 20)
        self.psw_valueLayoutBottom.addWidget(self.psw_valuePreset1)
        self.psw_valuePreset1.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_valueSlider, 0))
        self.psw_valuePreset1.setObjectName("orange")
        self.psw_valuePreset1.setMinimumHeight(25)

        self.psw_valuePreset2 = QtWidgets.QPushButton("0.10")
        self.psw_valuePreset2.setMaximumSize(40, 20)
        self.psw_valuePreset2.setMinimumSize(40, 20)
        self.psw_valueLayoutBottom.addWidget(self.psw_valuePreset2)
        self.psw_valuePreset2.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_valueSlider, 10))
        self.psw_valuePreset2.setObjectName("orange")
        self.psw_valuePreset2.setMinimumHeight(25)

        self.psw_valuePreset3 = QtWidgets.QPushButton("0.25")
        self.psw_valuePreset3.setMaximumSize(40, 20)
        self.psw_valuePreset3.setMinimumSize(40, 20)
        self.psw_valueLayoutBottom.addWidget(self.psw_valuePreset3)
        self.psw_valuePreset3.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_valueSlider, 25))
        self.psw_valuePreset3.setObjectName("orange")
        self.psw_valuePreset3.setMinimumHeight(25)

        self.psw_valuePreset4 = QtWidgets.QPushButton("0.50")
        self.psw_valuePreset4.setMaximumSize(40, 20)
        self.psw_valuePreset4.setMinimumSize(40, 20)
        self.psw_valueLayoutBottom.addWidget(self.psw_valuePreset4)
        self.psw_valuePreset4.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_valueSlider, 50))
        self.psw_valuePreset4.setObjectName("orange")
        self.psw_valuePreset4.setMinimumHeight(25)

        self.psw_valuePreset5 = QtWidgets.QPushButton("0.75")
        self.psw_valuePreset5.setMaximumSize(40, 20)
        self.psw_valuePreset5.setMinimumSize(40, 20)
        self.psw_valueLayoutBottom.addWidget(self.psw_valuePreset5)
        self.psw_valuePreset5.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_valueSlider, 75))
        self.psw_valuePreset5.setObjectName("orange")
        self.psw_valuePreset5.setMinimumHeight(25)

        self.psw_valuePreset6 = QtWidgets.QPushButton("1.00")
        self.psw_valuePreset6.setMaximumSize(40, 20)
        self.psw_valuePreset6.setMinimumSize(40, 20)
        self.psw_valueLayoutBottom.addWidget(self.psw_valuePreset6)
        self.psw_valuePreset6.clicked.connect(partial(self.paintSkinWeights_SetSliderValues, self.psw_valueSlider, 100))
        self.psw_valuePreset6.setObjectName("orange")
        self.psw_valuePreset6.setMinimumHeight(25)

        self.psw_valueLayoutBottom.setSpacing(20)
        self.psw_valueLayoutBottom.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        # flood weights
        self.psw_floodWeightsBtn = QtWidgets.QPushButton("Flood Weights")
        self.psw_floodWeightsBtn.setFont(headerFont)
        self.psw_floodWeightsBtn.setMaximumHeight(40)
        self.psw_floodWeightsBtn.setMinimumHeight(40)
        self.psw_influenceLayout.addWidget(self.psw_floodWeightsBtn)
        self.psw_floodWeightsBtn.clicked.connect(self.paintSkinWeights_floodWeights)
        self.psw_floodWeightsBtn.setObjectName("settings")

        # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # #
        # create the groupbox for stroke               #
        # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # #
        self.psw_groupBoxStroke = QtWidgets.QGroupBox("Stroke")
        self.psw_groupBoxStroke.setObjectName("light")
        self.psw_groupBoxStroke.setMinimumSize(QtCore.QSize(470, 150))
        self.psw_groupBoxStroke.setMaximumSize(QtCore.QSize(470, 150))
        self.psw_groupBoxStroke.setFont(headerFont)
        self.psw_mainLayout.addWidget(self.psw_groupBoxStroke)
        self.psw_strokeLayout = QtWidgets.QVBoxLayout(self.psw_groupBoxStroke)

        # # # radius(U) # # #
        self.psw_radiusULayout = QtWidgets.QHBoxLayout()
        self.psw_strokeLayout.addLayout(self.psw_radiusULayout)

        radiusULabel = QtWidgets.QLabel("Radius(U): ")
        radiusULabel.setStyleSheet("background: transparent;")
        radiusULabel.setFont(headerFont)
        self.psw_radiusULayout.addWidget(radiusULabel)

        # # # radius(U) slider # # #
        self.psw_radiusUSlider = QtWidgets.QSlider()
        self.psw_radiusULayout.addWidget(self.psw_radiusUSlider)
        self.psw_radiusUSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.psw_radiusUSlider.setRange(0, 50)
        self.psw_radiusUSlider.setValue(10)
        self.psw_radiusUSlider.setSingleStep(1)
        self.psw_radiusUSlider.setPageStep(1)
        self.psw_radiusUSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.psw_radiusUSlider.setTickInterval(10)

        # # # radius(U) field # # #
        self.psw_radiusUField = QtWidgets.QDoubleSpinBox()
        self.psw_radiusULayout.addWidget(self.psw_radiusUField)
        self.psw_radiusUField.setValue(10.00)
        self.psw_radiusUField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.psw_radiusUField.setReadOnly(True)

        # # # radius(U) signals/slots # # #
        self.psw_radiusUSlider.valueChanged.connect(
            partial(self.paintSkinWeights_UpdateSliders, self.psw_radiusUSlider, self.psw_radiusUField, False))
        self.psw_radiusUSlider.valueChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "radius", "slider", self.psw_radiusUSlider))

        # # # radius(L) # # #
        self.psw_radiuslLayout = QtWidgets.QHBoxLayout()
        self.psw_strokeLayout.addLayout(self.psw_radiuslLayout)

        radiuslLabel = QtWidgets.QLabel("Radius(L): ")
        radiuslLabel.setStyleSheet("background: transparent;")
        radiuslLabel.setFont(headerFont)
        self.psw_radiuslLayout.addWidget(radiuslLabel)

        # # # radius(L) slider # # #
        self.psw_radiuslSlider = QtWidgets.QSlider()
        self.psw_radiuslLayout.addWidget(self.psw_radiuslSlider)
        self.psw_radiuslSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.psw_radiuslSlider.setRange(0, 50)
        self.psw_radiuslSlider.setValue(0)
        self.psw_radiuslSlider.setSingleStep(1)
        self.psw_radiuslSlider.setPageStep(1)
        self.psw_radiuslSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.psw_radiuslSlider.setTickInterval(10)

        # # # radius(L) field # # #
        self.psw_radiuslField = QtWidgets.QDoubleSpinBox()
        self.psw_radiuslLayout.addWidget(self.psw_radiuslField)
        self.psw_radiuslField.setValue(0.00)
        self.psw_radiuslField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.psw_radiuslField.setReadOnly(True)

        # # # radius(L) signals/slots # # #
        self.psw_radiuslSlider.valueChanged.connect(
            partial(self.paintSkinWeights_UpdateSliders, self.psw_radiuslSlider, self.psw_radiuslField, False))
        self.psw_radiuslSlider.valueChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "lowerradius", "slider", self.psw_radiuslSlider))

        # # # reflection # # #
        self.psw_reflectionTopLayout = QtWidgets.QHBoxLayout()
        self.psw_strokeLayout.addLayout(self.psw_reflectionTopLayout)

        self.psw_reflectionToggleCB = QtWidgets.QCheckBox("Reflection")
        self.psw_reflectionTopLayout.addWidget(self.psw_reflectionToggleCB)
        self.psw_reflectionToggleCB.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "reflection", None, self.psw_reflectionToggleCB))

        self.psw_reflectionBottomLayout = QtWidgets.QHBoxLayout()
        self.psw_strokeLayout.addLayout(self.psw_reflectionBottomLayout)

        reflectLabel = QtWidgets.QLabel("Reflection Axis: ")
        reflectLabel.setStyleSheet("background: transparent;")
        reflectLabel.setFont(headerFont)
        self.psw_reflectionBottomLayout.addWidget(reflectLabel)

        self.psw_reflectAxisX = QtWidgets.QCheckBox("X")
        self.psw_reflectionBottomLayout.addWidget(self.psw_reflectAxisX)
        self.psw_reflectAxisX.setAutoExclusive(True)
        self.psw_reflectAxisX.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "reflectionaxis", "\"" + "x" + "\"", self.psw_reflectAxisX))

        self.psw_reflectAxisY = QtWidgets.QCheckBox("Y")
        self.psw_reflectionBottomLayout.addWidget(self.psw_reflectAxisY)
        self.psw_reflectAxisY.setAutoExclusive(True)
        self.psw_reflectAxisY.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "reflectionaxis", "\"" + "y" + "\"", self.psw_reflectAxisY))

        self.psw_reflectAxisZ = QtWidgets.QCheckBox("Z")
        self.psw_reflectionBottomLayout.addWidget(self.psw_reflectAxisZ)
        self.psw_reflectAxisZ.setAutoExclusive(True)
        self.psw_reflectAxisZ.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "reflectionaxis", "\"" + "z" + "\"", self.psw_reflectAxisZ))

        # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # #
        # create the groupbox for stylus pressure      #
        # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # #
        self.psw_groupBoxStylus = QtWidgets.QGroupBox("Stylus Pressure")
        self.psw_groupBoxStylus.setObjectName("light")
        self.psw_groupBoxStylus.setMinimumSize(QtCore.QSize(470, 100))
        self.psw_groupBoxStylus.setMaximumSize(QtCore.QSize(470, 100))
        self.psw_groupBoxStylus.setFont(headerFont)
        self.psw_mainLayout.addWidget(self.psw_groupBoxStylus)
        self.psw_stylusLayout = QtWidgets.QVBoxLayout(self.psw_groupBoxStylus)

        self.psw_stylusPressureLayout = QtWidgets.QHBoxLayout()
        self.psw_stylusLayout.addLayout(self.psw_stylusPressureLayout)

        self.psw_stylusPressureToggle = QtWidgets.QCheckBox("Stylus Pressure")
        self.psw_stylusPressureLayout.addWidget(self.psw_stylusPressureToggle)
        self.psw_stylusPressureToggle.setChecked(True)
        self.psw_stylusPressureToggle.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "usepressure", None, self.psw_stylusPressureToggle))

        spLabel = QtWidgets.QLabel("Pressure Mapping: ")
        spLabel.setStyleSheet("background: transparent;")
        spLabel.setFont(headerFont)
        self.psw_stylusPressureLayout.addWidget(spLabel)

        self.psw_stylusPressureOptions = QtWidgets.QComboBox()
        self.psw_stylusPressureLayout.addWidget(self.psw_stylusPressureOptions)
        self.psw_stylusPressureOptions.currentIndexChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "mappressure", "mapping", self.psw_stylusPressureOptions))
        self.psw_stylusPressureOptions.addItem("Opacity")
        self.psw_stylusPressureOptions.addItem("Radius")
        self.psw_stylusPressureOptions.addItem("Both")

        # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # #
        # create the groupbox for display settings     #
        # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # #
        self.psw_groupBoxDisplay = QtWidgets.QGroupBox("Display")
        self.psw_groupBoxDisplay.setObjectName("light")
        self.psw_groupBoxDisplay.setMinimumSize(QtCore.QSize(470, 150))
        self.psw_groupBoxDisplay.setMaximumSize(QtCore.QSize(470, 150))
        self.psw_groupBoxDisplay.setFont(headerFont)
        self.psw_mainLayout.addWidget(self.psw_groupBoxDisplay)
        self.psw_displayLayout = QtWidgets.QVBoxLayout(self.psw_groupBoxDisplay)

        # # # top settings # # #
        self.psw_displaySettingsTop = QtWidgets.QHBoxLayout()
        self.psw_displayLayout.addLayout(self.psw_displaySettingsTop)

        self.psw_displayDrawBrush = QtWidgets.QCheckBox("Draw Brush")
        self.psw_displaySettingsTop.addWidget(self.psw_displayDrawBrush)
        self.psw_displayDrawBrush.setChecked(True)
        self.psw_displayDrawBrush.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "outline", None, self.psw_displayDrawBrush))

        self.psw_displayDrawBrushPaint = QtWidgets.QCheckBox("Draw Brush While Painting")
        self.psw_displaySettingsTop.addWidget(self.psw_displayDrawBrushPaint)
        self.psw_displayDrawBrushPaint.setChecked(True)
        self.psw_displayDrawBrushPaint.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "outwhilepaint", None, self.psw_displayDrawBrushPaint))

        # # # mid settings # # #
        self.psw_displaySettingsMid = QtWidgets.QHBoxLayout()
        self.psw_displayLayout.addLayout(self.psw_displaySettingsMid)

        self.psw_displayDrawBrushTangent = QtWidgets.QCheckBox("Draw Brush Tangent Outline")
        self.psw_displaySettingsMid.addWidget(self.psw_displayDrawBrushTangent)
        self.psw_displayDrawBrushTangent.setChecked(True)
        self.psw_displayDrawBrushTangent.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "tangentOutline", None, self.psw_displayDrawBrushTangent))

        self.psw_displayDrawBrushFeedback = QtWidgets.QCheckBox("Draw Brush Feedback")
        self.psw_displaySettingsMid.addWidget(self.psw_displayDrawBrushFeedback)
        self.psw_displayDrawBrushFeedback.setChecked(True)
        self.psw_displayDrawBrushFeedback.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "brushfeedback", None, self.psw_displayDrawBrushFeedback))

        # # # bottom settings # # #
        self.psw_displaySettingsBot1 = QtWidgets.QHBoxLayout()
        self.psw_displayLayout.addLayout(self.psw_displaySettingsBot1)

        self.psw_displayShowWires = QtWidgets.QCheckBox("Show Wireframe")
        self.psw_displaySettingsBot1.addWidget(self.psw_displayShowWires)
        self.psw_displayShowWires.setChecked(True)
        self.psw_displayShowWires.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "showactive", None, self.psw_displayShowWires))

        self.psw_displayColorFeedback = QtWidgets.QCheckBox("Color Feedback")
        self.psw_displaySettingsBot1.addWidget(self.psw_displayColorFeedback)
        self.psw_displayColorFeedback.setChecked(True)
        self.psw_displayColorFeedback.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "colorfeedback", None, self.psw_displayColorFeedback))

        # # # bottom settings 2 # # #
        self.psw_displaySettingsBot2 = QtWidgets.QHBoxLayout()
        self.psw_displayLayout.addLayout(self.psw_displaySettingsBot2)

        self.psw_displayXRayJoints = QtWidgets.QCheckBox("X-Ray Joints")
        self.psw_displaySettingsBot2.addWidget(self.psw_displayXRayJoints)
        self.psw_displayXRayJoints.setChecked(False)
        self.psw_displayXRayJoints.stateChanged.connect(
            partial(self.paintSkinWeights_updateCTX, "xrayJoints", None, self.psw_displayXRayJoints))

        # spacer
        self.psw_mainLayout.addSpacerItem(
            QtWidgets.QSpacerItem(500, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_scriptJob(self):
        # create selection script job for populating weight table

        jobs = cmds.scriptJob(listJobs=True)
        try:
            if self.wtScriptJob in jobs:
                cmds.scriptJob(kill=self.wtScriptJob, force=True)
        except:
            pass

        # create the script job
        self.wtScriptJob = cmds.scriptJob(event=["SelectionChanged", self.weightTable_getInfs], kws=True)
        return self.wtScriptJob

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_paintWeightsMode(self):

        # paint weights mode
        mel.eval("ArtPaintSkinWeightsTool;")

        # change current index of the stack widget
        self.defomation_mainWidget.setCurrentIndex(1)

        # kick off script job to monitor when tool changes
        self.paintWeightScriptJob = cmds.scriptJob(event=["ToolChanged", self.paintSkinWeightsScriptJob], runOnce=True,
                                                   kws=True)

        # check artAttrSkinPaintCtx settings
        currentCtx = cmds.currentCtx()

        # # # influences # # #
        skinPaintMode = cmds.artAttrSkinPaintCtx(currentCtx, q=True, skinPaintMode=True)
        paintSelectMode = cmds.artAttrSkinPaintCtx(currentCtx, q=True, paintSelectMode=True)
        selectedattroper = cmds.artAttrSkinPaintCtx(currentCtx, q=True, selectedattroper=True)
        stampProfile = cmds.artAttrSkinPaintCtx(currentCtx, q=True, stampProfile=True)
        opacity = cmds.artAttrSkinPaintCtx(currentCtx, q=True, opacity=True)
        value = cmds.artAttrSkinPaintCtx(currentCtx, q=True, value=True)

        if skinPaintMode == 0:
            self.psw_paintMode_select.setChecked(True)
        if skinPaintMode == 1:
            self.psw_paintMode_paint.setChecked(True)
        if skinPaintMode == 2:
            self.psw_paintMode_paintSelect.setChecked(True)

        if paintSelectMode == 1:
            self.psw_paintSelect_Add.setChecked(True)
        if paintSelectMode == 2:
            self.psw_paintSelect_Remove.setChecked(True)
        if paintSelectMode == 3:
            self.psw_paintSelect_Toggle.setChecked(True)

        if selectedattroper == "additive":
            self.psw_paintOperation.setCurrentIndex(0)
        if selectedattroper == "absolute":
            self.psw_paintOperation.setCurrentIndex(1)
        if selectedattroper == "scale":
            self.psw_paintOperation.setCurrentIndex(21)
        if selectedattroper == "smooth":
            self.psw_paintOperation.setCurrentIndex(3)

        if stampProfile == "gaussian":
            self.psw_paintProfile_Gaussian.setChecked(True)
            self.psw_paintProfile_Gaussian.click()
        if stampProfile == "soft":
            self.psw_paintProfile_Soft.setChecked(True)
            self.psw_paintProfile_Soft.click()
        if stampProfile == "solid":
            self.psw_paintProfile_Solid.setChecked(True)
            self.psw_paintProfile_Solid.click()
        if stampProfile == "square":
            self.psw_paintProfile_Square.setChecked(True)
            self.psw_paintProfile_Square.click()

        self.psw_opacitySlider.setValue(opacity * 100)
        self.psw_valueSlider.setValue(value * 100)

        # stroke
        radius = cmds.artAttrSkinPaintCtx(currentCtx, q=True, radius=True)
        lowerRadius = cmds.artAttrSkinPaintCtx(currentCtx, q=True, lowerradius=True)
        reflection = cmds.artAttrSkinPaintCtx(currentCtx, q=True, reflection=True)
        reflectionaxis = cmds.artAttrSkinPaintCtx(currentCtx, q=True, reflectionaxis=True)

        self.psw_radiusUSlider.setValue(int(radius))
        self.psw_radiuslSlider.setValue(lowerRadius)
        self.psw_reflectionToggleCB.setChecked(reflection)

        if reflectionaxis == "x":
            self.psw_reflectAxisX.setChecked(True)
        if reflectionaxis == "y":
            self.psw_reflectAxisY.setChecked(True)
        if reflectionaxis == "z":
            self.psw_reflectAxisZ.setChecked(True)

        # stylus pressure
        usepressure = cmds.artAttrSkinPaintCtx(currentCtx, q=True, usepressure=True)
        mappressure = cmds.artAttrSkinPaintCtx(currentCtx, q=True, mappressure=True)

        self.psw_stylusPressureToggle.setChecked(usepressure)

        if mappressure == "Opacity":
            self.psw_stylusPressureOptions.setCurrentIndex(0)
        if mappressure == "Radius":
            self.psw_stylusPressureOptions.setCurrentIndex(1)
        if mappressure == "Both":
            self.psw_stylusPressureOptions.setCurrentIndex(2)

        # display
        outline = cmds.artAttrSkinPaintCtx(currentCtx, q=True, outline=True)
        outwhilepaint = cmds.artAttrSkinPaintCtx(currentCtx, q=True, outwhilepaint=True)
        tangentOutline = cmds.artAttrSkinPaintCtx(currentCtx, q=True, tangentOutline=True)
        brushfeedback = cmds.artAttrSkinPaintCtx(currentCtx, q=True, brushfeedback=True)
        showactive = cmds.artAttrSkinPaintCtx(currentCtx, q=True, showactive=True)
        colorfeedback = cmds.artAttrSkinPaintCtx(currentCtx, q=True, colorfeedback=True)
        xrayJoints = cmds.artAttrSkinPaintCtx(currentCtx, q=True, xrayJoints=True)

        self.psw_displayDrawBrush.setChecked(outline)
        self.psw_displayDrawBrushPaint.setChecked(outwhilepaint)
        self.psw_displayDrawBrushTangent.setChecked(tangentOutline)
        self.psw_displayDrawBrushFeedback.setChecked(brushfeedback)
        self.psw_displayShowWires.setChecked(showactive)
        self.psw_displayColorFeedback.setChecked(colorfeedback)
        self.psw_displayXRayJoints.setChecked(xrayJoints)

        # populate influence lists
        self.paintSkinWeights_populateModules()
        self.paintSkinWeights_populateInfs()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeightsScriptJob(self):

        # check current context
        currentTool = cmds.currentCtx()

        # if current context is not artAttrSkinCtx, setCurrentIndex back to 0
        if currentTool != "artAttrSkinContext":
            self.defomation_mainWidget.setCurrentIndex(0)

            currentSelection = cmds.ls(sl=True)
            cmds.select(clear=True)
            cmds.select(currentSelection)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_populateModules(self):

        # clear list
        self.psw_moduleInfluenceList.clear()

        # add modules to list
        modules = utils.returnRigModules()
        for module in modules:
            name = cmds.getAttr(module + ".moduleName")
            self.psw_moduleInfluenceList.addItem(name)

        # select all modules, populating the entire influence list
        self.psw_moduleInfluenceList.selectAll()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_populateInfs(self):

        # find the selected mesh
        selection = cmds.ls(sl=True)

        # clear influences in list
        influences = []
        self.psw_influenceList.clear()

        # check if valid selection
        if len(selection) >= 1:
            mesh = selection[0]
            if cmds.nodeType(mesh) == "transform":

                # check for skinCluster
                skinClusters = cmds.ls(type='skinCluster')

                # go through each found skin cluster, and if we find a skin cluster whose geometry matches our selection
                # get influences
                for cluster in skinClusters:
                    geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
                    geoTransform = cmds.listRelatives(geometry, parent=True)[0]
                    if geoTransform == mesh:
                        skinCluster = cluster
                        influences = cmds.skinCluster(cluster, q=True, inf=True)

        # compare influences in list to selected modules
        createdJoints = []
        modules = utils.returnRigModules()
        selectedModules = self.psw_moduleInfluenceList.selectedItems()

        for each in selectedModules:
            selectedText = each.text()
            for module in modules:
                modName = cmds.getAttr(module + ".moduleName")
                if modName == selectedText:
                    # get joints of that module
                    createdBones = cmds.getAttr(module + ".Created_Bones")
                    splitJoints = createdBones.split("::")

                    for bone in splitJoints:
                        if bone != "":
                            createdJoints.append(bone)

        # add the influneces to the list
        if len(influences) > 0:
            for inf in influences:
                if inf in createdJoints:
                    lockColor = QtGui.QColor(0, 0, 0)
                    lockBkgrd = QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.Dense2Pattern)
                    lockFont = QtGui.QFont()
                    lockFont.setPointSize(8)
                    lockFont.setBold(True)

                    item = QtWidgets.QListWidgetItem(inf)
                    locked = cmds.skinCluster(self.skinCluster, q=True, inf=inf, lw=True)
                    if locked:
                        item.setFont(lockFont)
                        item.setForeground(lockColor)
                        item.setBackground(lockBkgrd)
                    self.psw_influenceList.addItem(item)

            # auto select the first item in the list
            self.psw_influenceList.setCurrentRow(0)
            self.paintSkinWeights_changeInf()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_changeInf(self):
        try:
            selected = self.psw_influenceList.selectedItems()
            selected = selected[0].text()
            currentCtx = cmds.currentCtx()
            cmds.artAttrSkinPaintCtx(currentCtx, edit=True, influence=selected)

            # loop through all of the influences in the list and set the tool to not have them selected
            for i in range(self.psw_influenceList.count()):
                item = self.psw_influenceList.item(i)
                influence = item.text()
                string = "artSkinInflListChanging " + "\"" + influence + "\"" + " 0;"
                mel.eval(string)
                string = "artSkinInflListChanged artAttrSkinPaintCtx;"
                mel.eval(string)

            # turn on the selected influence
            string = "artSkinInflListChanging " + "\"" + selected + "\"" + " 1;"
            mel.eval(string)
            string = "artSkinInflListChanged artAttrSkinPaintCtx;"
            mel.eval(string)
        except:
            pass

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_mirrorSkinWeights(self):

        # get the current selection
        selection = cmds.ls(sl=True, flatten=True)

        # if the whole object is selected, use Maya's mirroring
        if selection[0].find(".vtx") == -1:
            mel.eval("MirrorSkinWeightsOptions;")

        # if holding shift, use Maya's mirroring:
        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            mel.eval("MirrorSkinWeightsOptions;")

        # otherwise, use custom mirroring
        else:
            # get selection and determine if selection is an object or component selection
            selectionType = None

            if len(selection) > 0:
                if selection[0].find(".vtx") != -1:
                    selectionType = "vertex"
                    selectedVerts = selection
                    # find the object name
                    objectName = selection[0].partition(".vtx")[0]

                else:
                    cmds.warning("No vertices selected.")
                    return

            # find total number of vertices in object
            totalNumVerts = cmds.polyEvaluate(objectName, v=True)
            cmds.select(objectName + ".vtx[*]")
            allVerts = cmds.ls(sl=True, flatten=True)
            mirrorVertices = []

            # find all joints in the object's skinCluster
            skinClusters = cmds.ls(type='skinCluster')

            # go through each found skin cluster, and if we find a skin cluster whose geometry matches our selection, get influences
            for cluster in skinClusters:
                geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
                geoTransform = cmds.listRelatives(geometry, parent=True)[0]
                if geoTransform == objectName:
                    skinCluster = cluster
                    influences = cmds.skinCluster(cluster, q=True, inf=True)

            # create the master list that will hold the vertex, its mirror, the influences of the vertex, the influences of the mirror, and the values
            masterInfDataList = []
            mirrorVertex = None

            for vert in selectedVerts:
                pos = cmds.pointPosition(vert)
                mirrorVertPosition = [pos[0] * -1, pos[1], pos[2]]
                mirrorVertPosX = mirrorVertPosition[0] * 1000
                mirrorVertPosX = math.floor(mirrorVertPosX)

                for i in range(totalNumVerts):
                    testPos = cmds.pointPosition(allVerts[i])
                    if testPos == mirrorVertPosition:
                        mirrorVertex = allVerts[i]
                        mirrorVertices.append(mirrorVertex)

                # get this vert's influence information
                vertexInfs = cmds.skinPercent(skinCluster, vert, q=True, ignoreBelow=0.0001, transform=None)
                infValues = cmds.skinPercent(skinCluster, vert, q=True, ignoreBelow=0.0001, value=True)

                # get the world position of the vertexInfs
                mirrorInfs = []
                for inf in vertexInfs:
                    worldPos = cmds.xform(inf, q=True, ws=True, t=True)

                    # try to get the mirror influence
                    mirrorPos = [round(worldPos[0] * -1, 2), round(worldPos[1], 2), round(worldPos[2], 2)]

                    for each in influences:
                        infPos = cmds.xform(each, q=True, ws=True, t=True)
                        newPos = [round(infPos[0], 2), round(infPos[1], 2), round(infPos[2], 2)]
                        if newPos == mirrorPos:
                            mirrorInfs.append(each)

                # now we have all of the data needed to perform the mirror
                data = [vert, mirrorVertex, vertexInfs, mirrorInfs, infValues]

                # perform mirror
                vert = data[1]
                infs = data[3]
                vals = data[4]

                # transformValueList
                if vert != None:
                    if len(data[2]) == len(data[3]):
                        cmds.skinPercent(skinCluster, vert, transformValue=[infs[0], 1.0])

                        transformValueList = []
                        for i in range(len(infs)):
                            transformValueList.append((str(infs[i]), float(vals[i])))

                        cmds.skinPercent(skinCluster, vert, transformValue=transformValueList)

                    else:
                        cmds.warning("skipping " + str(data[1]) + ". Missing symmetrical influence.")

            if len(mirrorVertices) > 0:
                cmds.select(mirrorVertices)
            else:
                cmds.select(selection)

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_copySkinWeights(self):

        selection = cmds.ls(sl=True)

        if len(selection) > 1:
            fromObj = selection[0]

            fromSkinCluster = riggingUtils.findRelatedSkinCluster(fromObj)
            fromJoints = cmds.skinCluster(fromSkinCluster, q=True, inf=True)

            cmds.select(selection[1])
            cmds.select(fromJoints, tgl=True)

            mel.eval("doEnableNodeItems false all;")
            cmds.dagPose(r=True, g=True, bp=True)

            newSkinCluster = cmds.skinCluster(tsb=True, mi=0, dr=4, sm=0)[0]
            cmds.copySkinWeights(ss=fromSkinCluster, ds=newSkinCluster, noMirror=True)
            mel.eval("doEnableNodeItems true all;")
        else:
            cmds.warning("Please select a source and target mesh.")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_hammerSkinWeights(self):

        try:
            mel.eval("weightHammerVerts;")

        except:
            cmds.confirmDialog(icon="warning", title="Hammer Skin Weights",
                               message="The weight hammer works on polygon vertices.  Please select at least 1 vertex.")


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_growOrShrink(self, mode):

        # validate selection
        valid = False
        selection = cmds.ls(sl=True, flatten=True)
        for each in selection:
            if each.find("vtx") != -1:
                valid = True

        if valid:
            cmds.polySelectConstraint(t=0x0001, pp=mode)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_loopOrRing(self, mode):

        # check length of selection
        valid = False
        selection = cmds.ls(sl=True, flatten=True)
        for each in selection:
            if each.find("vtx") != -1:
                valid = True

        # check length of selection
        if valid:
            if len(selection) >= 2:
                # convert the selection to edges
                edges = cmds.polyListComponentConversion(fv=True, te=True, internal=True)
                cmds.select(edges)

                # get the edge loop or ring
                if mode == "loop":
                    cmds.polySelectSp(loop=True)
                if mode == "ring":
                    cmds.polySelectSp(ring=True)

                # set back to verts
                verts = cmds.polyListComponentConversion(fe=True, tv=True)
                cmds.select(verts)
            else:
                cmds.warning("Please select at least two vertices.")


            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_shell(self):

        # validate selection
        valid = False
        selection = cmds.ls(sl=True, flatten=True)
        for each in selection:
            if each.find("vtx") != -1:
                valid = True
        if valid:
            cmds.ConvertSelectionToShell()


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_isolate(self):

        # get button state
        state = self.isolateSelection.isChecked()

        # validate selection
        valid = False
        selection = cmds.ls(sl=True, flatten=True)
        for each in selection:
            if each.find("vtx") != -1:
                valid = True

        if valid:
            if state:
                # convert selection to faces, grab shell, then back to verts
                cmds.select(cmds.polyListComponentConversion(tf=True))
                cmds.ConvertSelectionToShell()

                # isolate selection
                isoPnl = cmds.getPanel(wf=True)
                isoCrnt = cmds.isolateSelect(isoPnl, q=True, s=True)
                mel.eval('enableIsolateSelect %s %d' % (isoPnl, not isoCrnt))

                # convert back to verts
                cmds.select(cmds.polyListComponentConversion(tv=True))

                # change the button text to exit isolation mode
                self.isolateSelection.setText("Exit Isolation Mode")

            if not state:
                isoPnl = cmds.getPanel(wf=True)
                isoCrnt = cmds.isolateSelect(isoPnl, q=True, s=True)
                mel.eval('enableIsolateSelect %s %d' % (isoPnl, not isoCrnt))

                # change the button text to exit isolation mode
                self.isolateSelection.setText("Isolate Selection")


            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_addWeight(self, amount):

        # if no amount passed in, get amount from setWeight spin box
        if amount == None:
            amount = self.customWeightField.value()

        # get the selected transform from either list
        selectedTransformData = self.weightTable_getSelectedTransform()
        selectedTransform = selectedTransformData[0]
        lockInfs = selectedTransformData[1]
        length = selectedTransformData[2]

        # get skin cluster for selected verts
        cluster = self.weightTable_getSkinForSelected(selectedTransform, lockInfs)

        # skin the selected verts to the selected trasnform with the incoming amount
        canProceed = self.weightTable_checkIfLocked()
        if canProceed:
            if selectedTransform != None:
                if length > 2:
                    cmds.undoInfo(openChunk=True)
                    cmds.skinPercent(cluster, transformValue=[selectedTransform, amount])
                    cmds.undoInfo(closeChunk=True)
            if selectedTransform != None:
                if length == 2:
                    if len(self.weightTable_skinJoints.selectedItems()) > 0:
                        cmds.undoInfo(openChunk=True)
                        cmds.skinPercent(cluster, transformValue=[selectedTransform, amount])
                        cmds.undoInfo(closeChunk=True)

            if selectedTransform == None:
                cmds.warning("No influence selected in list to add weight to.")

        if lockInfs:
            self.weightTable_lockInfs(selectedTransform, lockInfs, cluster, False)

        # refresh UI
        self.weightTable_getInfs()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_getSelectedTransform(self):

        # get the selected transform from either list
        selectedTransform = None
        lockInfs = False
        length = self.weightTableVertList.count()

        if len(self.weightTable_skinJoints.selectedItems()) > 0:
            selectedTransformItem = self.weightTable_skinJoints.selectedItems()
            selectedTransform = selectedTransformItem[0].text()

        if len(self.weightTableVertList.selectedItems()) > 0:
            selectedTransformItem = self.weightTableVertList.selectedItems()
            selectedTransform = selectedTransformItem[0].text()
            lockInfs = True

        return [selectedTransform, lockInfs, length]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_getSkinForSelected(self, selectedTransform, lockInfs):
        # if vertices are selected, get that selection
        if self.weightTableVertList.count() > 0:

            selection = cmds.ls(sl=True, fl=True)
            # find the shape node associated with the seleted vertices
            shape = cmds.listRelatives(selection, parent=True)[0]
            # find the transform of the shape
            transform = cmds.listRelatives(shape, parent=True)[0]
            # find the skin cluster associated with the shape node
            connnections = cmds.listConnections(shape, connections=True)
            cluster = None
            for c in connnections:
                if cmds.nodeType(c) == "skinCluster":
                    cluster = c
                    if selectedTransform is not None:
                        # now if lockInfs is True, lock all influences not in the weightTableVertList
                        if lockInfs:
                            self.weightTable_lockInfs(selectedTransform, lockInfs, c, True)
                        break
                if cmds.nodeType(c) == "objectSet":
                    set_connections = cmds.listConnections(c, connections=True)
                    for conn in set_connections:
                        if cmds.nodeType(conn) == "skinCluster":
                            cluster = conn
                            if selectedTransform is not None:
                                if lockInfs:
                                    self.weightTable_lockInfs(selectedTransform, lockInfs, c, True)
                            break
            return cluster

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_checkIfLocked(self):

        numLocked = []
        for i in range(self.weightTableVertList.count()):
            item = self.weightTableVertList.item(i)
            jointName = item.text()

            # check to see if the joint is locked
            if cmds.objExists(jointName):
                locked = cmds.skinCluster(self.skinCluster, q=True, inf=jointName, lw=True)
                if locked:
                    numLocked.append(jointName)

        if len(numLocked) < (self.weightTableVertList.count() - 1):
            return True
        else:
            return False


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_lockInfs(self, selectedTransform, lockInfs, cluster, lock):
        # get all of the influences
        allInfs = []
        previouslyLocked = []
        allInfItems = self.weightTable_skinJoints.count()
        for i in range(allInfItems):
            allInfs.append(self.weightTable_skinJoints.item(i).text())

        # get the influences in the weightTableVertList
        doNotLock = []
        vertsInfs = self.weightTableVertList.count()
        for i in range(vertsInfs):
            jointName = self.weightTableVertList.item(i).text()
            if cmds.objExists(jointName):
                locked = cmds.skinCluster(cluster, q=True, inf=jointName, lw=True)
                if not locked:
                    doNotLock.append(self.weightTableVertList.item(i).text())
                if locked:
                    previouslyLocked.append(self.weightTableVertList.item(i).text())

        # lock infs not in doNotLock list
        if lock:
            for inf in allInfs:
                if inf not in doNotLock:
                    cmds.skinCluster(cluster, edit=True, inf=inf, lockWeights=True)

        if lock == False:
            # unlock infs not in doNotLock list
            for inf in allInfs:
                if inf not in doNotLock:
                    cmds.skinCluster(cluster, edit=True, inf=inf, lockWeights=False)
            for inf in previouslyLocked:
                cmds.skinCluster(cluster, edit=True, inf=inf, lockWeights=True)


            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_getInfs(self):

        currentSelection = None
        listWidget = None
        # get current selection in lists
        if len(self.weightTable_skinJoints.selectedItems()) > 0:
            currentSelection = self.weightTable_skinJoints.selectedItems()[0].text()
            listWidget = self.weightTable_skinJoints

        if len(self.weightTableVertList.selectedItems()) > 0:
            currentSelection = self.weightTableVertList.selectedItems()[0].text()
            listWidget = self.weightTableVertList

        # clear the influence list
        self.weightTable_skinJoints.clear()
        self.weightTableVertList.clear()
        self.weightTableInfList.clear()

        # find the selected mesh
        selection = cmds.ls(sl=True)
        if len(selection) >= 1:
            mesh = selection[0]

            if cmds.nodeType(mesh) == "transform":
                self.weightTable_populateSkinJoints(mesh)
            if cmds.nodeType(mesh) == "mesh":
                shapeNode = cmds.listRelatives(mesh, parent=True)
                if shapeNode != None:
                    transformNode = cmds.listRelatives(shapeNode[0], parent=True)
                    if transformNode != None:
                        cluster = self.weightTable_populateSkinJoints(transformNode[0])

                        # vertex influence list
                        self.weightTable_populateVertexJoints(selection, cluster)

        # reselect
        if currentSelection != None:
            items = listWidget.findItems(currentSelection, QtCore.Qt.MatchExactly)
            if len(items) == 1:
                row = listWidget.row(items[0])
                listWidget.setCurrentRow(row)

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_populateSkinJoints(self, mesh):

        # check for skinCluster
        skinClusters = cmds.ls(type='skinCluster')
        self.influences = []

        # go through each found skin cluster, and if we find a skin cluster whose geometry matches our selection, get influences
        for cluster in skinClusters:
            geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
            geoTransform = cmds.listRelatives(geometry, parent=True)[0]
            if geoTransform == mesh:
                self.skinCluster = cluster
                self.influences = cmds.skinCluster(cluster, q=True, inf=True)

        # add the influneces to the list
        if len(self.influences) > 0:
            for inf in self.influences:
                self.weightTable_skinJoints.addItem(inf)

        # return info
        if self.skinCluster != None:
            return self.skinCluster


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_populateVertexJoints(self, vertices, cluster):

        # find all of the influences of the selected vertices
        influenceJoints = []
        for vertex in vertices:
            infs = cmds.skinPercent(cluster, vertex, q=True, transform=None, ib=.001)
            for inf in infs:
                influenceJoints.append(inf)

        # remove duplicates from the influence joints list
        vertInfluences = []
        vertInfluences = list(set(influenceJoints))

        # re-create the headers
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        customColor = QtGui.QColor(25, 175, 255)
        labelItem = QtWidgets.QListWidgetItem("Joint")
        labelItem.setFont(headerFont)
        labelItem.setFlags(QtCore.Qt.NoItemFlags)
        labelItem.setForeground(customColor)
        labelItem.setBackground(QtCore.Qt.black)
        labelItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.weightTableVertList.addItem(labelItem)

        # add these to the weightTableVertList
        lockColor = QtGui.QColor(255, 0, 0)
        lockFont = QtGui.QFont()
        lockFont.setPointSize(8)
        lockFont.setBold(True)

        for each in vertInfluences:

            item = QtWidgets.QListWidgetItem(each)
            locked = cmds.skinCluster(cluster, q=True, inf=each, lw=True)
            if locked:
                item.setFont(lockFont)
                item.setForeground(lockColor)

            self.weightTableVertList.addItem(item)

        # find average weights
        self.weightTable_populateAvgWeight(vertices, cluster, vertInfluences)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_populateAvgWeight(self, vertices, cluster, influences):

        # find the infleunce values for each vertex
        averages = []
        for influence in influences:
            data = []
            for vert in vertices:
                value = cmds.skinPercent(cluster, vert, q=True, transform=influence)
                data.append(value)
            avg = sum(data) / float(len(data))
            averages.append(avg)

        # recreate the header
        customColor = QtGui.QColor(25, 175, 255)
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        labelValue = QtWidgets.QListWidgetItem("Avg. Weight")
        labelValue.setFont(headerFont)
        labelValue.setFlags(QtCore.Qt.NoItemFlags)
        labelValue.setForeground(customColor)
        labelValue.setBackground(QtCore.Qt.black)
        labelValue.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.weightTableInfList.addItem(labelValue)

        # add averages
        for each in averages:
            entry = '{0:.10f}'.format(each)
            self.weightTableInfList.addItem(str(entry))


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_inrementWeight(self, direction):

        # get the amount from setWeight
        amount = self.customWeightField.value()

        # get the selected transform from either list
        selectedTransformData = self.weightTable_getSelectedTransform()
        selectedTransform = selectedTransformData[0]
        lockInfs = selectedTransformData[1]
        length = selectedTransformData[2]

        # get skin cluster for selected verts
        cluster = self.weightTable_getSkinForSelected(selectedTransform, lockInfs)

        if cluster is not None:
            # skin the selected verts to the selected trasnform with the incoming amount
            if length > 1:
                if selectedTransform != None:
                    if direction == "up":
                        cmds.undoInfo(openChunk=True)
                        cmds.skinPercent(cluster, relative=True, transformValue=[selectedTransform, amount])
                        cmds.undoInfo(closeChunk=True)

                    if direction == "down":
                        cmds.undoInfo(openChunk=True)
                        cmds.skinPercent(cluster, relative=True, transformValue=[selectedTransform, (amount * -1)])
                        cmds.undoInfo(closeChunk=True)

            if lockInfs:
                self.weightTable_lockInfs(selectedTransform, lockInfs, cluster, False)

        # refresh UI
        self.weightTable_getInfs()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_scaleWeight(self, direction):

        # if no amount passed in, get amount from setWeight spin box
        amount = self.scaleCustomWeightField.value()

        # get the selected transform from either list
        selectedTransformData = self.weightTable_getSelectedTransform()
        selectedTransform = selectedTransformData[0]
        lockInfs = selectedTransformData[1]
        length = selectedTransformData[2]

        # get skin cluster for selected verts
        cluster = self.weightTable_getSkinForSelected(selectedTransform, lockInfs)

        # skin the selected verts to the selected trasnform with the incoming amount
        selection = cmds.ls(sl=True, fl=True)
        for each in selection:
            currentValue = cmds.skinPercent(cluster, each, transform=selectedTransform, q=True)
            if length > 2:
                if selectedTransform != None:
                    if direction == None:
                        cmds.undoInfo(openChunk=True)
                        cmds.skinPercent(cluster, transformValue=[selectedTransform, (currentValue * amount)])
                        cmds.undoInfo(closeChunk=True)

                    if direction == "up":
                        cmds.undoInfo(openChunk=True)
                        cmds.skinPercent(cluster, transformValue=[selectedTransform,
                                                                  (((currentValue * 5) / 100) + currentValue)])
                        cmds.undoInfo(closeChunk=True)

                    if direction == "down":
                        cmds.undoInfo(openChunk=True)
                        cmds.skinPercent(cluster, transformValue=[selectedTransform,
                                                                  (currentValue - ((currentValue * 5) / 100))])
                        cmds.undoInfo(closeChunk=True)

        if lockInfs:
            self.weightTable_lockInfs(selectedTransform, lockInfs, cluster, False)

        # refresh UI
        self.weightTable_getInfs()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_copyWeight(self):

        self.weightCopy_infList = []
        self.weightCopy_valList = []

        selection = cmds.ls(sl=True, flatten=True)
        if len(selection) > 1:
            cmds.warning("Please select only 1 vertex.")
            return

        else:
            if selection[0].find(".vtx") != -1:
                # get weight values
                self.weightCopy_infList = cmds.skinPercent(self.skinCluster, selection[0], q=True, transform=None,
                                                           ib=.001)
                self.weightCopy_valList = cmds.skinPercent(self.skinCluster, selection[0], q=True, value=True, ib=.001)

                # update line edit
                self.vertexBufferLayout.setText(selection[0] + " copied to buffer")


            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_pasteWeight(self):

        proceed = False

        # get selected vertices and determine if selection is valid
        selection = cmds.ls(sl=True, flatten=True)
        for each in selection:
            if each.find(".vtx") != -1:
                proceed = True

        # if selection is valid, paste the weights from the buffer
        if proceed:
            for each in selection:
                transformPairs = []
                try:
                    if len(self.weightCopy_infList) > 0:
                        for i in range(len(self.weightCopy_infList)):
                            transformPairs.append((self.weightCopy_infList[i], self.weightCopy_valList[i]))

                    cmds.undoInfo(openChunk=True)
                    cmds.skinPercent(self.skinCluster, each, transformValue=transformPairs)
                    cmds.undoInfo(closeChunk=True)

                except:
                    pass

            self.weightTable_getInfs()


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_blendWeight(self):

        proceed = False

        # get selected vertices and determine if selection is valid
        selection = cmds.ls(sl=True, flatten=True)
        for each in selection:
            if each.find(".vtx") != -1:
                proceed = True

        # if selection is valid, grow the selection
        cmds.polySelectConstraint(t=0x0001, pp=1)
        cmds.polySelectConstraint(t=0x0001, pp=1)
        newSelection = cmds.ls(sl=True, flatten=True)

        # filter out original selection from new selection
        for vert in newSelection:
            if vert in selection:
                cmds.select(vert, tgl=True)

        vertsToBlend = cmds.ls(sl=True, flatten=True)

        # weight hammer
        mel.eval("weightHammerVerts;")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_connectInfluenceLists(self, topLevel, vertLevel, *args):

        # connect the skin joints list the the vertex skin info joint list so that only 1 item can be selected in either list at a time
        if topLevel:
            if len(self.weightTableVertList.selectedItems()) > 0:
                self.weightTableVertList.clearSelection()
        if vertLevel:
            if len(self.weightTable_skinJoints.selectedItems()) > 0:
                self.weightTable_skinJoints.clearSelection()


            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_showInfluencedVerts(self, inSelection):

        # store current selection
        currentSelection = cmds.ls(sl=True, fl=True)

        # get selected joint in influence list
        selected = self.weightTable_skinJoints.selectedItems()
        if len(selected) > 1:
            cmds.warning("Please select only 1 joint in the list.")
        if len(selected) == 1:
            joint = selected[0].text()
            cmds.selectMode(component=True)
            cmds.skinCluster(self.skinCluster, edit=True, siv=joint)
            newSelection = cmds.ls(sl=True, fl=True)

            # if the new selection is nothing new, select the original selection and put the mesh in the correct selectMode
            if len(newSelection) == 1:
                if cmds.nodeType(newSelection[0]) == "mesh":
                    if len(currentSelection) == 1:
                        cmds.selectMode(object=True)
                    cmds.select(currentSelection)
                    cmds.warning("No influenced vertices for that joint.")

            # if inSelection arg is True, compare the original selection to the new selection
            if inSelection:
                selectSet = []
                for each in newSelection:
                    if each in currentSelection:
                        selectSet.append(each)

                # select new selectSet
                cmds.select(selectSet)

            # refresh UI
            self.weightTable_getInfs()


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def weightTable_focusInfluencedVerts(self):

        # store current selection
        currentSelection = cmds.ls(sl=True, fl=True)

        # get selected joint in influence list
        selected = self.psw_influenceList.selectedItems()
        if len(selected) > 1:
            cmds.warning("Please select only 1 joint in the list.")
        if len(selected) == 1:
            joint = selected[0].text()
            cmds.selectMode(component=True)
            cmds.skinCluster(self.skinCluster, edit=True, siv=joint)

        # fit and view
        utils.fitSelection()

        # select original selection
        cmds.select(currentSelection)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_focusInfluencedJoint(self):

        # store current selection
        currentSelection = cmds.ls(sl=True, fl=True)

        # get selected joint in influence list
        selected = self.psw_influenceList.selectedItems()
        if len(selected) > 1:
            cmds.warning("Please select only 1 joint in the list.")
        if len(selected) == 1:
            joint = selected[0].text()
            cmds.select(joint)

        # fit and view
        utils.fitSelection()

        # select original selection
        cmds.select(currentSelection)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def weightTable_toggleJointSelectMode(self):

        selectable = self.weightTableJointSel.isChecked()

        if selectable:
            cmds.selectType(joint=False)
        else:
            cmds.selectType(joint=True)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def createContextMenuWeightTable(self, point):

        contextMenu = QtWidgets.QMenu()
        contextMenu.addAction("Unlock Joint", self.contextMenu_unlockJoint)
        contextMenu.addAction("Lock Joint", self.contextMenu_lockJoint)
        contextMenu.exec_(self.weightTableVertList.mapToGlobal(point))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenu_unlockJoint(self):

        try:
            selected = self.weightTableVertList.selectedItems()
            selected = selected[0].text()
            cmds.skinCluster(self.skinCluster, edit=True, inf=selected, lw=False)
            self.weightTable_getInfs()
        except:
            pass

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def contextMenu_lockJoint(self):

        try:
            selected = self.weightTableVertList.selectedItems()
            selected = selected[0].text()
            cmds.skinCluster(self.skinCluster, edit=True, inf=selected, lw=True)
            self.weightTable_getInfs()
        except:
            pass



        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_searchModules(self):
        searchKey = self.psw_modSearchBar.text()
        searchKeys = []

        if searchKey.find(",") != -1:
            searchKeys = searchKey.split(",")
        else:
            searchKeys.append(searchKey)

        # get all items in the joint list
        allItems = []
        for i in range(self.psw_moduleInfluenceList.count()):
            item = self.psw_moduleInfluenceList.item(i)
            itemName = item.text()
            allItems.append([item, itemName])

        # hide all items in list
        for item in allItems:
            item[0].setHidden(True)
            item[0].setSelected(False)

        # find items in list with search key and show item
        if searchKey.find("*") == 0:
            matchedItems = self.psw_moduleInfluenceList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchWildcard)
            for item in matchedItems:
                item.setHidden(False)
                item.setSelected(True)

        else:
            matchedItems = []
            for searchKey in searchKeys:
                matchedItems.extend(
                    self.psw_moduleInfluenceList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchContains))

            for item in matchedItems:
                item.setHidden(False)
                item.setSelected(True)

        # populate infs
        self.paintSkinWeights_populateInfs()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_searchInfluences(self):

        searchKey = self.psw_infSearchBar.text()
        # get all items in the joint list
        allItems = []
        for i in range(self.psw_influenceList.count()):
            item = self.psw_influenceList.item(i)
            itemName = item.text()
            allItems.append([item, itemName])

        # hide all items in list
        for item in allItems:
            item[0].setHidden(True)
            item[0].setSelected(False)

        # find items in list with search key and show item
        if searchKey.find("*") == 0:
            matchedItems = self.psw_influenceList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchWildcard)
            for item in matchedItems:
                item.setHidden(False)
                item.setSelected(True)

        else:
            matchedItems = self.psw_influenceList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchContains)
            for item in matchedItems:
                item.setHidden(False)
                item.setSelected(True)
                print "selecting" + str(item.text())
                self.paintSkinWeights_changeInf()

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_createContextMenu(self, point):

        contextMenu = QtWidgets.QMenu()
        contextMenu.addAction("Unlock Selected Joint", partial(self.paintSkinWeights_lockJoint, False, True))
        contextMenu.addAction("Unlock Unselected Joints", partial(self.paintSkinWeights_lockJoint, False, False))
        contextMenu.addAction("Lock Selected Joint", partial(self.paintSkinWeights_lockJoint, True, True))
        contextMenu.addAction("Lock Unselected Joints", partial(self.paintSkinWeights_lockJoint, True, False))

        contextMenu.addAction("Focus Vertices Influenced by Joint", self.weightTable_focusInfluencedVerts)
        contextMenu.addAction("Focus Selected Joint", self.weightTable_focusInfluencedJoint)

        contextMenu.exec_(self.psw_influenceList.mapToGlobal(point))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_lockJoint(self, lock, selected):

        try:
            selectedItem = self.psw_influenceList.selectedItems()
            selectedItem = selectedItem[0].text()

            if selected:
                cmds.skinCluster(self.skinCluster, edit=True, inf=selectedItem, lw=lock)

            if not selected:
                for i in range(self.psw_influenceList.count()):
                    item = self.psw_influenceList.item(i).text()
                    if item != selectedItem:
                        cmds.skinCluster(self.skinCluster, edit=True, inf=item, lw=lock)

            self.paintSkinWeights_populateInfs()
        except:
            pass

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_updateCTX(self, attribute, value, widget, *args):

        # special cases
        if value == None:
            value = str(widget.isChecked())

        if value == "mapping":
            index = self.psw_stylusPressureOptions.currentIndex()
            if index == 0:
                value = str("\"" + "Opacity" + "\"")
            if index == 1:
                value = str("\"" + "Radius" + "\"")
            if index == 2:
                value = str("\"" + "Both" + "\"")

        if value == "paintOp":
            index = self.psw_paintOperation.currentIndex()
            if index == 0:
                value = str("\"" + "additive" + "\"")
            if index == 1:
                value = str("\"" + "absolute" + "\"")
            if index == 2:
                value = str("\"" + "scale" + "\"")
            if index == 3:
                value = str("\"" + "smooth" + "\"")

        if value == "slider":
            value = str(widget.value())

        if value == "sliderEdit":
            value = str(float(widget.value()) / 100)
        currentCtx = cmds.currentCtx()
        execString = "cmds.artAttrSkinPaintCtx(" + "\"" + currentCtx + "\"" + ", edit = True, " + attribute + " = " + value + ")"
        try:
            exec execString
        except Exception as e:
            print e

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_togglePaintProfile(self, button, img):

        for each in self.paintProfileButtons:
            widget = each[0]
            image = each[1]

            icon = QtGui.QIcon(image)
            widget.setIcon(icon)

        state = button.isChecked()

        if state:
            icon = QtGui.QIcon(image)
            widget.setIcon(icon)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_UpdateSliders(self, getValueFrom, putValueOn, doMath, *args):

        # if getting the value from the slider, divide by 100 when setting doubleSpinBox
        value = getValueFrom.value()

        if doMath:
            if value > 1:
                value = float(value) / 100
                putValueOn.setValue(value)
            if value == 0:
                putValueOn.setValue(float(0.00))

        if not doMath:
            putValueOn.setValue(value)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def paintSkinWeights_SetSliderValues(self, slider, value, *args):

        slider.setValue(value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_floodWeights(self):

        value = self.psw_valueSlider.value()
        value = value / 100

        currentCtx = cmds.currentCtx()
        currentMode = cmds.artAttrSkinPaintCtx(currentCtx, q=True, sao=True)
        if currentMode == "additive":
            cmds.artAttrSkinPaintCtx(currentCtx, edit=True, clear=True)
        else:
            cmds.artAttrSkinPaintCtx(currentCtx, edit=True, clear=value)

    ###############################################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # EXTERNAL FILES CALLED
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ###############################################################################################################

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def overrideJointNames_UI(self):

        import Tools.Rigging.ART_OverrideJointNames as ojn
        ojn.run()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_deformationWizardLaunch(self):

        import Tools.Rigging.ART_WeightWizard as aww
        aww.run(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_smoothSkinUI(self):

        import Tools.Rigging.ART_WeightWizard as aww
        aww.runOnlySkinTools(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_importSkinWeights(self):

        from Tools.Rigging import ART_ImportWeights
        ART_ImportWeights.ART_ImportSkinWeights(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paintSkinWeights_exportSkinWeights(self):

        from Tools.Rigging import ART_ExportWeights
        ART_ExportWeights.ART_ExportSkinWeights(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addOrRemoveInfs_UI(self):

        from Tools.Rigging import ART_AddOrRemoveInfluences
        ART_AddOrRemoveInfluences.ART_AddOrRemoveInfluences(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def moveInfluences_UI(self):

        from Tools.Rigging import ART_MoveInfluences
        ART_MoveInfluences.ART_MoveInfluences(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def debugRigs(self):
        # Original Author: Jeremy Ernst

        # run publish process
        from Tools.Rigging import ART_DebugRigs
        ART_DebugRigs.ART_DebugRigs(self.mainUI)
