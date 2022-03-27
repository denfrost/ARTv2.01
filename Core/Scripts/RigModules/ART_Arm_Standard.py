"""
Author: Jeremy Ernst

========
Contents
========

|   **Must Have Methods:**
|       :py:func:`addAttributes <RigModules.ART_Arm_Standard.ART_Arm_Standard.addAttributes>`
|       :py:func:`skeletonSettings_UI <RigModules.ART_Arm_Standard.ART_Arm_Standard.skeletonSettings_UI>`
|       :py:func:`pickerUI <RigModules.ART_Arm_Standard.ART_Arm_Standard.pickerUI>`
|       :py:func:`addJointMoverToOutliner <RigModules.ART_Arm_Standard.ART_Arm_Standard.addJointMoverToOutliner>`
|       :py:func:`updateSettingsUI <RigModules.ART_Arm_Standard.ART_Arm_Standard.updateSettingsUI>`
|       :py:func:`applyModuleChanges <RigModules.ART_Arm_Standard.ART_Arm_Standard.applyModuleChanges>`
|       :py:func:`resetSettings <RigModules.ART_Arm_Standard.ART_Arm_Standard.resetSettings>`
|       :py:func:`pinModule <RigModules.ART_Arm_Standard.ART_Arm_Standard.pinModule>`
|       :py:func:`skinProxyGeo <RigModules.ART_Arm_Standard.ART_Arm_Standard.skinProxyGeo>`
|       :py:func:`buildRigCustom <RigModules.ART_Arm_Standard.ART_Arm_Standard.buildRigCustom>`
|       :py:func:`importFBX <RigModules.ART_Arm_Standard.ART_Arm_Standard.importFBX>`
|       :py:func:`selectRigControls <RigModules.ART_Arm_Standard.ART_Arm_Standard.selectRigControls>`
|       :py:func:`setupPickWalking <RigModules.ART_Arm_Standard.ART_Arm_Standard.setupPickWalking>`
|       :py:func:`aimMode_Setup <RigModules.ART_Arm_Standard.ART_Arm_Standard.aimMode_Setup>`
|
|   **Module Specific Methods:**
|       :py:func:`_getMainArmJoints <RigModules.ART_Arm_Standard.ART_Arm_Standard._getMainArmJoints>`
|       :py:func:`_getTwistJoints <RigModules.ART_Arm_Standard.ART_Arm_Standard._getTwistJoints>`
|       :py:func:`_getarmScale <RigModules.ART_Arm_Standard.ART_Arm_Standard._getarmScale>`
|       :py:func:`_getFingerJoints <RigModules.ART_Arm_Standard.ART_Arm_Standard._getFingerJoints>`
|       :py:func:`_getFingerBaseName <RigModules.ART_Arm_Standard.ART_Arm_Standard._getFingerBaseName>`
|       :py:func:`coplanarMode <RigModules.ART_Arm_Standard.ART_Arm_Standard.coplanarMode>`
|       :py:func:`includeClavicle <RigModules.ART_Arm_Standard.ART_Arm_Standard.includeClavicle>`
|       :py:func:`switchFingerMode <RigModules.ART_Arm_Standard.ART_Arm_Standard.switchFingerMode>`
|       :py:func:`switchMode <RigModules.ART_Arm_Standard.ART_Arm_Standard.switchMode>`
|       :py:func:`switchClavMode <RigModules.ART_Arm_Standard.ART_Arm_Standard.switchClavMode>`
|       :py:func:`changeSide <RigModules.ART_Arm_Standard.ART_Arm_Standard.changeSide>`
|       :py:func:`_createControlNode <RigModules.ART_Arm_Standard.ART_Arm_Standard._createControlNode>`
|       :py:func:`_createRigGroups <RigModules.ART_Arm_Standard.ART_Arm_Standard._createRigGroups>`
|       :py:func:`buildFingers <RigModules.ART_Arm_Standard.ART_Arm_Standard.buildFingers>`
|       :py:func:`buildIkArm <RigModules.ART_Arm_Standard.ART_Arm_Standard.buildIkArm>`
|       :py:func:`buildFkArm <RigModules.ART_Arm_Standard.ART_Arm_Standard.buildFkArm>`
|       :py:func:`buildClavicleRig <RigModules.ART_Arm_Standard.ART_Arm_Standard.buildClavicleRig>`
|       :py:func:`_setupRigModes <RigModules.ART_Arm_Standard.ART_Arm_Standard._setupRigModes>`
|       :py:func:`_createUpperArmTwists <RigModules.ART_Arm_Standard.ART_Arm_Standard._createUpperArmTwists>`
|       :py:func:`_createLowerArmTwists <RigModules.ART_Arm_Standard.ART_Arm_Standard._createLowerArmTwists>`
|       :py:func:`_hookUpArm <RigModules.ART_Arm_Standard.ART_Arm_Standard._hookUpArm>`
|       :py:func:`_setupClavMode <RigModules.ART_Arm_Standard.ART_Arm_Standard._setupClavMode>`
|       :py:func:`_autoClavFinalize <RigModules.ART_Arm_Standard.ART_Arm_Standard._autoClavFinalize>`
|
|   **Interface Methods:**
|       :py:func:`updateOutliner <RigModules.ART_Arm_Standard.ART_Arm_Standard.updateOutliner>`
|       :py:func:`_editJointMoverViaSpinBox <RigModules.ART_Arm_Standard.ART_Arm_Standard._editJointMoverViaSpinBox>`
|       :py:func:`_editJointMoverTwistBones <RigModules.ART_Arm_Standard.ART_Arm_Standard._editJointMoverTwistBones>`
|       :py:func:`_editJointMoverMetaCarpals <RigModules.ART_Arm_Standard.ART_Arm_Standard._editJointMoverMetaCarpals>`
|       :py:func:`_toggleButtonState <RigModules.ART_Arm_Standard.ART_Arm_Standard._toggleButtonState>`

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

import Utilities.interfaceUtils as interfaceUtils
import Utilities.riggingUtils as riggingUtils
import Utilities.utils as utils
import maya.cmds as cmds
from Base.ART_RigModule import ART_RigModule
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# file attributes
search = "biped:arm"
className = "ART_Arm_Standard"
jointMover = "Core/JointMover/z_up/ART_Arm_Standard.ma"
baseName = "arm"
displayName = "Arm"
rigs = ["FK::IK"]
fbxImport = ["None", "FK", "IK", "Both"]
matchData = [True, ["Match FK to IK", "Match IK to FK"]]
sorting = 0
tooltip_image = "ART_Arm_Standard"


# begin class
class ART_Arm_Standard(ART_RigModule):
    """This class creates the arm module that builds an arm rig similar to ARTv1
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

        ART_RigModule.__init__(self, "ART_Arm_Standard_Module", "ART_Arm_Standard", moduleUserName)

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
        bones = "clavicle::upperarm::lowerarm::hand::thumb_01::thumb_02::thumb_03::index_01::"
        bones += "index_02::index_03::middle_01::middle_02::middle_03::ring_01::"
        bones += "ring_02::ring_03::pinky_01::pinky_02::pinky_03::"

        cmds.addAttr(self.networkNode, sn="Created_Bones", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".Created_Bones", bones, type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="baseName", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".baseName", baseName, type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="canAim", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".canAim", True, lock=True)

        cmds.addAttr(self.networkNode, sn="aimMode", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".aimMode", False, lock=True)

        # joint mover settings
        cmds.addAttr(self.networkNode, sn="armTwists", keyable=False)
        cmds.setAttr(self.networkNode + ".armTwists", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="forearmTwists", keyable=False)
        cmds.setAttr(self.networkNode + ".forearmTwists", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="thumbJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".thumbJoints", 2, lock=True)

        cmds.addAttr(self.networkNode, sn="thumbMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".thumbMeta", True, lock=True)

        cmds.addAttr(self.networkNode, sn="indexJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".indexJoints", 3, lock=True)

        cmds.addAttr(self.networkNode, sn="indexMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".indexMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="middleJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".middleJoints", 3, lock=True)

        cmds.addAttr(self.networkNode, sn="middleMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".middleMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="ringJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".ringJoints", 3, lock=True)

        cmds.addAttr(self.networkNode, sn="ringMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".ringMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="pinkyJoints", keyable=False)
        cmds.setAttr(self.networkNode + ".pinkyJoints", 3, lock=True)

        cmds.addAttr(self.networkNode, sn="pinkyMeta", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".pinkyMeta", False, lock=True)

        cmds.addAttr(self.networkNode, sn="side", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".side", "Left", type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="includeClavicle", keyable=False, at="bool")
        cmds.setAttr(self.networkNode + ".includeClavicle", True, lock=True)

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
        ART_RigModule.skeletonSettings_UI(self, name, 335, 500, True)

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
        self.frame.setMinimumSize(QtCore.QSize(320, 465))
        self.frame.setMaximumSize(QtCore.QSize(320, 465))

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

        # coplanar mode and bake offsets layout
        self.armToolsLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.armToolsLayout)

        # # Coplanar mode
        # self.coplanarBtn = QtWidgets.QPushButton("Coplanar Mode")
        # self.coplanarBtn.setMinimumHeight(30)
        # self.coplanarBtn.setMaximumHeight(30)
        # self.coplanarBtn.setFont(headerFont)
        # self.armToolsLayout.addWidget(self.coplanarBtn)
        # self.coplanarBtn.setCheckable(True)
        # self.coplanarBtn.clicked.connect(self.coplanarMode)
        # text = "[EXPERIMENTAL] Forces arm joints to always be planar for best IK setup."
        # self.coplanarBtn.setToolTip(text)
        # self.coplanarBtn.setObjectName("settings")

        # Bake OFfsets
        self.bakeOffsetsBtn = QtWidgets.QPushButton("Bake Offsets")
        self.bakeOffsetsBtn.setMinimumHeight(30)
        self.bakeOffsetsBtn.setMaximumHeight(30)
        self.bakeOffsetsBtn.setFont(headerFont)
        self.armToolsLayout.addWidget(self.bakeOffsetsBtn)
        self.bakeOffsetsBtn.clicked.connect(self.bakeOffsets)
        text = "Bake the offset mover values up to the global movers to get them aligned."
        self.bakeOffsetsBtn.setToolTip(text)
        self.bakeOffsetsBtn.setObjectName("settings")


        # Clavicle Settings
        spacerItem = QtWidgets.QSpacerItem(200, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.customSettingsLayout.addItem(spacerItem)

        self.clavicleCB = QtWidgets.QCheckBox("Include Clavicle?")
        self.clavicleCB.setChecked(True)
        self.customSettingsLayout.addWidget(self.clavicleCB)

        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.customSettingsLayout.addItem(spacerItem)

        # Twist Bone Settings
        self.twistSettingsLabel = QtWidgets.QLabel("Twist Bone Settings: ")
        self.twistSettingsLabel.setFont(headerFont)
        self.twistSettingsLabel.setStyleSheet("color: white;")
        self.customSettingsLayout.addWidget(self.twistSettingsLabel)

        self.separatorA = QtWidgets.QFrame()
        self.separatorA.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorA.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.customSettingsLayout.addWidget(self.separatorA)

        self.twistBonesLayout = QtWidgets.QHBoxLayout()
        self.customSettingsLayout.addLayout(self.twistBonesLayout)

        self.twistForm = QtWidgets.QFormLayout()
        self.upperarmTwistLabel = QtWidgets.QLabel("UpperArm: ")
        self.upperarmTwistLabel.setFont(font)
        self.twistForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.upperarmTwistLabel)
        self.upperarmTwistNum = QtWidgets.QSpinBox()
        self.upperarmTwistNum.setMaximum(3)
        self.twistForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.upperarmTwistNum)
        self.twistBonesLayout.addLayout(self.twistForm)

        self.lowerArmTwistForm = QtWidgets.QFormLayout()
        self.lowerarmTwistLabel = QtWidgets.QLabel("LowerArm: ")
        self.lowerarmTwistLabel.setFont(font)
        self.lowerArmTwistForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lowerarmTwistLabel)
        self.lowerarmTwistNum = QtWidgets.QSpinBox()
        self.lowerarmTwistNum.setMaximum(3)
        self.lowerArmTwistForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lowerarmTwistNum)
        self.twistBonesLayout.addLayout(self.lowerArmTwistForm)

        # Hand Settings Section
        self.handSettingsLabel = QtWidgets.QLabel("Hand Settings: ")
        self.handSettingsLabel.setFont(headerFont)
        self.handSettingsLabel.setStyleSheet("color: white;")
        self.customSettingsLayout.addWidget(self.handSettingsLabel)

        self.separatorB = QtWidgets.QFrame()
        self.separatorB.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorB.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.customSettingsLayout.addWidget(self.separatorB)

        # Thumb Settings: add VBoxLayout
        self.fingerVBoxLayout = QtWidgets.QVBoxLayout()
        self.customSettingsLayout.addLayout(self.fingerVBoxLayout)

        # THUMB
        self.thumbLayout = QtWidgets.QHBoxLayout()

        self.thumbLabel = QtWidgets.QLabel("Thumb Joints: ")
        self.thumbLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.thumbLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.thumbLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.thumbLayout.addWidget((self.thumbLabel))

        self.thumbNum = QtWidgets.QSpinBox()
        self.thumbNum.setMaximum(2)
        self.thumbNum.setMinimumSize(QtCore.QSize(50, 20))
        self.thumbNum.setMaximumSize(QtCore.QSize(50, 20))
        self.thumbNum.setValue(2)
        self.thumbNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.thumbLayout.addWidget(self.thumbNum)

        self.thumbMeta = QtWidgets.QCheckBox("Include Metacarpal")
        self.thumbMeta.setChecked(True)
        self.thumbMeta.setMinimumSize(QtCore.QSize(150, 20))
        self.thumbMeta.setMaximumSize(QtCore.QSize(150, 20))
        self.thumbLayout.addWidget(self.thumbMeta)
        self.fingerVBoxLayout.addLayout(self.thumbLayout)

        # INDEX
        self.indexLayout = QtWidgets.QHBoxLayout()

        self.indexLabel = QtWidgets.QLabel("Index Joints: ")
        self.indexLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.indexLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.indexLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.indexLayout.addWidget((self.indexLabel))

        self.indexNum = QtWidgets.QSpinBox()
        self.indexNum.setMaximum(3)
        self.indexNum.setValue(3)
        self.indexNum.setMinimumSize(QtCore.QSize(50, 20))
        self.indexNum.setMaximumSize(QtCore.QSize(50, 20))
        self.indexNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.indexLayout.addWidget(self.indexNum)

        self.indexMeta = QtWidgets.QCheckBox("Include Metacarpal")
        self.indexMeta.setMinimumSize(QtCore.QSize(150, 20))
        self.indexMeta.setMaximumSize(QtCore.QSize(150, 20))
        self.indexLayout.addWidget(self.indexMeta)
        self.fingerVBoxLayout.addLayout(self.indexLayout)

        # MIDDLE
        self.middleLayout = QtWidgets.QHBoxLayout()

        self.middleLabel = QtWidgets.QLabel("Middle Joints: ")
        self.middleLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.middleLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.middleLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.middleLayout.addWidget((self.middleLabel))

        self.middleNum = QtWidgets.QSpinBox()
        self.middleNum.setMaximum(3)
        self.middleNum.setValue(3)
        self.middleNum.setMinimumSize(QtCore.QSize(50, 20))
        self.middleNum.setMaximumSize(QtCore.QSize(50, 20))
        self.middleNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.middleLayout.addWidget(self.middleNum)

        self.middleMeta = QtWidgets.QCheckBox("Include Metacarpal")
        self.middleMeta.setMinimumSize(QtCore.QSize(150, 20))
        self.middleMeta.setMaximumSize(QtCore.QSize(150, 20))
        self.middleLayout.addWidget(self.middleMeta)
        self.fingerVBoxLayout.addLayout(self.middleLayout)

        # RING
        self.ringLayout = QtWidgets.QHBoxLayout()

        self.ringLabel = QtWidgets.QLabel("Ring Joints: ")
        self.ringLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.ringLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.ringLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.ringLayout.addWidget(self.ringLabel)

        self.ringNum = QtWidgets.QSpinBox()
        self.ringNum.setMaximum(3)
        self.ringNum.setValue(3)
        self.ringNum.setMinimumSize(QtCore.QSize(50, 20))
        self.ringNum.setMaximumSize(QtCore.QSize(50, 20))
        self.ringNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.ringLayout.addWidget(self.ringNum)

        self.ringMeta = QtWidgets.QCheckBox("Include Metacarpal")
        self.ringMeta.setMinimumSize(QtCore.QSize(150, 20))
        self.ringMeta.setMaximumSize(QtCore.QSize(150, 20))
        self.ringLayout.addWidget(self.ringMeta)
        self.fingerVBoxLayout.addLayout(self.ringLayout)

        # PINKY
        self.pinkyLayout = QtWidgets.QHBoxLayout()

        self.pinkyLabel = QtWidgets.QLabel("Pinky Joints: ")
        self.pinkyLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.pinkyLabel.setMinimumSize(QtCore.QSize(100, 20))
        self.pinkyLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.pinkyLayout.addWidget((self.pinkyLabel))

        self.pinkyNum = QtWidgets.QSpinBox()
        self.pinkyNum.setMaximum(3)
        self.pinkyNum.setValue(3)
        self.pinkyNum.setMinimumSize(QtCore.QSize(50, 20))
        self.pinkyNum.setMaximumSize(QtCore.QSize(50, 20))
        self.pinkyNum.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pinkyLayout.addWidget(self.pinkyNum)

        self.pinkyMeta = QtWidgets.QCheckBox("Include Metacarpal")
        self.pinkyMeta.setMinimumSize(QtCore.QSize(150, 20))
        self.pinkyMeta.setMaximumSize(QtCore.QSize(150, 20))
        self.pinkyLayout.addWidget(self.pinkyMeta)
        self.fingerVBoxLayout.addLayout(self.pinkyLayout)

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

        # button signal/slots
        self.changeNameBtn.clicked.connect(partial(self.changeModuleName, baseName, self, self.rigUiInst))
        self.changeParentBtn.clicked.connect(partial(self.changeModuleParent, self, self.rigUiInst))
        self.mirrorModuleBtn.clicked.connect(partial(self.setMirrorModule, self, self.rigUiInst))
        self.applyButton.clicked.connect(partial(self.applyModuleChanges, self))

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(self.groupBox, QtCore.SIGNAL("toggled(bool)"), self.frame.setVisible)
        self.groupBox.setChecked(False)

        # spinBox & checkbox signal/slots
        self.upperarmTwistNum.valueChanged.connect(self._toggleButtonState)
        self.lowerarmTwistNum.valueChanged.connect(self._toggleButtonState)
        self.thumbNum.valueChanged.connect(self._toggleButtonState)
        self.indexNum.valueChanged.connect(self._toggleButtonState)
        self.middleNum.valueChanged.connect(self._toggleButtonState)
        self.ringNum.valueChanged.connect(self._toggleButtonState)
        self.pinkyNum.valueChanged.connect(self._toggleButtonState)

        self.pinkyMeta.stateChanged.connect(self._toggleButtonState)
        self.ringMeta.stateChanged.connect(self._toggleButtonState)
        self.middleMeta.stateChanged.connect(self._toggleButtonState)
        self.indexMeta.stateChanged.connect(self._toggleButtonState)
        self.thumbMeta.stateChanged.connect(self._toggleButtonState)

        self.clavicleCB.stateChanged.connect(self._toggleButtonState)

        # add custom skeletonUI settings  name, parent, rig types to install, mirror module, thigh twist, calf twists,
        # ball joint, toes,
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

        borderItem = interfaceUtils.pickerBorderItem(center.x() - 80, center.y() - 130, 110, 260, clearBrush,
                                                     moduleNode)

        # get controls
        fkControls = self.getControls(False, "fkControls")
        fkControls = sorted(fkControls)
        ik_controls = self.getControls(False, "ikControls")
        ikControls = []

        for each in ik_controls:
            if each.find("hand") != -1:
                ikControls.append(each)
            if each.find("elbow") != -1:
                ikControls.append(each)

        upArmTwistControls = self.getControls(False, "upArmTwistControls")
        upArmTwistControls = sorted(upArmTwistControls)
        loArmTwistControls = self.getControls(False, "loArmTwistControls")
        loArmTwistControls = sorted(loArmTwistControls)
        clavControls = []
        if cmds.getAttr(networkNode + ".includeClavicle") is True:
            clavControls = self.getControls(False, "clavControls")
            clavControls = sorted(clavControls)

        buttonData = []
        controls = []

        # =======================================================================
        # ik buttons
        # =======================================================================
        ikHandButton = interfaceUtils.pickerButton(20, 20, [50, 190], ikControls[0], yellowBrush,
                                                   borderItem)
        buttonData.append([ikHandButton, ikControls[0], yellowBrush])
        controls.append(ikControls[0])

        ikElbowButton = interfaceUtils.pickerButton(20, 20, [50, 100], ikControls[1], yellowBrush,
                                                    borderItem)
        buttonData.append([ikElbowButton, ikControls[1], yellowBrush])
        controls.append(ikControls[0])

        if len(clavControls) > 0:
            ikClavButton = interfaceUtils.pickerButton(20, 20, [50, 10], clavControls[1], yellowBrush,
                                                       borderItem)
            buttonData.append([ikClavButton, clavControls[1], yellowBrush])
            controls.append(clavControls[1])

        # =======================================================================
        # fk buttons
        # =======================================================================
        fkArmBtn = interfaceUtils.pickerButton(20, 60, [50, 35], fkControls[2], blueBrush, borderItem)
        buttonData.append([fkArmBtn, fkControls[2], blueBrush])
        controls.append(fkControls[2])

        fkElbowBtn = interfaceUtils.pickerButton(20, 60, [50, 125], fkControls[1], blueBrush, borderItem)
        buttonData.append([fkElbowBtn, fkControls[1], blueBrush])
        controls.append(fkControls[1])

        fkHandBtn = interfaceUtils.pickerButton(40, 40, [40, 215], fkControls[0], blueBrush, borderItem)
        buttonData.append([fkHandBtn, fkControls[0], blueBrush])
        controls.append(fkControls[0])

        if len(clavControls) > 0:
            fkClavButton = interfaceUtils.pickerButton(20, 20, [25, 10], clavControls[0], blueBrush,
                                                       borderItem)
            buttonData.append([fkClavButton, clavControls[0], blueBrush])
            controls.append(clavControls[0])

        # =======================================================================
        # twist bones
        # =======================================================================
        if upArmTwistControls is not None:
            if len(upArmTwistControls) > 0:
                y = 35
                for i in range(len(upArmTwistControls)):
                    button = interfaceUtils.pickerButton(15, 15, [75, y], upArmTwistControls[i],
                                                         purpleBrush, borderItem)
                    buttonData.append([button, upArmTwistControls[i], purpleBrush])
                    controls.append(upArmTwistControls[i])
                    y = y + 22

        if loArmTwistControls is not None:
            if len(loArmTwistControls) > 0:
                y = 170
                for i in range(len(loArmTwistControls)):
                    button = interfaceUtils.pickerButton(15, 15, [75, y], loArmTwistControls[i],
                                                         purpleBrush, borderItem)
                    buttonData.append([button, loArmTwistControls[i], purpleBrush])
                    controls.append(loArmTwistControls[i])
                    y = y - 22

        # =======================================================================
        # settings button
        # =======================================================================
        settingsBtn = interfaceUtils.pickerButton(20, 20, [85, 235], namespace + self.name + "_settings", greenBrush,
                                                  borderItem)
        buttonData.append([settingsBtn, namespace + ":" + self.name + "_settings", greenBrush])
        controls.append(namespace + ":" + self.name + "_settings")
        interfaceUtils.addTextToButton("S", settingsBtn)

        # =======================================================================
        # #FINGERS !!!! THIS IS A SUB-PICKER !!!!
        # =======================================================================

        # if there are fingers, create a finger picker
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        fingerControls = self.getControls(False, "fkFingerControls")
        ikFingerControls = []
        if cmds.objExists(controlNode + ".ikFingerControls"):
            ikFingerControls = self.getControls(False, "ikFingerControls")

        # create selection set lists
        thumbFingers = []
        indexFingers = []
        middleFingers = []
        ringFingers = []
        pinkyFingers = []

        metaCarpals = []
        distalKnuckles = []
        middleKnuckles = []
        proximalKnuckles = []
        fkFingerControls = []
        fingerButtonData = []

        if len(fingerControls) > 0:

            name = cmds.getAttr(networkNode + ".moduleName")
            fingerBorder = interfaceUtils.pickerBorderItem(center.x() + 35, center.y() - 75, 100, 100, clearBrush,
                                                           moduleNode, name + "_fingers")
            fingerBorder.setParentItem(borderItem)
            interfaceUtils.addTextToButton(side[0] + "_Fingers", fingerBorder, False, False, True)

            # =======================================================================
            # THUMB
            # =======================================================================
            for finger in fingerControls:
                if finger.find("thumb_01") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 40], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    thumbFingers.append(finger)

                if finger.find("thumb_02") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 55], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    thumbFingers.append(finger)

                if finger.find("thumb_03") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 75], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    thumbFingers.append(finger)

                # =======================================================================
                # INDEX
                # =======================================================================
                if finger.find("index_metacarpal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 25], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    indexFingers.append(finger)
                    metaCarpals.append(finger)

                if finger.find("index_01") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 40], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    indexFingers.append(finger)
                    proximalKnuckles.append(finger)

                if finger.find("index_02") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 55], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    indexFingers.append(finger)
                    middleKnuckles.append(finger)

                if finger.find("index_03") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 75], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    indexFingers.append(finger)
                    distalKnuckles.append(finger)

                # =======================================================================
                # MIDDLE
                # =======================================================================
                if finger.find("middle_metacarpal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 25], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    middleFingers.append(finger)
                    metaCarpals.append(finger)

                if finger.find("middle_01") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 40], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    middleFingers.append(finger)
                    proximalKnuckles.append(finger)

                if finger.find("middle_02") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 55], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    middleFingers.append(finger)
                    middleKnuckles.append(finger)

                if finger.find("middle_03") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 75], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    middleFingers.append(finger)
                    distalKnuckles.append(finger)

                # =======================================================================
                # RING
                # =======================================================================
                if finger.find("ring_metacarpal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 25], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    ringFingers.append(finger)
                    metaCarpals.append(finger)

                if finger.find("ring_01") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 40], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    ringFingers.append(finger)
                    proximalKnuckles.append(finger)

                if finger.find("ring_02") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 55], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    ringFingers.append(finger)
                    middleKnuckles.append(finger)

                if finger.find("ring_03") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 75], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    ringFingers.append(finger)
                    distalKnuckles.append(finger)

                # =======================================================================
                # PINKY
                # =======================================================================
                if finger.find("pinky_metacarpal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 25], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    pinkyFingers.append(finger)
                    metaCarpals.append(finger)

                if finger.find("pinky_01") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 40], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    pinkyFingers.append(finger)
                    proximalKnuckles.append(finger)

                if finger.find("pinky_02") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 55], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    pinkyFingers.append(finger)
                    middleKnuckles.append(finger)

                if finger.find("pinky_03") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 75], finger, blueBrush, fingerBorder)
                    buttonData.append([button, finger, blueBrush])
                    fingerButtonData.append([button, finger, blueBrush])
                    controls.append(finger)
                    fkFingerControls.append(finger)
                    pinkyFingers.append(finger)
                    distalKnuckles.append(finger)

            # =======================================================================
            # IK FINGERS
            # =======================================================================
            for finger in ikFingerControls:

                if finger.find("index_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [35, 88], finger, yellowBrush,
                                                         fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("index_pv") != -1:
                    button = interfaceUtils.pickerButton(10, 6, [35, 67], finger, yellowBrush, fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("middle_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [50, 88], finger, yellowBrush,
                                                         fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("middle_pv") != -1:
                    button = interfaceUtils.pickerButton(10, 6, [50, 67], finger, yellowBrush, fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("ring_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [65, 88], finger, yellowBrush,
                                                         fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("ring_pv") != -1:
                    button = interfaceUtils.pickerButton(10, 6, [65, 67], finger, yellowBrush, fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("pinky_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [80, 88], finger, yellowBrush,
                                                         fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("pinky_pv") != -1:
                    button = interfaceUtils.pickerButton(10, 6, [80, 67], finger, yellowBrush, fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("thumb_distal") != -1:
                    button = interfaceUtils.pickerButton(10, 10, [20, 88], finger, yellowBrush,
                                                         fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("thumb_pv") != -1:
                    button = interfaceUtils.pickerButton(10, 6, [20, 67], finger, yellowBrush, fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

                if finger.find("hand_global") != -1:
                    button = interfaceUtils.pickerButton(5, 98, [94, 2], finger, yellowBrush, fingerBorder)
                    buttonData.append([button, finger, yellowBrush])
                    fingerButtonData.append([button, finger, yellowBrush])
                    controls.append(finger)
                    button.setToolTip(finger)

            # =======================================================================
            # FINGER MASS SELECT BUTTONS
            # =======================================================================
            metaCarpalAll_btn = interfaceUtils.pickerButtonAll(10, 10, [5, 25], metaCarpals, greenBrush, fingerBorder)
            metaCarpalAll_btn.setToolTip("select all metacarpal controls")

            proxiKnuckle_btn = interfaceUtils.pickerButtonAll(10, 10, [5, 40], proximalKnuckles, greenBrush,
                                                              fingerBorder)
            proxiKnuckle_btn.setToolTip("select all proximal knuckles")
            midKnuckle_btn = interfaceUtils.pickerButtonAll(10, 10, [5, 55], middleKnuckles, greenBrush, fingerBorder)
            midKnuckle_btn.setToolTip("select all middle knuckles")
            distKnuckle_btn = interfaceUtils.pickerButtonAll(10, 10, [5, 75], distalKnuckles, greenBrush, fingerBorder)
            distKnuckle_btn.setToolTip("select all distal knuckles")

            thumbs_btn = interfaceUtils.pickerButtonAll(10, 10, [20, 5], thumbFingers, greenBrush, fingerBorder)
            thumbs_btn.setToolTip("select all thumb controls")
            indexes_btn = interfaceUtils.pickerButtonAll(10, 10, [35, 5], indexFingers, greenBrush, fingerBorder)
            indexes_btn.setToolTip("select all index finger controls")
            middles_btn = interfaceUtils.pickerButtonAll(10, 10, [50, 5], middleFingers, greenBrush, fingerBorder)
            middles_btn.setToolTip("select all middle finger controls")
            rings_btn = interfaceUtils.pickerButtonAll(10, 10, [65, 5], ringFingers, greenBrush, fingerBorder)
            rings_btn.setToolTip("select all ring finger controls")
            pinkys_btn = interfaceUtils.pickerButtonAll(10, 10, [80, 5], pinkyFingers, greenBrush, fingerBorder)
            pinkys_btn.setToolTip("select all pinky finger controls")

            allFinger_btn = interfaceUtils.pickerButtonAll(12, 12, [5, 8], fkFingerControls, greenBrush, fingerBorder)
            allFinger_btn.setToolTip("select all fk finger controls")

        # =======================================================================
        # go through button data, adding menu items
        # =======================================================================
        for each in buttonData:
            if each not in fingerButtonData:
                button = each[0]

                fkIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/jointFilter.png"))))
                ikIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/ikMode.png"))))
                zeroIcon1 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroAll.png"))))
                zeroIcon2 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroSel.png"))))
                selectIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select.png"))))

                switchAction = QtWidgets.QAction('Match when Switching', button.menu)
                switchAction.setCheckable(True)
                switchAction.setChecked(True)

                button.menu.addAction(selectIcon, "Select All Arm Controls", partial(self.selectRigControls, "all"))
                button.menu.addAction(selectIcon, "Select FK Arm Controls", partial(self.selectRigControls, "fk"))
                button.menu.addAction(selectIcon, "Select IK Arm Controls", partial(self.selectRigControls, "ik"))
                button.menu.addSeparator()

                if len(clavControls) > 0:
                    if each[1] == clavControls[0] or each[1] == clavControls[1]:
                        button.menu.addAction(fkIcon, "(Clav) FK Mode",
                                              partial(self.switchClavMode, "FK", switchAction))
                        button.menu.addAction(ikIcon, "(Clav) IK Mode",
                                              partial(self.switchClavMode, "IK", switchAction))

                    else:
                        button.menu.addAction(fkIcon, "(Arm) FK Mode", partial(self.switchMode, "FK", switchAction))
                        button.menu.addAction(ikIcon, "(Arm) IK Mode", partial(self.switchMode, "IK", switchAction))

                else:
                    button.menu.addAction(fkIcon, "(Arm) FK Mode", partial(self.switchMode, "FK", switchAction))
                    button.menu.addAction(ikIcon, "(Arm) IK Mode", partial(self.switchMode, "IK", switchAction))

                button.menu.addAction(switchAction)

                button.menu.addSeparator()

                button.menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
                button.menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))

        for each in fingerButtonData:
            button = each[0]

            fkIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/jointFilter.png"))))
            ikIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/ikMode.png"))))
            zeroIcon1 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroAll.png"))))
            zeroIcon2 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroSel.png"))))

            button.menu.addAction(fkIcon, "FK Mode (Finger)", partial(self.switchFingerMode, "FK", each[1]))
            button.menu.addAction(ikIcon, "IK Mode (Finger)", partial(self.switchFingerMode, "IK", each[1]))

            button.menu.addSeparator()
            button.menu.addAction(fkIcon, "FK Mode (All Fingers)", partial(self.switchFingerMode, "FK", "All"))
            button.menu.addAction(ikIcon, "IK Mode (All Fingers)", partial(self.switchFingerMode, "IK", "All"))

            button.menu.addSeparator()
            button.menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
            button.menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))

        # add spaces to menus for space-switching controls
        for each in [[fkArmBtn, fkControls[2]], [ikHandButton, ikControls[0]], [ikElbowButton, ikControls[1]]]:
            button = each[0]
            control = each[1]

            button.menu.addSeparator()
            button.addSpaces = partial(self.addSpacesToMenu, control, button)

        for each in fingerButtonData:
            button = each[0]
            control = each[1]

            if control.find("index_distal") != -1:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, control, button)

            if control.find("middle_distal") != -1:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, control, button)

            if control.find("ring_distal") != -1:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, control, button)

            if control.find("pinky_distal") != -1:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, control, button)

            if control.find("thumb_distal") != -1:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, control, button)

            if control.find("hand_global") != -1:
                button.menu.addSeparator()
                button.addSpaces = partial(self.addSpacesToMenu, control, button)

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
        self.outlinerWidgets = {}

        # Add the module to the tree widget in the outliner tab of the rig creator UI
        self.outlinerWidgets[self.name + "_treeModule"] = QtWidgets.QTreeWidgetItem(self.rigUiInst.treeWidget)
        self.rigUiInst.treeWidget.topLevelItem(index).setText(0, self.name)
        foreground = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.outlinerWidgets[self.name + "_treeModule"].setForeground(0, foreground)

        # add the clavicle
        self.outlinerWidgets[self.name + "_clavicle"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_treeModule"])
        self.outlinerWidgets[self.name + "_clavicle"].setText(0, self.name + "_clavicle")
        self.createGlobalMoverButton(self.name + "_clavicle", self.outlinerWidgets[self.name + "_clavicle"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_clavicle", self.outlinerWidgets[self.name + "_clavicle"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_clavicle", self.outlinerWidgets[self.name + "_clavicle"],
                                   self.rigUiInst)

        # add the upperarm
        self.outlinerWidgets[self.name + "_upperarm"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_treeModule"])
        self.outlinerWidgets[self.name + "_upperarm"].setText(0, self.name + "_upperarm")
        self.createGlobalMoverButton(self.name + "_upperarm", self.outlinerWidgets[self.name + "_upperarm"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_upperarm", self.outlinerWidgets[self.name + "_upperarm"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_upperarm", self.outlinerWidgets[self.name + "_upperarm"],
                                   self.rigUiInst)

        # add the upperarm twists
        self.outlinerWidgets[self.name + "_upperarm_twist_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_upperarm"])
        self.outlinerWidgets[self.name + "_upperarm_twist_01"].setText(0, self.name + "_upperarm_twist_01")
        self.createOffsetMoverButton(self.name + "_upperarm_twist_01",
                                     self.outlinerWidgets[self.name + "_upperarm_twist_01"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_upperarm_twist_01"].setHidden(True)

        self.outlinerWidgets[self.name + "_upperarm_twist_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_upperarm"])
        self.outlinerWidgets[self.name + "_upperarm_twist_02"].setText(0, self.name + "_upperarm_twist_02")
        self.createOffsetMoverButton(self.name + "_upperarm_twist_02",
                                     self.outlinerWidgets[self.name + "_upperarm_twist_02"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_upperarm_twist_02"].setHidden(True)

        self.outlinerWidgets[self.name + "_upperarm_twist_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_upperarm"])
        self.outlinerWidgets[self.name + "_upperarm_twist_03"].setText(0, self.name + "_upperarm_twist_03")
        self.createOffsetMoverButton(self.name + "_upperarm_twist_03",
                                     self.outlinerWidgets[self.name + "_upperarm_twist_03"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_upperarm_twist_03"].setHidden(True)

        # add the lowerarm
        self.outlinerWidgets[self.name + "_lowerarm"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_upperarm"])
        self.outlinerWidgets[self.name + "_lowerarm"].setText(0, self.name + "_lowerarm")
        self.createGlobalMoverButton(self.name + "_lowerarm", self.outlinerWidgets[self.name + "_lowerarm"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_lowerarm", self.outlinerWidgets[self.name + "_lowerarm"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_lowerarm", self.outlinerWidgets[self.name + "_lowerarm"],
                                   self.rigUiInst)

        # add the lowerarm twists
        self.outlinerWidgets[self.name + "_lowerarm_twist_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_lowerarm"])
        self.outlinerWidgets[self.name + "_lowerarm_twist_01"].setText(0, self.name + "_lowerarm_twist_01")
        self.createOffsetMoverButton(self.name + "_lowerarm_twist_01",
                                     self.outlinerWidgets[self.name + "_lowerarm_twist_01"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_lowerarm_twist_01"].setHidden(True)

        self.outlinerWidgets[self.name + "_lowerarm_twist_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_lowerarm"])
        self.outlinerWidgets[self.name + "_lowerarm_twist_02"].setText(0, self.name + "_lowerarm_twist_02")
        self.createOffsetMoverButton(self.name + "_lowerarm_twist_02",
                                     self.outlinerWidgets[self.name + "_lowerarm_twist_02"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_lowerarm_twist_02"].setHidden(True)

        self.outlinerWidgets[self.name + "_lowerarm_twist_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_lowerarm"])
        self.outlinerWidgets[self.name + "_lowerarm_twist_03"].setText(0, self.name + "_lowerarm_twist_03")
        self.createOffsetMoverButton(self.name + "_lowerarm_twist_03",
                                     self.outlinerWidgets[self.name + "_lowerarm_twist_03"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_lowerarm_twist_03"].setHidden(True)

        # add the hand
        self.outlinerWidgets[self.name + "_hand"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_lowerarm"])
        self.outlinerWidgets[self.name + "_hand"].setText(0, self.name + "_hand")
        self.createGlobalMoverButton(self.name + "_hand", self.outlinerWidgets[self.name + "_hand"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_hand", self.outlinerWidgets[self.name + "_hand"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_hand", self.outlinerWidgets[self.name + "_hand"], self.rigUiInst)

        # add the thumb
        self.outlinerWidgets[self.name + "_thumb_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_thumb_01"].setText(0, self.name + "_thumb_01")
        self.createGlobalMoverButton(self.name + "_thumb_01",
                                     self.outlinerWidgets[self.name + "_thumb_01"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_thumb_01",
                                     self.outlinerWidgets[self.name + "_thumb_01"], self.rigUiInst)

        self.outlinerWidgets[self.name + "_thumb_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_thumb_02"].setText(0, self.name + "_thumb_02")
        self.createGlobalMoverButton(self.name + "_thumb_02", self.outlinerWidgets[self.name + "_thumb_02"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_thumb_02", self.outlinerWidgets[self.name + "_thumb_02"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_thumb_02", self.outlinerWidgets[self.name + "_thumb_02"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_thumb_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_thumb_02"])
        self.outlinerWidgets[self.name + "_thumb_03"].setText(0, self.name + "_thumb_03")
        self.createGlobalMoverButton(self.name + "_thumb_03", self.outlinerWidgets[self.name + "_thumb_03"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_thumb_03", self.outlinerWidgets[self.name + "_thumb_03"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_thumb_03", self.outlinerWidgets[self.name + "_thumb_03"],
                                   self.rigUiInst)

        # add the index finger
        self.outlinerWidgets[self.name + "_index_metacarpal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_index_metacarpal"].setText(0, self.name + "_index_metacarpal")
        self.createGlobalMoverButton(self.name + "_index_metacarpal",
                                     self.outlinerWidgets[self.name + "_index_metacarpal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_metacarpal",
                                     self.outlinerWidgets[self.name + "_index_metacarpal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_index_metacarpal"].setHidden(True)

        self.outlinerWidgets[self.name + "_index_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_index_01"].setText(0, self.name + "_index_01")
        self.createGlobalMoverButton(self.name + "_index_01", self.outlinerWidgets[self.name + "_index_01"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_01", self.outlinerWidgets[self.name + "_index_01"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_index_01", self.outlinerWidgets[self.name + "_index_01"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_index_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_index_01"])
        self.outlinerWidgets[self.name + "_index_02"].setText(0, self.name + "_index_02")
        self.createGlobalMoverButton(self.name + "_index_02", self.outlinerWidgets[self.name + "_index_02"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index02", self.outlinerWidgets[self.name + "_index_02"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_index_02", self.outlinerWidgets[self.name + "_index_02"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_index_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_index_02"])
        self.outlinerWidgets[self.name + "_index_03"].setText(0, self.name + "_index_03")
        self.createGlobalMoverButton(self.name + "_index_03", self.outlinerWidgets[self.name + "_index_03"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_index_03", self.outlinerWidgets[self.name + "_index_03"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_index_03", self.outlinerWidgets[self.name + "_index_03"],
                                   self.rigUiInst)

        # add the middle finger
        self.outlinerWidgets[self.name + "_middle_metacarpal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_middle_metacarpal"].setText(0, self.name + "_middle_metacarpal")
        self.createGlobalMoverButton(self.name + "_middle_metacarpal",
                                     self.outlinerWidgets[self.name + "_middle_metacarpal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_metacarpal",
                                     self.outlinerWidgets[self.name + "_middle_metacarpal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_middle_metacarpal"].setHidden(True)

        self.outlinerWidgets[self.name + "_middle_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_middle_01"].setText(0, self.name + "_middle_01")
        self.createGlobalMoverButton(self.name + "_middle_01",
                                     self.outlinerWidgets[self.name + "_middle_01"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_01",
                                     self.outlinerWidgets[self.name + "_middle_01"], self.rigUiInst)
        self.createMeshMoverButton(self.name + "_middle_01", self.outlinerWidgets[self.name + "_middle_01"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_middle_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_middle_01"])
        self.outlinerWidgets[self.name + "_middle_02"].setText(0, self.name + "_middle_02")
        self.createGlobalMoverButton(self.name + "_middle_02", self.outlinerWidgets[self.name + "_middle_02"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_02", self.outlinerWidgets[self.name + "_middle_02"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_middle_02", self.outlinerWidgets[self.name + "_middle_02"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_middle_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_middle_02"])
        self.outlinerWidgets[self.name + "_middle_03"].setText(0, self.name + "_middle_03")
        self.createGlobalMoverButton(self.name + "_middle_03", self.outlinerWidgets[self.name + "_middle_03"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_middle_03", self.outlinerWidgets[self.name + "_middle_03"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_middle_03", self.outlinerWidgets[self.name + "_middle_03"],
                                   self.rigUiInst)

        # add the ring finger
        self.outlinerWidgets[self.name + "_ring_metacarpal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_ring_metacarpal"].setText(0, self.name + "_ring_metacarpal")
        self.createGlobalMoverButton(self.name + "_ring_metacarpal",
                                     self.outlinerWidgets[self.name + "_ring_metacarpal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_metacarpal",
                                     self.outlinerWidgets[self.name + "_ring_metacarpal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_ring_metacarpal"].setHidden(True)

        self.outlinerWidgets[self.name + "_ring_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_ring_01"].setText(0, self.name + "_ring_01")
        self.createGlobalMoverButton(self.name + "_ring_01", self.outlinerWidgets[self.name + "_ring_01"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_01", self.outlinerWidgets[self.name + "_ring_01"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ring_01", self.outlinerWidgets[self.name + "_ring_01"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_ring_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ring_01"])
        self.outlinerWidgets[self.name + "_ring_02"].setText(0, self.name + "_ring_02")
        self.createGlobalMoverButton(self.name + "_ring_02", self.outlinerWidgets[self.name + "_ring_02"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_02", self.outlinerWidgets[self.name + "_ring_02"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ring_02", self.outlinerWidgets[self.name + "_ring_02"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_ring_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_ring_02"])
        self.outlinerWidgets[self.name + "_ring_03"].setText(0, self.name + "_ring_03")
        self.createGlobalMoverButton(self.name + "_ring_03", self.outlinerWidgets[self.name + "_ring_03"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_ring_03", self.outlinerWidgets[self.name + "_ring_03"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_ring_03", self.outlinerWidgets[self.name + "_ring_03"],
                                   self.rigUiInst)

        # add the pinky finger
        self.outlinerWidgets[self.name + "_pinky_metacarpal"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_pinky_metacarpal"].setText(0, self.name + "_pinky_metacarpal")
        self.createGlobalMoverButton(self.name + "_pinky_metacarpal",
                                     self.outlinerWidgets[self.name + "_pinky_metacarpal"], self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_metacarpal",
                                     self.outlinerWidgets[self.name + "_pinky_metacarpal"], self.rigUiInst)
        self.outlinerWidgets[self.name + "_pinky_metacarpal"].setHidden(True)

        self.outlinerWidgets[self.name + "_pinky_01"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_hand"])
        self.outlinerWidgets[self.name + "_pinky_01"].setText(0, self.name + "_pinky_01")
        self.createGlobalMoverButton(self.name + "_pinky_01", self.outlinerWidgets[self.name + "_pinky_01"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_01", self.outlinerWidgets[self.name + "_pinky_01"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pinky_01", self.outlinerWidgets[self.name + "_pinky_01"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_pinky_02"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_pinky_01"])
        self.outlinerWidgets[self.name + "_pinky_02"].setText(0, self.name + "_pinky_02")
        self.createGlobalMoverButton(self.name + "_pinky_02", self.outlinerWidgets[self.name + "_pinky_02"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_02", self.outlinerWidgets[self.name + "_pinky_02"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pinky_02", self.outlinerWidgets[self.name + "_pinky_02"],
                                   self.rigUiInst)

        self.outlinerWidgets[self.name + "_pinky_03"] = QtWidgets.QTreeWidgetItem(
            self.outlinerWidgets[self.name + "_pinky_02"])
        self.outlinerWidgets[self.name + "_pinky_03"].setText(0, self.name + "_pinky_03")
        self.createGlobalMoverButton(self.name + "_pinky_03", self.outlinerWidgets[self.name + "_pinky_03"],
                                     self.rigUiInst)
        self.createOffsetMoverButton(self.name + "_pinky_03", self.outlinerWidgets[self.name + "_pinky_03"],
                                     self.rigUiInst)
        self.createMeshMoverButton(self.name + "_pinky_03", self.outlinerWidgets[self.name + "_pinky_03"],
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
    def updateSettingsUI(self):
        """
        Updates the skeleton settings UI based on the network node values for this module. Happens when the UI is
        launched and there are module metadata present
        """

        networkNode = self.returnNetworkNode

        upperarmTwists = cmds.getAttr(networkNode + ".armTwists")
        lowerarmTwists = cmds.getAttr(networkNode + ".forearmTwists")
        thumbJoints = cmds.getAttr(networkNode + ".thumbJoints")
        indexJoints = cmds.getAttr(networkNode + ".indexJoints")
        middleJoints = cmds.getAttr(networkNode + ".middleJoints")
        ringJoints = cmds.getAttr(networkNode + ".ringJoints")
        pinkyJoints = cmds.getAttr(networkNode + ".pinkyJoints")
        includeClav = cmds.getAttr(networkNode + ".includeClavicle")
        thumbMeta = cmds.getAttr(networkNode + ".thumbMeta")
        indexMeta = cmds.getAttr(networkNode + ".indexMeta")
        middleMeta = cmds.getAttr(networkNode + ".middleMeta")
        ringMeta = cmds.getAttr(networkNode + ".ringMeta")
        pinkyMeta = cmds.getAttr(networkNode + ".pinkyMeta")

        # update UI elements
        self.upperarmTwistNum.setValue(upperarmTwists)
        self.lowerarmTwistNum.setValue(lowerarmTwists)
        self.clavicleCB.setChecked(includeClav)

        self.thumbNum.setValue(thumbJoints)
        self.indexNum.setValue(indexJoints)
        self.middleNum.setValue(middleJoints)
        self.ringNum.setValue(ringJoints)
        self.pinkyNum.setValue(pinkyJoints)

        self.thumbMeta.setChecked(thumbMeta)
        self.indexMeta.setChecked(indexMeta)
        self.middleMeta.setChecked(middleMeta)
        self.ringMeta.setChecked(ringMeta)
        self.pinkyMeta.setChecked(pinkyMeta)

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

        # create list of the new created bones
        armJoints = []

        if self.clavicleCB.isChecked():
            armJoints.append(prefix + "clavicle" + suffix)
            armJoints.append(prefix + "upperarm" + suffix)
        else:
            armJoints.append(prefix + "upperarm" + suffix)

        # upperarm twists
        upperarmTwists = self.upperarmTwistNum.value()
        for i in range(upperarmTwists):
            armJoints.append(prefix + "upperarm_twist_0" + str(i + 1) + suffix)

        armJoints.append(prefix + "lowerarm" + suffix)

        # lowerarm twists
        lowerarmTwists = self.lowerarmTwistNum.value()
        for i in range(lowerarmTwists):
            armJoints.append(prefix + "lowerarm_twist_0" + str(i + 1) + suffix)

        armJoints.append(prefix + "hand" + suffix)

        # FINGERS
        thumbJoints = ["02", "03"]
        fingerJoints = ["01", "02", "03"]

        #  thumb
        thumbs = self.thumbNum.value()
        thumbMeta = self.thumbMeta.isChecked()
        if thumbMeta:
            armJoints.append(prefix + "thumb_01" + suffix)
        for i in range(thumbs):
            armJoints.append(prefix + "thumb_" + thumbJoints[i] + suffix)

        # index
        indexFingers = self.indexNum.value()
        indexMeta = self.indexMeta.isChecked()
        if indexMeta:
            armJoints.append(prefix + "index_metacarpal" + suffix)
        for i in range(indexFingers):
            armJoints.append(prefix + "index_" + fingerJoints[i] + suffix)

        # middle
        middleFingers = self.middleNum.value()
        middleMeta = self.middleMeta.isChecked()
        if middleMeta:
            armJoints.append(prefix + "middle_metacarpal" + suffix)
        for i in range(middleFingers):
            armJoints.append(prefix + "middle_" + fingerJoints[i] + suffix)

        # ring
        ringFingers = self.ringNum.value()
        ringMeta = self.ringMeta.isChecked()
        if ringMeta:
            armJoints.append(prefix + "ring_metacarpal" + suffix)
        for i in range(ringFingers):
            armJoints.append(prefix + "ring_" + fingerJoints[i] + suffix)

        # pinky
        pinkyFingers = self.pinkyNum.value()
        pinkyMeta = self.pinkyMeta.isChecked()
        if pinkyMeta:
            armJoints.append(prefix + "pinky_metacarpal" + suffix)
        for i in range(pinkyFingers):
            armJoints.append(prefix + "pinky_" + fingerJoints[i] + suffix)

        # build attrString
        attrString = ""
        for bone in armJoints:
            attrString += bone + "::"

        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # reset button
        self.applyButton.setEnabled(False)

        # update joint mover
        self._editJointMoverViaSpinBox(self.thumbNum, "thumb", True)
        self._editJointMoverViaSpinBox(self.indexNum, "index", False)
        self._editJointMoverViaSpinBox(self.middleNum, "middle", False)
        self._editJointMoverViaSpinBox(self.ringNum, "ring", False)
        self._editJointMoverViaSpinBox(self.pinkyNum, "pinky", False)

        self._editJointMoverTwistBones(self.upperarmTwistNum, "upperarm")
        self._editJointMoverTwistBones(self.lowerarmTwistNum, "lowerarm")

        self._editJointMoverMetaCarpals(self.thumbMeta, "thumb")
        self._editJointMoverMetaCarpals(self.indexMeta, "index")
        self._editJointMoverMetaCarpals(self.middleMeta, "middle")
        self._editJointMoverMetaCarpals(self.ringMeta, "ring")
        self._editJointMoverMetaCarpals(self.pinkyMeta, "pinky")

        self.includeClavicle()

        # set network node attributes
        cmds.setAttr(networkNode + ".armTwists", lock=False)
        cmds.setAttr(networkNode + ".armTwists", upperarmTwists, lock=True)

        cmds.setAttr(networkNode + ".forearmTwists", lock=False)
        cmds.setAttr(networkNode + ".forearmTwists", lowerarmTwists, lock=True)

        cmds.setAttr(networkNode + ".thumbJoints", lock=False)
        cmds.setAttr(networkNode + ".thumbJoints", thumbs, lock=True)

        cmds.setAttr(networkNode + ".indexJoints", lock=False)
        cmds.setAttr(networkNode + ".indexJoints", indexFingers, lock=True)

        cmds.setAttr(networkNode + ".middleJoints", lock=False)
        cmds.setAttr(networkNode + ".middleJoints", middleFingers, lock=True)

        cmds.setAttr(networkNode + ".ringJoints", lock=False)
        cmds.setAttr(networkNode + ".ringJoints", ringFingers, lock=True)

        cmds.setAttr(networkNode + ".pinkyJoints", lock=False)
        cmds.setAttr(networkNode + ".pinkyJoints", pinkyFingers, lock=True)

        cmds.setAttr(networkNode + ".includeClavicle", lock=False)
        cmds.setAttr(networkNode + ".includeClavicle", self.clavicleCB.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".thumbMeta", lock=False)
        cmds.setAttr(networkNode + ".thumbMeta", self.thumbMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".indexMeta", lock=False)
        cmds.setAttr(networkNode + ".indexMeta", self.indexMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".ringMeta", lock=False)
        cmds.setAttr(networkNode + ".ringMeta", self.ringMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".middleMeta", lock=False)
        cmds.setAttr(networkNode + ".middleMeta", self.middleMeta.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".pinkyMeta", lock=False)
        cmds.setAttr(networkNode + ".pinkyMeta", self.pinkyMeta.isChecked(), lock=True)

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

        for i in range(4):

            networkNode = self.returnNetworkNode
            attrs = cmds.listAttr(networkNode, ud=True)

            for attr in attrs:
                attrType = str(cmds.getAttr(networkNode + "." + attr, type=True))

                if attrType == "double":
                    if attr.find("Joints") == -1:
                        cmds.setAttr(networkNode + "." + attr, lock=False)
                        cmds.setAttr(networkNode + "." + attr, 0, lock=True)
                    else:
                        if attr.find("thumb") != -1:
                            cmds.setAttr(networkNode + "." + attr, lock=False)
                            cmds.setAttr(networkNode + "." + attr, 2, lock=True)
                        else:
                            cmds.setAttr(networkNode + "." + attr, lock=False)
                            cmds.setAttr(networkNode + "." + attr, 3, lock=True)

                if attrType == "bool":
                    if attr.find("thumbMeta") != -1 or attr.find("includeClavicle") != -1:
                        cmds.setAttr(networkNode + "." + attr, lock=False)
                        cmds.setAttr(networkNode + "." + attr, True, lock=True)

                    else:
                        cmds.setAttr(networkNode + "." + attr, lock=False)
                        cmds.setAttr(networkNode + "." + attr, False, lock=True)

                if attrType == "enum":
                    cmds.setAttr(networkNode + "." + attr, lock=False)
                    cmds.setAttr(networkNode + "." + attr, 0, lock=True)

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
        includeClav = cmds.getAttr(networkNode + ".includeClavicle")

        if state:
            if cmds.getAttr(networkNode + ".pinned") is True:
                return

            if includeClav:
                topLevelMover = self.name + "_clavicle_mover"
            else:
                topLevelMover = self.name + "_upperarm_mover"

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

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRigCustom(self, textEdit, uiInst):

        # get the network node and gather other needed data
        networkNode = self.returnNetworkNode
        armJoints = self._getMainArmJoints()

        # create a new network node to hold the control types
        self._createControlNode(networkNode)

        # have it build all rigs by default, unless there is an attr stating otherwise (backwards-compatability)
        numRigs = 2
        builtRigs = []

        # create groups and settings
        self._createRigGroups(networkNode, numRigs, armJoints)

        # build the rigs
        # if build FK was true, build the FK rig now
        self.buildFkArm(textEdit, uiInst, builtRigs, networkNode)
        builtRigs.append(["FK", [self.armCtrlGrp]])

        # if build IK was true, build the IK rig now
        ikArmJoints = self.buildIkArm(textEdit, uiInst, builtRigs, networkNode)
        builtRigs.append(["IK", [self.ikCtrlGrp]])

        # #create upper arm twist rig
        self._createUpperArmTwists(networkNode, armJoints)

        # create lowerarm twist rig
        self._createLowerArmTwists(networkNode, armJoints)

        # # #build finger rigs (if needed)
        fingers = self._getFingerJoints()
        if len(fingers) > 0:
            self.fingerGrp = cmds.group(empty=True, name=self.name + "_finger_group")
            constraint = cmds.parentConstraint(armJoints[1][2], self.fingerGrp)[0]
            cmds.delete(constraint)
            cmds.parent(self.fingerGrp, self.armGroup)
            self.buildFingers(fingers, textEdit, uiInst, builtRigs, networkNode)

        cmds.parent(ikArmJoints[0], self.armCtrlGrp)

        # Rig Clavicle
        if cmds.getAttr(networkNode + ".includeClavicle"):
            self.buildClavicleRig(textEdit, uiInst, builtRigs, networkNode)

            # Hook up ArmCtrlGrp
            attrData = self._hookUpArm(networkNode, armJoints)

            # setup set driven keys on our mode attr and those target attributes
            self._setupClavMode(networkNode, numRigs, attrData)

        # Hook up FK/IK Switching
        self._setupRigModes(numRigs, builtRigs, armJoints)

        # parent under offset_anim if it exists(it always should)
        if cmds.objExists("offset_anim"):
            cmds.parent(self.armGroup, "offset_anim")

        # return data
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        try:
            if cmds.getAttr(networkNode + ".includeClavicle"):
                uiInst.rigData.append([self.name + "_auto_clav_grp", "driver_" + parentBone, numRigs])
                uiInst.rigData.append([self.clavCtrlGrp, "driver_" + parentBone, numRigs])

            else:
                uiInst.rigData.append([self.armCtrlGrp, "driver_" + parentBone, numRigs])
        except Exception, e:
            print "ART_Arm_Standard: buildRigCustom:  " + str(e)

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
        armJoints = []
        clavJoint = None

        fingers = []
        controlNode = cmds.listConnections(networkNode + ".controls")[0]
        if cmds.objExists(controlNode + ".fkFingerControls"):
            fingers = self.getControls(False, "fkFingerControls")

        for bone in splitJoints:
            if bone != "":
                createdJoints.append(bone)

        for joint in createdJoints:
            if joint.find("upperarm") != -1:
                if joint.find("twist") == -1:
                    upArmJnt = joint
                    armJoints.append(upArmJnt)

            if joint.find("lowerarm") != -1:
                if joint.find("twist") == -1:
                    loArmJnt = joint
                    armJoints.append(loArmJnt)

            if joint.find("hand") != -1:
                handJoint = joint
                armJoints.append(handJoint)

            if joint.find("clavicle") != -1:
                clavJoint = joint

        solveClav = False
        clavControls = None
        if cmds.getAttr(networkNode + ".includeClavicle"):
            solveClav = True
            clavControls = self.getControls(False, "clavControls")
            clavControls = sorted(clavControls)

        if len(fingers) > 0:
            for finger in fingers:
                joint = finger.partition(":")[2].partition("_anim")[0]
                cmds.orientConstraint(joint, finger)
                returnControls.append(finger)

        # Handle Import Method/Constraints
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if importMethod == "FK":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 0)
            cmds.setAttr(character + ":" + moduleName + "_settings.clavMode", 0)

            if solveClav:
                cmds.orientConstraint(clavJoint, clavControls[0], mo=True)
                returnControls.append(clavControls[0])

            for joint in armJoints:
                cmds.orientConstraint(joint, character + ":fk_" + joint + "_anim", mo=True)
                returnControls.append(character + ":fk_" + joint + "_anim")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if importMethod == "IK":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 1)
            cmds.setAttr(character + ":" + moduleName + "_settings.clavMode", 1)

            if solveClav:
                cmds.pointConstraint(armJoints[0], clavControls[1])
                returnControls.append(clavControls[1])

            cmds.parentConstraint(armJoints[2], character + ":ik_" + armJoints[2] + "_anim", mo=True)
            returnControls.append(character + ":ik_" + armJoints[2] + "_anim")

            cmds.pointConstraint(armJoints[1], character + ":" + self.name + "_ik_elbow_anim", mo=True)
            returnControls.append(character + ":" + self.name + "_ik_elbow_anim")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if importMethod == "Both":
            cmds.setAttr(character + ":" + moduleName + "_settings.mode", 1)
            cmds.setAttr(character + ":" + moduleName + "_settings.clavMode", 1)

            if solveClav:
                cmds.orientConstraint(clavJoint, clavControls[0])
                returnControls.append(clavControls[0])

                cmds.pointConstraint(armJoints[0], clavControls[1])
                returnControls.append(clavControls[1])

            cmds.parentConstraint(armJoints[2], character + ":ik_" + armJoints[2] + "_anim", mo=True)
            returnControls.append(character + ":ik_" + armJoints[2] + "_anim")

            cmds.pointConstraint(armJoints[1], character + ":" + self.name + "_ik_elbow_anim", mo=True)
            returnControls.append(character + ":" + self.name + "_ik_elbow_anim")

            for joint in armJoints:
                cmds.orientConstraint(joint, character + ":fk_" + joint + "_anim", mo=True)
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
    def selectRigControls(self, mode):
        """
        (BASE CLASS OVERRIDE!)
        This method calls on getControls to return a list of the controls and the selects them.
        """

        fkControls = ["fkControls", "upArmTwistControls", "loArmTwistControls", "fkFingerControls", "clavControls"]
        ikControls = ["ikControls", "ikFingerControls", "clavControls"]

        cmds.select(clear=True)

        clavControls = self.getControls(False, "clavControls")
        clavControls = sorted(clavControls)

        # select all controls
        if mode == "all":
            controls = self.getControls()
            for each in controls:
                for control in each:
                    cmds.select(each, add=True)

        # select fk controls
        if mode == "fk":
            fkControls = self.getControls(False, "fkControls")
            fkControls.extend(self.getControls(False, "upArmTwistControls"))
            fkControls.extend(self.getControls(False, "loArmTwistControls"))
            fkControls.extend(self.getControls(False, "fkFingerControls"))
            if len(clavControls) > 0:
                fkControls.append(clavControls[0])

            for control in fkControls:
                cmds.select(control, add=True)

        # select ik controls
        if mode == "ik":
            ikControls = self.getControls(False, "ikControls")
            ikControls.extend(self.getControls(False, "ikFingerControls"))
            if len(clavControls) > 0:
                ikControls.append(clavControls[1])

            for control in ikControls:
                cmds.select(control, add=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setupPickWalking(self):
        """
        Sets up custom pickwalking between rig controls.

        .. note:: Current limitations: IK fingers are not setup to work with pickwalking as I don't assume they'll get
                  much use. If they need pickwalking in the future, it can be added.

                  Also, twist controls can not currently be pick-walked to from IK controls.

        :return: returns list of top level controls of the module that will need hooks to their parent controls
        """

        # get controls
        networkNode = self.returnNetworkNode

        fkControls = self.getControls(False, "fkControls")
        fkControls = sorted(fkControls)
        ikControls = self.getControls(False, "ikControls")
        ikControls = sorted(ikControls)
        ikControls.reverse()
        upArmTwistControls = self.getControls(False, "upArmTwistControls")
        upArmTwistControls = sorted(upArmTwistControls)
        loArmTwistControls = self.getControls(False, "loArmTwistControls")
        loArmTwistControls = sorted(loArmTwistControls)
        clavControls = []
        if cmds.getAttr(networkNode + ".includeClavicle") is True:
            clavControls = self.getControls(False, "clavControls")
            clavControls = sorted(clavControls)

        # setup FK pickwalking on arm
        if len(clavControls) > 0:
            cmds.addAttr(clavControls[0], ln="pickWalkDown", at="message")
            cmds.connectAttr(fkControls[2] + ".message", clavControls[0] + ".pickWalkDown")

            cmds.addAttr(fkControls[2], ln="pickWalkUp", at="message")
            cmds.connectAttr(clavControls[0] + ".message", fkControls[2] + ".pickWalkUp")

        cmds.addAttr(fkControls[2], ln="pickWalkDown", at="message")
        cmds.connectAttr(fkControls[1] + ".message", fkControls[2] + ".pickWalkDown")

        if upArmTwistControls is not None:
            if len(upArmTwistControls) > 0:

                if len(upArmTwistControls) == 1:
                    cmds.addAttr(fkControls[2], ln="pickWalkRight", at="message")
                    cmds.connectAttr(upArmTwistControls[0] + ".message", fkControls[2] + ".pickWalkRight")

                    cmds.addAttr(fkControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(upArmTwistControls[0] + ".message", fkControls[2] + ".pickWalkLeft")

                    cmds.addAttr(upArmTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[2] + ".message", upArmTwistControls[0] + ".pickWalkUp")

                if len(upArmTwistControls) == 2:
                    cmds.addAttr(fkControls[2], ln="pickWalkRight", at="message")
                    cmds.connectAttr(upArmTwistControls[0] + ".message", fkControls[2] + ".pickWalkRight")

                    cmds.addAttr(fkControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(upArmTwistControls[1] + ".message", fkControls[2] + ".pickWalkLeft")

                    cmds.addAttr(upArmTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[2] + ".message", upArmTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(upArmTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[2] + ".message", upArmTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(upArmTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(upArmTwistControls[1] + ".message", upArmTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(upArmTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(upArmTwistControls[0] + ".message", upArmTwistControls[1] + ".pickWalkLeft")

                if len(upArmTwistControls) == 3:
                    cmds.addAttr(fkControls[2], ln="pickWalkRight", at="message")
                    cmds.connectAttr(upArmTwistControls[0] + ".message", fkControls[2] + ".pickWalkRight")

                    cmds.addAttr(fkControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(upArmTwistControls[2] + ".message", fkControls[2] + ".pickWalkLeft")

                    cmds.addAttr(upArmTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(upArmTwistControls[1] + ".message", upArmTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(upArmTwistControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(upArmTwistControls[2] + ".message", upArmTwistControls[1] + ".pickWalkRight")

                    cmds.addAttr(upArmTwistControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(upArmTwistControls[1] + ".message", upArmTwistControls[2] + ".pickWalkLeft")

                    cmds.addAttr(upArmTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(upArmTwistControls[0] + ".message", upArmTwistControls[1] + ".pickWalkLeft")

                    cmds.addAttr(upArmTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[2] + ".message", upArmTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(upArmTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[2] + ".message", upArmTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(upArmTwistControls[2], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[2] + ".message", upArmTwistControls[2] + ".pickWalkUp")

        cmds.addAttr(fkControls[1], ln="pickWalkDown", at="message")
        cmds.connectAttr(fkControls[0] + ".message", fkControls[1] + ".pickWalkDown")

        cmds.addAttr(fkControls[1], ln="pickWalkUp", at="message")
        cmds.connectAttr(fkControls[2] + ".message", fkControls[1] + ".pickWalkUp")

        if loArmTwistControls is not None:
            if len(loArmTwistControls) > 0:

                if len(loArmTwistControls) == 1:
                    cmds.addAttr(fkControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(loArmTwistControls[0] + ".message", fkControls[1] + ".pickWalkRight")

                    cmds.addAttr(fkControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(loArmTwistControls[0] + ".message", fkControls[1] + ".pickWalkLeft")

                    cmds.addAttr(loArmTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[1] + ".message", loArmTwistControls[0] + ".pickWalkUp")

                if len(loArmTwistControls) == 2:
                    cmds.addAttr(fkControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(loArmTwistControls[0] + ".message", fkControls[1] + ".pickWalkRight")

                    cmds.addAttr(fkControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(loArmTwistControls[1] + ".message", fkControls[1] + ".pickWalkLeft")

                    cmds.addAttr(loArmTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[1] + ".message", loArmTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(loArmTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[1] + ".message", loArmTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(loArmTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(loArmTwistControls[1] + ".message", loArmTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(loArmTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(loArmTwistControls[0] + ".message", loArmTwistControls[1] + ".pickWalkLeft")

                if len(loArmTwistControls) == 3:
                    cmds.addAttr(fkControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(loArmTwistControls[0] + ".message", fkControls[1] + ".pickWalkRight")

                    cmds.addAttr(fkControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(loArmTwistControls[2] + ".message", fkControls[1] + ".pickWalkLeft")

                    cmds.addAttr(loArmTwistControls[0], ln="pickWalkRight", at="message")
                    cmds.connectAttr(loArmTwistControls[1] + ".message", loArmTwistControls[0] + ".pickWalkRight")

                    cmds.addAttr(loArmTwistControls[1], ln="pickWalkRight", at="message")
                    cmds.connectAttr(loArmTwistControls[2] + ".message", loArmTwistControls[1] + ".pickWalkRight")

                    cmds.addAttr(loArmTwistControls[2], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(loArmTwistControls[1] + ".message", loArmTwistControls[2] + ".pickWalkLeft")

                    cmds.addAttr(loArmTwistControls[1], ln="pickWalkLeft", at="message")
                    cmds.connectAttr(loArmTwistControls[0] + ".message", loArmTwistControls[1] + ".pickWalkLeft")

                    cmds.addAttr(loArmTwistControls[0], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[1] + ".message", loArmTwistControls[0] + ".pickWalkUp")

                    cmds.addAttr(loArmTwistControls[1], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[1] + ".message", loArmTwistControls[1] + ".pickWalkUp")

                    cmds.addAttr(loArmTwistControls[2], ln="pickWalkUp", at="message")
                    cmds.connectAttr(fkControls[1] + ".message", loArmTwistControls[2] + ".pickWalkUp")

        cmds.addAttr(fkControls[0], ln="pickWalkUp", at="message")
        cmds.connectAttr(fkControls[1] + ".message", fkControls[0] + ".pickWalkUp")

        # Setup pickwalking on IK controls
        if len(clavControls) > 0:
            cmds.addAttr(clavControls[1], ln="pickWalkDown", at="message")
            cmds.connectAttr(ikControls[1] + ".message", clavControls[1] + ".pickWalkDown")

            cmds.addAttr(ikControls[1], ln="pickWalkUp", at="message")
            cmds.connectAttr(clavControls[1] + ".message", ikControls[1] + ".pickWalkUp")

        cmds.addAttr(ikControls[1], ln="pickWalkDown", at="message")
        cmds.connectAttr(ikControls[0] + ".message", ikControls[1] + ".pickWalkDown")

        cmds.addAttr(ikControls[0], ln="pickWalkUp", at="message")
        cmds.connectAttr(ikControls[1] + ".message", ikControls[0] + ".pickWalkUp")

        # Fingers
        # create a list of all possible fingers
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")
        modName = cmds.getAttr(networkNode + ".moduleName")

        splitString = modName.split(baseName)
        prefix = splitString[0]
        suffix = splitString[1]

        baseThumbs = ["thumb_0l", "thumb_02", "thumb_03", "bigtoe_dummy"]
        baseIndexs = ["index_metacarpal", "index_01", "index_02", "index_03"]
        baseMiddles = ["middle_metacarpal", "middle_01", "middle_02", "middle_03"]
        baseRings = ["ring_metacarpal", "ring_01", "ring_02", "ring_03"]
        basePinkys = ["pinky_metacarpal", "pinky_01", "pinky_02", "pinky_03"]

        # go through the base fingers, and append our prefix and suffix to create our true finger names
        thumbs = []
        indexFingers = []
        middleFingers = []
        ringFingers = []
        pinkyFingers = []

        for finger in baseThumbs:
            string = prefix + finger + suffix + "_anim"
            thumbs.append(string)
        for finger in baseIndexs:
            string = prefix + finger + suffix + "_anim"
            indexFingers.append(string)
        for finger in baseMiddles:
            string = prefix + finger + suffix + "_anim"
            middleFingers.append(string)
        for finger in baseRings:
            string = prefix + finger + suffix + "_anim"
            ringFingers.append(string)
        for finger in basePinkys:
            string = prefix + finger + suffix + "_anim"
            pinkyFingers.append(string)

        # setup pickwalking logic
        finger_sets = [thumbs, indexFingers, middleFingers, ringFingers, pinkyFingers]
        i = 0

        for finger_set in finger_sets:
            for index in range(len(finger_set)):

                # check if finger exists
                if cmds.objExists(finger_set[index]):
                    # setup pickwalk down to this control relationship
                    if not cmds.objExists(ikControls[0] + ".pickWalkRight"):
                        cmds.addAttr(ikControls[0], ln="pickWalkRight", at="message")
                        cmds.connectAttr(finger_set[index] + ".message", ikControls[0] + ".pickWalkRight")

                    if not cmds.objExists(finger_set[index] + ".pickWalkLeft"):
                        cmds.addAttr(finger_set[index], ln="pickWalkLeft", at="message")
                        cmds.connectAttr(ikControls[0] + ".message", finger_set[index] + ".pickWalkLeft")

                    if not cmds.objExists(fkControls[0] + ".pickWalkRight"):
                        cmds.addAttr(fkControls[0], ln="pickWalkRight", at="message")
                        cmds.connectAttr(finger_set[index] + ".message", fkControls[0] + ".pickWalkRight")

                    if not cmds.objExists(finger_set[index] + ".pickWalkLeft"):
                        cmds.addAttr(finger_set[index], ln="pickWalkLeft", at="message")
                        cmds.connectAttr(fkControls[0] + ".message", finger_set[index] + ".pickWalkLeft")

                    # setup pickwalking down to next control
                    try:
                        if cmds.objExists(finger_set[index + 1]):
                            if not cmds.objExists(finger_set[index] + ".pickWalkDown"):
                                cmds.addAttr(finger_set[index], ln="pickWalkDown", at="message")
                                cmds.connectAttr(finger_set[index + 1] + ".message", finger_set[index] + ".pickWalkDown")

                                cmds.addAttr(finger_set[index + 1], ln="pickWalkUp", at="message")
                                cmds.connectAttr(finger_set[index] + ".message", finger_set[index + 1] + ".pickWalkUp")

                    except IndexError, e:
                        pass

                    # setup pickwalking left and right from this control
                    for x in range(i + 1, 5):
                        try:
                            if cmds.objExists(finger_sets[x][index]):
                                if not cmds.objExists(finger_set[index] + ".pickWalkRight"):
                                    cmds.addAttr(finger_set[index], ln="pickWalkRight", at="message")
                                    cmds.connectAttr(finger_sets[x][index] + ".message", finger_set[index] + ".pickWalkRight")
                                    break
                        except IndexError:
                            pass

                    for x in reversed(range(0, i)):
                        try:
                            if cmds.objExists(finger_sets[x][index]):
                                if not cmds.objExists(finger_set[index] + ".pickWalkLeft"):
                                    cmds.addAttr(finger_set[index], ln="pickWalkLeft", at="message")
                                    cmds.connectAttr(finger_sets[x][index] + ".message", finger_set[index] + ".pickWalkLeft")
                                    break
                        except IndexError:
                            pass
            i += 1

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
        armAim = [1, 0, 0]
        armUp = [0, 1, 0]
        handAim = [1, 0, 0]
        handUp = [0, -1, 0]

        if side == "Right":
            armAim = [-1, 0, 0]
            armUp = [0, -1, 0]
            handAim = [-1, 0, 0]
            handUp = [0, 1, 0]

        # if passed in state is True:
        if state:
            # setup aim constraints

            # clavicle
            cmds.aimConstraint(name + "_upperarm_lra", name + "_clavicle_mover_geo", aimVector=armAim,
                               upVector=armUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_upperarm_lra", mo=True)

            cmds.aimConstraint(name + "_upperarm_lra", name + "_clavicle_mover_offset", aimVector=armAim,
                               upVector=armUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_upperarm_lra", mo=True)

            # upperarm
            cmds.aimConstraint(name + "_lowerarm_lra", name + "_upperarm_mover_geo", aimVector=armAim,
                               upVector=armUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_lowerarm_lra", mo=True)

            cmds.aimConstraint(name + "_lowerarm_lra", name + "_upperarm_mover_offset", aimVector=armAim,
                               upVector=armUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_lowerarm_lra", mo=True)

            # lowerarm
            cmds.aimConstraint(name + "_hand_lra", name + "_lowerarm_mover_offset", aimVector=armAim,
                               upVector=armUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                               worldUpObject=name + "_lowerarm_lra", mo=True)

            # index finger
            if cmds.getAttr(name + "_index_metacarpal_mover_grp.v"):
                cmds.aimConstraint(name + "_index_01_lra", name + "_index_metacarpal_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_01_lra", mo=True)

            if cmds.getAttr(name + "_index_01_mover_grp.v"):
                cmds.aimConstraint(name + "_index_02_lra", name + "_index_01_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_02_lra", mo=True)

                cmds.aimConstraint(name + "_index_02_lra", name + "_index_01_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_02_lra", mo=True)

            if cmds.getAttr(name + "_index_02_mover_grp.v"):
                cmds.aimConstraint(name + "_index_03_lra", name + "_index_02_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_03_lra", mo=True)

                cmds.aimConstraint(name + "_index_03_lra", name + "_index_02_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_index_03_lra", mo=True)

            # middle finger
            if cmds.getAttr(name + "_middle_metacarpal_mover_grp.v"):
                cmds.aimConstraint(name + "_middle_01_lra", name + "_middle_metacarpal_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_01_lra", mo=True)

            if cmds.getAttr(name + "_middle_01_mover_grp.v"):
                cmds.aimConstraint(name + "_middle_02_lra", name + "_middle_01_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_02_lra", mo=True)

                cmds.aimConstraint(name + "_middle_02_lra", name + "_middle_01_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_02_lra", mo=True)

            if cmds.getAttr(name + "_middle_02_mover_grp.v"):
                cmds.aimConstraint(name + "_middle_03_lra", name + "_middle_02_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_03_lra", mo=True)

                cmds.aimConstraint(name + "_middle_03_lra", name + "_middle_02_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_middle_03_lra", mo=True)

            # ring finger
            if cmds.getAttr(name + "_ring_metacarpal_mover_grp.v"):
                cmds.aimConstraint(name + "_ring_01_lra", name + "_ring_metacarpal_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_01_lra", mo=True)

            if cmds.getAttr(name + "_ring_01_mover_grp.v"):
                cmds.aimConstraint(name + "_ring_02_lra", name + "_ring_01_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_02_lra", mo=True)

                cmds.aimConstraint(name + "_ring_02_lra", name + "_ring_01_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_02_lra", mo=True)

            if cmds.getAttr(name + "_ring_02_mover_grp.v"):
                cmds.aimConstraint(name + "_ring_03_lra", name + "_ring_02_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_03_lra", mo=True)

                cmds.aimConstraint(name + "_ring_03_lra", name + "_ring_02_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_ring_03_lra", mo=True)

            # pinky finger
            if cmds.getAttr(name + "_pinky_metacarpal_mover_grp.v"):
                cmds.aimConstraint(name + "_pinky_01_lra", name + "_pinky_metacarpal_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_01_lra", mo=True)

            if cmds.getAttr(name + "_pinky_01_mover_grp.v"):
                cmds.aimConstraint(name + "_pinky_02_lra", name + "_pinky_01_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_02_lra", mo=True)

                cmds.aimConstraint(name + "_pinky_02_lra", name + "_pinky_01_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_02_lra", mo=True)

            if cmds.getAttr(name + "_pinky_02_mover_grp.v"):
                cmds.aimConstraint(name + "_pinky_03_lra", name + "_pinky_02_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_03_lra", mo=True)

                cmds.aimConstraint(name + "_pinky_03_lra", name + "_pinky_02_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_pinky_03_lra", mo=True)

            # thumb finger
            if cmds.getAttr(name + "_thumb_01_mover_grp.v"):
                cmds.aimConstraint(name + "_thumb_02_lra", name + "_thumb_01_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_thumb_02_lra", mo=True)

            if cmds.getAttr(name + "_thumb_02_mover_grp.v"):
                cmds.aimConstraint(name + "_thumb_03_lra", name + "_thumb_02_mover_geo",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_thumb_03_lra", mo=True)

                cmds.aimConstraint(name + "_thumb_03_lra", name + "_thumb_02_mover_offset",
                                   aimVector=handAim, upVector=handUp, skip="x", wut="objectrotation", wu=[0, 1, 0],
                                   worldUpObject=name + "_thumb_03_lra", mo=True)

        # if passed in state is False:
        if not state:
            cmds.select(name + "_mover_grp", hi=True)
            aimConstraints = cmds.ls(sl=True, exactType="aimConstraint")

            for constraint in aimConstraints:
                cmds.lockNode(constraint, lock=False)
                cmds.delete(constraint)

            self.bakeOffsets()
            cmds.select(clear=True)

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
    def _getMainArmJoints(self):

        clavicleJoint = None
        upperarmJoint = None
        lowerarmJoint = None
        handJoint = None

        returnData = []

        joints = self.returnCreatedJoints

        # clavicle
        for joint in joints:
            if joint.find("clavicle") != -1:
                clavicleJoint = joint

        # upperarm
        joints = self.returnCreatedJoints
        for joint in joints:
            if joint.find("upperarm") != -1:
                if joint.find("twist") == -1:
                    upperarmJoint = joint

        # lowerarm
        for joint in joints:
            if joint.find("lowerarm") != -1:
                if joint.find("twist") == -1:
                    lowerarmJoint = joint

        # hand
        for joint in joints:
            if joint.find("hand") != -1:
                handJoint = joint

        returnData = [clavicleJoint, [upperarmJoint, lowerarmJoint, handJoint]]
        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getTwistJoints(self, upperarm, lowerarm):

        upperTwistBones = []
        lowerTwistBones = []

        joints = self.returnCreatedJoints

        # upper arm
        for joint in joints:
            if joint.find("upperarm") != -1:
                if joint.find("twist") != -1:
                    upperTwistBones.append(joint)

        # calf
        for joint in joints:
            if joint.find("lowerarm") != -1:
                if joint.find("twist") != -1:
                    lowerTwistBones.append(joint)

        if upperarm:
            return upperTwistBones
        if lowerarm:
            return lowerTwistBones

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getarmScale(self, joint):

        default = 30.0

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
    def _getFingerJoints(self):

        joints = self.returnCreatedJoints
        indexJoints = []
        middleJoints = []
        ringJoints = []
        pinkyJoints = []
        thumbJoints = []

        for joint in joints:

            if joint.find("thumb") != -1:
                thumbJoints.append(joint)

            if joint.find("index") != -1:
                indexJoints.append(joint)

            if joint.find("middle") != -1:
                if joint.find("index") == -1:
                    if joint.find("ring") == -1:
                        if joint.find("pinky") == -1:
                            middleJoints.append(joint)

            if joint.find("ring") != -1:
                ringJoints.append(joint)

            if joint.find("pinky") != -1:
                pinkyJoints.append(joint)

        returnData = []
        for each in [indexJoints, middleJoints, ringJoints, pinkyJoints, thumbJoints]:
            if each != []:
                returnData.append(each)
        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _getFingerBaseName(self, finger):

        nameData = self.returnPrefixSuffix
        if nameData[0] is not None:
            if nameData[1] is not None:
                jointName = finger.partition(nameData[0] + "_")[2].partition("_" + nameData[1])[0]
            else:
                jointName = finger.partition(nameData[0] + "_")[2]
        else:
            if nameData[1] is not None:
                jointName = finger.partition("_" + nameData[1])[0]
            else:
                jointName = finger.partition("_")[0]

        return jointName

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
                    except Exception:
                        pass

            # fire script job that watches the coplanarIkHandle attributes, and when they change, snap to IK knee in tz
            self.coplanarScriptJob1 = cmds.scriptJob(attributeChange=[self.name + "_coplanarIkHandle.translate",
                                                                      partial(riggingUtils.coPlanarModeSnap,
                                                                              self,
                                                                              self.name + "_coplanar_lowerarm",
                                                                              self.name + "_lowerarm_mover_offset",
                                                                              [self.name + "_coplanar_upperarm",
                                                                               self.name + "_coplanar_lowerarm"],
                                                                              [
                                                                                  self.name + "_upperarm_mover_offset",
                                                                                  self.name + "_lowerarm_mover_offset"],
                                                                              self.name + "_lowerarm_mover_offset",
                                                                              [])], kws=True)

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
    def includeClavicle(self, *args):
        """
        Set visibility and parenting on the joint movers depending on whether the include clavicle checkbox is true or
        false.
        """

        state = self.clavicleCB.isChecked()

        if state is False:

            # hide clavicle mover controls
            cmds.setAttr(self.name + "_clavicle_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_clavicle_mover_grp.v", 0, lock=True)

            # parent upperarm to mover_grp
            try:
                cmds.parent(self.name + "_upperarm_mover_grp", self.name + "_mover_grp")
            except Exception, e:
                print e

        if state is True:

            # show clavicle mover controls
            cmds.setAttr(self.name + "_clavicle_mover_grp.v", lock=False)
            cmds.setAttr(self.name + "_clavicle_mover_grp.v", 1, lock=True)

            # parent upperarm to mover_grp
            try:
                cmds.parent(self.name + "_upperarm_mover_grp", self.name + "_clavicle_mover")
            except Exception, e:
                print e

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def switchFingerMode(self, mode, finger, range=False):
        """
        Switch the rig mode on the finger to FK or IK, matching the pose of the current mode.

        :param mode: Which mode to switch to (FK, IK)
        :param finger: which finger to operate on
        :param range: Whether or not to switch/match over a range
        :return:
        """

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        # switch to FK mode
        if mode == "FK":
            if finger == "All":
                cmds.setAttr(namespace + ":" + self.name + "_settings.index_finger_mode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.index_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.middle_finger_mode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.middle_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.ring_finger_mode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.ring_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.pinky_finger_mode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.pinky_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.thumb_finger_mode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.thumb_finger_mode")

            else:
                if finger.partition(namespace)[2].find(":index") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.index_finger_mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.index_finger_mode")

                if finger.partition(namespace)[2].find(":middle") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.middle_finger_mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.middle_finger_mode")

                if finger.partition(namespace)[2].find(":ring") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.ring_finger_mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.ring_finger_mode")

                if finger.partition(namespace)[2].find(":pinky") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.pinky_finger_mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.pinky_finger_mode")

                if finger.partition(namespace)[2].find(":thumb") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.thumb_finger_mode", 0.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.thumb_finger_mode")

        if mode == "IK":

            if finger == "All":
                cmds.setAttr(namespace + ":" + self.name + "_settings.index_finger_mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.index_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.middle_finger_mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.middle_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.ring_finger_mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.ring_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.pinky_finger_mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.pinky_finger_mode")
                cmds.setAttr(namespace + ":" + self.name + "_settings.thumb_finger_mode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.thumb_finger_mode")

            else:
                if finger.partition(namespace)[2].find(":index") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.index_finger_mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.index_finger_mode")

                if finger.partition(namespace)[2].find(":middle") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.middle_finger_mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.middle_finger_mode")

                if finger.partition(namespace)[2].find(":ring") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.ring_finger_mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.ring_finger_mode")

                if finger.partition(namespace)[2].find(":pinky") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.pinky_finger_mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.pinky_finger_mode")

                if finger.partition(namespace)[2].find(":thumb") == 0:
                    # switch modes
                    cmds.setAttr(namespace + ":" + self.name + "_settings.thumb_finger_mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.thumb_finger_mode")

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

                # create a duplicate chain
                topCtrl = controls[2]
                topGrp = cmds.listRelatives(topCtrl, parent=True)[0]
                newControls = cmds.duplicate(topGrp)
                cmds.parent(newControls[0], world=True)

                # match the fk controls to the corresponding joint
                controls.reverse()
                for control in controls:
                    joint = control.partition("fk_")[2].partition("_anim")[0]
                    joint = namespace + ":" + joint

                    dupeCtrl = control.partition(namespace + ":")[2]
                    constraint = cmds.parentConstraint(joint, dupeCtrl)[0]

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
                controls = self.getControls(False, "ikControls")
                controls = sorted(controls)
                controls.reverse()

                # HAND
                # create a duplicate hand anim
                matchCtrl = cmds.duplicate(controls[0], po=True)[0]

                # match the hand anim to the hand joint
                joint = controls[0].partition("ik_")[2].partition("_anim")[0]
                joint = namespace + ":" + joint

                pConstraint = cmds.pointConstraint(joint, matchCtrl)[0]
                oConstraint = cmds.orientConstraint(joint, matchCtrl)[0]

                if side == "Left":
                    cmds.setAttr(oConstraint + ".offsetX", 90)
                if side == "Right":
                    cmds.setAttr(oConstraint + ".offsetX", -90)

                # this will now give use good values
                translate = cmds.getAttr(matchCtrl + ".translate")[0]
                rotate = cmds.getAttr(matchCtrl + ".rotate")[0]

                cmds.setAttr(controls[0] + ".translate", translate[0], translate[1], translate[2],
                             type='double3')
                cmds.setAttr(controls[0] + ".rotate", rotate[0], rotate[1], rotate[2], type='double3')
                cmds.setKeyframe(controls[0])

                # delete dupes
                cmds.delete(matchCtrl)

                # ELBOW
                # create a duplicate elbow pv anim
                control = controls[1]
                topGrp = cmds.listRelatives(control, parent=True)[0]
                newControls = cmds.duplicate(topGrp)
                cmds.parent(newControls[0], world=True)

                # match to the pvMatch node
                dupeCtrl = control.partition(namespace + ":")[2]
                constraint = cmds.pointConstraint(control + "_fkMatch", dupeCtrl)[0]

                # this will now give use good values
                translate = cmds.getAttr(dupeCtrl + ".translate")[0]

                cmds.setAttr(control + ".translate", translate[0], translate[1], translate[2],
                             type='double3')
                cmds.setKeyframe(control)

                # delete dupes
                cmds.delete(newControls[0])

                # switch modes
                if not range:
                    cmds.setAttr(namespace + ":" + self.name + "_settings.mode", 1.0)
                    cmds.setKeyframe(namespace + ":" + self.name + "_settings.mode")

        if range:
            self.switchClavMode(mode, checkBox, True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def switchClavMode(self, mode, checkBox, range=False):
        """
        Switches the rig mode on the clavicle (FK/IK). If checkbox value is True, match then switch.

        :param mode: The mode to switch to (FK/IK)
        :param checkBox: The match checkbox to query its value
        :param range: Whether or not to match and switch over frame range.

        """

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")
        controls = self.getControls(False, "clavControls")

        ik_control = None
        fk_control = None
        for control in controls:
            no_namespace = control.partition(":")[2]
            if no_namespace.startswith("ik"):
                ik_control = control
            if no_namespace.startswith("fk"):
                fk_control = control

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

        if mode == "FK":

            if not match:
                cmds.setAttr(namespace + ":" + self.name + "_settings.clavMode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.clavMode")

            if match:
                dupe = cmds.duplicate(fk_control, rr=True, po=True)[0]
                const = cmds.orientConstraint(namespace + ":" + self.name + "_clav_ik_start", dupe)[0]
                cmds.delete(const)

                rotateXvalue = cmds.getAttr(dupe + ".rotateX")
                rotateYvalue = cmds.getAttr(dupe + ".rotateY")
                rotateZvalue = cmds.getAttr(dupe + ".rotateZ")

                cmds.setAttr(fk_control + ".rotateX", rotateXvalue)
                cmds.setAttr(fk_control + ".rotateY", rotateYvalue)
                cmds.setAttr(fk_control + ".rotateZ", rotateZvalue)

                cmds.setKeyframe(fk_control)

                cmds.delete(dupe)
                cmds.setAttr(namespace + ":" + self.name + "_settings.clavMode", 0.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.clavMode")

        if mode == "IK":

            if not match:
                cmds.setAttr(namespace + ":" + self.name + "_settings.clavMode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.clavMode")

            if match:
                dupe = cmds.duplicate(ik_control, rr=True)[0]
                const = cmds.pointConstraint(namespace + ":" + self.name + "_ik_clav_matcher", dupe)[0]
                cmds.delete(const)

                transXvalue = cmds.getAttr(dupe + ".translateX")
                transYvalue = cmds.getAttr(dupe + ".translateY")
                transZvalue = cmds.getAttr(dupe + ".translateZ")

                cmds.setAttr(ik_control + ".translateX", transXvalue)
                cmds.setAttr(ik_control + ".translateY", transYvalue)
                cmds.setAttr(ik_control + ".translateZ", transZvalue)

                cmds.setKeyframe(ik_control)

                cmds.delete(dupe)

                cmds.setAttr(namespace + ":" + self.name + "_settings.clavMode", 1.0)
                cmds.setKeyframe(namespace + ":" + self.name + "_settings.clavMode")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeSide(self):
        """
        Import the given joint mover file for the side requested (from network node). For the Arm, there are 2 joint
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
        movers = self.returnJointMovers

        for moverGrp in movers:
            for mover in moverGrp:
                cmds.lockNode(mover, lock=False)

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

        # create the connection geo between the two
        self.applyModuleChanges(self)

        self.aimMode_Setup(True)

        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _createControlNode(self, networkNode):

        # create a new network node to hold the control types
        if not cmds.objExists(networkNode + ".controls"):
            cmds.addAttr(networkNode, sn="controls", at="message")

        controlNode = cmds.createNode("network", name=networkNode + "_Controls")
        cmds.addAttr(controlNode, sn="parentModule", at="message")

        # connect new network node to original network node
        cmds.connectAttr(networkNode + ".controls", controlNode + ".parentModule")

        return controlNode

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _createRigGroups(self, networkNode, numRigs, armJoints):

        # create the arm group
        self.armGroup = cmds.group(empty=True, name=self.name + "_group")
        constraint = cmds.parentConstraint(armJoints[1][0], self.armGroup)[0]
        cmds.delete(constraint)

        # create the arm settings group
        self.armSettings = cmds.group(empty=True, name=self.name + "_settings")
        cmds.parent(self.armSettings, self.armGroup)
        for attr in (cmds.listAttr(self.armSettings, keyable=True)):
            cmds.setAttr(self.armSettings + "." + attr, lock=True, keyable=False)

        # add mode attribute to settings
        if numRigs > 1:
            cmds.addAttr(self.armSettings, ln="mode", min=0, max=numRigs - 1, dv=0, keyable=True)

        # create the ctrl group (what will get the constraint to the parent)
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")
        self.armCtrlGrp = cmds.group(empty=True, name=self.name + "_arm_ctrl_grp")

        if cmds.getAttr(networkNode + ".includeClavicle"):
            constraint = cmds.parentConstraint(armJoints[0], self.armCtrlGrp)[0]
        else:
            constraint = cmds.parentConstraint("driver_" + parentBone, self.armCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(self.armCtrlGrp, self.armGroup)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildFingers(self, fingers, textEdit, uiInst, builtRigs, networkNode):

        """
        Builds the FK/IK finger rigs and sets up hand roll.

        :param fingers: fingers to build rigs for.
        :param textEdit: textEdit widget to write progress to
        :param builtRigs: how many rigs have been built.
        :param networkNode: module network node
        :return:
        """
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # create groups
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        armJoints = self._getMainArmJoints()
        fkFingerCtrlsGrp = cmds.group(empty=True, name=self.name + "_fk_finger_ctrls")
        const = cmds.parentConstraint(armJoints[1][2], fkFingerCtrlsGrp)[0]
        cmds.delete(const)

        handDrivenMasterGrp = cmds.duplicate(fkFingerCtrlsGrp, po=True, name=self.name + "_hand_driven_master_grp")
        handDrivenGrp = cmds.duplicate(fkFingerCtrlsGrp, po=True, name=self.name + "_hand_driven_grp")

        cmds.parent(handDrivenMasterGrp, self.fingerGrp)
        cmds.parent(handDrivenGrp, handDrivenMasterGrp)
        cmds.parent(fkFingerCtrlsGrp, handDrivenGrp)

        # setup constraints/sdks on handDrivenGrp
        const = cmds.parentConstraint("driver_" + armJoints[1][2], handDrivenGrp)

        fkRigInfo = []

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # create metacarpal controls
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        metaCarpals = []
        phalanges = []
        for each in fingers:
            if each[0].find("metacarpal") != -1:
                if each[0].find("thumb") == -1:
                    metaCarpals.append(each[0])

            fingerData = []
            for finger in each:
                if finger.find("metacarpal") == -1:
                    if each[0].find("thumb") == -1:
                        fingerData.append(finger)

            for finger in each:
                if finger.find("thumb") != -1:
                    fingerData.append(finger)

            phalanges.append(fingerData)

        for metacarpal in metaCarpals:
            data = riggingUtils.createControlFromMover(metacarpal, networkNode, True, False)
            ctrl = cmds.rename(data[0], metacarpal + "_anim")
            grp = cmds.rename(data[1], metacarpal + "_anim_grp")
            cmds.parent(grp, handDrivenGrp)

            # color the control
            riggingUtils.colorControl(ctrl)
            fkRigInfo.append(ctrl)

            for attr in [".scaleX", ".scaleY", ".scaleZ", ".visibility"]:
                cmds.setAttr(ctrl + attr, lock=True, keyable=False)

        # first create a group for the IK handles to go into

        ikHandlesGrp = cmds.group(empty=True, name=self.name + "_fkOrient_ikHandles_grp")
        cmds.parent(ikHandlesGrp, handDrivenGrp)

        # setup constraints
        const = cmds.parentConstraint([handDrivenGrp[0], self.fingerGrp], ikHandlesGrp)[0]

        # add attr (globalStick)
        cmds.addAttr(self.armSettings, ln="globalSticky", dv=0, min=0, max=1, keyable=True)

        # set driven keys
        cmds.setAttr(self.armSettings + ".globalSticky", 0)
        cmds.setAttr(const + "." + handDrivenGrp[0] + "W0", 1)
        cmds.setAttr(const + "." + self.fingerGrp + "W1", 0)
        cmds.setDrivenKeyframe([const + "." + handDrivenGrp[0] + "W0", const + "." + self.fingerGrp + "W1"],
                               cd=self.armSettings + ".globalSticky", itt='linear', ott='linear')

        cmds.setAttr(self.armSettings + ".globalSticky", 1)
        cmds.setAttr(const + "." + handDrivenGrp[0] + "W0", 0)
        cmds.setAttr(const + "." + self.fingerGrp + "W1", 1)
        cmds.setDrivenKeyframe([const + "." + handDrivenGrp[0] + "W0", const + "." + self.fingerGrp + "W1"],
                               cd=self.armSettings + ".globalSticky", itt='linear', ott='linear')

        cmds.setAttr(self.armSettings + ".globalSticky", 0)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # create the FK orient joints
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        fkOrients = []

        for each in phalanges:
            if len(each) > 0:

                # find tip locator name
                nameData = self.returnPrefixSuffix
                splitString = each[0]
                if nameData[0] != None:
                    splitString = each[0].partition(nameData[0])[2]

                if nameData[1] != None:
                    splitString = splitString.partition(nameData[1])[0]

                splitString = splitString.partition("_")[0]
                tipLoc = self.name + "_" + splitString + "_tip"

                # create base and end joints
                baseJnt = cmds.createNode('joint', name="fk_orient_" + each[0] + "_jnt")
                const = cmds.parentConstraint(each[0], baseJnt)[0]
                cmds.delete(const)

                endJnt = cmds.createNode('joint', name="fk_orient_" + each[0] + "_end")
                const = cmds.parentConstraint(tipLoc, endJnt)[0]
                cmds.delete(const)

                cmds.parent(endJnt, baseJnt)
                cmds.makeIdentity(baseJnt, t=0, r=1, s=0, apply=True)
                cmds.setAttr(baseJnt + ".v", 0, lock=True)

                # create SC ik handles for each chain
                ikNodes = cmds.ikHandle(sol="ikSCsolver", name=baseJnt + "_ikHandle", sj=baseJnt, ee=endJnt)[0]
                cmds.parent(ikNodes, ikHandlesGrp)
                cmds.setAttr(ikNodes + ".v", 0)

                # parent orient joint to metacarpal control if it exists
                jntBaseName = self._getFingerBaseName(each[0]).partition("_")[0]
                metaCtrl = ""
                for each in metaCarpals:
                    if each.find(jntBaseName) != -1:
                        metaCtrl = each + "_anim"

                if cmds.objExists(metaCtrl):
                    cmds.parent(baseJnt, metaCtrl)
                    fkOrients.append(baseJnt)
                else:
                    fkOrients.append(baseJnt)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # create FK controls for the phalanges
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        fkInfo = []
        for each in phalanges:
            fingerData = []

            for finger in each:
                # create the FK control/anim grp/driven grp
                data = riggingUtils.createControlFromMover(finger, networkNode, True, False, control_type="fk_rig_control")
                ctrl = cmds.rename(data[0], finger + "_anim")

                # mirroring attrs
                for attr in ["invertX", "invertY", "invertZ"]:
                    if not cmds.objExists(ctrl + "." + attr):
                        cmds.addAttr(ctrl, ln=attr, at="bool")

                cmds.setAttr(ctrl + ".invertX", 1)
                cmds.setAttr(ctrl + ".invertY", 1)

                grp = cmds.rename(data[1], finger + "_anim_grp")
                drivenGrp = cmds.group(empty=True, name=finger + "_driven_grp")
                const = cmds.parentConstraint(grp, drivenGrp)[0]
                cmds.delete(const)

                fkInfo.append([ctrl, finger])
                fkRigInfo.append(ctrl)

                # setup hierarchy
                cmds.parent(drivenGrp, grp)
                cmds.parent(ctrl, drivenGrp)

                cmds.makeIdentity(drivenGrp, t=1, r=1, s=1, apply=True)
                fingerData.append(ctrl)

                # color control
                riggingUtils.colorControl(ctrl)

                # lock attrs on ctrl
                cmds.setAttr(ctrl + ".v", lock=True, keyable=False)
                # cmds.aliasAttr(ctrl + ".sz", rm=True)

            fingerData.reverse()

            for i in range(len(fingerData)):
                try:
                    cmds.parent(fingerData[i] + "_grp", fingerData[i + 1])
                except IndexError:
                    pass

            fingerData.reverse()

            # parent FK control to metacarpal control if it exists
            jntBaseName = self._getFingerBaseName(each[0]).partition("_")[0]
            metaCtrl = ""
            for each in metaCarpals:
                if each.find(jntBaseName) != -1:
                    metaCtrl = each + "_anim"

            jntName = fingerData[0].partition("_anim")[0]
            baseJnt = "fk_orient_" + jntName + "_jnt"

            # parent the control to the meta control or to the fk finger controls group
            if cmds.objExists(metaCtrl):
                if metaCtrl.find("thumb") == -1:
                    cmds.parent(fingerData[0] + "_grp", metaCtrl)
                else:
                    cmds.parent(fingerData[0] + "_grp", fkFingerCtrlsGrp)
                    cmds.parent(baseJnt, fkFingerCtrlsGrp)

            else:
                cmds.parent(fingerData[0] + "_grp", fkFingerCtrlsGrp)
                cmds.parent(baseJnt, fkFingerCtrlsGrp)

            # add sticky attribute
            if fingerData[0].find("thumb") == -1:
                cmds.addAttr(fingerData[0], ln="sticky", defaultValue=0, minValue=0, maxValue=1, keyable=True)

            # setup the constraint between the fk finger orient joint and the ctrlGrp

            if metaCtrl == '':
                masterObj = fkFingerCtrlsGrp
            else:
                masterObj = metaCtrl

            constraint = cmds.parentConstraint([masterObj, baseJnt], fingerData[0] + "_grp", mo=True)[0]

            # set driven keyframes on constraint
            if cmds.objExists(fingerData[0] + ".sticky"):
                cmds.setAttr(fingerData[0] + ".sticky", 1)
                cmds.setAttr(constraint + "." + masterObj + "W0", 0)
                cmds.setAttr(constraint + "." + baseJnt + "W1", 1)
                cmds.setDrivenKeyframe([constraint + "." + masterObj + "W0", constraint + "." + baseJnt + "W1"],
                                       cd=fingerData[0] + ".sticky", itt="linear", ott="linear")

                cmds.setAttr(fingerData[0] + ".sticky", 0)
                cmds.setAttr(constraint + "." + masterObj + "W0", 1)
                cmds.setAttr(constraint + "." + baseJnt + "W1", 0)
                cmds.setDrivenKeyframe([constraint + "." + masterObj + "W0", constraint + "." + baseJnt + "W1"],
                                       cd=fingerData[0] + ".sticky", itt="linear", ott="linear")

        # write FK data to network node
        if len(fkRigInfo) > 0:
            controlNode = cmds.listConnections(networkNode + ".controls")[0]

            if not cmds.objExists(controlNode + ".fkFingerControls"):
                cmds.addAttr(controlNode, sn="fkFingerControls", at="message")
            for node in fkRigInfo:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".fkFingerControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # setup hand roll
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create our 4 locators(pivots) and position
        pinkyPiv = cmds.spaceLocator(name=self.name + "_hand_pinky_pivot")[0]
        thumbPiv = cmds.spaceLocator(name=self.name + "_hand_thumb_pivot")[0]
        midPiv = cmds.spaceLocator(name=self.name + "_hand_mid_pivot")[0]
        tipPiv = cmds.spaceLocator(name=self.name + "_hand_tip_pivot")[0]

        for piv in [pinkyPiv, thumbPiv, midPiv, tipPiv]:
            cmds.setAttr(piv + ".v", 0)

        # posititon locators

        const = cmds.parentConstraint(self.name + "_pinky_pivot", pinkyPiv)[0]
        cmds.delete(const)
        const = cmds.parentConstraint(self.name + "_thumb_pivot", thumbPiv)[0]
        cmds.delete(const)
        const = cmds.parentConstraint(self.name + "_palm_pivot", midPiv)[0]
        cmds.delete(const)
        const = cmds.parentConstraint(self.name + "_middle_tip", tipPiv)[0]
        cmds.delete(const)

        # create the control groups for the pivots so our values are zeroed
        for each in [pinkyPiv, thumbPiv, midPiv, tipPiv]:
            group = cmds.group(empty=True, name=each + "_grp")
            constraint = cmds.parentConstraint(each, group)[0]
            cmds.delete(constraint)
            cmds.parent(each, group)

        # setup hierarchy
        cmds.parent(thumbPiv + "_grp", pinkyPiv)
        cmds.parent(tipPiv + "_grp", thumbPiv)
        cmds.parent(midPiv + "_grp", tipPiv)

        # parent the arm IK handles under the midPiv locator
        cmds.parent(self.name + "_rp_arm_ikHandle", midPiv)
        cmds.parent(pinkyPiv + "_grp", self.ikHandCtrl)

        # add attrs to the IK hand control (side, roll, tip pivot)
        cmds.addAttr(self.ikHandCtrl, longName="side", defaultValue=0, keyable=True)
        cmds.addAttr(self.ikHandCtrl, longName="mid_bend", defaultValue=0, keyable=True)
        cmds.addAttr(self.ikHandCtrl, longName="mid_swivel", defaultValue=0, keyable=True)
        cmds.addAttr(self.ikHandCtrl, longName="tip_pivot", defaultValue=0, keyable=True)
        cmds.addAttr(self.ikHandCtrl, longName="tip_swivel", defaultValue=0, keyable=True)

        # hook up attrs to pivot locators
        cmds.connectAttr(self.ikHandCtrl + ".mid_bend", midPiv + ".rz")
        cmds.connectAttr(self.ikHandCtrl + ".tip_pivot", tipPiv + ".rz")

        cmds.connectAttr(self.ikHandCtrl + ".mid_swivel", midPiv + ".ry")
        cmds.connectAttr(self.ikHandCtrl + ".tip_swivel", tipPiv + ".ry")

        # set driven keys for side to side attr

        cmds.setAttr(self.ikHandCtrl + ".side", 0)
        cmds.setAttr(pinkyPiv + ".rx", 0)
        cmds.setAttr(thumbPiv + ".rx", 0)
        cmds.setDrivenKeyframe([pinkyPiv + ".rx", thumbPiv + ".rx"], cd=self.ikHandCtrl + ".side", itt='linear',
                               ott='linear')

        cmds.setAttr(self.ikHandCtrl + ".side", 180)
        cmds.setAttr(pinkyPiv + ".rx", -180)
        cmds.setAttr(thumbPiv + ".rx", 0)
        cmds.setDrivenKeyframe([pinkyPiv + ".rx", thumbPiv + ".rx"], cd=self.ikHandCtrl + ".side", itt='linear',
                               ott='linear')

        cmds.setAttr(self.ikHandCtrl + ".side", -180)
        cmds.setAttr(pinkyPiv + ".rx", 0)
        cmds.setAttr(thumbPiv + ".rx", 180)
        cmds.setDrivenKeyframe([pinkyPiv + ".rx", thumbPiv + ".rx"], cd=self.ikHandCtrl + ".side", itt='linear',
                               ott='linear')

        cmds.setAttr(self.ikHandCtrl + ".side", 0)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # setup ik fingers (if applicable)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        scaleFactor = riggingUtils.getScaleFactor()
        ikInfo = []
        ikCtrlData = []

        for each in phalanges:
            if len(each) == 3:
                ikJnts = []
                pvGrps = []

                # create the IK finger joints
                for bone in each:
                    jnt = cmds.createNode('joint', name="ik_" + bone + "_jnt")
                    const = cmds.parentConstraint(bone, jnt)[0]
                    cmds.delete(const)
                    ikJnts.append(jnt)

                # parent ik joints
                ikJnts.reverse()
                for i in range(len(ikJnts)):
                    try:
                        cmds.parent(ikJnts[i], ikJnts[i + 1])
                    except IndexError:
                        pass

                # create the ik tip jnt
                jnt = cmds.createNode('joint', name=ikJnts[0] + "_tip")

                # find tip locator name
                nameData = self.returnPrefixSuffix
                splitString = each[0]
                if nameData[0] != None:
                    splitString = each[0].partition(nameData[0])[2]

                if nameData[1] != None:
                    splitString = splitString.partition(nameData[1])[0]

                jntType = splitString.partition("_")[0]
                tipLoc = self.name + "_" + jntType + "_tip"

                const = cmds.parentConstraint(tipLoc, jnt)[0]
                cmds.delete(const)

                cmds.parent(jnt, ikJnts[0])
                ikJnts.reverse()
                ikJnts.append(jnt)

                cmds.makeIdentity(ikJnts[0], t=0, r=1, s=0, apply=True)

                # parent the ik to the handDrivenGrp
                cmds.parent(ikJnts[0], handDrivenGrp)
                cmds.setAttr(ikJnts[0] + ".v", 0, lock=True)

                # create the IK
                ikNodes = \
                    cmds.ikHandle(sol="ikRPsolver", name=self.name + jntType + "_ikHandle", sj=ikJnts[0],
                                  ee=ikJnts[2])[
                        0]
                ikTipNodes = \
                    cmds.ikHandle(sol="ikSCsolver", name=self.name + jntType + "_tip_ikHandle", sj=ikJnts[2],
                                  ee=ikJnts[3])[
                        0]
                cmds.setAttr(ikNodes + ".v", 0)
                cmds.parent(ikTipNodes, ikNodes)

                # create the IK PV
                poleVector = cmds.spaceLocator(name=self.name + "_" + jntType + "_pv_anim")[0]
                constraint = cmds.parentConstraint(ikJnts[1], poleVector)[0]
                cmds.delete(constraint)
                riggingUtils.colorControl(poleVector)

                # create a pole vector group
                pvGrp = cmds.group(empty=True, name=poleVector + "_grp")
                constraint = cmds.parentConstraint(poleVector, pvGrp)[0]
                cmds.delete(constraint)
                pvGrps.append(pvGrp)

                # parent to the joint, and move out away from finger
                cmds.parent(poleVector, ikJnts[1])

                if cmds.getAttr(networkNode + ".side") == "Left":
                    cmds.setAttr(poleVector + ".ty", -40 * scaleFactor)

                if cmds.getAttr(networkNode + ".side") == "Right":
                    cmds.setAttr(poleVector + ".ty", 40 * scaleFactor)

                cmds.makeIdentity(poleVector, t=1, r=1, s=1, apply=True)
                cmds.parent(poleVector, pvGrp, absolute=True)
                cmds.makeIdentity(poleVector, t=1, r=1, s=1, apply=True)

                # create the IK finger controls
                data = riggingUtils.createControlFromMover(each[2], networkNode, True, True, control_type="ik_rig_control")
                ikFingerCtrl = cmds.rename(data[0], each[2] + "_ik_anim")

                # mirroring attrs
                for attr in ["invertX", "invertY", "invertZ"]:
                    if not cmds.objExists(ikFingerCtrl + "." + attr):
                        cmds.addAttr(ikFingerCtrl, ln=attr, at="bool")

                cmds.setAttr(ikFingerCtrl + ".invertX", 1)
                cmds.setAttr(ikFingerCtrl + ".invertY", 1)

                ikFingerGrp = cmds.rename(data[1], each[2] + "_ik_anim_grp")
                spaceSwitcher = cmds.rename(data[2], each[2] + "_ik_anim_space_switcher")
                spaceFollow = cmds.rename(data[3], each[2] + "_ik_anim_space_switcher_follow")
                riggingUtils.colorControl(ikFingerCtrl)
                ikCtrlData.append(ikFingerCtrl)
                ikCtrlData.append(poleVector)

                # parent ik to ctrl
                cmds.parent(ikNodes, ikFingerCtrl)

                # create the PV constraint
                cmds.poleVectorConstraint(poleVector, ikNodes)

                # add attr to show pole vector control
                cmds.addAttr(ikFingerCtrl, longName="poleVectorVis", defaultValue=0, minValue=0, maxValue=1,
                             keyable=True)
                cmds.connectAttr(ikFingerCtrl + ".poleVectorVis", poleVector + ".v")

                for group in pvGrps:
                    cmds.parent(group, handDrivenGrp)

                # create the global IK control
                if not cmds.objExists(armJoints[1][2] + "_global_ik_anim"):
                    globalIkAnim = riggingUtils.createControl("square", 30, armJoints[1][2] + "_global_ik_anim",
                                                              True)

                    const = cmds.pointConstraint(midPiv, globalIkAnim)[0]
                    cmds.delete(const)

                    globalIkGrp = cmds.group(empty=True, name=globalIkAnim + "_grp")
                    const = cmds.pointConstraint(midPiv, globalIkGrp)[0]
                    cmds.delete(const)
                    const = cmds.orientConstraint(self.ikHandCtrl, globalIkGrp)[0]
                    cmds.delete(const)

                    cmds.parent(globalIkAnim, globalIkGrp)
                    cmds.makeIdentity(globalIkAnim, t=1, r=1, s=1, apply=True)

                    # translate down in z
                    cmds.setAttr(globalIkAnim + ".tz", -5)
                    cmds.makeIdentity(globalIkAnim, t=1, r=1, s=1, apply=True)

                    if self.up == "y":
                        cmds.setAttr(globalIkAnim + ".rx", 90)
                        cmds.makeIdentity(globalIkAnim, t=0, r=1, s=0, apply=True)

                    # reposition the grp to the control
                    cmds.parent(globalIkAnim, world=True)
                    constraint = cmds.pointConstraint(globalIkAnim, globalIkGrp)[0]
                    cmds.delete(constraint)

                    cmds.parent(globalIkAnim, globalIkGrp)
                    cmds.makeIdentity(globalIkAnim, t=1, r=1, s=1, apply=True)

                    riggingUtils.colorControl(globalIkAnim)

                    # create a space switcher grp
                    globalIKSpaceFollow = \
                        cmds.duplicate(globalIkGrp, po=True, name=globalIkAnim + "_space_switcher_follow")[0]
                    globalIKSpaceSwitch = \
                    cmds.duplicate(globalIkGrp, po=True, name=globalIkAnim + "_space_switcher")[0]

                    globalMasterGrp = cmds.group(empty=True, name=self.name + "_global_finger_ik_grp")
                    const = cmds.parentConstraint(armJoints[1][2], globalMasterGrp)[0]
                    cmds.delete(const)

                    cmds.parent(globalIKSpaceSwitch, globalIKSpaceFollow)
                    cmds.parent(globalIkGrp, globalIKSpaceSwitch)
                    cmds.parent(globalIKSpaceFollow, globalMasterGrp)
                    cmds.parent(globalMasterGrp, self.fingerGrp)
                    cmds.parentConstraint("driver_" + armJoints[1][2], globalMasterGrp, mo=True)

                    # add global ctrl visibility attr
                    cmds.addAttr(self.armSettings, ln="globalIkVis", dv=0, min=0, max=1, keyable=True)
                    shape = cmds.listRelatives(globalIkAnim, shapes=True)[0]
                    cmds.connectAttr(self.armSettings + ".globalIkVis", shape + ".v")

                    ikCtrlData.append(globalIkAnim)

                # parent ik control grps to this global control
                cmds.parent(spaceFollow, globalIkAnim)

                # collect data per finger
                ikInfo.append([globalIKSpaceFollow, globalIkAnim, ikJnts, jntType, spaceFollow, pvGrp])

        # write IK data to network node
        if len(ikCtrlData) > 0:
            controlNode = cmds.listConnections(networkNode + ".controls")[0]

            if not cmds.objExists(controlNode + ".ikFingerControls"):
                cmds.addAttr(controlNode, sn="ikFingerControls", at="message")
            for node in ikCtrlData:

                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".ikFingerControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "IK", type="string")

                if node.find("_pv_anim") == -1:
                    cmds.addAttr(node, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
                    cmds.setAttr(node + ".hasSpaceSwitching", lock=True)
                    cmds.addAttr(node, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
                    cmds.setAttr(node + ".canUseRotationSpace", lock=True)
                    cmds.addAttr(node, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
                    cmds.setAttr(node + ".canUseTranslationSpace", lock=True)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # setup finger modes/driven keys
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        for each in ikInfo:
            fkCtrl = each[2][0].partition("ik_")[2].rpartition("_jnt")[0] + "_anim_grp"
            cmds.addAttr(self.armSettings, ln=each[3] + "_finger_mode", dv=0, min=0, max=1, keyable=True)

            cmds.setAttr(self.armSettings + "." + each[3] + "_finger_mode", 0)
            cmds.setAttr(each[4] + ".v", 0)
            cmds.setAttr(each[5] + ".v", 0)
            cmds.setAttr(fkCtrl + ".v", 1)
            cmds.setDrivenKeyframe([each[4] + ".v", each[5] + ".v", fkCtrl + ".v"],
                                   cd=self.armSettings + "." + each[3] + "_finger_mode", itt='linear', ott='linear')

            cmds.setAttr(self.armSettings + "." + each[3] + "_finger_mode", 1)
            cmds.setAttr(each[4] + ".v", 1)
            cmds.setAttr(each[5] + ".v", 1)
            cmds.setAttr(fkCtrl + ".v", 0)
            cmds.setDrivenKeyframe([each[4] + ".v", each[5] + ".v", fkCtrl + ".v"],
                                   cd=self.armSettings + "." + each[3] + "_finger_mode", itt='linear', ott='linear')

            cmds.setAttr(self.armSettings + "." + each[3] + "_finger_mode", 0)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # parent IK finger joints under metacarpals (if they exist)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        for each in ikInfo:
            metaCtrl = ""
            jntBaseName = self._getFingerBaseName(each[2][0]).partition("_")[0]
            for carpal in metaCarpals:
                if carpal.find(jntBaseName) != -1:
                    metaCtrl = carpal + "_anim"

            if cmds.objExists(metaCtrl):
                cmds.parent(each[2][0], metaCtrl)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # Hook up driver joints
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        for each in fkInfo:
            fkCtrl = each[0]
            jnt = each[1]
            ikJnt = "ik_" + jnt + "_jnt"
            driverJnt = "driver_" + jnt

            # find joint base name
            nameData = self.returnPrefixSuffix
            splitString = jnt
            if nameData[0] != None:
                splitString = jnt.partition(nameData[0])[2]

            if nameData[1] != None:
                splitString = splitString.partition(nameData[1])[0]

            jntBaseName = splitString.partition("_")[0]

            if cmds.objExists(ikJnt):
                pConst = cmds.parentConstraint([fkCtrl, ikJnt], driverJnt, mo=True)[0]

                # set driven keys
                cmds.setAttr(self.armSettings + "." + jntBaseName + "_finger_mode", 0)
                cmds.setAttr(pConst + "." + fkCtrl + "W0", 1)
                cmds.setAttr(pConst + "." + ikJnt + "W1", 0)
                cmds.setDrivenKeyframe([pConst + "." + fkCtrl + "W0", pConst + "." + ikJnt + "W1"],
                                       cd=self.armSettings + "." + jntBaseName + "_finger_mode", itt='linear',
                                       ott='linear')

                cmds.setAttr(self.armSettings + "." + jntBaseName + "_finger_mode", 1)
                cmds.setAttr(pConst + "." + fkCtrl + "W0", 0)
                cmds.setAttr(pConst + "." + ikJnt + "W1", 1)
                cmds.setDrivenKeyframe([pConst + "." + fkCtrl + "W0", pConst + "." + ikJnt + "W1"],
                                       cd=self.armSettings + "." + jntBaseName + "_finger_mode", itt='linear',
                                       ott='linear')

                cmds.setAttr(self.armSettings + "." + jntBaseName + "_finger_mode", 0)

                # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale
                # into input 2, and plugs that into driver joint
                slot = 0
                for each in [fkCtrl, ikJnt]:
                    if cmds.objExists("master_anim"):
                        globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True,
                                                           name=jnt + "_globalScale")
                        cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
                        cmds.connectAttr(each + ".scale", globalScaleMult + ".input2")
                        riggingUtils.createConstraint(globalScaleMult, "driver_" + jnt, "scale", False, 2, slot,
                                                      "output")
                    else:
                        riggingUtils.createConstraint(each, "driver_" + jnt, "scale", False, 2, slot)

                    slot = slot + 1

            else:
                pConst = cmds.parentConstraint(fkCtrl, driverJnt)[0]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildIkArm(self, textEdit, uiInst, builtRigs, networkNode):

        # update progress
        if textEdit is not None:
            textEdit.append("        Starting IK Arm Rig Build..")

        # build the rig
        slot = len(builtRigs)

        # find the joints in the arm module that need rigging
        joints = self._getMainArmJoints()
        ikControls = []

        # =======================================================================
        # # create the ik arm joint chain
        # =======================================================================

        ikArmJoints = []
        for joint in joints[1]:
            jnt = cmds.createNode("joint", name="ik_" + joint + "_jnt")
            const = cmds.parentConstraint(joint, jnt)[0]
            cmds.delete(const)
            ikArmJoints.append(jnt)

        # create the wrist end joint
        jnt = cmds.createNode("joint", name="ik_" + ikArmJoints[2] + "_end_jnt")
        const = cmds.parentConstraint(ikArmJoints[2], jnt)[0]
        cmds.delete(const)
        ikArmJoints.append(jnt)

        # create hierarchy
        ikArmJoints.reverse()
        for i in range(len(ikArmJoints)):
            try:
                cmds.parent(ikArmJoints[i], ikArmJoints[i + 1])
            except IndexError:
                pass

        ikArmJoints.reverse()

        cmds.setAttr(ikArmJoints[0] + ".v", 0, lock=True)

        # move hand end joint out a bit. If tx is negative, add -2, if positive, add 2
        cmds.makeIdentity(ikArmJoints[0], t=0, r=1, s=0, apply=True)

        if cmds.getAttr(ikArmJoints[2] + ".tx") > 0:
            cmds.setAttr(ikArmJoints[3] + ".tx", 10)
        else:
            cmds.setAttr(ikArmJoints[3] + ".tx", -10)

        # =======================================================================
        # # connect controls up to blender nodes to drive driver joints
        # =======================================================================
        for joint in joints[1]:
            sourceBone = "ik_" + joint + "_jnt"

            cmds.pointConstraint(sourceBone, "driver_" + joint, mo=True)
            cmds.orientConstraint(sourceBone, "driver_" + joint)

            # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
            # input 2,and plugs that into driver joint
            if cmds.objExists("master_anim"):
                globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True,
                                                   name=joint + "_globalScale")
                cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
                cmds.connectAttr(sourceBone + ".scale", globalScaleMult + ".input2")
                riggingUtils.createConstraint(globalScaleMult, "driver_" + joint, "scale", False, 2, slot,
                                              "output")
            else:
                riggingUtils.createConstraint(sourceBone, "driver_" + joint, "scale", False, 2, slot)

        # =======================================================================
        # # create fk matching joints
        # =======================================================================
        fkMatchUpArm = cmds.duplicate(ikArmJoints[0], po=True, name="ik_" + joints[1][0] + "_fk_matcher")[0]
        fkMatchLowArm = cmds.duplicate(ikArmJoints[1], po=True, name="ik_" + joints[1][1] + "_fk_matcher")[
            0]
        fkMatchWrist = cmds.duplicate(ikArmJoints[2], po=True, name="ik_" + joints[1][2] + "_fk_matcher")[0]

        cmds.parent(fkMatchWrist, fkMatchLowArm)
        cmds.parent(fkMatchLowArm, fkMatchUpArm)

        # constrain fk match joints
        cmds.parentConstraint(ikArmJoints[0], fkMatchUpArm, mo=True)
        cmds.parentConstraint(ikArmJoints[1], fkMatchLowArm, mo=True)
        cmds.parentConstraint(ikArmJoints[2], fkMatchWrist, mo=True)

        # =======================================================================
        # # rotate order and preferred angle
        # =======================================================================
        # set rotate order on ikUpArm
        cmds.setAttr(ikArmJoints[0] + ".rotateOrder", 3)

        # set preferred angle on arm
        cmds.setAttr(ikArmJoints[1] + ".preferredAngleZ", -90)

        # =======================================================================
        # # create the ik control
        # =======================================================================
        handControlInfo = riggingUtils.createControlFromMover(joints[1][2], networkNode, True, True,
                                                              control_type="ik_rig_control")

        cmds.parent(handControlInfo[0], world=True)
        constraint = cmds.orientConstraint(self.name + "_ik_hand_ctrl_orient", handControlInfo[3])[0]
        cmds.delete(constraint)
        cmds.makeIdentity(handControlInfo[2], t=1, r=1, s=1, apply=True)
        cmds.parent(handControlInfo[0], handControlInfo[1])
        cmds.makeIdentity(handControlInfo[0], t=1, r=1, s=1, apply=True)

        # rename the control info
        self.ikHandCtrl = cmds.rename(handControlInfo[0], "ik_" + joints[1][2] + "_anim")
        cmds.rename(handControlInfo[1], self.ikHandCtrl + "_grp")
        cmds.rename(handControlInfo[2], self.ikHandCtrl + "_space_switcher")
        spaceSwitcherFollow = cmds.rename(handControlInfo[3], self.ikHandCtrl + "_space_switcher_follow")

        fkMatchGrp = cmds.group(empty=True, name=self.ikHandCtrl + "_fkMatch_grp")
        constraint = cmds.parentConstraint(fkMatchWrist, fkMatchGrp)[0]
        cmds.delete(constraint)

        cmds.parent(fkMatchGrp, self.ikHandCtrl)

        fkMatch = cmds.group(empty=True, name=self.ikHandCtrl + "_fkMatch")
        constraint = cmds.parentConstraint(fkMatchWrist, fkMatch)[0]
        cmds.delete(constraint)
        cmds.parent(fkMatch, fkMatchGrp)

        # create RP IK on arm and SC ik from wrist to wrist end
        rpIkHandle = \
            cmds.ikHandle(name=self.name + "_rp_arm_ikHandle", solver="ikRPsolver", sj=ikArmJoints[0],
                          ee=ikArmJoints[2])[0]
        scIkHandle = \
            cmds.ikHandle(name=self.name + "_sc_hand_ikHandle", solver="ikSCsolver", sj=ikArmJoints[2],
                          ee=ikArmJoints[3])[
                0]

        cmds.parent(scIkHandle, rpIkHandle)
        cmds.setAttr(rpIkHandle + ".v", 0)
        cmds.setAttr(scIkHandle + ".v", 0)

        cmds.setAttr(rpIkHandle + ".stickiness", 1)
        cmds.setAttr(rpIkHandle + ".snapEnable", 1)

        cmds.setAttr(scIkHandle + ".stickiness", 1)
        cmds.setAttr(scIkHandle + ".snapEnable", 1)

        # parent IK to ik control
        cmds.parent(rpIkHandle, self.ikHandCtrl)

        # =======================================================================
        # # create the ik pole vector
        # =======================================================================
        ikPvCtrlData = riggingUtils.createControlFromMover(joints[1][1], networkNode, True, False,
                                                           control_type="ik_rig_control")
        ikPvCtrl = cmds.rename(ikPvCtrlData[0], self.name + "_ik_elbow_anim")
        cmds.parent(ikPvCtrl, world=True)
        cmds.delete(ikPvCtrlData[1])
        cmds.xform(ikPvCtrl, cp=True)

        ikPvCtrlGrp = cmds.group(empty=True, name=self.name + "_ik_elbow_anim_grp")
        cmds.delete(cmds.pointConstraint(ikPvCtrl, ikPvCtrlGrp)[0])
        ikPvSpaceSwitch = cmds.duplicate(ikPvCtrlGrp, po=True, name=self.name + "_ik_elbow_anim_space_switcher")
        ikPvSpaceSwitchFollow = cmds.duplicate(ikPvCtrlGrp, po=True,
                                               name=self.name + "_ik_elbow_anim_space_switcher_follow")

        cmds.parent(ikPvCtrl, ikPvCtrlGrp)
        cmds.makeIdentity(ikPvCtrl, t=1, r=1, s=1, apply=True)
        cmds.parent(ikPvCtrlGrp, ikPvSpaceSwitch)
        cmds.makeIdentity(ikPvCtrlGrp, t=1, r=1, s=1, apply=True)
        cmds.parent(ikPvSpaceSwitch, ikPvSpaceSwitchFollow)
        cmds.makeIdentity(ikPvSpaceSwitch, t=1, r=1, s=1, apply=True)

        # setup pole vector constraint
        cmds.poleVectorConstraint(ikPvCtrl, rpIkHandle)

        # create the match group
        pvMatchGrp = cmds.group(empty=True, name=ikPvCtrl + "_fkMatchGrp")
        constraint = cmds.parentConstraint(ikPvCtrl, pvMatchGrp)[0]
        cmds.delete(constraint)

        fk_controls = self.getControls(False, "fkControls")
        fk_controls = sorted(fk_controls)
        cmds.parent(pvMatchGrp, fk_controls[1])

        pvMatch = cmds.group(empty=True, name=ikPvCtrl + "_fkMatch")
        constraint = cmds.parentConstraint(ikPvCtrl, pvMatch)[0]
        cmds.delete(constraint)

        cmds.parent(pvMatch, pvMatchGrp)

        # =======================================================================
        # # setup squash and stretch
        # =======================================================================
        # add attrs to the hand ctrl
        cmds.addAttr(self.ikHandCtrl, longName=("stretch"), at='double', min=0, max=1, dv=0, keyable=True)
        cmds.addAttr(self.ikHandCtrl, longName=("elbowLock"), at='double', min=0, max=1, dv=0, keyable=True)
        cmds.addAttr(self.ikHandCtrl, longName=("slide"), at='double', min=-1, max=1, dv=0, keyable=True)

        # get world positions of arm and ik
        baseGrp = cmds.group(empty=True, name=self.name + "_ik_arm_base_grp")
        endGrp = cmds.group(empty=True, name=self.name + "_ik_arm_end_grp")
        cmds.pointConstraint(ikArmJoints[0], baseGrp)
        cmds.pointConstraint(self.ikHandCtrl, endGrp)

        # load the stretchy ik plugin
        try:
            cmds.loadPlugin("ARTv2_Stretchy_IK")

            # create the node and hook up matrices
            ikNode = cmds.createNode("ARTv2_Stretchy_IK", name=self.name + "_stretchy_ik")
            cmds.connectAttr(baseGrp + ".worldMatrix[0]", ikNode + ".startMatrix")
            cmds.connectAttr(self.ikHandCtrl + ".worldMatrix[0]", ikNode + ".endMatrix")
            cmds.connectAttr(ikPvCtrl + ".worldMatrix[0]", ikNode + ".poleVectorMatrix")

            # set init lengths
            cmds.setAttr(ikNode + ".upInitLength", (cmds.getAttr(ikArmJoints[1] + ".tx")))
            cmds.setAttr(ikNode + ".downInitLength", (cmds.getAttr(ikArmJoints[2] + ".tx")))

            # connect attrs from hand control
            cmds.connectAttr(self.ikHandCtrl + ".stretch", ikNode + ".stretch")
            cmds.connectAttr(self.ikHandCtrl + ".slide", ikNode + ".slide")
            cmds.connectAttr(self.ikHandCtrl + ".elbowLock", ikNode + ".poleVectorLock")

            # hook up outputs into translate X of ikArm joints
            cmds.connectAttr(ikNode + ".upScale", ikArmJoints[1] + ".tx")
            cmds.connectAttr(ikNode + ".downScale", ikArmJoints[2] + ".tx")

        except Exception, e:
            cmds.warning("ARTv2_Stretchy_IK: " + str(e))

        # =======================================================================
        # # color controls and lock attrs
        # =======================================================================
        for control in [self.ikHandCtrl, ikPvCtrl]:
            riggingUtils.colorControl(control)

        for attr in [".scaleX", ".scaleY", ".scaleZ", ".visibility"]:
            cmds.setAttr(self.ikHandCtrl + attr, lock=True, keyable=False)

        for attr in [".scaleX", ".scaleY", ".scaleZ", ".rotateX", ".rotateY", ".rotateZ", ".visibility"]:
            cmds.setAttr(ikPvCtrl + attr, lock=True, keyable=False)

        # =======================================================================
        # # clean up IK nodes
        # =======================================================================
        self.ikCtrlGrp = cmds.group(empty=True, name=self.name + "_arm_ik_ctrls_grp")
        cmds.parent(self.ikCtrlGrp, self.armGroup)

        cmds.parent(ikPvSpaceSwitchFollow, self.ikCtrlGrp)
        cmds.parent(spaceSwitcherFollow, self.ikCtrlGrp)
        cmds.parent(fkMatchUpArm, self.ikCtrlGrp)

        cmds.parent(baseGrp, self.ikCtrlGrp)
        cmds.parent(endGrp, self.ikCtrlGrp)

        # add created control info to module
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        if not cmds.objExists(controlNode + ".ikControls"):
            cmds.addAttr(controlNode, sn="ikControls", at="message")

        # add proxy attrs for mode
        if cmds.objExists(self.armSettings + ".mode"):
            for node in [self.ikHandCtrl, ikPvCtrl]:
                cmds.addAttr(node, ln="mode", proxy=self.armSettings + ".mode", at="double", keyable=True)

        for node in [self.ikHandCtrl, ikPvCtrl]:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".ikControls", node + ".controlClass")

            cmds.addAttr(node, ln="controlType", dt="string")
            cmds.setAttr(node + ".controlType", "IK", type="string")

            # mirroring attrs
            for attr in ["invertX", "invertY", "invertZ"]:
                if not cmds.objExists(node + "." + attr):
                    cmds.addAttr(node, ln=attr, at="bool")

            cmds.addAttr(node, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".hasSpaceSwitching", lock=True)
            cmds.addAttr(node, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".canUseRotationSpace", lock=True)
            cmds.addAttr(node, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".canUseTranslationSpace", lock=True)

        cmds.setAttr(self.ikHandCtrl + ".invertX", 1)
        # update progress
        if textEdit is not None:
            textEdit.setTextColor(QtGui.QColor(0, 255, 18))
            textEdit.append("        SUCCESS: IK Build Complete!")
            textEdit.setTextColor(QtGui.QColor(255, 255, 255))

        return ikArmJoints

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildFkArm(self, textEdit, uiInst, builtRigs, networkNode):

        # update progress
        if textEdit is not None:
            textEdit.append("        Starting FK Arm Rig Build..")

        # build the rig
        slot = len(builtRigs)

        # find the joints in the arm module that need rigging
        joints = self._getMainArmJoints()
        fkControls = []
        self.topNode = None

        for joint in joints[1]:
            if joint.find("upperarm") != -1:
                data = riggingUtils.createControlFromMover(joint, networkNode, True, True, control_type="fk_rig_control")

                fkControl = cmds.rename(data[0], "fk_" + joint + "_anim")
                animGrp = cmds.rename(data[1], "fk_" + joint + "_anim_grp")
                spaceSwitcher = cmds.rename(data[2], "fk_" + joint + "_anim_space_switcher")
                spaceSwitchFollow = cmds.rename(data[3], "fk_" + joint + "_anim_space_switcher_follow")
                self.topNode = spaceSwitchFollow

                fkControls.append([spaceSwitchFollow, fkControl, joint])
                # color the control
                riggingUtils.colorControl(fkControl)

            else:
                data = riggingUtils.createControlFromMover(joint, networkNode, True, False, control_type="fk_rig_control")

                fkControl = cmds.rename(data[0], "fk_" + joint + "_anim")
                animGrp = cmds.rename(data[1], "fk_" + joint + "_anim_grp")

                fkControls.append([animGrp, fkControl, joint])

                # color the control
                riggingUtils.colorControl(fkControl)

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

            cmds.pointConstraint(control, "driver_" + joint, mo=True)
            cmds.orientConstraint(control, "driver_" + joint)

            # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
            # input 2,and plugs that into driver joint
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
        # parent top group into arm group
        cmds.parent(self.topNode, self.armCtrlGrp)

        # lock attrs
        for each in fkControls:
            control = each[1]
            for attr in [".scaleX", ".scaleY", ".scaleZ", ".visibility"]:
                cmds.setAttr(control + attr, lock=True, keyable=False)

        fkRigData = []
        for each in fkControls:
            fkRigData.append(each[1])

        # add created control info to module
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        if not cmds.objExists(controlNode + ".fkControls"):
            cmds.addAttr(controlNode, sn="fkControls", at="message")

        # add proxy attributes for mode
        if cmds.objExists(self.armSettings + ".mode"):
            for node in fkRigData:
                cmds.addAttr(node, ln="mode", proxy=self.armSettings + ".mode", at="double", keyable=True)

        # add metadata
        for node in fkRigData:
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

            if node.find("upperarm") != -1:
                cmds.addAttr(node, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
                cmds.setAttr(node + ".hasSpaceSwitching", lock=True)
                cmds.addAttr(node, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
                cmds.setAttr(node + ".canUseRotationSpace", lock=True)
                cmds.addAttr(node, ln="canUseTranslationSpace", at="bool", dv=0, keyable=False)
                cmds.setAttr(node + ".canUseTranslationSpace", lock=True)

        # update progress
        if textEdit is not None:
            textEdit.setTextColor(QtGui.QColor(0, 255, 18))
            textEdit.append("        SUCCESS: FK Build Complete!")
            textEdit.setTextColor(QtGui.QColor(255, 255, 255))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildClavicleRig(self, textEdit, uiInst, builtRigs, networkNode):

        # add clavicle mode to rig settings
        cmds.addAttr(self.armSettings, ln="clavMode", min=0, max=1, dv=0, keyable=True)

        # Rig Joint
        joints = self._getMainArmJoints()
        clavJoint = joints[0]
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")

        rigJntGrp = cmds.group(empty=True, name=self.name + "_clav_rigJnt_grp")
        cmds.delete(cmds.parentConstraint(clavJoint, rigJntGrp)[0])

        rigJnt = cmds.createNode("joint", name=self.name + "_clav_rigJnt")
        const = cmds.parentConstraint(clavJoint, rigJnt)[0]
        cmds.delete(const)
        cmds.parent(rigJnt, rigJntGrp)
        cmds.makeIdentity(rigJnt, t=0, r=1, s=0, apply=True)

        cmds.setAttr(rigJnt + ".v", 0, lock=True)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       FK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create rig control
        data = riggingUtils.createControlFromMover(clavJoint, networkNode, True, False, control_type="fk_rig_control")

        fkControl = cmds.rename(data[0], "fk_" + clavJoint + "_anim")
        animGrp = cmds.rename(data[1], "fk_" + clavJoint + "_anim_grp")
        riggingUtils.colorControl(fkControl)

        for attr in [".translateX", ".translateY", ".translateZ", ".scaleX", ".scaleY", ".scaleZ",
                     ".visibility"]:
            cmds.setAttr(fkControl + attr, lock=True, keyable=False)

        # create clav rig grp
        self.clavCtrlGrp = cmds.group(empty=True, name=self.name + "_clav_ctrl_grp")
        constraint = cmds.parentConstraint(parentBone, self.clavCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(self.clavCtrlGrp, self.armGroup)

        # parent fk clav to clav grp
        cmds.parent(animGrp, self.clavCtrlGrp)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       IK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create rig control
        ik_data = riggingUtils.createControlFromMover(clavJoint, networkNode, False, False, control_type="ik_rig_control")
        ikControl = cmds.rename(ik_data[0], "ik_" + clavJoint + "_anim")
        ikCtrlGrp = cmds.rename(ik_data[1], "ik_" + clavJoint + "_anim_grp")

        cmds.makeIdentity(ikControl, t=1, r=1, s=1, apply=True)

        upArmPiv = cmds.xform(joints[1][0], q=True, ws=True, rp=True)
        cmds.xform(ikControl, ws=True, piv=upArmPiv)
        cmds.xform(ikCtrlGrp, ws=True, piv=upArmPiv)

        riggingUtils.colorControl(ikControl)

        for attr in [".rotateX", ".rotateY", ".rotateZ", ".scaleX", ".scaleY", ".scaleZ", ".visibility"]:
            cmds.setAttr(ikControl + attr, lock=True, keyable=False)

        # create the ik joint chain
        startJnt = cmds.createNode("joint", name=self.name + "_clav_ik_start")
        endJnt = cmds.createNode("joint", name=self.name + "_clav_ik_end")
        pointJnt = cmds.createNode("joint", name=self.name + "_clav_follow")

        const = cmds.parentConstraint(clavJoint, startJnt)[0]
        cmds.delete(const)

        const = cmds.parentConstraint(joints[1][0], endJnt)[0]
        cmds.delete(const)

        const = cmds.parentConstraint(clavJoint, pointJnt)[0]
        cmds.delete(const)

        cmds.parent(endJnt, startJnt)
        cmds.parent(pointJnt, rigJntGrp)
        cmds.parent(startJnt, self.clavCtrlGrp)

        # hide joints
        for jnt in [startJnt, endJnt, pointJnt]:
            cmds.makeIdentity(jnt, t=0, r=1, s=0, apply=True)
            cmds.setAttr(jnt + ".v", 0, lock=True)

        # make FK arm follow IK clavicle correctly
        point_joint_master_grp = cmds.group(empty=True, name=self.name + "_clav_follow_grp")
        cmds.delete(cmds.parentConstraint(pointJnt, point_joint_master_grp)[0])
        cmds.parent(point_joint_master_grp, rigJntGrp)
        cmds.parentConstraint(endJnt, point_joint_master_grp, mo=True)

        point_joint_orient_grp = cmds.group(empty=True, name=self.name + "_clav_follow_orient_grp")
        cmds.delete(cmds.parentConstraint(pointJnt, point_joint_orient_grp)[0])
        cmds.parent(point_joint_orient_grp, point_joint_master_grp)

        point_joint_orient_space = cmds.group(empty=True, name=self.name + "_clav_follow_orient_space")
        cmds.delete(cmds.parentConstraint(pointJnt, point_joint_orient_space)[0])
        cmds.orientConstraint(point_joint_orient_space, point_joint_orient_grp)
        cmds.parent(point_joint_orient_space, self.clavCtrlGrp)

        cmds.parent(pointJnt, point_joint_orient_grp)

        # create the ikHandle
        ikNodes = cmds.ikHandle(sj=startJnt, ee=endJnt, sol="ikSCsolver", name=self.name + "_clav_ikHandle")[0]
        cmds.parent(ikNodes, ikControl)
        cmds.setAttr(ikNodes + ".v", 0, lock=True)
        cmds.setAttr(ikNodes + ".stickiness", 1)
        cmds.setAttr(ikNodes + ".snapEnable", 1)

        # =======================================================================
        # #lastly, connect controls up to blender nodes to drive driver joints
        # =======================================================================

        rigJntPointConst = cmds.pointConstraint([fkControl, startJnt], rigJnt, mo=True)[0]
        rigJointOrientConst = cmds.orientConstraint([fkControl, startJnt], rigJnt)[0]

        attrData = []
        for connection in [rigJntPointConst, rigJointOrientConst]:
            driveAttrs = []
            targets = cmds.getAttr(connection + ".target", mi=True)
            if len(targets) > 1:
                for each in targets:
                    driveAttrs.append(
                        cmds.listConnections(connection + ".target[" + str(each) + "].targetWeight", p=True))

                attrData.append(driveAttrs)
        cmds.setAttr(rigJointOrientConst + ".interpType", 2)

        # setup set driven keys on our moder attr and those target attributes
        for i in range(2):
            cmds.setAttr(self.armSettings + ".clavMode", i)

            # go through attr data and zero out anything but the first element in the list
            for data in attrData:
                for each in data:
                    cmds.setAttr(each[0], 0)

                cmds.setAttr(data[i][0], 1)

            # set driven keys
            for data in attrData:
                for each in data:
                    cmds.setDrivenKeyframe(each[0], cd=self.armSettings + ".clavMode", itt="linear",
                                           ott="linear")
        # =======================================================================
        # #connect controls up to blender nodes to drive driver joints
        # =======================================================================

        cmds.pointConstraint(rigJnt, "driver_" + clavJoint, mo=True)
        cmds.orientConstraint(rigJnt, "driver_" + clavJoint)

        # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
        # input 2,and plugs that into driver joint
        if cmds.objExists("master_anim"):
            globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True,
                                               name=clavJoint + "_globalScale")
            cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
            cmds.connectAttr(rigJnt + ".scale", globalScaleMult + ".input2")
            riggingUtils.createConstraint(globalScaleMult, "driver_" + clavJoint, "scale", False, 2, 1,
                                          "output")
        else:
            riggingUtils.createConstraint(rigJnt, "driver_" + clavJoint, "scale", False, 2, 1)

        # =======================================================================
        # #add IK matcher under FK clav control
        # =======================================================================
        ikMatchGrp = cmds.group(empty=True, name=self.name + "_ik_clav_matcher")
        cmds.parent(ikMatchGrp, fkControl)
        const = cmds.pointConstraint(ikControl, ikMatchGrp)[0]
        cmds.delete(const)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                    Clean Up                   # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        cmds.makeIdentity(pointJnt, t=0, r=1, s=0, apply=True)
        cmds.pointConstraint(endJnt, pointJnt, mo=True)

        # create a clavicle grp
        self.clavicleGrp = cmds.group(empty=True, name=self.name + "_clavicle_grp")
        const = cmds.parentConstraint(parentBone, self.clavicleGrp)[0]
        cmds.delete(const)

        cmds.parent(self.clavicleGrp, self.armGroup)

        # parent rigJnt to clavicle group
        cmds.parent(rigJntGrp, self.clavicleGrp)

        # parent autoClavGrp and self.clavCtrlGrp to clavicle grp
        cmds.parent(self.clavCtrlGrp, self.clavicleGrp)
        cmds.parent(ikCtrlGrp, self.clavCtrlGrp)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                Hook Up Modes                  # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        cmds.setAttr(self.armSettings + ".clavMode", 0)
        cmds.setAttr(animGrp + ".v", 1)
        cmds.setAttr(ikCtrlGrp + ".v", 0)
        cmds.setDrivenKeyframe([animGrp + ".v", ikCtrlGrp + ".v"], cd=self.armSettings + ".clavMode")

        cmds.setAttr(self.armSettings + ".clavMode", 1)
        cmds.setAttr(animGrp + ".v", 0)
        cmds.setAttr(ikCtrlGrp + ".v", 1)
        cmds.setDrivenKeyframe([animGrp + ".v", ikCtrlGrp + ".v"], cd=self.armSettings + ".clavMode")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #               Add Data to Node                # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # add created control info to module

        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        if not cmds.objExists(controlNode + ".clavControls"):
            cmds.addAttr(controlNode, sn="clavControls", at="message")

        # add proxy attrs for mode
        if cmds.objExists(self.armSettings + ".mode"):
            for node in [fkControl, ikControl]:
                cmds.addAttr(node, ln="clavMode", proxy=self.armSettings + ".clavMode", at="double",
                             keyable=True)

        for node in [fkControl, ikControl]:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".clavControls", node + ".controlClass")

            cmds.addAttr(node, ln="controlType", dt="string")

            # mirroring attrs
            for attr in ["invertX", "invertY", "invertZ"]:
                if not cmds.objExists(node + "." + attr):
                    cmds.addAttr(node, ln=attr, at="bool")

            if node == fkControl:
                cmds.setAttr(node + ".controlType", "FK", type="string")
            if node == ikControl:
                cmds.setAttr(node + ".controlType", "IK", type="string")

        cmds.setAttr(fkControl + ".invertX", 1)
        cmds.setAttr(fkControl + ".invertY", 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _setupRigModes(self, numRigs, builtRigs, armJoints):

        if numRigs > 1:
            attrData = []
            rampData = []

            """ CONSTRAINTS """
            # get the constraint connections on the driver joints for the arms
            connections = []
            for joint in armJoints[1]:
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

            # setup set driven keys on our moder attr and those target attributes
            for i in range(numRigs):

                cmds.setAttr(self.armSettings + ".mode", i)

                # go through attr data and zero out anything but the first element in the list
                for data in attrData:
                    for each in data:
                        cmds.setAttr(each[0], 0)

                    cmds.setAttr(data[i][0], 1)

                # set driven keys
                for data in attrData:
                    for each in data:
                        cmds.setDrivenKeyframe(each[0], cd=self.armSettings + ".mode", itt="linear", ott="linear")

            """ RAMPS """
            # direct connect mode to uCoord value (only works if there are 2 rigs...) <- not sure if that is the case
            #  still
            for data in rampData:
                # create a multiply node that takes first input of 1/numRigs and 2nd of mode direct connection
                multNode = cmds.shadingNode("multiplyDivide", asUtility=True,
                                            name=self.name + "_" + data.partition(".uCoord")[0] + "_mult")
                cmds.setAttr(multNode + ".input1X", float(float(1) / float(numRigs - 1)))
                cmds.connectAttr(self.armSettings + ".mode", multNode + ".input2X")
                cmds.connectAttr(multNode + ".outputX", data)

            # hook up control visibility
            for i in range(len(builtRigs)):
                cmds.setAttr(self.armSettings + ".mode", i)
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

                    cmds.setDrivenKeyframe(visNodes, at="visibility", cd=self.armSettings + ".mode", itt="linear",
                                           ott="linear")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _createUpperArmTwists(self, networkNode, armJoints):

        twistJoints = self._getTwistJoints(True, False)
        twistCtrls = None

        if cmds.getAttr(networkNode + ".side") == "Left":
            twistCtrls = riggingUtils.createCounterTwistRig(twistJoints, self.name, networkNode, armJoints[1][0],
                                                            armJoints[1][1], self.armGroup, self.armCtrlGrp)
        if cmds.getAttr(networkNode + ".side") == "Right":
            twistCtrls = riggingUtils.createCounterTwistRig(twistJoints, self.name, networkNode, armJoints[1][0],
                                                            armJoints[1][1], self.armGroup, self.armCtrlGrp)

        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        # add created controls to control node
        if not cmds.objExists(controlNode + ".upArmTwistControls"):
            cmds.addAttr(controlNode, sn="upArmTwistControls", at="message")
        if twistCtrls is not None:
            for node in twistCtrls:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".upArmTwistControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _createLowerArmTwists(self, networkNode, armJoints):

        twistJoints = self._getTwistJoints(False, True)
        twistCtrls = riggingUtils.createTwistRig(twistJoints, self.name, networkNode, armJoints[1][1], armJoints[1][2],
                                                 self.armGroup, self.armCtrlGrp)

        # add created controls to control node
        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        if not cmds.objExists(controlNode + ".loArmTwistControls"):
            cmds.addAttr(controlNode, sn="loArmTwistControls", at="message")
        if twistCtrls is not None:
            for node in twistCtrls:
                cmds.lockNode(node, lock=False)
                cmds.addAttr(node, ln="controlClass", at="message")
                cmds.connectAttr(controlNode + ".loArmTwistControls", node + ".controlClass")

                cmds.addAttr(node, ln="controlType", dt="string")
                cmds.setAttr(node + ".controlType", "FK", type="string")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _hookUpArm(self, networkNode, armJoints):

        if cmds.getAttr(networkNode + ".includeClavicle"):
            armCtrlPointConst = \
                cmds.pointConstraint(["fk_" + armJoints[0] + "_anim", self.name + "_clav_follow"],
                                     self.armCtrlGrp)[0]
            armCtrlOrientConst = \
                cmds.orientConstraint(["fk_" + armJoints[0] + "_anim", self.name + "_clav_follow"],
                                      self.armCtrlGrp)[0]

            attrData = []
            for connection in [armCtrlPointConst, armCtrlOrientConst]:
                driveAttrs = []
                targets = cmds.getAttr(connection + ".target", mi=True)
                if len(targets) > 1:
                    for each in targets:
                        driveAttrs.append(
                            cmds.listConnections(connection + ".target[" + str(each) + "].targetWeight",
                                                 p=True))

                    attrData.append(driveAttrs)

            return attrData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _setupClavMode(self, networkNode, numRigs, attrData):

        if cmds.getAttr(networkNode + ".includeClavicle"):
            for i in range(numRigs):
                cmds.setAttr(self.armSettings + ".clavMode", i)

                # go through attr data and zero out anything but the first element in the list
                for data in attrData:
                    for each in data:
                        cmds.setAttr(each[0], 0)

                    cmds.setAttr(data[i][0], 1)

                # set driven keys
                for data in attrData:
                    for each in data:
                        cmds.setDrivenKeyframe(each[0], cd=self.armSettings + ".clavMode", itt="linear",
                                               ott="linear")

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
    def updateOutliner(self):
        """
        Whenever changes are made to the module settings, update the outliner (in the rig creator) to show the new
        or removed movers. Tied to skeletonSettingsUI
        """

        # CLAVICLE

        if not self.clavicleCB.isChecked():
            self.outlinerWidgets[self.originalName + "_clavicle"].setHidden(True)
        else:
            self.outlinerWidgets[self.originalName + "_clavicle"].setHidden(False)

        # UPPERARM TWISTS
        armTwists = self.upperarmTwistNum.value()
        if armTwists == 0:
            self.outlinerWidgets[self.originalName + "_upperarm_twist_01"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_03"].setHidden(True)
        if armTwists == 1:
            self.outlinerWidgets[self.originalName + "_upperarm_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_03"].setHidden(True)
        if armTwists == 2:
            self.outlinerWidgets[self.originalName + "_upperarm_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_03"].setHidden(True)
        if armTwists == 3:
            self.outlinerWidgets[self.originalName + "_upperarm_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_upperarm_twist_03"].setHidden(False)

        # LOWERARM TWISTS
        lowerarmTwists = self.lowerarmTwistNum.value()
        if lowerarmTwists == 0:
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_01"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_03"].setHidden(True)
        if lowerarmTwists == 1:
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_03"].setHidden(True)
        if lowerarmTwists == 2:
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_03"].setHidden(True)
        if lowerarmTwists == 3:
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_01"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_lowerarm_twist_03"].setHidden(False)

        # THUMB
        thumbBones = self.thumbNum.value()
        thumbMeta = self.thumbMeta.isChecked()

        if thumbBones == 0:
            self.outlinerWidgets[self.originalName + "_thumb_02"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_thumb_03"].setHidden(True)
        if thumbBones == 1:
            self.outlinerWidgets[self.originalName + "_thumb_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thumb_03"].setHidden(True)
        if thumbBones == 2:
            self.outlinerWidgets[self.originalName + "_thumb_02"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_thumb_03"].setHidden(False)

        if thumbMeta:
            self.outlinerWidgets[self.originalName + "_thumb_01"].setHidden(False)
        if not thumbMeta:
            self.outlinerWidgets[self.originalName + "_thumb_01"].setHidden(True)

        # FINGERS
        fingers = [[self.indexNum, "index", self.indexMeta], [self.middleNum, "middle", self.middleMeta],
                   [self.ringNum, "ring", self.ringMeta], [self.pinkyNum, "pinky", self.pinkyMeta]]

        for finger in fingers:
            value = finger[0].value()
            meta = finger[2].isChecked()

            if value == 0:
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_01"].setHidden(True)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_02"].setHidden(True)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_03"].setHidden(True)
            if value == 1:
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_01"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_02"].setHidden(True)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_03"].setHidden(True)
            if value == 2:
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_01"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_02"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_03"].setHidden(True)
            if value == 3:
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_01"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_02"].setHidden(False)
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_03"].setHidden(False)

            if meta:
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_metacarpal"].setHidden(False)
            if not meta:
                self.outlinerWidgets[self.originalName + "_" + finger[1] + "_metacarpal"].setHidden(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _editJointMoverViaSpinBox(self, uiWidget, searchKey, isThumb, *args):
        """
        Sets visibility on joint movers depending on spinBox values for the fingers.

        :param uiWidget: spinBox
        :param searchKey: base name of finger (thumb, middle, rig, index, pinky)
        :param isThumb: special case, since there are 3 joints instead of 4
        :param args:

        """

        # check number in spinBox
        num = uiWidget.value()

        # set visibility on movers and geo depending on the value of num
        for i in range(num + 1):
            # purely for fanciness

            if isThumb is False:

                moverList = ["_01", "_02", "_03"]
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

            if isThumb is True:

                moverList = ["_02", "_03"]
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
        :param searchKey: lowerarm vs upperarm
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
    def _editJointMoverMetaCarpals(self, uiWidget, searchKey, *args):
        """
        Set the visibility and parenting of the proximal knuckles based on the spinBoxes

        :param uiWidget: spinBox
        :param searchKey: finger base name (pinky, index, middle, ring)

        """
        base_knuckle = "_01_mover_grp"
        metacarpal = "_metacarpal_mover"
        if searchKey == "thumb":
            metacarpal = "_01_mover"
            base_knuckle = "_02_mover_grp"

        # toggle visibility
        if uiWidget.isChecked():
            try:
                cmds.parent(self.name + "_" + searchKey + base_knuckle,
                            self.name + "_" + searchKey + metacarpal)
            except Exception, e:
                print e

            cmds.setAttr(self.name + "_" + searchKey + metacarpal + "_grp.v", lock=False)
            cmds.setAttr(self.name + "_" + searchKey + metacarpal + "_grp.v", 1, lock=True)

        if not uiWidget.isChecked():
            try:
                cmds.parent(self.name + "_" + searchKey + base_knuckle, self.name + "_hand_mover")
            except Exception, e:
                print e

            cmds.setAttr(self.name + "_" + searchKey + metacarpal + "_grp.v", lock=False)
            cmds.setAttr(self.name + "_" + searchKey + metacarpal + "_grp.v", 0, lock=True)

        # toggle mover vis
        self.rigUiInst.setMoverVisibility()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _toggleButtonState(self):
        """Toggle the state of the Apply Changes button."""

        state = self.applyButton.isEnabled()
        if state is False:
            self.applyButton.setEnabled(True)