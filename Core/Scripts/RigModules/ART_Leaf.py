"""
Author: Jeremy Ernst

========
Contents
========

|   **Must Have Methods:**
|       :py:func:`addAttributes <RigModules.ART_Leaf.ART_Leaf.addAttributes>`
|       :py:func:`skeletonSettings_UI <RigModules.ART_Leaf.ART_Leaf.skeletonSettings_UI>`
|       :py:func:`addJointMoverToOutliner <RigModules.ART_Leaf.ART_Leaf.addJointMoverToOutliner>`
|       :py:func:`updateSettingsUI <RigModules.ART_Leaf.ART_Leaf.updateSettingsUI>`
|       :py:func:`applyModuleChanges <RigModules.ART_Leaf.ART_Leaf.applyModuleChanges>`
|       :py:func:`pinModule <RigModules.ART_Leaf.ART_Leaf.pinModule>`
|       :py:func:`skinProxyGeo <RigModules.ART_Leaf.ART_Leaf.skinProxyGeo>`
|       :py:func:`buildRigCustom <RigModules.ART_Leaf.ART_Leaf.buildRigCustom>`
|       :py:func:`pickerUI <RigModules.ART_Leaf.ART_Leaf.pickerUI>`
|       :py:func:`importFBX <RigModules.ART_Leaf.ART_Leaf.importFBX>`
|
|   **Module Specific Methods:**
|       :py:func:`mirrorTransformations_Custom <RigModules.ART_Leaf.ART_Leaf.mirrorTransformations_Custom>`
|       :py:func:`changeProxyGeo <RigModules.ART_Leaf.ART_Leaf.changeProxyGeo>`
|       :py:func:`changeControlShape <RigModules.ART_Leaf.ART_Leaf.changeControlShape>`
|       :py:func:`changeButtonColor <RigModules.ART_Leaf.ART_Leaf.changeButtonColor>`
|       :py:func:`pasteSettings <RigModules.ART_Leaf.ART_Leaf.pasteSettings>`
|
|   **Interface Methods:**
|       :py:func:`removeCustomAttr <RigModules.ART_Leaf.ART_Leaf.removeCustomAttr>`
|       :py:func:`customAttr_UI <RigModules.ART_Leaf.ART_Leaf.customAttr_UI>`
|       :py:func:`_customAttr_UI_attrType <RigModules.ART_Leaf.ART_Leaf._customAttr_UI_attrType>`
|       :py:func:`customAttr_UI_Accept <RigModules.ART_Leaf.ART_Leaf.customAttr_UI_Accept>`
|       :py:func:`selectSettings <RigModules.ART_Leaf.ART_Leaf.selectSettings>`


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

import json
import os
from functools import partial

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
from Base.ART_RigModule import ART_RigModule
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# file attributes
search = "jnt:joint:leaf"
className = "ART_Leaf"
jointMover = "Core/JointMover/z_up/ART_Leaf.ma"
baseName = "jnt"
displayName = "Joint"
fbxImport = ["None", "FK"]
matchData = [False, None]  # This is for matching over frame range options. (Matching between rigs of the module)
tooltip_image = "ART_Leaf"


class ART_Leaf(ART_RigModule):
    """
    This class create a single joint with an FK rig and an optional dynamics rig.
    """

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

        ART_RigModule.__init__(self, "ART_Leaf_Module", "ART_Leaf", moduleUserName)

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
        cmds.setAttr(self.networkNode + ".Created_Bones", "jnt", type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="baseName", dt="string", keyable=False)
        cmds.setAttr(self.networkNode + ".baseName", baseName, type="string", lock=True)

        cmds.addAttr(self.networkNode, sn="canAim", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".canAim", False, lock=True)

        cmds.addAttr(self.networkNode, sn="aimMode", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".aimMode", False, lock=True)

        cmds.addAttr(self.networkNode, sn="controlType", at="enum",
                     en="Circle:Square:Triangle:Cube:Sphere:Cylinder:Arrow", keyable=False)
        cmds.setAttr(self.networkNode + ".controlType", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="proxyShape", at="enum", en="Cube:Cylinder:Capsule:Sphere:Cone",
                     keyable=False)
        cmds.setAttr(self.networkNode + ".proxyShape", 0, lock=True)

        cmds.addAttr(self.networkNode, sn="hasDynamics", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".hasDynamics", False, lock=True)

        cmds.addAttr(self.networkNode, sn="transX", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".transX", True, lock=True)

        cmds.addAttr(self.networkNode, sn="transY", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".transY", True, lock=True)

        cmds.addAttr(self.networkNode, sn="transZ", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".transZ", True, lock=True)

        cmds.addAttr(self.networkNode, sn="rotX", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".rotX", True, lock=True)

        cmds.addAttr(self.networkNode, sn="rotY", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".rotY", True, lock=True)

        cmds.addAttr(self.networkNode, sn="rotZ", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".rotZ", True, lock=True)

        cmds.addAttr(self.networkNode, sn="scaleX", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".scaleX", True, lock=True)

        cmds.addAttr(self.networkNode, sn="scaleY", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".scaleY", True, lock=True)

        cmds.addAttr(self.networkNode, sn="scaleZ", at="bool", keyable=False)
        cmds.setAttr(self.networkNode + ".scaleZ", True, lock=True)

        cmds.addAttr(self.networkNode, sn="customAttrs", dt="string", keyable=False)

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

        networkNode = self.returnNetworkNode

        # groupbox all modules get
        ART_RigModule.skeletonSettings_UI(self, name, 335, 438, True)

        font = QtGui.QFont()
        font.setPointSize(8)

        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # create a VBoxLayout to add to our Groupbox and then add a QFrame for our signal/slot
        self.mainLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setObjectName("lightnoborder")
        self.mainLayout.addWidget(self.frame)
        self.frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.frame.setMinimumSize(QtCore.QSize(320, 420))
        self.frame.setMaximumSize(QtCore.QSize(320, 420))

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

        # settings for control shape
        self.controlShapeLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.controlShapeLayout)

        self.controlShapeLabel = QtWidgets.QLabel("Control Type: ")
        self.controlShapeLabel.setFont(font)
        self.controlShapeLayout.addWidget(self.controlShapeLabel)

        self.controlShapeType = QtWidgets.QComboBox()
        self.controlShapeLayout.addWidget(self.controlShapeType)
        self.controlShapeType.addItem("Circle")
        self.controlShapeType.addItem("Square")
        self.controlShapeType.addItem("Triangle")
        self.controlShapeType.addItem("Cube")
        self.controlShapeType.addItem("Sphere")
        self.controlShapeType.addItem("Cylinder")
        self.controlShapeType.addItem("Arrow")
        text = "Change the shape of the control. This control will also be used for the rig build."
        self.controlShapeType.setToolTip(text)

        # settings for proxy geo shape
        self.proxyShapeLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.proxyShapeLayout)

        self.proxyShapeLabel = QtWidgets.QLabel("Proxy Shape: ")
        self.proxyShapeLabel.setFont(font)
        self.proxyShapeLayout.addWidget(self.proxyShapeLabel)

        self.proxyShapeType = QtWidgets.QComboBox()
        self.proxyShapeLayout.addWidget(self.proxyShapeType)
        self.proxyShapeType.addItem("Cube")
        self.proxyShapeType.addItem("Cylinder")
        self.proxyShapeType.addItem("Capsule")
        self.proxyShapeType.addItem("Sphere")
        self.proxyShapeType.addItem("Cone")
        text = "Change the shape of the proxy geometry. This is purely aesthetic and has no impact on the rig."
        self.proxyShapeType.setToolTip(text)

        # Rig Settings
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout.addItem(spacerItem)

        self.hasDynamics = QtWidgets.QCheckBox("Has Dynamics")
        self.layout.addWidget(self.hasDynamics)
        self.hasDynamics.setChecked(False)
        self.hasDynamics.clicked.connect(partial(self.applyModuleChanges, self))
        text = "Rig this module to have Maya dynamics built in."
        self.hasDynamics.setToolTip(text)

        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.layout.addItem(spacerItem)

        label = QtWidgets.QLabel("Keyable Attributes:")
        label.setFont(headerFont)
        self.layout.addWidget(label)

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self.layout.addItem(spacerItem)

        # TRANSLATES
        self.translateSettingsLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.translateSettingsLayout)

        self.txAttr = QtWidgets.QCheckBox("TranslateX")
        self.txAttr.setChecked(True)
        self.translateSettingsLayout.addWidget(self.txAttr)
        self.txAttr.clicked.connect(partial(self.applyModuleChanges, self))

        self.tyAttr = QtWidgets.QCheckBox("TranslateY")
        self.tyAttr.setChecked(True)
        self.translateSettingsLayout.addWidget(self.tyAttr)
        self.tyAttr.clicked.connect(partial(self.applyModuleChanges, self))

        self.tzAttr = QtWidgets.QCheckBox("TranslateZ")
        self.tzAttr.setChecked(True)
        self.translateSettingsLayout.addWidget(self.tzAttr)
        self.tzAttr.clicked.connect(partial(self.applyModuleChanges, self))

        # ROTATES
        self.rotateSettingsLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.rotateSettingsLayout)

        self.rxAttr = QtWidgets.QCheckBox("RotateX")
        self.rxAttr.setChecked(True)
        self.rotateSettingsLayout.addWidget(self.rxAttr)
        self.rxAttr.clicked.connect(partial(self.applyModuleChanges, self))

        self.ryAttr = QtWidgets.QCheckBox("RotateY")
        self.ryAttr.setChecked(True)
        self.rotateSettingsLayout.addWidget(self.ryAttr)
        self.ryAttr.clicked.connect(partial(self.applyModuleChanges, self))

        self.rzAttr = QtWidgets.QCheckBox("RotateZ")
        self.rzAttr.setChecked(True)
        self.rotateSettingsLayout.addWidget(self.rzAttr)
        self.rzAttr.clicked.connect(partial(self.applyModuleChanges, self))

        # SCALES
        self.scaleSettingsLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.scaleSettingsLayout)

        self.sxAttr = QtWidgets.QCheckBox("ScaleX")
        self.sxAttr.setChecked(True)
        self.scaleSettingsLayout.addWidget(self.sxAttr)
        self.sxAttr.clicked.connect(partial(self.applyModuleChanges, self))

        self.syAttr = QtWidgets.QCheckBox("ScaleY")
        self.syAttr.setChecked(True)
        self.scaleSettingsLayout.addWidget(self.syAttr)
        self.syAttr.clicked.connect(partial(self.applyModuleChanges, self))

        self.szAttr = QtWidgets.QCheckBox("ScaleZ")
        self.szAttr.setChecked(True)
        self.scaleSettingsLayout.addWidget(self.szAttr)
        self.szAttr.clicked.connect(partial(self.applyModuleChanges, self))

        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(self.groupBox, QtCore.SIGNAL("toggled(bool)"), self.frame.setVisible)
        self.groupBox.setChecked(False)

        # add custom attributes
        buttonLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(buttonLayout)

        self.addAttrBtn = QtWidgets.QPushButton("Add Custom Attribute")
        self.addAttrBtn.setObjectName("settings")
        self.addAttrBtn.setMinimumHeight(30)
        self.addAttrBtn.setMaximumHeight(30)
        buttonLayout.addWidget(self.addAttrBtn)
        self.addAttrBtn.clicked.connect(self.customAttr_UI)
        text = "Add a custom attribute. (Same as going to Modify > Add Attribute.)"
        self.addAttrBtn.setToolTip(text)

        self.removeAttrBtn = QtWidgets.QPushButton("Remove Selected Attr")
        self.removeAttrBtn.setObjectName("settings")
        self.removeAttrBtn.setMinimumHeight(30)
        self.removeAttrBtn.setMaximumHeight(30)
        buttonLayout.addWidget(self.removeAttrBtn)
        self.removeAttrBtn.clicked.connect(self.removeCustomAttr)
        text = "Remove a custom attribute."
        self.removeAttrBtn.setToolTip(text)

        self.customAttrsList = QtWidgets.QListWidget()
        self.layout.addWidget(self.customAttrsList)

        # add custom skeletonUI settings  name, parent, rig types to install, mirror module, thigh twist, calf twists,
        # ball joint, toes,
        # add to the rig cretor UI's module settings layout VBoxLayout
        self.rigUiInst.moduleSettingsLayout.addWidget(self.groupBox)

        # Populate the settings UI based on the network node attributes
        self.updateSettingsUI()

        # hook up combo box signals
        self.controlShapeType.currentIndexChanged.connect(partial(self.changeControlShape))
        self.proxyShapeType.currentIndexChanged.connect(partial(self.changeProxyGeo))

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

        # Add the module to the tree widget in the outliner tab of the rig creator UI
        self.outlinerWidgets[self.name + "_treeModule"] = QtWidgets.QTreeWidgetItem(self.rigUiInst.treeWidget)
        self.rigUiInst.treeWidget.topLevelItem(index).setText(0, self.name)
        foreground = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        self.outlinerWidgets[self.name + "_treeModule"].setForeground(0, foreground)

        # add the buttons
        self.createGlobalMoverButton(self.name, self.outlinerWidgets[self.name + "_treeModule"], self.rigUiInst)
        self.createOffsetMoverButton(self.name, self.outlinerWidgets[self.name + "_treeModule"], self.rigUiInst)
        self.createMeshMoverButton(self.name, self.outlinerWidgets[self.name + "_treeModule"], self.rigUiInst)

        # create selection script job for module
        self.updateBoneCount()
        self.createScriptJob()

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

        cmds.refresh(force=True)
        networkNode = self.returnNetworkNode

        # shapes
        controlShape = cmds.getAttr(networkNode + ".controlType")
        self.controlShapeType.setCurrentIndex(controlShape)

        proxyShape = cmds.getAttr(networkNode + ".proxyShape")
        self.proxyShapeType.setCurrentIndex(proxyShape)

        # transformations
        self.txAttr.setChecked(cmds.getAttr(networkNode + ".transX"))
        self.tyAttr.setChecked(cmds.getAttr(networkNode + ".transY"))
        self.tzAttr.setChecked(cmds.getAttr(networkNode + ".transZ"))

        self.rxAttr.setChecked(cmds.getAttr(networkNode + ".rotX"))
        self.ryAttr.setChecked(cmds.getAttr(networkNode + ".rotY"))
        self.rzAttr.setChecked(cmds.getAttr(networkNode + ".rotZ"))

        self.sxAttr.setChecked(cmds.getAttr(networkNode + ".scaleX"))
        self.syAttr.setChecked(cmds.getAttr(networkNode + ".scaleY"))
        self.szAttr.setChecked(cmds.getAttr(networkNode + ".scaleZ"))

        # has dynamics
        self.hasDynamics.setChecked(cmds.getAttr(networkNode + ".hasDynamics"))

        # custom attrs
        self.customAttrsList.clear()
        try:
            data = json.loads(cmds.getAttr(networkNode + ".customAttrs"))

            if isinstance(data[0], list):
                for each in data:
                    jsonString = json.dumps(each)
                    self.customAttrsList.addItem(jsonString)
            else:
                jsonString = json.dumps(data)
                self.customAttrsList.addItem(jsonString)
        except:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleChanges(self, moduleInst, *args):
        """
        Update the scene after the settings are changed in the skeleton settings UI. In the case of the chain, this
        usually means an increase or decrease in the number of joints in the chain.

        This means also updating the created_bones attr, updating the joint mover if needed,
        running self.updateNeck, updating the outliner, and updating the bone count.

        :param moduleInst: self (usually, but there are cases like templates where an inst on disc is passed in.)
        """

        networkNode = self.returnNetworkNode

        # translations
        cmds.setAttr(networkNode + ".transX", lock=False)
        cmds.setAttr(networkNode + ".transX", self.txAttr.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".transY", lock=False)
        cmds.setAttr(networkNode + ".transY", self.tyAttr.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".transZ", lock=False)
        cmds.setAttr(networkNode + ".transZ", self.tzAttr.isChecked(), lock=True)

        # rotations
        cmds.setAttr(networkNode + ".rotX", lock=False)
        cmds.setAttr(networkNode + ".rotX", self.rxAttr.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".rotY", lock=False)
        cmds.setAttr(networkNode + ".rotY", self.ryAttr.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".rotZ", lock=False)
        cmds.setAttr(networkNode + ".rotZ", self.rzAttr.isChecked(), lock=True)

        # scales
        cmds.setAttr(networkNode + ".scaleX", lock=False)
        cmds.setAttr(networkNode + ".scaleX", self.sxAttr.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".scaleY", lock=False)
        cmds.setAttr(networkNode + ".scaleY", self.syAttr.isChecked(), lock=True)

        cmds.setAttr(networkNode + ".scaleZ", lock=False)
        cmds.setAttr(networkNode + ".scaleZ", self.szAttr.isChecked(), lock=True)

        # dynamics
        cmds.setAttr(networkNode + ".hasDynamics", lock=False)
        cmds.setAttr(networkNode + ".hasDynamics", self.hasDynamics.isChecked(), lock=True)

        # shapes
        cmds.setAttr(networkNode + ".controlType", lock=False)
        cmds.setAttr(networkNode + ".controlType", self.controlShapeType.currentIndex(), lock=True)

        cmds.setAttr(networkNode + ".proxyShape", lock=False)
        cmds.setAttr(networkNode + ".proxyShape", self.proxyShapeType.currentIndex(), lock=True)

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
        topLevelMover = self.name + "_mover"

        if state:
            if cmds.getAttr(networkNode + ".pinned") is True:
                return
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
                        print each
                        print str(e)

            # create skinned geo group
            if not cmds.objExists("skinned_proxy_geo"):
                cmds.group(empty=True, name="skinned_proxy_geo")

            cmds.parent(dupeMesh, "skinned_proxy_geo")

            boneName = mesh.partition(name + "_")[2]
            boneName = boneName.partition("_proxy_geo")[0]
            joint = name

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

        if textEdit is not None:
            textEdit.append("        Building " + self.name + " Rig..")

        # get the created joint
        networkNode = self.returnNetworkNode
        joint = cmds.getAttr(networkNode + ".Created_Bones")
        joint = joint.replace("::", "")
        globalMover = joint + "_mover"
        parentBone = cmds.getAttr(networkNode + ".parentModuleBone")

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

        # determine the rigs to be built
        numRigs = 1
        if cmds.getAttr(networkNode + ".hasDynamics"):
            numRigs += 1

        builtRigs = []

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # create groups and settings
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # create the rig group
        self.rigGrp = cmds.group(empty=True, name=self.name + "_group")
        constraint = cmds.parentConstraint(globalMover, self.rigGrp)[0]
        cmds.delete(constraint)

        # create the rig settings group
        self.rigSettings = cmds.group(empty=True, name=self.name + "_settings")
        cmds.parent(self.rigSettings, self.rigGrp)
        for attr in (cmds.listAttr(self.rigSettings, keyable=True)):
            cmds.setAttr(self.rigSettings + "." + attr, lock=True, keyable=False)

        # add mode attribute to settings
        if numRigs > 1:
            cmds.addAttr(self.rigSettings, ln="mode", min=0, max=numRigs - 1, dv=0, keyable=True)

        # create the ctrl group (what will get the constraint to the parent)
        self.rigCtrlGrp = cmds.group(empty=True, name=self.name + "_ctrl_grp")
        constraint = cmds.parentConstraint(parentBone, self.rigCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(self.rigCtrlGrp, self.rigGrp)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # build the rigs
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                       FK                      # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # find the mover, duplicate it to create the rig control
        dupe = cmds.duplicate(globalMover, rr=True)[0]
        utils.deleteChildren(dupe)
        parent = cmds.listRelatives(dupe, parent=True)
        if parent is not None:
            cmds.parent(dupe, world=True)

        # turn on visiblity of the control
        cmds.setAttr(dupe + ".v", 1)

        # ensure pivot is correct
        piv = cmds.xform(joint, q=True, ws=True, rp=True)
        cmds.xform(dupe, ws=True, rp=piv)

        # rename the control
        fkControl = cmds.rename(dupe, joint + "_anim")

        # mirroring attrs
        for attr in ["invertX", "invertY", "invertZ"]:
            if not cmds.objExists(fkControl + "." + attr):
                cmds.addAttr(fkControl, ln=attr, at="bool")

        cmds.setAttr(fkControl + ".invertX", 1)

        # create an anim group for the control
        controlGrp = cmds.group(empty=True, name=joint + "_anim_grp")
        constraint = cmds.parentConstraint(joint, controlGrp)[0]
        cmds.delete(constraint)

        # create the space switcher group
        spaceSwitchFollow = cmds.duplicate(controlGrp, po=True, name=fkControl + "_space_switcher_follow")[0]
        spaceSwitch = cmds.duplicate(controlGrp, po=True, name=fkControl + "_space_switcher")[0]

        utils.deleteChildren(spaceSwitchFollow)
        utils.deleteChildren(spaceSwitch)

        cmds.parent(spaceSwitch, spaceSwitchFollow)
        cmds.parent(controlGrp, spaceSwitch)

        # parent the control under the controlGrp
        cmds.parent(fkControl, controlGrp)
        cmds.parent(spaceSwitchFollow, self.rigCtrlGrp)

        # freeze transformations on the control
        cmds.makeIdentity(fkControl, t=1, r=1, s=1, apply=True)

        # color the control
        cmds.setAttr(fkControl + ".overrideEnabled", 1)
        cmds.setAttr(fkControl + ".overrideColor", 18)

        # constrain joint
        cmds.parentConstraint(fkControl, "driver_" + joint)
        cmds.scaleConstraint(fkControl, "driver_" + joint)

        # parent under offset_anim if it exists(it always should)
        if cmds.objExists("offset_anim"):
            cmds.parent(self.rigGrp, "offset_anim")

        # check settings and lock attributes that need locking
        if not cmds.getAttr(networkNode + ".transX"):
            cmds.setAttr(fkControl + ".tx", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".transY"):
            cmds.setAttr(fkControl + ".ty", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".transZ"):
            cmds.setAttr(fkControl + ".tz", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".rotX"):
            cmds.setAttr(fkControl + ".rx", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".rotY"):
            cmds.setAttr(fkControl + ".ry", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".rotZ"):
            cmds.setAttr(fkControl + ".rz", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".scaleX"):
            cmds.setAttr(fkControl + ".sx", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".scaleY"):
            cmds.setAttr(fkControl + ".sy", lock=True, keyable=False)

        if not cmds.getAttr(networkNode + ".scaleZ"):
            cmds.setAttr(fkControl + ".sz", lock=True, keyable=False)

        # lock visibility regardless
        cmds.setAttr(fkControl + ".v", lock=True, keyable=False)

        # check for custom attributes and add them if they exist
        try:
            data = json.loads(cmds.getAttr(networkNode + ".customAttrs"))
            print data
            for each in data:
                attrName = each[0]
                attrType = each[1]

                if attrType == "Bool":
                    value = each[2]

                    if not cmds.objExists(fkControl + "." + attrName):
                        cmds.addAttr(fkControl, ln=attrName, at="bool", keyable=True, dv=value)

                if attrType == "Float":
                    minVal = each[2]
                    maxVal = each[3]
                    hasMin = True
                    hasMax = True

                    if minVal == '':
                        hasMin = False
                        minVal = 0

                    if maxVal == '':
                        hasMax = False
                        maxVal = 0

                    if not cmds.objExists(fkControl + "." + attrName):

                        if hasMin is False and hasMax is False:
                            cmds.addAttr(fkControl, ln=attrName, at="float", keyable=True, dv=float(each[4]))
                        if hasMin is False and hasMax is True:
                            cmds.addAttr(fkControl, ln=attrName, at="float", keyable=True, max=float(maxVal),
                                         dv=float(each[4]))
                        if hasMin is True and hasMax is False:
                            cmds.addAttr(fkControl, ln=attrName, at="float", keyable=True, min=float(minVal),
                                         dv=float(each[4]))

        except Exception, e:
            print e

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                   Dynamics                    # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if cmds.getAttr(networkNode + ".hasDynamics"):
            cubeGrp = cmds.group(empty=True, name=self.name + "_dyn_grp")
            const = cmds.parentConstraint(joint, cubeGrp)[0]
            cmds.delete(const)
            cmds.parent(cubeGrp, self.rigGrp)

            # make grp pivot same as parent bone
            piv = cmds.xform(parentBone, q=True, ws=True, rp=True)
            cmds.xform(cubeGrp, ws=True, piv=piv)
            cmds.parentConstraint("driver_" + parentBone, cubeGrp, mo=True)

            # creation: cube rigid body in same spot as leaf joint
            self.rigidCube = cmds.polyCube(name=self.name + "_dyn_obj")[0]
            const = cmds.parentConstraint(joint, self.rigidCube)[0]
            cmds.delete(const)

            cmds.setAttr(self.rigidCube + ".v", 0, lock=True)
            cmds.parent(self.rigidCube, cubeGrp)
            cmds.makeIdentity(self.rigidCube, t=1, r=1, s=1, apply=True)

            # usually this is done automatically, but for some reason, this damn cube would not add the attr
            # properly in the loop. so..hax
            cmds.addAttr(self.rigidCube, ln="sourceModule", dt="string")

            # create the rigid body
            cmds.select(self.rigidCube)
            rigidBody = cmds.rigidBody(act=True, m=1, damping=0.1, staticFriction=0.2, dynamicFriction=0.2,
                                       bounciness=0.6, layer=0, tesselationFactor=200)

            # create the spring constraint
            cmds.select(self.rigidCube)
            spring = cmds.constrain(spring=True, stiffness=100, damping=1.0, i=0)
            cmds.refresh(force=True)
            cmds.setAttr(spring + ".v", 0, lock=True)

            # position spring
            pos = cmds.xform(joint, q=True, ws=True, t=True)

            cmds.setAttr(spring + ".translateX", pos[0])
            cmds.setAttr(spring + ".translateY", pos[1])
            cmds.setAttr(spring + ".translateZ", pos[2])
            cmds.refresh(force=True)

            cmds.parent(spring, "driver_" + parentBone)

            # create a group that is point constrained to the cube, but orient constrained to the parent bone
            tracker = cmds.group(empty=True, name=self.name + "_dyn_tracker")
            const = cmds.parentConstraint(joint, tracker)[0]
            cmds.delete(const)

            cmds.parent(tracker, self.rigGrp)
            cmds.pointConstraint(self.rigidCube, tracker)
            orientConst = cmds.orientConstraint("driver_" + parentBone, tracker, mo=True)[0]

            # constrain joint
            cmds.parentConstraint(tracker, "driver_" + joint)
            cmds.scaleConstraint(tracker, "driver_" + joint)

            # add relevant settings to the settings node
            cmds.addAttr(self.rigSettings, ln="mass", keyable=True, dv=1)
            cmds.addAttr(self.rigSettings, ln="bounciness", keyable=True, dv=0.6, min=0, max=2)
            cmds.addAttr(self.rigSettings, ln="damping", keyable=True, dv=0.97, min=-10, max=10)
            cmds.addAttr(self.rigSettings, ln="springDamping", keyable=True, dv=1.0, min=-10, max=10)
            cmds.addAttr(self.rigSettings, ln="springStiffness", keyable=True, dv=500, min=0)
            cmds.addAttr(self.rigSettings, ln="orientToParent", keyable=True, dv=1, min=0, max=1)

            # then hook them up
            cmds.connectAttr(self.rigSettings + ".mass", rigidBody + ".mass")
            cmds.connectAttr(self.rigSettings + ".bounciness", rigidBody + ".bounciness")
            cmds.connectAttr(self.rigSettings + ".damping", rigidBody + ".damping")
            cmds.connectAttr(self.rigSettings + ".springStiffness", spring + ".springStiffness")
            cmds.connectAttr(self.rigSettings + ".springDamping", spring + ".springDamping")
            cmds.connectAttr(self.rigSettings + ".orientToParent", orientConst + ".driver_" + parentBone + "W0")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # #                   SETTINGS                    # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # mode
        if numRigs > 1:
            attrData = []

            """ CONSTRAINTS """
            # get the constraint connections on the driver joints for the leaf
            connections = []
            connections.extend(list(set(cmds.listConnections("driver_" + joint, type="constraint"))))

            for connection in connections:
                driveAttrs = []

                if cmds.nodeType(connection) in ["parentConstraint", "scaleConstraint"]:

                    # get those constraint target attributes for each constraint connection
                    targets = cmds.getAttr(connection + ".target", mi=True)
                    if len(targets) > 1:
                        for each in targets:
                            driveAttrs.append(
                                cmds.listConnections(connection + ".target[" + str(each) + "].targetWeight", p=True))

                        # add this data to our master list of constraint attribute data
                        attrData.append(driveAttrs)

            # setup set driven keys on our moder attr and those target attributes
            for i in range(numRigs):
                cmds.setAttr(self.rigSettings + ".mode", i)

                # go through attr data and zero out anything but the first element in the list
                for data in attrData:
                    for each in data:
                        cmds.setAttr(each[0], 0)

                    cmds.setAttr(data[i][0], 1)

                # set driven keys
                for data in attrData:
                    for each in data:
                        cmds.setDrivenKeyframe(each[0], cd=self.rigSettings + ".mode", itt="linear", ott="linear")

            # hook up control visibility
            cmds.setAttr(self.rigSettings + ".mode", 0)
            cmds.setAttr(controlGrp + ".v", 1)
            cmds.setDrivenKeyframe(controlGrp, at="visibility", cd=self.rigSettings + ".mode", itt="linear",
                                   ott="linear")

            cmds.setAttr(self.rigSettings + ".mode", 1)
            cmds.setAttr(controlGrp + ".v", 0)
            cmds.setDrivenKeyframe(controlGrp, at="visibility", cd=self.rigSettings + ".mode", itt="linear",
                                   ott="linear")

            cmds.setAttr(self.rigSettings + ".mode", 0)

        controlNode = cmds.listConnections(networkNode + ".controls")[0]
        controls = [fkControl]

        # add created controls to control node
        if not cmds.objExists(controlNode + ".leafControls"):
            cmds.addAttr(controlNode, sn="leafControls", at="message")
        for node in controls:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".leafControls", node + ".controlClass")

            cmds.addAttr(node, ln="controlType", dt="string")
            cmds.setAttr(node + ".controlType", "FK", type="string")

            cmds.addAttr(node, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".hasSpaceSwitching", lock=True)
            cmds.addAttr(node, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".canUseRotationSpace", lock=True)
            cmds.addAttr(node, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
            cmds.setAttr(node + ".canUseTranslationSpace", lock=True)

        # return data
        try:
            uiInst.rigData.append([self.rigCtrlGrp, "driver_" + parentBone, numRigs])

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
        self.namespace = namespace

        # create qBrushes
        blueBrush = QtGui.QColor(67, 122, 150)
        clearBrush = QtGui.QBrush(QtCore.Qt.black)
        clearBrush.setStyle(QtCore.Qt.NoBrush)

        # create border item
        if networkNode.find(":") != -1:
            moduleNode = networkNode.partition(":")[2]
        else:
            moduleNode = networkNode
        borderItem = interfaceUtils.pickerBorderItem(center.x() - 40, center.y() - 70, 50, 50, clearBrush, moduleNode)

        # get controls
        networkNode = self.returnNetworkNode
        controls = self.getControls(False, "leafControls")

        # anim button
        button = interfaceUtils.pickerButton(30, 30, [10, 2], controls[0], blueBrush, borderItem)
        button.setToolTip(self.name)

        # add right click menu to select settings
        fkIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/jointFilter.png"))))
        button.menu.addAction(fkIcon, "Settings", partial(self.selectSettings, namespace))
        button.menu.addAction("Change Button Color", partial(self.changeButtonColor, animUI, button, borderItem,
                                                             controls[0]))

        # spaces
        button.menu.addSeparator()
        button.addSpaces = partial(self.addSpacesToMenu, controls[0], button)

        # =======================================================================
        # #Create scriptJob for selection. Set scriptJob number to borderItem.data(5)
        # =======================================================================
        scriptJob = cmds.scriptJob(event=["SelectionChanged", partial(self.selectionScriptJob_animUI,
                                                                      [[button, controls[0], blueBrush]])],
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
        control = self.getControls(False, "leafControls")
        joints = cmds.getAttr(networkNode + ".Created_Bones")
        joint = joints.partition("::")[0]

        if importMethod == "FK":
            cmds.parentConstraint(joint, control[0])
            returnControls.append(control[0])

        if importMethod == "None":
            pass

        return returnControls

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
    def mirrorTransformations_Custom(self):
        """
        This method is run after the base class mirrorTransformations method and is used to do anything specific that
        a module might need that differs from all the base functionality. In the case of the chain, it needs to change
        some of the values to be negative or positive due to the local rotation axis of the joint movers.

        """

        networkNode = self.returnNetworkNode
        mirrorModule = cmds.getAttr(networkNode + ".mirrorModule")
        moduleName = cmds.getAttr(networkNode + ".moduleName")

        for mover in [self.name + "_mover", self.name + "_mover_offset", self.name + "_mover_geo"]:
            mirrorMover = mover.replace(moduleName, mirrorModule)
            for attr in [".tx", ".ry", ".rz"]:
                value = cmds.getAttr(mover + attr)
                cmds.setAttr(mirrorMover + attr, value * -1)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # handle parent offsets
        mirrorModGrp = mirrorModule + "_mover_grp"

        # get the connections/constraints to this group
        constraintData = {}

        # get all connection data to the parent group of the mirror module
        for attr in [".translateX", ".translateY", ".translateZ", ".rotateX", ".rotateY", ".rotateZ", ".scaleX",
                     ".scaleY", ".scaleZ"]:
            connection = cmds.listConnections(mirrorModGrp + attr, source=True, plugs=True)
            if connection is not None:

                # there should be a constraint connection. Let's remove the plug info to just get the constraint name.
                constraint = connection[0].partition(".")[0]

                # go ahead and disconnect the constraint now just in case there are any issues after deleting it.
                cmds.disconnectAttr(connection[0], mirrorModGrp + attr)

                # get the constraint targets and the constraint type
                targets = None
                type = None
                if cmds.nodeType(constraint) == "parentConstraint":
                    targets = cmds.parentConstraint(constraint, q=True, tl=True)
                    type = "parentConstraint"

                if cmds.nodeType(constraint) == "pointConstraint":
                    targets = cmds.pointConstraint(constraint, q=True, tl=True)
                    type = "pointConstraint"

                if cmds.nodeType(constraint) == "orientConstraint":
                    targets = cmds.orientConstraint(constraint, q=True, tl=True)
                    type = "orientConstraint"

                if cmds.nodeType(constraint) == "scaleConstraint":
                    targets = cmds.scaleConstraint(constraint, q=True, tl=True)
                    type = "scaleConstraint"

                # store all of this data so that we can recreate the constraint properly after adjusting the top level
                # group values
                if constraint not in constraintData:
                    constraintData[constraint] = [type, mirrorModGrp, targets]

                    # delete the constraint
                    cmds.delete(constraint)

        # make sure the mirror groups's values match the original's
        cmds.setAttr(mirrorModGrp + ".tx", cmds.getAttr(moduleName + "_mover_grp.tx") * -1)
        cmds.setAttr(mirrorModGrp + ".ty", cmds.getAttr(moduleName + "_mover_grp.ty"))
        cmds.setAttr(mirrorModGrp + ".tz", cmds.getAttr(moduleName + "_mover_grp.tz"))

        # recreate constraints
        for each in constraintData:
            data = constraintData.get(each)
            commandString = "cmds." + data[0] + "(" + str(data[2]) + ", \"" + data[
                1] + "\", mo=True, name=\"" + each \
                            + "\")"
            exec (commandString)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeProxyGeo(self, *args):
        """
        Changes the proxy geo of the leaf module joint mover. There are a few default shapes to choose from so that
        the proxy geo more resembles what it is standing in for.
        """

        currentSelection = cmds.ls(sl=True)

        # get new proxy geo value from comboBox
        newShape = self.proxyShapeType.currentText()

        # construct the path
        path = os.path.join(self.toolsPath, "Core/JointMover/controls/")
        fullPath = os.path.join(path, "proxy_" + newShape + ".ma")
        fullPath = utils.returnFriendlyPath(fullPath)

        # import the file
        cmds.file(fullPath, i=True, iv=True, type="mayaAscii", rnn=True)

        # assign materials if they exist, removing duplicate materials
        materials = [["*_blue_m", "blue_m"], ["*_green_m", "green_m"], ["*_red_m", "red_m"], ["*_white_m", "white_m"],
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
            except:
                pass

        # delete all deleteMaterials
        for mat in deleteMaterials:
            cmds.delete(mat)

        # parent under mover_geo
        cmds.parent("proxy_geo", self.name + "_mover_geo", r=True)
        if self.up == "y":
            cmds.setAttr("proxy_geo.rotateX", -90)
            cmds.makeIdentity("proxy_geo", t=0, r=1, s=0, apply=True)

        # delete old proxy geo
        cmds.delete(self.name + "_proxy_geo")
        proxy = cmds.rename("proxy_geo", self.name + "_proxy_geo")

        cmds.setAttr(proxy + ".overrideEnabled", True, lock=True)
        cmds.setAttr(proxy + ".overrideDisplayType", 2)

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
    def changeControlShape(self, *args):
        """
        Changes the control shape of the joint movers. Since the control shapes are used for the rig controls, this is
        to pick a contrrol shape that better fits the object.
        """

        currentSelection = cmds.ls(sl=True)

        # get new proxy geo value from comboBox
        newShape = self.controlShapeType.currentText()

        # construct the path
        path = os.path.join(self.toolsPath, "Core/JointMover/controls/")
        fullPath = os.path.join(path, "shape_" + newShape + ".ma")
        fullPath = utils.returnFriendlyPath(fullPath)

        # import the file
        cmds.file(fullPath, i=True, iv=True, type="mayaAscii", rnn=True)

        # replace the shape node of each mover with the new ones from the file
        for mover in ["_mover", "_mover_offset", "_mover_geo"]:

            if self.up == "y":
                cmds.setAttr("shape_curve" + mover + ".rotateX", -90)
                cmds.makeIdentity("shape_curve" + mover, t=1, r=1, s=1, apply=True)

            newMoverShape = cmds.listRelatives("shape_curve" + mover, children=True)[0]

            cmds.parent(newMoverShape, self.name + mover, r=True, shape=True)
            cmds.delete(self.name + mover + "Shape")
            cmds.rename(newMoverShape, self.name + mover + "Shape")

            cmds.delete("shape_curve" + mover)

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
    def changeButtonColor(self, animUI, button, border, control, color=None):
        """
        Leaf joints give the user the option to change the button's color. This function will remove the existing
        scriptJob, set the new button color, and create a new scriptJob with that information.

        :param animUI: The animation UI instance
        :param button: The button whose color we wish to set.
        :param border: The border item of the button that holds the scriptJob number to kill
        :param control: The control this button selects.
        """

        # launch a color dialog to  get a new color
        if color is None:
            newColor = QtWidgets.QColorDialog.getColor()
        else:
            newColor = color

        # delete the existing scriptJob
        scriptJob = border.data(5)
        cmds.scriptJob(kill=scriptJob)
        animUI.selectionScriptJobs.remove(scriptJob)

        # set the button color
        button.brush.setColor(newColor)

        # create the new scriptJob
        scriptJob = cmds.scriptJob(event=["SelectionChanged", partial(self.selectionScriptJob_animUI,
                                                                      [[button, control, newColor]])],
                                   kws=True)
        border.setData(5, scriptJob)
        animUI.selectionScriptJobs.append(scriptJob)

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

        # this shit right here is so hacky. For some reason, paste and reset have to run multiple times to get
        # everything
        # and I haven't taken the time to figure out why
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
                        try:
                            attrType = str(cmds.getAttr(networkNode + "." + attr, type=True))

                            if attrType != "string":
                                cmds.setAttr(networkNode + "." + attr, lock=False)
                                cmds.setAttr(networkNode + "." + attr, value, lock=True)

                            if attr == "customAttrs":
                                cmds.setAttr(networkNode + "." + attr, lock=False)
                                try:
                                    cmds.setAttr(networkNode + "." + attr, value, type="string", lock=True)
                                except:
                                    pass
                        except:
                            pass

                    # relaunch the UI
                    self.updateSettingsUI()
                    self.applyModuleChanges(self)
            else:
                cmds.warning("No data in clipboard")

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
    def removeCustomAttr(self):
        """
        Removes any custom attributes that were added via skeletonSettingsUI.
        """

        selected = self.customAttrsList.currentRow()
        selectedText = json.loads(self.customAttrsList.item(selected).text())
        self.customAttrsList.takeItem(selected)

        # remove custom attr info from network node attr
        networkNode = self.returnNetworkNode
        newList = []

        if cmds.objExists(networkNode + ".customAttrs"):

            data = json.loads(cmds.getAttr(networkNode + ".customAttrs"))

            if selectedText in data:
                for each in data:
                    if each != selectedText:
                        newList.append(each)

                jsonString = json.dumps(newList)
                cmds.setAttr(networkNode + ".customAttrs", lock=False)
                cmds.setAttr(networkNode + ".customAttrs", jsonString, type="string", lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def customAttr_UI(self):
        """
        A UI that allows users to create custom attributes in the skeleton settings UI for the leaf joint module. These
        custom attrs could then drive or be driven by other things in a post-script.
        :return:
        """

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")

        if cmds.window("pyART_customAttr_UI_Win", exists=True):
            cmds.deleteUI("pyART_customAttr_UI_Win", wnd=True)

        # create window
        self.custAttr_mainWin = QtWidgets.QMainWindow(self.rigUiInst)
        self.custAttr_mainWin.setMinimumSize(300, 180)
        self.custAttr_mainWin.setMaximumSize(300, 180)
        self.custAttr_mainWin.setWindowTitle("Add Attribute")
        self.custAttr_mainWin.setStyleSheet(self.style)
        self.custAttr_mainWin.setObjectName("pyART_customAttr_UI_Win")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.custAttr_mainWin.setWindowIcon(window_icon)

        # frame and layout
        self.custAttr_frame = QtWidgets.QFrame()
        self.custAttr_mainWin.setCentralWidget(self.custAttr_frame)

        mainLayout = QtWidgets.QVBoxLayout(self.custAttr_frame)

        # attribute name
        nameLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(nameLayout)

        label = QtWidgets.QLabel("Attribute Name:")
        label.setStyleSheet("background: transparent;")
        nameLayout.addWidget(label)

        self.custAttr_attrName = QtWidgets.QLineEdit()
        nameLayout.addWidget(self.custAttr_attrName)

        # attribute type
        typeLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(typeLayout)

        label = QtWidgets.QLabel("Attribute Type:")
        label.setStyleSheet("background: transparent;")
        typeLayout.addWidget(label)

        self.custAttr_attrType = QtWidgets.QComboBox()
        typeLayout.addWidget(self.custAttr_attrType)

        self.custAttr_attrType.addItem("Float")
        self.custAttr_attrType.addItem("Bool")
        self.custAttr_attrType.currentIndexChanged.connect(self._customAttr_UI_attrType)

        # min/max/default
        valueLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(valueLayout)

        self.custAttr_minField = QtWidgets.QLineEdit()
        self.custAttr_minField.setPlaceholderText("Min")
        valueLayout.addWidget(self.custAttr_minField)

        self.custAttr_maxField = QtWidgets.QLineEdit()
        self.custAttr_maxField.setPlaceholderText("Max")
        valueLayout.addWidget(self.custAttr_maxField)

        self.custAttr_defaultField = QtWidgets.QLineEdit()
        self.custAttr_defaultField.setPlaceholderText("Default")
        valueLayout.addWidget(self.custAttr_defaultField)

        # Ok/Cancel buttons
        buttonLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        self.custAttr_AcceptBTN = QtWidgets.QPushButton("Accept")
        buttonLayout.addWidget(self.custAttr_AcceptBTN)
        self.custAttr_AcceptBTN.setObjectName("settings")
        self.custAttr_AcceptBTN.clicked.connect(self.customAttr_UI_Accept)
        self.custAttr_AcceptBTN.setMinimumHeight(30)
        self.custAttr_AcceptBTN.setMaximumHeight(30)

        self.custAttr_CancelBTN = QtWidgets.QPushButton("Cancel")
        buttonLayout.addWidget(self.custAttr_CancelBTN)
        self.custAttr_CancelBTN.setObjectName("settings")
        self.custAttr_CancelBTN.setMinimumHeight(30)
        self.custAttr_CancelBTN.setMaximumHeight(30)
        self.custAttr_CancelBTN.clicked.connect(self.custAttr_mainWin.close)

        # show window
        self.custAttr_mainWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _customAttr_UI_attrType(self):

        if self.custAttr_attrType.currentText() == "Float":
            self.custAttr_minField.setVisible(True)
            self.custAttr_maxField.setVisible(True)

        if self.custAttr_attrType.currentText() == "Bool":
            self.custAttr_minField.setVisible(False)
            self.custAttr_maxField.setVisible(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def customAttr_UI_Accept(self):
        """
        Adds the custom attribute to the module's metaData so it will be created during the rig build.
        """

        # data list
        data = []
        networkNode = self.returnNetworkNode

        # get name
        name = self.custAttr_attrName.text()
        try:
            existingData = json.loads(cmds.getAttr(networkNode + ".customAttrs"))

            # double check that name is valid and doesn't already exist
            for each in existingData:
                if isinstance(each, list):
                    attrName = each[0]
                    if attrName == name:
                        cmds.warning("Attribute with given name already exists on this module.")
                        return
                else:
                    attrName = existingData[0]
                    if attrName == name:
                        cmds.warning("Attribute with given name already exists on this module.")
                        return
        except:
            pass

        data.append(name)

        # get type
        type = self.custAttr_attrType.currentText()
        data.append(type)

        if type == "Float":

            # get min/max
            minValue = self.custAttr_minField.text()
            maxValue = self.custAttr_maxField.text()

            if minValue != "" and maxValue != "":
                # validate
                try:
                    minValue = float(minValue)
                    maxValue = float(maxValue)

                    if minValue > maxValue:
                        cmds.warning("Min Value cannot be larger than the maximum value")
                        return

                except:
                    cmds.warning("Min or Max contain non-integers")
                    return

            data.append(minValue)
            data.append(maxValue)

        # get default
        defaultValue = self.custAttr_defaultField.text()

        try:
            defaultValue = float(defaultValue)

            if type == "Float":
                if minValue != "" and maxValue != "":
                    if defaultValue > maxValue or defaultValue < minValue:
                        cmds.warning("Default value not in range")
                        return

            if type == "Bool":
                if defaultValue > 1 or defaultValue < 0:
                    cmds.warning("Default value must be a 0 or 1")
                    return
        except:
            cmds.warning("Default value is a non-integer.")
            return

        data.append(defaultValue)

        # close UI
        cmds.deleteUI("pyART_customAttr_UI_Win", wnd=True)

        jsonString = json.dumps(data)

        # add to list
        self.customAttrsList.addItem(jsonString)

        # add to network node, get existing value
        newList = []
        try:
            existingData = json.loads(cmds.getAttr(networkNode + ".customAttrs"))
            if len(existingData) > 0:
                if isinstance(existingData[0], list):
                    for each in existingData:
                        newList.append(each)
        except:
            pass

        newList.append(data)
        jsonString = json.dumps(newList)
        cmds.setAttr(networkNode + ".customAttrs", lock=False)
        cmds.setAttr(networkNode + ".customAttrs", jsonString, type="string", lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectSettings(self, namespace):
        """
        selects the rig settings node for the leaf module.
        :param namespace: namespace of the asset.
        """
        cmds.select(namespace + self.name + "_settings")
