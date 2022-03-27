"""
Author: Jeremy Ernst

========
Contents
========

|   **Must Have Methods:**
|       :py:func:`addAttributes <RigModules.ART_Chain.ART_Chain.addAttributes>`
|       :py:func:`skeletonSettings_UI <RigModules.ART_Chain.ART_Chain.skeletonSettings_UI>`
|       :py:func:`addJointMoverToOutliner <RigModules.ART_Chain.ART_Chain.addJointMoverToOutliner>`
|       :py:func:`applyModuleChanges <RigModules.ART_Chain.ART_Chain.applyModuleChanges>`
|       :py:func:`updateSettingsUI <RigModules.ART_Chain.ART_Chain.updateSettingsUI>`
|       :py:func:`aimMode_Setup <RigModules.ART_Chain.ART_Chain.aimMode_Setup>`
|       :py:func:`pinModule <RigModules.ART_Chain.ART_Chain.pinModule>`
|       :py:func:`skinProxyGeo <RigModules.ART_Chain.ART_Chain.skinProxyGeo>`
|       :py:func:`buildRigCustom <RigModules.ART_Chain.ART_Chain.buildRigCustom>`
|       :py:func:`pickerUI <RigModules.ART_Chain.ART_Chain.pickerUI>`
|       :py:func:`importFBX <RigModules.ART_Chain.ART_Chain.importFBX>`
|       :py:func:`setupPickWalking <RigModules.ART_Chain.ART_Chain.setupPickWalking>`
|
|   **Optional Methods:**
|       :py:func:`jointMover_Build <RigModules.ART_Chain.ART_Chain.jointMover_Build>`
|       :py:func:`createMirrorModule_custom <RigModules.ART_Chain.ART_Chain.createMirrorModule_custom>`
|       :py:func:`mirrorTransformations <RigModules.ART_Chain.ART_Chain.mirrorTransformations>`
|       :py:func:`mirrorTransformations_Custom <RigModules.ART_Chain.ART_Chain.mirrorTransformations_Custom>`
|       :py:func:`pasteSettings <RigModules.ART_Chain.ART_Chain.pasteSettings>`
|       :py:func:`resetSettings <RigModules.ART_Chain.ART_Chain.resetSettings>`
|       :py:func:`selectRigControls <RigModules.ART_Chain.ART_Chain.selectRigControls>`
|       :py:func:`resetRigControls <RigModules.ART_Chain.ART_Chain.resetRigControls>`
|
|   **Module Specific Methods:**
|       :py:func:`addChainSegment <RigModules.ART_Chain.ART_Chain.addChainSegment>`
|       :py:func:`removeChainSegment <RigModules.ART_Chain.ART_Chain.removeChainSegment>`
|       :py:func:`hookUpMoverGlobalScale <RigModules.ART_Chain.ART_Chain.hookUpMoverGlobalScale>`
|       :py:func:`changeProxyGeo <RigModules.ART_Chain.ART_Chain.changeProxyGeo>`
|       :py:func:`changeControlShape <RigModules.ART_Chain.ART_Chain.changeControlShape>`
|       :py:func:`getCurrentNumberOfSegments <RigModules.ART_Chain.ART_Chain.getCurrentNumberOfSegments>`
|       :py:func:`hideLastGeo <RigModules.ART_Chain.ART_Chain.hideLastGeo>`
|       :py:func:`buildFkRig <RigModules.ART_Chain.ART_Chain.buildFkRig>`
|       :py:func:`buildIkRig <RigModules.ART_Chain.ART_Chain.buildIkRig>`
|       :py:func:`_createIkRibbon <RigModules.ART_Chain.ART_Chain._createIkRibbon>`
|       :py:func:`_createRibbonHair <RigModules.ART_Chain.ART_Chain._createRibbonHair>`
|       :py:func:`_moveHairFollicle <RigModules.ART_Chain.ART_Chain._moveHairFollicle>`
|       :py:func:`_getFacingDirection <RigModules.ART_Chain.ART_Chain._getFacingDirection>`
|       :py:func:`_setupSegmentScale <RigModules.ART_Chain.ART_Chain._setupSegmentScale>`
|       :py:func:`switchMode <RigModules.ART_Chain.ART_Chain.switchMode>`
|
|   **Interface Methods:**
|       :py:func:`toggleButtonState <RigModules.ART_Chain.ART_Chain.toggleButtonState>`
|       :py:func:`updateOutliner <RigModules.ART_Chain.ART_Chain.updateOutliner>`
|       :py:func:`picker_listWidget_select <RigModules.ART_Chain.ART_Chain.picker_listWidget_select>`
|       :py:func:`selectionScriptJob_animUI <RigModules.ART_Chain.ART_Chain.selectionScriptJob_animUI>`
|       :py:func:`picker_createContextMenu_FK <RigModules.ART_Chain.ART_Chain.picker_createContextMenu_FK>`
|       :py:func:`picker_createContextMenu <RigModules.ART_Chain.ART_Chain.picker_createContextMenu>`
|       :py:func:`switchMode_slider <RigModules.ART_Chain.ART_Chain.switchMode_slider>`


===============
File Attributes
===============
    * **icon:** This is the image file (125x75 .png) that gets used in the RigCreatorUI

    * **hoverIcon:** When you hover over the module in the module list, it will swap to this icon
      (background changes to orange). There are .psd template files for these.

    * **search:** These are search terms that are accepted when searching the list of modules in the
      RigCreatorUI

    * **class name:** The name of the class.

    * **jointMover:** The relative path to the joint mover file. Relative to the ARTv2 root directory.

    * **baseName:** The default name the module will get created with. Users can then add a prefix and/or
      suffix to the base name.

    * **rigs:** This is a simple list of what rigs this module can build. This feature isn't implemented yet,
      but the plan is to query this list and present these options to the user for them to select what rigs
      they want to build for the module. Right now, it will build all rigs.

    * **fbxImport:** This is a list that will show the options for the module in the import mocap interface.
      Normally, this list will have at least None and FK.

    * **matchData:** This is a list of options that will be presented for the module in a comboBox in the
      match over frame range interface. First argument is  a bool as to whether the module can or can't
      match. The second arg is a list of strings to display for the match options. For example:
      matchData = [True, ["Match FK to IK", "Match IK to FK"]]

===============
Class
===============
"""
# file imports
import json
import os
import re
from functools import partial

import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel

import Utilities.interfaceUtils as interfaceUtils
import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
from Base.ART_RigModule import ART_RigModule
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# file attributes
icon = "Modules/chain.png"
hoverIcon = "Modules/hover_chain.png"
search = "chain"
className = "ART_Chain"
jointMover = "Core/JointMover/z_up/ART_Chain.ma"
baseName = "chain"
displayName = "Chain"
rigs = ["FK", "IK", "Dynamic"]
fbxImport = ["None", "FK", "IK", "Both"]
matchData = [True, ["Match FK to IK", "Match IK to FK"]]
tooltip_image = "ART_Chain"


class ART_Chain(ART_RigModule):
    """This class creates the chain module, which can have a minimum of 2 joints and a maximum of 99."""

    def __init__(self, rigUiInst, moduleUserName):
        """Initiate the class, taking in the instance to the interface and the user specified name.

        :param rigUiInst: This is the rig creator interface instance being passed in.
        :param moduleUserName: This is the name specified by the user on module creation.

        Instantiate the following class variables as well:
            * **self.rigUiInst:** take the passed in interface instance and make it a class var
            * **self.moduleUserName:** take the passed in moduleUserName and make it a class var
            * **self.outlinerWidget:** an empty list that will hold all of the widgets added to the outliner

        Also, read the QSettings to find out where needed paths are.
        """

        self.rigUiInst = rigUiInst
        self.moduleUserName = moduleUserName
        self.outlinerWidgets = {}

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")

        ART_RigModule.__init__(self, "ART_Chain_Module", "ART_Chain", moduleUserName)

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    #                                                                                                           #
    # # # # # # # # # # # # # # # # #  M U S T   H A V E   M E T H O D S  # # # # # # # # # # # # # # # # # # # #
    #                                                                                                           #
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addAttributes(self):
        """
        Add custom attributes this module needs to the network node.

        Always calls on base class function first, then extends with any attributes unique to the class.
        """

        # call the base class method first to hook up our connections to the master module
        ART_RigModule.addAttributes(self)

        # add custom attributes for this specific module
        cmds.addAttr(self.networkNode, sn="Created_Bones", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".Created_Bones", "chain::chain::chain::", type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="baseName", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".baseName", baseName, type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="canAim", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".canAim", True, lock=True)

        cmds.addAttr(self.networkNode, sn="aimMode", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".aimMode", False, lock=True)

        cmds.addAttr(self.networkNode, sn="numJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".numJoints", 3, lock=True)

        cmds.addAttr(self.networkNode, sn="distribution", keyable=False)
        cmds.setAttr(self.networkNode + ".distribution", 2, lock=True)

        cmds.addAttr(self.networkNode, sn="controlType", at="enum",
                     en="Circle:Square:Cylinder", keyable=False)
        cmds.setAttr(self.networkNode + ".controlType", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="proxyShape", at="enum", en="Capsule:Box:Cylinder:Chain Link", keyable=False)
        cmds.setAttr(self.networkNode + ".proxyShape", 0, lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skeletonSettings_UI(self, name):
        """
        This is the UI for the module that has all of the configuration settings.

        :param name:  user given name of module (prefix + base_name + suffix)
        :param width: width of the skeleton settings groupBox. 335 usually
        :param height: height of the skeleton settings groupBox.
        :param checkable: Whether or not the groupBox can be collapsed.


        Build the groupBox that contains all of the settings for this module. Parent the groupBox
        into the main skeletonSettingsUI layout.
        Lastly, call on updateSettingsUI to populate the UI based off of the network node values.

        .. image:: /images/skeletonSettings.png

        """
        # width, height, checkable

        networkNode = self.returnNetworkNode
        font = QtGui.QFont()
        font.setPointSize(8)

        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # groupbox all modules get
        ART_RigModule.skeletonSettings_UI(self, name, 335, 380, True)

        # STANDARD BUTTONS

        # create a VBoxLayout to add to our Groupbox and then add a QFrame for our signal/slot
        self.mainLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setObjectName("lightnoborder")
        self.mainLayout.addWidget(self.frame)
        self.frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.frame.setMinimumSize(QtCore.QSize(320, 362))
        self.frame.setMaximumSize(QtCore.QSize(320, 362))

        # create layout that is a child of the frame
        self.layout = QtWidgets.QVBoxLayout(self.frame)

        # mirror module
        self.mirrorModLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.mirrorModLayout)
        self.mirrorModuleLabel = QtWidgets.QLabel("Mirror Module: ")
        self.mirrorModuleLabel.setFont(font)
        self.mirrorModLayout.addWidget(self.mirrorModuleLabel)

        mirror = cmds.getAttr(networkNode + ".mirrorModule")
        if mirror == "":
            mirror = "None"
        self.mirrorMod = QtWidgets.QLabel(mirror)
        self.mirrorMod.setFont(font)
        self.mirrorMod.setAlignment(QtCore.Qt.AlignHCenter)
        self.mirrorModLayout.addWidget(self.mirrorMod)

        # current parent
        self.currentParentMod = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.currentParentMod)
        self.currentParentLabel = QtWidgets.QLabel("Current Parent: ")
        self.currentParentLabel.setFont(font)
        self.currentParentMod.addWidget(self.currentParentLabel)

        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        self.currentParent = QtWidgets.QLabel(parent)
        self.currentParent.setFont(font)
        self.currentParent.setAlignment(QtCore.Qt.AlignHCenter)
        self.currentParentMod.addWidget(self.currentParent)

        # button layout for name/parent
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.buttonLayout)
        self.changeNameBtn = QtWidgets.QPushButton("Change Name")
        self.changeNameBtn.setMinimumHeight(30)
        self.changeNameBtn.setMaximumHeight(30)
        self.changeParentBtn = QtWidgets.QPushButton("Change Parent")
        self.changeParentBtn.setMinimumHeight(30)
        self.changeParentBtn.setMaximumHeight(30)
        self.mirrorModuleBtn = QtWidgets.QPushButton("Mirror Module")
        self.mirrorModuleBtn.setMinimumHeight(30)
        self.mirrorModuleBtn.setMaximumHeight(30)
        self.buttonLayout.addWidget(self.changeNameBtn)
        self.buttonLayout.addWidget(self.changeParentBtn)
        self.buttonLayout.addWidget(self.mirrorModuleBtn)
        self.changeNameBtn.setObjectName("settings")
        self.changeParentBtn.setObjectName("settings")
        self.mirrorModuleBtn.setObjectName("settings")

        text = "Change the name of the module."
        self.changeNameBtn.setToolTip(text)

        text = "Change the parent joint of the module."
        self.changeParentBtn.setToolTip(text)

        text = "Set the module that is a mirror of this module."
        self.mirrorModuleBtn.setToolTip(text)

        # button signal/slots
        self.changeNameBtn.clicked.connect(partial(self.changeModuleName, baseName, self, self.rigUiInst))
        self.changeParentBtn.clicked.connect(partial(self.changeModuleParent, self, self.rigUiInst))
        self.mirrorModuleBtn.clicked.connect(partial(self.setMirrorModule, self, self.rigUiInst))

        # bake offsets button
        self.bakeToolsLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.bakeToolsLayout)

        # Bake Offsets
        self.bakeOffsetsBtn = QtWidgets.QPushButton("Bake Offsets")
        self.bakeOffsetsBtn.setFont(headerFont)
        self.bakeOffsetsBtn.setMinimumHeight(30)
        self.bakeOffsetsBtn.setMaximumHeight(30)
        self.bakeToolsLayout.addWidget(self.bakeOffsetsBtn)
        self.bakeOffsetsBtn.clicked.connect(self.bakeOffsets)
        self.bakeOffsetsBtn.setObjectName("settings")
        text = "Bake the offset mover values up to the global movers to get them aligned."
        self.bakeOffsetsBtn.setToolTip(text)

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

        # proxy shape and control options
        self.proxyShapeLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.proxyShapeLayout)

        self.proxyShapeLabel = QtWidgets.QLabel("Proxy Mesh Shape: ")
        self.proxyShapeLayout.addWidget(self.proxyShapeLabel)

        self.proxyShape = QtWidgets.QComboBox()
        self.proxyShapeLayout.addWidget(self.proxyShape)
        text = "Change the shape of the proxy geometry. This is purely aesthetic and has no impact on the rig."
        self.proxyShape.setToolTip(text)

        for shape in ["Capsule", "Box", "Cylinder", "Chain Link"]:
            self.proxyShape.addItem(shape)

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout.addItem(spacerItem)

        self.jmCtrlLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.jmCtrlLayout)

        self.jmCtrlLabel = QtWidgets.QLabel("Joint Mover Ctrl: ")
        self.jmCtrlLayout.addWidget(self.jmCtrlLabel)

        self.jmCtrlShape = QtWidgets.QComboBox()
        self.jmCtrlLayout.addWidget(self.jmCtrlShape)
        text = "Change the shape of the control. This control will also be used for the rig build."
        self.jmCtrlShape.setToolTip(text)

        for shape in ["Circle", "Square", "Cylinder"]:
            self.jmCtrlShape.addItem(shape)

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

        # Number of joints in chain
        self.numJointsLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.numJointsLayout)

        self.numJointsLabel = QtWidgets.QLabel("Number of Joints in Chain: ")
        self.numJointsLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.numJointsLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.numJointsLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.numJointsLayout.addWidget((self.numJointsLabel))

        self.numJoints = QtWidgets.QSpinBox()
        self.numJoints.setMaximum(99)
        self.numJoints.setMinimum(2)
        self.numJoints.setMinimumSize(QtCore.QSize(100, 20))
        self.numJoints.setMaximumSize(QtCore.QSize(100, 20))
        self.numJoints.setValue(3)
        self.numJoints.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.numJointsLayout.addWidget(self.numJoints)
        self.numJoints.valueChanged.connect(self.toggleButtonState)

        # description of joints vs segments.
        self.segmentsLabel = QtWidgets.QLabel("(The chain will have " + str(self.numJoints.value() - 1) + " segments.)")
        self.layout.addWidget(self.segmentsLabel)

        # rebuild button
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout.addItem(spacerItem)

        self.applyButton = QtWidgets.QPushButton("Apply Changes")
        self.layout.addWidget(self.applyButton)
        self.applyButton.setFont(headerFont)
        self.applyButton.setMinimumSize(QtCore.QSize(300, 40))
        self.applyButton.setMaximumSize(QtCore.QSize(300, 40))
        self.applyButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.applyButton.setEnabled(False)
        self.applyButton.clicked.connect(partial(self.applyModuleChanges, self))
        text = "Update the scene with the module's new settings."
        self.applyButton.setToolTip(text)

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(self.groupBox, QtCore.SIGNAL("toggled(bool)"), self.frame.setVisible)
        self.groupBox.setChecked(False)

        # add custom skeletonUI settings  name, parent, rig types to install, mirror module, etc.
        # add to the rig cretor UI's module settings layout VBoxLayout
        self.rigUiInst.moduleSettingsLayout.addWidget(self.groupBox)

        # Populate the settings UI based on the network node attributes
        self.updateSettingsUI()

        # Connect signals/slots
        self.proxyShape.currentIndexChanged.connect(partial(self.changeProxyGeo))
        self.jmCtrlShape.currentIndexChanged.connect(partial(self.changeControlShape))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addJointMoverToOutliner(self):
        """
        Add the joint movers for this module to the outliner.

        Depending on the module settings, different joint movers may or may not be added. Also, each "joint" usually
        has three movers: global, offset, and geo. However, not all joints do, so this method is also used to specify
        which joint movers for each joint are added to the outliner.

        .. image:: /images/outliner.png

        """
        index = self.rigUiInst.treeWidget.topLevelItemCount()
        self.outlinerWidgets = {}
        self.chainWidgets = []

        # get number of joints in chain
        networkNode = self.returnNetworkNode
        currentNum = int(cmds.getAttr(networkNode + ".numJoints"))

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # Add the module to the tree widget in the outliner tab of the rig creator UI
        self.outlinerWidgets[self.name + "_treeModule"] = QtWidgets.QTreeWidgetItem(self.rigUiInst.treeWidget)
        self.rigUiInst.treeWidget.topLevelItem(index).setText(0, self.name)
        foreground = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.outlinerWidgets[self.name + "_treeModule"].setForeground(0, foreground)

        # for each joint in the chain, add that to the outliner
        parent = self.outlinerWidgets[self.name + "_treeModule"]
        name = "chain"
        number = ""
        for i in range(currentNum):
            if i < 9:
                number = "_0"

            else:
                number = "_"

            entry = prefix + name + suffix + number + str(i + 1)
            self.outlinerWidgets[entry] = QtWidgets.QTreeWidgetItem(parent)

            self.outlinerWidgets[entry].setText(0, entry)

            self.createGlobalMoverButton(entry, self.outlinerWidgets[entry], self.rigUiInst)
            self.createOffsetMoverButton(entry, self.outlinerWidgets[entry], self.rigUiInst)
            self.createMeshMoverButton(entry, self.outlinerWidgets[entry], self.rigUiInst)

            parent = self.outlinerWidgets[entry]
            self.chainWidgets.append(entry)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleChanges(self, moduleInst):
        """
        Update the scene after the settings are changed in the skeleton settings UI. In the case of the chain, this
        usually means an increase or decrease in the number of joints in the chain.

        This means also updating the created_bones attr, updating the joint mover if needed,
        running self.updateNeck, updating the outliner, and updating the bone count.

        :param moduleInst: self (usually, but there are cases like templates where an inst on disc is passed in.)
        """

        # turn off aimMode
        self.aimMode_Setup(False)

        # get prefix/suffix
        networkNode = self.returnNetworkNode
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # create list of the new created bones
        createdJoints = []

        # get current number of chain joints value
        # currentNum = int(cmds.getAttr(networkNode + ".numJoints"))
        currentNum = self.getCurrentNumberOfSegments()

        # get new number of chain joints value
        newNumJoints = self.numJoints.value()

        if newNumJoints != currentNum:
            # look for any attached modules
            attachedModules = self.checkForDependencies()
            if len(attachedModules) > 0:
                self.fixDependencies(attachedModules)

        if newNumJoints > currentNum:
            # add more chain segments
            for i in range((newNumJoints - currentNum)):
                self.addChainSegment(True)

        if newNumJoints < currentNum:
            # remove chain segments
            for i in range((currentNum - newNumJoints)):
                self.removeChainSegment()

        # update numJoints value
        cmds.setAttr(networkNode + ".numJoints", lock=False)
        cmds.setAttr(networkNode + ".numJoints", newNumJoints, lock=True)

        self.segmentsLabel.setText("(The chain will have " + str(self.numJoints.value() - 1) + " segments.)")

        # update shape attrs
        cmds.setAttr(networkNode + ".controlType", lock=False)
        cmds.setAttr(networkNode + ".controlType", self.jmCtrlShape.currentIndex(), lock=True)

        cmds.setAttr(networkNode + ".proxyShape", lock=False)
        cmds.setAttr(networkNode + ".proxyShape", self.proxyShape.currentIndex(), lock=True)

        # build attrString
        for i in range(newNumJoints):
            if i < 9:
                createdJoints.append(prefix + "chain" + suffix + "_0" + str(i + 1))
            else:
                createdJoints.append(prefix + "chain" + suffix + "_" + str(i + 1))

        attrString = ""
        for bone in createdJoints:
            attrString += bone + "::"

        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # reset button
        self.applyButton.setEnabled(False)

        # update outliner
        self.updateOutliner(currentNum)
        self.updateBoneCount()

        # turn on aim mode
        self.aimMode_Setup(True)

        # hide last mover's proxy geo
        self.hideLastGeo()

        # clear selection
        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateSettingsUI(self):
        """
        Update the skeleton settings UI based on the network node values for this module.
        """

        # this function will update the settings UI when the UI is launched based on the network node settings in the
        # scene
        networkNode = self.returnNetworkNode

        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # update UI elements
        self.numJoints.setValue(numJoints)

        self.segmentsLabel.setText("(The chain will have " + str(self.numJoints.value() - 1) + " segments.)")

        # apply changes
        self.applyButton.setEnabled(False)

        # shapes
        controlShape = cmds.getAttr(networkNode + ".controlType")
        self.jmCtrlShape.setCurrentIndex(controlShape)

        proxyShape = cmds.getAttr(networkNode + ".proxyShape")
        self.proxyShape.setCurrentIndex(proxyShape)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def aimMode_Setup(self, state):
        """
        This functions sets up or removes the setup for aim mode, which is a setting in the joint mover phase. Aim mode
        makes sure that the parent continues to aim at the child, and does so by setting up aim constraints between the
        movers.

        If the passed in state is False, it will remove the aimConstraints, making the parents no longer aim at their
        children.

        :param state: Whether or not to setup or remove the aim mode setup.

        """

        # get attributes needed
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        networkNode = self.returnNetworkNode
        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # setup aim vector details per side
        aimVector = [1, 0, 0]
        aimUp = [0, 1, 0]

        # if passed in state is True:
        if state:

            # setup aim constraints
            for i in range(int(numJoints)):
                x = i + 2
                if i < 9:
                    mover = prefix + "chain" + suffix + "_0" + str(i + 1)
                else:
                    mover = prefix + "chain" + suffix + "_" + str(i + 1)
                if x < 9:
                    master = prefix + "chain" + suffix + "_0" + str(x)
                else:
                    master = prefix + "chain" + suffix + "_" + str(x)

                if cmds.objExists(master + "_lra"):
                    cmds.aimConstraint(master + "_lra", mover + "_mover_offset", aimVector=aimVector, upVector=aimUp,
                                       wut="objectrotation", wu=[0, 1, 0], worldUpObject=master + "_mover_end", mo=True)

        # if passed in state is False:
        if not state:
            cmds.select(name + "_mover_grp", hi=True)
            aimConstraints = cmds.ls(sl=True, exactType="aimConstraint")

            for constraint in aimConstraints:
                cmds.lockNode(constraint, lock=False)
                cmds.delete(constraint)

            self.bakeOffsets()
            cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pinModule(self, state):
        """
        Pins the module in place in 3D space so that the parent module can no longer affect its position. It does this
        by constraining it to a locator that gets created in the same spot as the top level group of the module.

        :param state: Whether or not to setup pinning or remove pinning.

        """

        networkNode = self.returnNetworkNode
        topLevelMover = self.name + "_01_mover"

        # create a locator if state is true that will pin the module in place.
        if state:
            if cmds.getAttr(networkNode + ".pinned") is True:
                return
            loc = cmds.spaceLocator()[0]
            cmds.setAttr(loc + ".v", False, lock=True)
            constraint = cmds.parentConstraint(topLevelMover, loc)[0]
            cmds.delete(constraint)
            const = cmds.parentConstraint(loc, topLevelMover)[0]

            # add attributes to our network node that will allow us to track our constraint and locator for pinning.
            if not cmds.objExists(networkNode + ".pinConstraint"):
                cmds.addAttr(networkNode, ln="pinConstraint", keyable=True, at="message")
            if not cmds.objExists(networkNode + ".pinLocator"):
                cmds.addAttr(networkNode, ln="pinLocator", keyable=True, at="message")

            cmds.connectAttr(const + ".message", networkNode + ".pinConstraint")
            cmds.connectAttr(loc + ".message", networkNode + ".pinLocator")

        if not state:
            # delete the locator and constrint connected to the respective attributes to disable pinning.
            if cmds.objExists(networkNode + ".pinConstraint"):
                connections = cmds.listConnections(networkNode + ".pinConstraint")
                if connections is not None:
                    for connection in connections:
                        cmds.delete(connection)
            if cmds.objExists(networkNode + ".pinLocator"):
                connections = cmds.listConnections(networkNode + ".pinLocator")
                if connections is not None:
                    for connection in connections:
                        cmds.delete(connection)

        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skinProxyGeo(self):
        """
        Boiler-plate function that skins this modules' proxy geo.

        """

        # get the network node
        networkNode = self.returnNetworkNode

        name = cmds.getAttr(networkNode + ".moduleName")
        baseName = cmds.getAttr(networkNode + ".baseName")
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        # get this module's proxy geo meshes
        cmds.select(name + "_mover_grp", hi=True)
        proxyGeoMeshes = []
        selection = cmds.ls(sl=True)
        for each in selection:
            if each.find("proxy_geo") != -1:
                if cmds.nodeType(each) == "transform":
                    proxyGeoMeshes.append(each)

        lastMesh = max(proxyGeoMeshes)
        # skin the proxy geo meshes
        for mesh in proxyGeoMeshes:
            if mesh != lastMesh:
                # get material assignments of each face
                faceMaterials = utils.getFaceMaterials(mesh)

                # duplicate proxy geo mesh
                dupeMesh = cmds.duplicate(mesh, name="skin_" + mesh)[0]
                cmds.setAttr(dupeMesh + ".overrideEnabled", lock=False)
                cmds.setAttr(dupeMesh + ".overrideDisplayType", 0)

                # assign materials to faces
                for key in faceMaterials:
                    for each in faceMaterials.get(key):
                        try:
                            dupe = each.replace(each, "skin_" + each)
                            cmds.select(dupe)
                            cmds.hyperShade(assign=key)
                        except Exception, e:
                            print str(e)

                # create skinned geo group
                if not cmds.objExists("skinned_proxy_geo"):
                    cmds.group(empty=True, name="skinned_proxy_geo")

                cmds.parent(dupeMesh, "skinned_proxy_geo")

                boneName = mesh.partition(name + "_")[2]
                boneName = boneName.partition("_proxy_geo")[0]
                joint = prefix + baseName + suffix + "_" + boneName

                if not cmds.objExists(joint):
                    cmds.delete(dupeMesh)

                else:
                    cmds.select([dupeMesh, joint])
                    cmds.skinCluster(tsb=True, maximumInfluences=1, obeyMaxInfluences=True, bindMethod=0, skinMethod=0,
                                     normalizeWeights=True)
                    cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRigCustom(self, textEdit, uiInst):
        """
        Boiler-plate function for kicking off the various rigs that need to be built for this module. Also hooks up rig
        switching/blending and parents the top level nodes of the built rigs into the main hierarchy.

        :param textEdit: The textEdit widget to post status updates to
        :param uiInst: The Rig Creator ui instance

        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Building " + self.name + " Rig..")

        # get the network node and find out which rigs to build
        networkNode = self.returnNetworkNode
        buildFK = True
        buildIK = True

        # have it build all rigs by default, unless there is an attr stating otherwise (backwards- compatability)
        numRigs = 2
        builtRigs = []

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create a new network node to hold the control types
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if not cmds.objExists(networkNode + ".controls"):
            cmds.addAttr(networkNode, sn="controls", at="message")

        controlNode = cmds.createNode("network", name=networkNode + "_Controls")
        cmds.addAttr(controlNode, sn="parentModule", at="message")

        # connect new network node to original network node
        cmds.connectAttr(networkNode + ".controls", controlNode + ".parentModule")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create groups and settings
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create the chain group
        chainJoints = self.returnCreatedJoints
        if len(chainJoints) <= 3:
            buildIK = False

        self.chainGroup = cmds.group(empty=True, name=self.name + "_group")
        constraint = cmds.parentConstraint(chainJoints[0], self.chainGroup)[0]
        cmds.delete(constraint)

        # create the chain settings group
        self.chainSettings = cmds.group(empty=True, name=self.name + "_settings")
        cmds.parent(self.chainSettings, self.chainGroup)
        for attr in (cmds.listAttr(self.chainSettings, keyable=True)):
            cmds.setAttr(self.chainSettings + "." + attr, lock=True, keyable=False)

        # add mode attribute to settings
        if numRigs > 1:
            cmds.addAttr(self.chainSettings, ln="mode", min=0, max=numRigs - 1, dv=0, keyable=True)

        # create the ctrl group (what will get the constraint to the parent)
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        self.chainCtrlGrp = cmds.group(empty=True, name=self.name + "_chain_ctrl_grp")

        constraint = cmds.parentConstraint("driver_" + parentBone, self.chainCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(self.chainCtrlGrp, self.chainGroup)
        cmds.makeIdentity(self.chainCtrlGrp, t=1, r=1, s=1, apply=True)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # BUILD RIGS
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       FK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # if build FK was true, build the FK rig now
        if buildFK:
            fkInfo = self.buildFkRig(textEdit, uiInst, builtRigs, networkNode)
            builtRigs.append(["FK", fkInfo])  # [1] = nodes to hide

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       iK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if buildIK:
            ikInfo = self.buildIkRig(textEdit, uiInst, builtRigs, networkNode)
            builtRigs.append(["IK", ikInfo])

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #            Hook up FK/IK Switching            # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # mode
        if len(builtRigs) > 1:
            attrData = []
            rampData = []

            """ CONSTRAINTS """
            # get the constraint connections on the driver joints for the arms
            connections = []
            for joint in chainJoints:
                connections.extend(list(set(cmds.listConnections("driver_" + joint, type="constraint"))))
                ramps = (list(set(cmds.listConnections("driver_" + joint, type="ramp"))))
                for ramp in ramps:
                    connections.append(ramp + ".uCoord")

                for connection in connections:
                    driveAttrs = []

                    if cmds.nodeType(connection) in ["pointConstraint", "orientConstraint"]:

                        # get those constraint target attributes for each constraint connection
                        targets = cmds.getAttr(connection + ".target", mi=True)
                        if len(targets) > 1:
                            for each in targets:
                                driveAttrs.append(
                                    cmds.listConnections(
                                        connection + ".target[" + str(each) + "].targetWeight",
                                        p=True))

                            # add this data to our master list of constraint attribute data
                            attrData.append(driveAttrs)
                    else:
                        if cmds.nodeType(connection) == "ramp":
                            rampData.append(connection)

            rampData = list(set(rampData))

            # setup set driven keys on our moder attr and those target attributes
            for i in range(numRigs):

                cmds.setAttr(self.chainSettings + ".mode", i)

                # go through attr data and zero out anything but the first element in the list
                for data in attrData:
                    for each in data:
                        cmds.setAttr(each[0], 0)

                    cmds.setAttr(data[i][0], 1)

                # set driven keys
                for data in attrData:
                    for each in data:
                        cmds.setDrivenKeyframe(each[0], cd=self.chainSettings + ".mode", itt="linear",
                                               ott="linear")

            """ RAMPS """
            # direct connect mode to uCoord value (only works if there are 2 rigs) <- not sure if that is thecase still
            for data in rampData:
                # create a multiply node that takes first input of 1/numRigs and 2nd of mode direct connection
                multNode = cmds.shadingNode("multiplyDivide", asUtility=True,
                                            name=self.name + "_" + data.partition(".uCoord")[0] + "_mult")
                cmds.setAttr(multNode + ".input1X", float(float(1) / float(numRigs - 1)))
                cmds.connectAttr(self.chainSettings + ".mode", multNode + ".input2X")
                cmds.connectAttr(multNode + ".outputX", data)

            # hook up control visibility
            for i in range(len(builtRigs)):
                cmds.setAttr(self.chainSettings + ".mode", i)
                for rig in builtRigs:
                    visNodes = rig[1]
                    for node in visNodes:
                        if node is not None:
                            cmds.setAttr(node + ".v", 0)

                    if builtRigs.index(rig) == i:
                        visNodes = rig[1]
                        for node in visNodes:
                            if node is not None:
                                cmds.setAttr(node + ".v", 1)

                    cmds.setDrivenKeyframe(visNodes, at="visibility", cd=self.chainSettings + ".mode",
                                           itt="linear",
                                           ott="linear")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #            Parent Under Offset Ctrl           # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # parent under offset_anim if it exists(it always should)
        if cmds.objExists("offset_anim"):
            cmds.parent(self.chainGroup, "offset_anim")

        if cmds.objExists("rig_grp"):
            try:
                cmds.parent(self.ik_grp, "rig_grp")
            except AttributeError:
                # IK rig was not built
                pass

        # return data
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        try:
            uiInst.rigData.append([self.chainCtrlGrp, "driver_" + parentBone, numRigs])
        except Exception:
            pass

        # lock down network node
        cmds.lockNode(networkNode, lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pickerUI(self, center, animUI, networkNode, namespace):
        """
        Build the animation picker for the module. This particular picker is very unique compared to previous
        modules.


        :param center: the center of the QGraphicsScene
        :param animUI: the instance of the AnimationUI
        :param networkNode: the module's network node
        :param namespace: the namespace of the character

        """
        # create a style sheet specifically for this widget
        stylesheet = """
            QScrollBar:vertical {
            border: 2px solid black;
            background: rgb(0,0,0);
            width: 15px;
            margin: 22px 0 22px 0;
            }

            QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 rgb(60,60,60), stop:1 rgb(90,90,90));
            min-height: 20px;
            }

            QScrollBar::add-line:vertical {
            border: 2px solid black;
            background: rgb(90, 90, 90);
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
            border: 2px solid black;
            background: rgb(60, 60, 60);
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            border: 2px solid black;
            width: 3px;
            height: 3px;
            background-color: rgb(25,175,255);
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
            }

            QTabBar::tab
            {
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 rgb(30,30,30), stop:1 rgb(60,60,60));
            }

            QTabBar::tab:selected
            {
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 rgb(30,30,30), stop:1 rgb(25,175,255));
            }


            QTabBar::tab:hover
            {
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 rgb(30,30,30), stop:1 rgb(255,175,25));
            }

            QSlider::groove:horizontal {
            border: 1px solid black;
            background: rgb(60,60,60);
            height: 10px;
            border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
            background: qlineargradient(x1: 0, y1: 1,    x2: 0, y2: 0,
                stop: 0 rgb(30,30,30), stop: 1 rgb(25,175,255));
            background: qlineargradient(x1: 1, y1: 0, x2: 0, y2: 0.2,
                stop: 0 rgb(25,175,255), stop: 1 rgb(30,30,30));
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
            }

            QSlider::add-page:horizontal {
            background: rgb(0,0,0);
            border: 1px solid black;
            height: 10px;
            border-radius: 4px;
            }

            QSlider::handle:horizontal {
            background: rgb(25, 175, 255);
            border: 1px solid black;
            width: 13px;
            margin-top: -2px;
            margin-bottom: -2px;
            border-radius: 4px;
            }

            QSlider::handle:horizontal:hover {
            border: 1px solid rgb(255, 175,25);
            border-radius: 4px;
            }

            QSlider::sub-page:horizontal:disabled {
            background: #bbb;
            border-color: #999;
            }

            QSlider::add-page:horizontal:disabled {
            background: #eee;
            border-color: #999;
            }

            QSlider::handle:horizontal:disabled {
            background: #eee;
            border: 1px solid #aaa;
            border-radius: 4px;
            }

            QToolTip
            {
            color: #ffffff;
            background-color: #2a82da;
            border: 1px solid white;
            }


            QWidget
            {
            background-color: rgb(60,60,60);
            }
            """

        # get the namespace and the number of joints
        self.namespace = namespace
        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # get the controls
        fkControls = self.getControls(False, "fkControls")
        fkControls = sorted(fkControls)
        ikControls = self.getControls(False, "ikControls")
        ikControls = sorted(ikControls)

        # create qBrushes
        clearBrush = QtGui.QBrush(QtCore.Qt.black)
        clearBrush.setStyle(QtCore.Qt.NoBrush)
        greenBrush = QtGui.QColor(122, 150, 67)
        yellowBrush = QtGui.QColor(155, 118, 67)
        blueBrush = QtGui.QColor(67, 122, 150)

        # create the context menu
        if cmds.objExists(namespace + ":" + self.name + "_settings.mode"):
            contextMenu = self.picker_createContextMenu()
        else:
            contextMenu = self.picker_createContextMenu_FK()

        # create the picker border item
        if networkNode.find(":") != -1:
            moduleNode = networkNode.partition(":")[2]
        else:
            moduleNode = networkNode
        self.borderItem = interfaceUtils.pickerBorderItem(center.x() - 100, center.y() - 125, 200, 240, clearBrush,
                                                          moduleNode, None, contextMenu)
        interfaceUtils.addTextToButton(self.name, self.borderItem, False, True, False)

        # create a proxy widget for the fk/ik slider
        self.modeWidget = QtWidgets.QGraphicsProxyWidget(self.borderItem)

        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: transparent")
        widget.setMinimumSize(QtCore.QSize(180, 35))
        widget.setMaximumSize(QtCore.QSize(180, 35))
        layout = QtWidgets.QHBoxLayout(widget)

        # if both FK and IK rigs have been built, add an FK/IK blend slider widget
        if cmds.objExists(namespace + ":" + self.name + "_settings.mode"):
            label1 = QtWidgets.QLabel("FK")
            label1.setStyleSheet("color: rgb(26, 175, 255);")
            layout.addWidget(label1)

            slider = QtWidgets.QSlider()
            slider.setStyleSheet("background-color: rgb(60,60,60);")
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setMaximumWidth(160)
            slider.setRange(0, 100)
            slider.setStyleSheet(stylesheet)
            layout.addWidget(slider)
            slider.valueChanged.connect(partial(self.switchMode_slider, slider))
            slider.setToolTip("blend between FK and IK mode")

            modeVal = cmds.getAttr(namespace + ":" + self.name + "_settings.mode")
            slider.setValue(modeVal * 100)

            label2 = QtWidgets.QLabel("IK")
            label2.setStyleSheet("color: rgb(26, 175, 255);")
            layout.addWidget(label2)

        # embed the tabWidget in the proxyWidget and set the proxy widget position within the border item
        self.modeWidget.setWidget(widget)
        self.modeWidget.setPos(self.modeWidget.parentItem().boundingRect().bottomLeft())
        self.modeWidget.setPos(self.modeWidget.pos().x() + 10, self.modeWidget.pos().y() - 30)

        # create a proxy widget for the listWidget
        self.proxyWidget = QtWidgets.QGraphicsProxyWidget(self.borderItem)

        # create a main widget
        self.picker_mainWidget = QtWidgets.QWidget()
        self.picker_mainWidget.setStyleSheet("background: transparent")

        # create a tab widget
        tabWidget = QtWidgets.QTabWidget(self.picker_mainWidget)
        tabWidget.setMinimumSize(QtCore.QSize(160, 210))
        tabWidget.setMaximumSize(QtCore.QSize(160, 210))
        tabWidget.setStyleSheet(stylesheet)

        # create tab 1 (FK_Controls)
        tab_1 = QtWidgets.QWidget()
        tab_1.setStyleSheet(stylesheet)

        # create a list widget to hold all of the chain controls
        self.fk_listWidget = interfaceUtils.PickerList(contextMenu, self.borderItem, tab_1)
        self.fk_listWidget.setMinimumSize(QtCore.QSize(155, 190))
        self.fk_listWidget.setMaximumSize(QtCore.QSize(155, 190))
        self.fk_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.fk_listWidget.setSpacing(3)
        self.fk_listWidget.setAlternatingRowColors(True)
        self.fk_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.fk_listWidget.itemClicked.connect(partial(self.picker_listWidget_select, self.fk_listWidget))

        # add fk controls to listWidget
        for i in range(len(fkControls)):
            niceName = fkControls[i].partition(":")[2]
            niceName = "fk" + niceName.partition(self.name)[2]

            item = QtWidgets.QListWidgetItem()
            item.setText(niceName)

            # set data2 to be the full name of the control
            item.setData(QtCore.Qt.UserRole, fkControls[i])

            item.setForeground(blueBrush)
            self.fk_listWidget.addItem(item)

        # add the tab
        tabWidget.addTab(tab_1, "FK")

        # create tab 2 (IK_Controls)
        tab_2 = QtWidgets.QWidget()
        tab_2.setStyleSheet(stylesheet)

        # create a list widget to hold all of the chain controls
        self.ik_listWidget = interfaceUtils.PickerList(contextMenu, self.borderItem, tab_2)
        self.ik_listWidget.setMinimumSize(QtCore.QSize(155, 190))
        self.ik_listWidget.setMaximumSize(QtCore.QSize(155, 190))
        self.ik_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ik_listWidget.setSpacing(3)
        self.ik_listWidget.setAlternatingRowColors(True)
        self.ik_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ik_listWidget.itemClicked.connect(partial(self.picker_listWidget_select, self.ik_listWidget))

        # add ik controls to listWidget
        addLast = []
        for i in range(len(ikControls)):
            niceName = ikControls[i].partition(":")[2]
            niceName = "ik" + niceName.partition(self.name)[2]

            item = QtWidgets.QListWidgetItem()
            item.setText(niceName)

            # set data2 to be the full name of the control
            item.setData(QtCore.Qt.UserRole, ikControls[i])

            if niceName.find("offset") != -1:
                item.setForeground(blueBrush)
                addLast.append(item)
            else:
                item.setForeground(yellowBrush)
                self.ik_listWidget.addItem(item)

        for each in addLast:
            self.ik_listWidget.addItem(each)

        # add the tab
        tabWidget.addTab(tab_2, "IK")

        # embed the tabWidget in the proxyWidget and set the proxy widget position within the border item
        self.proxyWidget.setWidget(self.picker_mainWidget)
        self.proxyWidget.setPos(self.proxyWidget.parentItem().boundingRect().topLeft())
        self.proxyWidget.setPos(self.proxyWidget.pos().x() + 20, self.proxyWidget.pos().y() + 10)

        # =======================================================================
        # #Create scriptJob for selection. Set scriptJob number to borderItem.data(5)
        # =======================================================================
        scriptJob = cmds.scriptJob(
            event=["SelectionChanged", partial(self.selectionScriptJob_animUI, self.fk_listWidget,
                                               self.ik_listWidget)], kws=True)
        self.borderItem.setData(5, scriptJob)
        if scriptJob not in animUI.selectionScriptJobs:
            animUI.selectionScriptJobs.append(scriptJob)

        print "scriptJob Number: " + str(scriptJob)
        for each in animUI.selectionScriptJobs:
            print each

        # return items
        return [self.borderItem, False, None]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importFBX(self, importMethod, character):
        """
        Import FBX motion onto this module's rig controls.

        :param importMethod: The import method to be used (options defined in the file attributes)
        :param character: the namespace of the character

        Each module has to define what import methods it offers (at the very top of the module file) and then define
        how motion is imported using those methods.
        """

        returnControls = []

        networkNode = self.returnRigNetworkNode
        moduleName = cmds.getAttr(networkNode + ".moduleName")

        # find created joints
        joints = self.returnCreatedJoints

        # find controls
        controlNode = cmds.listConnections(networkNode + ".controls")[0]
        fkControls = self.getControls(False, "fkControls")
        ikControls = self.getControls(False, "ikControls")

        # Handle Import Method/Constraints
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if importMethod == "FK":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 0)

            for joint in joints:
                cmds.parentConstraint(joint, character + ":fk_" + joint + "_anim")
                returnControls.append(character + ":fk_" + joint + "_anim")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if importMethod == "IK":
            if cmds.objExists(character + ":" + moduleName + "_settings.mode"):
                cmds.setAttr(character + ":" + moduleName + "_settings.mode", 1)

                for control in ikControls:
                    # get the joint to have our control constrained to
                    joint = None
                    follicleJoint = cmds.listConnections(control + ".drivesJoint")[0]
                    pConst = cmds.listConnections(follicleJoint, type="pointConstraint", et=True)[0]
                    chain_ik_joint = cmds.listConnections(pConst)[0]
                    pconstraints = cmds.listConnections(chain_ik_joint, c=False, s=False, d=True,
                                                        type="pointConstraint", et=True)
                    for each in pconstraints:
                        if each.find("driver") != -1:
                            joint = each.replace("driver_", "")
                            joint = joint.partition("_pointConstraint1")[0]
                            joint = joint.partition(character + ":")[2]
                            break

                    cmds.parentConstraint(joint, control)
                    returnControls.append(control)
            else:
                cmds.warning("No IK controls to import motion onto.")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if importMethod == "Both":
            for joint in joints:
                cmds.parentConstraint(joint, character + ":fk_" + joint + "_anim")
                returnControls.append(character + ":fk_" + joint + "_anim")

            for control in ikControls:
                # get the joint to have our control constrained to
                joint = None
                follicleJoint = cmds.listConnections(control + ".drivesJoint")[0]
                pConst = cmds.listConnections(follicleJoint, type="pointConstraint", et=True)[0]
                chain_ik_joint = cmds.listConnections(pConst)[0]
                pconstraints = cmds.listConnections(chain_ik_joint, c=False, s=False, d=True,
                                                    type="pointConstraint", et=True)
                for each in pconstraints:
                    if each.find("driver") != -1:
                        joint = each.replace("driver_", "")
                        joint = joint.partition("_pointConstraint1")[0]
                        joint = joint.partition(character + ":")[2]
                        break

                cmds.parentConstraint(joint, control)
                returnControls.append(control)

        if importMethod == "None":
            pass

        return returnControls

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setupPickWalking(self):
        """
        Sets up pickwalking between the controls in the module. These are just defaults and the pickwalking
        relationships can be changed using the pickwalking tool.

        """

        # get controls
        networkNode = self.returnNetworkNode

        fkControls = self.getControls(False, "fkControls")
        fkControls = sorted(fkControls)
        ikControls = self.getControls(False, "ikControls")
        ikControls = sorted(ikControls)

        # setup FK pickwalking
        for i in range(len(fkControls)):
            cmds.addAttr(fkControls[i], ln="pickWalkDown", at="message")

            try:
                cmds.connectAttr(fkControls[i + 1] + ".message", fkControls[i] + ".pickWalkDown")
                cmds.addAttr(fkControls[i + 1], ln="pickWalkUp", at="message")
                cmds.connectAttr(fkControls[i] + ".message", fkControls[i + 1] + ".pickWalkUp")
            except IndexError:
                pass

        # setup IK pickwalking
        try:
            follicles = cmds.listRelatives(self.name + "_ribbon_follicles_grp", children=True)

            orderedControls = []
            joints = []

            for follicle in follicles:
                joint = cmds.listRelatives(follicle, children=True, ad=True, type='joint')[0]
                joints.append(joint)

            joints = sorted(joints)
            for joint in joints:
                control = cmds.listConnections(joint + ".drivenBy")[0]
                orderedControls.append(control)

            for i in range(len(orderedControls)):
                cmds.addAttr(orderedControls[i], ln="pickWalkDown", at="message")

                try:
                    cmds.connectAttr(orderedControls[i + 1] + ".message", orderedControls[i] + ".pickWalkDown")
                    cmds.addAttr(orderedControls[i + 1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(orderedControls[i] + ".message", orderedControls[i + 1] + ".pickWalkUp")
                except IndexError:
                    pass
        except ValueError:
            pass

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    #                                                                                                           #
    # # # # # # # # # # # # # # # # #   O P T I O N A L    M E T H O D S    # # # # # # # # # # # # # # # # # # #
    #                                                                                                           #
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def jointMover_Build(self, path):
        """
        Import the joint mover file with the given path.

        After importing the module's joint mover file, rename imported nodes to use module name.
        Then, assign existing matching materials to joint mover proxy geometry, deleting the imported
        materials if they were duplicates. Then parent into the main JointMover group. Lastly, hook up
        global scaling on the joint movers.

        Override of base class, so that the chain 'links' can be added as needed.

        :param path: Path of joint mover file to import
        """

        # get the full path for the joint mover file
        fullPath = os.path.join(self.toolsPath, path)

        # import the file
        if os.path.exists(fullPath):
            nodes = cmds.file(fullPath, i=True, iv=True, type="mayaAscii", rnn=True)
            validTypes = ["transform", "joint", "ikHandle"]

            # loop through returned nodes from import, and find the mover_grp, renaming it and all
            # children to have user specified name as prefix
            for node in nodes:
                if node.find("|mover_grp") == 0:
                    children = cmds.listRelatives(node, allDescendents=True, type="transform")
                    moverGrp = node.partition("|")[2]
                    movers = [moverGrp]

                    for child in children:
                        try:
                            if cmds.nodeType(child) in validTypes:
                                movers.append(child)
                        except Exception, e:
                            print e

                    for mover in movers:
                        try:
                            if mover.find("_") == 0:
                                cmds.rename(mover, self.name + mover)
                            else:
                                cmds.rename(mover, self.name + "_" + mover)
                        except Exception, e:
                            print mover, self.name + "_" + mover
                            print str(e)

                    # exit loop
                    break

            # assign materials if they exist, removing duplicate materials
            materials = [["*_blue_m", "blue_m"], ["*_green_m", "green_m"], ["*_red_m", "red_m"],
                         ["*_white_m", "white_m"], ["*_proxy_shader_tan", "proxy_shader_tan"],
                         ["*_proxy_shader_black", "proxy_shader_black"]]
            deleteMaterials = []
            for material in materials:
                try:
                    # select materials for the joint mover
                    cmds.select(material[0])
                    foundMaterials = cmds.ls(sl=True)

                    # loop through each color material (dupes)
                    for mat in foundMaterials:
                        cmds.hyperShade(objects=mat)
                        assignedGeo = cmds.ls(sl=True)

                        # select the geo and the original material, and assign
                        originalMaterial = material[1]
                        for geo in assignedGeo:
                            cmds.select([geo, originalMaterial])
                            cmds.hyperShade(assign=originalMaterial)

                        # delete the material no longer needed
                        deleteMaterials.append(mat)
                except Exception:
                    pass

            # delete all deleteMaterials
            for mat in deleteMaterials:
                cmds.delete(mat)

            # add to JointMover grp
            cmds.refresh(force=True)
            if not cmds.objExists("JointMover"):
                cmds.group(empty=True, name="JointMover")

            try:
                cmds.parent("|" + self.name + "_mover_grp", "JointMover")
            except Exception, e:
                print str(e)
            globalMover = utils.findGlobalMoverFromName(self.name)
            cmds.select(globalMover)
            cmds.setToolTo("moveSuperContext")

            # obey visibility toggles
            self.rigUiInst.setMoverVisibility()

            # add segments (x2) (since default chain length is 3, and joint mover file only has 1 segment.
            self.addChainSegment()
            self.addChainSegment()

            # hide last mover's proxy geo
            self.hideLastGeo()

            # hook up global scale on joint movers
            try:
                movers = self.returnJointMovers

                for each in [movers[0], movers[1]]:
                    for mover in each:
                        if not cmds.objExists(mover + ".globalScale"):
                            try:
                                cmds.aliasAttr("globalScale", mover + ".scaleZ")
                                cmds.connectAttr(mover + ".globalScale", mover + ".scaleX")
                                cmds.connectAttr(mover + ".globalScale", mover + ".scaleY")
                                cmds.setAttr(mover + ".scaleX", keyable=False)
                                cmds.setAttr(mover + ".scaleY", keyable=False)
                            except Exception:
                                pass
                # lock movers
                for each in movers:
                    for mover in each:
                        cmds.lockNode(mover, lock=True)
            except Exception:
                pass

        else:
            cmds.confirmDialog(title="Joint Mover", message="Could not find associated joint mover file.",
                               icon="critical")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createMirrorModule_custom(self):
        """
        This function can be run after a mirror of this module has been created. Some modules utilize it, others don't.
        In this case of the chain module, it simply applies module changes again to get the proxy and control shape
        changes applied.

        """

        self.applyModuleChanges(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorTransformations(self):
        """
        This method mirrors transformations for the module's mirror module.
        """

        # get the mirror module
        networkNode = self.returnNetworkNode
        mirrorModule = cmds.getAttr(networkNode + ".mirrorModule")
        moduleName = cmds.getAttr(networkNode + ".moduleName")
        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        baseName = cmds.getAttr(networkNode + ".baseName")

        # get mirror module instance and information
        mirrorInst = self.returnMirrorModuleInst

        # turn off aim mode
        mirrorInst.aimMode_Setup(False)

        moverTypes = self.returnJointMovers
        for moverType in moverTypes:
            for jointMover in moverType:

                mirrorMover = jointMover.replace(moduleName, mirrorModule, 1)
                if not cmds.objExists(mirrorMover):
                    mirrorMover = jointMover

                attrs = cmds.listAttr(jointMover, keyable=True)
                for attr in attrs:
                    value = cmds.getAttr(jointMover + "." + attr)
                    try:
                        cmds.setAttr(mirrorMover + "." + attr, value)
                    except Exception:
                        pass

        cmds.select(clear=True)

        # turn aim mode on
        mirrorInst.aimMode_Setup(True)

        # extend functionality
        self.mirrorTransformations_Custom()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorTransformations_Custom(self):
        """
        This method is run after the base class mirrorTransformations method and is used to do anything specific that
        a module might need that differs from all the base functionality. In the case of the chain, it needs to change
        some of the values to be negative or positive due to the local rotation axis of the joint movers.

        """
        # get needed data
        networkNode = self.returnNetworkNode
        mirrorModule = cmds.getAttr(networkNode + ".mirrorModule")
        moduleName = cmds.getAttr(networkNode + ".moduleName")
        movers = self.returnJointMovers

        # custom mirroring for chain module
        for moverGrp in movers:
            for mover in moverGrp:
                mirrorMover = mover.replace(moduleName, mirrorModule)
                for attr in [".tz", ".rx", ".ry"]:
                    value = cmds.getAttr(mirrorMover + attr)
                    cmds.setAttr(mirrorMover + attr, value * -1)

        # match the top level groups of the module as well, ensuring that we have a perfect mirror
        topLevelMirrorGrp = cmds.listRelatives(mirrorModule + "_mover_grp", children=True)[0]
        topLevelGrp = cmds.listRelatives(moduleName + "_mover_grp", children=True)[0]
        matrix = om.MMatrix(cmds.getAttr(topLevelGrp + ".worldMatrix"))
        mirrored_matrix = matrix.setElement(3, 0, -matrix[12])

        # get parent inverse matrix of control
        parentMatrix = om.MMatrix(cmds.getAttr(topLevelMirrorGrp + ".parentInverseMatrix"))
        newMatrix = mirrored_matrix * parentMatrix
        transform_matrix = om.MTransformationMatrix(newMatrix)
        translates = transform_matrix.translation(om.MSpace.kWorld)

        # set the mirrored translate values
        cmds.setAttr(topLevelMirrorGrp + ".tx", translates[0])
        cmds.setAttr(topLevelMirrorGrp + ".ty", translates[1])
        cmds.setAttr(topLevelMirrorGrp + ".tz", translates[2])

        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pasteSettings(self):
        """
        Paste the settings from the temp file on disk to the module's network node.

        This function is used in the right-click menu of the module on the skeleton settings interface.
        Occasionally, it is called outside of the menu. For example, when creating a mirror of the module,
        the settings are copied for the source module to then be later pasted on the mirror.

        After settings are pasted, applyModuleChanges is called to update the joint mover in the scene with
        the latest values. updateSettingsUI is also called to update the outliner.
        """
        # it does this 4 times because for some reason it would not grab everything one time through. Investigate
        for i in range(4):

            tempDir = cmds.internalVar(userTmpDir=True)
            clipboardFile = os.path.normcase(os.path.join(tempDir, "ART_clipboard.txt"))

            if os.path.exists(clipboardFile):
                # load the data
                json_file = open(clipboardFile)
                data = json.load(json_file)
                json_file.close()

                # attempt to paste data if module type is the same
                networkNode = self.returnNetworkNode
                moduleType = cmds.getAttr(networkNode + ".moduleType")
                if moduleType == data[0][1]:
                    for each in data:
                        attr = each[0]
                        value = each[1]
                        if attr == "numJoints":
                            self.numJoints.setValue(value)
                        if attr == "controlType":
                            self.jmCtrlShape.setCurrentIndex(value)
                        if attr == "proxyShape":
                            self.proxyShape.setCurrentIndex(value)

            else:
                cmds.warning("No data in clipboard")

        # relaunch the UI
        self.applyModuleChanges(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetSettings(self):
        """
        (Override from base class)
        Reset the settings of the module's network node.

        This function is used in the right-click menu of the module on the skeleton settings interface.

        """

        self.numJoints.setValue(3)
        self.jmCtrlShape.setCurrentIndex(0)
        self.proxyShape.setCurrentIndex(0)

        # relaunch the UI
        self.applyModuleChanges(self)
        self.updateSettingsUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectRigControls(self, mode):
        """
        This method calls on getControls to return a list of the controls and the selects them.

        :param mode: Which controls to select (FK, IK, or all)

        """

        fk_controls = self.getControls(False, "fkControls")
        ik_controls = self.getControls(False, "ikControls")

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        # select the controls
        if mode == "fk":
            for control in fk_controls:
                cmds.select(control, add=True)

        if mode == "ik":
            for control in ik_controls:
                cmds.select(control, add=True)

        if mode == "all":
            for controlGrp in [fk_controls, ik_controls]:
                for control in controlGrp:
                    cmds.select(control, add=True)

        if mode == "settings":
            cmds.select(clear=True)
            cmds.select(namespace + ":" + self.name + "_settings", add=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetRigControls(self, resetAll):
        """
        This method zeroes out control attributes. If resetAll is true, then it will zero out all rig controls for
        the module. Otherwise, it will only zero out the selected controls of the module.

        :param resetAll: Whether or not to reset only the selected controls or all controls of the module.
        """

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        if resetAll:

            # list any attributes on the network node that contain "controls"
            controls = self.getControls()

            # reset the attr on each control
            nonZeroAttrs = ["scale", "globalScale", "scaleX", "scaleY", "scaleZ"]
            skipAttrs = ["sineDropoff", "splineThickness", "showSpline", "showOffsetControls"]

            try:
                for control in controls:
                    for each in control:
                        attrs = cmds.listAttr(each, keyable=True)
                        for attr in attrs:
                            if attr not in nonZeroAttrs:
                                if attr not in skipAttrs:
                                    cmds.setAttr(each + "." + attr, 0)
                            else:
                                cmds.setAttr(each + "." + attr, 1)
            except Exception:
                cmds.warning("skipped " + str(control) + ". No valid controls found to reset.")

        if not resetAll:
            nonZeroAttrs = ["scale", "globalScale", "scaleX", "scaleY", "scaleZ"]
            skipAttrs = ["sineDropoff", "splineThickness", "showSpline", "showOffsetControls"]
            selection = cmds.ls(sl=True)

            for each in selection:
                attrs = cmds.listAttr(each, keyable=True)

                for attr in attrs:
                    if attr not in nonZeroAttrs:
                        if attr not in skipAttrs:
                            cmds.setAttr(each + "." + attr, 0)
                    else:
                        cmds.setAttr(each + "." + attr, 1)

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    #                                                                                                           #
    # # # # # # # # # # # # # #  M O D U L E   S P E C I F I C   M E T H O D S  # # # # # # # # # # # # # # # # #
    #                                                                                                           #
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addChainSegment(self, setupScale=False):
        """
        Adds a new joint mover segment onto the chain module. Called when the number of joints in the chain
        has increased.

        :param setupScale: Whether or not to setup the global scale attributes (so that scaling works with the root)

        """

        # turn renderer to default
        panels = cmds.getPanel(type='modelPanel')
        panelData = []
        for panel in panels:
            modelEditor = cmds.modelPanel(panel, q=True, modelEditor=True)
            renderSetting = cmds.modelEditor(modelEditor, q=True, rnm=True)
            panelData.append([modelEditor, renderSetting])
            cmds.modelEditor(modelEditor, edit=True, rnm="base_OpenGL_Renderer")

        cmds.refresh(force=True)

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # find last segment
        cmds.select(prefix + "chain" + suffix + "*_mover")
        selection = cmds.ls(sl=True)
        for each in selection:
            path = cmds.listRelatives(each, fullPath=True)[0]
            if self.name + "_mover_grp" not in path:
                cmds.select(each, tgl=True)

        movers = cmds.ls(sl=True)
        lastMover = max(movers)

        # find that chain segment number
        last_mover_suffix = lastMover.split(prefix + baseName + suffix)[1]
        number = re.split('\D+', last_mover_suffix)[1]

        # new number (iterate +1)
        newNumber = int(number) + 1
        if len(str(newNumber)) == 1:
            newNumber = str(0) + str(newNumber)

        # duplicate the last joint mover segment nodes, and rename them using the new number
        parentGrp = cmds.listRelatives(lastMover, parent=True)[0]
        duplicates = cmds.duplicate(parentGrp, rc=True)
        cmds.parent(duplicates[0], world=True)

        # rename duplicate
        newSegmentNodes = []
        for each in duplicates:
            # prefix + name + suffix
            replace_string = each.split(prefix + baseName + suffix)[1]

            newName = replace_string.replace(str(number), str(newNumber))
            newName = prefix + baseName + suffix + newName[:-1]
            print newName
            cmds.rename(each, newName)
            newSegmentNodes.append(newName)

        # parent new segment into last segment
        cmds.parent(newSegmentNodes[0], lastMover)

        # parent constrain top level group to lastMover's end node (then delete constraint)
        cmds.select(lastMover, hi=True)
        lastMovers = cmds.ls(sl=True)

        for node in lastMovers:
            if node.find(number + "_mover_end") != -1:
                cmds.delete(cmds.parentConstraint(node, newSegmentNodes[0])[0])

        # setup global scaling, passing in new mover and offset mover
        if setupScale is True:
            self.hookUpMoverGlobalScale([newSegmentNodes[1], newSegmentNodes[2]])

        # set render settings back to what they were
        for each in panelData:
            cmds.modelEditor(each[0], edit=True, rnm=each[1])
        cmds.refresh(force=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeChainSegment(self):
        """
        Removes a segment from the chain module. Called when the number of joints in the chain has been decreased.

        """

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # find last segment
        cmds.select(prefix + "chain" + suffix + "*_mover")
        selection = cmds.ls(sl=True)
        for each in selection:
            path = cmds.listRelatives(each, fullPath=True)[0]
            if self.name + "_mover_grp" not in path:
                cmds.select(each, tgl=True)

        movers = cmds.ls(sl=True)
        lastMover = max(movers)

        # find that chain segment number
        number = re.split('\D+', lastMover)[1]
        parentGrp = cmds.listRelatives(lastMover, parent=True)[0]

        # delete parentGrp
        cmds.delete(parentGrp)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def hookUpMoverGlobalScale(self, movers):
        """
        Hooks up the alias attr for global scale on any newly created chain segments.

        :param movers: List of movers to setup the alias attr on.

        """

        # hook up global scale on joint movers
        try:
            for mover in movers:
                if not cmds.objExists(mover + ".globalScale"):
                    try:
                        cmds.aliasAttr("globalScale", mover + ".scaleZ")
                        cmds.connectAttr(mover + ".globalScale", mover + ".scaleX")
                        cmds.connectAttr(mover + ".globalScale", mover + ".scaleY")
                        cmds.setAttr(mover + ".scaleX", keyable=False)
                        cmds.setAttr(mover + ".scaleY", keyable=False)
                    except Exception:
                        pass
                # lock movers
                for each in movers:
                    for mover in each:
                        cmds.lockNode(mover, lock=True)
        except Exception:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeProxyGeo(self, *args):
        """
        This method is unique to this module and allows the user to change the geometry of the proxy geo. This is purely
        for aesthetic purposes.

        .. seealso:: ART_Chain.skeletonSettings_UI()

        """

        currentSelection = cmds.ls(sl=True)

        # get new proxy geo value from comboBox
        newShape = self.proxyShape.currentText()

        # construct the path
        path = os.path.join(self.toolsPath, "Core/JointMover/controls/")
        fullPath = os.path.join(path, "proxy_chain_" + newShape + ".ma")
        fullPath = utils.returnFriendlyPath(fullPath)

        # get info from network node
        networkNode = self.returnNetworkNode
        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # get name info
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # swap out shapes
        for i in range(int(numJoints)):
            number = ""
            if i < 9:
                number = "0"

            # import the file
            cmds.file(fullPath, i=True, iv=True, type="mayaAscii", rnn=True)

            # assign materials if they exist, removing duplicate materials
            materials = [["*_blue_m", "blue_m"], ["*_green_m", "green_m"], ["*_red_m", "red_m"],
                         ["*_white_m", "white_m"],
                         ["*_proxy_shader_tan", "proxy_shader_tan"], ["*_proxy_shader_black", "proxy_shader_black"]]
            deleteMaterials = []
            for material in materials:
                try:
                    # select materials for the joint mover
                    cmds.select(material[0])
                    foundMaterials = cmds.ls(sl=True)

                    # loop through each color material (dupes)
                    for mat in foundMaterials:
                        cmds.hyperShade(objects=mat)
                        assignedGeo = cmds.ls(sl=True)

                        # select the geo and the original material, and assign
                        originalMaterial = material[1]
                        for geo in assignedGeo:
                            cmds.select([geo, originalMaterial])
                            cmds.hyperShade(assign=originalMaterial)

                        # delete the material no longer needed
                        deleteMaterials.append(mat)
                except Exception, e:
                    print e

            # delete all deleteMaterials
            for mat in deleteMaterials:
                cmds.delete(mat)

            # get current shape node
            currentShape = cmds.listRelatives(prefix + "chain" + suffix + "_" + number + str(i + 1) + "_proxy_geo",
                                              shapes=True)[0]

            # parent and scale constrain new shape transform to existing
            cmds.delete(cmds.parentConstraint(prefix + "chain" + suffix + "_" + number + str(i + 1) + "_proxy_geo",
                                              "proxy_geo")[0])
            cmds.delete(cmds.scaleConstraint(prefix + "chain" + suffix + "_" + number + str(i + 1) + "_proxy_geo",
                                             "proxy_geo")[0])

            # set new shape
            dupeShape = cmds.listRelatives("proxy_geo", shapes=True)[0]
            cmds.parent(dupeShape, prefix + "chain" + suffix + "_" + number + str(i + 1) + "_proxy_geo", r=True,
                        shape=True)

            # delete old shape
            cmds.delete("proxy_geo")
            cmds.delete(currentShape)

            # rename shape node
            newShape = cmds.listRelatives(prefix + "chain" + suffix + "_" + number + str(i + 1) + "_proxy_geo",
                                          shapes=True)[0]
            cmds.rename(newShape, currentShape)

        # apply module changes to write the new shape into the network node
        self.applyModuleChanges(self)

        # re-select selection
        cmds.select(currentSelection)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeControlShape(self, *args):
        """
        This method is unique to this module. It allows the user to change
        the shape of the control object of the joint mover, which also gets used as the control object for the rig.

        .. seealso:: ART_Chain.skeletonSettings_UI()

        """

        currentSelection = cmds.ls(sl=True)

        # get new proxy geo value from comboBox
        newShape = self.jmCtrlShape.currentText()

        # construct the path
        path = os.path.join(self.toolsPath, "Core/JointMover/controls/")
        fullPath = os.path.join(path, "shape_chain_" + newShape + ".ma")
        fullPath = utils.returnFriendlyPath(fullPath)

        # get info from network node
        networkNode = self.returnNetworkNode
        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # get name info
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # swap out shapes
        for i in range(int(numJoints)):
            number = ""
            if i < 9:
                number = "0"

            # import the file
            cmds.file(fullPath, i=True, iv=True, type="mayaAscii", rnn=True)

            # get current shape node
            for mover in ["_mover", "_mover_offset", "_mover_geo"]:
                currentShape = cmds.listRelatives(prefix + "chain" + suffix + "_" + number + str(i + 1) + mover,
                                                  shapes=True)[0]

                newMoverShape = cmds.listRelatives("shape_curve" + mover, children=True)[0]

                cmds.parent(newMoverShape, prefix + "chain" + suffix + "_" + number + str(i + 1) + mover, r=True,
                            shape=True)

                # delete things in scene
                cmds.delete("shape_curve" + mover)
                cmds.delete(currentShape)

                # rename shape
                new = \
                cmds.listRelatives(prefix + "chain" + suffix + "_" + number + str(i + 1) + mover, shapes=True)[0]
                cmds.rename(new, currentShape)

        # refresh UI to capture new mover shapes and set thier visibility
        self.rigUiInst.setMoverVisibility()

        # apply module changes
        self.applyModuleChanges(self)

        # re-select selection
        cmds.select(currentSelection)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getCurrentNumberOfSegments(self):
        """
        Finds the number of chain segments in the scene by finding the highest number in the joint mover hierarchy.

        :return: the highest number found in the chain joint mover hierarchy.

        """

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # find last segment
        cmds.select(prefix + "chain" + suffix + "*_mover")
        selection = cmds.ls(sl=True)
        for each in selection:
            path = cmds.listRelatives(each, fullPath=True)[0]
            if self.name + "_mover_grp" not in path:
                cmds.select(each, tgl=True)

        movers = cmds.ls(sl=True)
        lastMover = max(movers)
        last_mover_suffix = lastMover.split(prefix + baseName + suffix)[1]
        number = re.split('\D+', last_mover_suffix)[1]

        # find that chain segment number
        return int(number)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def hideLastGeo(self):
        """
        Hides the last joint-in-the-chain's proxy geo to avoid confusion with regards to chain segments.

        """

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # find last segment
        cmds.select(prefix + "chain" + suffix + "*_proxy_geo")
        selection = cmds.ls(sl=True)
        for each in selection:
            cmds.setAttr(each + ".visibility", lock=False)
            cmds.setAttr(each + ".visibility", 1, lock=True)
            path = cmds.listRelatives(each, fullPath=True)[0]
            if self.name + "_mover_grp" not in path:
                cmds.select(each, tgl=True)

        movers = cmds.ls(sl=True)
        lastMover = max(movers)
        cmds.setAttr(lastMover + ".visibility", lock=False)
        cmds.setAttr(lastMover + ".visibility", 0, lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildFkRig(self, textEdit, uiInst, builtRigs, networkNode):
        """
        Builds the FK rig for the chain.

        :param textEdit: The textEdit widget to post status updates to
        :param uiInst:  The Rig Creator ui instance
        :param builtRigs: How many rigs have been built so far
        :param networkNode: The network node of the module

        :return: Returns the top-level FK node to be parented into the rig.

        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Starting FK Chain Rig Build..")

        # build the rig
        slot = len(builtRigs)

        # find the joints in the module that need rigging
        joints = self.returnCreatedJoints
        fkControls = []
        self.topNode = None

        for joint in joints:
            if joint == joints[0]:
                data = riggingUtils.createControlFromMover(joint, networkNode, True, True)

                fkControl = cmds.rename(data[0], "fk_" + joint + "_anim")
                animGrp = cmds.rename(data[1], "fk_" + joint + "_anim_grp")
                spaceSwitcher = cmds.rename(data[2], "fk_" + joint + "_anim_space_switcher")
                spaceSwitchFollow = cmds.rename(data[3], "fk_" + joint + "_anim_space_switcher_follow")
                self.topNode = spaceSwitchFollow

                fkControls.append([spaceSwitchFollow, fkControl, joint])
                # color the control
                riggingUtils.colorControl(fkControl, 18)

            else:
                data = riggingUtils.createControlFromMover(joint, networkNode, True, False)

                fkControl = cmds.rename(data[0], "fk_" + joint + "_anim")
                animGrp = cmds.rename(data[1], "fk_" + joint + "_anim_grp")

                fkControls.append([animGrp, fkControl, joint])

                # color the control
                riggingUtils.colorControl(fkControl, 18)

        # create hierarchy
        fkControls.reverse()

        for i in range(len(fkControls)):
            try:
                cmds.parentConstraint(fkControls[i + 1][1], fkControls[i][0], mo=True)
                cmds.parent(fkControls[i][0], self.topNode)
            except IndexError:
                pass

        # =======================================================================
        # #lastly, connect controls up to blender nodes to drive driver joints
        # =======================================================================
        for each in fkControls:
            control = each[1]
            joint = each[2]

            cmds.pointConstraint(control, "driver_" + joint, mo=True)
            cmds.orientConstraint(control, "driver_" + joint)

            # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale
            # into input 2, and plugs that into driver joint
            if cmds.objExists("master_anim"):
                globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=joint + "_globalScale")
                cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
                cmds.connectAttr(control + ".scale", globalScaleMult + ".input2")
                riggingUtils.createConstraint(globalScaleMult, "driver_" + joint, "scale", False, 2, slot, "output")
            else:
                riggingUtils.createConstraint(control, "driver_" + joint, "scale", False, 2, slot)

        # #=======================================================================
        # clean up
        # #=======================================================================
        cmds.parent(self.topNode, self.chainCtrlGrp)

        # lock attrs
        for each in fkControls:
            control = each[1]
            for attr in [".visibility"]:
                cmds.setAttr(control + attr, lock=True, keyable=False)

            # remove the global scale alias attr
            cmds.aliasAttr(control + ".globalScale", remove=True)

        fkRigData = []
        for each in fkControls:
            fkRigData.append(each[1])

        # get controlNode
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        # add fk controls to control node
        if not cmds.objExists(controlNode + ".fkControls"):
            cmds.addAttr(controlNode, sn="fkControls", at="message")

        # add proxy attributes for mode
        if cmds.objExists(self.chainSettings + ".mode"):
            for node in fkRigData:
                cmds.addAttr(node, ln="mode", proxy=self.chainSettings + ".mode", at="double", keyable=True)

        for node in fkRigData:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".fkControls", node + ".controlClass")

            # add controlType info
            cmds.addAttr(node, ln="controlType", dt="string")
            cmds.setAttr(node + ".controlType", "FK", type="string")

        cmds.addAttr(fkRigData[-1], ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
        cmds.setAttr(fkRigData[-1] + ".hasSpaceSwitching", lock=True)
        cmds.addAttr(fkRigData[-1], ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
        cmds.setAttr(fkRigData[-1] + ".canUseRotationSpace", lock=True)
        cmds.addAttr(fkRigData[-1], ln="canUseTranslationSpace", at="bool", dv=0, keyable=False)
        cmds.setAttr(fkRigData[-1] + ".canUseTranslationSpace", lock=True)

        # update progress
        if textEdit is not None:
            textEdit.setTextColor(QtGui.QColor(0, 255, 18))
            textEdit.append("        SUCCESS: FK Build Complete!")
            textEdit.setTextColor(QtGui.QColor(255, 255, 255))

        return [self.topNode]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildIkRig(self, textEdit, uiInst, builtRigs, networkNode):
        """
        Builds the IK Ribbon Rig for the chain module.

        :param textEdit: The textEdit widget to post status updates to
        :param uiInst: The Rig Creator ui instance
        :param builtRigs: How many rigs have been built so far
        :param networkNode:The network node of the module

        :return: Returns the top-level IK node(s) to be parented into the rig.

        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Starting IK Chain Rig Build..")

        # get joints
        joints = self.returnCreatedJoints

        # get controlNode
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        # build ribbon
        ribbon = self._createIkRibbon(joints)
        sineSurface = cmds.duplicate(ribbon, name=self.name + "_ribbon_sine_surface")[0]

        # assign hair to the ribbon to get follicles
        hairGrp = self._createRibbonHair(ribbon, joints)

        # find out the number of chain segments
        chainSegments = len(joints) - 1
        lastGood = 1
        validNumbers = []

        # determine the proper spacing for the main IK controls
        for i in range(1, 12):
            if float(chainSegments) % float(i) == 0:
                if chainSegments - i != 0:
                    lastGood = i
                    validNumbers.append(i)

        # if there are more than 2 valid numbers (numbers that the amount of chainSegments is divisible by), get the
        # 2nd largest. (so if you have 16 segments, your numbers would be 1, 2, 4, and 8. 8 would only give us 3 IK
        # controls, so we'll take 4 instead, to have more IK controls.
        if len(validNumbers) >= 2:
            lastGood = validNumbers[-2]

        #
        #
        #
        # create nurbs curve along joint chain using distribution (wire curve)
        pts = []
        wireJnts = []
        offsetJnts = []
        for i in range(len(joints)):
            if float(i) % float(lastGood) == 0:
                wireJnts.append(joints[i])
            else:
                offsetJnts.append(joints[i])
            pos = cmds.xform(joints[i], q=True, ws=True, t=True)
            pts.append(pos)

        if len(pts) <= 3:
            wire = cmds.curve(d=1, p=pts, name=self.name + "_ribbon_wire_curve")
        else:
            wire = cmds.curve(d=3, p=pts, name=self.name + "_ribbon_wire_curve")
        wireShape = cmds.listRelatives(wire, shapes=True)[0]

        #
        #
        #
        # create skinning joints for wire nurbs curve
        wireSkinJnts = []
        x = 1
        for joint in wireJnts:
            # duplicate joint
            jnt = cmds.duplicate(joint, po=True, name=self.name + "_wire_jnt_" + str(x))[0]
            cmds.setAttr(jnt + ".visibility", 0, lock=True)
            wireSkinJnts.append(jnt)

            # parent to world
            cmds.parent(jnt, world=True)
            x += 1

        #
        #
        #
        # skin wire curve
        cmds.select(wireSkinJnts)
        cmds.select(wire, add=True)
        cmds.skinCluster(tsb=True, maximumInfluences=4, obeyMaxInfluences=True, bindMethod=0, skinMethod=0,
                         normalizeWeights=True)

        #
        #
        #
        # create control objects for wire joints
        ikMacroControls = []

        x = 1
        for jnt in wireJnts:
            data = riggingUtils.createControlFromMover(jnt, networkNode, True, True)

            # rename control nodes
            sep = "_0"
            if x > 9:
                sep = "_"
            ikControl = cmds.rename(data[0], "ik_" + self.name + sep + str(x) + "_anim")
            animGrp = cmds.rename(data[1], "ik_" + self.name + sep + str(x) + "_anim_grp")
            spaceSwitcher = cmds.rename(data[2], "ik_" + self.name + sep + str(x) + "_anim_space_switcher")
            spaceSwitchFollow = cmds.rename(data[3], "ik_" + self.name + sep + str(x) + "_anim_space_switcher_follow")
            ikMacroControls.append([spaceSwitchFollow, ikControl, jnt])

            # scale ikControl up a bit
            cmds.setAttr(ikControl + ".scaleX", 1.5)
            cmds.setAttr(ikControl + ".scaleY", 1.5)
            cmds.setAttr(ikControl + ".scaleZ", 1.5)
            cmds.makeIdentity(ikControl, t=0, r=0, s=1, apply=True)

            # parent skin joint under control
            cmds.parent(wireSkinJnts[x - 1], ikControl)
            x += 1

        #
        #
        #
        # add wire deformer from nurbs curve (wire) to ribbon
        cmds.select([ribbon, wire])
        wireDeformer = cmds.wire(ribbon, w=wire, gw=False, en=1.0, ce=0.0, li=0.0, name=self.name + "_ribbon_wire_deformer")[0]
        cmds.setAttr(wireDeformer + ".dropoffDistance[0]", 50)
        cmds.setAttr(wireDeformer + ".rotation", 0)

        #
        #
        #
        # get follow options on main middle controls (to follow start/end) option.
        followCtrls = []
        for ctrl in ikMacroControls:
            if ctrl is not ikMacroControls[0]:
                if ctrl is not ikMacroControls[-1]:
                    followCtrls.append(ctrl[1])

        followSpaces = []
        for i in range(len(followCtrls)):
            # create empty group to receive constraints
            grp = cmds.group(empty=True, name=followCtrls[i] + "_follow_space")
            followSpaces.append(grp)
            cmds.delete(cmds.parentConstraint(followCtrls[i], grp)[0])
            pConst = cmds.pointConstraint([ikMacroControls[0][1], ikMacroControls[-1][1]], grp, mo=True)[0]

            # create a follow group and put it under the follow anim grp
            followAnimGrp = cmds.listRelatives(followCtrls[i], parent=True)[0]
            spaceSwitchGrp = cmds.listRelatives(followAnimGrp, parent=True)[0]
            followGrp = cmds.group(empty=True, name=followAnimGrp.replace("anim_grp", "follow_grp"))
            cmds.delete(cmds.parentConstraint(followAnimGrp, followGrp)[0])
            cmds.parent(followGrp, spaceSwitchGrp)

            # constrain the follow group to the grp (so there is only 1 weight).
            constraint = cmds.pointConstraint(grp, followGrp, mo=True)[0]

            # add follow attribute to control
            cmds.addAttr(followCtrls[i], ln="follow", min=0, max=1, dv=0, keyable=True)

            # create blend colors node, where color1 is the followGrp's translate values. color2 is 0,0,0. blender will
            # connect to the follow attribute on the control
            blend = cmds.shadingNode("blendColors", asUtility=True, name=followCtrls[i].replace("_anim", "_blendColors"))
            cmds.connectAttr(followGrp + ".translate", blend + ".color1")
            cmds.connectAttr(followCtrls[i] + ".follow", blend + ".blender")
            cmds.connectAttr(blend + ".output", followAnimGrp + ".translate")

        #
        #
        #
        # get offset controls created (off of follicle joints)
        x = 1
        offsetCtrls = []
        for jnt in offsetJnts:
            follicleJnt = "follicle_" + jnt
            follicle = cmds.listRelatives(follicleJnt, parent=True)[0]

            # create a control for that joint
            data = riggingUtils.createControlFromMover(jnt, networkNode, True, False)

            # rename control nodes
            ctrl = cmds.rename(data[0], "ik_" + jnt + "_offset_anim")
            grp = cmds.rename(data[1], "ik_" + jnt + "_offset_anim_grp")
            offsetCtrls.append(grp)

            cmds.setAttr(ctrl + ".overrideEnabled", 1)
            cmds.setAttr(ctrl + ".overrideColor", 18)

            # parent grp under the follicle
            cmds.parent(grp, follicle)

            # parent the follicleJnt under the ctrl
            cmds.parent(follicleJnt, ctrl)
            for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
                cmds.setAttr(follicleJnt + attr, 0)

        #
        #
        #
        # add sine wave deformer setup and attributes
        cmds.setAttr(sineSurface + ".v", 0, lock=True)

        sineNodes = cmds.nonLinear(sineSurface, type='sine')
        sineHandle = sineNodes[1]
        sineDeformer = sineNodes[0]
        cmds.setAttr(sineHandle + ".v", 0, lock=True)

        # place sine deformer
        bounds = cmds.exactWorldBoundingBox(ribbon)
        scaleVal = max([bounds[3] - bounds[0], bounds[4] - bounds[1], bounds[5] - bounds[2]])
        scaleVal = scaleVal/2

        cmds.setAttr(sineHandle + ".sx", scaleVal)
        cmds.setAttr(sineHandle + ".sy", scaleVal)
        cmds.setAttr(sineHandle + ".sz", scaleVal)

        cmds.delete(cmds.pointConstraint(ribbon, sineHandle)[0])

        sineDirection = self._getFacingDirection(sineHandle)
        surfaceDirection = self._getFacingDirection(ribbon)

        sineGrp = cmds.group(empty=True, n=self.name + "_sine_grp")
        cmds.delete(cmds.pointConstraint(sineHandle, sineGrp)[0])
        cmds.parent(sineHandle, sineGrp)

        if sineDirection != surfaceDirection:
            aim = (1, 0, 0)
            if sineDirection == "Y":
                aim = (0, 1, 0)
            if sineDirection == "Z":
                aim = (1, 0, 0)

            cmds.delete(cmds.aimConstraint(ikMacroControls[-1][1], sineGrp, aimVector=aim, upVector=(0, 0, 1),
                                           worldUpType="scene")[0])

        # add sine deformer attrs
        cmds.addAttr(ikMacroControls[-1][1], ln="sineSep", nn="------------", at="enum", en="Sine::", keyable=True)
        cmds.addAttr(ikMacroControls[-1][1], ln="amplitude", keyable=True)
        cmds.addAttr(ikMacroControls[-1][1], ln="offset", keyable=True)
        cmds.addAttr(ikMacroControls[-1][1], ln="sineTwist", keyable=True)
        cmds.addAttr(ikMacroControls[-1][1], ln="sineDropoff", min=0, max=1, dv=1, keyable=True)

        cmds.connectAttr(ikMacroControls[-1][1] + ".amplitude", sineDeformer + ".amplitude")
        cmds.connectAttr(ikMacroControls[-1][1] + ".offset", sineDeformer + ".offset")
        cmds.connectAttr(ikMacroControls[-1][1] + ".sineDropoff", sineDeformer + ".dropoff")
        cmds.connectAttr(ikMacroControls[-1][1] + ".sineTwist", sineHandle + ".ry")

        # add blendshape of deformer surface to ribbon
        cmds.select(sineSurface)
        cmds.select(ribbon, add=True)
        blendshape = cmds.blendShape(n=self.name + "_ribbon_shapes")[0]
        cmds.setAttr(blendshape + "." + sineSurface, 1)
        cmds.reorderDeformers(wireDeformer, blendshape, ribbon)

        #
        #
        #
        # create a list of our follicle joints and setup aiming between them
        # get the follicle joints under the hair grp
        children = cmds.listRelatives(hairGrp, ad=True)
        follicleJnts = []
        for child in children:
            if cmds.nodeType(child) == "joint":
                follicleJnts.append(child)

        # make sure follicle joints are aiming at each other
        follicleJnts.reverse()
        for i in range(len(follicleJnts)):
            try:
                cmds.aimConstraint(follicleJnts[i], follicleJnts[i + 1], aimVector=[1, 0, 0], upVector=[0, 1, 0],
                                   worldUpType="vector", worldUpVector=[0, 0, 1], skip=["x"])
            except IndexError:
                pass
        follicleJnts.reverse()

        #
        #
        #
        # setup twist on IK
        ikStartTwist = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_ik_start_twist_mult")
        ikEndTwist = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_ik_end_twist_mult")

        cmds.connectAttr(ikMacroControls[0][1] + ".rx", ikStartTwist + ".input1X")
        cmds.setAttr(ikStartTwist + ".input2X", chainSegments)
        cmds.setAttr(ikStartTwist + ".operation", 2)

        cmds.connectAttr(ikMacroControls[-1][1] + ".rx", ikEndTwist + ".input1X")
        cmds.setAttr(ikEndTwist + ".input2X", chainSegments)
        cmds.setAttr(ikEndTwist + ".operation", 2)

        follow_ctrls_tmp = list(followCtrls)
        offset_ctrls_tmp = list(offsetCtrls)
        twistControls = [ikMacroControls[0][1]]

        for i in range(len(joints)):
            if float(i) % float(lastGood) == 0:
                if i != 0 and i != len(joints):
                    try:
                        twistControls.append(follow_ctrls_tmp[0])
                        follow_ctrls_tmp.pop(0)
                    except Exception, e:
                        print str(e)
            else:
                try:
                    ctrl = cmds.listRelatives(offset_ctrls_tmp[0], children=True)[0]
                    twistControls.append(ctrl)
                    offset_ctrls_tmp.pop(0)
                except Exception, e:
                    print str(e)
        twistControls.append(ikMacroControls[-1][1])

        counterDown = chainSegments
        counterUp = 1
        counter = 0
        for twistCtrl in twistControls:
            # create an add node and two mult nodes
            addNode = cmds.shadingNode("plusMinusAverage", asUtility=True, name=twistCtrl + "_addNode")
            multNode1 = cmds.shadingNode("multiplyDivide", asUtility=True, name=twistCtrl + "_multNodeSJ")
            multNode2 = cmds.shadingNode("multiplyDivide", asUtility=True, name=twistCtrl + "_multNodeEE")

            # connect the ikStartTwist outputX into both mult nodes and set input2X to be the appropriate number
            cmds.connectAttr(ikStartTwist + ".outputX", multNode1 + ".input1X")
            cmds.setAttr(multNode1 + ".input2X", counterDown)
            cmds.connectAttr(ikEndTwist + ".outputX", multNode2 + ".input1X")
            cmds.setAttr(multNode2 + ".input2X", counterUp)
            counterDown -= 1
            counterUp += 1

            # plug in the twist control.rx, and both mult node outputs into the addNode
            cmds.connectAttr(twistCtrl + ".rotateX", addNode + ".input1D[0]")
            if twistCtrl == ikMacroControls[0][1]:
                cmds.connectAttr(multNode2 + ".outputX", addNode + ".input1D[1]")
            if twistCtrl == ikMacroControls[-1][1]:
                cmds.connectAttr(multNode1 + ".outputX", addNode + ".input1D[1]")
            if twistCtrl != ikMacroControls[0][1]:
                if twistCtrl != ikMacroControls[-1][1]:
                    cmds.connectAttr(multNode1 + ".outputX", addNode + ".input1D[1]")
                    cmds.connectAttr(multNode2 + ".outputX", addNode + ".input1D[2]")

            # connect to the follicle joint
            cmds.connectAttr(addNode + ".output1D", follicleJnts[counter] + ".rotateX")

            # add attr to easily find out which follicle joint this control drives
            try:
                cmds.addAttr(twistCtrl, ln="drivesJoint", at="message")
                cmds.addAttr(follicleJnts[counter], ln="drivenBy", at="message")
                cmds.connectAttr(twistCtrl + ".drivesJoint", follicleJnts[counter] + ".drivenBy")
            except IndexError, e:
                print str(e)
                print "\nPASSED"

            counter += 1

        #
        #
        #
        # setup segment scale working on ribbon segments
        distanceNodes = []
        for i in range(len(follicleJnts)):
            if i < (len(follicleJnts) - 1):
                self._setupSegmentScale(follicleJnts[i], follicleJnts[i+1], distanceNodes)

        #
        #
        #
        # Get spline representation setup
        cmds.addAttr(ikMacroControls[-1][1], ln="splineSep", nn="------------", at="enum", en="Spline::", keyable=True)
        cmds.addAttr(ikMacroControls[-1][1], ln="showSpline", at="bool", dv=0, keyable=True)
        cmds.addAttr(ikMacroControls[-1][1], ln="splineThickness", min=0.0, max=10.0, dv=0.25, keyable=True)

        # create the spline
        pts = []

        for i in range(len(follicleJnts)):
            pos = cmds.xform(follicleJnts[i], q=True, ws=True, t=True)
            pts.append(pos)

        if len(pts) <= 3:
            splineRep = cmds.curve(d=1, p=pts, name=self.name + "_spline_representation")
        else:
            splineRep = cmds.curve(d=3, p=pts, name=self.name + "_spline_representation")

        # skin the spline to the follicle joints
        cmds.select(follicleJnts)
        cmds.select(splineRep, add=True)
        cmds.skinCluster(tsb=True, maximumInfluences=1, obeyMaxInfluences=True, bindMethod=0, skinMethod=0,
                         normalizeWeights=True)

        # add thickness to the spline with paintFX
        brushData = utils.convertCurvesToStrokes(splineRep)
        cmds.connectAttr(ikMacroControls[-1][1] + ".showSpline", brushData[0] + ".visibility")
        cmds.connectAttr(ikMacroControls[-1][1] + ".splineThickness", brushData[1] + ".brushWidth")

        cmds.setAttr(splineRep + ".overrideEnabled", 1)
        cmds.setAttr(splineRep + ".overrideDisplayType", 2)

        #
        #
        #
        # create a new joint chain that will be driven by the rig
        dupeJoints = cmds.duplicate(joints[0], rc=True)
        cmds.parent(dupeJoints[0], world=True)

        ikJoints = []
        num = 1
        for ikJnt in dupeJoints:
            sep = "_0"
            if num > 9:
                sep = "_"
            newJoint = cmds.rename(ikJnt, self.name + "_ik_chain" + sep + str(num))
            ikJoints.append(newJoint)
            num += 1

        #
        #
        #
        # Constrain the duplicated joint chain to the IK rig.
        for i in range(len(follicleJnts)):
            cmds.pointConstraint(follicleJnts[i], ikJoints[i], mo=True)
            cmds.orientConstraint(follicleJnts[i], ikJoints[i], mo=True)
            try:
                multNode = distanceNodes[i][0]
                cmds.connectAttr(multNode + ".outputX", ikJoints[i] + ".scaleX")

            except IndexError:
                pass

        # #
        # #
        # #
        # # Constrain the driver joints to the duplicated joint chain.
        print "IK ERROR SECTION:"
        print self.name
        print len(ikJoints)
        print len(joints)
        print ikJoints
        print joints

        for i in range(len(ikJoints)):
            print i

            cmds.pointConstraint(ikJoints[i], "driver_" + joints[i], mo=True)
            cmds.orientConstraint(ikJoints[i], "driver_" + joints[i])

            # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale
            # into input 2, and plugs that into driver joint
            if cmds.objExists("master_anim"):
                globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=joints[i] + "_globalScale")
                # the global scale mult changes below are unique to the chain due to the distance nodes,
                # which track world-space for the scaleX. So scaleX for the master anim can be ignored when figuring
                # out global scale.
                cmds.setAttr(globalScaleMult + ".input1X", 1)
                cmds.connectAttr("master_anim.scaleY", globalScaleMult + ".input1Y")
                cmds.connectAttr("master_anim.scaleZ", globalScaleMult + ".input1Z")
                cmds.connectAttr(ikJoints[i] + ".scale", globalScaleMult + ".input2")
                riggingUtils.createConstraint(globalScaleMult, "driver_" + joints[i], "scale", False, 2, 1, "output")
            else:
                riggingUtils.createConstraint(ikJoints[i], "driver_" + joints[i], "scale", False, 2, 1)

        print "END IK ERROR SECTION"
        #
        #
        #
        # Clean up attrs on controls
        for each in offsetCtrls:
            ctrl = cmds.listRelatives(each, children=True)[0]
            cmds.aliasAttr(ctrl + ".globalScale", remove=True)
            cmds.setAttr(ctrl + ".scaleX", lock=True, keyable=False)
            cmds.setAttr(ctrl + ".scaleY", lock=True, keyable=False)
            cmds.setAttr(ctrl + ".scaleZ", lock=True, keyable=False)
            cmds.setAttr(ctrl + ".visibility", lock=True, keyable=False)

        for each in ikMacroControls:
            ctrl = each[1]
            cmds.aliasAttr(ctrl + ".globalScale", remove=True)
            cmds.setAttr(ctrl + ".scaleY", lock=True, keyable=False)
            cmds.setAttr(ctrl + ".scaleZ", lock=True, keyable=False)
            cmds.setAttr(ctrl + ".visibility", lock=True, keyable=False)

        #
        #
        #
        # Clean up outliner
        ribbon_grp = cmds.group(empty=True, name=self.name + "_ribbon_grp")
        cmds.parent([ribbon, sineSurface], ribbon_grp)
        cmds.setAttr(ribbon_grp + ".visibility", 0)

        crv1 = cmds.listConnections(wireDeformer + ".deformedWire[0]")[0]
        crv2 = cmds.listConnections(wireDeformer + ".baseWire[0]")[0]
        curve_grp = cmds.group(empty=True, name=self.name + "_curve_grp")
        cmds.parent([crv1, crv2, splineRep], curve_grp)
        cmds.setAttr(curve_grp + ".visibility", 0)

        ik_ctrl_grp = cmds.group(empty=True, name=self.name + "_ik_ctrl_grp")
        for each in ikMacroControls:
            cmds.parent(each[0], ik_ctrl_grp)
        cmds.parent(ikJoints[0], ik_ctrl_grp)

        deformers_grp = cmds.group(empty=True, name=self.name + "_deformers_grp")
        cmds.setAttr(deformers_grp + ".visibility", 0)
        cmds.parent([sineGrp], deformers_grp)

        distance_grp = cmds.group(empty=True, name=self.name + "_distance_grp")
        cmds.setAttr(distance_grp + ".visibility", 0)
        for each in distanceNodes:
            cmds.parent(each[2], distance_grp)

        dnt_grp = cmds.group(empty=True, name=self.name + "_dnt_grp")
        stroke = cmds.rename(brushData[0], self.name + "_spline_rep_stroke")
        cmds.setAttr(hairGrp + ".visibility", 0)
        cmds.parent([hairGrp, stroke], dnt_grp)
        for each in followSpaces:
            cmds.parent(each, dnt_grp)

        self.ik_grp = cmds.group(empty=True, name=self.name + "_ik_chain_grp")
        cmds.parent([ribbon_grp, curve_grp, deformers_grp, distance_grp, dnt_grp], self.ik_grp)
        cmds.parent(self.ik_grp, self.chainGroup)
        cmds.parent(ik_ctrl_grp, self.chainCtrlGrp)

        # return nodes to hide when IK mode is off.
        returnData = []
        for each in ikMacroControls:
            returnData.append(each[0])
        returnData.extend(offsetCtrls)

        # hide joints
        cmds.setAttr(ikJoints[0] + ".visibility", 0, lock=True)

        # hide follicles
        follicles = cmds.listRelatives(hairGrp, children=True)
        for follicle in follicles:
            shape = cmds.listRelatives(follicle, shapes=True)[0]
            cmds.setAttr(shape + ".visibility", 0, lock=True)

        # add attr for toggling ik offset control visiblity
        cmds.addAttr(ikMacroControls[-1][1], ln="showOffsetControls", at="bool", dv=0, keyable=True)
        cmds.connectAttr(ikMacroControls[-1][1] + ".showOffsetControls", hairGrp + ".visibility")

        # add ik controls to control node
        if not cmds.objExists(controlNode + ".ikControls"):
            cmds.addAttr(controlNode, sn="ikControls", at="message")
        for node in twistControls:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".ikControls", node + ".controlClass")

            # add controlType info
            cmds.addAttr(node, ln="controlType", dt="string")
            cmds.setAttr(node + ".controlType", "IK", type="string")

            # mirroring attrs
            for attr in ["invertX", "invertY", "invertZ"]:
                if not cmds.objExists(node + "." + attr):
                    cmds.addAttr(node, ln=attr, at="bool")
            cmds.setAttr(node + ".invertZ", 1)

        # add proxy attributes for mode
        if cmds.objExists(self.chainSettings + ".mode"):
            for node in twistControls:
                cmds.addAttr(node, ln="mode", proxy=self.chainSettings + ".mode", at="double", keyable=True)

        for each in ikMacroControls:
            node = each[1]
            cmds.addAttr(node, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".hasSpaceSwitching", lock=True)
            cmds.addAttr(node, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".canUseRotationSpace", lock=True)
            cmds.addAttr(node, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".canUseTranslationSpace", lock=True)

        # update progress
        if textEdit is not None:
            textEdit.setTextColor(QtGui.QColor(0, 255, 18))
            textEdit.append("        SUCCESS: IK Build Complete!")
            textEdit.setTextColor(QtGui.QColor(255, 255, 255))

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _createIkRibbon(self, joints):
        """
        Create a nurbs surface by lofting two curves which were created by snapping to each joint position in the chain
        hierarchy.
        This ribbon will have follicles added to it that will be used to drive the joints.

        :param joints: a list of the joints in the chain, which is passed in so that 2 nurbs curves can be created at
        their positions.
        :return: return the created nurbs surface

        """

        # get number of joints
        numJnts = len(joints)

        # get segment length
        segmentLength = cmds.getAttr(joints[1] + ".translateX")

        points = []
        # need to get world position for curve points. going to offset the aim axis point halfway so the follicle is
        # on the joint
        for jnt in joints:
            pos = cmds.xform(jnt, q=True, ws=True, t=True)
            points.append(pos)

        # create a curve
        crv1 = cmds.curve(d=3, p=points)
        cmds.parent(crv1, joints[0])
        cmds.makeIdentity(crv1, t=1, r=1, s=1, apply=True)

        # duplicate the curve
        crv2 = cmds.duplicate(crv1)[0]

        # move curves in width axis
        cmds.setAttr(crv1 + ".translateZ", abs(segmentLength / 2) * -1)
        cmds.setAttr(crv2 + ".translateZ", abs(segmentLength / 2))

        cmds.parent(crv1, world=True)
        cmds.parent(crv2, world=True)

        # rebuild the curves
        crv1 = cmds.rebuildCurve(crv1, ch=True, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=numJnts, d=3, tol=0.01)[0]
        crv2 = cmds.rebuildCurve(crv2, ch=True, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=numJnts, d=3, tol=0.01)[0]

        # loft the curves to create our ribbon
        ribbon = cmds.loft(crv1, crv2, ch=True, rn=False, ar=True, rsn=True, d=3, ss=1, u=1, c=False, po=0,
                           name=self.name + "_ribbon_surface")[0]
        cmds.xform(ribbon, cp=True)

        # delete loft curves
        cmds.delete([crv1, crv2])
        return ribbon

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _createRibbonHair(self, ribbon, joints):
        """
        Take the passed in ribbon nurbs surface and add hair follicles (1 for each joint) to the ribbon.

        :param ribbon: the nurbs surface to add the follicles to
        :param joints: the list of joints in the chain that each created follicle will control
        :return: return the hair group which contains all of the hair follicles, and follicle joints under each follicle

        """

        hairGrp = cmds.group(empty=True, name=self.name + "_ribbon_follicles_grp")

        # create follicles
        for i in range(len(joints)):
            follicle = cmds.createNode("follicle")
            follicleTransform = cmds.listRelatives(follicle, parent=True)[0]
            follicleTransform = cmds.rename(follicleTransform, self.name + "_ribbon_follicle_0" + str(i + 1))
            follicle = cmds.listRelatives(follicleTransform, shapes=True)[0]

            # create joint under follicle
            follicleJnt = cmds.duplicate(joints[i], po=True, name="follicle_" + joints[i])[0]
            cmds.setAttr(follicleJnt + ".visibility", 0, lock=True)
            cmds.parent(follicleJnt, world=True)
            constraint = cmds.pointConstraint(follicleTransform, follicleJnt)[0]
            cmds.delete(constraint)
            cmds.parent(follicleJnt, follicleTransform, r=True)

            # connect follicle to ribbon
            ribbonShape = cmds.listRelatives(ribbon, shapes=True)[0]
            cmds.connectAttr(ribbonShape + ".worldMatrix[0]", follicle + ".inputWorldMatrix")
            cmds.connectAttr(ribbonShape + ".local", follicle + ".inputSurface")
            cmds.connectAttr(follicle + ".outRotate", follicleTransform + ".rotate")
            cmds.connectAttr(follicle + ".outTranslate", follicleTransform + ".translate")

            # orient follicle joint
            cmds.delete(cmds.orientConstraint(joints[i], follicleJnt)[0])
            cmds.makeIdentity(follicleJnt, t=1, r=1, s=1, apply=True)

            # set UV parameters based on # joints
            spansUV = cmds.getAttr(ribbonShape + ".spansUV")[0]
            maxSpans = max(spansUV)

            if spansUV[0] == maxSpans:
                cmds.setAttr(follicle + ".parameterV", 0.5)
                self._moveHairFollicle(joints[i], follicle, "parameterU")

            if spansUV[1] == maxSpans:
                cmds.setAttr(follicle + ".parameterU", 0.5)
                self._moveHairFollicle(joints[i], follicle, "parameterV")

            cmds.parent(follicleTransform, hairGrp)
        return hairGrp

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _moveHairFollicle(self, joint, follicle, parameter):
        """
        Adjusts the hair follicle's parameter (U or V) to line up with the given joint.

        :param joint: The joint the follicle needs to line up with
        :param follicle: The follicle that will be manipulated to line up with the above joint
        :param parameter: Whether or not to manipulate the U or V parameter.

        """

        # create distanceDimension node
        distanceNode = cmds.createNode("distanceDimShape")

        # create a decompose matrix node for the joint and follicle
        jointMatrix = cmds.createNode("decomposeMatrix")
        follicleMatrix = cmds.createNode("decomposeMatrix")

        # hook in joint and follicle world matrix into respective decompose matrix node
        cmds.connectAttr(joint + ".worldMatrix[0]", jointMatrix + ".inputMatrix")
        cmds.connectAttr(follicle + ".worldMatrix[0]", follicleMatrix + ".inputMatrix")

        # use the output translate of those to plug into start and end point of distance node
        cmds.connectAttr(jointMatrix + ".outputTranslate", distanceNode + ".startPoint")
        cmds.connectAttr(follicleMatrix + ".outputTranslate", distanceNode + ".endPoint")

        # increment follicle.parameter until distance is < 1
        cmds.setAttr(follicle + "." + parameter, 0)

        for i in range(1001):
            distance = cmds.getAttr(distanceNode + ".distance")
            if distance > 1:
                value = cmds.getAttr(follicle + "." + parameter)
                cmds.setAttr(follicle + "." + parameter, value + .001)
                newDist = cmds.getAttr(distanceNode + ".distance")
                if newDist > distance:
                    break

            if distance < 1.5:
                break

        # delete distance node
        cmds.delete(cmds.listRelatives(distanceNode, parent=True)[0])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getFacingDirection(self, obj):
        """
        Given the passed in object, find the facing vector (the aim vector) by getting the object's min and max bounds,
        subtracting those vectors, then normalizing the result, returning the largest of the 3 values.

        :param obj: The object whose bounds will be found to calculate the facing direction
        :return: return the facing direction (X, Y, or Z)

        """

        bounds = cmds.exactWorldBoundingBox(obj)
        v1 = om.MVector(bounds[0], bounds[1], bounds[2])
        v2 = om.MVector(bounds[3], bounds[4], bounds[5])
        vec = v2 - v1
        vec = vec.normalize()
        direction = max(vec)

        if vec[0] == direction:
            return "X"
        if vec[1] == direction:
            return "Y"
        if vec[2] == direction:
            return "Z"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _setupSegmentScale(self, jnt1, jnt2, nodesList):
        """
        Sets up the nodes needed for joint scaling on the ribbon rig by creating distance nodes between 2 joints.

        :param jnt1: First joint to be used as a start point in the distance node
        :param jnt2: Second joint to be used as an end point in the distance node
        :param nodesList: List to add created nodes to

        """

        # create distanceDimension node
        distanceNode = cmds.createNode("distanceDimShape")
        cmds.setAttr(distanceNode + ".visibility", 0)

        # create a decompose matrix node for the joint and follicle
        jnt1Matrix = cmds.createNode("decomposeMatrix")
        jnt2Matrix = cmds.createNode("decomposeMatrix")

        # hook in joint and follicle world matrix into respective decompose matrix node
        cmds.connectAttr(jnt1 + ".worldMatrix[0]", jnt1Matrix + ".inputMatrix")
        cmds.connectAttr(jnt2 + ".worldMatrix[0]", jnt2Matrix + ".inputMatrix")

        # use the output translate of those to plug into start and end point of distance node
        cmds.connectAttr(jnt1Matrix + ".outputTranslate", distanceNode + ".startPoint")
        cmds.connectAttr(jnt2Matrix + ".outputTranslate", distanceNode + ".endPoint")

        # create multiplyDivide node to get the scale factor
        multNode = cmds.shadingNode("multiplyDivide", asUtility=True)
        cmds.setAttr(multNode + ".input2X", cmds.getAttr(distanceNode + ".distance"))
        cmds.setAttr(multNode + ".operation", 2)
        cmds.connectAttr(distanceNode + ".distance", multNode + ".input1X")

        nodesList.append([multNode, jnt1, distanceNode])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def switchMode(self, mode, checkBox, frameRange=False):
        """
        This method switches between rig modes, matching the positions between rigs if the checkBox arg value is true.
        It also supports matching and switching over a frame range.

        :param mode: Which mode we are switching to
        :param checkBox: Whether or not we are matching when switching
        :param frameRange: Whether or not we are matching/switching over a frame range.

        """

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        # are we matching?
        if not frameRange:
            match = checkBox.isChecked()
        else:
            match = True

        # if being called from match over frame range
        if frameRange:
            if mode == matchData[1][0]:
                mode = "FK"
            if mode == matchData[1][1]:
                mode = "IK"

        # switch to FK mode
        if mode == "FK":
            # get current mode
            currentMode = cmds.getAttr(namespace + ":" + self.name + "_settings.mode")
            if currentMode == 0.0:
                cmds.warning("Already in FK mode.")
                return

            if not match:
                cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

            if match:
                # get fk controls
                controls = self.getControls(False, "fkControls")
                controls = sorted(controls)

                # create a duplicate
                ctrlGrp = cmds.listRelatives(controls[0], parent=True)[0]
                spaceGrp = cmds.listRelatives(ctrlGrp, parent=True)[0]
                topGrp = cmds.listRelatives(spaceGrp, parent=True)[0]

                newControls = cmds.duplicate(topGrp)
                cmds.parent(newControls[0], world=True)
                cmds.select(newControls[0], hi=True)
                cmds.delete(constraints=True)

                controls.reverse()
                for i in range(len(controls)):
                    try:
                        dupeCtrl = controls[i].partition(namespace + ":")[2]
                        dupeGrp = cmds.listRelatives(dupeCtrl, parent=True)[0]
                        parentCtrl = controls[i + 1].partition(namespace + ":")[2]
                        cmds.parentConstraint(parentCtrl, dupeGrp, mo=True)
                    except IndexError:
                        pass

                # match the fk controls to the corresponding joint
                controls.reverse()
                for control in controls:
                    joint = control.partition("fk_")[2].partition("_anim")[0]
                    joint = namespace + ":" + joint

                    dupeCtrl = control.partition(namespace + ":")[2]
                    constraint = cmds.parentConstraint(joint, dupeCtrl)[0]

                    dupe_scale = cmds.getAttr(joint + ".scale")[0]
                    cmds.setAttr(dupeCtrl + ".scale", dupe_scale[0], dupe_scale[1], dupe_scale[2], type='double3')

                    translate = cmds.getAttr(dupeCtrl + ".translate")[0]
                    rotate = cmds.getAttr(dupeCtrl + ".rotate")[0]
                    scale = cmds.getAttr(dupeCtrl + ".scale")[0]

                    cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2], type='double3')
                    cmds.setAttr(control + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')
                    cmds.setAttr(control + ".scale", scale[0], scale[1], scale[2], type='double3')

                    cmds.setKeyframe(control)
                    cmds.delete(constraint)

                # delete dupes
                cmds.delete(newControls[0])

                # switch modes
                if not frameRange:
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

        # switch to IK mode
        if mode == "IK":

            # get current mode
            if cmds.objExists(namespace + ":" + self.name + "_settings.mode"):
                currentMode = cmds.getAttr(namespace + ":" + self.name + "_settings.mode")
                if currentMode == 1.0:
                    return

                if not match:
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

                if match:

                    # get IK controls
                    controls = self.getControls(False, "ikControls")
                    controls = sorted(controls)

                    # duplicate controls
                    dupe_controls = []

                    for control in controls:
                        if control.find("offset") == -1:
                            ctrlGrp = cmds.listRelatives(control, parent=True)[0]
                            spaceGrp = cmds.listRelatives(ctrlGrp, parent=True)[0]
                            topGrp = cmds.listRelatives(spaceGrp, parent=True)[0]

                        else:
                            topGrp = cmds.listRelatives(control, parent=True)[0]

                        duplicateGrp = cmds.duplicate(topGrp)
                        cmds.parent(duplicateGrp[0], world=True)
                        dupe_controls.append(duplicateGrp[0])

                        # get the joint to have our control constrained to
                        joint = None
                        follicleJoint = cmds.listConnections(control + ".drivesJoint")[0]
                        pConst = cmds.listConnections(follicleJoint, type="pointConstraint", et=True)[0]
                        chain_ik_joint = cmds.listConnections(pConst)[0]
                        pconstraints = cmds.listConnections(chain_ik_joint, c=False, s=False, d=True,
                                                            type="pointConstraint", et=True)
                        for each in pconstraints:
                            if each.find("driver") != -1:
                                joint = each
                                break

                        # take the attrs from the dupe control and set them on the original
                        dupeCtrl = control.partition(namespace + ":")[2]
                        constraint = cmds.parentConstraint(joint, dupeCtrl)[0]

                        translate = cmds.getAttr(dupeCtrl + ".translate")[0]
                        rotate = cmds.getAttr(dupeCtrl + ".rotate")[0]

                        cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2], type='double3')
                        cmds.setAttr(control + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')

                        cmds.setKeyframe(control)
                        cmds.delete(constraint)

                    # delete dupes
                    cmds.delete(dupe_controls)

                    # switch modes
                    if not frameRange:
                        cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                        cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

            else:
                cmds.warning("No IK controls present to match to.")

    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    #                                                                                                           #
    # # # # # # # # # # # # # # # # # I N T E R F A C E   M E T H O D S # # # # # # # # # # # # # # # # # # # # #
    #                                                                                                           #
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////#

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleButtonState(self):
        """
        Toggles the state (enabled or disabled) of the Apply Changes button. Gets called when some element of the
        skeleton settings UI has changed.

        """
        state = self.applyButton.isEnabled()
        if state is False:
            self.applyButton.setEnabled(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateOutliner(self, oldNumber):
        """
        Whenever changes are made to the module settings, update the outliner to show the new or removed movers

        :param oldNumber: The original number of joints in the chain, so it can be compared to the new number.

        """

        # get number of joints in chain
        networkNode = self.returnNetworkNode
        currentNum = int(cmds.getAttr(networkNode + ".numJoints"))

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        # setup naming
        name = "chain"
        number = ""
        for i in range(currentNum):
            if i < 9:
                number = "_0"

            else:
                number = "_"

            # compare the old number to the new number
            if currentNum > oldNumber:
                # add more entries to the outliner
                parent = self.outlinerWidgets[max(self.chainWidgets)]

                for i in range(currentNum - oldNumber):
                    index = oldNumber + i
                    entry = prefix + name + suffix + number + str(index + 1)

                    if entry not in self.outlinerWidgets:
                        self.outlinerWidgets[entry] = QtWidgets.QTreeWidgetItem(parent)

                        self.outlinerWidgets[entry].setText(0, entry)

                        self.createGlobalMoverButton(entry, self.outlinerWidgets[entry], self.rigUiInst)
                        self.createOffsetMoverButton(entry, self.outlinerWidgets[entry], self.rigUiInst)
                        self.createMeshMoverButton(entry, self.outlinerWidgets[entry], self.rigUiInst)

                        parent = self.outlinerWidgets[entry]

                    # if the entry already exists, but is hidden, simply unhide it
                    if entry in self.outlinerWidgets:
                        self.outlinerWidgets[entry].setHidden(False)

            if currentNum < oldNumber:
                # hide existing entries in the outliner
                for i in range(oldNumber - currentNum):
                    index = oldNumber - i
                    entry = prefix + name + suffix + number + str(index)
                    self.outlinerWidgets[entry].setHidden(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def picker_listWidget_select(self, listWidget, *args):
        """
        Gets the selected items from the passed in listWidget and selects the associated controls/

        :param listWidget: List widget to get selected items from.

        """

        # get selected items from the passed in listWidget
        selected = listWidget.selectedItems()

        # get modifiers
        toggle = False
        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            toggle = True

        for each in selected:
            control = each.data(QtCore.Qt.UserRole)
            if toggle is False:
                cmds.select(control)
            if toggle is True:
                cmds.select(control, add=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectionScriptJob_animUI(self, fk_list, ik_list):
        """
        This method is called from a scriptjob anytime a selection is changed. It's sole purpose it to update the list
        widget selection to reflect if controls are selected or not.

        :param fk_list: The list widget that holds the fk controls
        :param ik_list: The list widget that holds the ik controls

        """
        selection = mel.eval("ls -sl;")
        if selection is None:
            selection = []

        listWidgetItems = []
        # get all fk listWidgetItems
        for i in range(fk_list.count()):
            item = fk_list.item(i)
            control = item.data(QtCore.Qt.UserRole)
            listWidgetItems.append([item, control])

        # get all ik listWidgetItems
        for i in range(ik_list.count()):
            item = ik_list.item(i)
            control = item.data(QtCore.Qt.UserRole)
            listWidgetItems.append([item, control])

        for each in listWidgetItems:
            if each[1] in selection:
                if not each[0].isSelected():
                    each[0].setSelected(True)

            else:
                each[0].setSelected(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def picker_createContextMenu_FK(self):
        """
        Create the right-click context menu for the chain's animation picker widget. This context menu has options
        for quickly selecting controls, zeroing out controls, and switching rig modes.

        :return: Returns the menu widget that was created
        """

        menu = QtWidgets.QMenu()

        fkIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/jointFilter.png"))))
        zeroIcon1 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroAll.png"))))
        zeroIcon2 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroSel.png"))))
        selectIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select.png"))))

        menu.addAction(selectIcon, "Select FK Chain Controls", partial(self.selectRigControls, "fk"))
        menu.addSeparator()

        menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
        menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))
        menu.addSeparator()

        return menu

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def picker_createContextMenu(self):
        """
        Create the right-click context menu for the chain's animation picker widget. This context menu has options
        for quickly selecting controls, zeroing out controls, and switching rig modes.

        :return: Returns the menu widget that was created
        """

        menu = QtWidgets.QMenu()

        fkIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/jointFilter.png"))))
        ikIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/ikMode.png"))))
        zeroIcon1 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroAll.png"))))
        zeroIcon2 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroSel.png"))))
        selectIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select.png"))))

        menu.addAction(selectIcon, "Select All Chain Controls", partial(self.selectRigControls, "all"))
        menu.addAction(selectIcon, "Select FK Chain Controls", partial(self.selectRigControls, "fk"))
        menu.addAction(selectIcon, "Select IK Chain Controls", partial(self.selectRigControls, "ik"))
        menu.addAction(selectIcon, "Select Chain Settings Node", partial(self.selectRigControls, "settings"))
        menu.addSeparator()

        switchAction = QtWidgets.QAction('Match when Switching', menu)
        switchAction.setCheckable(True)
        switchAction.setChecked(True)

        menu.addAction(fkIcon, "Chain FK Mode", partial(self.switchMode, "FK", switchAction))
        menu.addAction(ikIcon, "Chain IK Mode", partial(self.switchMode, "IK", switchAction))
        menu.addAction(switchAction)
        menu.addSeparator()

        menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
        menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))
        menu.addSeparator()

        return menu

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def switchMode_slider(self, slider, args):
        """
        This method updates the module's mode (0 - 1) based on the slider on the picker widget.

        :param slider: The slider widget whose value to query
        :param args: the current value of the slider (0 - 100)

        """

        value = float(args)/100

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        cmds.setAttr(namespace + ":" + self.name + "_settings.mode", value)
