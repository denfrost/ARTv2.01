"""
Author: Jeremy Ernst

    This is the base class from which all modules are created. When creating a new module,
    your module class should inherit from this base class. Example:

|        class ART_Head(ART_RigModule)

    In the __init__ of your module class, you will want to also run the base class __init__
    at the end of your module class __init__:

|        ART_RigModule.__init__(self, "ART_Head_Module", "ART_Head", moduleUserName)

    This module has two file attributes set by default. Your module class will need many more
    file attributes set. Please see another module as an example.

########
Contents
########

|   **Module Creation Functions:**
|       :func:`addAttributes <RigModules.Base.ART_RigModule.ART_RigModule.addAttributes>`
|       :func:`buildNetwork <RigModules.Base.ART_RigModule.ART_RigModule.buildNetwork>`
|       :func:`createMirrorModule <RigModules.Base.ART_RigModule.ART_RigModule.createMirrorModule>`
|       :func:`jointMover_Build <RigModules.Base.ART_RigModule.ART_RigModule.jointMover_Build>`
|       :func:`skeletonSettings_UI <RigModules.Base.ART_RigModule.ART_RigModule.skeletonSettings_UI>`
|
|   **Module Update Functions:**
|       :func:`applyModuleChanges <RigModules.Base.ART_RigModule.ART_RigModule.applyModuleChanges>`
|       :func:`checkForDependencies <RigModules.Base.ART_RigModule.ART_RigModule.checkForDependencies>`
|       :func:`deleteModule <RigModules.Base.ART_RigModule.ART_RigModule.deleteModule>`
|
|   **Module Settings and Interface Functions:**
|       :func:`applyTemplate <RigModules.Base.ART_RigModule.ART_RigModule.applyTemplate>`
|       :func:`changeModuleName <RigModules.Base.ART_RigModule.ART_RigModule.changeModuleName>`
|       :func:`changeModuleParent <RigModules.Base.ART_RigModule.ART_RigModule.changeModuleParent>`
|       :func:`copySettings <RigModules.Base.ART_RigModule.ART_RigModule.copySettings>`
|       :func:`pasteSettings <RigModules.Base.ART_RigModule.ART_RigModule.pasteSettings>`
|       :func:`resetSettings <RigModules.Base.ART_RigModule.ART_RigModule.resetSettings>`
|       :func:`createContextMenu <RigModules.Base.ART_RigModule.ART_RigModule.createContextMenu>`
|       :func:`createMirrorOfModule_UI <RigModules.Base.ART_RigModule.ART_RigModule.createMirrorOfModule_UI>`
|       :func:`createScriptJob <RigModules.Base.ART_RigModule.ART_RigModule.createScriptJob>`
|       :func:`mirrorTransformations <RigModules.Base.ART_RigModule.ART_RigModule.mirrorTransformations>`
|       :func:`mirrorTransformations_Custom <RigModules.Base.ART_RigModule.ART_RigModule.mirrorTransformations_Custom>`
|       :func:`resetTransforms <RigModules.Base.ART_RigModule.ART_RigModule.resetTransforms>`
|       :func:`setMirrorModule <RigModules.Base.ART_RigModule.ART_RigModule.setMirrorModule>`
|       :func:`updateBoneCount <RigModules.Base.ART_RigModule.ART_RigModule.updateBoneCount>`
|       :func:`updatePreview <RigModules.Base.ART_RigModule.ART_RigModule.updatePreview>`
|       :func:`updateSettingsUI <RigModules.Base.ART_RigModule.ART_RigModule.updateSettingsUI>`
|
|   **Module Joint Mover Functions:**
|       :func:`addJointMoverToOutliner <RigModules.Base.ART_RigModule.ART_RigModule.addJointMoverToOutliner>`
|       :func:`aimMode <RigModules.Base.ART_RigModule.ART_RigModule.aimMode>`
|       :func:`aimMode_Setup <RigModules.Base.ART_RigModule.ART_RigModule.aimMode_Setup>`
|       :func:`bakeOffsets <RigModules.Base.ART_RigModule.ART_RigModule.bakeOffsets>`
|       :func:`createGlobalMoverButton <RigModules.Base.ART_RigModule.ART_RigModule.createGlobalMoverButton>`
|       :func:`createMeshMoverButton <RigModules.Base.ART_RigModule.ART_RigModule.createMeshMoverButton>`
|       :func:`createOffsetMoverButton <RigModules.Base.ART_RigModule.ART_RigModule.createOffsetMoverButton>`
|       :func:`pinModule <RigModules.Base.ART_RigModule.ART_RigModule.pinModule>`
|       :func:`selectMover <RigModules.Base.ART_RigModule.ART_RigModule.selectMover>`
|       :func:`selectScriptJob <RigModules.Base.ART_RigModule.ART_RigModule.selectScriptJob>`
|       :func:`toggleShapeVis <RigModules.Base.ART_RigModule.ART_RigModule.toggleShapeVis>`
|       :func:`updateOutliner <RigModules.Base.ART_RigModule.ART_RigModule.updateOutliner>`
|
|   **Module Publish Functions:**
|       :func:`cleanUpRigPose <RigModules.Base.ART_RigModule.ART_RigModule.cleanUpRigPose>`
|       :func:`createRigPoseSliderForJoint <RigModules.Base.ART_RigModule.ART_RigModule.createRigPoseSliderForJoint>`
|       :func:`getReferencePose <RigModules.Base.ART_RigModule.ART_RigModule.getReferencePose>`
|       :func:`matchModelPose <RigModules.Base.ART_RigModule.ART_RigModule.matchModelPose>`
|       :func:`mirrorTransformations_RigPose <RigModules.Base.ART_RigModule.ART_RigModule.mirrorTransformations_RigPose>`
|       :func:`resetRigPose <RigModules.Base.ART_RigModule.ART_RigModule.resetRigPose>`
|       :func:`resetRigPose_Part <RigModules.Base.ART_RigModule.ART_RigModule.resetRigPose_Part>`
|       :func:`rigPose_UI <RigModules.Base.ART_RigModule.ART_RigModule.rigPose_UI>`
|       :func:`setPosePercentage <RigModules.Base.ART_RigModule.ART_RigModule.setPosePercentage>`
|       :func:`setPosePercentage_Part <RigModules.Base.ART_RigModule.ART_RigModule.setPosePercentage_Part>`
|       :func:`setReferencePose <RigModules.Base.ART_RigModule.ART_RigModule.setReferencePose>`
|       :func:`setReferencePoseSlider <RigModules.Base.ART_RigModule.ART_RigModule.setReferencePoseSlider>`
|       :func:`setSkeletonPose <RigModules.Base.ART_RigModule.ART_RigModule.setSkeletonPose>`
|       :func:`setupForRigPose <RigModules.Base.ART_RigModule.ART_RigModule.setupForRigPose>`
|       :func:`setupModelPoseForRig <RigModules.Base.ART_RigModule.ART_RigModule.setupModelPoseForRig>`
|       :func:`skinProxyGeo <RigModules.Base.ART_RigModule.ART_RigModule.skinProxyGeo>`
|       :func:`updateRigPose <RigModules.Base.ART_RigModule.ART_RigModule.updateRigPose>`
|
|   **Module Rig Functions**
|       :func:`buildRig <RigModules.Base.ART_RigModule.ART_RigModule.buildRig>`
|       :func:`buildRigCustom <RigModules.Base.ART_RigModule.ART_RigModule.buildRigCustom>`
|       :func:`deleteRig <RigModules.Base.ART_RigModule.ART_RigModule.deleteRig>`
|       :func:`getControls <RigModules.Base.ART_RigModule.ART_RigModule.getControls>`
|       :func:`importFBX <RigModules.Base.ART_RigModule.ART_RigModule.importFBX>`
|       :func:`importFBX_pre <RigModules.Base.ART_RigModule.ART_RigModule.importFBX_pre>`
|       :func:`resetRigControls <RigModules.Base.ART_RigModule.ART_RigModule.resetRigControls>`
|       :func:`selectRigControls <RigModules.Base.ART_RigModule.ART_RigModule.selectRigControls>`
|       :func:`selectionScriptJob_animUI <RigModules.Base.ART_RigModule.ART_RigModule.selectionScriptJob_animUI>`
|
|   **Module Utility Functions**
|       :func:`getAllModules <RigModules.Base.ART_RigModule.ART_RigModule.getAllModules>`
|       :func:`getModules <RigModules.Base.ART_RigModule.ART_RigModule.getModules>`
|       :func:`removeSkeletalConstraints <RigModules.Base.ART_RigModule.ART_RigModule.removeSkeletalConstraints>`
|       :func:`returnCreatedJoints <RigModules.Base.ART_RigModule.ART_RigModule.returnCreatedJoints>`
|       :func:`returnJointMovers <RigModules.Base.ART_RigModule.ART_RigModule.returnJointMovers>`
|       :func:`returnMirrorModuleInst <RigModules.Base.ART_RigModule.ART_RigModule.returnMirrorModuleInst>`
|       :func:`returnNetworkNode <RigModules.Base.ART_RigModule.ART_RigModule.returnNetworkNode>`
|       :func:`returnPrefixSuffix <RigModules.Base.ART_RigModule.ART_RigModule.returnPrefixSuffix>`
|       :func:`returnRigNetworkNode <RigModules.Base.ART_RigModule.ART_RigModule.returnRigNetworkNode>`
|
|
#########
Class
#########
"""

# file imports
import json
import os
from functools import partial
from decimal import *

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import Utilities.mathUtils as mathUtils
import Tools.System.Interfaces.ART_SimpleChooserDialog as choice_dialog

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# file attributes
fbxImport = ["None", "FK"]
matchData = [False, None]


class ART_RigModule():
    """
    Modules Base Class
    """
    def __init__(self, moduleName, moduleType, userCreatedName):
        """Initiate the class, taking in the instance to the interface and the user specified name.

        :param moduleName: This is the base name of the module, specified in the rig module.
        :param moduleType: This is the name of the module to create (the module class).
        :param userCreatedName: This is the name specified by the user on module creation.

        Instantiate the following class variables as well:
            * **self.modName:** Take the passed in moduleName and make it a class var
            * **self.moduleType:** Take the passed in moduleType and make it a class var
            * **self.rootMod:** The network node of the entire character asset
            * **self.name:** The user created name (prefix +  baseName + suffix) passed in
            * **self.originalName:** Also the user created name, but we want to store what the original name
              was on creation, as the user can rename the module later. This will allow us to make the link between
              what the module's original name was and what the new name is.
            * **self.outlinerControls:** A list of the outliner controls created when adding module joint movers to
              the outliner.

        Also, read the QSettings to find out where needed paths are.
        """

        # set class variables
        self.modName = moduleName
        self.moduleType = moduleType
        self.rootMod = None
        self.name = userCreatedName
        self.originalName = userCreatedName
        self.outlinerControls = []
        self.controlTypes = []

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # get the up-axis
        self.up = cmds.upAxis(q=True, ax=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildNetwork(self):
        """
        Build the network node for the module which will store all information needed by the module.
        Then, call on addAttributes to add the required module attributes to the network node.
        """

        # create the network node for our module
        self.networkNode = cmds.createNode("network", name=self.modName)

        # create attributes
        self.addAttributes()

        return self.networkNode

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addAttributes(self):
        """
        Add attributes to the network node that all modules need.
        """

        if self.moduleType is None:
            # add attributes specific to this module
            cmds.addAttr(self.networkNode, sn="rigModules", at="message")

        else:
            # add a rigging message attribute
            cmds.addAttr(self.networkNode, sn="parent", at="message")

            # add a module type attribute
            cmds.addAttr(self.networkNode, sn="moduleType", dt="string", keyable=False)
            cmds.setAttr(self.networkNode + ".moduleType", self.moduleType, type="string", lock=True)

            # and a module name attribute (used for skeleton settings UI groupbox label)
            cmds.addAttr(self.networkNode, sn="moduleName", dt="string", keyable=False)
            cmds.setAttr(self.networkNode + ".moduleName", self.name, type="string", lock=True)

            # add attr for parent module that user specfies
            cmds.addAttr(self.networkNode, sn="parentModuleBone", dt="string", keyable=False)

            # add attr for mirror module that user specfies
            cmds.addAttr(self.networkNode, sn="mirrorModule", dt="string", keyable=False)

            cmds.addAttr(self.networkNode, sn="pinned", at="bool", keyable=False)
            cmds.setAttr(self.networkNode + ".pinned", False, lock=True)

            # connect rigModule to root module node
            self.rootMod = self.getModules
            if self.rootMod is not None:
                cmds.connectAttr(self.rootMod + ".rigModules", self.networkNode + ".parent")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skeletonSettings_UI(self, name, width, height, checkable):
        """
        Build the framework for the skeleton settings that all modules need.

        :param name: user given name of module (prefix + base_name + suffix)
        :param width: width of the skeleton settings groupBox. 335 usually
        :param height: height of the skeleton settings groupBox.
        :param checkable: Whether or not the groupBox can be collapsed.
        """

        # add the groupbox for this module with the module name and module settings
        self.groupBox = QtWidgets.QGroupBox(name)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, width, height))
        self.groupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))

        if not checkable:
            self.groupBox.setMinimumSize(QtCore.QSize(width, height))

        if checkable:
            self.groupBox.setMinimumSize(QtCore.QSize(width, 0))

        self.groupBox.setMaximumSize(QtCore.QSize(width, height))
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(checkable)

        self.lockButton = QtWidgets.QPushButton()
        self.lockButton.setMinimumSize(QtCore.QSize(20, 20))
        self.lockButton.setMaximumSize(QtCore.QSize(20, 20))

        # load style sheet file
        style = interfaceUtils.get_style_sheet("artv2_style")
        self.groupBox.setStyleSheet(style)

        # set properties for filtering later
        self.groupBox.setObjectName(name)
        self.groupBox.setProperty("name", name)

        # set context menu policy on groupbox
        self.groupBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.groupBox.customContextMenuRequested.connect(self.createContextMenu)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeModuleName(self, baseName, moduleInst, rigUiInst):
        """
        Launch the interface that allows users to change the module name.

        :param baseName: The module base name (head, torso, leg, etc)
        :param moduleInst: The specific instance of the module
        :param rigUiInst: The instance of the rig creator interface.

        This will call on a separate class in Core/Tools called ART_ChangeModuleNameUI.py
        """

        # get prefix/suffix
        name = self.name
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        # when pressing the change name button on the skeleton settings UI (if it exists):

        # delete the UI if it already exists
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        if cmds.window(mayaWindow + "|pyArtChangeModuleNameUi", q=True, exists=True):
            cmds.deleteUI(mayaWindow + "|pyArtChangeModuleNameUi")

        # launch a UI for prefix/suffix/preview again
        import Tools.Rigging.ART_ChangeModuleNameUI as ART_ChangeModuleNameUI
        inst = ART_ChangeModuleNameUI.ART_ChangeModuleName_UI(baseName, moduleInst, rigUiInst, prefix, suffix,
                                                              interfaceUtils.getMainWindow())
        inst.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeModuleParent(self, moduleInst, rigUiInst):
        """
        Launch the interface that allows users to change the module's parent bone.

        :param moduleInst: The specific instance of the module
        :param rigUiInst: The instance of the rig creator interface.

        This will call on a separate class in Core/Tools called ART_ChangeModuleParentUI.py
        """

        # get current parent value
        currentParent = self.currentParent.text()

        # when pressing the change parent button on the skeleton settings UI (if it exists):

        # delete the UI if it already exists
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        if cmds.window(mayaWindow + "|pyArtChangeModuleParentUi", q=True, exists=True):
            cmds.deleteUI(mayaWindow + "|pyArtChangeModuleParentUi")

        # launch a UI for prefix/suffix/preview again
        import Tools.Rigging.ART_ChangeModuleParentUI as ART_ChangeModuleParentUI
        inst = ART_ChangeModuleParentUI.ART_ChangeModuleParent_UI(currentParent, moduleInst, rigUiInst,
                                                                  interfaceUtils.getMainWindow())
        inst.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setMirrorModule(self, moduleInst, rigUiInst):
        """
        Launch the interface that allows users to change the module's mirror module.
        Meaning, the module that is linked as a mirror of this module. Only modules of the same
        type can be linked as mirrors.

        :param moduleInst: The specific instance of the module
        :param rigUiInst: The instance of the rig creator interface.

        This will call on a separate class in Core/Tools called ART_SetMirrorModuleUI.py
        """

        # delete the UI if it already exists
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        if cmds.window(mayaWindow + "|pyArtSetMirrorModuleUi", q=True, exists=True):
            cmds.deleteUI(mayaWindow + "|pyArtSetMirrorModuleUi")

        # launch a UI for prefix/suffix/preview again
        import Tools.Rigging.ART_SetMirrorModuleUI as ART_SetMirrorModuleUI
        inst = ART_SetMirrorModuleUI.ART_SetMirrorModule_UI(moduleInst, rigUiInst, interfaceUtils.getMainWindow())
        inst.show()

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
                            print"jointMover_Build Error 1:"
                            print str(e)

                    for mover in movers:
                        try:
                            cmds.rename(mover, self.name + "_" + mover)
                        except Exception, e:
                            print"jointMover_Build Error 2:"
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
                print "jointMover_Build Error 3:"
                print str(e)
            globalMover = utils.findGlobalMoverFromName(self.name)
            cmds.select(globalMover)
            cmds.setToolTo("moveSuperContext")

            # obey visibility toggles
            self.rigUiInst.setMoverVisibility()

            # 1/13/16 Change # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
                self.lock_nodes()

            except Exception:
                pass

                # 1/13/16 Change # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        else:
            cmds.confirmDialog(title="Joint Mover", message="Could not find associated joint mover file.",
                               icon="critical")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectScriptJob(self, info):
        """
        Change icon color of the given joint mover's button in the outliner to show selection status.

        :param info: This list contains the button object, the joint mover control, and the original color icon.

        If the control given is selected, the icon is switched to a white icon. If it is not selected, the icon
        is set back to the original passed in icon.
        """

        pixmap = QtGui.QPixmap(20, 15)
        pixmap.fill(QtGui.QColor(255, 255, 255))
        whiteIcon = QtGui.QIcon(pixmap)

        # for each item in the passed in info [outliner button, mover control, unselected stylesheet],check if
        # the control is in the selection, and color the button appropriately
        for item in info:
            button = item[0]
            control = item[1]
            icon = item[2]

            selected = cmds.ls(selection=True)
            if control not in selected:
                self.outlinerWidgets[button].setIcon(icon)

            if control in selected:
                self.outlinerWidgets[button].setIcon(whiteIcon)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createGlobalMoverButton(self, name, parent, uiInstance):
        """
        Create the button in the outliner for the global mover control of a joint mover.

        :param name: The name of the joint mover control.
        :param parent: The outliner widget the created button will be parented to.
        :param uiInstance: The Rig Creator interface instance.
        """

        part = name.partition(self.name)[2]

        # create the icon
        pixmap = QtGui.QPixmap(20, 15)
        pixmap.fill(QtGui.QColor("yellow"))
        icon = QtGui.QIcon(pixmap)

        # create the button
        self.outlinerWidgets[name + "_globalMoverBtn"] = QtWidgets.QPushButton(icon, "")
        self.outlinerWidgets[name + "_globalMoverBtn"].setMinimumSize(QtCore.QSize(20, 15))
        self.outlinerWidgets[name + "_globalMoverBtn"].setMaximumSize(QtCore.QSize(20, 15))
        uiInstance.treeWidget.setItemWidget(parent, 1, self.outlinerWidgets[name + "_globalMoverBtn"])

        # connect and add to list
        self.outlinerWidgets[name + "_globalMoverBtn"].clicked.connect(
            partial(self.selectMover, part, True, False, False, self.outlinerWidgets[name + "_globalMoverBtn"]))
        self.outlinerControls.append([name + "_globalMoverBtn", name + "_mover", icon])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createOffsetMoverButton(self, name, parent, uiInstance):
        """
        Create the button in the outliner for the offset mover control of a joint mover.

        :param name: The name of the joint mover control.
        :param parent: The outliner widget the created button will be parented to.
        :param uiInstance: The Rig Creator interface instance.
        """
        part = name.partition(self.name)[2]

        # create the icon
        pixmap = QtGui.QPixmap(20, 15)
        pixmap.fill(QtGui.QColor(100, 200, 255))
        icon = QtGui.QIcon(pixmap)

        # create the button
        self.outlinerWidgets[name + "_offsetMoverBtn"] = QtWidgets.QPushButton(icon, "")
        self.outlinerWidgets[name + "_offsetMoverBtn"].setMinimumSize(QtCore.QSize(20, 15))
        self.outlinerWidgets[name + "_offsetMoverBtn"].setMaximumSize(QtCore.QSize(20, 15))
        uiInstance.treeWidget.setItemWidget(parent, 2, self.outlinerWidgets[name + "_offsetMoverBtn"])

        # connect and add to list
        self.outlinerWidgets[name + "_offsetMoverBtn"].clicked.connect(
            partial(self.selectMover, part, False, True, False, self.outlinerWidgets[name + "_offsetMoverBtn"]))
        self.outlinerControls.append([name + "_offsetMoverBtn", name + "_mover_offset", icon])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createMeshMoverButton(self, name, parent, uiInstance):
        """
        Create the button in the outliner for the geometry mover control of a joint mover.

        :param name: The name of the joint mover control.
        :param parent: The outliner widget the created button will be parented to.
        :param uiInstance: The Rig Creator interface instance.

        Note: The geometry mover is purely for aesthetics and does not affect the rigging.
        """

        part = name.partition(self.name)[2]

        # create the icon
        pixmap = QtGui.QPixmap(20, 15)
        pixmap.fill(QtGui.QColor(255, 176, 176))
        icon = QtGui.QIcon(pixmap)

        # create the button
        self.outlinerWidgets[name + "_geoMoverBtn"] = QtWidgets.QPushButton(icon, "")
        self.outlinerWidgets[name + "_geoMoverBtn"].setMinimumSize(QtCore.QSize(20, 15))
        self.outlinerWidgets[name + "_geoMoverBtn"].setMaximumSize(QtCore.QSize(20, 15))
        uiInstance.treeWidget.setItemWidget(parent, 3, self.outlinerWidgets[name + "_geoMoverBtn"])

        # connect and add to list
        self.outlinerWidgets[name + "_geoMoverBtn"].clicked.connect(
            partial(self.selectMover, part, False, False, True, self.outlinerWidgets[name + "_geoMoverBtn"]))
        self.outlinerControls.append([name + "_geoMoverBtn", name + "_mover_geo", icon])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createScriptJob(self):
        """
        Create the selection script job for the outliner buttons and their associated joint mover controls.

        This function purely creates the script job. The script job function that is run is called self.selectScriptJob.
        """

        self.scriptJob = cmds.scriptJob(
            event=["SelectionChanged", partial(self.selectScriptJob, self.outlinerControls)], runOnce=False,
            parent="pyArtRigCreatorUi", kws=True, per=False)
        self.rigUiInst.scriptJobs.append(self.scriptJob)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectMover(self, part, globalMover, offsetMover, geoMover, button):
        """
        Select the appropriate joint mover control based on the args passed in. Color the associated button white
        to show selection status.

        :param part: The name of the joint mover control.
        :param globalMover: Boolean of whether or not given control is a global mover.
        :param offsetMover: Boolean of whether or not given control is an offset mover.
        :param geoMover:  Boolean of whether or not given control is a mesh mover.
        :param button: The button in the outliner associated with the given mover.
        """

        # select mover and color button
        name = self.name + part
        print name

        # get modifiers
        toggle = False
        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            toggle = True

        if globalMover:
            cmds.select(name + "_mover", tgl=toggle)

            selected = cmds.ls(sl=True)
            if name + "_mover" in selected:
                button.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                button.setStyleSheet('background-color: rgb(255, 255, 0);')

        if offsetMover:
            cmds.select(name + "_mover_offset", tgl=toggle)

            selected = cmds.ls(sl=True)
            if name + "_mover_offset" in selected:
                self.outlinerWidgets[name + "_offsetMoverBtn"].setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                self.outlinerWidgets[name + "_offsetMoverBtn"].setStyleSheet('background-color: rgb(100, 220, 255);')

        if geoMover:
            cmds.select(name + "_mover_geo", tgl=toggle)

            selected = cmds.ls(sl=True)
            if name + "_mover_geo" in selected:
                self.outlinerWidgets[name + "_geoMoverBtn"].setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                self.outlinerWidgets[name + "_geoMoverBtn"].setStyleSheet('background-color: rgb(255, 176, 176);')

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

        Default menu actions created:
            * Copy Settings
            * Paste Settings
            * Reset Settings
            * Delete Module
            * Create Mirror of this Module
            * Mirror Transformations (only if a mirror is linked)
        """

        networkNode = self.returnNetworkNode
        mirror = cmds.getAttr(networkNode + ".mirrorModule")

        # icons
        icon_copy = QtGui.QIcon(os.path.join(self.iconsPath, "System/copy.png"))
        icon_paste = QtGui.QIcon(os.path.join(self.iconsPath, "System/paste.png"))
        icon_reset = QtGui.QIcon(os.path.join(self.iconsPath, "System/reset.png"))
        icon_delete = QtGui.QIcon(os.path.join(self.iconsPath, "System/delete.png"))
        icon_mirror = QtGui.QIcon(os.path.join(self.iconsPath, "System/mirrorXforms.png"))
        icon_createMirror = QtGui.QIcon(os.path.join(self.iconsPath, "System/createMirror.png"))
        icon_duplicate = QtGui.QIcon(os.path.join(self.iconsPath, "System/duplicate.png"))

        # create the context menu
        if networkNode != "ART_Root_Module":
            self.contextMenu = QtWidgets.QMenu()
            self.contextMenu.addAction(icon_copy, "Copy Settings", self.copySettings)
            self.contextMenu.addAction(icon_paste, "Paste Settings", self.pasteSettings)
            self.contextMenu.addAction(icon_reset, "Reset Settings", self.resetSettings)

            self.contextMenu.addSeparator()
            if mirror is not None:
                self.contextMenu.addAction(icon_mirror, "Mirror Transformations to " + mirror,
                                           self.mirrorTransformations)

            self.contextMenu.addAction(icon_createMirror, "Create Mirror of this Module",
                                       partial(self.createMirrorOfModule_UI, "ART_createMirrorModuleUI",
                                               "Create Mirror Module", "CREATE"))

            self.contextMenu.addAction(icon_duplicate, "Duplicate this Module",
                                       partial(self.createMirrorOfModule_UI, "ART_createDuplicateModuleUI",
                                               "Duplicate Module", "DUPLICATE", False, True))

            self.contextMenu.addSeparator()

            self.contextMenu.addAction(icon_delete, "Delete Module", self.deleteModule)
            self.contextMenu.exec_(self.groupBox.mapToGlobal(point))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def lock_nodes(self, lock=True):
        """
        Lock or unlock nodes.
        :param lock: Whether to lock or unlock.
        """

        movers = self.returnJointMovers
        for mover_type in movers:
            for mover in mover_type:
                cmds.lockNode(mover, lock=lock)

                # cmds.select(mover, hi=True)
                # children = cmds.ls(sl=True)
                # for child in children:
                #     cmds.lockNode(child, lock=lock)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def copySettings(self):
        """
        Copy the values from the network node of the module and store them in a temp file on disk.

        This function is used in the right-click menu of the module on the skeleton settings interface.
        Occasionally, it is called outside of the menu. For example, when creating a mirror of the module,
        the settings are copied for the source module to then be later pasted on the mirror.
        """

        networkNode = self.returnNetworkNode
        attrs = cmds.listAttr(networkNode, ud=True, hd=True)

        attrData = []
        for attr in attrs:
            value = cmds.getAttr(networkNode + "." + attr)
            attrData.append([attr, value])

        # write out attrData to a temp file
        tempDir = cmds.internalVar(userTmpDir=True)
        clipboardFile = os.path.normcase(os.path.join(tempDir, "ART_clipboard.txt"))

        f = open(clipboardFile, 'w')

        # dump the data with json
        json.dump(attrData, f)
        f.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pasteTransforms(self):

        tempDir = cmds.internalVar(userTmpDir=True)
        clipboardFile = os.path.normcase(os.path.join(tempDir, "ART_clipboard2.txt"))

        if os.path.exists(clipboardFile):
            # load the data
            json_file = open(clipboardFile)
            data = json.load(json_file)
            json_file.close()

            descendants = cmds.listRelatives(self.name + "_mover_grp", children=True, type="transform", ad=True, f=True)
            voidTypes = ["aimConstraint", "scaleConstraint", "parentConstraint", "pointConstraint",
                         "orientConstraint"]
            validNodes = []

            for each in descendants:
                if cmds.nodeType(each) not in voidTypes:
                    validNodes.append(each.rpartition("|")[2])

            topMover = utils.findGlobalMoverFromName(self.name)

            for each in data:
                # name, index, attr, value
                try:
                    mover = validNodes[each[1]]
                    cmds.setAttr(mover + "." + each[2], each[3])
                    print "pasting transforms from " + each[0] + " to " + mover

                except Exception, e:
                    print "pasteTransforms Error:"
                    print e

            cmds.select(topMover)

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

                        try:
                            attrType = str(cmds.getAttr(networkNode + "." + attr, type=True))

                            if attrType != "string":
                                cmds.setAttr(networkNode + "." + attr, lock=False)
                                cmds.setAttr(networkNode + "." + attr, value, lock=True)
                        except Exception, e:
                            print "Paste Settings Error: " + str(e)

            else:
                cmds.warning("No data in clipboard")

        # relaunch the UI
        self.updateSettingsUI()
        self.applyModuleChanges(self)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetSettings(self):
        """
        Reset the settings of the module's network node.

        This function is used in the right-click menu of the module on the skeleton settings interface.
        Occasionally, it is called outside of the menu.

        After settings are reset, applyModuleChanges is called to update the joint mover in the scene with
        the latest values. updateSettingsUI is also called to update the outliner.
        """

        # it does this 4 times because for some reason it would not grab everything one time through. Investigate
        for i in range(4):

            networkNode = self.returnNetworkNode
            attrs = cmds.listAttr(networkNode, ud=True)

            for attr in attrs:
                attrType = str(cmds.getAttr(networkNode + "." + attr, type=True))

                if attrType == "double":
                    cmds.setAttr(networkNode + "." + attr, lock=False)
                    cmds.setAttr(networkNode + "." + attr, 0, lock=True)

                if attrType == "bool":
                    cmds.setAttr(networkNode + "." + attr, lock=False)
                    cmds.setAttr(networkNode + "." + attr, True, lock=True)

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
    def applyTemplate(self, data, networkNode):
        """
        Takes the input data, and sets attributes on the given network node using that data. This input data comes
        from a template file that stores settings for modules as well as positional data for the joint movers
        of a module. This method only deals with the settings and not the positional data.

        :param data: list of data comprising of attributes and their values.
        :param networkNode: The network node that will be checked for those attributes, then have thier values set from
                            the data.

        """

        # set the attributes on the network node
        for attr in data:
            value = data.get(attr)

            try:
                attrType = str(cmds.getAttr(networkNode + "." + attr, type=True))
                cmds.setAttr(networkNode + "." + attr, lock=False)
                if attrType == "string":
                    cmds.setAttr(networkNode + "." + attr, value, type=attrType, lock=True)
                else:
                    cmds.setAttr(networkNode + "." + attr, value, lock=True)

            except Exception:
                print attr, value

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetTransforms(self, translate, rotate, scale, name):
        """
        Reset the given attributes of all movers in the module.

        :param translate: Boolean of whether or not to reset translation values.
        :param rotate: Boolean of whether or not to reset the rotation values.
        :param scale: Boolean of whether or not to reset the scale values.
        :param name: The module name. (prefix +  basename + suffix)

        This function is mainly called from ART_ResetModeUI.

        """

        cmds.select(name + "_mover_grp", hi=True)
        selection = cmds.ls(sl=True)

        globalMovers = []
        offsetMovers = []
        geoMovers = []

        for each in selection:
            if each.find("_mover") != -1:
                if each.partition("_mover")[2] == "":
                    globalMovers.append(each)
            if each.find("_mover_offset") != -1:
                if each.partition("_mover_offset")[2] == "":
                    offsetMovers.append(each)
            if each.find("_mover_geo") != -1:
                if each.partition("_mover_geo")[2] == "":
                    geoMovers.append(each)

        cmds.select(clear=True)

        for moverList in [globalMovers, offsetMovers, geoMovers]:
            for each in moverList:
                if translate:
                    for attr in [".tx", ".ty", ".tz"]:
                        try:
                            cmds.setAttr(each + attr, 0)
                        except:
                            pass
                if rotate:
                    for attr in [".rx", ".ry", ".rz"]:
                        try:
                            cmds.setAttr(each + attr, 0)
                        except:
                            pass
                if scale:
                    for attr in [".sx", ".sy", ".sz"]:
                        try:
                            cmds.setAttr(each + attr, 1)
                        except:
                            pass
        if cmds.window("ART_ResetXformsModeWin", exists=True):
            cmds.deleteUI("ART_ResetXformsModeWin", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def deleteModule(self):
        """
        Delete the module and all associated nodes and interfaces.

        First, this will delete the joint mover, remove the entry from the outliner and the skeleton settings UI.
        Then, it has to deal with any connected modules or mirror modules and resolve any issues there.

        """

        # delete the joint mover
        self.lock_nodes(lock=False)
        cmds.delete(self.name + "_mover_grp")

        # remove the entry from the outliner
        index = self.rigUiInst.treeWidget.indexOfTopLevelItem(self.outlinerWidgets[self.name + "_treeModule"])
        self.rigUiInst.treeWidget.takeTopLevelItem(index)

        # remove the groupbox
        self.groupBox.setParent(None)

        # deal with mirror module
        networkNode = self.returnNetworkNode
        mirrorModule = cmds.getAttr(networkNode + ".mirrorModule")
        if mirrorModule != None:
            if mirrorModule != "None":
                modules = utils.returnRigModules()
                for mod in modules:
                    modName = cmds.getAttr(mod + ".moduleName")
                    if modName == mirrorModule:

                        # set the mirrored version
                        cmds.setAttr(mod + ".mirrorModule", lock=False)
                        cmds.setAttr(mod + ".mirrorModule", "None", type="string", lock=True)

                        # get instance of mirror module's class
                        modType = cmds.getAttr(mod + ".moduleType")
                        modName = cmds.getAttr(mod + ".moduleName")
                        module = __import__("RigModules." + modType, {}, {}, [modType])

                        # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
                        moduleClass = getattr(module, module.className)

                        # find the instance of that module and call on the skeletonSettings_UI function
                        moduleInst = moduleClass(self.rigUiInst, modName)

                        # find the current groupBox for this module
                        for i in range(self.rigUiInst.moduleSettingsLayout.count()):
                            if type(self.rigUiInst.moduleSettingsLayout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                                if self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().title() == modName:
                                    self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().setParent(None)

                                    # relaunch the skeleton settings UI with new info
                                    moduleInst.skeletonSettings_UI(modName)

        # check for any attached modules
        attachedModules = self.checkForDependencies()
        elementList = []
        if len(attachedModules) > 0:

            for each in attachedModules:
                elementList.append([each[2], "  -> parent changed from:  ", each[1], "  to:  ", "root\n"])
                cmds.parent(each[2] + "_mover_grp", "root_mover")
                cmds.setAttr(each[0] + ".parentModuleBone", lock=False)
                cmds.setAttr(each[0] + ".parentModuleBone", "root", type="string", lock=True)
                each[3].currentParent.setText("root")
                mover = "root_mover"

                # create the connection geo between the two
                each[3].applyModuleChanges(each[3])
                cmds.select(clear=True)

        # remove the network node
        cmds.delete(networkNode)

        # delete scriptJob
        try:
            cmds.scriptJob(kill=self.scriptJob, force=True)
        except AttributeError:
            pass
        self.updateBoneCount()
        self.rigUiInst.moduleInstances.remove(self)

        # warn user about changes
        if len(attachedModules) > 0:
            winParent = interfaceUtils.getMainWindow()
            win = interfaceUtils.DialogMessage("Attention!",
                                               "The following modules have had their parent changed\
                                               due to the change in this module's structure:",
                                               elementList, 5, winParent)
            win.show()

        # refresh UI
        import Tools.Rigging.ART_RigCreatorUI as rigCreator
        rigCreator.createUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def checkForDependencies(self):
        """
        This method will check modules for any attached modules or children modules.

        This method is generally called when deleting a module or when changing a module name
        so that any connected modules are updated accordingly.

        :return: attached modules

        """

        # This method will check our module for any attached modules
        modules = self.getAllModules
        joints = self.returnCreatedJoints

        attachedMods = []
        instances = {}

        for inst in self.rigUiInst.moduleInstances:
            networkNode = inst.returnNetworkNode
            instances[networkNode] = inst

        for module in modules:
            parentJoint = cmds.getAttr(module + ".parentModuleBone")
            moduleName = cmds.getAttr(module + ".moduleName")
            if parentJoint in joints:
                instance = instances.get(module)
                attachedMods.append([module, parentJoint, moduleName, instance])

        return attachedMods

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def fixDependencies(self, affectedMods):
        """
        Takes the input modules and sets their parent to be the root, as their current parent module is being deleted or
        changed in some way. Then show a window informing the user that the afffected modules have been reparented to
        the root.

        :param affectedMods: A list of modules that are affected by their parent module changing or being deleted.
        :return:

        """
        elementList = []

        # first set parent to root mover since it will always be there
        for each in affectedMods:
            elementList.append([each[2], "  -> parent changed from:  ", each[1], "  to:  ", "root\n"])
            currentParent = cmds.listRelatives(each[2] + "_mover_grp", parent=True)[0]
            if currentParent != "root_mover":
                cmds.parentConstraint("root_mover", each[2] + "_mover_grp", mo=True)
                cmds.scaleConstraint("root_mover", each[2] + "_mover_grp", mo=True)
                cmds.setAttr(each[0] + ".parentModuleBone", lock=False)
                cmds.setAttr(each[0] + ".parentModuleBone", "root", type="string", lock=True)

                # then, update settings UI for those dependency modules to display new parent info
                modules = self.getAllModules

                if each[0] in modules:
                    modName = cmds.getAttr(each[0] + ".moduleName")

                    for modInst in self.rigUiInst.moduleInstances:
                        if modInst.networkNode == each[0]:
                            # find the current groupBox for this module
                            for i in range(self.rigUiInst.moduleSettingsLayout.count()):
                                if type(self.rigUiInst.moduleSettingsLayout.itemAt(
                                        i).widget()) == QtWidgets.QGroupBox:
                                    if self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().title() == modName:
                                        self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().setParent(None)

                                        # relaunch the skeleton settings UI with new info
                                        modInst.skeletonSettings_UI(modName)

            # create the connection geo between the two
            mover = "root_mover"
            each[3].applyModuleChanges(each[3])
            cmds.select(clear=True)

        # warn user about changes
        winParent = interfaceUtils.getMainWindow()
        win = interfaceUtils.DialogMessage("Attention!", "The following modules have had their parent changed due\
                                            to the change in this module's structure:",
                                           elementList, 5, winParent)
        win.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createMirrorOfModule_UI(self, objectName, windowTitle, buttonLabel, mirror=True, duplicate=False):
        """
        This method builds the interface for creating a mirror of a module or a duplicate of a module.

        .. image:: /images/mirrorModule.png

        """

        # copy the settings of the module
        self.copySettings()
        self.copyTransforms()

        # get basename and classname
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")
        className = cmds.getAttr(networkNode + ".moduleType")

        # launch a UI to get the name information
        self.mirrorWindow = QtWidgets.QMainWindow()
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.mirrorWindow.setWindowIcon(window_icon)

        # load stylesheet
        style = interfaceUtils.get_style_sheet("artv2_style")
        self.mirrorWindow.setStyleSheet(style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mirrorWindow.setCentralWidget(self.mainWidget)

        # set qt object name
        self.mirrorWindow.setObjectName("artv2_create_dupe_win")
        self.mirrorWindow.setWindowTitle(windowTitle)

        # create the mainLayout for the rig creator UI
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mirrorWindow.resize(300, 150)
        self.mirrorWindow.setSizePolicy(mainSizePolicy)
        self.mirrorWindow.setMinimumSize(QtCore.QSize(300, 150))
        self.mirrorWindow.setMaximumSize(QtCore.QSize(300, 150))

        # create the background image
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        # create the prefix pair of fields
        self.prefixForm = QtWidgets.QFormLayout()
        self.widgetLayout.addLayout(self.prefixForm)

        self.prefixLabel = QtWidgets.QLabel("Prefix: ")
        self.prefixForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.prefixLabel)

        self.prefix = QtWidgets.QLineEdit()
        self.prefixForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.prefix)

        # hookup signal/slot connection
        self.prefix.textChanged.connect(partial(self.updatePreview, baseName))

        # create the suffix pair of fields
        self.suffixForm = QtWidgets.QFormLayout()
        self.widgetLayout.addLayout(self.suffixForm)

        self.suffixLabel = QtWidgets.QLabel("Suffix: ")
        self.suffixForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.suffixLabel)

        self.suffix = QtWidgets.QLineEdit()
        self.suffixForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.suffix)

        # hookup signal/slot connection
        self.suffix.textChanged.connect(partial(self.updatePreview, baseName))

        # spacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLayout.addItem(spacerItem)

        # realtime preview of final module name
        self.previewForm = QtWidgets.QFormLayout()
        self.widgetLayout.addLayout(self.previewForm)
        self.previewLabel = QtWidgets.QLabel("Preview: ")
        self.previewName = QtWidgets.QLabel(baseName)
        self.previewName.setMinimumSize(QtCore.QSize(200, 20))
        self.previewName.setMaximumSize(QtCore.QSize(200, 20))
        self.previewName.setAlignment(QtCore.Qt.AlignHCenter)
        self.previewForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previewLabel)
        self.previewForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.previewName)

        # set preview font
        font = QtGui.QFont()
        font.setPointSize(12)
        self.previewName.setFont(font)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLayout.addItem(spacerItem1)

        # create button
        self.createButton = QtWidgets.QPushButton(buttonLabel)
        self.createButton.setObjectName("settings")
        self.widgetLayout.addWidget(self.createButton)
        self.createButton.setMinimumSize(QtCore.QSize(285, 40))
        self.createButton.setMaximumSize(QtCore.QSize(285, 40))
        self.createButton.setSizePolicy(mainSizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.createButton.setFont(font)

        # hookup signal/slot on create button
        if mirror:
            self.createButton.clicked.connect(self.createMirrorModule)
        if duplicate:
            self.createButton.clicked.connect(self.duplicateModule)

        # show the window
        self.mirrorWindow.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updatePreview(self, baseName, *args):
        """
        This simple method updates the module preview field(QLineEdit) with the entered prefix and suffix.

        :param baseName: base name of the module (example: arm)

        """

        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        string = ""
        if len(prefix) > 0:
            string += prefix + "_"

        string += baseName

        if len(suffix) > 0:
            string += "_" + suffix

        self.previewName.setText(string)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createMirrorModule(self):
        """
        This method creates the mirror of a module and is called from createMirrorOfModule_UI.

        To create the mirror of a module, after a few checks are done, a module of the same type is created first.
        If that module type has a left/right version of a joint mover file, the opposite version is brought in.
        All the normal steps of module creation are then gone through and lastly, mirrorTransformations is called.

        """

        userSpecName = str(self.previewName.text())
        networkNode = self.returnNetworkNode
        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        className = cmds.getAttr(networkNode + ".moduleType")

        # check to see if a module already has that name
        modules = utils.returnRigModules()
        mirrorModule = None
        moduleName = None

        for module in modules:
            name = cmds.getAttr(module + ".moduleName")
            if name == userSpecName:
                cmds.confirmDialog(title="Name Exists",
                                   message="A module with that name already exists. Please enter a unique name \
                                   for the module",
                                   icon="critical")
                return

        # now check the modules that contain the parent bone
        for module in modules:
            bones = cmds.getAttr(module + ".Created_Bones")
            splitJoints = bones.split("::")
            createdJoints = []

            # create a list of the created bones
            for bone in splitJoints:
                if bone != "":
                    createdJoints.append(bone)

            # see if the parent bone is in that list
            if parent in createdJoints:
                mirrorModule = cmds.getAttr(module + ".mirrorModule")
                moduleName = cmds.getAttr(module + ".moduleName")

        # if our parent bone's module, has a mirror module, we need to create this new mirror module under that
        # parent instead (if parent = l_thigh, mirror parent should be r_thigh)
        if mirrorModule is not None:
            for module in modules:
                modName = cmds.getAttr(module + ".moduleName")
                if modName == mirrorModule:

                    # find the parent's mover (if parent is l_thigh, mover would be l_leg_thigh_mover)
                    networkNodes = utils.returnRigModules()
                    mover = utils.findMoverNodeFromJointName(networkNodes, parent, False, True)
                    if mover is None:
                        mover = utils.findMoverNodeFromJointName(networkNodes, parent, True, False)
                        mover = mover.partition("_offset")[0]

                    # find mirror mover
                    mirrorMover = mover.replace(moduleName, mirrorModule)
                    baseName = cmds.getAttr(module + ".baseName")
                    boneList = cmds.getAttr(module + ".Created_Bones")
                    mirror = cmds.getAttr(module + ".mirrorModule")

                    # now, we need to find the joint from the mirror mover, and once there is a match, the parent\
                    # var now becomes that joint
                    if mirrorMover.endswith("_mover"):

                        split_string_orig = mirror.split(baseName)
                        split_string_mirror = mirrorModule.split(baseName)
                        list_of_bones = boneList.split("::")

                        option1 = parent.replace(split_string_orig[0], split_string_mirror[0])
                        option2 = parent.replace(split_string_orig[1], split_string_mirror[1])

                        inst = choice_dialog.SimpleChooser("Which Parent?",
                                                           "Please select from the viable parents found.",
                                                           [option1, option2])
                        newName = inst.result
                        if newName in list_of_bones:
                            parent = newName

        # arms and leg exception
        mirrorSide = None
        specialCaseModules = ["ART_Leg_Standard", "ART_Arm_Standard"]
        if className in specialCaseModules:
            side = cmds.getAttr(networkNode + ".side")
            if side == "Left":
                mirrorSide = "Right"
            if side == "Right":
                mirrorSide = "Left"

        # create an instance of the module
        mod = __import__("RigModules." + className, {}, {}, [className])

        # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
        moduleClass = getattr(mod, mod.className)
        jmPath = mod.jointMover
        if self.up == "y":
            jmPath = jmPath.replace("z_up", "y_up")

        # call functions to create network node, skeleton settings UI
        moduleInst = moduleClass(self.rigUiInst, userSpecName)
        self.rigUiInst.moduleInstances.append(moduleInst)
        networkNodeInst = moduleInst.buildNetwork()

        # if mirrorSide exists
        if mirrorSide is not None:
            jmPath = jmPath.partition(".ma")[0] + "_" + mirrorSide + ".ma"
            if mirrorSide == "Left":
                cmds.setAttr(networkNodeInst + ".side", lock=False)
                cmds.setAttr(networkNodeInst + ".side", "Left", type="string", lock=True)
            if mirrorSide == "Right":
                cmds.setAttr(networkNodeInst + ".side", lock=False)
                cmds.setAttr(networkNodeInst + ".side", "Right", type="string", lock=True)

        # build the settings UI/joint mover/add to outliner
        moduleInst.skeletonSettings_UI(userSpecName)
        moduleInst.jointMover_Build(jmPath)
        moduleInst.addJointMoverToOutliner()

        # update the created joints attribute on the network node with the new names
        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        createdBones = cmds.getAttr(networkNodeInst + ".Created_Bones")
        createdBones = createdBones.split("::")

        attrString = ""
        for bone in createdBones:
            if len(bone) > 1:
                attrString += prefix + bone + suffix + "::"

        cmds.setAttr(networkNodeInst + ".Created_Bones", lock=False)
        cmds.setAttr(networkNodeInst + ".Created_Bones", attrString, type="string", lock=True)

        # update the self.currentParent label and the parentModuleBone attr on the network node
        moduleInst.currentParent.setText(parent)

        cmds.setAttr(networkNodeInst + ".parentModuleBone", lock=False)
        cmds.setAttr(networkNodeInst + ".parentModuleBone", parent, type="string", lock=True)

        # find the current parent mover and its scale
        if parent == "root":
            mover = "root_mover"
            offsetMover = "root_mover"

        else:
            # find the parent mover name to parent to
            networkNodes = utils.returnRigModules()
            mover = utils.findMoverNodeFromJointName(networkNodes, parent, False, True)
            if mover is None:
                mover = utils.findMoverNodeFromJointName(networkNodes, parent)

        if mover is not None:
            cmds.parentConstraint(mover, userSpecName + "_mover_grp", mo=True)
            cmds.scaleConstraint(mover, userSpecName + "_mover_grp")

        # paste settings and turn on aim mode
        globalMover = utils.findGlobalMoverFromName(userSpecName)
        cmds.select(globalMover)
        cmds.setToolTo("moveSuperContext")

        utils.fitViewAndShade()
        cmds.refresh(force=True)
        moduleInst.pasteSettings()
        moduleInst.aimMode(True)

        # update the mirrorModule setting
        self.mirrorMod.setText(userSpecName)
        name = cmds.getAttr(networkNode + ".moduleName")
        moduleInst.mirrorMod.setText(name)

        cmds.setAttr(networkNode + ".mirrorModule", lock=False)
        cmds.setAttr(networkNode + ".mirrorModule", userSpecName, type="string", lock=True)

        cmds.setAttr(networkNodeInst + ".mirrorModule", lock=False)
        cmds.setAttr(networkNodeInst + ".mirrorModule", name, type="string", lock=True)

        # extended functionality
        self.createMirrorModule_custom()

        # mirror transformations
        self.mirrorTransformations()

        self.rigUiInst.populateNetworkList()

        # delete UI
        cmds.deleteUI("artv2_create_dupe_win", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createMirrorModule_custom(self):
        """
        This method is intended to be overwritten if needed in a derived class.
        """
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def duplicateModule(self):

        userSpecName = str(self.previewName.text())
        networkNode = self.returnNetworkNode
        parent = cmds.getAttr(networkNode + ".parentModuleBone")
        className = cmds.getAttr(networkNode + ".moduleType")

        # check to see if a module already has that name
        modules = utils.returnRigModules()

        for module in modules:
            name = cmds.getAttr(module + ".moduleName")
            if name == userSpecName:
                cmds.confirmDialog(title="Name Exists",
                                   message="A module with that name already exists. Please enter a unique name \
                                   for the module",
                                   icon="critical")
                return

        # create an instance of the module
        mod = __import__("RigModules." + className, {}, {}, [className])

        # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
        moduleClass = getattr(mod, mod.className)
        jmPath = mod.jointMover
        if self.up == "y":
            jmPath = jmPath.replace("z_up", "y_up")

        # call functions to create network node, skeleton settings UI
        moduleInst = moduleClass(self.rigUiInst, userSpecName)
        self.rigUiInst.moduleInstances.append(moduleInst)
        networkNodeInst = moduleInst.buildNetwork()

        # if mirrorSide exists
        if cmds.objExists(networkNode + ".side"):
                side = cmds.getAttr(networkNode + ".side")
                jmPath = jmPath.partition(".ma")[0] + "_" + side + ".ma"

        # build the settings UI/joint mover/add to outliner
        moduleInst.skeletonSettings_UI(userSpecName)
        moduleInst.jointMover_Build(jmPath)
        moduleInst.addJointMoverToOutliner()

        # update the created joints attribute on the network node with the new names
        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix = prefix + "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        createdBones = cmds.getAttr(networkNodeInst + ".Created_Bones")
        createdBones = createdBones.split("::")

        attrString = ""
        for bone in createdBones:
            if len(bone) > 1:
                attrString += prefix + bone + suffix + "::"

        cmds.setAttr(networkNodeInst + ".Created_Bones", lock=False)
        cmds.setAttr(networkNodeInst + ".Created_Bones", attrString, type="string", lock=True)

        # update the self.currentParent label and the parentModuleBone attr on the network node
        moduleInst.currentParent.setText(parent)

        cmds.setAttr(networkNodeInst + ".parentModuleBone", lock=False)
        cmds.setAttr(networkNodeInst + ".parentModuleBone", parent, type="string", lock=True)

        # find the current parent mover and its scale
        if parent == "root":
            mover = "root_mover"

        else:
            # find the parent mover name to parent to
            networkNodes = utils.returnRigModules()
            mover = utils.findMoverNodeFromJointName(networkNodes, parent, False, True)

        if mover is not None:
            cmds.parentConstraint(mover, userSpecName + "_mover_grp", mo=True)
            cmds.scaleConstraint(mover, userSpecName + "_mover_grp")

        # paste settings
        globalMover = utils.findGlobalMoverFromName(userSpecName)
        cmds.select(globalMover)
        cmds.setToolTo("moveSuperContext")

        utils.fitViewAndShade()
        cmds.refresh(force=True)
        moduleInst.pasteSettings()

        # paste transforms onto the duplicated module, then turn on aim mode
        moduleInst.pasteTransforms()
        moduleInst.aimMode(True)

        self.rigUiInst.populateNetworkList()

        # delete UI
        cmds.deleteUI("artv2_create_dupe_win", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorTransformations_RigPose(self):
        """
        This method is used when creating rig poses for modules. If a module has a mirror, this method will mirror the
        rig pose transformations to that mirror module.

        """

        # reset mirror module's rig pose
        mirrorModInst = self.returnMirrorModuleInst

        # ensure the mirrorModInst has a UI and is setup for rig pose creation
        mirrorModInst.setupForRigPose()
        # if not cmds.objExists(mirrorModInst.name + "_rigPose"):
        #     mirrorModInst.getReferencePose("rigPose")

        # call on base mirror transformations method
        self.mirrorTransformations()
        mirrorModInst.getReferencePose("rigPose")

        # update the rig pose of the mirrorModInst
        mirrorModInst.updateRigPose(mirrorModInst.overallSlider)
        mirrorModInst.cleanUpRigPose()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def copyTransforms(self):

        currentSelection = cmds.ls(sl=True)

        transformData = []
        moverTypes = self.returnJointMovers
        descendants = cmds.listRelatives(self.name + "_mover_grp", children=True, type="transform", ad=True, f=True)
        voidTypes = ["aimConstraint", "scaleConstraint", "parentConstraint", "pointConstraint",
                     "orientConstraint"]
        validNodes = []

        for each in descendants:
            if cmds.nodeType(each) not in voidTypes:
                validNodes.append(each.rpartition("|")[2])

        for moverType in moverTypes:
            for jointMover in moverType:
                elementNum = validNodes.index(jointMover)

                attrs = cmds.listAttr(jointMover, keyable=True)
                for attr in attrs:
                    value = cmds.getAttr(jointMover + "." + attr)
                    transformData.append([jointMover, elementNum, attr, value])

        # write out attrData to a temp file
        tempDir = cmds.internalVar(userTmpDir=True)
        clipboardFile = os.path.normcase(os.path.join(tempDir, "ART_clipboard2.txt"))

        f = open(clipboardFile, 'w')

        # dump the data with json
        json.dump(transformData, f)
        f.close()

        cmds.select(clear=True)
        if len(currentSelection) > 0:
            cmds.select(currentSelection)

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

        currentSelection = cmds.ls(sl=True)

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

        # turn off coplanar mode IF it exists on the module
        try:
            state = mirrorInst.coplanarBtn.isChecked()
            if state:
                mirrorInst.coplanarBtn.setChecked(False)
                mirrorInst.coplanarMode()
        except Exception:
            pass

        # copy rotation values to the mirror, and inverse the translation values
        moverTypes = self.returnJointMovers
        for moverType in moverTypes:
            for jointMover in moverType:
                attrs = cmds.listAttr(jointMover, keyable=True)

                for attr in attrs:
                    value = cmds.getAttr(jointMover + "." + attr)

                    # mirrorMover = jointMover.partition(moduleName)[2]
                    mirrorMover = jointMover.replace(moduleName, mirrorModule, 1)
                    if not cmds.objExists(mirrorMover):
                        mirrorMover = jointMover

                    mirrorAttrs = ["translateX", "translateY", "translateZ"]

                    if attr in mirrorAttrs:
                        try:
                            cmds.setAttr(mirrorMover + "." + attr, value * -1)
                        except Exception:
                            pass
                    else:
                        try:
                            cmds.setAttr(mirrorMover + "." + attr, value)
                        except Exception:
                            pass

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # match the top level groups of the module as well, ensuring that we have a perfect mirror
        topLevelMirrorGrp = cmds.listRelatives(mirrorModule + "_mover_grp", children=True)[0]
        topLevelGrp = cmds.listRelatives(moduleName + "_mover_grp", children=True)[0]

        # get the world matrix of the top level group
        matrix = om.MMatrix(cmds.getAttr(topLevelGrp + ".worldMatrix"))
        mirrored_matrix = matrix.setElement(3, 0, -matrix[12])

        # get parent inverse matrix of top level group
        parentMatrix = om.MMatrix(cmds.getAttr(topLevelMirrorGrp + ".parentInverseMatrix"))
        newMatrix = mirrored_matrix * parentMatrix
        transform_matrix = om.MTransformationMatrix(newMatrix)
        translates = transform_matrix.translation(om.MSpace.kWorld)

        # set the mirrored translations on the mirror top level group
        cmds.setAttr(topLevelMirrorGrp + ".tx", translates[0])
        cmds.setAttr(topLevelMirrorGrp + ".ty", translates[1])
        cmds.setAttr(topLevelMirrorGrp + ".tz", translates[2])

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # turn aim mode on
        mirrorInst.aimMode_Setup(True)

        # extend functionality
        self.mirrorTransformations_Custom()

        # reselect initial selection
        cmds.select(clear=True)
        if len(currentSelection) > 0:
            cmds.select(currentSelection)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def rigPose_UI(self, parentWidget):
        """
        This method creates the UI widget that gets parented into the publish UI that handles rig pose creation.

        A slider gets created for the overall module that goes from current pose to ideal rig pose. Then a slider
        gets created for each joint in the module to allow for finer control over the rig pose creation.

        :param parentWidget: the widget the rig pose UI (QFrame) will get parented to

        """

        # Add a QFrame for the widget
        self.rigPoseFrame = QtWidgets.QFrame()
        self.rigPoseFrame.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.rigPoseFrame.setMinimumWidth(310)
        self.rigPoseFrame.setMaximumWidth(310)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")

        # add the rig pose frame to the stackWidget
        parentWidget.addWidget(self.rigPoseFrame)
        numWidgetsInStack = parentWidget.count()
        parentWidget.setCurrentIndex(numWidgetsInStack - 1)

        # create an overall layout
        self.rigPoseLayout = QtWidgets.QVBoxLayout(self.rigPoseFrame)
        label = QtWidgets.QLabel(self.name)
        self.rigPoseLayout.addWidget(label)

        # create a slider for the overall module rig pose
        hboxLayout = QtWidgets.QHBoxLayout()
        self.rigPoseLayout.addLayout(hboxLayout)

        image1 = QtWidgets.QFrame()
        image1.setMinimumSize(30, 30)
        image1.setMaximumSize(30, 30)
        modelPoseImg = utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/modelPose.png"))
        image1.setStyleSheet("background-image: url(" + modelPoseImg + ");")
        hboxLayout.addWidget(image1)
        image1.setToolTip("Model Pose")

        self.overallSlider = QtWidgets.QSlider()
        self.overallSlider.setProperty("name", self.name)
        hboxLayout.addWidget(self.overallSlider)
        self.overallSlider.setOrientation(QtCore.Qt.Horizontal)
        self.overallSlider.setRange(0, 100)
        self.overallSlider.setSingleStep(1)
        self.overallSlider.setTracking(False)

        image2 = QtWidgets.QFrame()
        image2.setMinimumSize(30, 30)
        image2.setMaximumSize(30, 30)
        rigPoseImg = utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/rigPose.png"))
        image2.setStyleSheet("background-image: url(" + rigPoseImg + ");")
        hboxLayout.addWidget(image2)
        image2.setToolTip("Rig Pose")

        # create hboxlayout for resetAll and update Rig Pose buttons
        buttonLayout = QtWidgets.QHBoxLayout()
        self.rigPoseLayout.addLayout(buttonLayout)

        self.rigPoseResetAllBtn = QtWidgets.QPushButton("Reset Rig Pose")
        buttonLayout.addWidget(self.rigPoseResetAllBtn)
        self.rigPoseResetAllBtn.clicked.connect(self.resetRigPose)
        self.rigPoseResetAllBtn.setToolTip("Reset the module to it's initial ideal rig pose.")
        self.rigPoseResetAllBtn.setObjectName("settings")
        self.rigPoseResetAllBtn.setStyleSheet(self.style)
        self.rigPoseResetAllBtn.setMinimumHeight(30)

        self.rigPoseUpdateAllBtn = QtWidgets.QPushButton("Update Rig Pose")
        self.rigPoseUpdateAllBtn.setStyleSheet(self.style)
        buttonLayout.addWidget(self.rigPoseUpdateAllBtn)
        self.rigPoseUpdateAllBtn.clicked.connect(partial(self.updateRigPose, self.overallSlider))
        self.rigPoseUpdateAllBtn.setToolTip(
            "Update the rig pose if you've done any custom manipulations to the controls.")
        self.rigPoseUpdateAllBtn.setObjectName("settings")
        self.rigPoseUpdateAllBtn.setMinimumHeight(30)

        # create a frame for the advanced controls
        self.rigPose_advancedGroup = QtWidgets.QGroupBox("Advanced")
        self.rigPoseLayout.addWidget(self.rigPose_advancedGroup)
        self.rigPose_advancedLayout = QtWidgets.QVBoxLayout(self.rigPose_advancedGroup)

        # create a slider for each created joint
        joints = self.returnCreatedJoints
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")

        for joint in joints:

            if cmds.objExists(joint):
                self.createRigPoseSliderForJoint(joint)

            else:
                jointBaseName = joint
                if self.name != baseName:
                    nameData = self.name.split(baseName)

                    if nameData[0] != "":
                        jointBaseName = jointBaseName.partition(nameData[0])[2]
                    if nameData[1] != "":
                        jointBaseName = jointBaseName.partition(nameData[1])[0]

                if cmds.objExists(self.name + "_" + jointBaseName + "_mover"):
                    self.createRigPoseSliderForJoint(joint)

        # create mirror button if applicable
        if cmds.getAttr(networkNode + ".mirrorModule") != "":
            mirrorMod = cmds.getAttr(networkNode + ".mirrorModule")
            if mirrorMod != None:
                self.rigPoseMirrorBtn = QtWidgets.QPushButton("Mirror to: " + mirrorMod)
                self.rigPoseLayout.addWidget(self.rigPoseMirrorBtn)
                self.rigPoseMirrorBtn.clicked.connect(self.mirrorTransformations_RigPose)
                self.rigPoseMirrorBtn.setObjectName("settings")
                self.rigPoseMirrorBtn.setStyleSheet(self.style)

        self.rigPoseLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRig(self, textEdit, uiInst):
        """
        This method starts building the rig for a module. It will then call on buildRigCustom, which is implemented
        in each derived module class as an override function.

        :param textEdit: The text edit in the buildProgressUI that we output information to.
        :param uiInst: passed in instance of the buildProgressUI

        """

        # get current nodes in scene
        currentNodes = cmds.ls("*", long=True)
        successfulBuild = True
        errorMessage = ""

        # run the instance build function
        try:
            self.buildRigCustom(textEdit, uiInst)

        except Exception, e:
            import sys
            error_type, value, trace_back = sys.exc_info()
            tb = utils.get_traceback(trace_back, False)

            successfulBuild = False
            errorMessage = tb

        finally:
            networkNode = self.returnNetworkNode
            cmds.lockNode(networkNode, lock=True)

        # get all nodes in scene and compare to original list
        allNodes = cmds.ls("*", long=True)

        newNodes = list(set(allNodes).difference(currentNodes))

        for node in newNodes:
            if not cmds.objExists(node + ".sourceModule"):
                cmds.addAttr(node, ln="sourceModule", dt="string")

            try:
                cmds.setAttr(node + ".sourceModule", self.name, type="string")
            except Exception:
                print node

        if not successfulBuild:
            if textEdit is not None:
                textEdit.setTextColor(QtGui.QColor(255, 0, 0))
                textEdit.append("#Error building " + str(self.name))
                textEdit.append("\n")
                textEdit.append(errorMessage)
                textEdit.append("\n")
                textEdit.setTextColor(QtGui.QColor(255, 255, 255))
                uiInst.errors += 1
                # self.deleteRig()
            else:
                print errorMessage

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRigCustom(self, textEdit, uiInst):
        """
        This method is what truly builds the rig for each module. It is implemented in the derived module class.

        :param textEdit: The text edit in the buildProgressUI that we output information to.
        :param uiInst: passed in instance of the buildProgressUI

        """
        raise NotImplementedError("buildRigCustom not implemented {}".format(self.__class__.__name__))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def deleteRig(self):
        """
        This method deletes all rigging for the module.

        """

        allNodes = cmds.ls("*")
        deleteLater = []

        for node in allNodes:
            if cmds.objExists(node + ".sourceModule"):
                cmds.lockNode(node, lock=False)
                source = cmds.getAttr(node + ".sourceModule")
                if source == self.name:
                    deleteLater.append(node)

        for each in deleteLater:
            if cmds.objExists(each):
                cmds.delete(each)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorTransformations_Custom(self):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateSettingsUI(self):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleChanges(self, moduleInst):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addJointMoverToOutliner(self):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateOutliner(self):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skinProxyGeo(self):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def aimMode(self, state):
        """
        This method toggles the aim mode state if the module can have aim mode.

        It then calls on each derived module's aimMode_Setup which defines how to setup aim mode for the module.

        """

        networkNode = self.returnNetworkNode
        cmds.setAttr(networkNode + ".aimMode", lock=False)
        cmds.setAttr(networkNode + ".aimMode", state, lock=True)

        self.aimMode_Setup(state)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def aimMode_Setup(self, state):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setupModelPoseForRig(self):
        """
        This method is implemented in the derived module class.
        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def matchModelPose(self):
        """
        This method is implemented in the derived module class.

        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pinModule(self, state):
        """
        This method is implemented in the derived module class.

        """

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def bakeOffsets(self):
        """
        This method bakes any transforms on the offset movers up to the global movers, and then zeroes out the offset
        movers.

        """

        module_instances = utils.return_module_instances()
        for inst in module_instances:
            inst.pinModule(True)

        # get movers
        jointMovers = self.returnJointMovers

        # separate mover lists
        globalMovers = jointMovers[0]
        offsetMovers = jointMovers[1]
        constraints = []
        locators = []

        # create locators for the offsetMovers, then zero out offset mover
        for mover in offsetMovers:
            locatorName = mover.partition("_offset")[0] + "_loc"
            loc = cmds.spaceLocator(name=locatorName)[0]

            # constrain locator
            constraint = cmds.parentConstraint(mover, loc)[0]
            cmds.delete(constraint)

            # parent locator under a copy of the locatorName
            parentLoc = cmds.duplicate(loc)[0]
            cmds.parent(loc, parentLoc)
            locators.append(parentLoc)

        for mover in offsetMovers:
            if mover.partition("_offset")[0] in globalMovers:
                for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
                    try:
                        cmds.setAttr(mover + attr, 0)
                    except RuntimeError:
                        pass

        # snap global movers to locators
        for mover in globalMovers:
            if cmds.objExists(mover + "_loc"):
                print mover
                print mover + "_loc"
                constraint = cmds.parentConstraint(mover + "_loc", mover)[0]
                constraints.append(constraint)

        # remove locs
        for const in constraints:
            cmds.delete(const)

        for loc in locators:
            cmds.delete(loc)

        for inst in module_instances:
            inst.pinModule(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setupForRigPose(self, store=False):
        """
        This method unhides the movers and constrains the joints to the movers for creating the rig pose.

        If the user wants to create a custom rig pose (instead of using the sliders), this method sets the module
        up for that functionality.

        """

        # unlock joint movers
        cmds.select("JointMover", hi=True)
        jmNodes = cmds.ls(sl=True)
        for node in jmNodes:
            cmds.lockNode(node, lock=False)

        # find the mover shapes and set their visibility
        movers = self.returnJointMovers
        globalMovers = movers[0]
        shapes = []

        for each in movers:
            for mover in each:
                child = cmds.listRelatives(mover, children=True, shapes=True)
                if len(child) > 0:
                    shapes.append(mover + "|" + child[0])

            for shape in shapes:
                cmds.setAttr(shape + ".v", lock=False)
                cmds.setAttr(shape + ".v", 0, lock=True)

        # show global movers
        shapes = []
        for mover in globalMovers:
            child = cmds.listRelatives(mover, children=True, shapes=True)
            if len(child) > 0:
                shapes.append(mover + "|" + child[0])

        for shape in shapes:
            cmds.setAttr(shape + ".v", lock=False)
            cmds.setAttr(shape + ".v", 1, lock=True)

        # unlock mover group for this module and make visible
        self.lock_nodes(lock=False)
        cmds.setAttr(self.name + "_mover_grp.v", lock=False)
        cmds.setAttr(self.name + "_mover_grp.v", 1)

        # hide the proxy geo
        cmds.select(self.name + "_mover_grp", hi=True)
        allNodes = cmds.ls(sl=True)
        for node in allNodes:
            if node.find("_proxy_geo") != -1:
                if cmds.nodeType(node) == "mesh":
                    parent = cmds.listRelatives(node, parent=True)[0]
                    cmds.lockNode(parent, lock=False)
                    cmds.setAttr(parent + ".v", lock=False)
                    cmds.setAttr(parent + ".v", 0)
                    cmds.lockNode(parent, lock=True)

        # get the joints created by this module
        joints = self.returnCreatedJoints

        # create mover name
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")

        self.aimMode_Setup(False)
        for joint in joints:
            if cmds.objExists(joint + "_mover"):
                cmds.delete(cmds.parentConstraint(joint, joint + "_mover"))
                cmds.parentConstraint(joint + "_mover", joint)
            else:
                jointBaseName = joint
                if self.name != baseName:
                    nameData = self.name.split(baseName)

                    if nameData[0] != "":
                        jointBaseName = jointBaseName.partition(nameData[0])[2]
                    if nameData[1] != "":
                        jointBaseName = jointBaseName.partition(nameData[1])[0]

                if cmds.objExists(self.name + "_" + jointBaseName + "_mover"):
                    cmds.delete(cmds.parentConstraint(joint, self.name + "_" + jointBaseName + "_mover"))
                    cmds.parentConstraint(self.name + "_" + jointBaseName + "_mover", joint)

        if store:
            if self.name != "root":
                self.getReferencePose("modelPose")

        # lock joint movers
        cmds.select("JointMover", hi=True)
        jmNodes = cmds.ls(sl=True)
        for node in jmNodes:
            cmds.lockNode(node, lock=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setSkeletonPose(self, poseType):
        """
        This method constrains the joints to the movers and then stores that pose data for those joints.

        This could be the model pose or the rig pose.

        :param poseType: whether to set the model pose or rig pose for the joints.

        """
        # get the joints created by this module
        joints = self.returnCreatedJoints

        # create mover name
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")

        for joint in joints:
            if cmds.objExists(joint + "_mover_offset"):
                cmds.parentConstraint(joint + "_mover_offset", joint)

            else:
                jointBaseName = joint
                if self.name != baseName:
                    nameData = self.name.split(baseName)

                    if nameData[0] != "":
                        jointBaseName = jointBaseName.partition(nameData[0])[2]
                    if nameData[1] != "":
                        jointBaseName = jointBaseName.partition(nameData[1])[0]

                if cmds.objExists(self.name + "_" + jointBaseName + "_mover_offset"):
                    cmds.parentConstraint(self.name + "_" + jointBaseName + "_mover_offset", joint)

        # set pose
        self.setReferencePose(poseType)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def removeSkeletalConstraints(self):
        """
        This method removes any constraints on the joints. This tends to get called by removing rigging.

        """

        # get the joints created by this module and remove the constraints
        joints = self.returnCreatedJoints

        # create mover name
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")

        for joint in joints:
            if cmds.objExists(joint + "_mover_offset"):
                cmds.select(joint)
                cmds.delete(constraints=True)

            else:
                jointBaseName = joint
                if self.name != baseName:
                    nameData = self.name.split(baseName)

                    if nameData[0] != "":
                        jointBaseName = jointBaseName.partition(nameData[0])[2]
                    if nameData[1] != "":
                        jointBaseName = jointBaseName.partition(nameData[1])[0]

                if cmds.objExists(self.name + "_" + jointBaseName + "_mover_offset"):
                    cmds.select(joint)
                    cmds.delete(constraints=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def cleanUpRigPose(self):
        """
        This method hides the joint movers and unconstrains the joints from the movers after setting a rig pose.

        """

        # show the proxy geo
        cmds.select(self.name + "_mover_grp", hi=True)
        allNodes = cmds.ls(sl=True)
        for node in allNodes:
            if node.find("_proxy_geo") != -1:
                if cmds.nodeType(node) == "mesh":
                    parent = cmds.listRelatives(node, parent=True)[0]
                    cmds.lockNode(parent, lock=False)
                    cmds.setAttr(parent + ".v", lock=False)
                    cmds.setAttr(parent + ".v", 1)
                    cmds.lockNode(parent, lock=True)

        # unlock mover group for this module and make invisible
        cmds.lockNode(self.name + "_mover_grp", lock=False)
        cmds.setAttr(self.name + "_mover_grp.v", lock=False)

        cmds.setAttr(self.name + "_mover_grp.v", 0)

        cmds.setAttr(self.name + "_mover_grp.v", lock=True)
        cmds.lockNode(self.name + "_mover_grp", lock=True)

        # get the joints created by this module and remove the constraints
        joints = self.returnCreatedJoints

        # create mover name
        try:
            networkNode = self.returnNetworkNode
            baseName = cmds.getAttr(networkNode + ".baseName")

            for joint in joints:
                if cmds.objExists(joint + "_mover_offset"):
                    cmds.select(joint)
                    cmds.delete(constraints=True)

                else:
                    jointBaseName = joint
                    if self.name != baseName:
                        nameData = self.name.split(baseName)

                        if nameData[0] != "":
                            jointBaseName = jointBaseName.partition(nameData[0])[2]
                        if nameData[1] != "":
                            jointBaseName = jointBaseName.partition(nameData[1])[0]

                    if cmds.objExists(self.name + "_" + jointBaseName + "_mover_offset"):
                        cmds.select(joint)
                        cmds.delete(constraints=True)
        except Exception, e:
            cmds.warning(str(e))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateRigPose(self, slider):
        """
        This method updates what the stored rig pose is for a module. The default rig pose tends to be zeroed out
        rotations, but this function can essentially update what the max value on the rig pose slider sets the pose to.

        :param slider: The rig pose slider where the min is the current model pose and the max is the rig pose.

        """

        # get network node
        networkNode = self.returnNetworkNode

        # get pose data off networkNode
        originalData = json.loads(cmds.getAttr(networkNode + ".rigPose"))
        newPose = []

        for data in originalData:
            moverData = {}
            mover = data.get("mover")
            moverData["mover"] = mover

            if cmds.objExists(mover):
                translate = cmds.getAttr(mover + ".translate")[0]
                rotate = cmds.getAttr(mover + ".rotate")[0]

                moverData["translate"] = translate
                moverData["rotate"] = rotate
                newPose.append(moverData)

        jsonString = json.dumps(newPose)
        cmds.setAttr(networkNode + ".rigPose", jsonString, type="string")
        slider.setValue(0)
        slider.setValue(100)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetRigPose(self):
        """
        This method resets the module rig pose to be the default (zeroed rotations).

        """

        # get the network node
        networkNode = self.returnNetworkNode

        # remove the rigPose attribute on the networkNode
        cmds.deleteAttr(networkNode, at="rigPose")

        # recreate rig pose node with defaults
        self.getReferencePose("rigPose")

        # set slider
        self.overallSlider.setValue(0)
        self.overallSlider.setValue(100)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetRigPose_Part(self, part):
        """
        This method resets the given joint (part) rig pose to be zeroed rotations. This is for the part slider on
        the rig pose UI in the advanced section.

        :param part: The given joint name slider.

        """

        # get the networkNode
        networkNode = self.returnNetworkNode

        # get the poseData
        poseData = json.loads(cmds.getAttr(networkNode + ".rigPose"))

        # find our part in the pose data
        for data in poseData:
            mover = data.get("mover")
            if mover == part:
                rotate = data.get("rotate")

                try:
                    cmds.setAttr(mover + ".rotate", 0, 0, 0, type="double3")
                    data["rotate"] = (0.0, 0.0, 0.0)
                except:
                    pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getReferencePose(self, poseType, zeroPose=True, return_only=False):
        """
        This method gets the model pose or the rig pose (depending on poseType) and stores that data for the movers.

        :param poseType: Whether or not to get the model pose or rig pose.
        :param zeroPose: Whether or not the default rig pose should be set to zeroed rotations.
        :param return_only: Whether to simply return the data or to set the data.

        """

        # get movers
        jointMovers = self.returnJointMovers

        # separate mover lists
        globalMovers = jointMovers[0]
        offsetMovers = jointMovers[1]

        # get the network node
        networkNode = self.returnNetworkNode

        # if rigPose already exists, then do not set values
        if poseType == "rigPose":
            if cmds.objExists(networkNode + "." + poseType):
                return

        # create the pose data attr if needed
        if not cmds.objExists(networkNode + "." + poseType):
            cmds.addAttr(networkNode, sn=poseType, dt="string")

        # create reference pose data dict
        poseData = []

        # loop through each mover, getting the translate and rotate values, creating an attribute on the network node
        # to store those values
        getcontext().prec = 3

        for moverList in [globalMovers, offsetMovers]:
            for mover in moverList:
                moverData = {}
                moverData["mover"] = str(mover)

                for attr in ["translate", "rotate", "scale"]:
                    value_data = cmds.getAttr(mover + "." + attr)[0]
                    value = []
                    for each in value_data:
                        value.append(float(Decimal(each) / 1))

                    if zeroPose:
                        if poseType == "rigPose":
                            if attr == "rotate":
                                value = (0.0, 0.0, 0.0)

                    # add the data to the list
                    moverData[str(attr)] = value

                    # add mover data to the pose data list
                    poseData.append(moverData)

        if return_only is False:
            # dump the pose data list onto the poseType attribute
            jsonString = json.dumps(poseData)
            cmds.setAttr(networkNode + "." + poseType, jsonString, type="string")
        else:
            return poseData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setReferencePose(self, poseType):
        """
        This method gets the data for the given pose type (rig or model) and sets the movers with those values.

        :param poseType: Whether to set the model pose or the rig pose on the movers.

        """

        # get the network node
        networkNode = self.returnNetworkNode

        # get the pose data from the attribute
        if cmds.objExists(networkNode + "." + poseType):
            poseData = json.loads(cmds.getAttr(networkNode + "." + poseType))

            for data in poseData:
                mover = data.get("mover")
                translate = data.get("translate")
                rotate = data.get("rotate")

                # if the mover exists, set the values
                if cmds.objExists(mover):

                    # set translations
                    for i in range(len(translate)):
                        if i == 0:
                            try:
                                cmds.setAttr(mover + ".translateX", translate[i])
                            except:
                                pass
                        if i == 1:
                            try:
                                cmds.setAttr(mover + ".translateY", translate[i])
                            except:
                                pass
                        if i == 2:
                            try:
                                cmds.setAttr(mover + ".translateZ", translate[i])
                            except:
                                pass

                    # set rotations
                    for i in range(len(rotate)):
                        if i == 0:
                            try:
                                cmds.setAttr(mover + ".rotateX", rotate[i])
                            except:
                                pass
                        if i == 1:
                            try:
                                cmds.setAttr(mover + ".rotateY", rotate[i])
                            except:
                                pass
                        if i == 2:
                            try:
                                cmds.setAttr(mover + ".rotateZ", rotate[i])
                            except:
                                pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setReferencePoseSlider(self, part, *args):
        """
        This method takes the slider value of a given part and then calls on setPosePercentage, which will then find
        the values of the model pose and the rig pose and figure out based on the slider percentage what values to
        set on the mover.

        :param part: the joint mover which the slider is controlling.
        :param args: the values from the slider

        """

        percent = float(args[0]) * .01
        self.setPosePercentage(percent, part)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setPosePercentage(self, percent, part):
        """
        This method takes the percent from setReferencePoseSlider, gets the values of the model pose and rig pose
        for the given part, then calls on setPosePercentage_Part to find and set the values on the mover that is
        the percentage between model and rig pose.

        Example: If the model pose is a value of 10 and the rig pose is a value of 0, and the slider is at .5, then
        the value to set is 5. (But this is done and found per attribute)

        :param percent: What percent of model and rig pose to set.
        :param part: What joint mover to set the values on.

        """

        # get network node
        networkNode = self.returnNetworkNode

        # get reference pose attributes
        modelPoseData = json.loads(cmds.getAttr(networkNode + ".modelPose"))
        rigPoseData = json.loads(cmds.getAttr(networkNode + ".rigPose"))

        # get the data for each mover
        for poseData in modelPoseData:

            mover = poseData.get("mover")
            translate = poseData.get("translate")
            rotate = poseData.get("rotate")

            if part != None:
                if part == mover:
                    self.setPosePercentage_Part(percent, mover, modelPoseData, rigPoseData, poseData, translate, rotate)
            else:
                self.setPosePercentage_Part(percent, mover, modelPoseData, rigPoseData, poseData, translate, rotate)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setPosePercentage_Part(self, percent, mover, modelPoseData, rigPoseData, poseData, translate, rotate):
        """
        This method takes the data from setPosePercentage and figures out what values to set on the given part (mover).

        Example: If the model pose is a value of 10 and the rig pose is a value of 0, and the slider is at .5, then
        the value to set is 5. (But this is done and found per attribute)

        :param percent: the percent value of the slider. What percentage of the model and rig pose to use.
        :param mover: the mover to set the values on.
        :param modelPoseData: all of the data for the model pose for this mover.
        :param rigPoseData: all of the data for the rig pose for this mover.
        :param poseData: a list which includes the mover and its translate and rotate values.
        :param translate: the translate values for the model pose
        :param rotate: the rotate values for the model pose

        """

        # get the index of this entry in the rigPoseData list
        index = modelPoseData.index(poseData)

        # get the corresponding rig pose data
        rigData = rigPoseData[index]
        rigTranslate = rigData.get("translate")
        rigRotate = rigData.get("rotate")

        # find percentile between model and rig pose to set on each attribute
        for i in range(len(translate)):
            valueToSet = mathUtils.returnPercentile([translate[i], rigTranslate[i]], percent)
            if i == 0:
                cmds.setAttr(mover + ".translateX", valueToSet)
            if i == 1:
                cmds.setAttr(mover + ".translateY", valueToSet)
            if i == 2:
                cmds.setAttr(mover + ".translateZ", valueToSet)

        for i in range(len(rotate)):
            valueToSet = mathUtils.returnPercentile([rotate[i], rigRotate[i]], percent)
            if i == 0:
                cmds.setAttr(mover + ".rotateX", valueToSet)
            if i == 1:
                cmds.setAttr(mover + ".rotateY", valueToSet)
            if i == 2:
                cmds.setAttr(mover + ".rotateZ", valueToSet)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createRigPoseSliderForJoint(self, joint):
        """
        This method creates the rig pose slider widget for the given joint. (This shows up in the advanced section of
        the rig pose UI)

        :param joint: The joint that the slider will control.

        """

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")

        # create mover name
        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")

        jointName = joint

        if cmds.objExists(joint + "_mover"):
            jointName = joint

        else:

            jointBaseName = joint
            if self.name != baseName:
                nameData = self.name.split(baseName)

                if nameData[0] != "":
                    jointName = jointBaseName.partition(nameData[0])[2]
                if nameData[1] != "":
                    jointName = jointName.partition(nameData[1])[0]

                jointName = self.name + "_" + jointName

            else:
                jointName = self.name + "_" + jointName

        # create a master vertical layout
        mainLayout = QtWidgets.QVBoxLayout()
        self.rigPose_advancedLayout.addLayout(mainLayout)

        # create a label for the joint
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        jointLabel = QtWidgets.QLabel(joint + ":")
        jointLabel.setFont(font)
        mainLayout.addWidget(jointLabel)

        # create layout for slider/button
        layout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(layout)

        # create slider for joint
        slider = QtWidgets.QSlider()
        layout.addWidget(slider)
        slider.setProperty("name", joint)
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setSingleStep(1)
        slider.valueChanged.connect(partial(self.setReferencePoseSlider, jointName + "_mover"))
        slider.setTracking(False)
        self.overallSlider.valueChanged.connect(slider.setValue)

        # create reset button
        button = QtWidgets.QPushButton("Reset")
        button.setMinimumWidth(70)
        button.setMaximumWidth(70)
        button.setMinimumHeight(30)
        layout.addWidget(button)
        button.setObjectName("orange")
        button.setStyleSheet(self.style)

        button.clicked.connect(partial(self.resetRigPose_Part, jointName + "_mover"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateBoneCount(self):
        """
        This method looks at the create bones attribute of the module and gets the number of bones in that list
        and appends it onto the total bone count for the bone counter interface.

        """

        if cmds.window("ART_BoneCounterWin", exists=True):
            if self.rigUiInst.boneCounterInst is not None:
                self.rigUiInst.boneCounterInst.updateBoneCount()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleShapeVis(self, transform, value):
        """
        This method finds the shapes for the passed in transform and toggles the visibility based on the value.

        :param transform: the transform to get the shape nodes from.
        :param value: whether to show or hide the shape nodes.

        """

        self.lock_nodes(lock=False)
        if cmds.objExists(transform):
            shape = cmds.listRelatives(transform, shapes=True)
            if shape is not None:
                cmds.setAttr(shape[0] + ".v", lock=False)
                cmds.setAttr(shape[0] + ".v", value)
                cmds.setAttr(shape[0] + ".v", lock=True)
        self.lock_nodes()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectionScriptJob_animUI(self, buttonData):
        """
        This method is called from a scriptjob anytime a selection is changed. It's sole purpose it to update the button
        color on the anim picker to show if a control is selected or not.

        :param buttonData: pairings of button/control/brush. brush is the original color of the button.

        """

        selection = mel.eval("ls -sl;")
        if selection is None:
            selection = []

        for data in buttonData:
            control = data[1]
            button = data[0]
            brushColor = data[2]

            if control in selection:
                try:
                    button.brush.setColor(QtCore.Qt.white)
                    button.update()
                except:
                    pass

            else:
                try:
                    button.brush.setColor(brushColor)
                    button.update()
                except:
                    pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importFBX_pre(self, importMethod, character):
        """
        This method runs before an fbx is imported onto the control rig. It cuts any keys on the controls and zeroes
        the controls out before importing the fbx (which is called in the derived module class)

        :param importMethod: Whether or not the FBX is getting imported as FK, IK, Both, or None
        :param character: The namespace of the rig.

        """

        if importMethod != "None":
            controls = self.getControls()
            for control in controls:
                for each in control:
                    cmds.cutKey(each)

            self.resetRigControls(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importFBX(self, importMethod, character):
        """
        This method is implemented in the derived module class and defines how mocap is imported onto the rig controls.

        :param importMethod: Whether or not the FBX is getting imported as FK, IK, Both, or None
        :param character: The namespace of the rig.

        """

        pass

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
        ignoreAttrs = ["mode"]

        if resetAll:

            # list any attributes on the network node that contain "controls"
            control_list = self.getControls()
            controls = [item for sublist in control_list for item in sublist]
            print controls

            # reset the attr on each control
            nonZeroAttrs = ["scale", "globalScale", "scaleX", "scaleY", "scaleZ"]

            for control in controls:
                attrs = cmds.listAttr(control, keyable=True)
                print attrs
                for attr in attrs:
                    if attr not in ignoreAttrs:
                        if attr not in nonZeroAttrs:
                            print "setting {0} to 0".format(control)
                            try:
                                cmds.setAttr(control + "." + attr, 0)
                            except RuntimeError, e:
                                cmds.warning("skipped " + str(control) + ". {0}".format(e))
                        else:
                            print "setting {0} to 1".format(control)
                            try:
                                cmds.setAttr(control + "." + attr, 1)
                            except RuntimeError, e:
                                cmds.warning("skipped " + str(control) + ". {0}".format(e))
            # except StandardError:
            #     cmds.warning("skipped " + str(control) + ". No valid controls found to reset.")

        if not resetAll:
            nonZeroAttrs = ["scale", "globalScale", "scaleX", "scaleY", "scaleZ"]
            selection = cmds.ls(sl=True)

            for each in selection:
                attrs = cmds.listAttr(each, keyable=True)

                for attr in attrs:
                    if attr not in ignoreAttrs:
                        if attr not in nonZeroAttrs:
                            cmds.setAttr(each + "." + attr, 0)
                        else:
                            cmds.setAttr(each + "." + attr, 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getControls(self, all=True, attribute=None):
        """
        This method returns a list of all the rig controls of the module if all is True. Otherwise, checks for passed
        in attribute in the listAttr results and returns only those controls.

        :return: List of rig controls in the module based on args.

        """

        # get namespace
        networkNode = self.returnRigNetworkNode
        if networkNode is None:
            winParent = interfaceUtils.getMainWindow()
            win = interfaceUtils.DialogMessage("Error", "This function does not work without a namespace.", [], 0,
                                               winParent)
            win.show()
            return None

        controlNode = cmds.listConnections(networkNode + ".controls")[0]

        # get all attrs on the controlNode
        attrs = cmds.listAttr(controlNode, ud=True)

        # loop through attrs, getting connections
        returnControls = []
        for attr in attrs:
            connections = cmds.listConnections(controlNode + "." + attr, source=False)
            if connections is not None:
                if all is True:
                    returnControls.append(connections)
                if attribute is not None:
                    if attr == attribute:
                        returnControls = connections
        return returnControls

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def selectRigControls(self):
        """
        This method calls on getControls to return a list of the controls and the selects them.

        """

        controls = self.getControls()

        # get namespace
        networkNode = self.returnRigNetworkNode
        characterNode = cmds.listConnections(networkNode + ".parent")[0]
        namespace = cmds.getAttr(characterNode + ".namespace")

        for control in controls:

            cmds.select(control, add=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setupPickWalking(self):
        """
        This method is implemented in the derived module class and defines how pickwalking is setup within a module.
        """
        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addSpacesToMenu(self, control, buttonInst):

        import Tools.Animation.ART_SpaceSwitcher as space_switcher

        # space icon
        spaceIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/animSpace.png"))))

        # get existing menu QActions
        actionObjects = buttonInst.menu.children()
        actions = []
        for obj in actionObjects:
            actions.append(obj.text())

        # get control spaces
        if cmds.objExists(control + ".follow"):
            enumVal = cmds.addAttr(control + ".follow", q=True, en=True)
            splitString = enumVal.split(":")

            for space in splitString:
                if "Switch to space: " + space not in actions:
                    buttonInst.menu.addAction(spaceIcon, "Switch to space: " + space,
                                              partial(space_switcher.SwitchSpace, control, space))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PROPERTIES
    @property
    def getModules(self):
        """
        This method finds the main "character" module that has connections to all of the rig modules

        :return: returns the character node.

        """

        modules = cmds.ls(type="network")
        for module in modules:
            attrs = cmds.listAttr(module)
            if "rigModules" in attrs:
                return module

    @property
    def getAllModules(self):
        """
        This method finds all connected rig modules to the main character network node.

        :return: returns a list of the rig modules

        """

        modules = cmds.ls(type="network")
        returnMods = []
        for module in modules:
            attrs = cmds.listAttr(module)
            if "parent" in attrs:
                returnMods.append(module)

        return returnMods

    @property
    def returnNetworkNode(self):
        """
        This method returns the module's own network node.

        :return: the modules network node

        """
        networkNode = None
        networkNodes = cmds.ls(type="network")
        for node in networkNodes:
            attrs = cmds.listAttr(node)
            if "moduleName" in attrs:
                if cmds.getAttr(node + ".moduleName") == self.name:
                    networkNode = node

        return networkNode

    @property
    def returnRigNetworkNode(self):
        """
        This method returns the module's own network node using the namespace on the main character
        network node. This is so that if there are multiple characters in a scene, we know which
        network node for which character we are trying to return.

        :return: returns this module's network node in a scene with references.

        """
        modules = []
        networkNodes = cmds.ls(type="network")
        for node in networkNodes:
            attrs = cmds.listAttr(node)
            if "moduleName" in attrs:
                if cmds.getAttr(node + ".moduleName") == self.name:
                    characterNode = cmds.listConnections(node + ".parent")[0]
                    if cmds.objExists(characterNode + ".namespace"):
                        if cmds.getAttr(characterNode + ".namespace") == self.namespace.partition(":")[0]:
                            networkNode = node
                            return networkNode
                    else:
                        # if there is no namespace attr, then the character is not referenced in, so we can just return
                        # the one network node

                        # check .moduleName attr and see if it matches self.name
                        if cmds.getAttr(node + ".moduleName") == self.name:
                            return node

    @property
    def returnClassObject(self):
        return self

    @property
    def returnCreatedJoints(self):
        """
        This method loops through the Created Bones attribute on its network node and returns a list of the
        joints it will create given the current module settings.

        :return: A list of the created bones of the module.

        """

        networkNode = self.returnNetworkNode
        joints = cmds.getAttr(networkNode + ".Created_Bones")

        splitJoints = joints.split("::")
        createdJoints = []

        for bone in splitJoints:
            if bone != "":
                createdJoints.append(bone)

        return createdJoints

    @property
    def returnJointMovers(self):
        """
        This method finds and returns all joint movers for the module.

        :return: a list of all global movers, offset movers, and geo movers for the module.

        """

        cmds.select(self.name + "_mover_grp", hi=True)
        allNodes = cmds.ls(sl=True)

        globalMovers = []
        offsetMovers = []
        geoMovers = []

        for each in allNodes:
            if each.endswith("mover") is True:
                if cmds.nodeType(each) == "transform":
                    globalMovers.append(each)
            if each.endswith("mover_offset") is True:
                if cmds.nodeType(each) == "transform":
                    offsetMovers.append(each)
            if each.endswith("mover_geo") is True:
                if cmds.nodeType(each) == "transform":
                    geoMovers.append(each)

        return [globalMovers, offsetMovers, geoMovers]

    @property
    def returnMirrorModuleInst(self):
        """
        This method finds and returns the instance of a module's mirror module.

        :return: a pointer in memory to the instance of the mirror module.

        """

        # get network node
        networkNode = self.returnNetworkNode
        mirrorModule = cmds.getAttr(networkNode + ".mirrorModule")

        # find instance through rig UI inst
        for inst in self.rigUiInst.moduleInstances:
            networkNode = inst.returnNetworkNode
            moduleName = cmds.getAttr(networkNode + ".moduleName")
            if moduleName == mirrorModule:
                return inst

    @property
    def returnPrefixSuffix(self):
        """
        This method splits our module name by the base name and returns the prefix and suffix.

        :return: the user-defined prefix and suffix found by splitting the module name by the base name.

        """

        prefix = None
        suffix = None

        networkNode = self.returnNetworkNode
        baseName = cmds.getAttr(networkNode + ".baseName")
        splitName = self.name.split(baseName)
        if splitName[0] != '':
            prefix = splitName[0]
        if splitName[1] != '':
            suffix = splitName[1]
        return [prefix, suffix]
