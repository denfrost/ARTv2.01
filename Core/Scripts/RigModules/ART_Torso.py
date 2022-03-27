"""
Author: Jeremy Ernst

========
Contents
========

|   **Must Have Methods:**
|       :py:func:`addAttributes <RigModules.ART_Torso.ART_Torso.addAttributes>`
|       :py:func:`skeletonSettings_UI <RigModules.ART_Torso.ART_Torso.skeletonSettings_UI>`
|       :py:func:`pickerUI <RigModules.ART_Torso.ART_Torso.pickerUI>`
|       :py:func:`addJointMoverToOutliner <RigModules.ART_Torso.ART_Torso.addJointMoverToOutliner>`
|       :py:func:`applyModuleChanges <RigModules.ART_Torso.ART_Torso.applyModuleChanges>`
|       :py:func:`updateSettingsUI <RigModules.ART_Torso.ART_Torso.updateSettingsUI>`
|       :py:func:`resetSettings <RigModules.ART_Torso.ART_Torso.resetSettings>`
|       :py:func:`pinModule <RigModules.ART_Torso.ART_Torso.pinModule>`
|       :py:func:`skinProxyGeo <RigModules.ART_Torso.ART_Torso.skinProxyGeo>`
|       :py:func:`buildRigCustom <RigModules.ART_Torso.ART_Torso.buildRigCustom>`
|       :py:func:`importFBX <RigModules.ART_Torso.ART_Torso.importFBX>`
|       :py:func:`aimMode_Setup <RigModules.ART_Torso.ART_Torso.aimMode_Setup>`
|       :py:func:`setupPickWalking <RigModules.ART_Torso.ART_Torso.setupPickWalking>`
|
|   **Optional Methods:**
|       :py:func:`resetRigControls <RigModules.ART_Torso.ART_Torso.resetRigControls>`
|       :py:func:`selectRigControls <RigModules.ART_Torso.ART_Torso.selectRigControls>`
|
|   **Module Specific Methods:**
|       :py:func:`updateSpine <RigModules.ART_Torso.ART_Torso.updateSpine>`
|       :py:func:`includePelvis <RigModules.ART_Torso.ART_Torso.includePelvis>`
|       :py:func:`buildHips <RigModules.ART_Torso.ART_Torso.buildHips>`
|       :py:func:`buildFkSpine <RigModules.ART_Torso.ART_Torso.buildFkSpine>`
|       :py:func:`buildIKSpine <RigModules.ART_Torso.ART_Torso.buildIKSpine>`
|       :py:func:`setupAutoSpine <RigModules.ART_Torso.ART_Torso.setupAutoSpine>`
|       :py:func:`switchMode <RigModules.ART_Torso.ART_Torso.switchMode>`
|
|   **Interface Methods:**
|       :py:func:`_toggleButtonState <RigModules.ART_Torso.ART_Torso._toggleButtonState>`
|       :py:func:`updateOutliner <RigModules.ART_Torso.ART_Torso.updateOutliner>`
|       :py:func:`createContextMenu <RigModules.ART_Torso.ART_Torso.createContextMenu>`



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

        .. image:: /images/selectRigControls.png

===============
Class
===============
"""

import json
import os
import re
from functools import partial

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
from Base.ART_RigModule import ART_RigModule
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# file attributes
search = "biped:torso:spine"
className = "ART_Torso"
jointMover = "Core/JointMover/z_up/ART_Torso_3Spine.ma"
baseName = "torso"
displayName = "Torso"
rigs = ["FK::IK"]
fbxImport = ["None", "FK", "IK", "Both"]
matchData = [True, ["Match FK to IK", "Match IK to FK"]]
tooltip_image = "ART_Torso"


# begin class
class ART_Torso(ART_RigModule):
    """
    # class that defines a torso, with an FK and IK Ribbon rig
    """

    def __init__(self, rigUiInst, moduleUserName):
        """Initiate the class, taking in the instance to the interface and the user specified name.

        :param rigUiInst: This is the rig creator interface instance being passed in.
        :param moduleUserName: This is the name specified by the user on module creation.

        Instantiate the following class variables as well:
            * **self.rigUiInst:** take the passed in interface instance and make it a class var
            * **self.moduleUserName:** take the passed in moduleUserName and make it a class var
            * **self.outlinerWidget:** an empty list that will hold all of the widgets added to the outliner\
        """

        self.rigUiInst = rigUiInst
        self.moduleUserName = moduleUserName
        self.outlinerWidgets = {}

        ART_RigModule.__init__(self, "ART_Torso_Module", "ART_Torso", moduleUserName)

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
        Add custom attributes this module needs to the network node. (AKA metadata)

        Always calls on base class function first, then extends with any attributes unique to the class.
        """

        # call the base class method first to hook up our connections to the master module
        ART_RigModule.addAttributes(self)

        # add custom attributes for this specific module
        cmds.addAttr(self.networkNode, sn="Created_Bones", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".Created_Bones", "pelvis::spine_01::spine_02::spine_03::", type="string",
                     lock=True)

        cmds.addAttr(self.networkNode, sn="baseName", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".baseName", baseName, type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="canAim", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".canAim", True, lock=True)

        cmds.addAttr(self.networkNode, sn="aimMode", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".aimMode", False, lock=True)

        # joint mover settings

        cmds.addAttr(self.networkNode, sn="includePelvis", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".includePelvis", True, lock=True)

        cmds.addAttr(self.networkNode, sn="spineJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".spineJoints", 3, lock=True)

        # rig creation settings
        cmds.addAttr(self.networkNode, sn="buildFK", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".buildFK", True, lock=True)

        cmds.addAttr(self.networkNode, sn="buildIK", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".buildIK", True, lock=True)

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

        Build the groupBox that contains all of the settings for this module. Parent the groupBox
        into the main skeletonSettingsUI layout.
        Lastly, call on updateSettingsUI to populate the UI based off of the network node values.

        .. image:: /images/skeletonSettings.png

        """

        networkNode = self.returnNetworkNode

        # groupbox all modules get
        ART_RigModule.skeletonSettings_UI(self, name, 335, 275, True)

        font = QtGui.QFont()
        font.setPointSize(8)

        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # create a VBoxLayout to add to our Groupbox and then add a QFrame for our signal/slot
        self.layout = QtWidgets.QVBoxLayout(self.groupBox)
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setObjectName("lightnoborder")
        self.layout.addWidget(self.frame)

        self.frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.frame.setMinimumSize(QtCore.QSize(320, 240))
        self.frame.setMaximumSize(QtCore.QSize(320, 240))

        # add layout for custom settings
        self.customSettingsLayout = QtWidgets.QVBoxLayout(self.frame)

        # current parent
        self.currentParentMod = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.currentParentMod)
        self.currentParentLabel = QtWidgets.QLabel("Current Parent: ")
        self.currentParentLabel.setMinimumHeight(30)
        self.currentParentLabel.setMaximumHeight(30)
        self.currentParentLabel.setFont(font)
        self.currentParentMod.addWidget(self.currentParentLabel)

        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        self.currentParent = QtWidgets.QLabel(parent)
        self.currentParent.setFont(font)
        self.currentParent.setMinimumHeight(30)
        self.currentParent.setMaximumHeight(30)
        self.currentParent.setAlignment(QtCore.Qt.AlignHCenter)
        self.currentParentMod.addWidget(self.currentParent)

        # button layout for name/parent
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.buttonLayout)
        self.changeNameBtn = QtWidgets.QPushButton("Change Name")
        self.changeNameBtn.setMinimumHeight(30)
        self.changeNameBtn.setMaximumHeight(30)
        self.changeParentBtn = QtWidgets.QPushButton("Change Parent")
        self.changeParentBtn.setMinimumHeight(30)
        self.changeParentBtn.setMaximumHeight(30)
        self.buttonLayout.addWidget(self.changeNameBtn)
        self.buttonLayout.addWidget(self.changeParentBtn)
        self.changeNameBtn.setObjectName("settings")
        self.changeParentBtn.setObjectName("settings")

        text = "Change the name of the module."
        self.changeNameBtn.setToolTip(text)

        text = "Change the parent joint of the module."
        self.changeParentBtn.setToolTip(text)

        # bake offsets button
        self.bakeToolsLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.bakeToolsLayout)

        # Bake OFfsets
        self.bakeOffsetsBtn = QtWidgets.QPushButton("Bake Offsets")
        self.bakeOffsetsBtn.setMinimumHeight(30)
        self.bakeOffsetsBtn.setMaximumHeight(30)
        self.bakeOffsetsBtn.setFont(headerFont)
        self.bakeToolsLayout.addWidget(self.bakeOffsetsBtn)
        self.bakeOffsetsBtn.clicked.connect(self.bakeOffsets)
        self.bakeOffsetsBtn.setObjectName("settings")
        text = "Bake the offset mover values up to the global movers to get them aligned."
        self.bakeOffsetsBtn.setToolTip(text)

        # Pelvis Settings
        spacerItem = QtWidgets.QSpacerItem(200, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.customSettingsLayout.addItem(spacerItem)

        self.pelvisCB = QtWidgets.QCheckBox("Include Pelvis?")
        self.pelvisCB.setChecked(True)
        self.pelvisCB.setEnabled(False)
        self.pelvisCB.setVisible(False)
        self.customSettingsLayout.addWidget(self.pelvisCB)
        self.pelvisCB.stateChanged.connect(self._toggleButtonState)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.customSettingsLayout.addItem(spacerItem)

        # Spine Bones
        self.spineLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.spineLayout)

        self.numSpineBonesLabel = QtWidgets.QLabel("Number of Spine Bones: ")
        self.numSpineBonesLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.numSpineBonesLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.numSpineBonesLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.spineLayout.addWidget((self.numSpineBonesLabel))

        self.numSpine = QtWidgets.QSpinBox()
        self.numSpine.setMaximum(5)
        self.numSpine.setMinimum(2)
        self.numSpine.setMinimumSize(QtCore.QSize(100, 20))
        self.numSpine.setMaximumSize(QtCore.QSize(100, 20))
        self.numSpine.setValue(3)
        self.numSpine.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.spineLayout.addWidget(self.numSpine)

        # rebuild button
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.customSettingsLayout.addItem(spacerItem)

        self.applyButton = QtWidgets.QPushButton("Apply Changes")
        self.customSettingsLayout.addWidget(self.applyButton)
        self.applyButton.setFont(headerFont)
        self.applyButton.setMinimumSize(QtCore.QSize(300, 40))
        self.applyButton.setMaximumSize(QtCore.QSize(300, 40))
        self.applyButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.applyButton.setEnabled(False)
        text = "Update the scene with the module's new settings."
        self.applyButton.setToolTip(text)

        # add to the rig cretor UI's module settings layout VBoxLayout
        self.rigUiInst.moduleSettingsLayout.addWidget(self.groupBox)

        # button signal/slots
        self.changeNameBtn.clicked.connect(partial(self.changeModuleName, baseName, self, self.rigUiInst))
        self.changeParentBtn.clicked.connect(partial(self.changeModuleParent, self, self.rigUiInst))
        self.applyButton.clicked.connect(partial(self.applyModuleChanges, self))

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(self.groupBox, QtCore.SIGNAL("toggled(bool)"), self.frame.setVisible)
        self.groupBox.setChecked(False)

        # spinBox & checkbox signal/slots
        self.numSpine.valueChanged.connect(self._toggleButtonState)

        # Populate the settings UI based on the network node attributes
        self.updateSettingsUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pickerUI(self, center, animUI, networkNode, namespace):
        """
        Build the animation picker for the module.

        :param center: the center of the QGraphicsScene
        :param animUI: the instance of the AnimationUI
        :param networkNode: the module's network node
        :param namespace: the namespace of the character

        """

        self.namespace = namespace

        # create qBrushes
        yellowBrush = QtGui.QColor(155, 118, 67)
        blueBrush = QtGui.QColor(67, 122, 150)
        purpleBrush = QtGui.QColor(82, 67, 155)
        greenBrush = QtGui.QColor(122, 150, 67)
        clearBrush = QtGui.QBrush(QtCore.Qt.black)
        clearBrush.setStyle(QtCore.Qt.NoBrush)

        # create the picker border item
        if networkNode.find(":") != -1:
            moduleNode = networkNode.partition(":")[2]
        else:
            moduleNode = networkNode

        borderItem = interfaceUtils.pickerBorderItem(center.x() - 75, center.y() - 100, 150, 200, clearBrush,
                                                     moduleNode)

        # get controls
        fkControls = self.getControls(False, "fkControls")
        fkControls = sorted(fkControls)

        ikControls = self.getControls(False, "ikControls")
        ikControls = sorted(ikControls)
        pelvisControls = self.getControls(False, "pelvisControls")
        pelvisControls = sorted(pelvisControls)

        buttonData = []

        # get number of spine joints
        spineJoints = int(cmds.getAttr(networkNode + ".spineJoints"))

        if pelvisControls is not None:
            pelvisButton = interfaceUtils.pickerButtonCustom(100, 20, [[0, 0], [100, 0], [90, 20], [10, 20]], [25, 175],
                                                             pelvisControls[1], blueBrush, borderItem)
            bodyButton = interfaceUtils.pickerButton(110, 20, [20, 150], pelvisControls[0], yellowBrush,
                                                     borderItem)
            buttonData.append([pelvisButton, pelvisControls[1], blueBrush])
            buttonData.append([bodyButton, pelvisControls[0], yellowBrush])

        if spineJoints == 2:
            spine1Button = interfaceUtils.pickerButtonCustom(100, 50, [[10, 0], [100, 0], [110, 50], [0, 50]], [20, 95],
                                                             fkControls[0], blueBrush, borderItem)
            spine2Button = interfaceUtils.pickerButtonCustom(100, 60, [[10, 60], [100, 60], [110, 0], [0, 0]], [20, 30],
                                                             fkControls[1], blueBrush, borderItem)
            buttonData.append([spine1Button, fkControls[0], blueBrush])
            buttonData.append([spine2Button, fkControls[1], blueBrush])

        if spineJoints == 3:
            chestAnimButton = interfaceUtils.pickerButton(120, 20, [15, 25], ikControls[0], yellowBrush,
                                                          borderItem)
            midAnimButton = interfaceUtils.pickerButton(90, 20, [30, 100], ikControls[1], yellowBrush,
                                                        borderItem)
            buttonData.append([chestAnimButton, ikControls[0], yellowBrush])
            buttonData.append([midAnimButton, ikControls[1], yellowBrush])

            spine1Button = interfaceUtils.pickerButtonCustom(80, 20, [[10, 0], [100, 0], [105, 20], [5, 20]], [20, 125],
                                                             fkControls[0], blueBrush, borderItem)
            spine2Button = interfaceUtils.pickerButtonCustom(80, 20, [[10, 20], [100, 20], [100, 0], [10, 0]], [20, 75],
                                                             fkControls[1], blueBrush, borderItem)
            spine3Button = interfaceUtils.pickerButtonCustom(80, 20, [[10, 20], [100, 20], [105, 0], [5, 0]], [20, 50],
                                                             fkControls[2], blueBrush, borderItem)
            buttonData.append([spine1Button, fkControls[0], blueBrush])
            buttonData.append([spine2Button, fkControls[1], blueBrush])
            buttonData.append([spine3Button, fkControls[2], blueBrush])

        if spineJoints == 4:
            chestAnimButton = interfaceUtils.pickerButton(120, 20, [15, 25], ikControls[0], yellowBrush,
                                                          borderItem)
            midAnimButton = interfaceUtils.pickerButton(90, 15, [30, 90], ikControls[1], yellowBrush,
                                                        borderItem)
            buttonData.append([chestAnimButton, ikControls[0], yellowBrush])
            buttonData.append([midAnimButton, ikControls[1], yellowBrush])

            spine1Button = interfaceUtils.pickerButtonCustom(80, 15, [[10, 0], [100, 0], [105, 15], [5, 15]], [20, 130],
                                                             fkControls[0], blueBrush, borderItem)
            spine2Button = interfaceUtils.pickerButtonCustom(80, 15, [[10, 15], [100, 15], [95, 0], [15, 0]], [20, 110],
                                                             fkControls[1], blueBrush, borderItem)
            spine3Button = interfaceUtils.pickerButtonCustom(80, 15, [[15, 15], [95, 15], [100, 0], [10, 0]], [20, 70],
                                                             fkControls[2], blueBrush, borderItem)
            spine4Button = interfaceUtils.pickerButtonCustom(80, 15, [[10, 15], [100, 15], [110, 0], [0, 0]], [20, 50],
                                                             fkControls[3], blueBrush, borderItem)
            buttonData.append([spine1Button, fkControls[0], blueBrush])
            buttonData.append([spine2Button, fkControls[1], blueBrush])
            buttonData.append([spine3Button, fkControls[2], blueBrush])
            buttonData.append([spine4Button, fkControls[3], blueBrush])

        if spineJoints == 5:
            chestAnimButton = interfaceUtils.pickerButton(120, 20, [15, 25], ikControls[0], yellowBrush,
                                                          borderItem)
            midAnimButton = interfaceUtils.pickerButton(90, 20, [30, 95], ikControls[1], yellowBrush,
                                                        borderItem)
            buttonData.append([chestAnimButton, ikControls[0], yellowBrush])
            buttonData.append([midAnimButton, ikControls[1], yellowBrush])

            spine1Button = interfaceUtils.pickerButtonCustom(80, 10, [[0, 10], [110, 10], [105, 0], [5, 0]], [20, 135],
                                                             fkControls[0], blueBrush, borderItem)
            spine2Button = interfaceUtils.pickerButtonCustom(80, 10, [[5, 10], [105, 10], [100, 0], [10, 0]], [20, 120],
                                                             fkControls[1], blueBrush, borderItem)
            spine3Button = interfaceUtils.pickerButtonCustom(80, 10, [[10, 10], [100, 10], [100, 0], [10, 0]], [20, 80],
                                                             fkControls[2], blueBrush, borderItem)
            spine4Button = interfaceUtils.pickerButtonCustom(80, 10, [[10, 10], [100, 10], [105, 0], [5, 0]], [20, 65],
                                                             fkControls[3], blueBrush, borderItem)
            spine5Button = interfaceUtils.pickerButtonCustom(80, 10, [[5, 10], [105, 10], [110, 0], [0, 0]], [20, 50],
                                                             fkControls[4], blueBrush, borderItem)
            buttonData.append([spine1Button, fkControls[0], blueBrush])
            buttonData.append([spine2Button, fkControls[1], blueBrush])
            buttonData.append([spine3Button, fkControls[2], blueBrush])
            buttonData.append([spine4Button, fkControls[3], blueBrush])
            buttonData.append([spine5Button, fkControls[4], blueBrush])

        # =======================================================================
        # settings button
        # =======================================================================
        settingsBtn = interfaceUtils.pickerButton(20, 20, [125, 180], namespace + self.name + "_settings", greenBrush,
                                                  borderItem)
        buttonData.append([settingsBtn, namespace + self.name + "_settings", greenBrush])
        interfaceUtils.addTextToButton("S", settingsBtn)

        # =======================================================================
        # go through button data, adding menu items
        # =======================================================================
        for each in buttonData:
            button = each[0]

            fkIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/jointFilter.png"))))
            ikIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/ikMode.png"))))
            zeroIcon1 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroAll.png"))))
            zeroIcon2 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroSel.png"))))
            selectIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select.png"))))

            switchAction = QtWidgets.QAction('Match when Switching', button.menu)
            switchAction.setCheckable(True)
            switchAction.setChecked(True)

            button.menu.addAction(selectIcon, "Select All Torso Controls", partial(self.selectRigControls, "all"))
            button.menu.addAction(selectIcon, "Select FK Torso Controls", partial(self.selectRigControls, "fk"))
            button.menu.addAction(selectIcon, "Select IK Torso Controls", partial(self.selectRigControls, "ik"))

            button.menu.addSeparator()

            button.menu.addAction(fkIcon, "FK Mode", partial(self.switchMode, "FK", switchAction))
            button.menu.addAction(ikIcon, "IK Mode", partial(self.switchMode, "IK", switchAction))
            button.menu.addAction(switchAction)

            button.menu.addSeparator()

            button.menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
            button.menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))

            # body anim spaces
            if pelvisControls is not None:
                if each[1] == pelvisControls[0]:
                    button.menu.addSeparator()
                    button.addSpaces = partial(self.addSpacesToMenu, each[1], button)

            # chest anim spaces
            if ikControls is not None:
                if each[1] == ikControls[0]:
                    button.menu.addSeparator()
                    button.addSpaces = partial(self.addSpacesToMenu, each[1], button)

            # fk spine 01 spaces
            if each[1] == fkControls[0]:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, each[1], button)

        # =======================================================================
        # #Create scriptJob for selection. Set scriptJob number to borderItem.data(5)
        # =======================================================================
        scriptJob = cmds.scriptJob(event=["SelectionChanged", partial(self.selectionScriptJob_animUI, buttonData)],
                                   kws=True)
        borderItem.setData(5, scriptJob)
        animUI.selectionScriptJobs.append(scriptJob)

        return [borderItem, False, scriptJob]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addJointMoverToOutliner(self):
        """
        Add the joint movers for this module to the outliner. (called from ART_AddModuleUI)

        Depending on the module settings, different joint movers may or may not be added. Also, each "joint" usually
        has three movers: global, offset, and geo. However, not all joints do, so this method is also used to specify
        which joint movers for each joint are added to the outliner.

        .. image:: /images/outliner.png

        """

        index = self.rigUiInst.treeWidget.topLevelItemCount()
        self.outlinerWidgets = {}

        # Add the module to the tree widget in the outliner tab of the rig creator UI
        self.outlinerWidgets[self.name + "_treeModule"] = QtWidgets.QTreeWidgetItem(self.rigUiInst.treeWidget)
        self.rigUiInst.treeWidget.topLevelItem(index).setText(0, self.name)
        foreground = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.outlinerWidgets[self.name + "_treeModule"].setForeground(0, foreground)

        # add the pelvis
        self.outlinerWidgets[self.name + "_pelvis"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_treeModule"])
        self.outlinerWidgets[self.name + "_pelvis"].setText(0, self.name + "_pelvis")
        self.createGlobalMoverButton(self.name + "_pelvis", self.outlinerWidgets[self.name + "_pelvis"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pelvis", self.outlinerWidgets[self.name + "_pelvis"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pelvis", self.outlinerWidgets[self.name + "_pelvis"],
                                   self.rigUiInst)

        # add spine01
        self.outlinerWidgets[self.name + "_spine_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_treeModule"])
        self.outlinerWidgets[self.name + "_spine_01"].setText(0, self.name + "_spine_01")
        self.createGlobalMoverButton(self.name + "_spine_01", self.outlinerWidgets[self.name + "_spine_01"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_spine_01", self.outlinerWidgets[self.name + "_spine_01"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_spine_01", self.outlinerWidgets[self.name + "_spine_01"],
                                   self.rigUiInst)

        # add spine02
        self.outlinerWidgets[self.name + "_spine_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_spine_01"])
        self.outlinerWidgets[self.name + "_spine_02"].setText(0, self.name + "_spine_02")
        self.createGlobalMoverButton(self.name + "_spine_02", self.outlinerWidgets[self.name + "_spine_02"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_spine_02", self.outlinerWidgets[self.name + "_spine_02"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_spine_02", self.outlinerWidgets[self.name + "_spine_02"],
                                   self.rigUiInst)

        # add spine03
        self.outlinerWidgets[self.name + "_spine_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_spine_02"])
        self.outlinerWidgets[self.name + "_spine_03"].setText(0, self.name + "_spine_03")
        self.createGlobalMoverButton(self.name + "_spine_03", self.outlinerWidgets[self.name + "_spine_03"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_spine_03", self.outlinerWidgets[self.name + "_spine_03"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_spine_03", self.outlinerWidgets[self.name + "_spine_03"],
                                   self.rigUiInst)

        # add spine04
        self.outlinerWidgets[self.name + "_spine_04"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_spine_03"])
        self.outlinerWidgets[self.name + "_spine_04"].setText(0, self.name + "_spine_04")
        self.createGlobalMoverButton(self.name + "_spine_04", self.outlinerWidgets[self.name + "_spine_04"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_spine_04", self.outlinerWidgets[self.name + "_spine_04"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_spine_04", self.outlinerWidgets[self.name + "_spine_04"],
                                   self.rigUiInst)

        # add spine05
        self.outlinerWidgets[self.name + "_spine_05"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_spine_04"])
        self.outlinerWidgets[self.name + "_spine_05"].setText(0, self.name + "_spine_05")
        self.createGlobalMoverButton(self.name + "_spine_05", self.outlinerWidgets[self.name + "_spine_05"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_spine_05", self.outlinerWidgets[self.name + "_spine_05"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_spine_05", self.outlinerWidgets[self.name + "_spine_05"],
                                   self.rigUiInst)

        # create selection script job for module
        self.createScriptJob()

        # update based on spinBox values
        self.updateOutliner()
        self.updateBoneCount()
        self.rigUiInst.treeWidget.expandAll()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleChanges(self, moduleInst):

        networkNode = self.returnNetworkNode

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

        # create list of the new created bones
        spineJoints = []
        if self.pelvisCB.isChecked():
            spineJoints.append(prefix + "pelvis" + suffix)

        # get current spine value
        currentNum = int(cmds.getAttr(networkNode + ".spineJoints"))

        # get new spine value
        uiSpineNum = self.numSpine.value()

        # if duplicating, there is an issue where both the UI and the network node are updated at once,
        # meaning this comparrison will not actually update with the proper settings.
        # So, here, find the number of spine joints in the scene
        rels = cmds.listRelatives(self.name + "_mover_grp", children=True, type="transform", ad=True)

        numbers = []
        for r in rels:
            num = re.findall(r'\d{2}', r)
            if num not in numbers:
                numbers.append(num)

        sceneSpineNum = int(max(numbers)[0])

        if uiSpineNum != currentNum or sceneSpineNum != currentNum:
            # update spine value, and call on update spine
            cmds.setAttr(networkNode + ".spineJoints", lock=False)
            cmds.setAttr(networkNode + ".spineJoints", uiSpineNum, lock=True)

            # look for any attached modules
            attachedModules = self.checkForDependencies()
            self.updateSpine(attachedModules, currentNum)

        for i in range(uiSpineNum):
            spineJoints.append(prefix + "spine_0" + str(i + 1) + suffix)

        # build attrString
        attrString = ""
        for bone in spineJoints:
            attrString += bone + "::"

        networkNode = self.returnNetworkNode
        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # pelvis
        self.includePelvis()

        # reset button
        self.applyButton.setEnabled(False)

        # update outliner
        self.updateOutliner()
        self.updateBoneCount()

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
        Updates the skeleton settings UI based on the network node values for this module. Happens when the UI is
        launched and there are module metadata present
        """

        networkNode = self.returnNetworkNode

        includePelvis = cmds.getAttr(networkNode + ".includePelvis")
        numSpine = cmds.getAttr(networkNode + ".spineJoints")

        # update UI elements
        self.numSpine.setValue(numSpine)
        self.pelvisCB.setChecked(includePelvis)

        # apply changes
        self.applyButton.setEnabled(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetSettings(self):
        """
        (OVERRIDE OF BASE CLASS!)
        Reset the settings of the module's network node.

        This function is used in the right-click menu of the module on the skeleton settings interface.
        Occasionally, it is called outside of the menu.

        After settings are reset, applyModuleChanges is called to update the joint mover in the scene with
        the latest values. updateSettingsUI is also called to update the outliner.
        """

        self.pelvisCB.setChecked(True)
        self.numSpine.setValue(3)

        # relaunch the UI
        self.applyModuleChanges(self)
        self.updateSettingsUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pinModule(self, state):
        """
        Pins the module in place (joint movers), so that the parent module no longer affects it.
        :param state: (bool). Whether the module is pinned or not.

        """

        networkNode = self.returnNetworkNode
        includePelvis = cmds.getAttr(networkNode + ".includePelvis")

        if state:
            if cmds.getAttr(networkNode + ".pinned") is True:
                return

            if includePelvis:
                topLevelMover = self.name + "_pelvis_mover"
            else:
                topLevelMover = self.name + "_spine_01_mover"

            loc = cmds.spaceLocator()[0]
            cmds.setAttr(loc + ".v", False, lock=True)
            constraint = cmds.parentConstraint(topLevelMover, loc)[0]
            cmds.delete(constraint)
            const = cmds.parentConstraint(loc, topLevelMover)[0]

            if not cmds.objExists(networkNode + ".pinConstraint"):
                cmds.addAttr(networkNode, ln="pinConstraint", keyable=True, at="message")
            if not cmds.objExists(networkNode + ".pinLocator"):
                cmds.addAttr(networkNode, ln="pinLocator", keyable=True, at="message")

            cmds.connectAttr(const + ".message", networkNode + ".pinConstraint")
            cmds.connectAttr(loc + ".message", networkNode + ".pinLocator")

        if not state:
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
         Skin the proxy geo brought in by the module. Each module has to define how it wants to skin its proxy geo.
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
                parent = cmds.listRelatives(each, parent=True)[0]
                if cmds.nodeType(each) == "transform":
                    proxyGeoMeshes.append(each)

        # skin the proxy geo meshes
        for mesh in proxyGeoMeshes:

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
            joint = prefix + boneName + suffix

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
        The base class gets a buildRig function called from the buildProgressUI. This function has some pre/post
        functionality that labels new nodes created by the buildRigCustom method. Each derived class will need to have a
        buildRigCustom implemented. This method should call on any rig building functions for that module.

        -each module should have its own settings group : self.name + "_settings"
        -each module should have something similar to the builtRigs list, which is a list that holds what rigs have been
        built (NOT, which are going to BE built, but the ones that already have)
            -this list looks something like this: [["FK", [nodesToHide]],["IK", [nodesToHide]]]
            -this is used when it's time to setup the mode switching

        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Building " + self.name + " Rig..")

        # get the network node and find out which rigs to build
        networkNode = self.returnNetworkNode
        buildFK = True
        buildIK = True

        # create a new network node to hold the control types
        if not cmds.objExists(networkNode + ".controls"):
            cmds.addAttr(networkNode, sn="controls", at="message")

        controlNode = cmds.createNode("network", name=networkNode + "_Controls")
        cmds.addAttr(controlNode, sn="parentModule", at="message")

        # connect new network node to original network node
        cmds.connectAttr(networkNode + ".controls", controlNode + ".parentModule")

        # have it build all rigs by default, unless there is an attr stating otherwise (backwards- compatability)
        numRigs = 0
        if cmds.objExists(networkNode + ".buildFK"):
            buildFK = cmds.getAttr(networkNode + ".buildFK")
            if buildFK:
                numRigs += 1
        if cmds.objExists(networkNode + ".buildIK"):
            buildIK_V1 = cmds.getAttr(networkNode + ".buildIK")
            if buildIK_V1:
                numRigs += 1

        builtRigs = []

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create groups and settings
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create the spine group
        spineJoints = self.returnCreatedJoints
        self.spineGroup = cmds.group(empty=True, name=self.name + "_group")
        constraint = cmds.parentConstraint(spineJoints[0], self.spineGroup)[0]
        cmds.delete(constraint)

        joints = []
        for jnt in spineJoints:
            if jnt.find("pelvis") == -1:
                joints.append(jnt)

        # create the spine settings group
        self.spineSettings = cmds.group(empty=True, name=self.name + "_settings")
        cmds.parent(self.spineSettings, self.spineGroup)
        for attr in (cmds.listAttr(self.spineSettings, keyable=True)):
            cmds.setAttr(self.spineSettings + "." + attr, lock=True, keyable=False)

        # add mode attribute to settings
        if numRigs > 1:
            cmds.addAttr(self.spineSettings, ln="mode", min=0, max=numRigs - 1, dv=0, keyable=True)

        # create the ctrl group (what will get the constraint to the parent)
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        self.spineCtrlGrp = cmds.group(empty=True, name=self.name + "_spine_ctrl_grp")

        constraint = cmds.parentConstraint("driver_" + parentBone, self.spineCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(self.spineCtrlGrp, self.spineGroup)
        cmds.makeIdentity(self.spineCtrlGrp, t=1, r=1, s=1, apply=True)

        includePelvis = cmds.getAttr(networkNode + ".includePelvis")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # build the rigs
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        if includePelvis:
            self.buildHips(textEdit, uiInst, builtRigs, networkNode)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       FK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # if build FK was true, build the FK rig now
        if buildFK:
            fkInfo = self.buildFkSpine(textEdit, uiInst, builtRigs, networkNode)
            builtRigs.append(["FK", fkInfo])  # [1] = nodes to hide

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       IK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # if build IK was true, build the IK rig now
        if buildIK:
            ikInfo = self.buildIKSpine(textEdit, uiInst, builtRigs, networkNode)
            if len(joints) > 2:
                builtRigs.append(["IK", ikInfo])  # [1] = nodes to hide

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
            for joint in spineJoints:
                connections.extend(list(set(cmds.listConnections("driver_" + joint, type="constraint"))))
                ramps = (list(set(cmds.listConnections("driver_" + joint, type="ramp"))))
                for ramp in ramps:
                    connections.append(ramp + ".uCoord")

                for connection in connections:
                    driveAttrs = []

                    if cmds.nodeType(connection) in ["pointConstraint", "orientConstraint", "parentConstraint"]:

                        # get those constraint target attributes for each constraint connection
                        targets = cmds.getAttr(connection + ".target", mi=True)
                        if len(targets) > 1:
                            for each in targets:
                                driveAttrs.append(
                                    cmds.listConnections(connection + ".target[" + str(each) + "].targetWeight",
                                                         p=True))

                            # add this data to our master list of constraint attribute data
                            attrData.append(driveAttrs)
                    else:
                        if cmds.nodeType(connection) == "ramp":
                            rampData.append(connection)

            rampData = list(set(rampData))

            # setup set driven keys on our moder attr and those target attributes
            for i in range(numRigs):

                cmds.setAttr(self.spineSettings + ".mode", i)

                # go through attr data and zero out anything but the first element in the list
                for data in attrData:
                    for each in data:
                        cmds.setAttr(each[0], 0)

                    cmds.setAttr(data[i][0], 1)

                # set driven keys
                for data in attrData:
                    for each in data:
                        cmds.setDrivenKeyframe(each[0], cd=self.spineSettings + ".mode", itt="linear",
                                               ott="linear")

            """ RAMPS """
            # direct connect mode to uCoord value (only works if there are 2 rigs) <- not sure if that is thecase still
            for data in rampData:
                # create a multiply node that takes first input of 1/numRigs and 2nd of mode direct connection
                multNode = cmds.shadingNode("multiplyDivide", asUtility=True,
                                            name=self.name + "_" + data.partition(".uCoord")[0] + "_mult")
                cmds.setAttr(multNode + ".input1X", float(float(1) / float(numRigs - 1)))
                cmds.connectAttr(self.spineSettings + ".mode", multNode + ".input2X")
                cmds.connectAttr(multNode + ".outputX", data)

            # hook up control visibility
            for i in range(len(builtRigs)):
                cmds.setAttr(self.spineSettings + ".mode", i)
                for rig in builtRigs:
                    visNodes = rig[1]
                    for node in visNodes:
                        if node != None:
                            cmds.setAttr(node + ".v", 0)

                    if builtRigs.index(rig) == i:
                        visNodes = rig[1]
                        for node in visNodes:
                            if node is not None:
                                cmds.setAttr(node + ".v", 1)

                    cmds.setDrivenKeyframe(visNodes, at="visibility", cd=self.spineSettings + ".mode",
                                           itt="linear",
                                           ott="linear")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #            Parent Under Offset Ctrl           # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # parent under offset_anim if it exists(it always should)
        if cmds.objExists("offset_anim"):
            cmds.parent(self.spineGroup, "offset_anim")

        # return data
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        try:
            uiInst.rigData.append([self.spineCtrlGrp, "driver_" + parentBone, numRigs])
        except:
            pass

        # lock down network node
        cmds.lockNode(networkNode, lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importFBX(self, importMethod, character):
        """
        This method defines how mocap is imported onto the rig controls.

        :param importMethod: Whether or not the FBX is getting imported as FK, IK, Both, or None
        :param character: The namespace of the rig.

        """

        returnControls = []

        # get basic info of node
        networkNode = self.returnRigNetworkNode
        moduleName = cmds.getAttr(networkNode + ".moduleName")
        baseModuleName = cmds.getAttr(networkNode + ".baseName")

        # find prefix/suffix of module name
        prefixSuffix = moduleName.split(baseModuleName)
        prefix = None
        suffix = None

        if prefixSuffix[0] != '':
            prefix = prefixSuffix[0]
        if prefixSuffix[1] != '':
            suffix = prefixSuffix[1]

        # get controls
        pelvisControls = self.getControls(False, "pelvisControls")
        fkControls = self.getControls(False, "fkControls")
        ikControls = self.getControls(False, "ikControls")

        # get joints
        joints = cmds.getAttr(networkNode + ".Created_Bones")
        splitJoints = joints.split("::")
        createdJoints = []

        for bone in splitJoints:
            if bone != "":
                createdJoints.append(bone)

        # IMPORT (FK OR IK)
        for joint in createdJoints:
            if joint.find("pelvis") != -1:
                cmds.parentConstraint(joint, pelvisControls[1])
                returnControls.append(pelvisControls[1])

        # IMPORT FK
        if importMethod == "FK" or importMethod == "Both":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 0)

            for joint in createdJoints:
                if cmds.objExists(character + ":" + "fk_" + joint + "_anim"):
                    cmds.parentConstraint(joint, character + ":" + "fk_" + joint + "_anim")
                    returnControls.append(character + ":" + "fk_" + joint + "_anim")

        # IMPORT IK
        if importMethod == "IK" or importMethod == "Both":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 1)

            topJoint = createdJoints[-1]
            midJoint = createdJoints[(len(createdJoints)) / 2]

            cmds.parentConstraint(topJoint, ikControls[0])
            returnControls.append(ikControls[0])

            cmds.parentConstraint(midJoint, ikControls[1])
            returnControls.append(ikControls[1])

        # IMPORT NONE
        if importMethod == "None":
            pass

        return returnControls

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def aimMode_Setup(self, state):
        """
        Sets up (or removes the setup) of aim mode for the joint mover rig. This ensures the parent always aims
        at the child mover.

        :param state: (bool). Whether to setup or tear down aim mode.

        """

        # get attributes needed
        name = self.name
        networkNode = self.returnNetworkNode
        numSpine = cmds.getAttr(networkNode + ".spineJoints")

        # setup aim vector details per side
        aimVector = [1, 0, 0]
        aimUp = [0, 1, 0]

        # if passed in state is True:
        if state:
            # setup aim constraints

            if numSpine == 2:
                cmds.aimConstraint(name + "_spine_02_lra", name + "_spine_01_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_02_lra", mo=True)

            if numSpine == 3:
                cmds.aimConstraint(name + "_spine_02_lra", name + "_spine_01_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_02_lra",  mo=True)

                cmds.aimConstraint(name + "_spine_03_lra", name + "_spine_02_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_03_lra", mo=True)

            if numSpine == 4:
                cmds.aimConstraint(name + "_spine_02_lra", name + "_spine_01_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_02_lra", mo=True)

                cmds.aimConstraint(name + "_spine_03_lra", name + "_spine_02_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_03_lra", mo=True)

                cmds.aimConstraint(name + "_spine_04_lra", name + "_spine_03_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_04_lra", mo=True)

            if numSpine == 5:
                cmds.aimConstraint(name + "_spine_02_lra", name + "_spine_01_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_02_lra", mo=True)

                cmds.aimConstraint(name + "_spine_03_lra", name + "_spine_02_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_03_lra", mo=True)

                cmds.aimConstraint(name + "_spine_04_lra", name + "_spine_03_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_04_lra", mo=True)

                cmds.aimConstraint(name + "_spine_05_lra", name + "_spine_04_mover_offset", aimVector=aimVector,
                                   upVector=aimUp, wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_spine_05_lra", mo=True)

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
    def setupPickWalking(self):
        """
        Sets up custom pickwalking between rig controls.

        :return: returns list of top level controls of the module that will need hooks to their parent controls
        """

        # get controls
        fkControls = self.getControls(False, "fkControls")
        fkControls = sorted(fkControls)

        ikControls = self.getControls(False, "ikControls")
        ikControls = sorted(ikControls)
        pelvisControls = self.getControls(False, "pelvisControls")
        pelvisControls = sorted(pelvisControls)

        # setup FK pick-walking
        if len(pelvisControls) > 0:
            # body anim pickwalking down to hip anim
            cmds.addAttr(pelvisControls[0], ln="pickWalkDown", at="message")
            cmds.connectAttr(pelvisControls[1] + ".message", pelvisControls[0] + ".pickWalkDown")

            # hip anim pickwalking up to body anim
            cmds.addAttr(pelvisControls[1], ln="pickWalkUp", at="message")
            cmds.connectAttr(pelvisControls[0] + ".message", pelvisControls[1] + ".pickWalkUp")

            # hip anim pickwalking down to fk spine 01
            cmds.addAttr(pelvisControls[1], ln="pickWalkDown", at="message")
            cmds.connectAttr(fkControls[0] + ".message", pelvisControls[1] + ".pickWalkDown")

            # fk spine 01 pickwalking up to hip anim
            cmds.addAttr(fkControls[0], ln="pickWalkUp", at="message")
            cmds.connectAttr(pelvisControls[1] + ".message", fkControls[0] + ".pickWalkUp")

        # for each spine control, setup pickwalk up and down
        for i in range(len(fkControls)):
            try:
                if cmds.objExists(fkControls[i + 1]):
                    cmds.addAttr(fkControls[i], ln="pickWalkDown", at="message")
                    cmds.connectAttr(fkControls[i + 1] + ".message", fkControls[i] + ".pickWalkDown")

                    cmds.addAttr(fkControls[i + 1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[i] + ".message", fkControls[i + 1] + ".pickWalkUp")
            except IndexError, e:
                print e

        # setup IK pick-walking
        cmds.addAttr(fkControls[-1], ln="pickWalkDown", at="message")
        cmds.connectAttr(ikControls[1] + ".message", fkControls[-1] + ".pickWalkDown")

        cmds.addAttr(ikControls[1], ln="pickWalkUp", at="message")
        cmds.connectAttr(fkControls[-1] + ".message", ikControls[1] + ".pickWalkUp")

        cmds.addAttr(ikControls[1], ln="pickWalkDown", at="message")
        cmds.connectAttr(ikControls[0] + ".message", ikControls[1] + ".pickWalkDown")

        cmds.addAttr(ikControls[0], ln="pickWalkUp", at="message")
        cmds.connectAttr(ikControls[1] + ".message", ikControls[0] + ".pickWalkUp")

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
    def resetRigControls(self, resetAll):
        """
        Override of base class method that will reset the rig controls to a default state (the creation state).

        :param resetAll: Whether or not to reset all of the rig controls in this module.
        :return:
        """

        # get namespace
        nonZeroAttrs = ["scale", "globalScale", "scaleX", "scaleY", "scaleZ", "twist_amount", "rotationInfluence",
                        "autoSpine"]

        if resetAll is True:

            # list any attributes on the network node that contain "controls"
            controls = self.getControls(True)
            # get that data on that attr
            for control in controls:
                for each in control:
                    # reset the attr on each control
                    try:
                        attrs = cmds.listAttr(each, keyable=True)
                        for attr in attrs:
                            if attr not in nonZeroAttrs:
                                try:
                                    cmds.setAttr(each + "." + attr, 0)
                                except:
                                    pass
                            else:
                                try:
                                    cmds.setAttr(each + "." + attr, 1)
                                except:
                                    pass
                    except:
                        cmds.warning("skipped " + str(control) + ". No valid controls found to reset.")

        if resetAll is False:
            selection = cmds.ls(sl=True)
            print selection
            for each in selection:
                attrs = cmds.listAttr(each, keyable=True)
                for attr in attrs:
                    if attr not in nonZeroAttrs:

                        try:
                            cmds.setAttr(each + "." + attr, 0)
                        except:
                            pass
                    else:
                        try:
                            cmds.setAttr(each + "." + attr, 1)
                        except Exception, e:
                            print e

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectRigControls(self, mode):
        """
        (BASE CLASS OVERRIDE!)
        This method calls on getControls to return a list of the controls and the selects them.
        """

        cmds.select(clear=True)

        if mode == "all":
            controls = self.getControls()
            for control in controls:
                for each in control:
                    cmds.select(each, add=True)

        if mode == "fk":
            fkControls = self.getControls(False, "fkControls")
            fkControls = sorted(fkControls)
            for control in fkControls:
                cmds.select(control, add=True)

        if mode == "ik":
            ikControls = self.getControls(False, "ikControls")
            for control in ikControls:
                cmds.select(control, add=True)

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
    def updateSpine(self, attachedModules, oldNum):
        """
        Updates the joint mover in the scene based on the new number of spine bones that needs to be present.
        This method will record the joint mover positions, remove the joint mover, then import in the new file that
        corresponds to the new number of spine joints.

        :param attachedModules: Any modules that may be affected by this change
        :param oldNum: The old (current) number of spine bones
        """

        # gather information (current name, current parent, etc)
        networkNode = self.returnNetworkNode
        name = cmds.getAttr(networkNode + ".moduleName")
        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        newNum = int(cmds.getAttr(networkNode + ".spineJoints"))

        # call on base class delete
        movers = self.returnJointMovers
        for moverGrp in movers:
            for mover in moverGrp:
                cmds.lockNode(mover, lock=False)

        # store mover positions (movers = [all global, all offset, all geo])
        basePositions = {}

        for each in movers:
            for mover in each:
                attrs = cmds.listAttr(mover, keyable=True)
                attrValues = []
                for attr in attrs:
                    value = cmds.getAttr(mover + "." + attr)
                    attrValues.append([attr, value])
                basePositions[mover] = attrValues

        if cmds.getAttr(networkNode + ".aimMode") is True:
            self.aimMode_Setup(False)

        # delete joint mover
        cmds.delete(self.name + "_mover_grp")

        # build new jmPath name
        jmPath = jointMover.partition(".ma")[0].rpartition("_")[0] + "_" + str(newNum) + "Spine.ma"
        if self.up == "y":
            jmPath = jmPath.replace("z_up", "y_up")

        self.jointMover_Build(jmPath)

        # apply base positions
        for key in basePositions:

            mover = key
            attrList = basePositions.get(key)

            for attr in attrList:
                if cmds.objExists(mover):
                    cmds.setAttr(mover + "." + attr[0], attr[1])

        # parent the joint mover to the offset mover of the parent
        mover = ""
        if parent == "root":
            mover = "root_mover"

        else:
            # find the parent mover name to parent to
            networkNodes = utils.returnRigModules()
            mover = utils.findMoverNodeFromJointName(networkNodes, parent)

        # delete the old constraint and create the new one
        if cmds.objExists(self.name + "_mover_grp_parentConstraint*"):
            cmds.delete(self.name + "_mover_grp_parentConstraint*")

        if mover is not None:
            cmds.parentConstraint(mover, self.name + "_mover_grp", mo=True)

        if cmds.objExists(self.name + "_mover_grp_scaleConstraint*"):
            cmds.delete(self.name + "_mover_grp_scaleConstraint*")

        if mover is not None:
            cmds.scaleConstraint(mover, self.name + "_mover_grp", mo=True)

        # create the connection geo between the two
        self.applyModuleChanges(self)

        self.aimMode_Setup(True)

        cmds.select(clear=True)

        # if there were any module dependencies, fix those now.
        if len(attachedModules) > 0:
            self.fixDependencies(attachedModules)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def includePelvis(self, *args):
        """
         This method will change visiblity and parenting on joint movers in the module depending on whether there will
         be a pelvis or not.

        """

        state = self.pelvisCB.isChecked()

        if state is not False:

            # hide  mover controls
            cmds.setAttr(self.name + "_pelvis_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_pelvis_mover_grp.v", 0, lock=True)

            # parent to mover_grp
            try:
                cmds.parent(self.name + "_spine_01_mover_grp", self.name + "_mover_grp")
            except Exception, e:
                print e

        if state is True:

            # show mover controls
            cmds.setAttr(self.name + "_pelvis_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_pelvis_mover_grp.v", 1, lock=True)

            # parent to mover_grp
            try:
                cmds.parent(self.name + "_spine_01_mover_grp", self.name + "_pelvis_mover")
            except Exception, e:
                print e

        networkNode = self.returnNetworkNode
        cmds.setAttr(networkNode + ".includePelvis", lock=False)
        cmds.setAttr(networkNode + ".includePelvis", state, lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildHips(self, textEdit, uiInst, builtRigs, networkNode):
        """
        Builds the hip rig (body anim and hip anim controls)
        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Building Pelvis Rig..")

        # find the joints in the spine module that need rigging
        allJnts = self.returnCreatedJoints
        joints = []
        for jnt in allJnts:
            if jnt.find("pelvis") != -1:
                joints.append(jnt)

        # create the grp and position and orient it correctly
        controlInfo = riggingUtils.createControlFromMover(joints[0], networkNode, True, True,
                                                          control_type="ik_rig_control")
        self.bodyAnim = cmds.rename(controlInfo[0], self.name + "_body_anim")
        self.bodyAnimGrp = cmds.rename(controlInfo[1], self.name + "_body_anim_grp")
        self.bodyAnimSpace = cmds.rename(controlInfo[2], self.name + "_body_anim_space_switcher")
        self.bodyAnimFollow = cmds.rename(controlInfo[3], self.name + "_body_anim_space_switcher_follow")
        riggingUtils.colorControl(self.bodyAnim, 17)

        # Pelvis
        hipControlInfo = riggingUtils.createControlFromMover(joints[0], networkNode, True, False,
                                                             control_type="fk_rig_control")
        self.hipAnim = cmds.rename(hipControlInfo[0], self.name + "_hip_anim")
        self.hipAnimGrp = cmds.rename(hipControlInfo[1], self.name + "_hip_anim_grp")
        riggingUtils.colorControl(self.hipAnim, 18)

        cmds.parent(self.hipAnimGrp, self.bodyAnim)

        for each in [self.bodyAnim, self.hipAnim]:
            for attr in [".scaleX", ".scaleY", ".scaleZ", ".visibility"]:
                cmds.setAttr(each + attr, lock=True, keyable=False)

        cmds.parent(self.bodyAnimFollow, self.spineCtrlGrp)

        # =======================================================================
        # #lastly, connect controls up to blender nodes to drive driver joints
        # =======================================================================
        cmds.pointConstraint(self.hipAnim, "driver_" + joints[0], mo=True)
        cmds.orientConstraint(self.hipAnim, "driver_" + joints[0])

        # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
        # input 2, and plugs that into driver joint
        if cmds.objExists("master_anim"):
            globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=joints[0] + "_globalScale")
            cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
            cmds.connectAttr(self.hipAnim + ".scale", globalScaleMult + ".input2")
            riggingUtils.createConstraint(globalScaleMult, "driver_" + joints[0], "scale", False, 2, 0, "output")
        else:
            riggingUtils.createConstraint(self.hipAnim, "driver_" + joints[0], "scale", False, 2, 0)

        # get controlNode
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        # add pelvis controls to control node
        if not cmds.objExists(controlNode + ".pelvisControls"):
            cmds.addAttr(controlNode, sn="pelvisControls", at="message")

        # add proxy attributes for mode
        if cmds.objExists(self.spineSettings + ".mode"):
            for node in [self.hipAnim, self.bodyAnim]:
                cmds.addAttr(node, ln="mode", proxy=self.spineSettings + ".mode", at="double", keyable=True)

        for node in [self.hipAnim, self.bodyAnim]:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".pelvisControls", node + ".controlClass")

            # add controlType attr
            cmds.addAttr(node, ln="controlType", dt="string")
            cmds.setAttr(node + ".controlType", "IK", type="string")

        cmds.addAttr(self.bodyAnim, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
        cmds.setAttr(self.bodyAnim + ".hasSpaceSwitching", lock=True)
        cmds.addAttr(self.bodyAnim, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
        cmds.setAttr(self.bodyAnim + ".canUseRotationSpace", lock=True)
        cmds.addAttr(self.bodyAnim, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
        cmds.setAttr(self.bodyAnim + ".canUseTranslationSpace", lock=True)

        # update progress
        if textEdit is not None:
            textEdit.setTextColor(QtGui.QColor(0, 255, 18))
            textEdit.append("        SUCCESS: Pelvis Rig Build Complete!")
            textEdit.setTextColor(QtGui.QColor(255, 255, 255))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildFkSpine(self, textEdit, uiInst, builtRigs, networkNode):
        """
        Builds the FK spine rig.
        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Starting FK Spine Rig Build..")

        # build the rig
        slot = len(builtRigs)

        # find the joints in the spine module that need rigging
        allJnts = self.returnCreatedJoints
        joints = []

        for jnt in allJnts:
            if jnt.find("pelvis") == -1:
                joints.append(jnt)

        fkControls = []
        self.topNode = None
        includePelvis = cmds.getAttr(networkNode + ".includePelvis")

        for joint in joints:
            if joint == joints[0]:
                data = riggingUtils.createControlFromMover(joint, networkNode, True, True,
                                                           control_type="fk_rig_control")

                fkControl = cmds.rename(data[0], "fk_" + joint + "_anim")
                animGrp = cmds.rename(data[1], "fk_" + joint + "_anim_grp")
                spaceSwitcher = cmds.rename(data[2], "fk_" + joint + "_anim_space_switcher")
                spaceSwitchFollow = cmds.rename(data[3], "fk_" + joint + "_anim_space_switcher_follow")
                self.topNode = spaceSwitchFollow

                fkControls.append([spaceSwitchFollow, fkControl, joint])
                # color the control
                riggingUtils.colorControl(fkControl, 18)

            else:
                data = riggingUtils.createControlFromMover(joint, networkNode, True, False,
                                                           control_type="fk_rig_control")

                fkControl = cmds.rename(data[0], "fk_" + joint + "_anim")
                animGrp = cmds.rename(data[1], "fk_" + joint + "_anim_grp")

                fkControls.append([animGrp, fkControl, joint])

                # color the control
                riggingUtils.colorControl(fkControl, 18)

        # create hierarchy
        fkControls.reverse()

        for i in range(len(fkControls)):
            try:
                cmds.parent(fkControls[i][0], fkControls[i + 1][1])
            except IndexError:
                pass

        # =======================================================================
        # #lastly, connect controls up to blender nodes to drive driver joints
        # =======================================================================
        for each in fkControls:
            control = each[1]
            joint = each[2]

            cmds.parentConstraint(control, "driver_" + joint, mo=True)

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
        fkSpineParent = self.bodyAnim
        if includePelvis:
            cmds.parent(self.topNode, self.bodyAnim)
        else:
            cmds.parent(self.topNode, self.spineCtrlGrp)
            fkSpineParent = self.spineCtrlGrp

        # lock attrs
        for each in fkControls:
            control = each[1]
            for attr in [".visibility"]:
                cmds.setAttr(control + attr, lock=True, keyable=False)

        fkRigData = []
        for each in fkControls:
            fkRigData.append(each[1])

        # get controlNode
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        # add fk controls to control node
        if not cmds.objExists(controlNode + ".fkControls"):
            cmds.addAttr(controlNode, sn="fkControls", at="message")

        # add proxy attributes for mode
        if cmds.objExists(self.spineSettings + ".mode"):
            for node in fkRigData:
                cmds.addAttr(node, ln="mode", proxy=self.spineSettings + ".mode", at="double", keyable=True)

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

        return [spaceSwitchFollow]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildIKSpine(self, textEdit, uiInst, builtRigs, networkNode):
        """
        Builds the IK spine rig.
        """

        # update progress
        if textEdit is not None:
            textEdit.append("        Starting IK Spine Rig Build..")

        slot = len(builtRigs)

        # find the joints in the spine module that need rigging
        allJnts = self.returnCreatedJoints
        joints = []

        for jnt in allJnts:
            if jnt.find("pelvis") == -1:
                joints.append(jnt)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Start SplineIK creation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        if len(joints) > 2:
            # duplicate the spine joints we'll need for the spline IK

            parent = None
            rigJoints = []

            for joint in joints:
                spineBone = cmds.duplicate(joint, parentOnly=True, name="splineIK_" + joint)[0]

                if parent != None:
                    cmds.parent(spineBone, parent)

                else:
                    cmds.parent(spineBone, world=True)

                parent = spineBone
                rigJoints.append(str(spineBone))

            # create spine twist joints that will be children of the spline IK joints. This will allow us to control
            # twist distribution directly
            for joint in rigJoints:
                twistJoint = cmds.duplicate(joint, name="twist_" + joint, parentOnly=True)[0]
                cmds.parent(twistJoint, joint)

            # find the driver top and mid joints
            topDriverJoint = "driver_" + joints[-1]
            midDriverJoint = "driver_" + joints[len(joints) / 2]

            ###########################################################################################################
            ###########################################################################################################
            # create the spline IK
            ###########################################################################################################
            ###########################################################################################################

            ikNodes = cmds.ikHandle(sj=str(rigJoints[0]), ee=str(rigJoints[len(rigJoints) - 1]), sol="ikSplineSolver",
                                    createCurve=True, simplifyCurve=True, parentCurve=False,
                                    name=str(rigJoints[0]) + "_splineIK")
            ikHandle = ikNodes[0]
            ikCurve = ikNodes[2]
            ikCurve = cmds.rename(ikCurve, self.name + "_spine_splineIK_curve")
            cmds.setAttr(ikCurve + ".inheritsTransform", 0)
            cmds.setAttr(ikHandle + ".v", 0)
            cmds.setAttr(ikCurve + ".v", 0)

            # create the three joints to skin the curve to
            botJoint = cmds.duplicate(rigJoints[0], name=self.name + "_splineIK_bot_jnt", parentOnly=True)[0]
            topJoint = \
                cmds.duplicate(rigJoints[len(rigJoints) - 1], name=self.name + "_splineIK_top_jnt", parentOnly=True)[0]
            midJoint = cmds.duplicate(topJoint, name=self.name + "_splineIK_mid_jnt", parentOnly=True)[0]

            cmds.parent([botJoint, topJoint, midJoint], world=True)

            constraint = cmds.pointConstraint([botJoint, topJoint], midJoint)[0]
            cmds.delete(constraint)

            # any joint that is not the bottom or top joint needs to be point constrained to be evenly spread
            drivenConsts = []
            if len(joints) == 3:
                drivenConst1 = cmds.pointConstraint([midJoint, rigJoints[1]], "twist_" + rigJoints[1], mo=True)[0]
                cmds.setAttr(drivenConst1 + "." + rigJoints[1] + "W1", 0)
                drivenConsts.append(drivenConst1)

            if len(joints) == 4:
                drivenConst1 = \
                    cmds.pointConstraint([botJoint, midJoint, rigJoints[1]], "twist_" + rigJoints[1], mo=True)[0]
                drivenConst2 = \
                    cmds.pointConstraint([topJoint, midJoint, rigJoints[2]], "twist_" + rigJoints[2], mo=True)[0]

                cmds.setAttr(drivenConst1 + "." + rigJoints[1] + "W2", 0)
                cmds.setAttr(drivenConst2 + "." + rigJoints[2] + "W2", 0)
                drivenConsts.append(drivenConst1)
                drivenConsts.append(drivenConst2)

            if len(joints) == 5:
                drivenConst1 = \
                    cmds.pointConstraint([botJoint, midJoint, rigJoints[1]], "twist_" + rigJoints[1], mo=True)[0]
                drivenConst2 = cmds.pointConstraint([midJoint, rigJoints[2]], "twist_" + rigJoints[2], mo=True)[0]
                drivenConst3 = \
                    cmds.pointConstraint([midJoint, topJoint, rigJoints[3]], "twist_" + rigJoints[3], mo=True)[0]

                cmds.setAttr(drivenConst1 + "." + rigJoints[1] + "W2", 0)
                cmds.setAttr(drivenConst2 + "." + rigJoints[2] + "W1", 0)
                cmds.setAttr(drivenConst3 + "." + rigJoints[3] + "W2", 0)

                drivenConsts.append(drivenConst1)
                drivenConsts.append(drivenConst2)
                drivenConsts.append(drivenConst3)

            # skin the joints to the curve
            cmds.select([botJoint, topJoint, midJoint])
            skin = cmds.skinCluster([botJoint, topJoint, midJoint], ikCurve, toSelectedBones=True)[0]

            # skin weight the curve
            curveShape = cmds.listRelatives(ikCurve, shapes=True)[0]
            numSpans = cmds.getAttr(curveShape + ".spans")
            degree = cmds.getAttr(curveShape + ".degree")
            numCVs = numSpans + degree

            # this should always be the case, but just to be safe
            if numCVs == 4:
                cmds.skinPercent(skin, ikCurve + ".cv[0]", transformValue=[(botJoint, 1.0)])
                cmds.skinPercent(skin, ikCurve + ".cv[1]", transformValue=[(botJoint, 0.5), (midJoint, 0.5)])
                cmds.skinPercent(skin, ikCurve + ".cv[2]", transformValue=[(midJoint, 0.5), (topJoint, 0.5)])
                cmds.skinPercent(skin, ikCurve + ".cv[3]", transformValue=[(topJoint, 1.0)])

            ###########################################################################################################
            ###########################################################################################################
            # create the spline IK controls
            ###########################################################################################################
            ###########################################################################################################

            ikControls = []

            ###############################################
            # TOP CTRL
            ###############################################

            data = riggingUtils.createControlFromMover(joints[-1], networkNode, True, True,
                                                       control_type="ik_rig_control")

            topCtrl = cmds.rename(data[0], self.name + "_chest_ik_anim")
            animGrp = cmds.rename(data[1], self.name + "_chest_ik_anim_grp")
            driverGrp = cmds.duplicate(animGrp, parentOnly=True, name=self.name + "_chest_ik_anim_driver_grp")[0]
            spaceSwitcher = cmds.rename(data[2], self.name + "_chest_ik_anim_space_switcher")
            spaceSwitchFollow = cmds.rename(data[3], self.name + "_chest_ik_anim_space_switcher_follow")

            self.topNode = spaceSwitchFollow

            ikControls.append([spaceSwitchFollow, topCtrl, joints[-1]])

            cmds.parent(driverGrp, animGrp)
            cmds.parent(topCtrl, driverGrp)
            cmds.parent(topJoint, topCtrl)

            # color the control
            riggingUtils.colorControl(topCtrl, 17)

            ###############################################
            # MID CTRL
            ###############################################

            data = riggingUtils.createControlFromMover(joints[len(joints) / 2], networkNode, True, False,
                                                       control_type="ik_rig_control")

            midCtrl = cmds.rename(data[0], self.name + "_mid_ik_anim")
            midGrp = cmds.rename(data[1], self.name + "_mid_ik_anim_grp")
            midDriver = cmds.duplicate(midGrp, parentOnly=True, name=self.name + "_mid_ik_anim_driver_grp")[0]
            midDriverTrans = cmds.duplicate(midGrp, parentOnly=True,
                                            name=self.name + "_mid_ik_anim_trans_driver_grp")[0]

            cmds.parent(midCtrl, midDriver)
            cmds.parent(midDriver, midDriverTrans)
            cmds.parent(midDriverTrans, midGrp)
            cmds.parent(midJoint, midCtrl)
            ikControls.append([midGrp, midCtrl, joints[len(joints) / 2]])

            # color the control
            riggingUtils.colorControl(midCtrl, 25)

            ###############################################
            # BOT CTRL
            ###############################################
            includePelvis = cmds.getAttr(networkNode + ".includePelvis")

            if includePelvis:
                cmds.parent(botJoint, self.hipAnim)

            else:
                cmds.parent(botJoint, self.spineCtrlGrp)

            ###########################################################################################################
            ###########################################################################################################
            # ADDING STRETCH
            ###########################################################################################################
            ###########################################################################################################

            # add the attr to the top ctrl
            cmds.addAttr(topCtrl, longName='stretch', defaultValue=0, minValue=0, maxValue=1, keyable=True)
            cmds.addAttr(topCtrl, longName='squash', defaultValue=0, minValue=0, maxValue=1, keyable=True)

            # create the curveInfo node#find
            cmds.select(ikCurve)
            curveInfoNode = cmds.arclen(cmds.ls(sl=True), ch=True, name=self.name + "_splineIK_curveInfo")
            originalLength = cmds.getAttr(curveInfoNode + ".arcLength")

            # create the multiply/divide node that will get the scale factor
            divideNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_splineIK_scaleFactor")
            divideNode_Inverse = cmds.shadingNode("multiplyDivide", asUtility=True,
                                                  name=self.name + "_splineIK_inverse")
            cmds.setAttr(divideNode + ".operation", 2)
            cmds.setAttr(divideNode + ".input2X", originalLength)
            cmds.setAttr(divideNode_Inverse + ".operation", 2)
            cmds.setAttr(divideNode_Inverse + ".input1X", originalLength)

            # create the blendcolors node
            blenderNode = cmds.shadingNode("blendColors", asUtility=True, name=self.name + "_splineIK_blender")
            cmds.setAttr(blenderNode + ".color2R", 1)

            blenderNode_Inverse = cmds.shadingNode("blendColors", asUtility=True,
                                                   name=self.name + "_splineIK_blender_inverse")
            cmds.setAttr(blenderNode_Inverse + ".color2R", 1)
            squashFactor = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_squash_mult")
            cmds.setAttr(squashFactor + ".input2X", 0.5)

            # connect attrs
            cmds.connectAttr(curveInfoNode + ".arcLength", divideNode + ".input1X")
            cmds.connectAttr(curveInfoNode + ".arcLength", divideNode_Inverse + ".input2X")
            cmds.connectAttr(divideNode + ".outputX", blenderNode + ".color1R")
            cmds.connectAttr(divideNode_Inverse + ".outputX", blenderNode_Inverse + ".color1R")

            cmds.connectAttr(topCtrl + ".stretch", blenderNode + ".blender")
            cmds.connectAttr(topCtrl + ".squash", squashFactor + ".input1X")
            cmds.connectAttr(squashFactor + ".outputX", blenderNode_Inverse + ".blender")

            # apply squash and stretch to joints
            for i in range(len(rigJoints)):
                children = cmds.listRelatives(rigJoints[i], children=True)
                for child in children:
                    if child.find("twist") != -1:
                        twistJoint = child

                cmds.connectAttr(blenderNode_Inverse + ".outputR", twistJoint + ".scaleY")
                cmds.connectAttr(blenderNode_Inverse + ".outputR", twistJoint + ".scaleZ")

            cmds.connectAttr(blenderNode + ".outputR", rigJoints[0] + ".scaleX")

            # setup drivenConst to only be active when stretch is on
            for const in drivenConsts:
                targets = cmds.getAttr(const + ".target", mi=True)
                for each in targets:
                    attr = cmds.listConnections(const + ".target[" + str(each) + "].targetWeight", p=True)

                    cmds.setAttr(topCtrl + ".stretch", 1)
                    cmds.setDrivenKeyframe(attr[0], cd=topCtrl + ".stretch")

                    cmds.setAttr(topCtrl + ".stretch", 0)
                    if len(joints) == 3:
                        if const == drivenConst1:
                            if each == targets[0]:
                                cmds.setAttr(attr[0], 0)
                            if each == targets[1]:
                                cmds.setAttr(attr[0], 1)

                    if len(joints) == 4:
                        if each == targets[2]:
                            cmds.setAttr(attr[0], 1)
                        else:
                            cmds.setAttr(attr[0], 0)

                    if len(joints) == 5:
                        if const == drivenConst1:
                            if each == targets[2]:
                                cmds.setAttr(attr[0], 1)
                            else:
                                cmds.setAttr(attr[0], 0)

                        if const == drivenConst2:
                            if each == targets[1]:
                                cmds.setAttr(attr[0], 1)
                            else:
                                cmds.setAttr(attr[0], 0)

                        if const == drivenConst3:
                            if each == targets[2]:
                                cmds.setAttr(attr[0], 1)
                            else:
                                cmds.setAttr(attr[0], 0)

                    cmds.setDrivenKeyframe(attr[0], cd=topCtrl + ".stretch")

            ###########################################################################################################
            ###########################################################################################################
            # ADDING TWiST
            ###########################################################################################################
            ###########################################################################################################

            # add twist amount attrs and setup
            cmds.select(topCtrl)
            cmds.addAttr(longName='twist_amount', defaultValue=1, minValue=0, keyable=True)

            # find number of spine joints and divide 1 by numSpineJoints
            num = len(joints)
            val = 1.0 / float(num)
            twistamount = val

            locGrp = cmds.group(empty=True, name=self.name + "_spineIK_twist_grp")
            if includePelvis:
                cmds.parent(locGrp, self.bodyAnim)

            else:
                cmds.parent(locGrp, self.spineCtrlGrp)

            for i in range(int(num - 1)):

                # create a locator that will be orient constrained between the body and chest
                locator = cmds.spaceLocator(name=joints[i] + "_twistLoc")[0]
                group = cmds.group(empty=True, name=joints[i] + "_twistLocGrp")
                constraint = cmds.parentConstraint(joints[i], locator)[0]
                cmds.delete(constraint)
                constraint = cmds.parentConstraint(joints[i], group)[0]
                cmds.delete(constraint)
                cmds.parent(locator, group)
                cmds.parent(group, locGrp)
                cmds.setAttr(locator + ".v", 0, lock=True)

                # duplicate the locator and parent it under the group. This will be the locator that takes the rotation
                # x twist amount and gives us the final value

                orientLoc = cmds.duplicate(locator, name=joints[i] + "_orientLoc")[0]
                cmds.parent(orientLoc, locator)
                cmds.makeIdentity(orientLoc, t=1, r=1, s=1, apply=True)

                # set weights on constraint
                firstValue = 1 - twistamount
                secondValue = 1 - firstValue

                # create constraints between body/chest
                if includePelvis:
                    constraint = cmds.orientConstraint([self.bodyAnim, topCtrl], locator)[0]
                    cmds.setAttr(constraint + "." + self.bodyAnim + "W0", firstValue)
                    cmds.setAttr(constraint + "." + topCtrl + "W1", secondValue)

                else:
                    # find module's parent bone
                    constraint = cmds.orientConstraint([rigJoints[i], topCtrl], locator)[0]
                    cmds.setAttr(constraint + "." + rigJoints[i] + "W0", firstValue)
                    cmds.setAttr(constraint + "." + topCtrl + "W1", secondValue)

                # factor in twist amount
                twistMultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=joints[i] + "_twist_amount")

                # expose the twistAmount on the control as an attr
                cmds.connectAttr(topCtrl + ".twist_amount", twistMultNode + ".input2X")
                cmds.connectAttr(topCtrl + ".twist_amount", twistMultNode + ".input2Y")
                cmds.connectAttr(topCtrl + ".twist_amount", twistMultNode + ".input2Z")
                cmds.connectAttr(locator + ".rotate", twistMultNode + ".input1")

                cmds.connectAttr(twistMultNode + ".output", orientLoc + ".rotate")

                # constrain the spine joint to the orientLoc
                skipped = ["y", "z"]

                cmds.orientConstraint([locator, rigJoints[i]], orientLoc, mo=True)
                cmds.orientConstraint(orientLoc, "twist_splineIK_" + joints[i])
                twistamount = twistamount + val

            # =======================================================================
            # #connect controls up to blender nodes to drive driver joints
            # =======================================================================
            ik_jnt_follow_nodes = []
            for joint in joints:
                ik_jnt_follow = cmds.group(empty=True, name=joint + "_ik_follow")
                ik_jnt_follow_nodes.append(ik_jnt_follow)
                rigJnt = "twist_splineIK_" + joint

                cmds.pointConstraint(rigJnt, ik_jnt_follow)

                if joint == joints[len(joints) - 1]:
                    cmds.orientConstraint(topJoint, ik_jnt_follow)
                else:
                    cmds.orientConstraint(rigJnt, ik_jnt_follow)

                cmds.parentConstraint(ik_jnt_follow, "driver_" + joint, mo=True)

                # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale
                # into input 2, and plugs that into driver joint
                if cmds.objExists("master_anim"):
                    globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=joint + "_globalScale")
                    cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
                    cmds.connectAttr(rigJnt + ".scale", globalScaleMult + ".input2")
                    riggingUtils.createConstraint(globalScaleMult, "driver_" + joint, "scale", False, 2, slot, "output")
                else:
                    riggingUtils.createConstraint(rigJnt, "driver_" + joint, "scale", False, 2, slot)

            # =======================================================================
            # #clean things up
            # =======================================================================

            # parent the components to the body anim or parent module bone

            if includePelvis:
                cmds.parent(midGrp, self.bodyAnim)
            else:
                cmds.parent(midGrp, self.spineCtrlGrp)

            # ensure after parenting the midGrp that everything is still nice and zeroed out.
            cmds.parent(midCtrl, world=True)
            cmds.parent(midJoint, world=True)

            for attr in [".rx", ".ry", ".rz"]:
                cmds.setAttr(midGrp + attr, 0)

            cmds.parent(midCtrl, midDriver)
            cmds.makeIdentity(midCtrl, t=1, r=1, s=0, apply=True)
            cmds.parent(midJoint, midCtrl)

            # parent the chest ik space switcher follow node to the body anim or parent module bone
            if includePelvis:
                cmds.parent(spaceSwitchFollow, self.bodyAnim)
            else:
                cmds.parent(spaceSwitchFollow, self.spineCtrlGrp)

            # ensure after parenting the space switcher follow for the ik chest, that everything is still nice and
            # zeroed out.
            cmds.parent(topCtrl, world=True)
            cmds.parent(topJoint, world=True)
            for attr in [".rx", ".ry", ".rz"]:
                if cmds.getAttr(spaceSwitchFollow + attr) < 45:
                    if cmds.getAttr(spaceSwitchFollow + attr) > 0:
                        cmds.setAttr(spaceSwitchFollow + attr, 0)

                if cmds.getAttr(spaceSwitchFollow + attr) >= 80:
                    if cmds.getAttr(spaceSwitchFollow + attr) < 90:
                        cmds.setAttr(spaceSwitchFollow + attr, 90)

                if cmds.getAttr(spaceSwitchFollow + attr) > 90:
                    if cmds.getAttr(spaceSwitchFollow + attr) < 100:
                        cmds.setAttr(spaceSwitchFollow + attr, 90)

                if cmds.getAttr(spaceSwitchFollow + attr) <= -80:
                    if cmds.getAttr(spaceSwitchFollow + attr) > -90:
                        cmds.setAttr(spaceSwitchFollow + attr, -90)

                if cmds.getAttr(spaceSwitchFollow + attr) > -90:
                    if cmds.getAttr(spaceSwitchFollow + attr) < -100:
                        cmds.setAttr(spaceSwitchFollow + attr, -90)

            cmds.parent(topCtrl, driverGrp)
            cmds.makeIdentity(topCtrl, t=1, r=1, s=0, apply=True)
            cmds.parent(topJoint, topCtrl)

            # =======================================================================
            # #ensure top spine joint stays pinned to top ctrl
            # =======================================================================

            children = cmds.listRelatives(rigJoints[len(rigJoints) - 1], children=True)
            for child in children:
                if child.find("twist") != -1:
                    twistJoint = child

            topSpineBone = twistJoint.partition("twist_")[2]
            topSpineJointConstraint = cmds.pointConstraint([topJoint, topSpineBone], twistJoint)[0]

            # connect attr on top spine joint constraint
            targets = cmds.pointConstraint(topSpineJointConstraint, q=True, weightAliasList=True)

            cmds.connectAttr(topCtrl + ".stretch", topSpineJointConstraint + "." + targets[0])

            conditionNode = cmds.shadingNode("condition", asUtility=True, name=self.name + "_twist_stretch_toggle")
            cmds.connectAttr(topCtrl + ".stretch", conditionNode + ".firstTerm")
            cmds.setAttr(conditionNode + ".secondTerm", 1)
            cmds.setAttr(conditionNode + ".colorIfTrueR", 0)

            minusNode = cmds.shadingNode("plusMinusAverage", asUtility=True, name=self.name + "_twist_stretch_minus")
            cmds.setAttr(minusNode + ".operation", 2)
            cmds.connectAttr(conditionNode + ".secondTerm", minusNode + ".input1D[0]")
            cmds.connectAttr(topCtrl + ".stretch", minusNode + ".input1D[1]")
            cmds.connectAttr(minusNode + ".output1D", topSpineJointConstraint + "." + targets[1])

            # =======================================================================
            # #create stretch meter attr
            # =======================================================================
            cmds.addAttr(topCtrl, longName='stretchFactor', keyable=True)
            cmds.connectAttr(divideNode + ".outputX", topCtrl + ".stretchFactor")
            cmds.setAttr(topCtrl + ".stretchFactor", lock=True)

            cmds.addAttr(midCtrl, longName='stretchFactor', keyable=True)
            cmds.connectAttr(topCtrl + ".stretchFactor", midCtrl + ".stretchFactor")
            cmds.setAttr(midCtrl + ".stretchFactor", lock=True)

            # =======================================================================
            # #lock and hide attrs that should not be keyable
            # =======================================================================

            for control in [topCtrl, midCtrl]:
                for attr in [".sx", ".sy", ".sz", ".v"]:
                    cmds.setAttr(control + attr, keyable=False, lock=True)

            # =======================================================================
            # #organize scene
            # =======================================================================
            IKgrp = cmds.group(empty=True, name=self.name + "_ik_grp")
            cmds.parent(IKgrp, self.spineCtrlGrp)

            cmds.parent(ikCurve, IKgrp)
            cmds.parent(ikHandle, IKgrp)
            cmds.parent(rigJoints[0], IKgrp)
            for each in ik_jnt_follow_nodes:
                cmds.parent(each, IKgrp)

            for jnt in rigJoints:
                cmds.setAttr(jnt + ".v", 0, lock=True)

            for jnt in [botJoint, midJoint, topJoint]:
                cmds.setAttr(jnt + ".v", 0, lock=True)

            # =======================================================================
            # #create matching nodes
            # =======================================================================
            chest_match_node = cmds.duplicate(topCtrl, po=True, name=topCtrl + "_MATCH")
            cmds.parent(chest_match_node, topDriverJoint)

            mid_match_node = cmds.duplicate(midCtrl, po=True, name=midCtrl + "_MATCH")
            cmds.parent(mid_match_node, midDriverJoint)

            # =======================================================================
            # #setup auto spine
            # =======================================================================
            self.setupAutoSpine(textEdit, uiInst, builtRigs, networkNode, midDriver, midDriverTrans, topCtrl, botJoint)

            # get controlNode
            controlNode = cmds.listConnections(networkNode + ".controls")[0]

            # add fk controls to control node
            if not cmds.objExists(controlNode + ".ikControls"):
                cmds.addAttr(controlNode, sn="ikControls", at="message")

            # add proxy attributes for mode
            if cmds.objExists(self.spineSettings + ".mode"):
                for node in [topCtrl, midCtrl]:
                    cmds.addAttr(node, ln="mode", proxy=self.spineSettings + ".mode", at="double", keyable=True)

            for node in [topCtrl, midCtrl]:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".ikControls", node + ".controlClass")

                # add controlType info
                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "IK", type="string")

            cmds.addAttr(topCtrl, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
            cmds.setAttr(topCtrl + ".hasSpaceSwitching", lock=True)
            cmds.addAttr(topCtrl, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(topCtrl + ".canUseRotationSpace", lock=True)
            cmds.addAttr(topCtrl, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(topCtrl + ".canUseTranslationSpace", lock=True)

            # update progress
            if textEdit is not None:
                textEdit.setTextColor(QtGui.QColor(0, 255, 18))
                textEdit.append("        SUCCESS: IK Build Complete!")
                textEdit.setTextColor(QtGui.QColor(255, 255, 255))

            return [spaceSwitchFollow, midGrp]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setupAutoSpine(self, textEdit, uiInst, builtRigs, networkNode, midDriver, midDriverTrans, topCtrl, botJnt):
        """
        Sets up auto-spine for the IK mid control.
        """

        cmds.addAttr(topCtrl, longName='autoSpine', defaultValue=0, minValue=0, maxValue=1, keyable=True)
        cmds.addAttr(topCtrl, longName='rotationInfluence', defaultValue=.25, minValue=0, maxValue=1, keyable=True)

        topCtrlMultRY = cmds.shadingNode("multiplyDivide", asUtility=True,
                                         name=self.name + "_autoSpine_top_driver_mult_ry")
        topCtrlMultRZ = cmds.shadingNode("multiplyDivide", asUtility=True,
                                         name=self.name + "_autoSpine_top_driver_mult_rz")
        topCtrlMultSwitchRY = cmds.shadingNode("multiplyDivide", asUtility=True,
                                               name=self.name + "_autoSpine_top_mult_switch_ry")
        topCtrlMultSwitchRZ = cmds.shadingNode("multiplyDivide", asUtility=True,
                                               name=self.name + "_autoSpine_top_mult_switch_rz")

        # =======================================================================
        # create a node that will track all world space translations and rotations on the chest IK anim
        # =======================================================================
        chestMasterTrackNode = cmds.spaceLocator(name=self.name + "_chest_ik_track_parent")[0]
        constraint = cmds.parentConstraint(topCtrl, chestMasterTrackNode)[0]
        cmds.delete(constraint)

        chestTrackNode = cmds.spaceLocator(name=self.name + "_chest_ik_tracker")[0]
        constraint = cmds.parentConstraint(topCtrl, chestTrackNode)[0]
        cmds.delete(constraint)

        cmds.parent(chestTrackNode, chestMasterTrackNode)
        cmds.parentConstraint(topCtrl, chestTrackNode)

        if cmds.getAttr(networkNode + ".includePelvis"):
            cmds.parent(chestMasterTrackNode, self.bodyAnim)
        else:
            cmds.parent(chestMasterTrackNode, self.spineCtrlGrp)

        # hide locator
        cmds.setAttr(chestMasterTrackNode + ".v", 0)

        botJntLoc = cmds.group(empty=True, name=self.name + "_botJnt_tracker")
        constraint = cmds.parentConstraint(botJnt, botJntLoc)[0]
        cmds.delete(constraint)
        cmds.parent(botJntLoc, botJnt)
        cmds.makeIdentity(botJntLoc, t=1, r=1, s=1, apply=True)
        cmds.parentConstraint(botJnt, botJntLoc)[0]

        # =======================================================================
        # Rotate Y
        # =======================================================================
        cmds.connectAttr(chestTrackNode + ".ry", topCtrlMultRY + ".input1X")
        cmds.connectAttr(topCtrl + ".rotationInfluence", topCtrlMultRY + ".input2X")

        cmds.connectAttr(topCtrlMultRY + ".outputX", topCtrlMultSwitchRY + ".input1X")
        cmds.connectAttr(topCtrl + ".autoSpine", topCtrlMultSwitchRY + ".input2X")
        cmds.connectAttr(topCtrlMultSwitchRY + ".outputX", midDriver + ".tz")

        # =======================================================================
        # Rotate Z
        # =======================================================================
        multInverse = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_autoSpine_mult_rz_inverse")
        cmds.connectAttr(topCtrl + ".rotationInfluence", multInverse + ".input1X")
        cmds.setAttr(multInverse + ".input2X", -1)

        cmds.connectAttr(chestTrackNode + ".rz", topCtrlMultRZ + ".input1X")
        cmds.connectAttr(multInverse + ".outputX", topCtrlMultRZ + ".input2X")

        cmds.connectAttr(topCtrlMultRZ + ".outputX", topCtrlMultSwitchRZ + ".input1X")
        cmds.connectAttr(topCtrl + ".autoSpine", topCtrlMultSwitchRZ + ".input2X")
        cmds.connectAttr(topCtrlMultSwitchRZ + ".outputX", midDriver + ".ty")

        # =======================================================================
        # Translate X
        # =======================================================================

        # Chest Control Translate X + Hip Control Translate X / 2 * autpSpine
        autoSpineTXNode = cmds.shadingNode("plusMinusAverage", asUtility=True, name=midDriverTrans + "_TX_Avg")
        cmds.setAttr(autoSpineTXNode + ".operation", 3)
        autoSpineTX_MultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=midDriverTrans + "_TX_Mult")

        cmds.connectAttr(topCtrl + ".translateX", autoSpineTXNode + ".input1D[0]")
        cmds.connectAttr(botJntLoc + ".translateX", autoSpineTXNode + ".input1D[1]")
        cmds.connectAttr(autoSpineTXNode + ".output1D", autoSpineTX_MultNode + ".input1X")
        cmds.connectAttr(topCtrl + ".autoSpine", autoSpineTX_MultNode + ".input2X")
        cmds.connectAttr(autoSpineTX_MultNode + ".outputX", midDriverTrans + ".translateX")

        # =======================================================================
        # Translate Y
        # =======================================================================
        autoSpineTYNode = cmds.shadingNode("plusMinusAverage", asUtility=True, name=midDriverTrans + "_TY_Avg")
        cmds.setAttr(autoSpineTYNode + ".operation", 3)
        autoSpineTY_MultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=midDriverTrans + "_TY_Mult")

        cmds.connectAttr(chestTrackNode + ".translateY", autoSpineTYNode + ".input1D[0]")
        cmds.connectAttr(botJntLoc + ".translateY", autoSpineTYNode + ".input1D[1]")
        cmds.connectAttr(autoSpineTYNode + ".output1D", autoSpineTY_MultNode + ".input1X")
        cmds.connectAttr(topCtrl + ".autoSpine", autoSpineTY_MultNode + ".input2X")
        cmds.connectAttr(autoSpineTY_MultNode + ".outputX", midDriverTrans + ".translateY")

        # =======================================================================
        # Translate Z
        # =======================================================================
        autoSpineTZNode = cmds.shadingNode("plusMinusAverage", asUtility=True, name=midDriverTrans + "_TZ_Avg")
        cmds.setAttr(autoSpineTZNode + ".operation", 3)
        autoSpineTZ_MultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=midDriverTrans + "_TZ_Mult")

        cmds.connectAttr(chestTrackNode + ".translateZ", autoSpineTZNode + ".input1D[0]")
        cmds.connectAttr(botJntLoc + ".translateZ", autoSpineTZNode + ".input1D[1]")
        cmds.connectAttr(autoSpineTZNode + ".output1D", autoSpineTZ_MultNode + ".input1X")
        cmds.connectAttr(topCtrl + ".autoSpine", autoSpineTZ_MultNode + ".input2X")
        cmds.connectAttr(autoSpineTZ_MultNode + ".outputX", midDriverTrans + ".translateZ")

        cmds.setAttr(topCtrl + ".autoSpine", 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def switchMode(self, mode, checkBox, range=False):
        """
        Switch the rig mode to FK or IK, matching the pose while switching if the checkbox is True.

        :param mode: Which mode to switch to (FK, IK)
        :param checkBox: The match checkbox (if True, match, then switch)
        :param range: Whether to match/switch over range
        """

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        # are we matching?
        if not range:
            match = checkBox.isChecked()
        else:
            match = True

        # if being called from match over frame range
        if range:
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

                # create a duplicate chain
                topCtrl = controls[0]
                topGrp = cmds.listRelatives(topCtrl, parent=True)[0]
                newControls = cmds.duplicate(topGrp)
                cmds.parent(newControls[0], world=True)

                # match the fk controls to the corresponding joint
                for control in controls:
                    joint = control.partition("fk_")[2].partition("_anim")[0]
                    joint = namespace + ":" + joint

                    dupeCtrl = control.partition(namespace + ":")[2]
                    constraint = cmds.parentConstraint(joint, dupeCtrl)[0]

                    translate = cmds.getAttr(dupeCtrl + ".translate")[0]
                    rotate = cmds.getAttr(dupeCtrl + ".rotate")[0]
                    cmds.delete(constraint)

                    cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2],
                                 type='double3')
                    cmds.setAttr(control + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')

                    cmds.setKeyframe(control)

                # delete dupes
                cmds.delete(newControls[0])

                # switch modes
                if not range:
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

        # switch to IK mode
        if mode == "IK":

            # get current mode
            currentMode = cmds.getAttr(namespace + ":" + self.name + "_settings.mode")
            if currentMode == 1.0:
                cmds.warning("Already in IK mode.")
                return

            if not match:
                cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

            if match:

                # get IK controls
                controls = self.getControls(False, "ikControls")

                # Chest
                # create a duplicate chest anim
                control = controls[0]
                topGrp = cmds.listRelatives(control, parent=True)[0]
                newControls = cmds.duplicate(topGrp)
                cmds.parent(newControls[0], world=True)

                # match the chest anim to the last spine joint
                fkControls = self.getControls(False, "fkControls")
                fkControls = sorted(fkControls)

                joint = fkControls[-1].partition("_anim")[0].partition("fk_")[2]
                joint = namespace + ":" + joint

                dupeCtrl = control.partition(namespace + ":")[2]
                constraint = cmds.parentConstraint(joint, dupeCtrl)[0]
                cmds.delete(constraint)

                # this will now give use good values
                translate = cmds.getAttr(dupeCtrl + ".translate")[0]
                rotate = cmds.getAttr(dupeCtrl + ".rotate")[0]

                cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2],
                             type='double3')
                cmds.setAttr(control + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')
                cmds.setKeyframe(control)

                # delete dupes
                cmds.delete(newControls[0])

                # set auto spine off
                cmds.setAttr(control + ".autoSpine", 0)
                cmds.setKeyframe(control + ".autoSpine")

                # Mid Anim
                # create a duplicate mid spine anim
                control = controls[1]
                topGrp = cmds.listRelatives(control, parent=True)[0]
                newControls = cmds.duplicate(topGrp)
                cmds.parent(newControls[0], world=True)

                # match the mid spibne anim to the mid spine joint
                allJnts = self.returnCreatedJoints
                joints = []
                for jnt in allJnts:
                    if jnt.find("pelvis") == -1:
                        joints.append(jnt)

                joint = "driver_" + joints[len(joints) / 2]
                joint = namespace + ":" + joint
                dupeCtrl = control.partition(namespace + ":")[2]

                constraint = cmds.parentConstraint(joint, dupeCtrl)[0]
                cmds.delete(constraint)

                # this will now give use good values
                translate = cmds.getAttr(dupeCtrl + ".translate")[0]
                rotate = cmds.getAttr(dupeCtrl + ".rotate")[0]

                cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2],
                             type='double3')
                cmds.setAttr(control + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')
                cmds.setKeyframe(control)

                # delete dupes
                cmds.delete(newControls[0])

                # switch modes
                if not range:
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

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
    def _toggleButtonState(self):

        state = self.applyButton.isEnabled()
        if state is False:
            self.applyButton.setEnabled(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateOutliner(self):
        """
        Whenever changes are made to the module settings, update the outliner (in the rig creator) to show the new
        or removed movers. Tied to skeletonSettingsUI
        """

        # PELVIS

        if not self.pelvisCB.isChecked():
            self.outlinerWidgets[self.originalName + "_pelvis"].setHidden(True)
        else:
            self.outlinerWidgets[self.originalName + "_pelvis"].setHidden(False)

        # SPINE
        numSpine = self.numSpine.value()
        if numSpine == 2:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(True)
        if numSpine == 3:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(True)
        if numSpine == 4:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(True)
        if numSpine == 5:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createContextMenu(self, point):
        """
        Create the right-click menu for the module.

        :param point: Point on monitor to spawn the right-click menu.
        """

        networkNode = self.returnNetworkNode

        # icons
        icon_reset = QtGui.QIcon(os.path.join(self.iconsPath, "System/reset.png"))
        icon_delete = QtGui.QIcon(os.path.join(self.iconsPath, "System/delete.png"))
        icon_duplicate = QtGui.QIcon(os.path.join(self.iconsPath, "System/duplicate.png"))

        # create the context menu
        if networkNode != "ART_Root_Module":
            self.contextMenu = QtWidgets.QMenu()
            self.contextMenu.addAction(icon_reset, "Reset Settings", self.resetSettings)

            self.contextMenu.addSeparator()

            self.contextMenu.addAction(icon_duplicate, "Duplicate this Module",
                                       partial(self.createMirrorOfModule_UI, "ART_createDuplicateModuleUI",
                                               "Duplicate Module", "DUPLICATE", False, True))

            self.contextMenu.addSeparator()

            self.contextMenu.addAction(icon_delete, "Delete Module", self.deleteModule)
            self.contextMenu.exec_(self.groupBox.mapToGlobal(point))