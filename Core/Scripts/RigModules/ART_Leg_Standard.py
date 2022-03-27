"""
Author: Jeremy Ernst

========
Contents
========

|   **Must Have Methods:**
|       :py:func:`addAttributes <RigModules.ART_Leg_Standard.ART_Leg_Standard.addAttributes>`
|       :py:func:`skeletonSettings_UI <RigModules.ART_Leg_Standard.ART_Leg_Standard.skeletonSettings_UI>`
|       :py:func:`pickerUI <RigModules.ART_Leg_Standard.ART_Leg_Standard.pickerUI>`
|       :py:func:`addJointMoverToOutliner <RigModules.ART_Leg_Standard.ART_Leg_Standard.addJointMoverToOutliner>`
|       :py:func:`updateSettingsUI <RigModules.ART_Leg_Standard.ART_Leg_Standard.updateSettingsUI>`
|       :py:func:`applyModuleChanges <RigModules.ART_Leg_Standard.ART_Leg_Standard.applyModuleChanges>`
|       :py:func:`resetSettings <RigModules.ART_Leg_Standard.ART_Leg_Standard.resetSettings>`
|       :py:func:`pinModule <RigModules.ART_Leg_Standard.ART_Leg_Standard.pinModule>`
|       :py:func:`skinProxyGeo <RigModules.ART_Leg_Standard.ART_Leg_Standard.skinProxyGeo>`
|       :py:func:`buildRigCustom <RigModules.ART_Leg_Standard.ART_Leg_Standard.buildRigCustom>`
|       :py:func:`importFBX <RigModules.ART_Leg_Standard.ART_Leg_Standard.importFBX>`
|       :py:func:`aimMode_Setup <RigModules.ART_Leg_Standard.ART_Leg_Standard.aimMode_Setup>`
|       :py:func:`setupPickWalking <RigModules.ART_Leg_Standard.ART_Leg_Standard.setupPickWalking>`
|
|   **Optional Methods:**
|       :py:func:`importFBX_post <RigModules.ART_Leg_Standard.ART_Leg_Standard.importFBX_post>`
|       :py:func:`mirrorTransformations_Custom <RigModules.ART_Leg_Standard.ART_Leg_Standard.mirrorTransformations_Custom>`
|       :py:func:`selectRigControls <RigModules.ART_Leg_Standard.ART_Leg_Standard.selectRigControls>`
|
|   **Module Specific Methods:**
|       :py:func:`buildIkRig <RigModules.ART_Leg_Standard.ART_Leg_Standard.buildIkRig>`
|       :py:func:`_ik_rig_setup <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_setup>`
|       :py:func:`_ik_rig_foot_ctrl <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_foot_ctrl>`
|       :py:func:`_ik_rig_knee_display <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_knee_display>`
|       :py:func:`_ik_rig_create_foot_joints <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_create_foot_joints>`
|       :py:func:`_ik_rig_create_foot_roll_rig <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_create_foot_roll_rig>`
|       :py:func:`_ik_rig_setup_foot_roll_rig <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_setup_foot_roll_rig>`
|       :py:func:`_ik_rig_complete_foot_roll_rig <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_complete_foot_roll_rig>`
|       :py:func:`_ik_rig_setup_knee_twist <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_setup_knee_twist>`
|       :py:func:`_ik_rig_setup_squash_stretch <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_setup_squash_stretch>`
|       :py:func:`_ik_rig_no_flip_knee <RigModules.ART_Leg_Standard.ART_Leg_Standard._ik_rig_no_flip_knee>`
|       :py:func:`buildToeRigs <RigModules.ART_Leg_Standard.ART_Leg_Standard.buildToeRigs>`
|       :py:func:`_getBallGeo <RigModules.ART_Leg_Standard.ART_Leg_Standard._getBallGeo>`
|       :py:func:`_getLegScale <RigModules.ART_Leg_Standard.ART_Leg_Standard._getLegScale>`
|       :py:func:`_getMainLegJoints <RigModules.ART_Leg_Standard.ART_Leg_Standard._getMainLegJoints>`
|       :py:func:`_getLegTwistJoints <RigModules.ART_Leg_Standard.ART_Leg_Standard._getLegTwistJoints>`
|       :py:func:`includeBallJoint <RigModules.ART_Leg_Standard.ART_Leg_Standard.includeBallJoint>`
|       :py:func:`changeSide <RigModules.ART_Leg_Standard.ART_Leg_Standard.changeSide>`
|       :py:func:`coplanarMode <RigModules.ART_Leg_Standard.ART_Leg_Standard.coplanarMode>`
|       :py:func:`switchMode <RigModules.ART_Leg_Standard.ART_Leg_Standard.switchMode>`
|       :py:func:`ikKneeMatch <RigModules.ART_Leg_Standard.ART_Leg_Standard.ikKneeMatch>`
|
|   **Interface Methods:**
|       :py:func:`_toggleButtonState <RigModules.ART_Leg_Standard.ART_Leg_Standard._toggleButtonState>`
|       :py:func:`_editMetaTarsals <RigModules.ART_Leg_Standard.ART_Leg_Standard._editMetaTarsals>`
|       :py:func:`_editJointMoverViaSpinBox <RigModules.ART_Leg_Standard.ART_Leg_Standard._editJointMoverViaSpinBox>`
|       :py:func:`_editJointMoverTwistBones <RigModules.ART_Leg_Standard.ART_Leg_Standard._editJointMoverTwistBones>`
|       :py:func:`updateOutliner <RigModules.ART_Leg_Standard.ART_Leg_Standard.updateOutliner>`


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
from functools import partial

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.mathUtils as mathUtils
import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils

from Base.ART_RigModule import ART_RigModule
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# file attributes
search = "biped:leg"
className = "ART_Leg_Standard"
jointMover = "Core/JointMover/z_up/ART_Leg_Standard.ma"
baseName = "leg"
displayName = "Leg"
rigs = ["FK::IK"]
fbxImport = ["None", "FK", "IK", "Both"]
matchData = [True, ["Match FK to IK", "Match IK to FK"]]
tooltip_image = "ART_Leg_Standard"


class ART_Leg_Standard(ART_RigModule):
    """
    # class that defines a common biped leg, with an FK and IK rig (where the IK rig is modeled after ARTv1's style)
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

        ART_RigModule.__init__(self, "ART_Leg_Standard_Module", "ART_Leg_Standard", moduleUserName)

        # get up-axis of maya
        self.up = cmds.upAxis(q=True, ax=True)

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
        cmds.setAttr(self.networkNode + ".Created_Bones", "thigh::calf::foot::ball::", type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="baseName", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".baseName", baseName, type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="canAim", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".canAim", True, lock=True)

        cmds.addAttr(self.networkNode, sn="aimMode", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".aimMode", False, lock=True)

        # joint mover settings
        cmds.addAttr(self.networkNode, sn="thighTwists", keyable=False)
        cmds.setAttr(self.networkNode + ".thighTwists", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="calfTwists", keyable=False)
        cmds.setAttr(self.networkNode + ".calfTwists", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="bigToeJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".bigToeJoints", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="bigToeMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".bigToeMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="indexToeJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".indexToeJoints", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="indexToeMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".indexToeMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="middleToeJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".middleToeJoints", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="middleToeMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".middleToeMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="ringToeJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".ringToeJoints", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="ringToeMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".ringToeMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="pinkyToeJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".pinkyToeJoints", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="pinkyToeMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".pinkyToeMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="includeBall", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".includeBall", True, lock=True)

        cmds.addAttr(self.networkNode, sn="side", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".side", "Left", type="string", lock=True)

        # rig creation settings
        cmds.addAttr(self.networkNode, sn="buildFK", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".buildFK", True, lock=True)

        cmds.addAttr(self.networkNode, sn="buildIK_V1", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".buildIK_V1", True, lock=True)

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
        ART_RigModule.skeletonSettings_UI(self, name, 335, 480, True)

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
        self.frame.setMinimumSize(QtCore.QSize(320, 445))
        self.frame.setMaximumSize(QtCore.QSize(320, 445))

        # add layout for custom settings
        self.customSettingsLayout = QtWidgets.QVBoxLayout(self.frame)

        # mirror module
        self.mirrorModLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.mirrorModLayout)
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

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.customSettingsLayout.addItem(spacerItem)

        # current parent
        self.currentParentMod = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.currentParentMod)
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
        self.customSettingsLayout.addLayout(self.buttonLayout)
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

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.customSettingsLayout.addItem(spacerItem)

        # add side settings
        self.sideLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.sideLayout)
        self.sideLabel = QtWidgets.QLabel("Side:    ")
        self.sideLabel.setFont(font)
        self.leftSideBtn = QtWidgets.QRadioButton("Left Side")
        self.rightSideBtn = QtWidgets.QRadioButton("Right Side")
        self.sideLayout.addWidget(self.sideLabel)
        self.sideLayout.addWidget(self.leftSideBtn)
        self.sideLayout.addWidget(self.rightSideBtn)

        text = "Set the module to be configured so that the geometry is for the left side of the character."
        self.leftSideBtn.setToolTip(text)

        text = "Set the module to be configured so that the geometry is for the right side of the character."
        self.rightSideBtn.setToolTip(text)

        # get current side
        if cmds.getAttr(networkNode + ".side") == "Left":
            self.leftSideBtn.setChecked(True)
        if cmds.getAttr(networkNode + ".side") == "Right":
            self.rightSideBtn.setChecked(True)

        self.leftSideBtn.clicked.connect(self.changeSide)
        self.rightSideBtn.clicked.connect(self.changeSide)

        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.customSettingsLayout.addItem(spacerItem)

        # coplanar mode and bake offsets layout
        self.legToolsLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.legToolsLayout)

        # Coplanar mode
        # self.coplanarBtn = QtWidgets.QPushButton("Coplanar Mode")
        # self.coplanarBtn.setObjectName("settings")
        # self.coplanarBtn.setMinimumHeight(30)
        # self.coplanarBtn.setMaximumHeight(30)
        # self.coplanarBtn.setFont(headerFont)
        # self.legToolsLayout.addWidget(self.coplanarBtn)
        # self.coplanarBtn.setCheckable(True)
        # self.coplanarBtn.clicked.connect(self.coplanarMode)
        # text = "[EXPERIMENTAL] Forces leg joints to always be planar for best IK setup."
        # self.coplanarBtn.setToolTip(text)

        # Bake OFfsets
        self.bakeOffsetsBtn = QtWidgets.QPushButton("Bake Offsets")
        self.bakeOffsetsBtn.setObjectName("settings")
        self.bakeOffsetsBtn.setMinimumHeight(30)
        self.bakeOffsetsBtn.setMaximumHeight(30)
        self.bakeOffsetsBtn.setFont(headerFont)
        self.legToolsLayout.addWidget(self.bakeOffsetsBtn)
        self.bakeOffsetsBtn.clicked.connect(self.bakeOffsets)
        text = "Bake the offset mover values up to the global movers to get them aligned."
        self.bakeOffsetsBtn.setToolTip(text)

        # Twist Bones Section
        self.twistSettingsLabel = QtWidgets.QLabel("Twist Bone Settings: ")
        self.twistSettingsLabel.setFont(headerFont)
        self.customSettingsLayout.addWidget(self.twistSettingsLabel)

        self.separatorA = QtWidgets.QFrame()
        self.separatorA.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorA.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.customSettingsLayout.addWidget(self.separatorA)

        # twist bones HBoxLayout
        self.twistBonesLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.twistBonesLayout)

        self.twistForm = QtWidgets.QFormLayout()
        self.thighTwistLabel = QtWidgets.QLabel("Thigh Twists: ")
        self.thighTwistLabel.setFont(font)
        self.twistForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.thighTwistLabel)
        self.thighTwistNum = QtWidgets.QSpinBox()
        self.thighTwistNum.setMaximum(3)
        self.twistForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.thighTwistNum)
        self.twistBonesLayout.addLayout(self.twistForm)

        self.calfForm = QtWidgets.QFormLayout()
        self.calfTwistLabel = QtWidgets.QLabel("Calf Twists: ")
        self.calfTwistLabel.setFont(font)
        self.calfForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.calfTwistLabel)
        self.calfTwistNum = QtWidgets.QSpinBox()
        self.calfTwistNum.setMaximum(3)
        self.calfForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.calfTwistNum)
        self.twistBonesLayout.addLayout(self.calfForm)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.customSettingsLayout.addItem(spacerItem)

        # Feet Settings Section
        self.feetSettingsLabel = QtWidgets.QLabel("Foot Settings: ")
        self.feetSettingsLabel.setFont(headerFont)
        self.customSettingsLayout.addWidget(self.feetSettingsLabel)

        self.separatorB = QtWidgets.QFrame()
        self.separatorB.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorB.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.customSettingsLayout.addWidget(self.separatorB)

        self.ballJoint = QtWidgets.QCheckBox("Include Ball Joint?")
        self.ballJoint.setChecked(True)
        self.customSettingsLayout.addWidget(self.ballJoint)

        # Toe Settings: add VBoxLayout
        self.toeVBoxLayout = QtWidgets.QVBoxLayout()
        self.customSettingsLayout.addLayout(self.toeVBoxLayout)

        # BIG TOE
        self.bigToeLayout = QtWidgets.QHBoxLayout()

        self.bigToeLabel = QtWidgets.QLabel("Big Toe Joints: ")
        self.bigToeLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.bigToeLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.bigToeLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.bigToeLayout.addWidget(self.bigToeLabel)

        self.bigToeNum = QtWidgets.QSpinBox()
        self.bigToeNum.setMaximum(2)
        self.bigToeNum.setMinimumSize(QtCore.QSize(50, 20))
        self.bigToeNum.setMaximumSize(QtCore.QSize(50, 20))
        self.bigToeNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.bigToeLayout.addWidget(self.bigToeNum)

        self.bigToeMeta = QtWidgets.QCheckBox("Include Metatarsal")
        self.bigToeLayout.addWidget(self.bigToeMeta)
        self.toeVBoxLayout.addLayout(self.bigToeLayout)

        # INDEX TOE
        self.indexToeLayout = QtWidgets.QHBoxLayout()

        self.indexToeLabel = QtWidgets.QLabel("Index Toe Joints: ")
        self.indexToeLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.indexToeLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.indexToeLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.indexToeLayout.addWidget((self.indexToeLabel))

        self.indexToeNum = QtWidgets.QSpinBox()
        self.indexToeNum.setMaximum(3)
        self.indexToeNum.setMinimumSize(QtCore.QSize(50, 20))
        self.indexToeNum.setMaximumSize(QtCore.QSize(50, 20))
        self.indexToeNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.indexToeLayout.addWidget((self.indexToeNum))

        self.indexToeMeta = QtWidgets.QCheckBox("Include Metatarsal")
        self.indexToeLayout.addWidget(self.indexToeMeta)
        self.toeVBoxLayout.addLayout(self.indexToeLayout)

        # MIDDLE TOE
        self.middleToeLayout = QtWidgets.QHBoxLayout()

        self.middleToeLabel = QtWidgets.QLabel("Middle Toe Joints: ")
        self.middleToeLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.middleToeLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.middleToeLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.middleToeLayout.addWidget(self.middleToeLabel)

        self.middleToeNum = QtWidgets.QSpinBox()
        self.middleToeNum.setMaximum(3)
        self.middleToeNum.setMinimumSize(QtCore.QSize(50, 20))
        self.middleToeNum.setMaximumSize(QtCore.QSize(50, 20))
        self.middleToeNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.middleToeLayout.addWidget(self.middleToeNum)

        self.middleToeMeta = QtWidgets.QCheckBox("Include Metatarsal")
        self.middleToeLayout.addWidget(self.middleToeMeta)
        self.toeVBoxLayout.addLayout(self.middleToeLayout)

        # RING TOE
        self.ringToeLayout = QtWidgets.QHBoxLayout()

        self.ringToeLabel = QtWidgets.QLabel("Ring Toe Joints: ")
        self.ringToeLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.ringToeLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.ringToeLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.ringToeLayout.addWidget(self.ringToeLabel)

        self.ringToeNum = QtWidgets.QSpinBox()
        self.ringToeNum.setMaximum(3)
        self.ringToeNum.setMinimumSize(QtCore.QSize(50, 20))
        self.ringToeNum.setMaximumSize(QtCore.QSize(50, 20))
        self.ringToeNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.ringToeLayout.addWidget(self.ringToeNum)

        self.ringToeMeta = QtWidgets.QCheckBox("Include Metatarsal")
        self.ringToeLayout.addWidget(self.ringToeMeta)
        self.toeVBoxLayout.addLayout(self.ringToeLayout)

        # PINKY TOE
        self.pinkyToeLayout = QtWidgets.QHBoxLayout()

        self.pinkyToeLabel = QtWidgets.QLabel("Pinky Toe Joints: ")
        self.pinkyToeLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.pinkyToeLabel.setMinimumSize(QtCore.QSize(200, 20))
        self.pinkyToeLabel.setMaximumSize(QtCore.QSize(200, 20))
        self.pinkyToeLayout.addWidget(self.pinkyToeLabel)

        self.pinkyToeNum = QtWidgets.QSpinBox()
        self.pinkyToeNum.setMaximum(3)
        self.pinkyToeNum.setMinimumSize(QtCore.QSize(50, 20))
        self.pinkyToeNum.setMaximumSize(QtCore.QSize(50, 20))
        self.pinkyToeNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pinkyToeLayout.addWidget(self.pinkyToeNum)

        self.pinkyToeMeta = QtWidgets.QCheckBox("Include Metatarsal")
        self.pinkyToeLayout.addWidget(self.pinkyToeMeta)
        self.toeVBoxLayout.addLayout(self.pinkyToeLayout)

        # rebuild button
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
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

        # SIGNALS/SLOTS

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(self.groupBox, QtCore.SIGNAL("toggled(bool)"), self.frame.setVisible)
        self.groupBox.setChecked(False)

        # button signal/slots
        self.changeNameBtn.clicked.connect(partial(self.changeModuleName, baseName, self, self.rigUiInst))
        self.changeParentBtn.clicked.connect(partial(self.changeModuleParent, self, self.rigUiInst))
        self.mirrorModuleBtn.clicked.connect(partial(self.setMirrorModule, self, self.rigUiInst))
        self.applyButton.clicked.connect(partial(self.applyModuleChanges, self))

        # spinBox & checkbox signal/slots
        self.thighTwistNum.valueChanged.connect(self._toggleButtonState)
        self.calfTwistNum.valueChanged.connect(self._toggleButtonState)
        self.bigToeNum.valueChanged.connect(self._toggleButtonState)
        self.indexToeNum.valueChanged.connect(self._toggleButtonState)
        self.middleToeNum.valueChanged.connect(self._toggleButtonState)
        self.ringToeNum.valueChanged.connect(self._toggleButtonState)
        self.pinkyToeNum.valueChanged.connect(self._toggleButtonState)
        self.ballJoint.stateChanged.connect(self._toggleButtonState)
        self.ballJoint.stateChanged.connect(partial(self.includeBallJoint, True))

        self.pinkyToeMeta.stateChanged.connect(self._toggleButtonState)
        self.ringToeMeta.stateChanged.connect(self._toggleButtonState)
        self.middleToeMeta.stateChanged.connect(self._toggleButtonState)
        self.indexToeMeta.stateChanged.connect(self._toggleButtonState)
        self.bigToeMeta.stateChanged.connect(self._toggleButtonState)

        # add custom skeletonUI settings  name, parent, rig types to install, mirror module, thigh twist,
        # calf twists, ball joint, toes,
        # add to the rig cretor UI's module settings layout VBoxLayout
        self.rigUiInst.moduleSettingsLayout.addWidget(self.groupBox)

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
        side = cmds.getAttr(networkNode + ".side")

        # create the picker border item
        if networkNode.find(":") != -1:
            moduleNode = networkNode.partition(":")[2]
        else:
            moduleNode = networkNode

        borderItem = interfaceUtils.pickerBorderItem(center.x() - 75, center.y() - 130, 150, 260, clearBrush,
                                                     moduleNode)

        # get controls
        fkControls = self.getControls(False, "fkControls")
        ikControls = self.getControls(False, "ikV1Controls")
        thighTwistControls = self.getControls(False, "thighTwistControls")
        thighTwistControls = sorted(thighTwistControls)
        calfTwistControls = self.getControls(False, "calfTwistControls")
        calfTwistControls = sorted(calfTwistControls)

        # the upside of writing the controls to a string attr was knowing the order of the controls. The downside to
        # having it be connections is that the return order appears to be kind of random and I have to do shit like this
        fkThighCtrl = None
        fkCalfCtrl = None
        fkFootCtrl = None
        fkBallCtrl = None

        for control in fkControls:
            if "thigh" in control:
                fkThighCtrl = control
            if "calf" in control:
                fkCalfCtrl = control
            if "foot" in control:
                fkFootCtrl = control
            if "ball" in control:
                fkBallCtrl = control

        buttonData = []
        controls = []

        ikFootCtrl = None
        ikHeelCtrl = None
        ikToeWigCtrl = None
        ikToeTipCtrl = None

        for control in ikControls:
            if "heel" in control:
                ikHeelCtrl = control
            if "foot" in control:
                ikFootCtrl = control
            if "wiggle" in control:
                ikToeWigCtrl = control
            if "tip" in control:
                ikToeTipCtrl = control

        # create the picker buttons
        # ik buttons
        ikFootBtn = interfaceUtils.pickerButton(30, 30, [30, 225], ikFootCtrl, yellowBrush, borderItem)
        buttonData.append([ikFootBtn, ikFootCtrl, yellowBrush])
        controls.append(ikFootCtrl)

        ikHeelBtn = interfaceUtils.pickerButton(20, 20, [5, 235], ikHeelCtrl, yellowBrush, borderItem)
        buttonData.append([ikHeelBtn, ikHeelCtrl, yellowBrush])
        controls.append(ikHeelCtrl)

        ikToeTipBtn = interfaceUtils.pickerButton(20, 20, [135, 235], ikToeTipCtrl, yellowBrush,
                                                  borderItem)
        buttonData.append([ikToeTipBtn, ikToeTipCtrl, yellowBrush])
        controls.append(ikToeTipCtrl)

        ikToeWiggleBtn = interfaceUtils.pickerButton(20, 20, [97, 200], ikToeWigCtrl, yellowBrush,
                                                     borderItem)
        buttonData.append([ikToeWiggleBtn, ikToeWigCtrl, yellowBrush])
        controls.append(ikToeWigCtrl)

        # fk buttons
        fkThighBtn = interfaceUtils.pickerButton(30, 100, [30, 10], fkThighCtrl, blueBrush, borderItem)
        buttonData.append([fkThighBtn, fkThighCtrl, blueBrush])
        controls.append(fkThighCtrl)

        fkCalfBtn = interfaceUtils.pickerButton(30, 90, [30, 122], fkCalfCtrl, blueBrush, borderItem)
        buttonData.append([fkCalfBtn, fkCalfCtrl, blueBrush])
        controls.append(fkCalfCtrl)

        fkFootBtn = interfaceUtils.pickerButton(30, 30, [62, 225], fkFootCtrl, blueBrush, borderItem)
        buttonData.append([fkFootBtn, fkFootCtrl, blueBrush])
        controls.append(fkFootCtrl)

        if len(fkControls) == 4:
            fkBallBtn = interfaceUtils.pickerButton(30, 30, [97, 225], fkBallCtrl, blueBrush, borderItem)
            buttonData.append([fkBallBtn, fkBallCtrl, blueBrush])
            controls.append(fkBallCtrl)

        # thigh twists
        if thighTwistControls is not None:
            if len(thighTwistControls) > 0:
                y = 20
                for i in range(len(thighTwistControls)):
                    button = interfaceUtils.pickerButton(20, 20, [5, y], thighTwistControls[i], purpleBrush,
                                                         borderItem)
                    buttonData.append([button, thighTwistControls[i], purpleBrush])
                    controls.append(thighTwistControls[i])
                    y = y + 30

        if calfTwistControls is not None:
            if len(calfTwistControls) > 0:
                y = 192
                for i in range(len(calfTwistControls)):
                    button = interfaceUtils.pickerButton(20, 20, [5, y], calfTwistControls[i], purpleBrush,
                                                         borderItem)
                    buttonData.append([button, calfTwistControls[i], purpleBrush])
                    controls.append(calfTwistControls[i])
                    y = y - 30

        # =======================================================================
        # #TOES !!!! THIS IS A SUB-PICKER !!!!
        # =======================================================================

        # if there are toes, create a toe picker
        toeControls = self.getControls(False, "toeControls")
        if len(toeControls) > 0:

            name = cmds.getAttr(networkNode + ".moduleName")
            toeBorder = interfaceUtils.pickerBorderItem(center.x() + 35, center.y() - 75, 100, 100, clearBrush,
                                                        moduleNode, name + "_toes")
            toeBorder.setParentItem(borderItem)
            interfaceUtils.addTextToButton(side[0] + "_Toes", toeBorder, False, True, False)

            # create selection set lists
            bigToes = []
            indexToes = []
            middleToes = []
            ringToes = []
            pinkyToes = []

            metaTarsals = []
            distalKnuckles = []
            middleKnuckles = []
            proximalKnuckles = []

            # BIG TOE
            for toe in toeControls:
                if toe.find("bigtoe_metatarsal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 25], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    bigToes.append(toe)
                    metaTarsals.append(toe)

                if toe.find("bigtoe_proximal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 40], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    bigToes.append(toe)
                    proximalKnuckles.append(toe)

                if toe.find("bigtoe_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 75], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    bigToes.append(toe)
                    distalKnuckles.append(toe)

                # INDEX TOE
                if toe.find("index_metatarsal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 25], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    indexToes.append(toe)
                    metaTarsals.append(toe)

                if toe.find("index_proximal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 40], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    indexToes.append(toe)
                    proximalKnuckles.append(toe)

                if toe.find("index_middle") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 55], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    indexToes.append(toe)
                    middleKnuckles.append(toe)

                if toe.find("index_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 75], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    indexToes.append(toe)
                    distalKnuckles.append(toe)

                # MIDDLE TOE
                if toe.find("middle_metatarsal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 25], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    middleToes.append(toe)
                    metaTarsals.append(toe)

                if toe.find("middle_proximal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 40], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    middleToes.append(toe)
                    proximalKnuckles.append(toe)

                if toe.find("middle_middle") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 55], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    middleToes.append(toe)
                    middleKnuckles.append(toe)

                if toe.find("middle_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 75], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    middleToes.append(toe)
                    distalKnuckles.append(toe)

                # RING TOE
                if toe.find("ring_metatarsal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 25], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    ringToes.append(toe)
                    metaTarsals.append(toe)

                if toe.find("ring_proximal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 40], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    ringToes.append(toe)
                    proximalKnuckles.append(toe)

                if toe.find("ring_middle") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 55], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    ringToes.append(toe)
                    middleKnuckles.append(toe)

                if toe.find("ring_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 75], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    ringToes.append(toe)
                    distalKnuckles.append(toe)

                # PINKY TOE
                if toe.find("pinky_metatarsal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 25], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    pinkyToes.append(toe)
                    metaTarsals.append(toe)

                if toe.find("pinky_proximal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 40], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    pinkyToes.append(toe)
                    proximalKnuckles.append(toe)

                if toe.find("pinky_middle") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 55], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    pinkyToes.append(toe)
                    middleKnuckles.append(toe)

                if toe.find("pinky_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 75], toe, blueBrush, toeBorder)
                    buttonData.append([button, toe, blueBrush])
                    controls.append(toe)
                    pinkyToes.append(toe)
                    distalKnuckles.append(toe)

            # TOE MASS SELECT BUTTONS
            interfaceUtils.pickerButtonAll(10, 10, [5, 25], metaTarsals, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [5, 40], proximalKnuckles, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [5, 55], middleKnuckles, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [5, 75], distalKnuckles, greenBrush, toeBorder)

            interfaceUtils.pickerButtonAll(10, 10, [20, 5], bigToes, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [35, 5], indexToes, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [50, 5], middleToes, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [65, 5], ringToes, greenBrush, toeBorder)
            interfaceUtils.pickerButtonAll(10, 10, [80, 5], pinkyToes, greenBrush, toeBorder)

        # settings button
        settingsBtn = interfaceUtils.pickerButton(20, 20, [65, 40], namespace + self.name + "_settings", greenBrush,
                                                  borderItem)
        buttonData.append([settingsBtn, namespace + ":" + self.name + "_settings", greenBrush])
        controls.append(namespace + ":" + self.name + "_settings")
        interfaceUtils.addTextToButton("S", settingsBtn)

        # go through button data, adding menu items
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

            button.menu.addAction(selectIcon, "Select All Leg Controls", partial(self.selectRigControls, "all"))
            button.menu.addAction(selectIcon, "Select FK Leg Controls", partial(self.selectRigControls, "fk"))
            button.menu.addAction(selectIcon, "Select IK Leg Controls", partial(self.selectRigControls, "ik"))
            button.menu.addSeparator()

            button.menu.addAction(fkIcon, "FK Mode", partial(self.switchMode, "FK", switchAction))
            button.menu.addAction(ikIcon, "IK Mode", partial(self.switchMode, "IK", switchAction))
            button.menu.addAction(switchAction)

            button.menu.addSeparator()
            button.menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
            button.menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))

        # ik foot anim spaces
        ikFootBtn.menu.addSeparator()
        ikFootBtn.addSpaces = partial(self.addSpacesToMenu, ikFootCtrl, ikFootBtn)

        # select all button
        interfaceUtils.pickerButtonAll(20, 20, [65, 10], controls, greenBrush, borderItem)

        # =======================================================================
        # #Create scriptJob for selection. Set scriptJob number to borderItem.data(5)
        # =======================================================================
        scriptJob = cmds.scriptJob(event=["SelectionChanged", partial(self.selectionScriptJob_animUI, buttonData)],
                                   kws=True)
        borderItem.setData(5, scriptJob)
        animUI.selectionScriptJobs.append(scriptJob)

        # return data and set to mirror if side is right
        if side == "Right":
            return [borderItem, True, scriptJob]
        else:
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

        # Add the module to the tree widget in the outliner tab of the rig creator UI
        self.outlinerWidgets[self.name + "_treeModule"] = QtWidgets.QTreeWidgetItem(self.rigUiInst.treeWidget)
        self.rigUiInst.treeWidget.topLevelItem(index).setText(0, self.name)
        foreground = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.outlinerWidgets[self.name + "_treeModule"].setForeground(0, foreground)

        # add the thigh
        self.outlinerWidgets[self.name + "_thigh"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_treeModule"])
        self.outlinerWidgets[self.name + "_thigh"].setText(0, self.name + "_thigh")
        self.createGlobalMoverButton(self.name + "_thigh", self.outlinerWidgets[self.name + "_thigh"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_thigh", self.outlinerWidgets[self.name + "_thigh"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_thigh", self.outlinerWidgets[self.name + "_thigh"],
                                   self.rigUiInst)

        # add the thigh twists
        self.outlinerWidgets[self.name + "_thigh_twist_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_thigh"])
        self.outlinerWidgets[self.name + "_thigh_twist_01"].setText(0, self.name + "_thigh_twist_01")
        self.createOffsetMoverButton(self.name + "_thigh_twist_01",
                                     self.outlinerWidgets[self.name + "_thigh_twist_01"],
                                     self.rigUiInst)
        self.outlinerWidgets[self.name + "_thigh_twist_01"].setHidden(True)

        self.outlinerWidgets[self.name + "_thigh_twist_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_thigh"])
        self.outlinerWidgets[self.name + "_thigh_twist_02"].setText(0, self.name + "_thigh_twist_02")
        self.createOffsetMoverButton(self.name + "_thigh_twist_02",
                                     self.outlinerWidgets[self.name + "_thigh_twist_02"],
                                     self.rigUiInst)
        self.outlinerWidgets[self.name + "_thigh_twist_02"].setHidden(True)

        self.outlinerWidgets[self.name + "_thigh_twist_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_thigh"])
        self.outlinerWidgets[self.name + "_thigh_twist_03"].setText(0, self.name + "_thigh_twist_03")

        self.createOffsetMoverButton(self.name + "_thigh_twist_03",
                                     self.outlinerWidgets[self.name + "_thigh_twist_03"],
                                     self.rigUiInst)
        self.outlinerWidgets[self.name + "_thigh_twist_03"].setHidden(True)

        # add the calf
        self.outlinerWidgets[self.name + "_calf"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_thigh"])
        self.outlinerWidgets[self.name + "_calf"].setText(0, self.name + "_calf")
        self.createGlobalMoverButton(self.name + "_calf", self.outlinerWidgets[self.name + "_calf"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_calf", self.outlinerWidgets[self.name + "_calf"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_calf", self.outlinerWidgets[self.name + "_calf"],
                                   self.rigUiInst)

        # add the calf twists
        self.outlinerWidgets[self.name + "_calf_twist_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_calf"])
        self.outlinerWidgets[self.name + "_calf_twist_01"].setText(0, self.name + "_calf_twist_01")

        self.createOffsetMoverButton(self.name + "_calf_twist_01",
                                     self.outlinerWidgets[self.name + "_calf_twist_01"],
                                     self.rigUiInst)

        self.outlinerWidgets[self.name + "_calf_twist_01"].setHidden(True)

        self.outlinerWidgets[self.name + "_calf_twist_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_calf"])
        self.outlinerWidgets[self.name + "_calf_twist_02"].setText(0, self.name + "_calf_twist_02")

        self.createOffsetMoverButton(self.name + "_calf_twist_02",
                                     self.outlinerWidgets[self.name + "_calf_twist_02"],
                                     self.rigUiInst)

        self.outlinerWidgets[self.name + "_calf_twist_02"].setHidden(True)

        self.outlinerWidgets[self.name + "_calf_twist_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_calf"])
        self.outlinerWidgets[self.name + "_calf_twist_03"].setText(0, self.name + "_calf_twist_03")

        self.createOffsetMoverButton(self.name + "_calf_twist_03",
                                     self.outlinerWidgets[self.name + "_calf_twist_03"],
                                     self.rigUiInst)

        self.outlinerWidgets[self.name + "_calf_twist_03"].setHidden(True)

        # add the foot
        self.outlinerWidgets[self.name + "_foot"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_calf"])
        self.outlinerWidgets[self.name + "_foot"].setText(0, self.name + "_foot")
        self.createGlobalMoverButton(self.name + "_foot", self.outlinerWidgets[self.name + "_foot"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_foot", self.outlinerWidgets[self.name + "_foot"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_foot", self.outlinerWidgets[self.name + "_foot"],
                                   self.rigUiInst)

        # add the ball
        self.outlinerWidgets[self.name + "_ball"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_foot"])
        self.outlinerWidgets[self.name + "_ball"].setText(0, self.name + "_ball")
        self.createGlobalMoverButton(self.name + "_ball", self.outlinerWidgets[self.name + "_ball"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ball", self.outlinerWidgets[self.name + "_ball"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ball", self.outlinerWidgets[self.name + "_ball"],
                                   self.rigUiInst)

        # add the big toes
        self.outlinerWidgets[self.name + "_bigtoe_metatarsal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_bigtoe_metatarsal"].setText(0, self.name + "_bigtoe_metatarsal")
        self.createGlobalMoverButton(self.name + "_bigtoe_metatarsal",
                                     self.outlinerWidgets[self.name + "_bigtoe_metatarsal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_bigtoe_metatarsal",
                                     self.outlinerWidgets[self.name + "_bigtoe_metatarsal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_bigtoe_metatarsal"].setHidden(True)

        self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"].setText(0,
                                                                              self.name + "_bigtoe_proximal_phalange")
        self.createGlobalMoverButton(self.name + "_bigtoe_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_bigtoe_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_bigtoe_proximal_phalange",
                                   self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"],
                                   self.rigUiInst)
        self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_bigtoe_distal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_bigtoe_proximal_phalange"])
        self.outlinerWidgets[self.name + "_bigtoe_distal_phalange"].setText(0,
                                                                            self.name + "_bigtoe_distal_phalange")
        self.createGlobalMoverButton(self.name + "_bigtoe_distal_phalange",
                                     self.outlinerWidgets[self.name + "_bigtoe_distal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_bigtoe_distal_phalange",
                                     self.outlinerWidgets[self.name + "_bigtoe_distal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_bigtoe_distal_phalange",
                                   self.outlinerWidgets[self.name + "_bigtoe_distal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_bigtoe_distal_phalange"].setHidden(True)

        # add the index toes
        self.outlinerWidgets[self.name + "_index_metatarsal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_index_metatarsal"].setText(0, self.name + "_index_metatarsal")
        self.createGlobalMoverButton(self.name + "_index_metatarsal",
                                     self.outlinerWidgets[self.name + "_index_metatarsal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_metatarsal",
                                     self.outlinerWidgets[self.name + "_index_metatarsal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_index_metatarsal"].setHidden(True)

        self.outlinerWidgets[self.name + "_index_proximal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_index_proximal_phalange"].setText(0,
                                                                             self.name + "_index_proximal_phalange")
        self.createGlobalMoverButton(self.name + "_index_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_index_proximal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_index_proximal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_index_proximal_phalange",
                                   self.outlinerWidgets[self.name + "_index_proximal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_index_proximal_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_index_middle_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_index_proximal_phalange"])
        self.outlinerWidgets[self.name + "_index_middle_phalange"].setText(0,
                                                                           self.name + "_index_middle_phalange")
        self.createGlobalMoverButton(self.name + "_index_middle_phalange",
                                     self.outlinerWidgets[self.name + "_index_middle_phalange"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_middle_phalange",
                                     self.outlinerWidgets[self.name + "_index_middle_phalange"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_index_middle_phalange",
                                   self.outlinerWidgets[self.name + "_index_middle_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_index_middle_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_index_distal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_index_middle_phalange"])
        self.outlinerWidgets[self.name + "_index_distal_phalange"].setText(0,
                                                                           self.name + "_index_distal_phalange")
        self.createGlobalMoverButton(self.name + "_index_distal_phalange",
                                     self.outlinerWidgets[self.name + "_index_distal_phalange"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_distal_phalange",
                                     self.outlinerWidgets[self.name + "_index_distal_phalange"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_index_distal_phalange",
                                   self.outlinerWidgets[self.name + "_index_distal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_index_distal_phalange"].setHidden(True)

        # add the middle toes
        self.outlinerWidgets[self.name + "_middle_metatarsal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_middle_metatarsal"].setText(0, self.name + "_middle_metatarsal")
        self.createGlobalMoverButton(self.name + "_middle_metatarsal",
                                     self.outlinerWidgets[self.name + "_middle_metatarsal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_metatarsal",
                                     self.outlinerWidgets[self.name + "_middle_metatarsal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_middle_metatarsal"].setHidden(True)

        self.outlinerWidgets[self.name + "_middle_proximal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_middle_proximal_phalange"].setText(0,
                                                                              self.name + "_middle_proximal_phalange")
        self.createGlobalMoverButton(self.name + "_middle_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_middle_proximal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_middle_proximal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_middle_proximal_phalange",
                                   self.outlinerWidgets[self.name + "_middle_proximal_phalange"],
                                   self.rigUiInst)
        self.outlinerWidgets[self.name + "_middle_proximal_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_middle_middle_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_middle_proximal_phalange"])
        self.outlinerWidgets[self.name + "_middle_middle_phalange"].setText(0,
                                                                            self.name + "_middle_middle_phalange")
        self.createGlobalMoverButton(self.name + "_middle_middle_phalange",
                                     self.outlinerWidgets[self.name + "_middle_middle_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_middle_phalange",
                                     self.outlinerWidgets[self.name + "_middle_middle_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_middle_middle_phalange",
                                   self.outlinerWidgets[self.name + "_middle_middle_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_middle_middle_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_middle_distal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_middle_middle_phalange"])
        self.outlinerWidgets[self.name + "_middle_distal_phalange"].setText(0,
                                                                            self.name + "_middle_distal_phalange")
        self.createGlobalMoverButton(self.name + "_middle_distal_phalange",
                                     self.outlinerWidgets[self.name + "_middle_distal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_distal_phalange",
                                     self.outlinerWidgets[self.name + "_middle_distal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_middle_distal_phalange",
                                   self.outlinerWidgets[self.name + "_middle_distal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_middle_distal_phalange"].setHidden(True)

        # add the ring toes
        self.outlinerWidgets[self.name + "_ring_metatarsal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_ring_metatarsal"].setText(0, self.name + "_ring_metatarsal")
        self.createGlobalMoverButton(self.name + "_ring_metatarsal",
                                     self.outlinerWidgets[self.name + "_ring_metatarsal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_metatarsal",
                                     self.outlinerWidgets[self.name + "_ring_metatarsal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_ring_metatarsal"].setHidden(True)

        self.outlinerWidgets[self.name + "_ring_proximal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_ring_proximal_phalange"].setText(0,
                                                                            self.name + "_ring_proximal_phalange")
        self.createGlobalMoverButton(self.name + "_ring_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_ring_proximal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_ring_proximal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ring_proximal_phalange",
                                   self.outlinerWidgets[self.name + "_ring_proximal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_ring_proximal_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_ring_middle_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ring_proximal_phalange"])
        self.outlinerWidgets[self.name + "_ring_middle_phalange"].setText(0,
                                                                          self.name + "_ring_middle_phalange")
        self.createGlobalMoverButton(self.name + "_ring_middle_phalange",
                                     self.outlinerWidgets[self.name + "_ring_middle_phalange"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_middle_phalange",
                                     self.outlinerWidgets[self.name + "_ring_middle_phalange"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ring_middle_phalange",
                                   self.outlinerWidgets[self.name + "_ring_middle_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_ring_middle_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_ring_distal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ring_middle_phalange"])
        self.outlinerWidgets[self.name + "_ring_distal_phalange"].setText(0,
                                                                          self.name + "_ring_distal_phalange")
        self.createGlobalMoverButton(self.name + "_ring_distal_phalange",
                                     self.outlinerWidgets[self.name + "_ring_distal_phalange"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_distal_phalange",
                                     self.outlinerWidgets[self.name + "_ring_distal_phalange"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ring_distal_phalange",
                                   self.outlinerWidgets[self.name + "_ring_distal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_ring_distal_phalange"].setHidden(True)

        # add the pinky toes
        self.outlinerWidgets[self.name + "_pinky_metatarsal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_pinky_metatarsal"].setText(0, self.name + "_pinky_metatarsal")
        self.createGlobalMoverButton(self.name + "_pinky_metatarsal",
                                     self.outlinerWidgets[self.name + "_pinky_metatarsal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_metatarsal",
                                     self.outlinerWidgets[self.name + "_pinky_metatarsal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_pinky_metatarsal"].setHidden(True)

        self.outlinerWidgets[self.name + "_pinky_proximal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ball"])
        self.outlinerWidgets[self.name + "_pinky_proximal_phalange"].setText(0,
                                                                             self.name + "_pinky_proximal_phalange")
        self.createGlobalMoverButton(self.name + "_pinky_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_pinky_proximal_phalange"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_proximal_phalange",
                                     self.outlinerWidgets[self.name + "_pinky_proximal_phalange"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pinky_proximal_phalange",
                                   self.outlinerWidgets[self.name + "_pinky_proximal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_pinky_proximal_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_pinky_middle_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_pinky_proximal_phalange"])
        self.outlinerWidgets[self.name + "_pinky_middle_phalange"].setText(0,
                                                                           self.name + "_pinky_middle_phalange")
        self.createGlobalMoverButton(self.name + "_pinky_middle_phalange",
                                     self.outlinerWidgets[self.name + "_pinky_middle_phalange"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_middle_phalange",
                                     self.outlinerWidgets[self.name + "_pinky_middle_phalange"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pinky_middle_phalange",
                                   self.outlinerWidgets[self.name + "_pinky_middle_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_pinky_middle_phalange"].setHidden(True)

        self.outlinerWidgets[self.name + "_pinky_distal_phalange"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_pinky_middle_phalange"])
        self.outlinerWidgets[self.name + "_pinky_distal_phalange"].setText(0,
                                                                           self.name + "_pinky_distal_phalange")
        self.createGlobalMoverButton(self.name + "_pinky_distal_phalange",
                                     self.outlinerWidgets[self.name + "_pinky_distal_phalange"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_distal_phalange",
                                     self.outlinerWidgets[self.name + "_pinky_distal_phalange"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pinky_distal_phalange",
                                   self.outlinerWidgets[self.name + "_pinky_distal_phalange"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_pinky_distal_phalange"].setHidden(True)

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
    def updateSettingsUI(self):
        """
        Updates the skeleton settings UI based on the network node values for this module. Happens when the UI is
        launched and there are module metadata present
        """

        networkNode = self.returnNetworkNode

        thighTwists = cmds.getAttr(networkNode + ".thighTwists")
        calfTwists = cmds.getAttr(networkNode + ".calfTwists")
        bigToes = cmds.getAttr(networkNode + ".bigToeJoints")
        indexToes = cmds.getAttr(networkNode + ".indexToeJoints")
        middleToes = cmds.getAttr(networkNode + ".middleToeJoints")
        ringToes = cmds.getAttr(networkNode + ".ringToeJoints")
        pinkyToes = cmds.getAttr(networkNode + ".pinkyToeJoints")
        includeBall = cmds.getAttr(networkNode + ".includeBall")
        bigToeMeta = cmds.getAttr(networkNode + ".bigToeMeta")
        indexToeMeta = cmds.getAttr(networkNode + ".indexToeMeta")
        middleToeMeta = cmds.getAttr(networkNode + ".middleToeMeta")
        ringToeMeta = cmds.getAttr(networkNode + ".ringToeMeta")
        pinkyToeMeta = cmds.getAttr(networkNode + ".pinkyToeMeta")

        # update UI elements
        self.thighTwistNum.setValue(thighTwists)
        self.calfTwistNum.setValue(calfTwists)
        self.ballJoint.setChecked(includeBall)

        self.bigToeNum.setValue(bigToes)
        self.indexToeNum.setValue(indexToes)
        self.middleToeNum.setValue(middleToes)
        self.ringToeNum.setValue(ringToes)
        self.pinkyToeNum.setValue(pinkyToes)

        self.bigToeMeta.setChecked(bigToeMeta)
        self.indexToeMeta.setChecked(indexToeMeta)
        self.middleToeMeta.setChecked(middleToeMeta)
        self.ringToeMeta.setChecked(ringToeMeta)
        self.pinkyToeMeta.setChecked(pinkyToeMeta)

        # apply changes
        self.applyButton.setEnabled(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleChanges(self, moduleInst):
        """
        Update the scene after the settings are changed in the skeleton settings UI.

        This means also updating the created_bones attr, updating the joint mover if needed,
        updating the outliner, and updating the bone count.

        :param moduleInst: self (usually, but there are cases like templates where an inst on disc is passed in.)
        """

        # create an array of the created bones that fit a format [thighName, thighTwistA, calfName, etc]
        createdBones = self.returnCreatedJoints
        # list all base names of spinBox/checkBox joints
        removeBones = ["ball", "thigh_twist_0", "calf_twist_0", "pinky", "index", "bigtoe", "ring", "middle"]

        removeList = []
        for bone in createdBones:
            for removeBone in removeBones:
                if bone.find(removeBone) != -1:
                    removeList.append(bone)

        keepBones = []
        for bone in createdBones:
            if bone not in removeList:
                keepBones.append(bone)

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

        networkNode = self.returnNetworkNode
        if cmds.getAttr(networkNode + ".aimMode") is True:
            self.aimMode_Setup(False)

        legJoints = [keepBones[0]]

        # get thigh twists, calf twists, and toes
        thighTwists = self.thighTwistNum.value()
        for i in range(thighTwists):
            legJoints.append(prefix + "thigh_twist_0" + str(i + 1) + suffix)
        legJoints.append(keepBones[1])

        calfTwists = self.calfTwistNum.value()
        for i in range(calfTwists):
            legJoints.append(prefix + "calf_twist_0" + str(i + 1) + suffix)
        legJoints.append(keepBones[2])

        ballJoint = self.ballJoint.isChecked()
        if ballJoint:
            legJoints.append(prefix + "ball" + suffix)

        # toes
        bigToes = self.bigToeNum.value()
        bigToeJoints = ["proximal_phalange", "distal_phalange"]
        toeJoints = ["proximal_phalange", "middle_phalange", "distal_phalange"]
        for i in range(bigToes):
            legJoints.append(prefix + "bigtoe_" + bigToeJoints[i] + suffix)

        indexToes = self.indexToeNum.value()
        for i in range(indexToes):
            legJoints.append(prefix + "index_" + toeJoints[i] + suffix)

        middleToes = self.middleToeNum.value()
        for i in range(middleToes):
            legJoints.append(prefix + "middle_" + toeJoints[i] + suffix)

        ringToes = self.ringToeNum.value()
        for i in range(ringToes):
            legJoints.append(prefix + "ring_" + toeJoints[i] + suffix)

        pinkyToes = self.pinkyToeNum.value()
        for i in range(pinkyToes):
            legJoints.append(prefix + "pinky_" + toeJoints[i] + suffix)

        # metatarsals
        if self.bigToeMeta.isChecked():
            legJoints.append(prefix + "bigtoe_metatarsal" + suffix)
        if self.indexToeMeta.isChecked():
            legJoints.append(prefix + "index_metatarsal" + suffix)
        if self.middleToeMeta.isChecked():
            legJoints.append(prefix + "middle_metatarsal" + suffix)
        if self.ringToeMeta.isChecked():
            legJoints.append(prefix + "ring_metatarsal" + suffix)
        if self.pinkyToeMeta.isChecked():
            legJoints.append(prefix + "pinky_metatarsal" + suffix)

        # build attrString
        attrString = ""
        for bone in legJoints:
            attrString += bone + "::"

        networkNode = self.returnNetworkNode
        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # reset button
        self.applyButton.setEnabled(False)

        # hide/show ball geo based on numToes
        numToes = 0
        for each in [self.bigToeNum, self.indexToeNum, self.middleToeNum, self.ringToeNum, self.pinkyToeNum]:
            value = each.value()
            if value > 0:
                numToes += 1
        ballGeo = self._getBallGeo()
        if ballGeo is not None:
            cmds.setAttr(ballGeo + ".v", lock=False)
            if numToes > 0:
                cmds.setAttr(ballGeo + ".v", 0, lock=False)
            else:
                cmds.setAttr(ballGeo + ".v", 1, lock=False)

        # update joint mover
        self._editJointMoverViaSpinBox(self.bigToeNum, "bigtoe", True)
        self._editJointMoverViaSpinBox(self.indexToeNum, "index", False)
        self._editJointMoverViaSpinBox(self.middleToeNum, "middle", False)
        self._editJointMoverViaSpinBox(self.ringToeNum, "ring", False)
        self._editJointMoverViaSpinBox(self.pinkyToeNum, "pinky", False)

        self._editJointMoverTwistBones(self.thighTwistNum, "thigh")
        self._editJointMoverTwistBones(self.calfTwistNum, "calf")

        self.includeBallJoint(False)

        self._editMetaTarsals(self.bigToeMeta, "bigtoe")
        self._editMetaTarsals(self.indexToeMeta, "index")
        self._editMetaTarsals(self.middleToeMeta, "middle")
        self._editMetaTarsals(self.ringToeMeta, "ring")
        self._editMetaTarsals(self.pinkyToeMeta, "pinky")

        # set network node attributes
        cmds.setAttr(networkNode + ".thighTwists", lock=False)
        cmds.setAttr(networkNode + ".thighTwists", thighTwists, lock=True)

        cmds.setAttr(networkNode + ".calfTwists", lock=False)
        cmds.setAttr(networkNode + ".calfTwists", calfTwists, lock=True)

        cmds.setAttr(networkNode + ".bigToeJoints", lock=False)
        cmds.setAttr(networkNode + ".bigToeJoints", bigToes, lock=True)

        cmds.setAttr(networkNode + ".indexToeJoints", lock=False)
        cmds.setAttr(networkNode + ".indexToeJoints", indexToes, lock=True)

        cmds.setAttr(networkNode + ".middleToeJoints", lock=False)
        cmds.setAttr(networkNode + ".middleToeJoints", middleToes, lock=True)

        cmds.setAttr(networkNode + ".ringToeJoints", lock=False)
        cmds.setAttr(networkNode + ".ringToeJoints", ringToes, lock=True)

        cmds.setAttr(networkNode + ".pinkyToeJoints", lock=False)
        cmds.setAttr(networkNode + ".pinkyToeJoints", pinkyToes, lock=True)

        cmds.setAttr(networkNode + ".includeBall", lock=False)
        cmds.setAttr(networkNode + ".includeBall", ballJoint, lock=True)

        cmds.setAttr(networkNode + ".bigToeMeta", lock=False)
        cmds.setAttr(networkNode + ".bigToeMeta", self.bigToeMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".indexToeMeta", lock=False)
        cmds.setAttr(networkNode + ".indexToeMeta", self.indexToeMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".ringToeMeta", lock=False)
        cmds.setAttr(networkNode + ".ringToeMeta", self.ringToeMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".middleToeMeta", lock=False)
        cmds.setAttr(networkNode + ".middleToeMeta", self.middleToeMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".pinkyToeMeta", lock=False)
        cmds.setAttr(networkNode + ".pinkyToeMeta", self.pinkyToeMeta.isChecked(), lock=True)

        # update outliner
        self.updateOutliner()
        self.updateBoneCount()

        self.aimMode_Setup(True)

        # clear selection
        cmds.select(clear=True)

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

        networkNode = self.returnNetworkNode
        attrs = cmds.listAttr(networkNode, ud=True, hd=True)

        for attr in attrs:
            attrType = str(cmds.getAttr(networkNode + "." + attr, type=True))

            if attrType == "double":
                cmds.setAttr(networkNode + "." + attr, lock=False)
                cmds.setAttr(networkNode + "." + attr, 0, lock=True)

            if attrType == "bool":
                if attr.find("Meta") != -1:
                    cmds.setAttr(networkNode + "." + attr, lock=False)
                    cmds.setAttr(networkNode + "." + attr, False, lock=True)
                if attr.find("Meta") == -1:
                    cmds.setAttr(networkNode + "." + attr, lock=False)
                    cmds.setAttr(networkNode + "." + attr, True, lock=True)

        # relaunch the UI
        self.updateSettingsUI()
        self.applyModuleChanges(self)

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

        if state:
            if cmds.getAttr(networkNode + ".pinned") is True:
                return
            topLevelMover = self.name + "_thigh_mover"
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

        # SPECIAL CASE FOR TOES/NO TOES
        numToes = 0
        for attr in ["bigToeJoints", "indexToeJoints", "middleToeJoints", "ringToeJoints", "pinkyToeJoints"]:
            value = cmds.getAttr(networkNode + "." + attr)
            if value > 0:
                numToes += 1

        if numToes != 0:
            ballGeo = self._getBallGeo()

            if cmds.objExists("skin_" + ballGeo):
                cmds.delete("skin_" + ballGeo)

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

        # ToDo: this could instead instantiate a new class that handles all the leg rig building.
        # This would give some future-proofing, as new leg rig build options could be added, which could swap out
        # which class gets instantiated.

        # get the network node and find out which rigs to build
        networkNode = self.returnNetworkNode
        buildFK = True
        buildIK_V1 = True
        side = cmds.getAttr(networkNode + ".side")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create a new network node to hold the control types
        if not cmds.objExists(networkNode + ".controls"):
            cmds.addAttr(networkNode, sn="controls", at="message")

        controlNode = cmds.createNode("network", name=networkNode + "_Controls")
        cmds.addAttr(controlNode, sn="parentModule", at="message")

        # connect new network node to original network node
        cmds.connectAttr(networkNode + ".controls", controlNode + ".parentModule")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # have it build all rigs by default, unless there is an attr stating otherwise (backwards- compatability)
        numRigs = 0
        if cmds.objExists(networkNode + ".buildFK"):
            buildFK = cmds.getAttr(networkNode + ".buildFK")
            if buildFK:
                numRigs += 1
        if cmds.objExists(networkNode + ".buildIK_V1"):
            buildIK_V1 = cmds.getAttr(networkNode + ".buildIK_V1")
            if buildIK_V1:
                numRigs += 1

        # find the joints in the leg module that need rigging
        joints = self._getMainLegJoints()

        builtRigs = []

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create groups and settings
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create the leg group
        legJoints = self._getMainLegJoints()
        self.legGroup = cmds.group(empty=True, name=self.name + "_group")
        constraint = cmds.parentConstraint(legJoints[0], self.legGroup)[0]
        cmds.delete(constraint)

        # create the leg settings group
        self.legSettings = cmds.group(empty=True, name=self.name + "_settings")
        cmds.parent(self.legSettings, self.legGroup)
        for attr in (cmds.listAttr(self.legSettings, keyable=True)):
            cmds.setAttr(self.legSettings + "." + attr, lock=True, keyable=False)

        # add mode attribute to settings
        if numRigs > 1:
            cmds.addAttr(self.legSettings, ln="mode", min=0, max=numRigs - 1, dv=0, keyable=True)

        # create the ctrl group (what will get the constraint to the parent)
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        parent_space_grp = cmds.group(empty=True, name=self.name + "_parent_space_grp")
        cmds.delete(cmds.parentConstraint(parentBone, parent_space_grp)[0])

        self.legCtrlGrp = cmds.group(empty=True, name=self.name + "_leg_ctrl_grp")
        constraint = cmds.parentConstraint(legJoints[0], self.legCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(parent_space_grp, self.legGroup)
        cmds.parent(self.legCtrlGrp, parent_space_grp)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # build the rigs
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       FK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # if build FK was true, build the FK rig now
        if buildFK:

            # update progress
            if textEdit is not None:
                textEdit.append("        Starting FK Rig Build..")

            # build the rig
            slot = len(builtRigs)
            fkRigData = riggingUtils.createFkRig(joints, networkNode, numRigs, slot)
            self.topNode = fkRigData[0]

            builtRigs.append(["FK", [self.topNode]])

            # parent top node into leg group
            if self.topNode is not None:
                cmds.parent(self.topNode, self.legCtrlGrp)

            # lock attrs
            for each in fkRigData[1]:
                for attr in [".scaleX", ".scaleY", ".scaleZ", ".visibility"]:
                    cmds.setAttr(each + attr, lock=True, keyable=False)

            # add created controls to control node
            controlNode = cmds.listConnections(networkNode + ".controls")[0]

            if not cmds.objExists(controlNode + ".fkControls"):
                cmds.addAttr(controlNode, sn="fkControls", at="message")

            # add proxy attributes for mode
            if cmds.objExists(self.legSettings + ".mode"):
                for node in fkRigData[1]:
                    cmds.addAttr(node, ln="mode", proxy=self.legSettings + ".mode", at="double", keyable=True)

            for node in fkRigData[1]:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".fkControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

                # add mirroring attrs
                for attr in ["invertX", "invertY", "invertZ"]:
                    if not cmds.objExists(node + "." + attr):
                        cmds.addAttr(node, ln=attr, at="bool")

                cmds.setAttr(node + ".invertX", 1)
                cmds.setAttr(node + ".invertY", 1)

            # update progress
            if textEdit is not None:
                textEdit.setTextColor(QtGui.QColor(0, 255, 18))
                textEdit.append("        SUCCESS: FK Build Complete!")
                textEdit.setTextColor(QtGui.QColor(255, 255, 255))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       IK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # if build IK was true, build the IK rig now
        if buildIK_V1:

            # update progress
            if textEdit is not None:
                textEdit.append("        Starting IK (version 1) Rig Build..")

            # build the rig
            slot = len(builtRigs)
            ikInfo = self.buildIkRig(numRigs, slot)
            builtRigs.append(["IK", [self.ikFootCtrl + "_grp", ikInfo[1]]])

            # lock attributes on controls
            for each in ikInfo[0]:
                for attr in [".visibility", ".scaleX", ".scaleY", ".scaleZ"]:
                    cmds.setAttr(each + attr, lock=True, keyable=False)

                if each != self.ikFootCtrl:
                    for attr in [".translateX", ".translateY", ".translateZ"]:
                        cmds.setAttr(each + attr, lock=True, keyable=False)

            # add created controls to control node
            controlNode = cmds.listConnections(networkNode + ".controls")[0]

            if not cmds.objExists(controlNode + ".ikV1Controls"):
                cmds.addAttr(controlNode, sn="ikV1Controls", at="message")

            # add proxy attributes for mode
            if cmds.objExists(self.legSettings + ".mode"):
                for node in ikInfo[0]:
                    cmds.addAttr(node, ln="mode", proxy=self.legSettings + ".mode", at="double", keyable=True)

            for node in ikInfo[0]:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".ikV1Controls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "IK", type="string")

            cmds.addAttr(self.ikFootCtrl, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
            cmds.setAttr(self.ikFootCtrl + ".hasSpaceSwitching", lock=True)
            cmds.addAttr(self.ikFootCtrl, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(self.ikFootCtrl + ".canUseRotationSpace", lock=True)
            cmds.addAttr(self.ikFootCtrl, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(self.ikFootCtrl + ".canUseTranslationSpace", lock=True)

            # update progress
            if textEdit is not None:
                textEdit.setTextColor(QtGui.QColor(0, 255, 18))
                textEdit.append("        SUCCESS: IK Build Complete!")
                textEdit.setTextColor(QtGui.QColor(255, 255, 255))

        # ===================================================================
        # #create thigh twist rig
        # ===================================================================
        twistJoints = self._getLegTwistJoints(True, False)
        twistCtrls = riggingUtils.createCounterTwistRig(twistJoints, self.name, networkNode, legJoints[0], legJoints[1],
                                                        self.name + "_group", self.legCtrlGrp)

        # add created controls to control node
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        if not cmds.objExists(controlNode + ".thighTwistControls"):
            cmds.addAttr(controlNode, sn="thighTwistControls", at="message")

        if twistCtrls is not None:
            for node in twistCtrls:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".thighTwistControls", node + ".controlClass")
                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

        # create calf twist rig
        twistJoints = self._getLegTwistJoints(False, True)
        twistCtrls = riggingUtils.createTwistRig(twistJoints, self.name, networkNode, legJoints[1], legJoints[2],
                                                 self.name + "_group", self.legCtrlGrp)

        if not cmds.objExists(controlNode + ".calfTwistControls"):
            cmds.addAttr(controlNode, sn="calfTwistControls", at="message")
        if twistCtrls is not None:
            for node in twistCtrls:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".calfTwistControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

        # =======================================================================
        # # #build toe rigs (if needed)
        # =======================================================================
        prefix = self.name.partition(baseName)[0]
        suffix = self.name.partition(baseName)[2]

        # lists of toe joints
        bigToeJoints = ["proximal_phalange", "distal_phalange"]
        toeJoints = ["proximal_phalange", "middle_phalange", "distal_phalange"]

        # loop through our toe attrs, building the toe rig as we go
        for attr in [[".bigToeJoints", "bigtoe", ".bigToeMeta"], [".indexToeJoints", "index", ".indexToeMeta"],
                     [".middleToeJoints", "middle", ".middleToeMeta"], [".ringToeJoints", "ring", ".ringToeMeta"],
                     [".pinkyToeJoints", "pinky", ".pinkyToeMeta"]]:
            metaValue = cmds.getAttr(networkNode + attr[2])

            value = cmds.getAttr(networkNode + attr[0])
            toes = []

            if metaValue:
                toes.append(prefix + attr[1] + "_metatarsal" + suffix)

            if attr[0] != ".bigToeJoints":
                for i in range(int(value)):
                    toes.append(prefix + attr[1] + "_" + toeJoints[i] + suffix)

                # build toe rigs
                self.buildToeRigs(toes)

            else:
                for i in range(int(value)):
                    toes.append(prefix + attr[1] + "_" + bigToeJoints[i] + suffix)
                # build toe rigs
                self.buildToeRigs(toes)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # hook up settings
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # mode
        if numRigs > 1:
            attrData = []
            rampData = []

            """ CONSTRAINTS """
            # get the constraint connections on the driver joints for the legs
            connections = []
            for joint in legJoints:
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
                                    cmds.listConnections(connection + ".target[" + str(each) + "].targetWeight",
                                                         p=True))

                            # add this data to our master list of constraint attribute data
                            attrData.append(driveAttrs)
                    else:
                        if cmds.nodeType(connection) == "ramp":
                            rampData.append(connection)

            rampData = list(set(rampData))

            # setup set driven keys on our mode attr and those target attributes
            for i in range(numRigs):
                cmds.setAttr(self.legSettings + ".mode", i)
                # go through attr data and zero out anything but the first element in the list
                for data in attrData:
                    for each in data:
                        cmds.setAttr(each[0], 0)
                    cmds.setAttr(data[i][0], 1)

                # set driven keys
                for data in attrData:
                    for each in data:
                        cmds.setDrivenKeyframe(each[0], cd=self.legSettings + ".mode", itt="linear", ott="linear")

            """ RAMPS """
            # direct connect mode to uCoord value (only works if there are 2 rigs...) <- not sure if that is the case
            # still
            for data in rampData:
                # create a multiply node that takes first input of 1/numRigs and 2nd of mode direct connection
                multNode = cmds.shadingNode("multiplyDivide", asUtility=True,
                                            name=self.name + "_" + data.partition(".uCoord")[0] + "_mult")
                cmds.setAttr(multNode + ".input1X", float(float(1) / float(numRigs - 1)))
                cmds.connectAttr(self.legSettings + ".mode", multNode + ".input2X")
                cmds.connectAttr(multNode + ".outputX", data)

            """
            builtRigs is a list of the rigs that have been built, but each element has the label of what rig was built,
            and nodes to hide as the second element,
            like so: ["FK", [topNode]]
                    -the second element is a list of nodes. for FK, there is only 1 item in this list.

            each element in the builtRigs list should coincide with the mode #, so if FK is element 0 in built rigs,
            mode 0 should be FK.
            """
            # hook up control visibility
            for i in range(len(builtRigs)):
                cmds.setAttr(self.legSettings + ".mode", i)
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

                    cmds.setDrivenKeyframe(visNodes, at="visibility", cd=self.legSettings + ".mode", itt="linear",
                                           ott="linear")

            # parent under offset_anim if it exists(it always should)
            if cmds.objExists("offset_anim"):
                cmds.parent(self.legGroup, "offset_anim")

        # return data
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        try:
            uiInst.rigData.append([parent_space_grp, "driver_" + parentBone, numRigs])
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
    def importFBX(self, importMethod, character):
        """
        This method defines how mocap is imported onto the rig controls.

        :param importMethod: Whether or not the FBX is getting imported as FK, IK, Both, or None
        :param character: The namespace of the rig.

        """

        returnControls = []

        networkNode = self.returnRigNetworkNode
        moduleName = cmds.getAttr(networkNode + ".moduleName")

        # find created joints
        joints = cmds.getAttr(networkNode + ".Created_Bones")

        splitJoints = joints.split("::")
        createdJoints = []
        legJoints = []

        for bone in splitJoints:
            if bone != "":
                createdJoints.append(bone)

        for joint in createdJoints:
            if joint.find("thigh") != -1:
                if joint.find("twist") == -1:
                    thighJoint = joint
                    legJoints.append(thighJoint)

            if joint.find("calf") != -1:
                if joint.find("twist") == -1:
                    calfJoint = joint
                    legJoints.append(calfJoint)

            if joint.find("foot") != -1:
                footJoint = joint
                legJoints.append(footJoint)

            if joint.find("ball") != -1:
                ballJoint = joint
                legJoints.append(ballJoint)

        # Handle Import Method/Constraints
        if importMethod is not "None":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 0)
            for joint in legJoints:
                cmds.orientConstraint(joint, character + ":fk_" + joint + "_anim")
                returnControls.append(character + ":fk_" + joint + "_anim")

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
        side = cmds.getAttr(networkNode + ".side")

        # setup aim vector details per side
        legAim = [-1, 0, 0]
        legUp = [0, 1, 0]
        ballAim = [0, -1, 0]
        toeAim = [1, 0, 0]
        toeUp = [0, 1, 0]

        if side == "Right":
            legAim = [1, 0, 0]
            legUp = [0, -1, 0]
            ballAim = [0, 1, 0]
            toeAim = [-1, 0, 0]
            toeUp = [0, -1, 0]

        # if passed in state is True:
        if state:
            # setup aim constraints

            # mesh movers on thigh/calf
            cmds.aimConstraint(name + "_calf_lra", name + "_thigh_mover_geo", aimVector=legAim,
                               upVector=legUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_calf_lra", mo=True)

            cmds.aimConstraint(name + "_foot_lra", name + "_calf_mover_geo", aimVector=legAim,
                               upVector=legUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_foot_lra", mo=True)

            cmds.aimConstraint(name + "_calf_mover_offset", name + "_thigh_mover_offset", aimVector=legAim,
                               upVector=legUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_calf_mover_offset", mo=True)

            cmds.aimConstraint(name + "_foot_mover_offset", name + "_calf_mover_offset", aimVector=legAim,
                               upVector=legUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_foot_mover_offset", mo=True)

            # ball
            # if cmds.getAttr(name + "_ball_mover_grp.v"):
            #     cmds.aimConstraint(name + "_ball_mover_offset", name + "_foot_mover_offset", aimVector=ballAim,
            #                        upVector=legUp, skip="y", wut="objectrotation", wu=[0, 1, 0],
            #                        worldUpObject=name + "_ball_mover_offset", mo=True)

            # big toe

            if cmds.getAttr(name + "_bigtoe_proximal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_bigtoe_proximal_phalange_mover_offset",
                                   name + "_bigtoe_metatarsal_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_bigtoe_proximal_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_bigtoe_distal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_bigtoe_distal_phalange_mover_offset",
                                   name + "_bigtoe_proximal_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_bigtoe_distal_phalange_mover_offset", mo=True)

            # index toe
            if cmds.getAttr(name + "_index_proximal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_index_proximal_phalange_mover_offset",
                                   name + "_index_metatarsal_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_proximal_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_index_middle_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_index_middle_phalange_mover_offset",
                                   name + "_index_proximal_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_middle_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_index_distal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_index_distal_phalange_mover_offset",
                                   name + "_index_middle_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_distal_phalange_mover_offset", mo=True)

            # middle toe
            if cmds.getAttr(name + "_middle_proximal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_middle_proximal_phalange_mover_offset",
                                   name + "_middle_metatarsal_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_proximal_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_middle_middle_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_middle_middle_phalange_mover_offset",
                                   name + "_middle_proximal_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_middle_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_middle_distal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_middle_distal_phalange_mover_offset",
                                   name + "_middle_middle_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_distal_phalange_mover_offset", mo=True)

            # ring toe
            if cmds.getAttr(name + "_ring_proximal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_ring_proximal_phalange_mover_offset",
                                   name + "_ring_metatarsal_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_proximal_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_ring_middle_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_ring_middle_phalange_mover_offset",
                                   name + "_ring_proximal_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_middle_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_ring_distal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_ring_distal_phalange_mover_offset",
                                   name + "_ring_middle_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_distal_phalange_mover_offset", mo=True)

            # pinky toe
            if cmds.getAttr(name + "_pinky_proximal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_pinky_proximal_phalange_mover_offset",
                                   name + "_pinky_metatarsal_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_proximal_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_pinky_middle_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_pinky_middle_phalange_mover_offset",
                                   name + "_pinky_proximal_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_middle_phalange_mover_offset", mo=True)

            if cmds.getAttr(name + "_pinky_distal_phalange_mover_grp.v"):
                cmds.aimConstraint(name + "_pinky_distal_phalange_mover_offset",
                                   name + "_pinky_middle_phalange_mover_offset", aimVector=toeAim,
                                   upVector=toeUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_distal_phalange_mover_offset", mo=True)

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

        .. note:: Current limitations: twist controls can not currently be pick-walked to from IK controls.
        """

        # get rig controls
        fkControls = self.getControls(False, "fkControls")
        ikControls = self.getControls(False, "ikV1Controls")
        thighTwistControls = self.getControls(False, "thighTwistControls")
        thighTwistControls = sorted(thighTwistControls)
        calfTwistControls = self.getControls(False, "calfTwistControls")
        calfTwistControls = sorted(calfTwistControls)

        fkThighCtrl = None
        fkCalfCtrl = None
        fkFootCtrl = None
        fkBallCtrl = None

        for control in fkControls:
            if "thigh" in control:
                fkThighCtrl = control
            if "calf" in control:
                fkCalfCtrl = control
            if "foot" in control:
                fkFootCtrl = control
            if "ball" in control:
                fkBallCtrl = control

        ikFootCtrl = None
        ikHeelCtrl = None
        ikToeWigCtrl = None
        ikToeTipCtrl = None

        for control in ikControls:
            if "heel" in control:
                ikHeelCtrl = control
            if "foot" in control:
                ikFootCtrl = control
            if "wiggle" in control:
                ikToeWigCtrl = control
            if "tip" in control:
                ikToeTipCtrl = control

        # setup pickwalking among FK controls
        cmds.addAttr(fkThighCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(fkCalfCtrl + ".message", fkThighCtrl + ".pickWalkDown")

        if thighTwistControls is not None:
            if len(thighTwistControls) > 0:

                if len(thighTwistControls) == 1:
                    cmds.addAttr(fkThighCtrl, ln="pickWalkRight", at="message")
                    cmds.connectAttr(thighTwistControls[0] + ".message", fkThighCtrl + ".pickWalkRight")

                    cmds.addAttr(fkThighCtrl, ln="pickWalkLeft", at="message")
                    cmds.connectAttr(thighTwistControls[0] + ".message", fkThighCtrl + ".pickWalkLeft")

                    cmds.addAttr(thighTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkThighCtrl + ".message", thighTwistControls[0] + ".pickWalkUp")

                if len(thighTwistControls) == 2:
                    cmds.addAttr(fkThighCtrl, ln="pickWalkRight", at="message")
                    cmds.connectAttr(thighTwistControls[0] + ".message", fkThighCtrl + ".pickWalkRight")

                    cmds.addAttr(fkThighCtrl, ln="pickWalkLeft", at="message")
                    cmds.connectAttr(thighTwistControls[1] + ".message", fkThighCtrl + ".pickWalkLeft")

                    cmds.addAttr(thighTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkThighCtrl + ".message", thighTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(thighTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkThighCtrl + ".message", thighTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(thighTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(thighTwistControls[1] + ".message",
                                     thighTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(thighTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(thighTwistControls[0] + ".message",
                                     thighTwistControls[1] + ".pickWalkLeft")

                if len(thighTwistControls) == 3:
                    cmds.addAttr(fkThighCtrl, ln="pickWalkRight", at="message")
                    cmds.connectAttr(thighTwistControls[0] + ".message", fkThighCtrl + ".pickWalkRight")

                    cmds.addAttr(fkThighCtrl, ln="pickWalkLeft", at="message")
                    cmds.connectAttr(thighTwistControls[2] + ".message", fkThighCtrl + ".pickWalkLeft")

                    cmds.addAttr(thighTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(thighTwistControls[1] + ".message",
                                     thighTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(thighTwistControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(thighTwistControls[2] + ".message",
                                     thighTwistControls[1] + ".pickWalkRight")

                    cmds.addAttr(thighTwistControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(thighTwistControls[1] + ".message",
                                     thighTwistControls[2] + ".pickWalkLeft")

                    cmds.addAttr(thighTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(thighTwistControls[0] + ".message",
                                     thighTwistControls[1] + ".pickWalkLeft")

                    cmds.addAttr(thighTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkThighCtrl + ".message", thighTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(thighTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkThighCtrl + ".message", thighTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(thighTwistControls[2], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkThighCtrl + ".message", thighTwistControls[2] + ".pickWalkUp")

        cmds.addAttr(fkCalfCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(fkFootCtrl + ".message", fkCalfCtrl + ".pickWalkDown")

        cmds.addAttr(fkCalfCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(fkThighCtrl + ".message", fkCalfCtrl + ".pickWalkUp")

        if calfTwistControls is not None:
            if len(calfTwistControls) > 0:

                if len(calfTwistControls) == 1:
                    cmds.addAttr(fkCalfCtrl, ln="pickWalkRight", at="message")
                    cmds.connectAttr(calfTwistControls[0] + ".message", fkCalfCtrl + ".pickWalkRight")

                    cmds.addAttr(fkCalfCtrl, ln="pickWalkLeft", at="message")
                    cmds.connectAttr(calfTwistControls[0] + ".message", fkCalfCtrl + ".pickWalkLeft")

                    cmds.addAttr(calfTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkCalfCtrl + ".message", calfTwistControls[0] + ".pickWalkUp")

                if len(calfTwistControls) == 2:
                    cmds.addAttr(fkCalfCtrl, ln="pickWalkRight", at="message")
                    cmds.connectAttr(calfTwistControls[0] + ".message", fkCalfCtrl + ".pickWalkRight")

                    cmds.addAttr(fkCalfCtrl, ln="pickWalkLeft", at="message")
                    cmds.connectAttr(calfTwistControls[1] + ".message", fkCalfCtrl + ".pickWalkLeft")

                    cmds.addAttr(calfTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkCalfCtrl + ".message", calfTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(calfTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkCalfCtrl + ".message", calfTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(calfTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(calfTwistControls[1] + ".message",
                                     calfTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(calfTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(calfTwistControls[0] + ".message",
                                     calfTwistControls[1] + ".pickWalkLeft")

                if len(calfTwistControls) == 3:
                    cmds.addAttr(fkCalfCtrl, ln="pickWalkRight", at="message")
                    cmds.connectAttr(calfTwistControls[0] + ".message", fkCalfCtrl + ".pickWalkRight")

                    cmds.addAttr(fkCalfCtrl, ln="pickWalkLeft", at="message")
                    cmds.connectAttr(calfTwistControls[2] + ".message", fkCalfCtrl + ".pickWalkLeft")

                    cmds.addAttr(calfTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(calfTwistControls[1] + ".message",
                                     calfTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(calfTwistControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(calfTwistControls[2] + ".message",
                                     calfTwistControls[1] + ".pickWalkRight")

                    cmds.addAttr(calfTwistControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(calfTwistControls[1] + ".message",
                                     calfTwistControls[2] + ".pickWalkLeft")

                    cmds.addAttr(calfTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(calfTwistControls[0] + ".message",
                                     calfTwistControls[1] + ".pickWalkLeft")

                    cmds.addAttr(calfTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkCalfCtrl + ".message", calfTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(calfTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkCalfCtrl + ".message", calfTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(calfTwistControls[2], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkCalfCtrl + ".message", calfTwistControls[2] + ".pickWalkUp")

        if fkBallCtrl is not None:
            cmds.addAttr(fkFootCtrl, ln="pickWalkDown", at="message")
            cmds.connectAttr(fkBallCtrl + ".message", fkFootCtrl + ".pickWalkDown")

            cmds.addAttr(fkBallCtrl, ln="pickWalkUp", at="message")
            cmds.connectAttr(fkFootCtrl + ".message", fkBallCtrl + ".pickWalkUp")

        cmds.addAttr(fkFootCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(fkCalfCtrl + ".message", fkFootCtrl + ".pickWalkUp")

        # IK Controls
        print ikFootCtrl
        print ikControls
        cmds.addAttr(ikFootCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(ikHeelCtrl + ".message", ikFootCtrl + ".pickWalkDown")

        cmds.addAttr(ikHeelCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(ikToeWigCtrl + ".message", ikHeelCtrl + ".pickWalkDown")

        cmds.addAttr(ikToeWigCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(ikToeTipCtrl + ".message", ikToeWigCtrl + ".pickWalkDown")

        cmds.addAttr(ikToeTipCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(ikToeWigCtrl + ".message", ikToeTipCtrl + ".pickWalkUp")

        cmds.addAttr(ikToeWigCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(ikHeelCtrl + ".message", ikToeWigCtrl + ".pickWalkUp")

        cmds.addAttr(ikHeelCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(ikFootCtrl + ".message", ikHeelCtrl + ".pickWalkUp")

        # Toes
        # create a list of all possible toes
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")
        modName = cmds.getAttr(networkNode + ".moduleName")

        splitString = modName.split(baseName)
        prefix = splitString[0]
        suffix = splitString[1]

        baseBigToes = ["bigtoe_metatarsal", "bigtoe_proximal_phalange", "bigtoe_distal_phalange",
                       "bigtoe_dummy"]
        baseIndexToes = ["index_metatarsal", "index_proximal_phalange", "index_middle_phalange",
                         "index_distal_phalange"]
        baseMiddleToes = ["middle_metatarsal", "middle_proximal_phalange", "middle_middle_phalange",
                          "middle_distal_phalange"]
        baseRingToes = ["ring_metatarsal", "ring_proximal_phalange", "ring_middle_phalange",
                        "ring_distal_phalange"]
        basePinkyToes = ["pinky_metatarsal", "pinky_proximal_phalange", "pinky_middle_phalange",
                         "pinky_distal_phalange"]

        # go through the base toes, and append our prefix and suffix to create our true toe names
        bigToes = []
        indexToes = []
        middleToes = []
        ringToes = []
        pinkyToes = []

        for toe in baseBigToes:
            string = "fk_" + prefix + toe + suffix + "_anim"
            bigToes.append(string)
        for toe in baseIndexToes:
            string = "fk_" + prefix + toe + suffix + "_anim"
            indexToes.append(string)
        for toe in baseMiddleToes:
            string = "fk_" + prefix + toe + suffix + "_anim"
            middleToes.append(string)
        for toe in baseRingToes:
            string = "fk_" + prefix + toe + suffix + "_anim"
            ringToes.append(string)
        for toe in basePinkyToes:
            string = "fk_" + prefix + toe + suffix + "_anim"
            pinkyToes.append(string)

        # setup pickwalking logic
        toe_sets = [bigToes, indexToes, middleToes, ringToes, pinkyToes]
        i = 0

        for toe_set in toe_sets:
            for index in range(len(toe_set)):

                # check if toe exists
                if cmds.objExists(toe_set[index]):
                    # setup pickwalk down to this control relationship
                    if not cmds.objExists(ikToeWigCtrl + ".pickWalkRight"):
                        cmds.addAttr(ikToeWigCtrl, ln="pickWalkRight", at="message")
                        cmds.connectAttr(toe_set[index] + ".message", ikToeWigCtrl + ".pickWalkRight")

                    if not cmds.objExists(toe_set[index] + ".pickWalkLeft"):
                        cmds.addAttr(toe_set[index], ln="pickWalkLeft", at="message")
                        cmds.connectAttr(ikToeWigCtrl + ".message", toe_set[index] + ".pickWalkLeft")

                    if fkBallCtrl is not None:
                        if not cmds.objExists(fkBallCtrl + ".pickWalkRight"):
                            cmds.addAttr(fkBallCtrl, ln="pickWalkRight", at="message")
                            cmds.connectAttr(toe_set[index] + ".message", fkBallCtrl + ".pickWalkRight")

                        if not cmds.objExists(toe_set[index] + ".pickWalkLeft"):
                            cmds.addAttr(toe_set[index], ln="pickWalkLeft", at="message")
                            cmds.connectAttr(fkBallCtrl + ".message", toe_set[index] + ".pickWalkLeft")

                    else:
                        if not cmds.objExists(fkFootCtrl + ".pickWalkRight"):
                            cmds.addAttr(fkFootCtrl, ln="pickWalkRight", at="message")
                            cmds.connectAttr(toe_set[index] + ".message", fkFootCtrl + ".pickWalkRight")

                        if not cmds.objExists(toe_set[index] + ".pickWalkLeft"):
                            cmds.addAttr(toe_set[index], ln="pickWalkLeft", at="message")
                            cmds.connectAttr(fkFootCtrl + ".message", toe_set[index] + ".pickWalkLeft")

                    # setup pickwalking down to next control
                    try:
                        if cmds.objExists(toe_set[index + 1]):
                            if not cmds.objExists(toe_set[index] + ".pickWalkDown"):
                                cmds.addAttr(toe_set[index], ln="pickWalkDown", at="message")
                                cmds.connectAttr(toe_set[index + 1] + ".message",
                                                 toe_set[index] + ".pickWalkDown")

                                cmds.addAttr(toe_set[index + 1], ln="pickWalkUp", at="message")
                                cmds.connectAttr(toe_set[index] + ".message",
                                                 toe_set[index + 1] + ".pickWalkUp")

                    except IndexError:
                        pass

                    # setup pickwalking left and right from this control
                    for x in range(i + 1, 5):
                        try:
                            if cmds.objExists(toe_sets[x][index]):
                                if not cmds.objExists(toe_set[index] + ".pickWalkRight"):
                                    cmds.addAttr(toe_set[index], ln="pickWalkRight", at="message")
                                    cmds.connectAttr(toe_sets[x][index] + ".message",
                                                     toe_set[index] + ".pickWalkRight")
                                    break
                        except IndexError:
                            pass

                    for x in reversed(range(0, i)):
                        try:
                            if cmds.objExists(toe_sets[x][index]):
                                if not cmds.objExists(toe_set[index] + ".pickWalkLeft"):
                                    cmds.addAttr(toe_set[index], ln="pickWalkLeft", at="message")
                                    cmds.connectAttr(toe_sets[x][index] + ".message",
                                                     toe_set[index] + ".pickWalkLeft")
                                    break
                        except IndexError:
                            pass
            i += 1

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
    def importFBX_post(self, importMethod, character):
        """
        Some modules may require some post operations after importing fbx motion. In the case of the leg, It will go
        through and match the knee twist to properly align up with the imported motion.

        :param importMethod: Whether the motion is being imported on FK, IK, or Both
        :param character: the character namespace
        """

        # get leg joints/controls
        legJoints = self._getMainLegJoints()
        self.ikFootCtrl = character + ":ik_" + legJoints[2] + "_anim"

        cmds.refresh(force=True)

        # get start and end frames
        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)

        networkNode = self.returnRigNetworkNode
        moduleName = cmds.getAttr(networkNode + ".moduleName")

        # run match over frame range to match the IK to the FK rig
        if importMethod == "IK" or importMethod == "Both":
            import Tools.Animation.ART_MatchOverRangeUI as match
            match.Match(character, [[networkNode, "Match IK to FK"]], start, end)

        if importMethod == "IK":
            cmds.selectKey(character + ":" + moduleName + "_settings.mode")
            cmds.cutKey()
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorTransformations_Custom(self):
        """
        Some modules may require post mirror transform operations. This is run after the base class mirror
        transformations.
        """

        networkNode = self.returnNetworkNode
        mirrorModule = cmds.getAttr(networkNode + ".mirrorModule")
        moduleName = cmds.getAttr(networkNode + ".moduleName")

        for mover in [self.name + "_toe_pivot_mover", self.name + "_heel_pivot_mover"]:
            for attr in [".rotateY", ".rotateZ"]:
                value = cmds.getAttr(mover + attr)
                mirrorMover = mover.replace(moduleName, mirrorModule)
                cmds.setAttr(mirrorMover + attr, value * -1)

            for attr in [".translateY", ".translateZ"]:
                value = cmds.getAttr(mover + attr)
                mirrorMover = mover.replace(moduleName, mirrorModule)
                cmds.setAttr(mirrorMover + attr, value)

        for mover in [self.name + "_outside_pivot_mover", self.name + "_inside_pivot_mover"]:
            for attr in [".rotateX", ".rotateZ"]:
                value = cmds.getAttr(mover + attr)
                mirrorMover = mover.replace(moduleName, mirrorModule)
                cmds.setAttr(mirrorMover + attr, value * -1)

        # outside translates
        value = cmds.getAttr(self.name + "_outside_pivot_mover.tz")
        mirrorMover = (self.name + "_outside_pivot_mover").replace(moduleName, mirrorModule)
        cmds.setAttr(mirrorMover + ".tz", value)

        value = cmds.getAttr(self.name + "_outside_pivot_mover.ty")
        mirrorMover = (self.name + "_outside_pivot_mover").replace(moduleName, mirrorModule)
        cmds.setAttr(mirrorMover + ".ty", value)

        # inside translates
        value = cmds.getAttr(self.name + "_inside_pivot_mover.tz")
        mirrorMover = (self.name + "_inside_pivot_mover").replace(moduleName, mirrorModule)
        cmds.setAttr(mirrorMover + ".tz", value)

        value = cmds.getAttr(self.name + "_inside_pivot_mover.tx")
        mirrorMover = (self.name + "_inside_pivot_mover").replace(moduleName, mirrorModule)
        cmds.setAttr(mirrorMover + ".tx", value)

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

        # select all controls
        if mode == "all":
            controls = self.getControls()
            for control in controls:
                for each in control:
                    cmds.select(each, add=True)

        # select fk controls
        if mode == "fk":
            fkControls = self.getControls(False, "fkControls")
            fkControls.extend(self.getControls(False, "thighTwistControls"))
            fkControls.extend(self.getControls(False, "calfTwistControls"))

            for control in fkControls:
                cmds.select(control, add=True)

        # select ik controls
        if mode == "ik":
            ikControls = self.getControls(False, "ikV1Controls")

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
    def buildIkRig(self, numRigs, slot):
        """
        Builds the IK rig for the leg module (similar to ARTv1 IK leg)
        """
        # setup the skeleton for the IK rig
        setup = self._ik_rig_setup(numRigs, slot)
        networkNode = setup[0]
        legJoints = setup[1]

        # build the IK foot control and create the leg IK
        legRigNodes = self._ik_rig_foot_ctrl(legJoints, networkNode)
        legIk = legRigNodes[0]
        ikFootGrp = legRigNodes[1]

        # setup the no-flip knee
        self._ik_rig_no_flip_knee(legJoints, networkNode, legIk)

        # create the IK knee vector display
        ikKneeGrp = self._ik_rig_knee_display(networkNode)

        # create the IK ball and toe joints
        ballExists = self._ik_rig_create_foot_joints(numRigs, slot, legJoints, networkNode)

        if ballExists:
            # create the necessary components for the foot roll rig
            footRollNodes = self._ik_rig_create_foot_roll_rig(legJoints, numRigs, slot)

            # setup the set driven keys to make the foot roll rig work
            toeCtrls = footRollNodes[0]
            pivots = footRollNodes[1]
            self._ik_rig_setup_foot_roll_rig(networkNode, toeCtrls, pivots)

            # complete the foot roll rig setup by setting up the hierarchy of controls
            ikNodes = [legIk[0], footRollNodes[2][0][0], footRollNodes[2][1][0]]
            self._ik_rig_complete_foot_roll_rig(networkNode, toeCtrls, pivots, ikNodes)

        # connect ik twist attr to custom attr on foot ctrl
        self._ik_rig_setup_knee_twist(legIk, networkNode)

        # add squash and stretch to the leg rig
        squashNodes = self._ik_rig_setup_squash_stretch()

        # clean up
        cmds.parent(self.ikThigh, self.legCtrlGrp)
        ikGrp = cmds.group(name=self.name + "_ik_group", empty=True)
        cmds.parent(ikKneeGrp, ikGrp)
        cmds.parent([ikFootGrp, ikGrp, squashNodes[0], squashNodes[1]], self.legGroup)

        if ballExists:
            return [[self.ikFootCtrl, toeCtrls[0], toeCtrls[2], toeCtrls[1]], ikKneeGrp]
        else:
            return [[self.ikFootCtrl], ikKneeGrp]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_setup(self, numRigs, slot):

        networkNode = self.returnNetworkNode

        # get main leg joints to duplicate for IK leg rig
        legJoints = self._getMainLegJoints()

        self.ikThigh = cmds.duplicate(legJoints[0], po=True, name="ikV1_" + legJoints[0] + "_joint")[0]
        self.ikCalf = cmds.duplicate(legJoints[1], po=True, name="ikV1_" + legJoints[1] + "_joint")[0]
        self.ikFoot = cmds.duplicate(legJoints[2], po=True, name="ikV1_" + legJoints[2] + "_joint")[0]

        for joint in [self.ikThigh, self.ikCalf, self.ikFoot]:
            parent = cmds.listRelatives(joint, parent=True)
            if parent is not None:
                cmds.parent(joint, world=True)

        # create heirarchy
        cmds.parent(self.ikFoot, self.ikCalf)
        cmds.parent(self.ikCalf, self.ikThigh)

        # freeze rotates
        cmds.makeIdentity(self.ikThigh, t=0, r=1, s=0, apply=True)

        # hook up driver joints to these ik joints
        i = 0
        for joint in [self.ikThigh, self.ikCalf, self.ikFoot]:
            cmds.pointConstraint(joint, "driver_" + legJoints[i])
            cmds.orientConstraint(joint, "driver_" + legJoints[i])

            # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
            # input 2, and plugs that into driver joint
            if cmds.objExists("master_anim"):
                globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=legJoints[i] + "_globalScale")
                cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
                cmds.connectAttr(joint + ".scale", globalScaleMult + ".input2")
                riggingUtils.createConstraint(globalScaleMult, "driver_" + legJoints[i], "scale", False, numRigs, slot,
                                              "output")
            else:
                riggingUtils.createConstraint(joint, "driver_" + legJoints[i], "scale", False, numRigs, slot)

            cmds.setAttr(joint + ".v", 0, lock=True)
            i += 1

        return [networkNode, legJoints]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_foot_ctrl(self, legJoints, networkNode):

        footControlInfo = riggingUtils.createControlFromMover(legJoints[2], networkNode, False, True,
                                                              control_type="ik_rig_control")

        cmds.parent(footControlInfo[0], world=True)
        # constraint = cmds.orientConstraint(self.name + "_ik_foot_ctrl_orient", footControlInfo[3])[0]
        # cmds.delete(constraint)
        cmds.makeIdentity(footControlInfo[2], t=1, r=1, s=1, apply=True)
        cmds.parent(footControlInfo[0], footControlInfo[1])
        cmds.makeIdentity(footControlInfo[0], t=1, r=1, s=1, apply=True)

        # rename the control info
        self.ikFootCtrl = cmds.rename(footControlInfo[0], "ik_" + legJoints[2] + "_anim")

        # add mirroring attrs
        for attr in ["invertX", "invertY", "invertZ"]:
            if not cmds.objExists(self.ikFootCtrl + "." + attr):
                cmds.addAttr(self.ikFootCtrl, ln=attr, at="bool")

        cmds.setAttr(self.ikFootCtrl + ".invertX", 1)

        cmds.rename(footControlInfo[1], self.ikFootCtrl + "_grp")
        cmds.rename(footControlInfo[2], self.ikFootCtrl + "_space_switcher")
        spaceSwitcherFollow = cmds.rename(footControlInfo[3], self.ikFootCtrl + "_space_switcher_follow")

        # Create leg RP IK
        legIkNodes = cmds.ikHandle(name=self.name + "_noFlip_ikHandle", solver="ikRPsolver", sj=self.ikThigh,
                                   ee=self.ikFoot)
        cmds.setAttr(legIkNodes[0] + ".v", 0, lock=True)

        # parent ik under the foot control
        cmds.parent(legIkNodes[0], self.ikFootCtrl)

        # create a FK matcher node
        fkMatchGrp = cmds.group(empty=True, name="ik_" + legJoints[2] + "_anim_fkMatchGrp")
        constr = cmds.parentConstraint(self.ikFoot, fkMatchGrp)[0]
        cmds.delete(constr)
        cmds.parent(fkMatchGrp, self.ikFootCtrl)

        fkMatch = cmds.group(empty=True, name="ik_" + legJoints[2] + "_anim_fkMatch")
        constr = cmds.parentConstraint(self.ikFoot, fkMatch)[0]
        cmds.delete(constr)
        cmds.parent(fkMatch, fkMatchGrp)

        # color the foot control
        riggingUtils.colorControl(self.ikFootCtrl)

        return [legIkNodes, spaceSwitcherFollow]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_knee_display(self, networkNode):

        legJoints = self._getMainLegJoints()
        networkNode = self.returnNetworkNode
        mover = utils.findAssociatedMover(legJoints[1], networkNode)

        kneeControl = self._get_rig_control_object(mover, "ik_rig_control", self.name + "_ik_knee_anim")
        cmds.delete(cmds.pointConstraint(self.ikCalf, kneeControl)[0])

        kneeGrp = cmds.group(empty=True, name=self.name + "_ik_knee_anim_grp")
        cmds.delete(cmds.parentConstraint(self.ikCalf, kneeGrp)[0])

        cmds.parent(kneeControl, kneeGrp)
        cmds.makeIdentity(kneeControl, t=1, r=1, s=1, apply=True)

        cmds.parentConstraint(self.ikCalf, kneeGrp, mo=True)
        cmds.setAttr(kneeControl + ".overrideEnabled", 1)
        cmds.setAttr(kneeControl + ".overrideDisplayType", 2)

        # color the control
        riggingUtils.colorControl(kneeControl)

        return kneeGrp

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_create_foot_joints(self, numRigs, slot, legJoints, networkNode):

        ballExists = False

        # create ball and toe joints
        if len(legJoints) == 4:
            if cmds.objExists(legJoints[3]):
                ballExists = True

        # ball joint creation
        if ballExists:
            self.ikBallJoint = cmds.createNode("joint", name="ikV1_" + legJoints[3] + "_joint")
            constraint = cmds.parentConstraint(legJoints[3], self.ikBallJoint)[0]
            cmds.delete(constraint)

            cmds.setAttr(self.ikBallJoint + ".v", 0, lock=True)

            ball_joint_driven = cmds.duplicate(self.ikBallJoint, name="ik_" + legJoints[3] + "_driven_joint")[0]

            # set the ball pivot on the ground plane
            cmds.select(self.ikBallJoint)
            if self.up == "z":
                cmds.move(0, moveZ=True, ws=True)
            else:
                cmds.move(0, moveY=True, ws=True)

            # toe joint creation
            baseName = cmds.getAttr(networkNode + ".baseName")
            nameData = self.name.split(baseName)

            self.ikToeJoint = cmds.createNode("joint", name="ikV1_" + nameData[0] + "toe" + nameData[1] + "_joint")
            constraint = cmds.pointConstraint(self.name + "_toe_pivot_mover", self.ikToeJoint)[0]
            cmds.delete(constraint)
            constraint = cmds.orientConstraint(self.name + "_ball_mover", self.ikToeJoint)[0]
            cmds.delete(constraint)

            cmds.setAttr(self.ikToeJoint + ".v", 0, lock=True)

            # parent ball and toe joints into ik joint hierarchy
            cmds.parent(self.ikToeJoint, self.ikBallJoint)
            cmds.parent(self.ikBallJoint, self.ikFoot)
            cmds.parent(ball_joint_driven, self.ikBallJoint)
            cmds.makeIdentity(self.ikBallJoint, t=0, r=1, s=0, apply=True)
            cmds.makeIdentity(ball_joint_driven, t=0, r=1, s=0, apply=True)

            # constrain driver ball joint to ik ball joint
            cmds.pointConstraint(ball_joint_driven, "driver_" + legJoints[3], mo=True)
            cmds.orientConstraint(ball_joint_driven, "driver_" + legJoints[3], mo=True)

            # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale
            # into input 2, and plugs that into driver joint
            if cmds.objExists("master_anim"):
                globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=legJoints[3] + "_globalScale")
                cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
                cmds.connectAttr(ball_joint_driven + ".scale", globalScaleMult + ".input2")
                riggingUtils.createConstraint(globalScaleMult, "driver_" + legJoints[3], "scale", False, numRigs, slot,
                                              "output")
            else:
                riggingUtils.createConstraint(ball_joint_driven, "driver_" + legJoints[3], "scale", False, numRigs, slot)

        return ballExists

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_create_foot_roll_rig(self, legJoints, numRigs, slot):

        # create the SC IK for the ball -> toe
        ballIKNodes = cmds.ikHandle(name=self.name + "_ikHandle_ball", solver="ikSCsolver", sj=self.ikFoot,
                                    ee=self.ikBallJoint)
        toeIKNodes = cmds.ikHandle(name=self.name + "_ikHandle_toe", solver="ikSCsolver", sj=self.ikBallJoint,
                                   ee=self.ikToeJoint)
        cmds.setAttr(ballIKNodes[0] + ".v", 0, lock=True)
        cmds.setAttr(toeIKNodes[0] + ".v", 0, lock=True)

        # create the locators we need for the foot rig
        toeTipPivot = cmds.spaceLocator(name=self.name + "_ik_foot_toe_tip_pivot")[0]
        insidePivot = cmds.spaceLocator(name=self.name + "_ik_foot_inside_pivot")[0]
        outsidePivot = cmds.spaceLocator(name=self.name + "_ik_foot_outside_pivot")[0]
        heelPivot = cmds.spaceLocator(name=self.name + "_ik_foot_heel_pivot")[0]
        toePivot = cmds.spaceLocator(name=self.name + "_ik_foot_toe_pivot")[0]
        ballPivot = cmds.spaceLocator(name=self.name + "_ik_foot_ball_pivot")[0]
        masterBallPivot = cmds.spaceLocator(name=self.name + "_master_foot_ball_pivot")[0]

        # create the controls
        heelControl = self._get_rig_control_object(self.name + "_heel_pivot_mover", "ik_rig_control",
                                                   self.name + "_heel_ctrl")
        toeWiggleControl = self._get_rig_control_object(self.name + "_ball_mover", "ik_rig_control",
                                                        self.name + "_toe_wiggle_ctrl")
        toeControl = self._get_rig_control_object(self.name + "_toe_pivot_mover", "ik_rig_control",
                                                  self.name + "_toe_tip_ctrl")

        for node in [toeWiggleControl, toeControl]:
            # add mirroring attrs
            for attr in ["invertX", "invertY", "invertZ"]:
                if not cmds.objExists(node + "." + attr):
                    cmds.addAttr(node, ln=attr, at="bool")

        cmds.setAttr(toeWiggleControl + ".invertX", 1)
        cmds.setAttr(toeWiggleControl + ".invertY", 1)

        cmds.setAttr(toeControl + ".invertX", 1)
        cmds.setAttr(toeControl + ".invertY", 1)
        cmds.setAttr(toeControl + ".invertZ", 1)

        # position controls
        cmds.delete(cmds.pointConstraint(self.name + "_heel_pivot_orient", heelControl)[0])
        cmds.delete(cmds.pointConstraint(self.name + "_toe_pivot_mover", toeControl)[0])
        cmds.delete(cmds.pointConstraint(legJoints[3], toeWiggleControl)[0])

        # create control groups and orient controls properly

        # heelControl
        heelCtrlGrp = cmds.group(empty=True, name=self.name + "_heel_ctrl_grp")
        cmds.delete(cmds.parentConstraint(self.name + "_heel_pivot_orient", heelCtrlGrp)[0])
        cmds.parent(heelControl, heelCtrlGrp)
        cmds.makeIdentity(heelControl, t=1, r=1, s=1, apply=True)

        # toeControl
        toeCtrlGrp = cmds.group(empty=True, name=self.name + "_toe_tip_ctrl_grp")
        cmds.delete(cmds.pointConstraint(toeControl, toeCtrlGrp)[0])
        cmds.delete(cmds.orientConstraint(self.ikToeJoint, toeCtrlGrp)[0])
        cmds.parent(toeControl, toeCtrlGrp)
        cmds.makeIdentity(toeControl, t=0, r=1, s=0, apply=True)
        cmds.makeIdentity(toeControl, t=1, r=1, s=1, apply=True)

        # toeWiggleControl
        toeWiggleCtrlGrp = cmds.group(empty=True, name=self.name + "_toe_wiggle_ctrl_grp")
        constraint = cmds.pointConstraint(legJoints[3], toeWiggleCtrlGrp)[0]
        cmds.delete(constraint)
        constraint = cmds.orientConstraint(legJoints[3], toeWiggleCtrlGrp)[0]
        cmds.delete(constraint)
        cmds.parent(toeWiggleControl, toeWiggleCtrlGrp)
        cmds.makeIdentity(toeWiggleControl, t=1, r=1, s=1, apply=True)

        # place the pivot locators
        cmds.delete(cmds.pointConstraint(heelControl, heelPivot)[0])
        cmds.delete(cmds.orientConstraint(self.name + "_ik_foot_ctrl_orient", heelPivot)[0])
        cmds.delete(cmds.pointConstraint(toeWiggleControl, ballPivot)[0])
        cmds.delete(cmds.orientConstraint(self.name + "_ik_foot_ctrl_orient", ballPivot)[0])
        cmds.delete(cmds.pointConstraint(toeWiggleControl, masterBallPivot)[0])
        cmds.delete(cmds.orientConstraint(self.name + "_ik_foot_ctrl_orient", masterBallPivot)[0])
        cmds.delete(cmds.pointConstraint(toeControl, toeTipPivot)[0])
        cmds.delete(cmds.orientConstraint(self.name + "_ik_foot_ctrl_orient", toeTipPivot)[0])
        cmds.delete(cmds.pointConstraint(toeControl, toePivot)[0])
        cmds.delete(cmds.orientConstraint(self.name + "_ik_foot_ctrl_orient", toePivot)[0])
        cmds.delete(cmds.parentConstraint(self.name + "_inside_pivot_mover_orient", insidePivot)[0])
        cmds.delete(cmds.parentConstraint(self.name + "_outside_pivot_mover_orient", outsidePivot)[0])

        # set the ball pivot on the ground plane
        cmds.select(ballPivot)
        if self.up == "z":
            cmds.move(0, moveZ=True, ws=True)
        else:
            cmds.move(0, moveY=True, ws=True)

        # create groups for each pivot and parent the pivot to the corresponding group
        for piv in [heelPivot, ballPivot, toeTipPivot, toePivot, insidePivot, outsidePivot, masterBallPivot]:
            pivGrp = cmds.group(empty=True, name=piv + "_grp")
            cmds.delete(cmds.parentConstraint(piv, pivGrp)[0])
            cmds.parent(piv, pivGrp)
            shape = cmds.listRelatives(piv, shapes=True)[0]
            cmds.setAttr(shape + ".v", 0)

        # setup pivot hierarchy
        cmds.parent(toeWiggleCtrlGrp, toePivot)
        cmds.parent(ballPivot + "_grp", toePivot)
        cmds.parent(toePivot + "_grp", heelPivot)
        cmds.parent(heelPivot + "_grp", outsidePivot)
        cmds.parent(outsidePivot + "_grp", insidePivot)
        cmds.parent(insidePivot + "_grp", toeTipPivot)

        # return data
        pivots = [toeTipPivot, insidePivot, outsidePivot, heelPivot, toePivot, ballPivot, masterBallPivot]
        return [[heelControl, toeWiggleControl, toeControl], pivots, [ballIKNodes, toeIKNodes]]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_setup_foot_roll_rig(self, networkNode, ctrls, pivots):

        # ctrls = heel, toeWiggle, toe
        # pivots = toeTip, inside, outside, heel, toe, ball, masterBall

        # get the side attribute
        side = cmds.getAttr(networkNode + ".side")

        # # # FOOT ROLL # # #
        driven = [pivots[3] + ".rx", pivots[4] + ".rx", pivots[5] + ".rx"]
        riggingUtils.set_driven_key_frames(ctrls[0] + ".rz", driven, 0, [0, 0, 0])
        riggingUtils.set_driven_key_frames(ctrls[0] + ".rz", driven, -90, [0, 0, 90])
        riggingUtils.set_driven_key_frames(ctrls[0] + ".rz", driven, 90, [-90, 0, 0])

        cmds.setAttr(ctrls[0] + ".rz", 0)
        for each in driven:
            cmds.setAttr(each, 0)

        # # # HEEL CONTROL RX & RY # # #
        cmds.connectAttr(ctrls[0] + ".rx", pivots[5] + ".rz")
        cmds.connectAttr(ctrls[0] + ".ry", pivots[5] + ".ry")

        # # # TOE CONTROL RY & RZ # # #
        if side == "Left":
            cmds.connectAttr(ctrls[2] + ".ry", pivots[0] + ".rz")

        else:
            toeRzMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_toeTipPivot_RZ_mult")
            cmds.setAttr(toeRzMult + ".input2X", -1)
            cmds.connectAttr(ctrls[2] + ".ry", toeRzMult + ".input1X")
            cmds.connectAttr(toeRzMult + ".outputX", pivots[0] + ".rz")

        toeRxMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_toeTipPivot_RX_mult")
        cmds.setAttr(toeRxMult + ".input2X", -1)
        cmds.connectAttr(ctrls[2] + ".rz", toeRxMult + ".input1X")
        cmds.connectAttr(toeRxMult + ".outputX", pivots[0] + ".rx")

        # # # # FOOT SIDE TO SIDE # # #
        driven = [pivots[1] + ".rx", pivots[2] + ".rx"]
        riggingUtils.set_driven_key_frames(ctrls[2] + ".rx", driven, 0, [0, 0])
        riggingUtils.set_driven_key_frames(ctrls[2] + ".rx", driven, -90, [0, -90])
        riggingUtils.set_driven_key_frames(ctrls[2] + ".rx", driven, 90, [90, 0])

        cmds.setAttr(ctrls[2] + ".rx", 0)
        for each in driven:
            cmds.setAttr(each, 0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_complete_foot_roll_rig(self, networkNode, ctrls, pivots, ikNodes):

        # ctrls = heel, toeWiggle, toe
        # pivots = toeTip, inside, outside, heel, toe, ball, masterBall
        # ikNodes = leg, ball, toe

        # get the side attribute
        side = cmds.getAttr(networkNode + ".side")

        # parent the IK nodes into the foot rig setup
        cmds.parent(ikNodes[0], pivots[5])
        cmds.parent(ikNodes[1], pivots[5])
        cmds.parent(ikNodes[2], ctrls[1])

        cmds.parent([pivots[0] + "_grp", ctrls[0] + "_grp", ctrls[2] + "_grp"], pivots[6])
        cmds.parent(pivots[6] + "_grp", self.ikFootCtrl)

        # add the heel pivot and ball pivot attrs to the foot control
        cmds.addAttr(ctrls[0], longName=("heelPivot"), defaultValue=0, keyable=True)
        cmds.addAttr(ctrls[0], longName=("ballPivot"), defaultValue=0, keyable=True)

        # setup heel and ball pivot
        if side == "Left":
            cmds.connectAttr(ctrls[0] + ".heelPivot", pivots[3] + ".rz")
            cmds.connectAttr(ctrls[0] + ".ballPivot", pivots[6] + ".rz")

        else:
            heelPivotMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_heelPivotMult")
            cmds.setAttr(heelPivotMult + ".input2X", -1)
            cmds.connectAttr(ctrls[0] + ".heelPivot", heelPivotMult + ".input1X")
            cmds.connectAttr(heelPivotMult + ".outputX", pivots[3] + ".rz")

            ballPivotMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_ballPivotMult")
            cmds.setAttr(ballPivotMult + ".input2X", -1)
            cmds.connectAttr(ctrls[0] + ".ballPivot", ballPivotMult + ".input1X")
            cmds.connectAttr(ballPivotMult + ".outputX", pivots[6] + ".rz")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_setup_knee_twist(self, legIk, networkNode):

        # get the side attribute
        side = cmds.getAttr(networkNode + ".side")

        # add the twist attr to the ik foot anim
        cmds.addAttr(self.ikFootCtrl, longName="knee_twist", at='double', keyable=True)

        # get the current twist value
        twist = cmds.getAttr(legIk[0] + ".twist")

        # create a plusMinusAverage node that takes in the current twist and the knee_twist attr value
        knee_twist_add_node = cmds.shadingNode("plusMinusAverage", asUtility=True, name=self.name + "_knee_twist_add")
        cmds.setAttr(knee_twist_add_node + ".input1D[0]", twist)
        if side == "Right":
            cmds.connectAttr(self.ikFootCtrl + ".knee_twist", knee_twist_add_node + ".input1D[1]")
        if side == "Left":
            # need to create a mult node to invert the result
            mult_node = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_knee_twist_mult")
            cmds.setAttr(mult_node + ".input2X", -1)
            cmds.connectAttr(self.ikFootCtrl + ".knee_twist", mult_node + ".input1X")
            cmds.connectAttr(mult_node + ".outputX", knee_twist_add_node + ".input1D[1]")

        # connect to the ik handle twist
        cmds.connectAttr(knee_twist_add_node + ".output1D", legIk[0] + ".twist")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_setup_squash_stretch(self):

        # Note about stretch bias, since this part is really confusing:
        #
        #     the math goes like this:
        #         if the current leg length > original leg length, then the leg needs to stretch (if attr is on)
        #         1.) take the stretch bias attr from the foot control and divide by 5.
        #             -Why 5? It's just an arbitrary number. The point of stretch bias is to essentially add onto the
        #             original length, so that when we divide current by original, we get a slightly smaller number than
        #             we normally would. If stretch bias is 0, this returns 0. If 1, then .2
        #         2.) Take that result and add 1.
        #             -Why? So that we aren't dividing the current length by 0 (original length * that result).
        #             At most, we would divide it by current length/(original * 1.2)
        #             -At least would be current length /(original * 1)
        #         3.) Take the add node result (1 + stretch bias output) and multiply it by original length
        #         4.) Take the current length and put that into input1 of a new mult node
        #         5.) Take the result of step 3 and put it into input 2. Set operation to divide
        #         6.) This gets us current/(original * stretch bias output)
        #         7.) Lastly, create a blendColors node passing in color 1r as 1.0, and 2r as the scale factor
        #         8.) Pass in the stretch attr into blender. if stretch is .5, given 1 and 1.3, result is 1.15.
        #         That is the scale to be applied to joints.

        # add attrs to the foot ctrl
        cmds.addAttr(self.ikFootCtrl, longName=("stretch"), at='double', min=0, max=1, dv=0, keyable=True)
        cmds.addAttr(self.ikFootCtrl, longName=("squash"), at='double', min=0, max=1, dv=0, keyable=True)
        cmds.addAttr(self.ikFootCtrl, longName=("toeCtrlVis"), at='bool', dv=0, keyable=True)

        # need to get the total length of the leg chain
        totalDist = abs(cmds.getAttr(self.ikCalf + ".tx") + cmds.getAttr(self.ikFoot + ".tx"))

        # create a distanceBetween node
        distBetween = cmds.shadingNode("distanceBetween", asUtility=True, name=self.name + "_ik_leg_distBetween")

        # get world positions of thigh and ik
        baseGrp = cmds.group(empty=True, name=self.name + "_ik_leg_base_grp")
        endGrp = cmds.group(empty=True, name=self.name + "_ik_leg_end_grp")
        cmds.pointConstraint(self.ikThigh, baseGrp)
        cmds.pointConstraint(self.ikFootCtrl, endGrp)

        # hook in group translates into distanceBetween node inputs
        cmds.connectAttr(baseGrp + ".translate", distBetween + ".point1")
        cmds.connectAttr(endGrp + ".translate", distBetween + ".point2")

        # create a condition node that will compare original length to current length
        # if second term is greater than, or equal to the first term, the chain needs to stretch
        ikLegCondition = cmds.shadingNode("condition", asUtility=True, name=self.name + "_ik_leg_stretch_condition")
        cmds.setAttr(ikLegCondition + ".operation", 3)
        cmds.connectAttr(distBetween + ".distance", ikLegCondition + ".secondTerm")
        cmds.setAttr(ikLegCondition + ".firstTerm", totalDist)

        # hook up the condition node's return colors
        cmds.setAttr(ikLegCondition + ".colorIfTrueR", totalDist)
        cmds.connectAttr(distBetween + ".distance", ikLegCondition + ".colorIfFalseR")

        # add attr to foot control for stretch bias
        cmds.addAttr(self.ikFootCtrl, ln="stretchBias", minValue=-1.0, maxValue=1.0, defaultValue=0.0, keyable=True)

        # add divide node so that instead of driving 0-1, we're actually only driving 0 - 0.2
        divNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_stretchBias_Div")
        cmds.connectAttr(self.ikFootCtrl + ".stretchBias", divNode + ".input1X")
        cmds.setAttr(divNode + ".operation", 2)
        cmds.setAttr(divNode + ".input2X", 5)

        # create the add node and connect the stretchBias into it, adding 1
        addNode = cmds.shadingNode("plusMinusAverage", asUtility=True, name=self.name + "_stretchBias_Add")
        cmds.connectAttr(divNode + ".outputX", addNode + ".input1D[0]")
        cmds.setAttr(addNode + ".input1D[1]", 1.0)

        # connect output of addNode to new mult node input1x
        stretchBiasMultNode = cmds.shadingNode("multiplyDivide", asUtility=True,
                                               name=self.name + "_stretchBias_multNode")
        cmds.connectAttr(addNode + ".output1D", stretchBiasMultNode + ".input1X")

        # create the mult/divide node(set to divide) that will take the original creation length as a static value in
        # input2x, and the connected length into 1x. This will get the scale factor
        legDistMultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_leg_dist_multNode")
        cmds.setAttr(legDistMultNode + ".operation", 2)  # divide
        cmds.connectAttr(ikLegCondition + ".outColorR", legDistMultNode + ".input1X")

        # set input2x to totalDist
        cmds.setAttr(stretchBiasMultNode + ".input2X", totalDist)
        cmds.connectAttr(stretchBiasMultNode + ".outputX", legDistMultNode + ".input2X")

        """ This differs from the original code. Instead of using a condition, I will use a blendColors node so that
        stretch % has an effect """

        # create a blendColors node for stretch
        blendResult = cmds.shadingNode("blendColors", asUtility=True, name=self.name + "_leg_stretch_scaleFactor")
        cmds.setAttr(blendResult + ".color2R", 1)
        cmds.connectAttr(legDistMultNode + ".outputX", blendResult + ".color1R")
        cmds.connectAttr(self.ikFootCtrl + ".stretch", blendResult + ".blender")

        # create a blendColors node for squash
        blendResultSquash = cmds.shadingNode("blendColors", asUtility=True, name=self.name + "_leg_squash_scaleFactor")
        cmds.setAttr(blendResultSquash + ".color2R", 1)
        cmds.connectAttr(legDistMultNode + ".outputX", blendResultSquash + ".color1R")
        cmds.connectAttr(self.ikFootCtrl + ".squash", blendResultSquash + ".blender")

        # get the sqrt of the scale factor by creating a multiply node and setting it to power operation
        powerNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_sqrt_scaleFactor")
        cmds.setAttr(powerNode + ".operation", 3)
        cmds.connectAttr(blendResultSquash + ".outputR", powerNode + ".input1X")
        cmds.setAttr(powerNode + ".input2X", .5)

        # now divide 1 by that result
        squashDivNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=self.name + "_squash_Value")
        cmds.setAttr(squashDivNode + ".operation", 2)
        cmds.setAttr(squashDivNode + ".input1X", 1)
        cmds.connectAttr(powerNode + ".outputX", squashDivNode + ".input2X")

        # connect to leg joint scale attributes
        cmds.connectAttr(blendResult + ".outputR", self.ikThigh + ".sx")
        cmds.connectAttr(blendResult + ".outputR", self.ikCalf + ".sx")

        cmds.connectAttr(squashDivNode + ".outputX", self.ikCalf + ".sy")
        cmds.connectAttr(squashDivNode + ".outputX", self.ikCalf + ".sz")

        cmds.connectAttr(squashDivNode + ".outputX", self.ikThigh + ".sy")
        cmds.connectAttr(squashDivNode + ".outputX", self.ikThigh + ".sz")

        return [baseGrp, endGrp]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _ik_rig_no_flip_knee(self, legJoints, networkNode, legIk):

        # create a locator that will serve as the pole vector
        kneeLoc = cmds.spaceLocator(name=self.name + "_knee_loc")[0]

        # snap the kneeLoc to the calf joint
        cmds.delete(cmds.pointConstraint(legJoints[1], kneeLoc)[0])

        # parent the kneeLoc to the calf and freeze rotations
        cmds.parent(kneeLoc, legJoints[1])
        cmds.makeIdentity(kneeLoc, t=0, r=1, s=0, apply=True)

        # move the locator out
        scaleFactor = riggingUtils.getModuleScaleFactor([legJoints[1], legJoints[2]], "translateX", 83.0)
        side = cmds.getAttr(networkNode + ".side")
        if side == "Left":
            cmds.setAttr(kneeLoc + ".ty", (-40 * scaleFactor))
        if side == "Right":
            cmds.setAttr(kneeLoc + ".ty", (40 * scaleFactor))

        # unparent the kneeLoc and zero the rotations
        cmds.parent(kneeLoc, world=True)
        for attr in ["rotateX", "rotateY", "rotateZ"]:
            cmds.setAttr(kneeLoc + "." + attr, 0)

        # freeze translations
        cmds.makeIdentity(kneeLoc, t=1, r=0, s=0, apply=True)

        # create some locators that we will use to counter the knee twist later
        original_pv_location = cmds.duplicate(kneeLoc)[0]
        pv_under_knee_location = cmds.duplicate(kneeLoc)[0]
        cmds.parent(pv_under_knee_location, legJoints[1])

        # snap to the ankle, then parent to the ankle, then move out to the side
        master_knee_loc = cmds.duplicate(kneeLoc, po=True, name=self.name + "_knee_loc_master")[0]

        cmds.delete(cmds.pointConstraint(legJoints[2], master_knee_loc)[0])
        cmds.parent(master_knee_loc, legJoints[2])
        cmds.makeIdentity(master_knee_loc, t=1, r=1, s=1, apply=True)

        if side == "Left":
            cmds.setAttr(master_knee_loc + ".translateZ", (-70 * scaleFactor))
        if side == "Right":
            cmds.setAttr(master_knee_loc + ".translateZ", (70 * scaleFactor))
        cmds.parent(master_knee_loc, world=True)
        cmds.parent(kneeLoc, master_knee_loc)

        # create the pole vector constraint
        cmds.poleVectorConstraint(kneeLoc, legIk[0])

        # # counter the twist attr on the ikHandle so the knee is facing forward again
        # for i in range(3600):
        #     distance = mathUtils.getDistanceBetween(original_pv_location, pv_under_knee_location)
        #     if distance > 2:
        #         cmds.setAttr(legIk[0] + ".twist", (cmds.getAttr(legIk[0] + ".twist") + 0.1))

        # delete our temp locators
        cmds.delete([original_pv_location, pv_under_knee_location])

        # create a kneeLoc group with it's rotate pivot at the ankle joint.parent under foot control
        kneeLocGrp = cmds.group(empty=True, name=self.name + "_knee_loc_grp")
        cmds.delete(cmds.parentConstraint(legJoints[2], kneeLocGrp)[0])
        cmds.parent(kneeLocGrp, self.ikFootCtrl)

        # duplicate the kneeLocGrp to have and parent under the kneeLocGrp to have zeroed values
        cmds.parent(master_knee_loc, kneeLocGrp)

        # hide the knee loc
        cmds.setAttr(kneeLoc + ".v", 0, lock=True)

        return kneeLocGrp

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildToeRigs(self, joints):
        """
        Builds FK rigs for the given toes.

        :param joints: which toe joints to build rigs for.
        """
        networkNode = self.returnNetworkNode

        # number of rigs. Might need to be pulled from a setting in the future
        buildFK = True
        buildIK = False  # later feature? Skip for now.
        numRigs = 0

        if buildFK:
            numRigs += 1
        if buildIK:
            numRigs += 1

        if numRigs > 1:
            cmds.addAttr(self.legSettings, ln="toeRigMode", min=0, max=numRigs - 1, dv=0, keyable=True)

        if numRigs >= 1:
            # setup visibility to leg settings toe mode (will need to add attribute first)
            if not cmds.objExists(self.legSettings + ".toeCtrlVis"):
                cmds.addAttr(self.legSettings, ln="toeCtrlVis", min=0, max=1, dv=0, keyable=True)

        # build the fk rig if needed
        if buildFK:

            if not cmds.objExists(self.name + "_toe_rig_grp"):
                toeRigGrp = cmds.group(empty=True, name=self.name + "_toe_rig_grp")
                cmds.parent(toeRigGrp, self.legGroup)

            # create the control from the mover
            fkToeNodes = riggingUtils.createFkRig(joints, networkNode, numRigs, 0)

            # add created controls to control node
            controlNode = cmds.listConnections(networkNode + ".controls")[0]

            if not cmds.objExists(controlNode + ".toeControls"):
                cmds.addAttr(controlNode, sn="toeControls", at="message")

            for node in fkToeNodes[1]:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".toeControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

                # add mirroring attrs
                for attr in ["invertX", "invertY", "invertZ"]:
                    if not cmds.objExists(node + "." + attr):
                        cmds.addAttr(node, ln=attr, at="bool")

                cmds.setAttr(node + ".invertX", 1)
                cmds.setAttr(node + ".invertY", 1)

            for toe in fkToeNodes[1]:
                # duplicate the toe group for each toe, parent under the toe grp, freeze transforms,
                # and parent the toe control under it
                drivenGrp = cmds.duplicate(toe + "_grp", po=True, name=toe + "_driven_grp")
                cmds.parent(drivenGrp, toe + "_grp")
                cmds.makeIdentity(drivenGrp, t=1, r=1, s=1, apply=True)
                cmds.parent(toe, drivenGrp)

                # need to find the top most group node's parent, and unparent the top most group node from it
                # parent under the toe rig grp and parentConstraint to original parent's driver joint
                parent = cmds.listRelatives(toe + "_grp", parent=True)

                if parent is None:
                    cmds.parent(toe + "_grp", self.name + "_toe_rig_grp")

                    # get the joint the parent is driving
                    joint = toe.partition("fk_")[2].partition("_anim")[0]
                    parent = cmds.listRelatives(joint, parent=True)[0]
                    driverJnt = "driver_" + parent
                    cmds.parentConstraint(driverJnt, toe + "_grp", mo=True)

                # setup set connections on toes for toe ctrl vis
                cmds.connectAttr(self.legSettings + ".toeCtrlVis", toe + "_grp.v")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getBallGeo(self):

        returnData = None
        cmds.select(self.name + "_mover_grp", hi=True)
        selection = cmds.ls(sl=True)

        for each in selection:
            if cmds.objExists(each + ".noToes"):
                returnData = each

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getLegScale(self, joint):

        default = 42.5

        # get length of thigh bone
        length = abs(cmds.getAttr(joint + ".tx"))

        factor = length/default
        return factor

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getMainLegJoints(self):

        thighJoint = None
        calfJoint = None
        footJoint = None
        ballJoint = None

        returnData = []

        # thigh
        joints = self.returnCreatedJoints
        for joint in joints:
            if joint.find("thigh") != -1:
                if joint.find("twist") == -1:
                    thighJoint = joint
                    returnData.append(thighJoint)

        # calf
        for joint in joints:
            if joint.find("calf") != -1:
                if joint.find("twist") == -1:
                    calfJoint = joint
                    returnData.append(calfJoint)

        # foot
        for joint in joints:
            if joint.find("foot") != -1:
                footJoint = joint
                returnData.append(footJoint)

        # ball
        for joint in joints:
            if joint.find("ball") != -1:
                ballJoint = joint
                returnData.append(ballJoint)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getLegTwistJoints(self, thighTwists, calfTwists):

        thighTwistBones = []
        calfTwistBones = []

        joints = self.returnCreatedJoints

        # thigh
        for joint in joints:
            if joint.find("thigh") != -1:
                if joint.find("twist") != -1:
                    thighTwistBones.append(joint)

        # calf
        for joint in joints:
            if joint.find("calf") != -1:
                if joint.find("twist") != -1:
                    calfTwistBones.append(joint)

        if thighTwists:
            return thighTwistBones
        if calfTwists:
            return calfTwistBones

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def includeBallJoint(self, apply, *args):
        """
        Set visibility and parenting on the joint movers depending on whether the include ball joint checkbox is true or
        false.
        """

        state = self.ballJoint.isChecked()

        self.bigToeNum.setEnabled(state)
        self.indexToeNum.setEnabled(state)
        self.middleToeNum.setEnabled(state)
        self.ringToeNum.setEnabled(state)
        self.pinkyToeNum.setEnabled(state)

        if state is False:
            # set values back to 0
            self.bigToeNum.setValue(0)
            self.indexToeNum.setValue(0)
            self.middleToeNum.setValue(0)
            self.ringToeNum.setValue(0)
            self.pinkyToeNum.setValue(0)

            # show ball to toe bone geo
            # ToDo: Need to update this with something new

            # hide ball mover controls
            cmds.setAttr(self.name + "_ball_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_ball_mover_grp.v", 0, lock=True)

        if state is True:
            # show ball mover controls
            cmds.setAttr(self.name + "_ball_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_ball_mover_grp.v", 1, lock=True)

        # apply changes
        if apply:
            self.applyModuleChanges(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeSide(self):
        """
        Import the given joint mover file for the side requested (from network node). For the Leg, there are 2 joint
        mover files: Left and Right. This will change the movers to the opposite side.
        """

        # gather information (current name, current parent, etc)
        networkNode = self.returnNetworkNode
        name = cmds.getAttr(networkNode + ".moduleName")
        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        currentSide = cmds.getAttr(networkNode + ".side")

        if cmds.getAttr(networkNode + ".aimMode") is True:
            self.aimMode_Setup(False)

        # call on base class delete
        cmds.select(self.name + "_mover_grp", hi=True)
        nodes = cmds.ls(sl=True)
        for node in nodes:
            cmds.lockNode(node, lock=False)
        cmds.delete(self.name + "_mover_grp")

        # figure out side
        if currentSide == "Left":
            cmds.setAttr(networkNode + ".side", lock=False)
            cmds.setAttr(networkNode + ".side", "Right", type="string", lock=True)
            side = "Right"
        if currentSide == "Right":
            cmds.setAttr(networkNode + ".side", lock=False)
            cmds.setAttr(networkNode + ".side", "Left", type="string", lock=True)
            side = "Left"

        # build new jmPath name
        jmPath = jointMover.partition(".ma")[0] + "_" + side + ".ma"
        if self.up == "y":
            jmPath = jmPath.replace("z_up", "y_up")
        self.jointMover_Build(jmPath)

        # parent the joint mover to the offset mover of the parent
        mover = ""

        if parent == "root":
            cmds.parent(name + "_mover_grp", "root_mover")
            mover = "root_mover"

        else:
            # find the parent mover name to parent to
            networkNodes = utils.returnRigModules()
            mover = utils.findMoverNodeFromJointName(networkNodes, parent)
            if mover is not None:
                cmds.parent(name + "_mover_grp", mover)

        self.applyModuleChanges(self)
        self.aimMode_Setup(True)
        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def coplanarMode(self):
        """
        Co-planar mode is a tool for the joint mover rig that snaps the movers to a rotate plane so that the chain is
        built ideally for an IK setup.
        """

        # current selection
        currentSelection = cmds.ls(sl=True)

        # get the state of the button
        state = self.coplanarBtn.isChecked()

        # write the attribute on the module
        networkNode = self.returnNetworkNode

        aimState = cmds.getAttr(networkNode + ".aimMode")

        if state:

            # lock out offset movers as they aren't to be used in coplanar mode
            offsetMovers = self.returnJointMovers[1]
            for mover in offsetMovers:
                cmds.lockNode(mover, lock=False)
                for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
                    try:
                        cmds.setAttr(mover + attr, lock=True)
                    except:
                        pass

            # fire script job that watches the coplanarIkHandle attributes, and when they change, snap to IK knee in tz
            self.coplanarScriptJob1 = cmds.scriptJob(attributeChange=[self.name + "_coplanarIkHandle.translate",
                                                                      partial(riggingUtils.coPlanarModeSnap,
                                                                              self,
                                                                              self.name + "_coplanar_knee",
                                                                              self.name + "_calf_mover_offset",
                                                                              [self.name + "_coplanar_thigh",
                                                                               self.name + "_coplanar_knee"],
                                                                              [
                                                                                  self.name + "_thigh_mover_offset",
                                                                                  self.name + "_calf_mover_offset"],
                                                                              self.name + "_foot_mover", [])],
                                                     kws=True)

            # make sure aim mode is on
            if not aimState:
                self.aimMode_Setup(True)

            # reselect current selection
            if len(currentSelection) > 0:
                cmds.select(currentSelection)

        if not state:
            # unlock all offset movers
            offsetMovers = self.returnJointMovers[1]
            for mover in offsetMovers:
                for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
                    try:
                        cmds.setAttr(mover + attr, lock=False)

                    except:
                        pass

                cmds.lockNode(mover, lock=True)

            cmds.scriptJob(kill=self.coplanarScriptJob1)
            self.aimMode_Setup(False)

            if aimState:
                self.aimMode_Setup(True)

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
        side = cmds.getAttr(networkNode + ".side")

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
                controls.reverse()

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

                # get/set translate and rotate on controls
                for control in controls:
                    joint = control.partition("fk_")[2].partition("_anim")[0]
                    joint = namespace + ":" + joint

                    dupeCtrl = control.partition(namespace + ":")[2]
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
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

        # switch to IK mode
        if mode == "IK":

            # get current mode
            currentMode = cmds.getAttr(namespace + ":" + self.name + "_settings.mode")
            if currentMode == 1.0:
                return

            if not match:
                cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

            if match:

                # get IK controls
                controls = self.getControls(False, "ikV1Controls")
                controls = sorted(controls)
                control = controls[0]

                # duplicate the control once more and parent under the fkMatch node
                matchCtrl = cmds.duplicate(control, po=True)[0]

                # match the foot anim to the foot joint
                joint = control.partition("ik_")[2].partition("_anim")[0]
                joint = namespace + ":" + joint

                pConstraint = cmds.pointConstraint(joint, matchCtrl)[0]
                oConstraint = cmds.orientConstraint(joint, matchCtrl)[0]

                if side == "Left":
                    cmds.setAttr(oConstraint + ".offsetY", 90)
                if side == "Right":
                    cmds.setAttr(oConstraint + ".offsetY", 90)
                    cmds.setAttr(oConstraint + ".offsetZ", 180)

                cmds.delete([pConstraint, oConstraint])

                # go through each control and cutkeys and zero
                currentTime = cmds.currentTime(q=True)
                for each in controls:
                    cmds.select(each)
                    cmds.cutKey(t=(currentTime, currentTime))
                    cmds.select(each)
                    self.resetRigControls(False)

                # this will now give us good values
                translate = cmds.getAttr(matchCtrl + ".translate")[0]
                rotate = cmds.getAttr(matchCtrl + ".rotate")[0]

                cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2],
                             type='double3')
                cmds.setAttr(control + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')

                cmds.setKeyframe(control)

                # delete dupes
                cmds.delete(matchCtrl)

                # match the toe wiggle control to the ball (if applicable)
                fkControls = self.getControls(False, "fkControls")
                fkControls = sorted(fkControls)
                if len(fkControls) > 3:
                    toeWiggle = controls[3]
                    ball = fkControls[0]

                    rotate = cmds.getAttr(ball + ".rotate")[0]
                    cmds.setAttr(toeWiggle + ".rotate", rotate[0], rotate[1], rotate[2],
                                 type='double3')

                # match the knee twist
                legJoints = self._getMainLegJoints()
                self.ikKneeMatch(namespace, namespace + ":" + legJoints[1], namespace + ":" + legJoints[0],
                                 namespace + ":ikV1_" + legJoints[1] + "_joint")

                # switch modes
                if not range:
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def ikKneeMatch(self, character, startJoint, middleJoint, endJoint):
        """
        Matches the knee_twist attribute of the IK leg to the angle of the reference knee.
        """

        cmds.setAttr(character + ":" + self.name + "_settings.mode", 0.0)

        # get leg joints/controls
        legJoints = self._getMainLegJoints()
        self.ikFootCtrl = character + ":ik_" + legJoints[2] + "_anim"

        # create locators
        point1 = cmds.spaceLocator()[0]
        cmds.parentConstraint(startJoint, point1)

        point2 = cmds.spaceLocator()[0]
        cmds.parentConstraint(endJoint, point2)

        # get current angle
        origAngle = mathUtils.getAngleBetween(point1, point2)
        direction = 1
        if origAngle != 0:
            cmds.setAttr(self.ikFootCtrl + ".knee_twist", 1)
            newAngle = mathUtils.getAngleBetween(point1, point2)

            if newAngle > origAngle:
                direction = -1

        # reset knee twist
        cmds.setAttr(self.ikFootCtrl + ".knee_twist", 0)
        cmds.setKeyframe(self.ikFootCtrl + ".knee_twist")

        # HIDE EVERYTHING
        panels = cmds.getPanel(type="modelPanel")
        for panel in panels:
            editor = cmds.modelPanel(panel, q=True, modelEditor=True)
            cmds.modelEditor(editor, edit=True, allObjects=0)

        # find best angle
        for x in range(3000):

            angle = mathUtils.getAngleBetween(point1, point2)
            print angle

            if angle > 1:
                currentVal = cmds.getAttr(self.ikFootCtrl + ".knee_twist")
                cmds.setAttr(self.ikFootCtrl + ".knee_twist", currentVal + direction)
                cmds.refresh()

            else:
                cmds.setKeyframe(self.ikFootCtrl + ".knee_twist")
                break

        # cmds.delete([point1, point2])

        # SHOW EVERYTHING
        panels = cmds.getPanel(type="modelPanel")
        for panel in panels:
            editor = cmds.modelPanel(panel, q=True, modelEditor=True)
            cmds.modelEditor(editor, edit=True, allObjects=1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_rig_control_object(self, node, mode, name):

        if cmds.objExists(node + "." + mode):
            connection = cmds.listConnections(node + "." + mode)[0]

            ctrl = cmds.duplicate(connection)[0]
            parent = cmds.listRelatives(ctrl, parent=True)
            if parent is not None:
                cmds.parent(ctrl, world=True)

            # turn on visiblity of the control
            cmds.setAttr(ctrl + ".v", lock=False)
            cmds.setAttr(ctrl + ".v", 1)

            for attr in [".translateX", ".translateY", ".translateZ", ".rotateX", ".rotateY", ".rotateZ", ".scaleX",
                         ".scaleY", ".scaleZ"]:
                cmds.setAttr(ctrl + attr, lock=False, keyable=True)

            ctrl = cmds.rename(ctrl, name)
            return ctrl

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
    def _editMetaTarsals(self, uiWidget, searchKey, *args):
        """
        Set teh visibility and parenting of the toe movers based on the spin box values of the meta tarsals.

        :param uiWidget: spinbox to query value
        :param searchKey: which toe to operate on (pinky, index, etc)
        """

        # uiWidget is the spinBox
        # isBigToe will be the special case, since there are only the three joints instead of the 4
        # searchKey is the basname (bigToe, middle, ring, etc)

        # toggle visibility
        if uiWidget.isChecked():
            try:
                cmds.parent(self.name + "_" + searchKey + "_proximal_phalange_mover_grp",
                            self.name + "_" + searchKey + "_metatarsal_mover")
            except Exception, e:
                print e

            cmds.setAttr(self.name + "_" + searchKey + "_metatarsal_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_" + searchKey + "_metatarsal_mover_grp.v", 1, lock=True)

        if not uiWidget.isChecked():
            try:
                cmds.parent(self.name + "_" + searchKey + "_proximal_phalange_mover_grp", self.name + "_ball_mover")
            except Exception, e:
                print e

            cmds.setAttr(self.name + "_" + searchKey + "_metatarsal_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_" + searchKey + "_metatarsal_mover_grp.v", 0, lock=True)

        # toggle mover vis
        self.rigUiInst.setMoverVisibility()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _editJointMoverViaSpinBox(self, uiWidget, searchKey, isBigToe, *args):
        """
        Sets visibility on joint movers depending on spinBox values for the toes.

        :param uiWidget: spinBox
        :param searchKey: base name of toe (big, middle, rig, index, pinky)
        :param isBigToe: special case, since there are 3 joints instead of 4
        :param args:

        """

        # uiWidget is the spinBox
        # isBigToe will be the special case, since there are only the three joints instead of the 4
        # searchKey is the basname (bigToe, middle, ring, etc)

        # check number in spinBox
        num = uiWidget.value()

        # set visibility on movers and geo depending on the value of num
        for i in range(num + 1):
            cmds.refresh(force=True)

            if isBigToe is False:

                moverList = ["_proximal_phalange", "_middle_phalange", "_distal_phalange"]
                for mover in moverList:
                    if moverList.index(mover) <= i - 1:
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover", True)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_offset", True)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_geo", True)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_lra", True)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", lock=False)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", 1, lock=True)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_proxy_geo.v", 1)

                    if i == 0:
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover", False)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_offset", False)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_geo", False)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_lra", False)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", lock=False)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", 0, lock=True)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_proxy_geo.v", 0)

            if isBigToe is True:

                moverList = ["_proximal_phalange", "_distal_phalange"]
                for mover in moverList:
                    if moverList.index(mover) <= i - 1:
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover", True)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_offset", True)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_geo", True)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_lra", True)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", lock=False)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", 1, lock=True)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_proxy_geo.v", 1)

                    if i == 0:
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover", False)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_offset", False)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_mover_geo", False)
                        self.toggleShapeVis(self.name + "_" + searchKey + mover + "_lra", False)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", lock=False)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_mover_grp.v", 0, lock=True)
                        cmds.setAttr(self.name + "_" + searchKey + mover + "_proxy_geo.v", 0)

        # toggle mover vis
        self.rigUiInst.setMoverVisibility()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _editJointMoverTwistBones(self, uiWidget, searchKey, *args):
        """
        Set visiblity on twist joint movers depending on spinBox values.

        :param uiWidget: spinbox
        :param searchKey: thigh vs calf
        :param args:

        """

        # check number in spinBox
        num = uiWidget.value()

        for i in range(num + 1):

            if i == 0:
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", 0, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", 0, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", 0, lock=True)

            if i == 1:
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", 1, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", 0, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", 0, lock=True)

            if i == 2:
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", 1, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", 1, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", 0, lock=True)

            if i == 3:
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_01_mover_grp.v", 1, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_02_mover_grp.v", 1, lock=True)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", lock=False)
                cmds.setAttr(self.name + "_" + searchKey + "_twist_03_mover_grp.v", 1, lock=True)

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

        # THIGH TWISTS
        thighTwists = self.thighTwistNum.value()
        if thighTwists == 0:
            self.outlinerWidgets[self.originalName + "_thigh_twist_01"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_thigh_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_thigh_twist_03"].setHidden(True)
        if thighTwists == 1:
            self.outlinerWidgets[self.originalName + "_thigh_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thigh_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_thigh_twist_03"].setHidden(True)
        if thighTwists == 2:
            self.outlinerWidgets[self.originalName + "_thigh_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thigh_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thigh_twist_03"].setHidden(True)
        if thighTwists == 3:
            self.outlinerWidgets[self.originalName + "_thigh_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thigh_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thigh_twist_03"].setHidden(False)

        # CALF TWISTS
        calfTwists = self.calfTwistNum.value()
        if calfTwists == 0:
            self.outlinerWidgets[self.originalName + "_calf_twist_01"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_calf_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_calf_twist_03"].setHidden(True)
        if calfTwists == 1:
            self.outlinerWidgets[self.originalName + "_calf_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_calf_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_calf_twist_03"].setHidden(True)
        if calfTwists == 2:
            self.outlinerWidgets[self.originalName + "_calf_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_calf_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_calf_twist_03"].setHidden(True)
        if calfTwists == 3:
            self.outlinerWidgets[self.originalName + "_calf_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_calf_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_calf_twist_03"].setHidden(False)

        # BALL JOINT
        ballJoint = self.ballJoint.isChecked()
        if ballJoint:
            self.outlinerWidgets[self.originalName + "_ball"].setHidden(False)
        else:
            self.outlinerWidgets[self.originalName + "_ball"].setHidden(True)

        # BIG TOES
        bigToes = self.bigToeNum.value()
        bigToeMeta = self.bigToeMeta.isChecked()

        if bigToes == 0:
            self.outlinerWidgets[self.originalName + "_bigtoe_proximal_phalange"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_bigtoe_distal_phalange"].setHidden(True)
        if bigToes == 1:
            self.outlinerWidgets[self.originalName + "_bigtoe_proximal_phalange"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_bigtoe_distal_phalange"].setHidden(True)
        if bigToes == 2:
            self.outlinerWidgets[self.originalName + "_bigtoe_proximal_phalange"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_bigtoe_distal_phalange"].setHidden(False)

        if bigToeMeta:
            self.outlinerWidgets[self.originalName + "_bigtoe_metatarsal"].setHidden(False)
        if not bigToeMeta:
            self.outlinerWidgets[self.originalName + "_bigtoe_metatarsal"].setHidden(True)

        toes = [[self.indexToeNum, "index", self.indexToeMeta], [self.middleToeNum, "middle", self.middleToeMeta],
                [self.ringToeNum, "ring", self.ringToeMeta], [self.pinkyToeNum, "pinky", self.pinkyToeMeta]]

        # OTHER TOES
        for toe in toes:
            value = toe[0].value()
            meta = toe[2].isChecked()

            if value == 0:
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_proximal_phalange"].setHidden(True)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_middle_phalange"].setHidden(True)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_distal_phalange"].setHidden(True)
            if value == 1:
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_proximal_phalange"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_middle_phalange"].setHidden(True)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_distal_phalange"].setHidden(True)
            if value == 2:
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_proximal_phalange"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_middle_phalange"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_distal_phalange"].setHidden(True)
            if value == 3:
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_proximal_phalange"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_middle_phalange"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_distal_phalange"].setHidden(False)

            if meta:
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_metatarsal"].setHidden(False)
            if not meta:
                self.outlinerWidgets[self.originalName + "_" + toe[1] + "_metatarsal"].setHidden(True)