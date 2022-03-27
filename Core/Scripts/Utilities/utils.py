"""
Author: Jeremy Ernst

########
Contents
########

|   **Node Traversal Utilities:**
|       :func:`returnRigModules <Utilities.utils.returnRigModules>`
|       :func:`returnCharacterModule <Utilities.utils.returnCharacterModule>`
|       :func:`returnCharacterModules <Utilities.utils.returnCharacterModules>`
|       :func:`returnRigModuleTypes <Utilities.utils.returnRigModuleTypes>`
|       :func:`getViableParents <Utilities.utils.getViableParents>`
|       :func:`deleteChildren <Utilities.utils.deleteChildren>`
|       :func:`find_all_incoming <Utilities.utils.find_all_incoming>`
|
|   **Joint Mover Utilities:**
|       :func:`findAndRenameOutlinerChildren <Utilities.utils.findAndRenameOutlinerChildren>`
|       :func:`findAssociatedMover <Utilities.utils.findAssociatedMover>`
|       :func:`findMoverNodeFromJointName <Utilities.utils.findMoverNodeFromJointName>`
|       :func:`findOffsetMoverFromName <Utilities.utils.findOffsetMoverFromName>`
|       :func:`findGlobalMoverFromName <Utilities.utils.findGlobalMoverFromName>`
|
|   **Mesh Utilities:**
|       :func:`splitMesh <Utilities.utils.splitMesh>`
|       :func:`findAllSkinnableGeo <Utilities.utils.findAllSkinnableGeo>`
|       :func:`getLodData <Utilities.utils.getLodData>`
|       :func:`exportMesh <Utilities.utils.exportMesh>`
|       :func:`findExportMeshData <Utilities.utils.findExportMeshData>`
|       :func:`getFaceMaterials <Utilities.utils.getFaceMaterials>`
|
|   **Path Utilities:**
|       :func:`win_path_convert <Utilities.utils.win_path_convert>`
|       :func:`returnFriendlyPath <Utilities.utils.returnFriendlyPath>`
|       :func:`returnNicePath <Utilities.utils.returnNicePath>`
|
|   **Misc. Utilities:**
|       :func:`fitViewAndShade <Utilities.utils.fitViewAndShade>`
|       :func:`fitSelection <Utilities.utils.fitSelection>`
|       :func:`get_mobject <Utilities.utils.get_mobject>`
|       :func:`get_namespace <Utilities.utils.get_namespace>`
|       :func:`remove_namespace <Utilities.utils.remove_namespace>`
|
|

#########
Functions
#########
"""

import json
import os
import re
import traceback

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya, OpenMayaAnim
import maya.api.OpenMaya as api


import interfaceUtils as interfaceUtils
import riggingUtils as riggingUtils
from ThirdParty.Qt import QtWidgets, QtCore

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


class MirrorTable(object):

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def __init__(self):
        """
        In Progress: Used to build mirror table for pose mirroring. Currently run by hand, but needs to be run after rig
        build. Also, control invert values need to be manually set, and this needs to be changed. Invert axis attributes
        should be added before this, and the values set on the controls after control creation.
        """

        character = returnCharacterModule()
        modules = cmds.listConnections(character + ".rigModules")

        self.mirror_table = []
        self.unique_controls = []

        # find modules that have mirrors
        mirror_module_pairs = self._find_module_mirrors(modules)

        self._find_mirror_controls(mirror_module_pairs)

        # create origin locator
        origin_joint = find_origin_control()
        if cmds.objExists("mirror_origin"):
            cmds.lockNode("mirror_origin", lock=False)
            cmds.delete("mirror_origin")

        origin_transform = cmds.group(empty=True, name="mirror_origin")
        cmds.parent(origin_transform, "rig_grp")
        cmds.delete(cmds.pointConstraint(origin_joint, origin_transform)[0])
        cmds.pointConstraint(origin_joint, origin_transform, mo=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_mirror_controls(self, mirror_pairs):

        for key in mirror_pairs.keys():
            src_ctrl_node = cmds.listConnections(key + ".controls")[0]
            value = mirror_pairs.get(key)

            if value is not None:
                mir_ctrl_node = cmds.listConnections(value + ".controls")[0]
                attrs = cmds.listAttr(src_ctrl_node, ud=True)
                for attr in attrs:
                    self._find_matching_mirror_control(key, value, attr, src_ctrl_node, mir_ctrl_node)

                for each in self.unique_controls:
                    if not cmds.objExists(each + ".unique"):
                        cmds.addAttr(each, ln="unique", at="bool")
                    cmds.setAttr(each + ".unique", True)

                for each in self.mirror_table:
                    self._setup_mirroring(each)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _setup_mirroring(self, mirrored_control_pair):

        if mirrored_control_pair[0] is not None:
            if mirrored_control_pair[1] is not None:
                if not cmds.objExists(mirrored_control_pair[0] + ".mirror"):
                    cmds.addAttr(mirrored_control_pair[0], ln="mirror", at="message")
                else:
                    connection = cmds.listConnections(mirrored_control_pair[0] + ".mirror", source=False)
                    if connection is not None:
                        cmds.disconnectAttr(mirrored_control_pair[0] + ".mirror", connection[0] + ".mirror")
                if not cmds.objExists(mirrored_control_pair[1] + ".mirror"):
                    cmds.addAttr(mirrored_control_pair[1], ln="mirror", at="message")
                if mirrored_control_pair[0] != mirrored_control_pair[1]:
                    cmds.connectAttr(mirrored_control_pair[0] + ".mirror", mirrored_control_pair[1] + ".mirror")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_matching_mirror_control(self, source_mod, mirror_mod, attr, src_ctrls, mir_ctrls):

        controls = cmds.listConnections(src_ctrls + "." + attr, source=False)
        if controls is not None:
            if cmds.objExists(mir_ctrls + "." + attr):
                mirror_controls = cmds.listConnections(mir_ctrls + "." + attr, source=False)
                if mirror_controls is not None:
                    if len(controls) == len(mirror_controls):
                        for control, mirror_control in map(None, controls, mirror_controls):
                            self.mirror_table.append([control, mirror_control])
                    else:
                        self._find_unique_controls(source_mod, mirror_mod, controls, mirror_controls)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_unique_controls(self, source_mod, mirror_mod, controls, mirror_controls):

        source_module_name = cmds.getAttr(source_mod + ".moduleName")
        source_base_name = cmds.getAttr(source_mod + ".baseName")
        mirror_module_name = cmds.getAttr(mirror_mod + ".moduleName")
        mirror_base_name = cmds.getAttr(mirror_mod + ".baseName")

        source_prefix_suffix = get_prefix_suffix(source_module_name, source_base_name)
        mirror_prefix_suffix = get_prefix_suffix(mirror_module_name, mirror_base_name)

        for control in controls:
            self._identify_if_unique(control, source_prefix_suffix, mirror_prefix_suffix)

        for mirror_control in mirror_controls:
            self._identify_if_unique(mirror_control, mirror_prefix_suffix, source_prefix_suffix)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _identify_if_unique(self, control, source_name_data, mirror_name_data):

        search = control
        if source_name_data[0] is not None:
            search = control.replace(source_name_data[0], mirror_name_data[0])
        if source_name_data[1] is not None:
            search = control.replace(source_name_data[1], mirror_name_data[1])

        if search != control:
            if cmds.objExists(search):
                self.mirror_table.append([control, search])
            else:
                self.unique_controls.append(control)
        else:
            self.unique_controls.append(control)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_module_mirrors(self, modules):

        pairs = {}
        module_dict = create_module_dict()

        for module_node in modules:
            if cmds.getAttr(module_node + ".mirrorModule") is not None:
                mirror_name = cmds.getAttr(module_node + ".mirrorModule")
                mirror_module_node = module_dict.get(mirror_name)
                if module_node not in pairs.values():
                    pairs[module_node] = mirror_module_node
            else:
                if module_node not in pairs.values():
                    pairs[module_node] = module_node

        return pairs


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnRigModules():
    """
    Look for all network nodes in the scene. Return network nodes that have a .parent attribute.

    :return: list of network nodes that have .parent attr, signifying an ART network node
    """

    modules = []
    networkNodes = cmds.ls(type="network")

    if "ART_Root_Module" in networkNodes:
        modules.append("ART_Root_Module")
        index = networkNodes.index("ART_Root_Module")
        networkNodes.pop(index)

    for node in networkNodes:
        attrs = cmds.listAttr(node)
        if "parent" in attrs:
            modules.append(node)

    return modules


def return_module_instances():

    network_nodes = returnRigModules()

    instances = []

    for node in network_nodes:
        niceName = cmds.getAttr(node + ".moduleName")
        moduleType = cmds.getAttr(node + ".moduleType")
        mod = __import__("RigModules." + moduleType, {}, {}, [moduleType])

        # find the instance of that module
        moduleClass = getattr(mod, mod.className)
        moduleInst = moduleClass(None, niceName)
        instances.append(moduleInst)

    return instances

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnCharacterModule():
    """
    Look for all network nodes in the scene. Return the main network node that all other ART network nodes
    connect to (also known as the character node)

    :return: character node that stores character information.
    """

    networkNodes = cmds.ls(type="network")
    for node in networkNodes:
        attrs = cmds.listAttr(node)

        if "parent" not in attrs:
            if "rigModules" in attrs:
                return node


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnCharacterModules():
    """
    Look for all network nodes in the scene. Return all character network nodes found.

    :return: list of character network nodes which list details about the character.
    """

    modules = []
    networkNodes = cmds.ls(type="network")
    for node in networkNodes:
        attrs = cmds.listAttr(node)

        if "parent" not in attrs:
            if "rigModules" in attrs:
                modules.append(node)

    return modules


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnRigModuleTypes():
    """
    Look for all network nodes in the scene. Get the moduleType attribute value for any valid nodes and
    append that to our list of modules to return, giving us a list of all of the types of modules our character
    has.

    :return: list of the different types of modules in our scene (ART_Arm, ART_Leg, etc)
    """

    modTypes = []
    networkNodes = cmds.ls(type="network")
    for node in networkNodes:
        attrs = cmds.listAttr(node)

        if "parent" in attrs:
            modType = cmds.getAttr(node + ".moduleType")
            if modType not in modTypes:
                modTypes.append(modType)

    return modTypes


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getViableParents():
    """
    Look for all network nodes in the scene, and search for the Created_Bones attribute, which holds the names
    of the bones a particular module will create given its current settings. Add all created bones from all modules
    to a list to be returned.

    :return: list of all the bone names created by the current modules in the scene.
    """

    # look through the node network and find created bone lists
    modules = returnRigModules()

    bonesList = []
    for module in modules:
        if cmds.objExists(module + ".Created_Bones"):
            bonesList.append(cmds.getAttr(module + ".Created_Bones"))

    # now we have a long string of all of the created bones. we need to split them up into individual items
    parents = []
    for bone in bonesList:
        bones = bone.split("::")

        for bone in reversed(bones):
            if bone != "":
                parents.append(bone)

    # once done, add each one to the comboBox
    return parents


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findMoverNodeFromJointName(networkNodes, jointName, offsetMover=True, globalMover=False):
    """
    Look for the passed in joint name in the Created_Bones attribute of all network nodes in the scene.
    Once found, find the joint's associated offset or global mover.

    :param networkNodes: list of network nodes to search for jointName in Created_Bones attribute
    :param jointName: name of joint whose mover (offset or global) we are trying to find
    :param offsetMover: Whether to return the offset mover
    :param globalMover: Whether to return the global mover
    :return: the name of the associated joint mover for the given joint
    """

    # take the passed in list, and if there is a created_Bones attribute, search it for the jointName
    for node in networkNodes:
        boneList = []
        if cmds.objExists(node + ".Created_Bones"):
            boneList.append(cmds.getAttr(node + ".Created_Bones"))
        for bone in boneList:
            splitBones = bone.split("::")

            for joint in splitBones:
                if joint == jointName:
                    # get the module name and module class
                    moduleName = cmds.getAttr(node + ".moduleName")
                    moduleClass = cmds.getAttr(node + ".moduleType")

                    if node != "ART_Root_Module":
                        basename = cmds.getAttr(node + ".baseName")
                    else:
                        basename = moduleName

                    # start building up the mover name we need and return it
                    if offsetMover:
                        moverName = jointName + "_mover_offset"
                    if globalMover:
                        moverName = jointName + "_mover"

                    if cmds.objExists(moverName):
                        return moverName

                    else:
                        if offsetMover:
                            moverName = jointName + "_mover_offset"
                        if globalMover:
                            moverName = jointName + "_mover"

                        # comparing basename and moduleName, get prefix and suffix
                        prefix = moduleName.partition(basename)[0]
                        suffix = moduleName.partition(basename)[2]

                        # make sure not partitioning on an empty separator
                        if prefix == "":
                            prefix = "&&"
                        if suffix == "":
                            suffix = "$$"

                        noPrefix = jointName.partition(prefix)[2]
                        if noPrefix != "":
                            moverName = noPrefix
                        noSuffix = moverName.rpartition(suffix)[0]
                        if noSuffix != "":
                            moverName = noSuffix

                        # construct mover name.
                        if offsetMover:
                            moverName = moduleName + "_" + moverName

                            if cmds.objExists(moverName):
                                if moverName.find("_mover") != -1:
                                    return moverName
                            else:
                                moverName += "_mover_offset"

                                if cmds.objExists(moverName):
                                    return moverName

                        if globalMover:
                            moverName = moduleName + "_" + moverName

                            if cmds.objExists(moverName):
                                if moverName.find("_mover") != -1:
                                    return moverName
                            else:
                                moverName += "_mover"

                                if cmds.objExists(moverName):
                                    return moverName


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findOffsetMoverFromName(name):
    """
    Find the top-most offset mover of a given module and return it.

    :param name: name of the module whose top-most offset mover we wish to find.
    :return: name of the offset mover of given module name.
    """

    grp = name + "_mover_grp"
    if cmds.objExists(grp):
        topLevelGrp = cmds.listRelatives(grp, children=True)
        if len(topLevelGrp) > 0:
            globalMover = cmds.listRelatives(topLevelGrp[0], children=True, type="transform")
            if len(globalMover) > 0:
                offsetMover = cmds.listRelatives(globalMover[0], children=True, type="transform")
                if len(offsetMover) > 0:
                    return offsetMover[0]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findGlobalMoverFromName(name):
    """
    Find the top-most global mover of a given module and return it.

    :param name: name of the module whose top-most global mover we wish to find.
    :return: name of the global mover of given module name.
    """

    grp = name + "_mover_grp"

    if cmds.objExists(grp):
        topLevelGrp = cmds.listRelatives(grp, children=True)

        if len(topLevelGrp) > 0:
            if topLevelGrp[0].find("mover") != -1:
                if topLevelGrp[0].find("offset") == -1:
                    if topLevelGrp[0].find("grp") == -1:
                        return topLevelGrp[0]

                    else:
                        globalMover = cmds.listRelatives(topLevelGrp[0], children=True, type="transform")

                        if len(globalMover) > 0:
                            return globalMover[0]

            else:
                globalMover = cmds.listRelatives(topLevelGrp[0], children=True, type="transform")

                if len(globalMover) > 0:
                    return globalMover[0]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def fitViewAndShade():
    """
    Focus the camera on what is in the scene, fitting it to the view, then turn on shaded mode.
    """

    # clear selection and fit view
    previousSelection = cmds.ls(sl=True)
    cmds.select(clear=True)
    cmds.viewFit()
    panels = cmds.getPanel(type='modelPanel')

    # turn on smooth shading
    for panel in panels:
        editor = cmds.modelPanel(panel, q=True, modelEditor=True)
        cmds.modelEditor(editor, edit=True, displayAppearance="smoothShaded", backfaceCulling=False)
    if len(previousSelection) > 0:
        cmds.select(previousSelection)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def xrayJoints():
    """
    Gets the current model editor and turns on xray joints
    """

    panels = cmds.getPanel(type='modelPanel')
    for panel in panels:
        editor = cmds.modelPanel(panel, q=True, modelEditor=True)
        cmds.modelEditor(editor, edit=True, jointXray=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def fitSelection():
    """
    Frame the camera up on the current selection.
    """

    mel.eval("FrameSelected;")
    mel.eval("fitPanel -selected;")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getFaceMaterials(geo):
    """
    Get and return the materials assigned to each face of the passed in geometry.
    """

    mat2face = {}
    shape = cmds.listRelatives(geo, s=True)[0]
    sgs = cmds.listConnections(shape, type="shadingEngine")

    if sgs is not None:
        for sg in sgs:
            faces = []
            members = cmds.sets(sg, q=True)
            if members is not None:
                for item in members:
                    if geo in item:
                        faces.append(item)

            mat2face[sg] = faces

    return mat2face


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findAndRenameOutlinerChildren(widgetItem, partitionName, newName):
    """
    Find all child widgets of the passed in widgetItem and set their text to the new module name. Usually invoked
    when a user wants to change the module name.

    :param widgetItem: widget to search and replace the names of the children widgets
    :param partitionName: the original module name
    :param newName: the new module name
    """

    children = widgetItem.childCount()
    for i in range(children):
        child = widgetItem.child(i)
        mover = child.text(0).partition(partitionName)[2]
        child.setText(0, newName + mover)
        findAndRenameOutlinerChildren(child, partitionName, newName)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def deleteChildren(node):
    """
    Delete all children of the passed in transform node.

    :param node: node whose children we want to delete.
    """

    relatives = cmds.listRelatives(node, children=True, f=True)
    if relatives is not None:
        for each in relatives:
            if cmds.nodeType(each) == "transform":
                if cmds.objExists(each):
                    cmds.delete(each)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findMatchingModule(joint):
    """
    Look through all network nodes for their created bones attribute and find the network node that contains the input
    joint

    :param joint: joint to find associated network node
    :return: associated network node
    """

    # find all network nodes with .Created_Bones attr. find the network node that has the
    # input bone listed
    networkNodes = cmds.ls(type="network")
    for node in networkNodes:
        attr = cmds.listAttr(node, string="Created_Bones")
        if attr is not None:
            splitString = cmds.getAttr(node + "." + attr[0])
            bones = splitString.split("::")
            if joint in bones:
                # get the control node
                controlNode = cmds.listConnections(node + ".controls")
                return controlNode


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findAssociatedControl(node):
    # ToDo: Not sure if this is used anywhere. Check and delete if not.

    control_connections = []
    control_node = findMatchingModule(node.partition(":")[2])
    if control_node is not None:
        attrs = cmds.listAttr(control_node[0], ud=True)
        for attr in attrs:
            conns = cmds.listConnections(control_node[0] + "." + attr, source=False)
            if conns is not None:
                control_connections.extend(conns)

    controls = []
    _findAssociatedControl(node, controls, control_connections)

    print controls


def create_module_dict():
    """Creates and returns a dictionary of module network node and module name pairs."""

    return_dict = {}
    character = returnCharacterModule()
    modules = cmds.listConnections(character + ".rigModules")
    for module in modules:
        mod_name = cmds.getAttr(module + ".moduleName")
        return_dict[mod_name] = module

    return return_dict


def get_prefix_suffix(name, base_name):
    """
    Take the given name and base_name and find the prefix and suffix.
    :param name: the name of the module (ex: arm_l)
    :param base_name: the base name of the module (ex: arm)
    :return:
    """

    prefix = None
    suffix = None

    splitName = name.split(base_name)
    if splitName[0] != '':
        prefix = splitName[0]
    if splitName[1] != '':
        suffix = splitName[1]
    return [prefix, suffix]


def find_parent_controls(control):
    """
    Finds a given control's parent controls. Not just in terms of direct hierarchy, but any control in the entire rig
    that influences the given control. For example, the offset_anim and body_anim affect many controls.
    :param control:
    :return:
    """
    if not cmds.objExists(control):
        return
    relatives = cmds.listRelatives(control, fullPath=True)
    parent_controls = []

    if relatives is not None:
        nodes = relatives[0].split("|")

        parent_controls = []
        for node in nodes:
            if cmds.objExists(node + ".controlClass"):
                if node != control:
                    parent_controls.append(node)

    return parent_controls


def find_origin_control():
    """ Finds the control to use as a reflection point for mirroring poses."""

    root_children = cmds.listRelatives("root", children=True)
    test = []

    for each in root_children:
        children = cmds.listRelatives(each, allDescendents=True)
        if children is not None:
            test.append([each, len(children)])

    origin_joint = "root"
    current_max = 0
    for each in test:
        if each[1] > current_max:
            current_max = each[1]
            origin_joint = each[0]
        elif each[1] == current_max:
            current_max = 0
            origin_joint = "root"

    return origin_joint


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def _findAssociatedControl(node, control_list, valid_controls):
    """
    Take the input node (usually a bone) and find any controls that might control that bone and add those to the
    returnList

    :param node: Usually a joint that you are trying to find controls which drive this joint
    :param inst: instance of the class that calls on this function
    :return: A list of controls that affect the input node

    """

    okNodes = ["ramp", "blendColors", "transform", "multiplyDivide", "joint", "constraint"]
    if node == "root":
        control_list.append("root_anim")

    connections = cmds.listConnections(node, source=True, destination=False)
    if connections is not None:
        for connection in connections:
            if cmds.nodeType(connection) in okNodes:
                if connection.find("_anim") != -1:
                    if connection in valid_controls:
                        if connection not in control_list:
                            control_list.append(connection)
                else:
                    _findAssociatedControl(connection, control_list, valid_controls)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findAssociatedMover(joint, module, useOffset=False):
    """
    Find the global mover associated with the passed in joint and the passed in network node. Usually invoked from
    riggingUtils when creating a control from a joint mover.

    :param joint: name of the joint whose associated mover you wish to find.
    :param module: name of the module the joint belongs to. Used to figure out if any prefixes or suffixes were used.
    :return: name of global mover
    """

    if module == "ART_Root_Module":
        return "root_mover"

    # figure out the name
    moduleName = cmds.getAttr(module + ".moduleName")
    baseName = cmds.getAttr(module + ".baseName")

    moverName = joint + "_mover"

    if cmds.objExists(moverName):
        return moverName

    else:
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
            boneName = joint.partition(suffixSeparator)[0]
        else:
            boneName = joint.partition(prefixSeparator)[2].partition(suffixSeparator)[0]

        # get the mover node
        if useOffset:
            mover = prefix + baseName + suffix + "_" + boneName + "_mover_offset"
            mover = mover.replace(" ", "")
        else:
            mover = prefix + baseName + suffix + "_" + boneName + "_mover"
            mover = mover.replace(" ", "")

        if cmds.objExists(mover):
            return mover

        else:
            return None


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def find_all_incoming(start_nodes, max_depth=None):
    """
    Recursively finds all unique incoming dependencies for the specified node.

    :return: list of dependencies associated with node.
    """

    dependencies = set()
    _find_all_incoming(start_nodes, dependencies, max_depth, 0)
    return list(dependencies)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def _find_all_incoming(start_nodes, dependencies, max_depth, depth):
    """
    Recursively finds all unique incoming dependencies for the specified node.
    """

    if max_depth and depth > max_depth:
        return
    kwargs = dict(s=True, d=False)
    incoming = cmds.listConnections(list(start_nodes), **kwargs)
    if not incoming:
        return
    non_visitied = set(cmds.ls(incoming, l=True)).difference(dependencies)
    dependencies.update(non_visitied)
    if non_visitied:
        _find_all_incoming(non_visitied, dependencies, max_depth, depth + 1)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_mobject(name):
    """
    Get's MObject from given name.
    """

    selection_list = OpenMaya.MSelectionList()
    selection_list.add(name)
    mobject = OpenMaya.MObject()
    selection_list.getDependNode(0, mobject)
    return mobject


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_module_types():
    """
    Searches the rig modules folder for all the module types

    :return: Returns a list of the module types
    """

    settings = QtCore.QSettings("Epic Games", "ARTv2")
    toolsPath = settings.value("toolsPath")

    modulesLocation = os.path.normcase(os.path.join(toolsPath, "Core/Scripts/RigModules"))
    files = os.listdir(modulesLocation)
    modules = []
    returnData = []

    for f in files:
        if f.rpartition(".")[2] == "py":
            modules.append(f)

    for mod in modules:
        niceName = mod.rpartition(".")[0]
        if niceName != "__init__":

            # get the icon path from the module and add the icon to the push button
            try:
                module = __import__("RigModules." + niceName, {}, {}, [niceName])
                baseName = module.baseName
                returnData.append(baseName)
            except AttributeError:
                pass

    return returnData


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_namespace(name):
    """
    Gets the namespace from the given name.

    :param name: String to extract the namespace from.
    :return: The extracted namespace
    """

    namespace = re.match('[_0-9a-zA-Z]+(?=:)(:[_0-9a-zA-Z]+(?=:))*', name)
    if namespace:
        namespace = '%s:' % str(namespace.group(0))
    else:
        namespace = ''
    return namespace


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def remove_namespace(name):
    """
    Removes the namespace from the given name

    :param name: The name with the namespace
    :return: The name without the namesapce
    """

    namespace = get_namespace(name)
    if namespace:
        return re.sub('^{0}'.format(namespace), '', name)
    return name


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def win_path_convert(path=None):
    """
    Converts back slashes to forward slashes
    """

    separator = os.sep
    if separator != "/":
        path = path.replace(os.sep, "/")
    return path


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def exportMesh(mainUI, exportMeshes, exportPath, removeBones, poseDict):
    """
    Take the passed in information and export skeletal meshes to FBX format in the specified output path.
    Invoked from ART_ExportMeshes.py

    :param mainUI: instance of rig creator interface. Used to access rig creator class variables
    :param exportMeshes: list of meshes to export for the given LOD
    :param exportPath: output path of FBX file for the given LOD
    :param removeBones: which bones, if any, to remove for the given LOD
    :param poseDict: transform values for bones to be applied to given LOD before removing bones, in order to bake in a\
    pose.


    Details:

    When exporting a LOD skeletal mesh, there are many steps that need to happen:
        * First, the LOD needs to go back to the model pose. If there are any joints this LOD needs to remove, we must
          save out the skin weight information first.
        * If there is a LOD pose to set, set the pose then while the mesh is still skinned.
        * After setting the LOD pose, search for any connected blendshapes the meshes may have. If there are not true
          copies of the mesh in the scene, manually create new morph target copies by going through each blendshape
          attribute turning them on, one by one, duplicating the mesh each time.
        * After checking for blendshapes, delete history on the meshes. This will bake the LOD pose in.
        * Next, re-apply the blendshapes now that the pose is baked in and import the skin weights.
        * If there were bones to remove, before removing the joints, transfer the weighting of those bones to the bone
          that was specified to transfer weighting to. Usually this is the first valid parent. So if removing all finger
          bones in an LOD, you would likely transfer all finger weights to the hand bone.
        * Once the weighting is transferred, it is then safe to delete the bones that were to be removed.
        * Now, we start building our selection of things to export. First though, we will check for any incoming
          connections to our joints that we want to export, and break those connections. These are usually connections
          to the rig, and we don't want FBX exporting all of that stuff.
        * Build the selection (joints and morphs) and export FBX
    """

    # before starting this function, the file should be saved (by whichever function is calling this function)

    # make sure fbx plugin is loaded
    cmds.loadPlugin("fbxmaya")

    # set FBX settings
    mel.eval("FBXExportSmoothingGroups -v 1")
    mel.eval("FBXExportSmoothMesh -v 0")
    mel.eval("FBXExportTangents -v 1")
    mel.eval("FBXExportUpAxis Z")
    mel.eval("FBXExportCameras -v 0")
    mel.eval("FBXExportConstraints -v 0")
    mel.eval("FBXExportShapes -v 1")
    mel.eval("FBXExportSkins -v 1")

    # Create a progress bar
    exportFileName = os.path.basename(exportPath)
    title = os.path.splitext(exportFileName)[0]

    progBar = interfaceUtils.ProgressBar(title)
    progBar.setTextVisible(True)
    progBar.show()

    # find the value range
    maxVal = 4 + len(exportMeshes)

    if poseDict is not None:
        maxVal += 1
    if removeBones is not None:
        maxVal += len(exportMeshes) * 4

    progBar.setRange(0, maxVal)
    progBar.setValue(0)
    progBar.show()

    # if joints to remove, save out skinning
    import Utilities.riggingUtils as riggingUtils

    weightFiles = []
    if exportMeshes and removeBones or removeBones is not None:

        for mesh in exportMeshes:
            skinCluster = riggingUtils.findRelatedSkinCluster(mesh)

            # find a temporary place to save the weights out to
            fullPath = os.path.join(cmds.internalVar(uwd=True), "artv2")
            fullPath = os.path.join(fullPath, "weights")
            if not os.path.exists(fullPath):
                os.makedirs(fullPath)

            meshCheck = False
            # do a check to make sure we don't have naming conflicts
            if mesh.find("|") != -1:
                shortName = mesh.rpartition("|")[2]
                cmds.select("*" + shortName + "*")
                selection = cmds.ls(sl=True, long=False, transforms=True, shapes=False)
                if len(selection) > 1:
                    string = ""
                    for each in selection:
                        string += each + "\n"

                    # launch a message box informing of the issue
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setWindowTitle("Naming Conflict")
                    msgBox.setText(
                        "More than one object shares the same name. Names should be unique.\
                        Please fix and try the operation again.")
                    msgBox.setInformativeText(string)
                    msgBox.setIcon(QtWidgets.QMessageBox.Critical)
                    ret = msgBox.exec_()

                    # clean up
                    if ret == QtWidgets.QMessageBox.Ok:
                        for file in weightFiles:
                            os.remove(file)
                    return

                else:
                    meshCheck = True
            else:
                meshCheck = True

            if meshCheck:
                fullPath = os.path.join(fullPath, mesh + ".weights")
                fullPath = returnFriendlyPath(fullPath)

                # add file to our list so we can delete later
                weightFiles.append(fullPath)

                # create skin class instance and save weights to location
                progBar.setFormat("Exporting Skin Weights..")
                progBar.setValue(progBar.getValue() + 1)
                skin = riggingUtils.export_skin_weights(fullPath, mesh)
                if skin is not None:
                    skin.exportSkinWeights(fullPath)

    if exportMeshes is None:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Export Error")
        msgBox.setText("No meshes assigned to this LOD.")
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.exec_()
        return

    # if LOD pose exists, set LOD pose (meshes are still weighted)
    if poseDict is not None:
        progBar.setFormat("Setting LOD Pose..")
        progBar.setValue(progBar.getValue() + 1)
        for key in poseDict:
            data = poseDict.get(key)
            if cmds.objExists(key):
                for each in data:
                    # translate, rotate, scale
                    if each == data[0]:
                        cmds.setAttr(key + ".translateX", each[0])
                        cmds.setAttr(key + ".translateY", each[1])
                        cmds.setAttr(key + ".translateZ", each[2])

                    if each == data[1]:
                        cmds.setAttr(key + ".rotateX", each[0])
                        cmds.setAttr(key + ".rotateY", each[1])
                        cmds.setAttr(key + ".rotateZ", each[2])

                    if each == data[2]:
                        cmds.setAttr(key + ".scaleX", each[0])
                        cmds.setAttr(key + ".scaleY", each[1])
                        cmds.setAttr(key + ".scaleZ", each[2])

    # delete the history on the meshes after setting the pose
    if exportMeshes and removeBones or removeBones is not None:
        for mesh in exportMeshes:

            blendshapeList = []
            deleteShapes = []

            # find blendshapes
            blendshapes = cmds.ls(type="blendShape")
            for blendshape in blendshapes:
                geo = cmds.blendShape(blendshape, q=True, geometry=True)
                if geo is not None:
                    geo = cmds.listRelatives(geo, parent=True)
                    if geo is not None:
                        if geo[0] == mesh:
                            attrs = cmds.listAttr(blendshape, m=True, string="weight")
                            if attrs is not None:
                                for attr in attrs:
                                    # if not, manually create shapes by toggling attrs and duplicating mesh
                                    if not cmds.objExists(attr):
                                        cmds.setAttr(blendshape + "." + attr, 1)
                                        dupe = cmds.duplicate(mesh)[0]

                                        # parent to world
                                        parent = cmds.listRelatives(dupe, parent=True)
                                        if parent is not None:
                                            cmds.parent(dupe, world=True)

                                        # rename the duplicate mesh to the blendshape name
                                        cmds.rename(dupe, attr)
                                        cmds.setAttr(blendshape + "." + attr, 0)
                                        deleteShapes.append(attr)

                                # add the blendshape node name and its attrs to the master blendshape list
                                blendshapeList.append([blendshape, attrs])

            # delete history
            cmds.delete(mesh, ch=True)

            # reapply blendshapes
            for item in blendshapeList:
                bshapeName = item[0]
                shapeList = item[1]

                i = 1
                for shape in shapeList:
                    if cmds.objExists(bshapeName):
                        cmds.blendShape(bshapeName, edit=True, t=(mesh, i, shape, 1.0))

                    else:
                        cmds.select([shape, mesh], r=True)
                        cmds.blendShape(name=bshapeName)
                        cmds.select(clear=True)

            for each in deleteShapes:
                cmds.delete(each)
        progBar.setFormat("Deleting Mesh History..")
        progBar.setValue(progBar.getValue() + 1)

    # go back to model pose
    # for inst in mainUI.moduleInstances:
    #     try:
    #         inst.setupForRigPose()
    #         inst.setReferencePose("modelPose")
    #         inst.cleanUpRigPose()
    #     except:
    #         pass

    # import skin weights
    if exportMeshes and removeBones or removeBones is not None:

        for mesh in exportMeshes:
            progBar.setFormat("Importing Skin Weights")
            progBar.setValue(progBar.getValue() + 1)

            fullPath = os.path.join(cmds.internalVar(uwd=True), "artv2")
            fullPath = os.path.join(fullPath, "weights")
            fullPath = os.path.join(fullPath, mesh + ".weights")
            fullPath = returnFriendlyPath(fullPath)
            if os.path.exists(fullPath):
                riggingUtils.import_skin_weights(fullPath, mesh, True)

    for f in weightFiles:
        os.remove(f)

    # transfer weighting information
    for mesh in exportMeshes:
        skinCluster = riggingUtils.findRelatedSkinCluster(mesh)

        if skinCluster is None:
            continue
        # prune weights
        cmds.skinPercent(skinCluster, mesh, prw=0.001)

        # remove unused influences
        weightedInfs = cmds.skinCluster(skinCluster, q=True, weightedInfluence=True)
        allInfs = cmds.skinCluster(skinCluster, q=True, inf=True)
        for inf in allInfs:
            if inf not in weightedInfs:
                cmds.skinCluster(skinCluster, edit=True, ri=inf)

        # get mesh influences
        meshInfluences = cmds.skinCluster(skinCluster, q=True, wi=True)

        # transfer weighting
        if removeBones is not None:
            for entry in removeBones:
                transferBone = entry[0]
                deleteBones = entry[1]

                for joint in deleteBones:
                    if joint in meshInfluences:

                        currentInfluences = cmds.skinCluster(skinCluster, q=True, inf=True)
                        if transferBone not in currentInfluences:
                            cmds.skinCluster(skinCluster, e=True, wt=0, ai=transferBone)

                        for x in range(cmds.polyEvaluate(mesh, v=True)):
                            value = cmds.skinPercent(skinCluster, (mesh + ".vtx[" + str(x) + "]"), t=joint, q=True)
                            if value > 0:
                                cmds.skinPercent(skinCluster, (mesh + ".vtx[" + str(x) + "]"),
                                                 tmw=[joint, transferBone])

        progBar.setFormat("Transferring Weighting..")
        progBar.setValue(progBar.getValue() + 1)

    # delete joints to remove
    if removeBones is not None:
        progBar.setFormat("Deleting Chosen Bones..")
        progBar.setValue(progBar.getValue() + 1)

        for entry in removeBones:
            deleteBones = entry[1]
            for bone in deleteBones:
                try:
                    cmds.delete(bone)
                except Exception, e:
                    print "Unable to remove joint: " + str(bone)
                    print e

    # handle morph targets
    blendShapeNodes = []
    blendShapeMeshes = []

    for mesh in exportMeshes:
        progBar.setFormat("Checking for Morph Targets..")
        progBar.setValue(progBar.getValue() + 1)

        blendshapes = cmds.ls(type="blendShape")
        for blendshape in blendshapes:
            geo = cmds.blendShape(blendshape, q=True, geometry=True)
            if geo is not None:
                geo = cmds.listRelatives(geo, parent=True)
                if geo is not None:

                    if geo[0] == mesh:
                        blendShapeNodes.append(blendshape)
                        # get blendshapes
                        attrs = cmds.listAttr(blendshape, m=True, string="weight")
                        if attrs is not None:
                            for attr in attrs:
                                if cmds.objExists(attr):
                                    blendShapeMeshes.append(attr)

    # before building selection, remove any connections from our skeleton
    progBar.setFormat("Removing Connections on Skeleton..")
    progBar.setValue(progBar.getValue() + 1)

    cmds.select("root", hi=True)
    selection = cmds.ls(sl=True)
    for each in selection:
        connT = cmds.connectionInfo(each + ".translate", sourceFromDestination=True)
        if connT != '':
            cmds.disconnectAttr(connT, each + ".translate")
        connR = cmds.connectionInfo(each + ".rotate", sourceFromDestination=True)
        if connR != '':
            cmds.disconnectAttr(connR, each + ".rotate")
        connS = cmds.connectionInfo(each + ".scale", sourceFromDestination=True)
        if connS != '':
            cmds.disconnectAttr(connS, each + ".scale")

    # rename joints if override data is present
    if cmds.objExists("ART_RIG_ROOT.exportOverrides"):
        connections = cmds.listConnections("ART_RIG_ROOT.exportOverrides")
        if connections is not None:
            attrs = cmds.listAttr(connections[0], ud=True)

            for attr in attrs:
                value = cmds.getAttr(connections[0] + "." + attr)

                if cmds.objExists(attr):
                    cmds.rename(attr, value)

    # export (select root, geometry, and any morphs)
    cmds.select(clear=True)

    # build selection
    progBar.setFormat("Building Selection For Export..")
    progBar.setValue(progBar.getValue() + 1)

    for mesh in exportMeshes:
        cmds.select(mesh, add=True)
    cmds.select("root", add=True)
    for bShapeMesh in blendShapeMeshes:
        cmds.select(bShapeMesh, add=True)

    progBar.setFormat("FBX Exporting...")
    progBar.setValue(maxVal)

    selection = cmds.ls(sl=True)
    mel.eval("FBXExport -f \"" + exportPath + "\" -s")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findExportMeshData():
    """
    Search through the character node LOD attributes to find out what and how to export the LOD.
    This data included the LOD pose, the bones to remove, the meshes for the LOD, the output path
    for the FBX, and the LOD name.

    :return: [output path for FBX, list of meshes to export for LOD, list of bones to remove for LOD,
             pose to put LOD in before removing bones, the LOD number]
    """

    lodAttrs = getLodData()
    characterNode = returnCharacterModule()

    if lodAttrs is not None:
        # get json data from attribute
        lodData = ["_Pose", "_Bones", "_Meshes", "_FilePath", "LOD"]

    returnData = []

    for attr in lodAttrs:

        meshValue = None
        boneValue = None
        pathValue = None
        poseData = None
        lodNumber = None

        for entry in lodData:
            if cmds.objExists(characterNode + "." + attr + entry):
                if entry == "_Bones":
                    try:
                        boneValue = json.loads(cmds.getAttr(characterNode + "." + attr + entry))
                    except:
                        pass
                if entry == "_Meshes":
                    try:
                        meshValue = cmds.listConnections(characterNode + "." + attr + entry)
                    except:
                        cmds.warning("No meshes assigned to this LOD.")
                        pass
                if entry == "_FilePath":
                    pathValue = json.loads(cmds.getAttr(characterNode + "." + attr + entry))
                if entry == "_Pose":
                    try:
                        poseData = json.loads(cmds.getAttr(characterNode + "." + attr + entry))
                    except:
                        pass
            else:
                if entry == "LOD":
                    lodNumber = attr

        # append to return data
        returnData.append([pathValue, meshValue, boneValue, poseData, lodNumber])

    return returnData


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getLodData():
    """
    Search the character node for and LOD related attributes and return those.

    :return: list of attributes on character node that contain LOD export data.
    """

    # get mesh info from character node
    characterNode = returnCharacterModule()
    attrs = cmds.listAttr(characterNode, ud=True, string="LOD_*_FilePath")

    lodAttrs = []
    if attrs is not None:
        for attr in attrs:
            lodAttrs.append(attr.partition("_FilePath")[0])

    return lodAttrs


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnTooltipPath(path):

    nicePath = os.path.normpath(path)
    nicePath = os.path.realpath(nicePath)
    return nicePath


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnFriendlyPath(path):
    """
    Take the incoming path and replace back slashes with forward slashes

    :param path: directory or file path to replace back slashes in
    :return: a directory or file path with only forward slashes
    """

    nicePath = os.path.normpath(path)
    if nicePath.partition("\\")[2] != "":
        nicePath = nicePath.replace("\\", "/")
    return nicePath


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnNicePath(toolsPath, imagePath):
    """
    Take the incoming path and file and use os.path.join to create a new file path. Then replace all
    back slashes with forward slashes.

    :param toolsPath: the base directory path
    :param imagePath: the file name to join onto the base path
    :return: a joined path with only forward slashes
    """

    image = os.path.normpath(os.path.join(toolsPath, imagePath))
    if image.partition("\\")[2] != "":
        image = image.replace("\\", "/")
    return image


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def splitMesh(mesh, assetName):
    """
    Take the given mesh and break it into chunks based on the influence weights of each bone. For example,
    if the mesh was a leg that was skinned to a thigh bone, a calf bone, and a foot bone, this function will
    split the leg mesh into three new meshes, one for each major influence. This is sometimes known as an
    "anim mesh"

    :param mesh: name of mesh to split up
    :param assetName: name of character or rig (the name given on publish)
    :return: a list of the newly created meshes
    """

    # get mesh's skinCluster
    skinCluster = riggingUtils.findRelatedSkinCluster(mesh)

    # get the influences in that skinCluster
    influences = cmds.skinCluster(skinCluster, q=True, inf=True)

    # create a group if it doesn't exist
    if not cmds.objExists(assetName + "_animMeshGrp"):
        cmds.group(empty=True, name=assetName + "_animMeshGrp")

    newMeshes = []
    # loop through each influence, creating a mesh for that influnece is applicable
    for influence in influences:
        # create a new mesh
        if cmds.objExists(mesh + "_" + influence):
            cmds.warning("Mesh with name: " + mesh + "_" + influence + " already exists. Skipping.")
        else:
            newMesh = cmds.duplicate(mesh, name=mesh + "_" + influence)[0]

            # unlock attrs so we can add a constraint later
            for attr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
                cmds.setAttr(newMesh + attr, lock=False)

            # if there is only 1 influence, constrain the entire mesh as is
            if len(influences) <= 1:
                cmds.parentConstraint(influence, newMesh, mo=True)

            # otherwise, loop through each influence getting the components affected by that influence
            else:
                verts = []
                notWeighted = []

                for i in range(cmds.polyEvaluate(mesh, v=True)):
                    value = cmds.skinPercent(skinCluster, mesh + ".vtx[" + str(i) + "]", transform=influence, q=True)

                    if value > 0.5:
                        verts.append(newMesh + ".vtx[" + str(i) + "]")

                    else:
                        notWeighted.append(newMesh + ".vtx[" + str(i) + "]")

                # if the amount of non-weighted verts is the same as the number of verts in the mesh, delete the mesh.
                if len(notWeighted) == cmds.polyEvaluate(mesh, v=True):
                    cmds.delete(newMesh)

                if verts:
                    # select all verts
                    cmds.select(newMesh + ".vtx[*]")

                    # Convert the selection to contained faces
                    if len(verts) != cmds.polyEvaluate(mesh, v=True):
                        # unselect the verts we want to keep, convert remaining to faces and delete
                        cmds.select(verts, tgl=True)
                        cmds.select(cmds.polyListComponentConversion(fv=True, tf=True, internal=False))
                        cmds.delete()

                    # constrain mesh to influence, parent mesh to group
                    cmds.parentConstraint(influence, newMesh, mo=True)
                    cmds.parent(newMesh, assetName + "_animMeshGrp")

                    # fill holes, triangulate, and smooth normals
                    cmds.polyCloseBorder(newMesh, ch=False)
                    cmds.polyTriangulate(newMesh, ch=False)
                    cmds.polySoftEdge(newMesh, a=90, ch=False)
                    newMeshes.append(newMesh)

    return (newMeshes)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findAllSkinnableGeo():
    """
    Find all meshes in the scene, list their parents. If the parent is not part of the joint mover (proxy geo,
    lra representations, or bone representation geo) add it to the list of meshes that can be skinned.

    :return: a list of geometry that is valid for skinning.
    """

    meshes = cmds.ls(type="mesh")
    skinnableGeo = []

    for mesh in meshes:
        print "mesh is: {0}".format(mesh)
        parent = cmds.listRelatives(mesh, parent=True, type="transform")[0]
        print "mesh parent is: {0}".format(parent)
        if parent is not None:
            if parent.find("proxy_geo") == -1:
                if parent.find("lra") == -1:
                    if parent.find("bone_geo") == -1:
                        skinnableGeo.append(parent)
            if parent.find("proxy_geo") != -1:
                # get that parent
                transformParent = cmds.listRelatives(parent, parent=True)
                if transformParent is not None:
                    if transformParent[0].find("skinned") == 0:
                        skinnableGeo.append(parent)

    skinnableGeo = set(skinnableGeo)
    return skinnableGeo


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getMayaPyLoc():
    """
    This function finds the location of the mayapy interpreter for batch functions.

    :return: mayapy location
    """

    operatingSystem = cmds.about(operatingSystem=True)
    windows = ["win64", "nt"]
    linux = ["linux", "linux64"]
    mac = ["mac"]

    mayaLoc = None
    mayapy = None

    for key in sorted(os.environ.keys()):
        if key.find("MAYA_LOCATION") != -1:
            mayaLoc = os.environ[key]

    if operatingSystem in windows:
        mayapy = returnFriendlyPath(os.path.join(mayaLoc, "bin"))
        mayapy = returnFriendlyPath(os.path.join(mayapy, "mayapy.exe"))

    else:
        # need to confirm this works on Linux and Mac OS
        mayapy = returnFriendlyPath(os.path.join(mayaLoc, "bin"))
        mayapy = returnFriendlyPath(os.path.join(mayapy, "mayapy"))


    return mayapy


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def convertCurvesToStrokes(curve):

    brush = cmds.getDefaultBrush()

    intermediateObject = cmds.getAttr(curve + ".io")
    if intermediateObject == 0:

        newStroke = cmds.stroke(seed=0, pressure=True)
        newBrush = cmds.duplicate(brush, ic=True)
        brushStartSetup(newBrush[0])

        cmds.connectAttr(newBrush[0] + ".outBrush", newStroke + ".brush")
        cmds.connectAttr("time1.outTime", newBrush[0] + ".time")

        spans = cmds.getAttr(curve + ".spans")
        spans *= 6

        cmds.setAttr(newStroke + ".pathCurve[0].samples", spans)
        cmds.setAttr(newStroke + ".useNormal", 0)
        cmds.setAttr(newStroke + ".normalY", 1.0)
        cmds.setAttr(newStroke + ".minimalTwist", True)

        cmds.connectAttr(curve + ".ws", newStroke + ".pathCurve[0].curve")
        cmds.setAttr(newStroke + ".perspective", 1)
        cmds.setAttr(newStroke + ".displayPercent", 100.0)

        cmds.setAttr(newStroke + ".overrideEnabled", 1)
        cmds.setAttr(newStroke + ".overrideDisplayType", 2)

        return [newStroke, newBrush[0]]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def brushStartSetup(brushNode):

    bScale = cmds.getAttr(brushNode + ".globalScale")
    screenWidth = cmds.getAttr(brushNode + ".screenspaceWidth")
    scaleFace = cmds.getAttr("strokeGlobals.sceneScale")
    forceRealLights = cmds.getAttr("strokeGlobals.forceRealLights")
    forceDepth = cmds.getAttr("strokeGlobals.forceDepth")

    if scaleFace < .00001:
        scaleFace = .00001

    cmds.setAttr(brushNode + ".globalScale", bScale * scaleFace)
    if forceRealLights:
        cmds.setAttr(brushNode + ".realLights", 1)
    if forceDepth:
        cmds.setAttr(brushNode + ".depth", 1)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def findModuleInstances(character):

    returnModules = []
    # get rig modules
    if cmds.objExists(character + ":" + "ART_RIG_ROOT"):
        modules = cmds.listConnections(character + ":" + "ART_RIG_ROOT.rigModules")

        for module in modules:
            niceName = cmds.getAttr(module + ".moduleName")
            moduleType = cmds.getAttr(module + ".moduleType")
            mod = __import__("RigModules." + moduleType, {}, {}, [moduleType])

            # find the instance of that module
            moduleClass = getattr(mod, mod.className)
            moduleInst = moduleClass(None, niceName)
            returnModules.append(moduleInst)
            moduleInst.namespace = character + ":"

    return returnModules


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_traceback(traceback_object, add_locals=True):

    while 1:
        if not traceback_object.tb_next:
            break
        traceback_object = traceback_object.tb_next

    stack = []

    frame = traceback_object.tb_frame
    while frame:
        stack.append(frame)
        frame = frame.f_back
    stack.reverse()

    return_string = traceback.format_exc(traceback_object)
    return_string += "\n\n"

    for each in stack:
        return_string += "\n"
        return_string += "Function {0} in {1} at line {2}".format(each.f_code.co_name, each.f_code.co_filename,
                                                                  each.f_lineno)
        if add_locals:
            for key, value in each.f_locals.items():
                return_string += "\n\t\t{0}:  {1}".format(key, value)

    return return_string


def get_all_controls(all_characters=True, character_node=None):
    """
    Gets all controls of either all characters, or the specified character.
    :param all_characters: Whether or not to get controls for all characters in the scene.
    :param character_node: A specific character to get controls for.
    :return: A list of the controls.
    """

    return_controls = []

    if all_characters:
        character_modules = returnCharacterModules()
        for each in character_modules:
            controls = _get_character_controls(each)
            return_controls.extend(controls)
    else:
        if character_node is not None:
            if cmds.objExists(character_node):
                return_controls = _get_character_controls(character_node)
            else:
                raise RuntimeError("No valid character node supplied.")
        else:
            raise RuntimeError("No valid character node supplied.")

    return return_controls


def _get_character_controls(character_node):

    character_controls = []

    if cmds.objExists(character_node):
        modules = cmds.listConnections(character_node + ".rigModules")
        if modules is not None:
            for module in modules:
                controls = cmds.listConnections(module + ".controls")
                if controls is not None:
                    for control in controls:
                        attrs = cmds.listAttr(control, ud=True)

                        # loop through attrs, getting connections
                        for attr in attrs:
                            connections = cmds.listConnections(control + "." + attr, source=False)
                            if connections is not None:
                                character_controls.extend(connections)

    return character_controls
