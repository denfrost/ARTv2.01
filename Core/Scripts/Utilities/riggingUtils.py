"""
Author: Jeremy Ernst

This module is a collection of utility functions for generic rigging and skinning tasks.
There are also classes in the module that deal with saving and loading skin weight files.
"""

import json
import os
import time

import maya.cmds as cmds
from maya import OpenMaya, OpenMayaAnim

import mathUtils as mathUtils
import utils as utils


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# GLOBALS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
ATTRIBUTES = ['skinningMethod', 'normalizeWeights', 'dropoffRate',
              'maintainMaxInfluences', 'maxInfluences','bindMethod',
              'useComponents', 'normalizeWeights', 'weightDistribution',
              'heatmapFalloff']


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# FUNCTIONS (STAND-ALONE)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def set_driven_key_frames(driver, driven, driverValue, drivenValues):

    cmds.setAttr(driver, driverValue)
    for i in range(len(driven)):
        cmds.setAttr(driven[i], drivenValues[i])

    cmds.setDrivenKeyframe(driven, cd=driver, itt="linear", ott="linear")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getModuleScaleFactor(elements, attribute, standard):

    length = 0
    for element in elements:
        value = abs(cmds.getAttr(element + "." + attribute))
        length += value

    factor = length/standard
    return factor


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getScaleFactor():

    upAxis = cmds.upAxis(q=True, ax=True)
    index = 5
    if upAxis == "y":
        index = 4

    # ===========================================================================
    # #find meshes
    # ===========================================================================
    weightedMeshes = []
    skinClusters = cmds.ls(type='skinCluster')

    for cluster in skinClusters:
        geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
        geoTransform = cmds.listRelatives(geometry, parent=True)[0]
        weightedMeshes.append(geoTransform)

    # scale factor of 1 = 180cm
    if len(weightedMeshes) > 0:
        scale = cmds.exactWorldBoundingBox(weightedMeshes, ii=True)[index]
        scaleFactor = scale / 180
    else:
        scaleFactor = 1

    return scaleFactor


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createDriverSkeleton():
    # Original Author: Jeremy Ernst

    # ===========================================================================
    # #duplicate the entire skeleton
    # ===========================================================================
    duplicateSkel = cmds.duplicate("root", rc=True)[0]
    cmds.select("root", hi=True)
    joints = cmds.ls(sl=True)

    cmds.select(duplicateSkel, hi=True)
    dupeJoints = cmds.ls(sl=True)

    # ===========================================================================
    # #rename the duplicate joints
    # ===========================================================================
    driverJoints = []
    for i in range(int(len(dupeJoints))):

        if cmds.objExists(dupeJoints[i]):
            driverJoint = cmds.rename(dupeJoints[i], "driver_" + joints[i])
            driverJoints.append(driverJoint)

    # ===========================================================================
    # #create a direct connection between the driver and the export joints
    # ===========================================================================
    for joint in driverJoints:
        exportJoint = joint.partition("driver_")[2]
        cmds.connectAttr(joint + ".translate", exportJoint + ".translate")
        cmds.connectAttr(joint + ".rotate", exportJoint + ".rotate")
        cmds.connectAttr(joint + ".scale", exportJoint + ".scale")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def buildSkeleton():
    # get all of the rig modules in the scene
    modules = utils.returnRigModules()
    renamed = []

    returnData = []
    # go through each one, and find the created bones for that modules
    createdJoints = []
    for module in modules:
        if module != "ART_Root_Module":
            joints = cmds.getAttr(module + ".Created_Bones")
            splitJoints = joints.split("::")

            for bone in splitJoints:
                if bone != "":
                    # create the joint
                    if cmds.objExists(bone):
                        renamed.append(bone + "_renamed")
                        cmds.rename(bone, bone + "_renamed")
                    cmds.select(clear=True)
                    newJoint = cmds.joint(name=str(bone))
                    cmds.select(clear=True)

                    # find the LRA control
                    moduleName = cmds.getAttr(module + ".moduleName")
                    baseName = cmds.getAttr(module + ".baseName")

                    # find prefix/suffix if available
                    prefix = moduleName.partition(baseName)[0]
                    suffix = moduleName.partition(baseName)[2]
                    if prefix == "":
                        prefixSeparator = " "
                    else:
                        prefixSeparator = prefix

                    if suffix == "":
                        suffixSeparator = " "
                    else:
                        suffixSeparator = suffix

                    # get the bone name (for example, thigh)
                    if prefix == "":
                        boneName = bone.partition(suffixSeparator)[0]
                    else:
                        boneName = bone.partition(prefixSeparator)[2].partition(suffixSeparator)[0]

                    # had to make an exception for the chain module since the original logic was operating on a fixed
                    # number of joints
                    if "ART_Chain_Module" in module:
                        boneName = bone.rpartition("_")[2]
                        lra = prefix + baseName + suffix + "_" + boneName + "_lra"

                    else:
                        # get the lra node
                        lra = prefix + baseName + suffix + "_" + boneName + "_lra"
                        lra = lra.replace(" ", "")

                        if not cmds.objExists(lra):
                            lra = prefix + baseName + suffix + "_lra"
                            lra = lra.replace(" ", "")

                    # add this lra/joint pair to our return data
                    returnData.append([newJoint, lra])

                    # position bone at lra
                    constraint = cmds.parentConstraint(lra, newJoint)[0]
                    cmds.delete(constraint)

                    # find parent joint and append data to list
                    if bone != splitJoints[0]:
                        relatives = str(cmds.listRelatives(lra, fullPath=True))
                        relatives = relatives.split("|")
                        relatives = relatives[::-1]
                        for relative in relatives:
                            searchKey = lra.partition("_lra")[0]

                            if relative.find(searchKey) == -1:
                                parentBoneName = relative.partition(moduleName + "_")[2].partition("_mover")[0]
                                if "ART_Chain_Module" in module:
                                    parent = prefix + baseName + suffix + "_" + parentBoneName
                                else:
                                    parent = prefix + parentBoneName + suffix
                                if [bone, parent] not in createdJoints:
                                    createdJoints.append([bone, parent])
                                break
                    else:
                        parent = cmds.getAttr(module + ".parentModuleBone")
                        if [bone, parent] not in createdJoints:
                            createdJoints.append([bone, parent])

        # if this is the root module, it's a bit simpler
        else:
            jointName = cmds.getAttr(module + ".Created_Bones")
            # create the joint
            if cmds.objExists(jointName):
                cmds.warning(
                    "Object with name: " + jointName + " already exists. Renaming object with _renamed suffix.")
                cmds.rename(jointName, jointName + "_renamed")

            cmds.select(clear=True)
            cmds.joint(name=str(jointName))
            cmds.select(clear=True)

    # go through the data and setup the hierarchy now that all bones have been created
    for joint in createdJoints:
        cmds.parent(joint[0], joint[1])

    # freeze rotation transformations
    cmds.makeIdentity("root", t=False, r=True, s=False, apply=True)

    return [returnData, renamed]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createFkRig(joints, networkNode, numRigs, slot):
    # Original Author: Jeremy Ernst

    # lists
    fkControls = []

    # ===========================================================================
    # #take the list of incoming joints and find each joint's mover
    # ===========================================================================
    for joint in joints:
        globalMover = utils.findAssociatedMover(joint, networkNode)

        if globalMover is not None:
            if cmds.objExists(globalMover + ".fk_rig_control"):
                ctrl = cmds.listConnections(globalMover + ".fk_rig_control")[0]
                if cmds.objExists(ctrl):
                    globalMover = ctrl

        # =======================================================================
        # #if a mover is found, duplicate it and unparent the duplicate
        # =======================================================================
        if globalMover is not None:
            dupe = cmds.duplicate(globalMover, rr=True)[0]
            utils.deleteChildren(dupe)
            parent = cmds.listRelatives(dupe, parent=True)
            if parent is not None:
                cmds.parent(dupe, world=True)

            # turn on visiblity of the control
            cmds.setAttr(dupe + ".v", lock=False)
            cmds.setAttr(dupe + ".v", 1)

            # ensure pivot is correct
            cmds.delete(cmds.parentConstraint(joint, dupe)[0])
            piv = cmds.xform(joint, q=True, ws=True, rp=True)
            cmds.xform(dupe, ws=True, rp=piv)

            # rename the control
            fkControl = cmds.rename(dupe, "fk_" + joint + "_anim")
            fkControls.append([joint, fkControl])

            # create a group for the control
            controlGrp = cmds.group(empty=True, name="fk_" + joint + "_anim_grp")
            constraint = cmds.parentConstraint(joint, controlGrp)[0]
            cmds.delete(constraint)

            # parent the control under the controlGrp
            cmds.parent(fkControl, controlGrp)

            # freeze transformations on the control
            cmds.makeIdentity(fkControl, t=1, r=1, s=1, apply=True)

            # color the control
            colorControl(fkControl)

    returnData = None
    createdControls = []

    # ===========================================================================
    # #go through the fk controls data and get the joint parent to create the hierarchy
    # ===========================================================================
    for data in fkControls:
        joint = data[0]
        control = data[1]
        createdControls.append(control)

        # =======================================================================
        # #parent the anim group to the parent control
        # =======================================================================
        parent = cmds.listRelatives(joint, parent=True)
        if parent is not None:
            group = control + "_grp"
            parentControl = "fk_" + parent[0] + "_anim"
            if parent[0] in joints:
                if cmds.objExists(parentControl):
                    cmds.parent(group, parentControl)

            else:
                returnData = group

        # =======================================================================
        # #lastly, connect controls up to blender nodes to drive driver joints
        # =======================================================================
        cmds.pointConstraint(control, "driver_" + joint, mo=True)
        cmds.orientConstraint(control, "driver_" + joint)

        # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
        # input 2, and plugs that into driver joint
        if cmds.objExists("master_anim"):
            globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=joint + "_globalScale")
            cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
            cmds.connectAttr(control + ".scale", globalScaleMult + ".input2")
            createConstraint(globalScaleMult, "driver_" + joint, "scale", False, numRigs, slot, "output")
        else:
            createConstraint(control, "driver_" + joint, "scale", False, numRigs, slot)

    return [returnData, createdControls]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createCounterTwistRig(joints, name, networkNode, startJoint, endJoint, parentGrp, ctrl_group):
    # Original Author: Jeremy Ernst

    # Usage: create a counter twist rig using the incoming joints
    if len(joints) == 0:
        return

    # data lists
    createdGroups = []
    createdControls = []

    # ===========================================================================
    # #create the manual controls for the twist joints
    # ===========================================================================
    for i in range(len(joints)):

        # driven group
        group = cmds.group(empty=True, name=joints[i] + "_driven_grp")

        constraint = cmds.parentConstraint(joints[i], group)[0]
        cmds.delete(constraint)

        # anim group
        animGrp = cmds.duplicate(group, po=True, name=joints[i] + "_anim_grp")[0]
        cmds.parent(group, animGrp)
        createdGroups.append(animGrp)

        # create the twist control
        control = createControlFromMover(joints[i], networkNode, True, False, True, keep_pivot=True)
        twistCtrl = cmds.rename(control, joints[i] + "_anim")
        twist_shape = cmds.listRelatives(twistCtrl, shapes=True)[0]
        cmds.lockNode(twistCtrl, lock=False)
        cmds.setAttr(twist_shape + ".v", lock=False)
        cmds.setAttr(twist_shape + ".v", 1)
        cmds.aliasAttr(twistCtrl + ".scaleZ", rm=True)

        # mirroring attrs
        for attr in ["invertX", "invertY", "invertZ"]:
            if not cmds.objExists(twistCtrl + "." + attr):
                cmds.addAttr(twistCtrl, ln=attr, at="bool")

        cmds.setAttr(twistCtrl + ".invertX", 1)
        cmds.setAttr(twistCtrl + ".invertY", 1)

        createdControls.append(twistCtrl)
        cmds.delete(cmds.parentConstraint(joints[i], twistCtrl)[0])
        cmds.parent(twistCtrl, group)

        cmds.setAttr(twistCtrl + ".v", lock=True, keyable=False)
        cmds.makeIdentity(twistCtrl, t=1, r=1, s=1, apply=True)

        # constrain the driver joint to the twist control
        cmds.parentConstraint(twistCtrl, "driver_" + joints[i])

        # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
        # input 2, and plugs that into driver joint
        if cmds.objExists("master_anim"):
            globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=twistCtrl + "_globalScale")
            cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
            cmds.connectAttr(twistCtrl + ".scale", globalScaleMult + ".input2")
            createConstraint(globalScaleMult, "driver_" + joints[i], "scale", False, 2, 1, "output")
        else:
            createConstraint(twistCtrl, "driver_" + joints[i], "scale", False, 2, 1)

        cmds.refresh()
        colorControl(twistCtrl)

    # ===========================================================================
    # #create the ik twist joint chain
    # ===========================================================================
    cmds.refresh()
    ikTwistUpper = cmds.createNode("joint", name=name + "_counter_twist_ik")
    cmds.delete(cmds.parentConstraint(startJoint, ikTwistUpper)[0])
    ikTwistLower = cmds.createNode("joint", name=name + "_counter_twist_ik_end")
    cmds.delete(cmds.parentConstraint(endJoint, ikTwistLower)[0])

    cmds.parent(ikTwistLower, ikTwistUpper)
    cmds.setAttr(ikTwistUpper + ".v", 0, lock=True)

    # create IK twist extractor chain
    cmds.makeIdentity(ikTwistUpper, t=0, r=1, s=0, apply=True)

    # create IK handle
    twist_ik = cmds.ikHandle(sol="ikRPsolver", name=name + "_counter_twist_ikHandle", sj=ikTwistUpper, ee=ikTwistLower)[0]
    cmds.parent(twist_ik, "driver_" + startJoint)
    cmds.setAttr(twist_ik + ".poleVectorX", 0)
    cmds.setAttr(twist_ik + ".poleVectorY", 0)
    cmds.setAttr(twist_ik + ".poleVectorZ", 0)
    cmds.setAttr(twist_ik + ".v", 0, lock=True)
    cmds.delete(cmds.parentConstraint("driver_" + endJoint, twist_ik)[0])

    # create locator
    twist_tracker = cmds.spaceLocator(name=name + "_twist_tracker")[0]
    cmds.delete(cmds.parentConstraint("driver_" + startJoint, twist_tracker)[0])
    cmds.parent(twist_tracker, "driver_" + startJoint)
    cmds.setAttr(twist_tracker + ".v", 0, lock=True)

    # set rotate order on ik twist joints to yzx
    cmds.setAttr(ikTwistUpper + ".rotateOrder", 1)

    # constrain locator to ikTwistUpper
    cmds.orientConstraint(ikTwistUpper, twist_tracker)

    # Group up controls and parent into rig
    twistGrp = cmds.group(empty=True, name=name + "_counter_twist_grp")
    constraint = cmds.parentConstraint(startJoint, twistGrp)[0]
    cmds.delete(constraint)

    for group in createdGroups:
        cmds.parent(group, twistGrp)

    # ===========================================================================
    # #add twist grp to parent group and add all anim groups to twist group
    # ===========================================================================
    cmds.parent(twistGrp, parentGrp)
    dnt_group = cmds.group(empty=True, name=name + "_twist_extract_grp")
    cmds.delete(cmds.parentConstraint(parentGrp, dnt_group)[0])
    cmds.parent(dnt_group, parentGrp)
    cmds.parentConstraint(ctrl_group, dnt_group, mo=True)
    cmds.parent(ikTwistUpper, dnt_group)

    # constrain the group to the startJoint so it follows with the action of the limb
    cmds.parentConstraint("driver_" + startJoint, twistGrp, mo=True)

    # ===========================================================================
    # #hook up multiply divide nodes
    # ===========================================================================

    # second one takes the output of the counterMultNode and multiplies it with the twist amount
    increment = float(1.0) / float(len(joints))
    defaultValue = 1
    for i in range(len(joints)):
        attrName = joints[i] + "_twistAmt"
        grpName = joints[i] + "_driven_grp"
        cmds.addAttr(name + "_settings", ln=attrName, dv=defaultValue, keyable=True)
        defaultValue -= increment

        # multNode creation
        rollMultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=joints[i] + "_rollNode")
        cmds.connectAttr(twist_tracker + ".rotateX", rollMultNode + ".input1X")
        cmds.connectAttr(name + "_settings." + attrName, rollMultNode + ".input2X")

        # connect output of roll node to driven group
        cmds.connectAttr(rollMultNode + ".outputX", grpName + ".rotateX")

    # add attr on rig settings node for manual twist control visibility
    cmds.addAttr(name + "_settings", longName=(startJoint + "_twistCtrlVis"), at='bool', dv=0, keyable=True)
    cmds.connectAttr(name + "_settings." + startJoint + "_twistCtrlVis", twistGrp + ".v")

    return createdControls


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createTwistRig(joints, name, networkNode, startJoint, endJoint, parentGrp, ctrl_grp):
    """
    Creates a standard twist rig, that takes the twist of a joint and distributes it among the twist joints. There is
    an expectation with this function that the offset mover for the twist joints will be the control.

    :param joints: twist joints
    :param name: module name
    :param networkNode: module network node
    :param startJoint: parent joint of twists
    :param endJoint: joint whose rotation is used to drive twist
    :param parentGrp: module rig group
    :return: created twist controls
    """

    # Usage: create a standard twist rig using the incoming joints
    defaultValue = .75
    createdControls = []

    if len(joints) >= 1:
        # create our roll group
        rollGrp = cmds.group(empty=True, name=name + "_" + startJoint + "_twist_grp")
        cmds.parent(rollGrp, parentGrp)
        cmds.parentConstraint("driver_" + startJoint, rollGrp)
    else:
        return

    # create twist extractor chain
    ik_start_joint = cmds.createNode('joint', name=name + "_" + endJoint + "_ik_start")
    cmds.delete(cmds.parentConstraint(endJoint, ik_start_joint)[0])
    ik_end_joint = cmds.createNode('joint', name=name + "_" + endJoint + "_ik_end")
    cmds.delete(cmds.parentConstraint(startJoint, ik_end_joint)[0])

    cmds.parent(ik_end_joint, ik_start_joint)
    cmds.makeIdentity(ik_start_joint, t=0, r=1, s=0, apply=True)

    twist_ik = cmds.ikHandle(sj=ik_start_joint, ee=ik_end_joint, sol="ikRPsolver",
                             name=name + endJoint + "_twist_ikHandle")[0]
    cmds.setAttr(twist_ik + ".v", 0, lock=True)
    cmds.parent(twist_ik, "driver_" + endJoint)

    for attr in [".poleVectorX", ".poleVectorY", ".poleVectorZ"]:
        cmds.setAttr(twist_ik + attr, 0)

    twist_extractor = cmds.spaceLocator(name=name + "_" + endJoint + "_twist_tracker")[0]
    cmds.delete(cmds.parentConstraint(endJoint, twist_extractor)[0])
    cmds.setAttr(twist_extractor + ".v", 0, lock=True)
    cmds.parent(twist_extractor, "driver_" + endJoint)
    cmds.orientConstraint(ik_start_joint, twist_extractor)

    twist_extract_grp = cmds.group(empty=True, name=name + "_" + endJoint + "_twist_extract_grp")
    cmds.delete(cmds.parentConstraint(endJoint, twist_extract_grp)[0])
    cmds.parent(twist_extract_grp, parentGrp)
    cmds.parentConstraint("driver_" + startJoint, twist_extract_grp, mo=True)

    cmds.parent(ik_start_joint, twist_extract_grp)
    cmds.setAttr(ik_start_joint + ".v", 0, lock=True)

    # create controls and hook up twist
    for i in range(len(joints)):

        # =======================================================================
        # #create the twist ctrl group
        # =======================================================================
        twistCtrlGrp = cmds.group(empty=True, name=joints[i] + "_twist_ctrl_grp")
        constraint = cmds.parentConstraint("driver_" + joints[i], twistCtrlGrp)[0]
        cmds.delete(constraint)

        cmds.parent(twistCtrlGrp, rollGrp)

        # =======================================================================
        # #create the driven twist group
        # =======================================================================
        twistDrivenGrp = cmds.duplicate(twistCtrlGrp, po=True, name=joints[i] + "_twist_driven_grp")[0]
        cmds.delete(cmds.parentConstraint(joints[i], twistDrivenGrp)[0])
        cmds.parent(twistDrivenGrp, twistCtrlGrp)
        cmds.makeIdentity(twistDrivenGrp, t=1, r=1, s=1, apply=True)

        # =======================================================================
        # #create the manual twist control
        # =======================================================================
        control = createControlFromMover(joints[i], networkNode, True, False, True, keep_pivot=True)
        twistCtrl = cmds.rename(control, joints[i] + "_anim")
        twist_shape = cmds.listRelatives(twistCtrl, shapes=True)[0]
        cmds.lockNode(twistCtrl, lock=False)
        cmds.setAttr(twist_shape + ".v", lock=False)
        cmds.setAttr(twist_shape + ".v", 1)
        cmds.aliasAttr(twistCtrl + ".scaleZ", rm=True)

        # mirroring attrs
        for attr in ["invertX", "invertY", "invertZ"]:
            if not cmds.objExists(twistCtrl + "." + attr):
                cmds.addAttr(twistCtrl, ln=attr, at="bool")

        cmds.setAttr(twistCtrl + ".invertX", 1)
        cmds.setAttr(twistCtrl + ".invertY", 1)

        createdControls.append(twistCtrl)
        constraint = cmds.parentConstraint(joints[i], twistCtrl)[0]
        cmds.delete(constraint)
        cmds.setAttr(twistCtrl + ".v", lock=True, keyable=False)

        cmds.parent(twistCtrl, twistDrivenGrp)
        cmds.makeIdentity(twistCtrl, t=1, r=1, s=1, apply=True)
        colorControl(twistCtrl)

        # =======================================================================
        # #drive the twist
        # =======================================================================
        cmds.addAttr(name + "_settings", ln=joints[i] + "_twistAmt", dv=defaultValue, keyable=True)
        twistMultNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=joints[i] + "_mult_node")
        cmds.connectAttr(twist_extractor + ".rx", twistMultNode + ".input1X")
        cmds.connectAttr(name + "_settings." + joints[i] + "_twistAmt", twistMultNode + ".input2X")
        twistInvertNode = cmds.shadingNode("multiplyDivide", asUtility=True, name=joints[i] + "_twist_invert")
        cmds.connectAttr(twistMultNode + ".outputX", twistInvertNode + ".input1X")
        cmds.setAttr(twistInvertNode + ".input2X", -1)
        cmds.connectAttr(twistInvertNode + ".outputX", twistDrivenGrp + ".rx")

        # constrain the driver joint to the twist control
        cmds.parentConstraint(twistCtrl, "driver_" + joints[i])
        cmds.scaleConstraint(twistCtrl, "driver_" + joints[i])

        # plug master control scale into a new mult node that takes joint.scale into input 1, and master.scale into
        # input 2, and plugs that into driver joint
        if cmds.objExists("master_anim"):
            globalScaleMult = cmds.shadingNode("multiplyDivide", asUtility=True, name=twistCtrl + "_globalScale")
            cmds.connectAttr("master_anim.scale", globalScaleMult + ".input1")
            cmds.connectAttr(twistCtrl + ".scale", globalScaleMult + ".input2")
            createConstraint(globalScaleMult, "driver_" + joints[i], "scale", False, 2, 1, "output")
        else:
            createConstraint(twistCtrl, "driver_" + joints[i], "scale", False, 2, 1)

        # increment the default value
        increment = float(0.75) / float(len(joints))
        defaultValue -= increment

    # add attr on rig settings node for manual twist control visibility
    if len(joints) >= 1:
        cmds.addAttr(name + "_settings", longName=(startJoint + "_twistCtrlVis"), at='bool', dv=0, keyable=True)
        cmds.connectAttr(name + "_settings." + startJoint + "_twistCtrlVis", rollGrp + ".v")

    return createdControls


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createControlFromMover(joint, networkNode, orientToJoint, buildSpaceSwitch, useOffset=False, **kwargs):
    # ===========================================================================
    # #take the list of incoming joints and find each joint's mover
    # ===========================================================================
    globalMover = utils.findAssociatedMover(joint, networkNode, useOffset)

    if "control_type" in kwargs:
        if globalMover is not None:
            control_type = kwargs.get("control_type")
            if cmds.objExists(globalMover + "." + control_type):
                ctrl = cmds.listConnections(globalMover + "." + control_type)[0]
                if cmds.objExists(ctrl):
                    globalMover = ctrl

    # ===========================================================================
    # #if a mover is found, duplicate it and unparent the duplicate
    # ===========================================================================
    if globalMover is not None:
        control = cmds.duplicate(globalMover, rr=True)[0]
        utils.deleteChildren(control)

        for attr in [".translateX", ".translateY", ".translateZ", ".rotateX", ".rotateY", ".rotateZ", ".scaleX",
                     ".scaleY", ".scaleZ"]:
            cmds.setAttr(control + attr, lock=False, keyable=True)

        parent = cmds.listRelatives(control, parent=True)
        if parent is not None:
            cmds.parent(control, world=True)

        # turn on visiblity of the control
        cmds.setAttr(control + ".v", lock=False)
        cmds.setAttr(control + ".v", 1)

        if "snap" in kwargs:
            if kwargs["snap"]:
                cmds.delete(cmds.parentConstraint(joint, control)[0])

        # ensure pivot is correct
        if "keep_pivot" not in kwargs:
            piv = cmds.xform(joint, q=True, ws=True, rp=True)
            cmds.xform(control, ws=True, rp=piv)

        if not useOffset:
            # create a group for the control
            controlGrp = cmds.group(empty=True, name=control + "_grp")
            if orientToJoint:
                constraint = cmds.parentConstraint(joint, controlGrp)[0]
            else:
                constraint = cmds.pointConstraint(joint, controlGrp)[0]

            cmds.delete(constraint)

            # parent the control under the controlGrp
            cmds.parent(control, controlGrp)

            # freeze transformations on the control
            cmds.makeIdentity(control, t=1, r=1, s=1, apply=True)

            # =======================================================================
            # #buildSpaceSwitch nodes if needed
            # =======================================================================
            if buildSpaceSwitch:
                spaceSwitchFollow = cmds.duplicate(controlGrp, po=True, name=control + "_space_switcher_follow")[0]
                spaceSwitch = cmds.duplicate(controlGrp, po=True, name=control + "_space_switcher")[0]

                utils.deleteChildren(spaceSwitchFollow)
                utils.deleteChildren(spaceSwitch)

                cmds.parent(spaceSwitch, spaceSwitchFollow)
                cmds.parent(controlGrp, spaceSwitch)

                return [control, controlGrp, spaceSwitch, spaceSwitchFollow]

            else:
                return [control, controlGrp]

        else:
            return control


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createConstraint(target, destination, attr, maintainOffset, numRigs, slot, customAttr=None):
    # Original Author: Jeremy Ernst

    # ===========================================================================
    # #takes the incoming destination and hooks it up to the source using a ramp node
    # ===========================================================================
    if not cmds.objExists(destination + "_" + attr + "_ramp_node"):
        cmds.shadingNode("ramp", asTexture=True, name=destination + "_" + attr + "_ramp_node")
        cmds.setAttr(destination + "_" + attr + "_ramp_node.type", 1)

    # ===========================================================================
    # #if maintainOffset is passed in, store current destination attr values in an add node as an offset
    # ===========================================================================
    if maintainOffset:
        if not cmds.objExists(destination + "_" + attr + "_offset_node_" + str(slot)):
            cmds.shadingNode("plusMinusAverage", asUtility=True,
                             name=destination + "_" + attr + "_offset_node_" + str(slot))

        offsetValues = cmds.getAttr(destination + "." + attr)[0]
        cmds.setAttr(destination + "_" + attr + "_offset_node_" + str(slot) + ".input3D[0]", offsetValues[0],
                     offsetValues[1], offsetValues[2], type="double3")

    # ===========================================================================
    # #if maintainOffset is True, passed in the target attribute into the add node to add with the offset values
    # ===========================================================================
    if maintainOffset:
        cmds.connectAttr(target + "." + attr, destination + "_" + attr + "_offset_node_" + str(slot) + ".input3D[1]")
        cmds.connectAttr(destination + "_" + attr + "_offset_node_" + str(slot) + ".output3D",
                         destination + "_" + attr + "_ramp_node.colorEntryList[" + str(slot) + "].color")

    # ===========================================================================
    # #otherwise, connect target + .attr to the ramp
    # ===========================================================================
    else:
        if customAttr is None:
            cmds.connectAttr(target + "." + attr,
                             destination + "_" + attr + "_ramp_node.colorEntryList[" + str(slot) + "].color")
        else:
            cmds.connectAttr(target + "." + customAttr,
                             destination + "_" + attr + "_ramp_node.colorEntryList[" + str(slot) + "].color")

    # ===========================================================================
    # #get the point position on the ramp for this slot.
    # ===========================================================================
    try:
        pointPos = 1 / (numRigs - 1) * slot
    except:
        pointPos = 0

    cmds.setAttr(destination + "_" + attr + "_ramp_node.colorEntryList[" + str(slot) + "].position", pointPos)

    # ===========================================================================
    # #make the output connection if it doesn't yet exist
    # ===========================================================================
    rampExists = cmds.connectionInfo(destination + "." + attr, isDestination=True)
    if not rampExists:
        cmds.connectAttr(destination + "_" + attr + "_ramp_node.outColor", destination + "." + attr)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def coPlanarModeSnap(instance, snapTarget, snapMover, ikJoints, orientMovers, orientCtrl, skipAttrs):
    # snap the incoming snapMover to snapTarget using the input attribute
    cmds.undoInfo(openChunk=True)
    cmds.cycleCheck(e=False)

    # get current aimState
    for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
        cmds.setAttr(snapMover + attr, lock=False)

    constraint = cmds.pointConstraint(snapTarget, snapMover, skip=skipAttrs)[0]
    cmds.delete(constraint)
    cmds.cycleCheck(e=True)

    for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
        cmds.setAttr(snapMover + attr, lock=True)

    for i in range(len(ikJoints)):
        connection = cmds.connectionInfo(orientMovers[i] + ".rotateX", sourceFromDestination=True)
        aimConstraint = connection.rpartition(".")[0]

        for attr in [[".rx", ".offsetX"]]:
            value = cmds.getAttr(orientCtrl + attr[0])
            cmds.setAttr(aimConstraint + attr[1], value)

    cmds.undoInfo(closeChunk=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def createControl(controlType, size, name, useScaleFactor=True):
    if useScaleFactor:
        scale = getScaleFactor()
    else:
        scale = 1

    if controlType == "circle":
        control = cmds.circle(c=(0, 0, 0), sw=360, r=size * scale, d=3, name=name)[0]

    if controlType == "square":
        control = cmds.circle(c=(0, 0, 0), s=4, sw=360, r=size * scale, d=1, name=name)[0]
        cmds.setAttr(control + ".rz", 45)

    if controlType == "arrow":
        control = cmds.curve(name=name, d=1,
                             p=[(0, -45, 0), (5, -45, 0), (5, -62, 0), (10, -62, 0), (0, -72, 0), (-10, -62, 0),
                                (-5, -62, 0), (-5, -45, 0), (0, -45, 0)])
        cmds.xform(control, cp=True)
        bounds = cmds.exactWorldBoundingBox(control)
        length = abs(bounds[1] - bounds[4]) / 2
        cmds.xform(control, r=True, rp=(0, length, 0), sp=(0, length, 0))
        cmds.move(0, 0, 0, rpr=True)

        cmds.setAttr(control + ".scaleX", size * scale)
        cmds.setAttr(control + ".scaleY", size * scale)
        cmds.setAttr(control + ".scaleZ", size * scale)

    if controlType == "arrowOnBall":
        control = cmds.curve(name=name, d=1, p=[(0.80718, 0.830576, 8.022739), (0.80718, 4.219206, 7.146586),
                                                (0.80718, 6.317059, 5.70073), (2.830981, 6.317059, 5.70073),
                                                (0, 8.422749, 2.94335), (-2.830981, 6.317059, 5.70073),
                                                (-0.80718, 6.317059, 5.70073), (-0.80718, 4.219352, 7.146486),
                                                (-0.80718, 0.830576, 8.022739), (-4.187851, 0.830576, 7.158003),
                                                (-6.310271, 0.830576, 5.705409), (-6.317059, 2.830981, 5.7007),
                                                (-8.422749, 0, 2.94335), (-6.317059, -2.830981, 5.70073),
                                                (-6.317059, -0.830576, 5.70073), (-4.225134, -0.830576, 7.142501),
                                                (-0.827872, -0.830576, 8.017446), (-0.80718, -4.176512, 7.160965),
                                                (-0.80718, -6.317059, 5.70073), (-2.830981, -6.317059, 5.70073),
                                                (0, -8.422749, 2.94335), (2.830981, -6.317059, 5.70073),
                                                (0.80718, -6.317059, 5.70073), (0.80718, -4.21137, 7.151987),
                                                (0.80718, -0.830576, 8.022739), (4.183345, -0.830576, 7.159155),
                                                (6.317059, -0.830576, 5.70073), (6.317059, -2.830981, 5.70073),
                                                (8.422749, 0, 2.94335), (6.317059, 2.830981, 5.70073),
                                                (6.317059, 0.830576, 5.70073), (4.263245, 0.830576, 7.116234),
                                                (0.80718, 0.830576, 8.022739)])

        cmds.setAttr(control + ".scaleX", size * scale)
        cmds.setAttr(control + ".scaleY", size * scale)
        cmds.setAttr(control + ".scaleZ", size * scale)

    if controlType == "semiCircle":
        control = cmds.curve(name=name, d=3,
                             p=[(0, 0, 0), (7, 0, 0), (8, 0, 0), (5, 4, 0), (0, 5, 0), (-5, 4, 0), (-8, 0, 0),
                                (-7, 0, 0), (0, 0, 0)])
        cmds.xform(control, ws=True, t=(0, 5, 0))
        cmds.xform(control, ws=True, piv=(0, 0, 0))
        cmds.makeIdentity(control, t=1, apply=True)

        cmds.setAttr(control + ".scaleX", size * scale)
        cmds.setAttr(control + ".scaleY", size * scale)
        cmds.setAttr(control + ".scaleZ", size * scale)

    if controlType == "pin":
        control = cmds.curve(name=name, d=1, p=[(12, 0, 0), (0, 0, 0), (-12, -12, 0), (-12, 12, 0), (0, 0, 0)])
        cmds.xform(control, ws=True, piv=[12, 0, 0])
        cmds.setAttr(control + ".scaleY", .5)
        cmds.makeIdentity(control, t=1, apply=True)

        cmds.setAttr(control + ".scaleX", size * scale)
        cmds.setAttr(control + ".scaleY", size * scale)
        cmds.setAttr(control + ".scaleZ", size * scale)

    if controlType == "sphere":
        points = [(0, 0, 1), (0, 0.5, 0.866), (0, 0.866025, 0.5), (0, 1, 0), (0, 0.866025, -0.5), (0, 0.5, -0.866025),
                  (0, 0, -1), (0, -0.5, -0.866025), (0, -0.866025, -0.5), (0, -1, 0), (0, -0.866025, 0.5),
                  (0, -0.5, 0.866025), (0, 0, 1), (0.707107, 0, 0.707107), (1, 0, 0), (0.707107, 0, -0.707107),
                  (0, 0, -1), (-0.707107, 0, -0.707107), (-1, 0, 0), (-0.866025, 0.5, 0), (-0.5, 0.866025, 0),
                  (0, 1, 0), (0.5, 0.866025, 0), (0.866025, 0.5, 0), (1, 0, 0), (0.866025, -0.5, 0),
                  (0.5, -0.866025, 0), (0, -1, 0), (-0.5, -0.866025, 0), (-0.866025, -0.5, 0), (-1, 0, 0),
                  (-0.707107, 0, 0.707107), (0, 0, 1)]
        control = cmds.curve(name=name, d=1, p=points)

        cmds.setAttr(control + ".scaleX", size * scale)
        cmds.setAttr(control + ".scaleY", size * scale)
        cmds.setAttr(control + ".scaleZ", size * scale)

    return control


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def colorControl(control, value=False):
    # unlock overrides
    cmds.setAttr(control + ".overrideEnabled", 1)

    if value is False:
        # get the world position of the control
        cmds.refresh(force=True)
        worldPos = cmds.xform(control, q=True, ws=True, t=True)
        if worldPos[0] > 0:
            cmds.setAttr(control + ".overrideColor", 6)
        else:
            cmds.setAttr(control + ".overrideColor", 13)

    else:
        cmds.setAttr(control + ".overrideColor", value)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def fixSkinWeights():
    # get selection
    selection = cmds.ls(sl=True)
    newSelection = []

    # loop through selection getting the shapes and meshes
    for each in selection:
        shapes = cmds.listRelatives(each, shapes=True, pa=True)
        meshes = cmds.ls(shapes, type="mesh")

        # duplicate the object
        duplicateObject = cmds.duplicate(each, rr=True)
        cmds.delete(duplicateObject[0], ch=True)

        newShapes = cmds.listRelatives(duplicateObject[0], shapes=True, pa=True)
        newMeshes = cmds.ls(newShapes, type="mesh")

        # find skinCluster of original object
        skinCluster = findRelatedSkinCluster(each)

        # find bones in skinCluster
        bones = cmds.listConnections(skinCluster + ".matrix", d=True)
        maxInfs = cmds.skinCluster(skinCluster, q=True, mi=True)
        newSkin = cmds.skinCluster(bones, duplicateObject[0], mi=maxInfs, dr=4)[0]
        cmds.copySkinWeights(ss=skinCluster, ds=newSkin, nm=True)

        # rename
        cmds.delete(each)
        newObj = cmds.rename(duplicateObject, each)
        newSelection.append(newObj)

    cmds.select(newSelection)


def export_skin_weights(file_path=None, geometry=None):
    """Exports out skin weight from selected geometry"""
    data = list()
    # error handling
    if not file_path:
        return OpenMaya.MGlobal_displayError("No file path given.")
    if not geometry:
        geometry = _geometry_check(geometry)
        if not geometry:
            return OpenMaya.MGlobal_displayError("No valid geometry.")

    # build up skin data
    skin_clusters = find_skin_clusters(geometry)
    if not skin_clusters:
        skin_message = "No skin clusters found on {0}.".format(geometry)
        OpenMaya.MGlobal_displayWarning(skin_message)
    for skin_cluster in skin_clusters:
        skin_data_init = SkinData(skin_cluster)
        skin_data = skin_data_init.gather_data()
        data.append(skin_data)
        args = [skin_data_init.skin_cluster, file_path]
        export_message = "SkinCluster: {0} has " \
                         "been exported to {1}.".format(*args)
        OpenMaya.MGlobal_displayInfo(export_message)

    # dump data
    file_path = utils.win_path_convert(file_path)
    data = json.dumps(data, sort_keys=True, ensure_ascii=True, indent=2)
    fobj = open(file_path, 'wb')
    fobj.write(data)
    fobj.close()


def find_skin_clusters(nodes):
    """Uses all incoming to search relatives to
    find associated skinCluster.
    @PARAMS:
        nodes: list
    """
    skin_clusters = list()
    if not isinstance(nodes, list):
        nodes = [nodes]
    relatives = cmds.listRelatives(nodes, ad=True, path=True)
    all_incoming = utils.find_all_incoming(relatives)
    for node in all_incoming:
        if cmds.nodeType(node) == "skinCluster":
            if node not in skin_clusters:
                skin_clusters.append(node)
    return skin_clusters


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findRelatedSkinCluster(object):
    skinClusters = cmds.ls(type='skinCluster')

    for cluster in skinClusters:
        geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
        geoTransform = cmds.listRelatives(geometry, parent=True)[0]

        dagPath = cmds.ls(geoTransform, long=True)[0]

        if geoTransform == object:
            return cluster
        elif dagPath == object:
            return cluster


def import_skin_weights(file_path=None, geometry=None, remove_unused=None):
    # error handling
    if not file_path:
        return OpenMaya.MGlobal_displayError("No file path given.")
    if not geometry:
        return

    # load data
    if not os.path.exists(file_path):
        path_message = "Could not find {0} file.".format(file_path)
        return OpenMaya.MGlobal_displayWarning(path_message)

    fobj = open(file_path, "rb")
    data = json.load(fobj)

    # check verts
    vert_check = _vert_check(data, geometry)
    if not vert_check:
        return

    # import skin weights
    _import_skin_weights(data, geometry, file_path, remove_unused)


def _import_skin_weights(data, geometry, file_path, remove_unused=None):
    # loop through skin data
    for skin_data in data:
        geometry = skin_data["shape"]
        if not cmds.objExists(geometry):
            continue

        skin_clusters = find_skin_clusters(geometry)
        if skin_clusters:
            skin_cluster = SkinData(skin_clusters[0])
            skin_cluster.set_data(skin_data)
        else:
            # TODO: make joint remapper, Chris has a setup for this already
            skin_cluster = _create_new_skin_cluster(skin_data, geometry)
            if not skin_cluster:
                continue
            skin_cluster[0].set_data(skin_data)
        if remove_unused:
            if skin_clusters:
                _remove_unused_influences(skin_clusters[0])
            else:
                _remove_unused_influences(skin_cluster[1])
        OpenMaya.MGlobal_displayInfo("Imported {0}".format(file_path))


def _vert_check(data, geometry):
    # check vertex count
    for skin_data in data:
        geometry = skin_data["shape"]
        vert_count = cmds.polyEvaluate(geometry, vertex=True)
        import_vert_count = len(skin_data["blendWeights"])
        if vert_count != import_vert_count:
            vert_message = "The vert count does not match for this geometry: " + str(geometry)
            return OpenMaya.MGlobal_displayError(vert_message)
    return True


def _create_new_skin_cluster(skin_data, geometry):
    # check joints
    joints = skin_data["weights"].keys()
    unused_joints = list()
    scene_joints = set([utils.remove_namespace(joint) for joint \
                        in cmds.ls(type="joint")])
    for joint in joints:
        if not joint in scene_joints:
            unused_joints.append(joint)
    # TODO: make joint remapper, Chris has a setup for this already
    if unused_joints and not scene_joints:
        return
    try:
        skin_cluster = cmds.skinCluster(joints, geometry, tsb=True, nw=2,
                                        n=skin_data["skinCluster"])[0]

        return (SkinData(skin_cluster), skin_cluster)

    except Exception:
        pass


def _remove_unused_influences(skin_cluster):
    influences_to_remove = list()
    weighted_influences = cmds.skinCluster(skin_cluster, q=True, wi=True)
    final_transforms = cmds.skinCluster(skin_cluster, q=True, inf=True)
    for influence in final_transforms:
        if influence not in weighted_influences:
            influences_to_remove.append(influence)
    for influence in influences_to_remove:
        cmds.skinCluster(skin_cluster, e=True, ri=influence)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CLASSES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SkinWeights(object):
    '''
    Takes in a .WEIGHTS file from disk, an existing skinCluster, or a skinned mesh as inputs
    If qtProgbar == 'internal' then it will generate a modal progbar
    '''

    def __init__(self, skinFile=None, skinCluster=None, mesh=None):
        self.skin = None
        self.vertices = None
        self.skinFile = None
        self.mesh = None
        self.uvSet = None
        self.numVerts = None
        self.skinDict = None
        self.joints = []
        self.applied = False

        # TODO: check that the file is really on disk
        if skinFile:
            if os.path.exists(skinFile):
                self.skinDict = self.importSkinFile(skinFile)
                self.skinFile = skinFile
            else:
                cmds.warning('riggingUtils.SkinWeights: cannot find file on disk: ' + skinFile)
        if skinCluster:
            if cmds.objExists(skinCluster):
                self.skin = skinCluster
                self.mesh = cmds.listConnections(skinCluster + '.outputGeometry')[0]
            else:
                cmds.warning('riggingUtils.SkinWeights: cannot find skinCluster: ' + skinCluster)
        if mesh:
            if cmds.objExists(mesh):
                self.mesh = mesh
                sk = findRelatedSkinCluster(mesh)
                if sk:
                    self.skin = sk
                else:
                    cmds.warning('riggingUtils.SkinWeights: mesh has no skinCluster: ' + mesh)
            else:
                cmds.warning('riggingUtils.SkinWeights: Cannot find mesh: ' + mesh)

    def exportSkinWeights(self, filePath, qtProgbar=None, freq=1):
        time1 = time.time()
        vertPoints = cmds.getAttr(self.mesh + '.vtx[*]')

        f = {}
        header = {}
        vtxDict = {}
        skin = findRelatedSkinCluster(self.mesh)

        numVerts = cmds.polyEvaluate(self.mesh, vertex=1)

        # fill header
        header['mesh'] = self.mesh
        header['skinCluster'] = skin
        header['numVerts'] = numVerts
        header['uvSet'] = cmds.polyUVSet(self.mesh, currentUVSet=1, q=1)[0]

        # fill vtxDict
        if qtProgbar == 'internal':
            from Utilities.interfaceUtils import progressDialog
            qtProgbar = progressDialog((0, numVerts), label="Exporting skin weights...")
        elif qtProgbar:
            qtProgbar.setRange(0, numVerts)
            qtProgbar.setValue(0)
        for vtx in range(0, numVerts):
            vtxDict[vtx] = {}
            vtxDict[vtx]['world'] = tuple(cmds.pointPosition(self.mesh + '.vtx[' + str(vtx) + ']', w=1))
            vtxDict[vtx]['local'] = tuple(cmds.pointPosition(self.mesh + '.vtx[' + str(vtx) + ']', l=1))
            # we will loop all the skinning influences of this vertex and record their names and values
            vtxDict[vtx]['skinning'] = []

            joints = cmds.skinPercent(skin, self.mesh + '.vtx[' + str(vtx) + ']', q=1, t=None)
            influence_value = cmds.skinPercent(skin, self.mesh + '.vtx[' + str(vtx) + ']', q=True, v=True)

            for jnt, val in zip(joints, influence_value):
                if val > 0:
                    vtxDict[vtx]['skinning'].append([jnt, val])

            uv = cmds.polyListComponentConversion(self.mesh + ".vtx[" + str(vtx) + "]", fv=True, tuv=True)
            vtxDict[vtx]['uv'] = cmds.polyEditUV(uv, q=True)
            if qtProgbar:
                qtProgbar.setValue(vtx)

        f['header'] = header
        f['vtxDict'] = vtxDict
        wFile = file(filePath, mode='w')
        wFile.write(json.dumps(f, wFile, indent=4))
        wFile.close()

        # TODO: validate this
        time2 = time.time()
        print 'exportSkinWeights: Weights saved to: %s in %0.3f sec' % (filePath, (time2 - time1))
        return True

    def importSkinFile(self, filePath):
        import json
        if os.path.exists(filePath):
            f = open(filePath, 'r')
            self.skinDict = json.load(f)
            f.close()

            self.skin = self.skinDict['header']['skinCluster']
            self.mesh = self.skinDict['header']['mesh']
            self.uvSet = self.skinDict['header']['uvSet']
            self.numVerts = self.skinDict['header']['numVerts']
            self.vertices = self.skinDict['vtxDict']

            for vtx in self.skinDict['vtxDict']:
                # build joint list
                for inf in self.skinDict['vtxDict'][vtx]['skinning']:
                    if inf[0] not in self.joints:
                        self.joints.append(inf[0])

    # This validates that the influence joints exist
    def verifiedInfluences(self, joints):
        jointsInScene = []
        for jnt in joints:
            if cmds.objExists(jnt):
                jointsInScene.append(jnt)
            else:
                cmds.warning('SKIN WEIGHT IMPORT: Cannot find joint that matches', jnt, 'in the current scene.')
        return jointsInScene

    def square_distance(self, pointA, pointB):
        # squared euclidean distance
        distance = 0
        dimensions = len(pointA)  # assumes both points have the same dimensions
        for dimension in range(dimensions):
            distance += (pointA[dimension] - pointB[dimension]) ** 2
        return distance

    # Toss the UV list to a point array
    def uvListToPointArray(self, uvPoints):
        returnArray = []
        if len(uvPoints) > 2:
            for i in range(0, len(uvPoints), 2):
                newPos = [uvPoints[i], uvPoints[i + 1]]
                if len(newPos) != 2:
                    cmds.error(newPos + ' not 2d!')
                returnArray.append(newPos)
        else:
            returnArray.append(uvPoints)
        return returnArray

    def applySkinWeights(self, mesh, applyBy='Vertex Order', killSkin=0, debug=0, qtProgbar=None):
        self.skin = findRelatedSkinCluster(mesh)

        # remove existing skin cluster
        if self.skin and killSkin or not self.skin:
            if killSkin:
                bindposes = cmds.listConnections(self.skin + '.bindPose')
                bindposes.append(self.skin)
                for obj in bindposes:
                    cmds.delete(obj)
            bind = self.verifiedInfluences(self.joints)
            bind.append(mesh)
            sel = cmds.ls(sl=1)
            cmds.select(cl=1)
            cmds.select(bind)
            self.skin = cmds.skinCluster(skinMethod=0, name=(mesh.split('|')[-1] + "_skinCluster"))[0]
            cmds.select(sel)

        if self.skin:
            # build kdTree if required
            vtxDict = {}
            vtxList = []
            vtxTree = None

            # parse weight file
            if applyBy == 'World Position':
                for vtx in self.vertices:
                    pos = self.vertices[vtx]['world']
                    vtxDict[str(pos)] = vtx
                    vtxList.append(pos)
                start = time.time()
                vtxTree = mathUtils.KDTree.construct_from_data(vtxList)
                elapsed = (time.time() - start)
            if applyBy == 'Local Position':
                for vtx in self.vertices:
                    pos = self.vertices[vtx]['local']
                    vtxDict[str(pos)] = vtx
                    vtxList.append(pos)
                start = time.time()
                vtxTree = mathUtils.KDTree.construct_from_data(vtxList)
                elapsed = (time.time() - start)
            if applyBy == 'UV Position':
                for vtx in self.vertices:
                    pos = self.vertices[vtx]['uv']
                    # When one vtx has multiple UV locations, we add it to the mapping table once for each location
                    if len(pos) > 2:
                        for i in range(0, len(pos), 2):
                            newPos = [pos[i], pos[i + 1]]
                            if debug:
                                print 'NEWPOS:', newPos
                            if len(newPos) > 2:
                                cmds.error(newPos + ' not 2d!')
                            vtxDict[str(newPos)] = vtx
                            vtxList.append(newPos)

                    else:
                        vtxDict[str(pos)] = vtx
                        vtxList.append(pos)
                if debug:
                    print 'VTXLIST:', vtxList
                    print 'VTXDICT:', vtxDict
                start = time.time()
                vtxTree = mathUtils.KDTree.construct_from_data(vtxList)
                elapsed = (time.time() - start)

            verts = cmds.polyEvaluate(mesh, vertex=1)
            # progress bar
            if qtProgbar == 'internal':
                from Utilities.interfaceUtils import progressDialog
                qtProgbar = progressDialog((0, verts), label="Importing skin weights...")
            elif qtProgbar:
                qtProgbar.setRange(0, verts)
                qtProgbar.setValue(0)

            # set the weights
            try:
                cmds.undoInfo(openChunk=True)
                time1 = time.time()
                for vtx in range(0, verts):
                    if applyBy == 'Vertex Order':
                        # TODO: check if numVerts match
                        cmds.skinPercent(self.skin, mesh + ".vtx[" + str(vtx) + "]",
                                         transformValue=self.vertices[str(vtx)]['skinning'])
                    if applyBy == 'World Position':
                        if vtxTree:
                            vtxPos = \
                                vtxTree.query(tuple(cmds.pointPosition(mesh + '.vtx[' + str(vtx) + ']', w=1)), t=1)[0]
                            vtxMaya = mesh + '.vtx[' + str(vtx) + ']'
                            if debug:
                                print 'Original vertex', vtxDict[str(vtxPos)], 'maps to new vtx', vtxMaya
                            cmds.skinPercent(self.skin, vtxMaya,
                                             transformValue=self.vertices[vtxDict[str(vtxPos)]]['skinning'])
                        else:
                            cmds.warning('IMPORT SKIN WEIGHTS: No existing kdTree built.')
                    if applyBy == 'Local Position':
                        if vtxTree:
                            vtxPos = vtxTree.query(tuple(cmds.pointPosition(mesh + '.vtx[' + str(vtx) + ']')), t=1)[0]
                            vtxMaya = mesh + '.vtx[' + str(vtx) + ']'
                            if debug:
                                print 'Original vertex', vtxDict[str(vtxPos)], 'maps to new vtx', vtxMaya
                            cmds.skinPercent(self.skin, vtxMaya,
                                             transformValue=self.vertices[vtxDict[str(vtxPos)]]['skinning'])
                        else:
                            cmds.warning('IMPORT SKIN WEIGHTS: No existing kdTree built.')
                    if applyBy == 'UV Space':
                        if vtxTree:
                            uvPoint = cmds.polyEditUV(
                                    cmds.polyListComponentConversion(mesh + ".vtx[" + str(vtx) + "]", fv=True,
                                                                     tuv=True),
                                    q=1)
                            pos = self.uvListToPointArray(uvPoint)
                            vtxPos = None

                            if debug:
                                print 'uvPoint:', uvPoint
                                print 'pos:', pos
                            # check for multiple uv points assoc with the vert
                            if len(pos) > 1:
                                distance = None
                                vtxPos = None
                                for p in pos:
                                    if debug:
                                        print pos
                                        print p
                                    closest = vtxTree.query(tuple(p), t=1)[0]
                                    dist = self.square_distance(p, closest)
                                    if not distance:
                                        distance = dist
                                        vtxPos = closest
                                    else:
                                        if dist < distance:
                                            distance = dist
                                            vtxPos = closest

                            else:
                                vtxPos = vtxTree.query(tuple(pos[0]), t=1)[0]
                            vtxMaya = mesh + '.vtx[' + str(vtx) + ']'
                            if debug:
                                print 'vtxPos:', str(vtxPos)
                                print 'Original UV vertex', vtxDict[str(vtxPos)], 'maps to new UV vtx', vtxMaya
                                print 'SKINNING:', self.vertices[vtxDict[str(vtxPos)]]['skinning'], vtxDict[str(vtxPos)]
                            cmds.skinPercent(self.skin, vtxMaya,
                                             transformValue=self.vertices[vtxDict[str(vtxPos)]]['skinning'])
                        else:
                            cmds.warning('IMPORT SKIN WEIGHTS: No existing kdTree built.')

                    # Update the progressbar, but only every 100th vertex
                    if qtProgbar:
                        if vtx % 100 == 0 or (vtx + 1) == verts:
                            qtProgbar.setValue(vtx + 1)
                time2 = time.time()
                print 'importSkinWeights: Weights loaded from %s in %0.3f sec' % (self.skinFile, (time2 - time1))
            except Exception as e:
                print e
            finally:
                cmds.undoInfo(closeChunk=True)

        else:
            cmds.warning('IMPORT SKIN WEIGHTS: No skinCluster found on: ' + mesh)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SkinData(object):
    def __init__(self, skin_cluster):

        # globals/data
        self.skin_cluster = skin_cluster
        deformer = cmds.deformer(skin_cluster, q=True, g=True)[0]
        self.shape = cmds.listRelatives(deformer, parent=True, path=True)[0]
        self.mobject = utils.get_mobject(self.skin_cluster)
        self.skin_set = OpenMayaAnim.MFnSkinCluster(self.mobject)
        self.data = {
            "weights": dict(),
            "blendWeights": list(),
            "skinCluster": self.skin_cluster,
            "shape": self.shape
        }

    def gather_data(self):

        # get incluence and blend weight data
        dag_path, mobject = self.get_skin_dag_path_and_mobject()
        self.get_influence_weights(dag_path, mobject)
        self.get_blend_weights(dag_path, mobject)

        # add in attribute data
        for attribute in ATTRIBUTES:
            self.data[attribute] = cmds.getAttr("{0}.{1}". \
                                                format(self.skin_cluster,
                                                       attribute))
        return self.data

    def get_skin_dag_path_and_mobject(self):
        function_set = OpenMaya.MFnSet(self.skin_set.deformerSet())
        selection_list = OpenMaya.MSelectionList()
        function_set.getMembers(selection_list, False)
        dag_path = OpenMaya.MDagPath()
        mobject = OpenMaya.MObject()
        selection_list.getDagPath(0, dag_path, mobject)
        return dag_path, mobject

    def get_influence_weights(self, dag_path, mobject):
        weights = self._get_weights(dag_path, mobject)

        influence_paths = OpenMaya.MDagPathArray()
        influence_count = self.skin_set.influenceObjects(influence_paths)
        components_per_influence = weights.length() / influence_count
        for count in xrange(influence_paths.length()):
            name = influence_paths[count].partialPathName()
            name = utils.remove_namespace(name)
            weight_data = [weights[influence * influence_count + count] \
                           for influence in xrange(components_per_influence)]
            self.data["weights"][name] = weight_data

    def _get_weights(self, dag_path, mobject):
        """Where the API magic happens."""
        weights = OpenMaya.MDoubleArray()
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        pointer = util.asUintPtr()

        # magic call
        self.skin_set.getWeights(dag_path, mobject, weights, pointer);
        return weights

    def get_blend_weights(self, dag_path, mobject):
        return self._get_blend_weights(dag_path, mobject)

    def _get_blend_weights(self, dag_path, mobject):
        weights = OpenMaya.MDoubleArray()

        # magic call
        self.skin_set.getBlendWeights(dag_path, mobject, weights)
        blend_data = [weights[blend_weight] for \
                      blend_weight in xrange(weights.length())]
        self.data["blendWeights"] = blend_data

    def set_data(self, data):
        """Final point for importing weights. Sets and applies influences
        and blend weight values.
        @PARAMS:
            data: dict()
        """
        self.data = data
        dag_path, mobject = self.get_skin_dag_path_and_mobject()
        self.set_influence_weights(dag_path, mobject)
        self.set_blend_weights(dag_path, mobject)

        # set skinCluster Attributes
        for attribute in ATTRIBUTES:
            cmds.setAttr('{0}.{1}'.format(self.skin_cluster, attribute),
                         self.data[attribute])

    def set_influence_weights(self, dag_path, mobject):
        weights = self._get_weights(dag_path, mobject)
        influence_paths = OpenMaya.MDagPathArray()
        influence_count = self.skin_set.influenceObjects(influence_paths)
        components_per_influence = weights.length() / influence_count

        # influences
        unused_influences = list()
        influences = [influence_paths[inf_count].partialPathName() for \
                      inf_count in xrange(influence_paths.length())]

        # build influences/weights
        for imported_influence, imported_weights in self.data['weights'].items():
            for inf_count in xrange(influence_paths.length()):
                influence_name = influence_paths[inf_count].partialPathName()
                influence_name = utils.remove_namespace(influence_name)
                if influence_name == imported_influence:
                    # set the weights
                    for count in xrange(components_per_influence):
                        weights.set(imported_weights[count],
                                    count * influence_count + inf_count)
                    influences.remove(influence_name)
                    break
            else:
                unused_influences.append(imported_influence)

        # TODO: make joint remapper
        if unused_influences and influences:
            OpenMaya.MGlobal_displayWarning("Make a joint remapper, Aaron!")

        # set influences
        influence_array = OpenMaya.MIntArray(influence_count)
        for count in xrange(influence_count):
            influence_array.set(count, count)
        # set weights
        self.skin_set.setWeights(dag_path, mobject, influence_array, weights, False)

    def set_blend_weights(self, dag_path, mobject):
        blend_weights = OpenMaya.MDoubleArray(len(self.data['blendWeights']))
        for influence, weight in enumerate(self.data['blendWeights']):
            blend_weights.set(weight, influence)
        self.skin_set.setBlendWeights(dag_path, mobject, blend_weights)
