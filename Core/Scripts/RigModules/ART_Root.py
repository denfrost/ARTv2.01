"""
Author: Jeremy Ernst

========
Contents
========

|   **Must Have Methods:**
|       :py:func:`addAttributes <RigModules.ART_Root.ART_Root.addAttributes>`
|       :py:func:`skeletonSettings_UI <RigModules.ART_Root.ART_Root.skeletonSettings_UI>`
|       :py:func:`pickerUI <RigModules.ART_Root.ART_Root.pickerUI>`
|       :py:func:`addJointMoverToOutliner <RigModules.ART_Root.ART_Root.addJointMoverToOutliner>`
|       :py:func:`buildRigCustom <RigModules.ART_Root.ART_Root.buildRigCustom>`
|       :py:func:`importFBX <RigModules.ART_Root.ART_Root.importFBX>`
|       :py:func:`setupPickWalking <RigModules.ART_Root.ART_Root.setupPickWalking>`



===============
File Attributes
===============
    * **icon:** This is the image file (125x75 .png) that gets used in the RigCreatorUI

    * **search:** These are search terms that are accepted when searching the list of modules in the
      RigCreatorUI

    * **class name:** The name of the class.

    * **baseName:** The default name the module will get created with. Users can then add a prefix and/or
      suffix to the base name.

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
from functools import partial
import os

import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# external imports
from Base.ART_RigModule import ART_RigModule
import Utilities.riggingUtils as riggingUtils
import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils

# file attributes
icon = "Core/Icons/Modules/root.png"
search = "Root"
className = "ART_Root"
baseName = "root"
displayName = "Root"
fbxImport = ["None", "Root Motion: Offset", "Root Motion: Master", "Root Motion: Root"]
matchData = [False, None]


class ART_Root(ART_RigModule):
    """
    This class builds the root module, which all 'characters' must have. It is not a selectable module in the UI, it
    is automatically created when the rigCreator is launched.
    """

    def __init__(self, rigUiInst, moduleUserName):
        """Initiate the class, taking in the instance to the interface and the user specified name.

        :param rigUiInst: This is the rig creator interface instance being passed in.
        :param moduleUserName: This is the name specified by the user on module creation.

        Instantiate the following class variables as well:
            * **self.rigUiInst:** take the passed in interface instance and make it a class var
            * **self.moduleUserName:** take the passed in moduleUserName and make it a class var
            * **self.outlinerWidget:** an empty list that will hold all of the widgets added to the outliner

        """
        self.rigUiInst = rigUiInst
        self.moduleUserName = moduleUserName
        self.outlinerWidgets = {}

        ART_RigModule.__init__(self, "ART_Root_Module", "ART_Root", moduleUserName)

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
        cmds.setAttr(self.networkNode + ".Created_Bones", "root", type="string", lock=True)

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

        # groupbox all modules get
        ART_RigModule.skeletonSettings_UI(self, name, 335, 85, False)

        # add a label to the root module saying this module cannot be edited or removed
        self.layout = QtWidgets.QVBoxLayout(self.groupBox)
        self.label = QtWidgets.QLabel("All rigs must have a root module. This module cannot be edited or removed.")
        self.layout.addWidget(self.label)
        self.label.setGeometry(QtCore.QRect(10, 20, 300, 60))
        self.label.setMinimumHeight(60)
        self.label.setWordWrap(True)

        # add to the rig cretor UI's module settings layout VBoxLayout
        self.rigUiInst.moduleSettingsLayout.addWidget(self.groupBox)

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
        yellowBrush = QtGui.QColor(155, 118, 67)
        blueBrush = QtGui.QColor(67, 122, 150)
        purpleBrush = QtGui.QColor(82, 67, 155)
        greenBrush = QtGui.QColor(122, 150, 67)
        clearBrush = QtGui.QBrush(QtCore.Qt.black)
        clearBrush.setStyle(QtCore.Qt.NoBrush)

        # create border item
        if networkNode.find(":") != -1:
            moduleNode = networkNode.partition(":")[2]
        else:
            moduleNode = networkNode
        borderItem = interfaceUtils.pickerBorderItem(center.x() - 40, center.y() - 70, 50, 98, clearBrush, moduleNode)

        # get controls + namespace
        networkNode = self.returnNetworkNode
        controls = self.getControls(False, "rootControls")

        masterCtrl = None
        offsetCtrl = None
        rootCtrl = None

        for control in controls:
            if control.find("master") != -1:
                index = controls.index(control)
                masterCtrl = controls[index]
            if control.find("offset") != -1:
                index = controls.index(control)
                offsetCtrl = controls[index]
            if control.find("root") != -1:
                index = controls.index(control)
                rootCtrl = controls[index]

        # master anim button
        masterBtn = interfaceUtils.pickerButton(30, 30, [10, 2], masterCtrl, yellowBrush, borderItem)
        interfaceUtils.addTextToButton("M", masterBtn)

        # offset anim button
        offsetBtn = interfaceUtils.pickerButton(30, 30, [10, 34], offsetCtrl, blueBrush, borderItem)
        interfaceUtils.addTextToButton("O", offsetBtn)

        # root anim button
        rootBtn = interfaceUtils.pickerButton(30, 30, [10, 66], rootCtrl, purpleBrush, borderItem)
        interfaceUtils.addTextToButton("R", rootBtn)

        # =======================================================================
        # #Context Menu
        # =======================================================================
        zeroIcon1 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroAll.png"))))
        zeroIcon2 = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/zeroSel.png"))))

        masterBtn.menu.addAction(zeroIcon1, "Zero Out Attrs (All)", partial(self.resetRigControls, True))
        masterBtn.menu.addAction(zeroIcon2, "Zero Out Attrs (Sel)", partial(self.resetRigControls, False))
        masterBtn.menu.addSeparator()
        masterBtn.addSpaces = partial(self.addSpacesToMenu, masterCtrl, masterBtn)

        # =======================================================================
        # #Create scriptJob for selection. Set scriptJob number to borderItem.data(5)
        # =======================================================================
        scriptJob = cmds.scriptJob(event=["SelectionChanged", partial(self.selectionScriptJob_animUI, [
            [masterBtn, masterCtrl, yellowBrush], [offsetBtn, offsetCtrl, blueBrush],
            [rootBtn, rootCtrl, purpleBrush]])], kws=True)
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

        # create selection script job for module
        self.updateBoneCount()
        self.createScriptJob()

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
            textEdit.append("        Building Root Rig..")

        # get the created joint
        networkNode = self.returnNetworkNode
        rootJoint = cmds.getAttr(networkNode + ".Created_Bones")

        # create a new network node to hold the control types
        if not cmds.objExists(networkNode + ".controls"):
            cmds.addAttr(networkNode, sn="controls", at="message")
        controlNode = cmds.createNode("network", name=networkNode + "_Controls")
        cmds.addAttr(controlNode, sn="parentModule", at="message")

        # connect new network node to original network node
        cmds.connectAttr(networkNode + ".controls", controlNode + ".parentModule")

        # create the rig grp
        rigGrp = cmds.group(empty=True, name="rig_grp")

        # Need to build 3 controls, the master, the offset, and the root control
        masterControls = riggingUtils.createControlFromMover(rootJoint, networkNode, False, True,
                                                             control_type="ik_rig_control")

        # rename controls
        masterControl = cmds.rename(masterControls[0], "master_anim")
        masterCtrlGrp = cmds.rename(masterControls[1], "master_anim_grp")
        masterSpaceSwitch = cmds.rename(masterControls[2], "master_anim_space_switcher")
        masterSpace = cmds.rename(masterControls[3], "master_anim_space_switcher_follow")
        cmds.setAttr(masterControl + ".overrideEnabled", 1)
        cmds.setAttr(masterControl + ".overrideColor", 17)
        cmds.parent(masterSpace, rigGrp)

        # alias attr master control
        cmds.aliasAttr("globalScale", masterControl + ".scaleZ")
        cmds.connectAttr(masterControl + ".globalScale", masterControl + ".scaleX")
        cmds.connectAttr(masterControl + ".globalScale", masterControl + ".scaleY")
        cmds.setAttr(masterControl + ".scaleX", keyable=False)
        cmds.setAttr(masterControl + ".scaleY", keyable=False)
        cmds.setAttr(masterControl + ".visibility", lock=True, keyable=False)

        # create offset anim control
        offsetControls = riggingUtils.createControlFromMover(rootJoint, networkNode, False, True,
                                                             control_type="fk_rig_control")

        offsetAnim = cmds.rename(offsetControls[0], "offset_anim")

        # mirroring attrs
        for attr in ["invertX", "invertY", "invertZ"]:
            if not cmds.objExists(offsetAnim + "." + attr):
                cmds.addAttr(offsetAnim, ln=attr, at="bool")
            if not cmds.objExists(masterControl + "." + attr):
                cmds.addAttr(masterControl, ln=attr, at="bool")

        cmds.setAttr(offsetAnim + ".invertX", 1)
        cmds.setAttr(masterControl + ".invertX", 1)

        cmds.parent(offsetAnim, masterControl)
        cmds.delete(offsetControls[3])
        cmds.setAttr(offsetAnim + ".overrideEnabled", 1)
        cmds.setAttr(offsetAnim + ".overrideColor", 18)

        for attr in [".visibility", ".scaleX", ".scaleY", ".scaleZ"]:
            cmds.setAttr(offsetAnim + attr, lock=True, keyable=False)

        # create the root control
        rootAnim = riggingUtils.createControl("sphere", 5, "root_anim", False)
        cmds.parent(rootAnim, offsetAnim)
        cmds.makeIdentity(rootAnim, t=1, r=1, s=1, apply=True)
        cmds.setAttr(rootAnim + ".overrideEnabled", 1)
        cmds.setAttr(rootAnim + ".overrideColor", 30)
        cmds.parentConstraint(rootAnim, "driver_root")
        cmds.scaleConstraint(rootAnim, "driver_root")

        for attr in [".visibility", ".scaleX", ".scaleY", ".scaleZ"]:
            cmds.setAttr(rootAnim + attr, lock=True, keyable=False)

        # setup connections to the control network node
        if not cmds.objExists(controlNode + ".rootControls"):
            cmds.addAttr(controlNode, ln="rootControls", at="message")

        for node in [masterControl, offsetAnim, rootAnim]:
            cmds.lockNode(node, lock=False)
            cmds.addAttr(node, ln="controlClass", at="message")
            cmds.connectAttr(controlNode + ".rootControls", node + ".controlClass")

            cmds.addAttr(node, ln="controlType", dt="string")
            cmds.setAttr(node + ".controlType", "FK", type="string")

        # setup default spaces
        cmds.addAttr(masterControl, ln="hasSpaceSwitching", at="bool", dv=1, keyable=False)
        cmds.setAttr(masterControl + ".hasSpaceSwitching", lock=True)
        cmds.addAttr(masterControl, ln="canUseRotationSpace", at="bool", dv=1, keyable=False)
        cmds.setAttr(masterControl + ".canUseRotationSpace", lock=True)
        cmds.addAttr(masterControl, ln="canUseTranslationSpace", at="bool", dv=1, keyable=False)
        cmds.setAttr(masterControl + ".canUseTranslationSpace", lock=True)

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
        Import FBX motion onto this module's rig controls.

        :param importMethod: The import method to be used (options defined in the file attributes)
        :param character: the namespace of the character

        Each module has to define what import methods it offers (at the very top of the module file) and then define
        how motion is imported using those methods.
        """

        returnControls = []

        if importMethod == "Root Motion: Offset":
            cmds.parentConstraint("root", character + ":" + "offset_anim")
            returnControls.append(character + ":" + "offset_anim")

        if importMethod == "Root Motion: Master":
            cmds.parentConstraint("root", character + ":" + "master_anim")
            returnControls.append(character + ":" + "master_anim")

        if importMethod == "Root Motion: Root":
            cmds.parentConstraint("root", character + ":" + "root_anim")
            returnControls.append(character + ":" + "root_anim")

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
        Sets up custom pickwalking between rig controls.

        :return: returns list of top level controls of the module that will need hooks to their parent controls
        """

        # get controls
        controls = self.getControls(False, "rootControls")

        masterCtrl = None
        offsetCtrl = None
        rootCtrl = None

        for control in controls:
            if control.find("master") != -1:
                index = controls.index(control)
                masterCtrl = controls[index]
            if control.find("offset") != -1:
                index = controls.index(control)
                offsetCtrl = controls[index]
            if control.find("root") != -1:
                index = controls.index(control)
                rootCtrl = controls[index]

        # setup pickwalking
        cmds.addAttr(masterCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(offsetCtrl + ".message", masterCtrl + ".pickWalkDown")

        cmds.addAttr(offsetCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(masterCtrl + ".message", offsetCtrl + ".pickWalkUp")

        cmds.addAttr(offsetCtrl, ln="pickWalkDown", at="message")
        cmds.connectAttr(rootCtrl + ".message", offsetCtrl + ".pickWalkDown")

        cmds.addAttr(rootCtrl, ln="pickWalkUp", at="message")
        cmds.connectAttr(offsetCtrl + ".message", rootCtrl + ".pickWalkUp")
