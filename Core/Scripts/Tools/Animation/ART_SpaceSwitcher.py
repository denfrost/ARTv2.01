"""
Module for handling space switching. Contains classes for creating spaces, and interface classes for managing spaces.
"""

import json

import maya.cmds as cmds
import maya.api.OpenMaya as api

from ThirdParty.Qt import QtCore
import Utilities.utils as utils

SETTINGS = QtCore.QSettings("Epic Games", "ARTv2")
TOOLSPATH = SETTINGS.value("toolsPath")
PROJPATH = SETTINGS.value("projectPath")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_array_size(space_node):
    """
    Gets the number of spaces on the given control.

    :param str space_node: The control that has an array of spaces to query.
    :return: Returns the array size and the MPlug of the spaces attribute in a list.
    :rtype: [int, MPlug]
    """

    array_size = 0
    plug = None

    if not cmds.objExists(space_node):
        raise RuntimeError(space_node + " does not exist!")
    selection = api.MGlobal.getSelectionListByName(space_node)
    obj = selection.getDependNode(0)
    # noinspection PyArgumentList
    depend_node = api.MFnDependencyNode(obj)
    if cmds.objExists(space_node + ".spaces"):
        plug = depend_node.findPlug("spaces", False)
        array_size = plug.numElements()

    return [array_size, plug]


def find_control_spaces(control):
    """
    Given the control, find all spaces available to that control.

    :param str control: The animation control to locate spaces on.
    :return: Returns a list of spaces found.
    :rtype: An array of strings.
    """

    spaces = []
    if cmds.objExists(control):
        array_size = get_array_size(control)
        for i in range(0, array_size[0]):
            name = cmds.getAttr(control + ".spaces[" + str(i) + "].space_name")
            spaces.append(name)
    return spaces


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class CreateSpace(object):
    """
    Class for creating a space on a control.

    Example:

    .. code-block:: python

        import Tools.Animation.ART_SpaceSwitcher as sw
        sw.CreateSpace("l hand", "weapon_jnt_anim", "weapon_jnt_l_anim")

    """

    def __init__(self, name, control, target, space_type="parent"):
        """
        :param str name: The name of the space.
        :param str control: The control which is getting the space.
        :param str target: The object which is the space for the control.
        :param str space_type: The type of constraint to use when creating the space.
        """

        self.space_type = space_type

        is_valid = self._does_control_allow_spaces(control)
        if is_valid:
            self._create_space_switcher_setup()
            referenced = self._check_for_reference()

            if referenced:
                raise RuntimeError("Can not setup spaces with a referenced rig. Please edit the rig to setup spaces.")
            created_space_info = self._create_space_groups(control, target, referenced)
            if created_space_info is not False:
                self._add_space_entry(control, name, created_space_info)
            else:
                raise RuntimeError("could not setup space. Does the space already exist?")
        else:
            raise RuntimeError("control is not setup to have space-switching capabilities. Aborting.")

    def _does_control_allow_spaces(self, control):
        if not cmds.objExists(control + "_space_switcher_follow"):
            return False
        return True

    def _create_space_switcher_setup(self):
        create_group = False
        group_exists = False

        rig_referenced = self._check_for_reference()
        if not rig_referenced:
            if cmds.objExists("spaces") is False:
                create_group = True
            else:
                group_exists = True

        if create_group:
            space_group = cmds.group(empty=True, name="spaces")
            if cmds.objExists("rig_grp"):
                cmds.parent(space_group, "rig_grp")

        else:
            if group_exists is False:
                cmds.warning("Rig is referenced. The initial space switcher must be setup in a non-referenced file."
                             " Aborting")
            else:
                pass
            return

    def _create_space_groups(self, control, target, referenced):

        if not cmds.objExists(control + "_to_" + target + "_space"):
            space_group = cmds.group(empty=True, name=control + "_to_" + target + "_space")

            spaces_group = "spaces"
            if referenced:
                namespace = control.split(":")[0]
                spaces_group = namespace + ":spaces"

            cmds.parent(space_group, spaces_group)
            cmds.parentConstraint(target, space_group)

            space_offset_group = cmds.group(empty=True, name=space_group + "_offset")
            cmds.parent(space_offset_group, space_group)
            cmds.delete(cmds.parentConstraint(control, space_offset_group)[0])

            space_buffer_group = cmds.group(empty=True, name=space_group + "_buffer")
            cmds.parent(space_buffer_group, spaces_group)
            buffer_constraint = cmds.parentConstraint(space_offset_group, space_buffer_group)[0]

            cmds.addAttr(space_buffer_group, ln="space_group", at="message")
            cmds.connectAttr(space_group + ".message", space_buffer_group + ".space_group")

            space_constraint = None
            if self.space_type == "parent":
                space_constraint = cmds.parentConstraint(space_buffer_group, control + "_space_switcher_follow")[0]
            if self.space_type == "translation":
                space_constraint = cmds.pointConstraint(space_buffer_group, control + "_space_switcher_follow")[0]
            if self.space_type == "rotation":
                space_constraint = cmds.orientConstraint(space_buffer_group, control + "_space_switcher_follow")[0]

            return [space_buffer_group, buffer_constraint, space_constraint, space_offset_group]
        return False

    def _add_space_entry(self, control, name, space_info):

        array_size = get_array_size(control)[0]
        if array_size == 0:
            self._create_space_attr(control, name)
        else:
            # add new space to enum attribute
            enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
            split_string = enum_val.split(":")
            if name in split_string:
                cmds.warning("space name: " + str(name) + " already exists!")
                return
            else:
                enum_val += ":" + name
                cmds.addAttr(control + ".follow", edit=True, en=enum_val)

        cmds.setAttr(control + ".spaces[" + str(array_size) + "].space_name", name, type="string")

        buffer_node = space_info[0]
        space_node = cmds.listConnections(buffer_node + ".space_group")
        space_constraint = space_info[2]

        cmds.setAttr(space_info[1] + ".nodeState", 10)

        if space_node is not None:
            space_node = space_node[0]
            cmds.connectAttr(space_node + ".message", control + ".spaces[" + str(array_size) + "].space_node")

        constraint_weight = space_constraint + "." + buffer_node + "W" + str(array_size)

        condition_node = cmds.shadingNode("condition", asUtility=True, name=control + "_" + name + "_condition")
        cmds.connectAttr(control + ".follow", condition_node + ".firstTerm")
        cmds.setAttr(condition_node + ".secondTerm", array_size + 1)
        cmds.setAttr(condition_node + ".colorIfTrueR", 1)
        cmds.setAttr(condition_node + ".colorIfFalseR", 0)
        cmds.setAttr(condition_node + ".colorIfTrueG", 0)
        cmds.setAttr(condition_node + ".colorIfFalseG", 10)
        cmds.connectAttr(condition_node + ".outColorR", constraint_weight)
        cmds.connectAttr(condition_node + ".outColorG", space_info[1] + ".nodeState")

    def _create_space_attr(self, control, name):

        if cmds.objExists(control + ".follow"):
            enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
            split_string = enum_val.split(":")
            if name in split_string:
                cmds.warning("space name: " + str(name) + " already exists!")
                return
            else:
                enum_val += ":" + name
                cmds.addAttr(control + ".follow", edit=True, en=enum_val)

        else:
            cmds.addAttr(control, ln="follow", at="enum", en="default:" + name + ":", keyable=False)

        if not cmds.objExists(control + ".spaces"):
            cmds.addAttr(control, ln="spaces", at="compound", nc=2, m=True)
            cmds.addAttr(control, ln="space_name", dt="string", parent="spaces")
            cmds.addAttr(control, ln="space_node", at="message", parent="spaces")

    def _check_for_reference(self):

        references = cmds.ls(type="reference")
        if len(references) > 0:
            for reference in references:
                if reference != "sharedReferenceNode":
                    reference_path = cmds.referenceQuery(reference, filename=True)
                    if PROJPATH in reference_path:
                        reference_name = cmds.referenceQuery(reference, namespace=True)
                        if cmds.objExists(reference_name + ":ART_RIG_ROOT"):
                            return True

        return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SwitchSpace(object):
    """
    Class for switching spaces on a control

    Example:

    .. code-block:: python

        import Tools.Animation.ART_SpaceSwitcher as sw
        sw.SwitchSpace("char:ik_hand_l_anim", "weapon")

    """

    def __init__(self, control, space):
        """
        :param str control: The control to switch the space on.
        :param str space: The name of the space to switch to.
        """

        if not cmds.objExists(control + ".follow"):
            raise RuntimeError("Control is not a valid space switch control!")
        space_attribute = self._get_space_info(control, space)
        is_valid = self._validate_nodes(control, space_attribute, space)
        if is_valid:
            self._switch_space(control, space_attribute)
        # else:
        #     raise RuntimeError("provided info is not valid.")

    def _get_space_info(self, control, space):
        sub_space = None
        space_info = get_array_size(control)
        array_size = space_info[0]
        plug = space_info[1]
        active_space_node = None

        active_space = cmds.getAttr(control + ".follow")
        enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
        split_string = enum_val.split(":")
        active_space_name = split_string[active_space]

        for i in range(0, array_size):
            active_sub_space = plug.elementByLogicalIndex(i)
            space_name = cmds.getAttr(str(active_sub_space) + ".space_name")
            if space_name == active_space_name:
                active_space_node = str(active_sub_space)
                break

        for i in range(0, array_size):
            space_element = plug.elementByLogicalIndex(i)
            space_name = cmds.getAttr(str(space_element) + ".space_name")
            if space_name == space:
                sub_space = str(space_element)
                break

        return [sub_space, active_space_node, plug]

    def _validate_nodes(self, control, space_attribute, space):
        if not cmds.objExists(control):
            return False
        if not cmds.objExists(control + "_space_switcher_follow"):
            return False

        if space_attribute[0] is None:
            if space == "default":
                return True

        space_node = cmds.listConnections(space_attribute[0] + ".space_node")
        if space_node is not None:
            space_offset = space_node[0] + "_offset"
            if not cmds.objExists(space_offset):
                return False
        else:
            return False

        return True

    def _switch_space(self, control, space_info):

        currentMode = cmds.evaluationManager(q=True, mode=True)[0]
        cmds.evaluationManager(mode="off")

        locator = self._bookmark_location(control)

        # switch the attr to trigger the space switch
        enumVal = cmds.addAttr(control + ".follow", q=True, en=True)
        splitString = enumVal.split(":")
        if space_info[0] is not None:
            switch_to = cmds.getAttr(space_info[0] + ".space_name")
        else:
            switch_to = "default"
        value = splitString.index(switch_to)
        cmds.setAttr(control + ".follow", value)

        duplicate_control = self._get_new_transforms(control, locator)

        # delete stuff
        cmds.delete(locator)
        if cmds.objExists(duplicate_control):
            cmds.delete(duplicate_control)

        cmds.evaluationManager(mode=currentMode)

    def _bookmark_location(self, control):

        # set pre-key
        currentTime = cmds.currentTime(q=True)
        cmds.currentTime(currentTime - 1)
        cmds.setKeyframe(control)
        cmds.setKeyframe(control + ".follow", itt="stepnext", ott="step")

        # set the currentTime back to what it was
        cmds.currentTime(currentTime)

        # mark the control's current location with a locator
        loc = cmds.spaceLocator()[0]
        cmds.delete(cmds.parentConstraint(control, loc)[0])

        return loc

    def _get_new_transforms(self, control, locator):

        duplicate_control = cmds.duplicate(control, po=True)[0]

        # constrain the duplicate to the locator
        constraints = []
        try:
            point_constraint = cmds.pointConstraint(locator, duplicate_control)[0]
            constraints.append(point_constraint)
        except StandardError:
            pass

        try:
            orient_constraint = cmds.orientConstraint(locator, duplicate_control)[0]
            constraints.append(orient_constraint)
        except StandardError:
            pass

        # get the keyable attrs on the duplicate_control
        query_attrs = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
        attrs = cmds.listAttr(duplicate_control, keyable=True)

        for attr in attrs:
            if attr in query_attrs:
                cmds.setAttr(control + "." + attr, cmds.getAttr(duplicate_control + "." + attr))

        cmds.setKeyframe(control)
        cmds.setKeyframe(control + ".follow", itt="stepnext", ott="step")

        return duplicate_control


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class RenameSpace(object):
    """
    Class for handling renaming of spaces.

    Example:

    .. code-block:: python

        import Tools.Animation.ART_SpaceSwitcher as sw
        sw.RenameSpace("char:ik_hand_l_anim", "l hand", "IK left hand")

    """

    def __init__(self, control, space, new_name):
        """
        :param str control: The name of the control which has the space to rename.
        :param str space: The name of the space to rename.
        :param str new_name: The new name of the space.
        """

        if space == "default":
            raise RuntimeError("Cannot rename default space.")
        referenced = self._check_for_reference()
        if referenced is True:
            raise RuntimeError("Cannot rename spaces in a referenced rig!")
        space_attr_to_rename = self._find_space(space, control)
        self._rename_space(space_attr_to_rename, space, new_name, control)

    def _rename_space(self, space_attr, space, new_name, control):

        cmds.setAttr(space_attr, new_name, type="string")

        enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
        new_enum = enum_val.replace(space, new_name)
        cmds.addAttr(control + ".follow", edit=True, en=new_enum)

    def _find_space(self, space, space_switcher):
        space_attr = None

        space_info = get_array_size(space_switcher)
        array_size = space_info[0]
        plug = space_info[1]

        for i in range(0, array_size):
            sub_space = plug.elementByLogicalIndex(i)
            space_name = cmds.getAttr(str(sub_space) + ".space_name")
            if space_name == space:
                space_attr = str(sub_space) + ".space_name"
                break

        return str(space_attr)

    def _check_for_reference(self):

        references = cmds.ls(type="reference")
        if len(references) > 0:
            for reference in references:
                if reference != "sharedReferenceNode":
                    reference_name = cmds.referenceQuery(reference, namespace=True)
                    if cmds.objExists(reference_name + ":ART_RIG_ROOT"):
                        return True

        return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class DeleteSpace(object):
    """
    Class for handling deletion of spaces.

    Example:

    .. code-block:: python

        import Tools.Animation.ART_SpaceSwitcher as sw
        sw.DeleteSpace("char:ik_hand_l_anim", "l hand")

    """

    def __init__(self, control, space_to_delete):
        """
        :param str control: The name of the control to delete the space from.
        :param str space_to_delete: The name of the space to remove.
        """

        if space_to_delete == "default":
            raise RuntimeError("Cannot delete the default space.")

        space_info = self._find_space(space_to_delete, control)
        space_attr = space_info[0]

        if space_attr == str(None):
            raise RuntimeError("The given name for the space to delete could not be found: " + str(space_to_delete))

        if not self._check_space(control, space_to_delete):
            raise RuntimeError("The space to delete is currently active or has active keys. Unable to complete "
                               "operation.")

        self._delete_space(space_attr, control, space_to_delete)

    def _find_space(self, space_to_delete, control):
        space_attr = None
        index = None

        space_info = get_array_size(control)
        array_size = space_info[0]
        plug = space_info[1]

        for i in range(0, array_size):
            sub_space = plug.elementByLogicalIndex(i)
            space_name = cmds.getAttr(str(sub_space) + ".space_name")

            if space_name == space_to_delete:
                space_attr = str(sub_space)
                index = i
                break

        return [str(space_attr), index]

    def _check_space(self, control, space_to_delete):

        enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
        split_string = enum_val.split(":")
        index = split_string.index(space_to_delete)
        active_index = cmds.getAttr(control + ".follow")

        if index == active_index:
            return False

        return True

    def _delete_space(self, space_attr, control, space_to_delete):

        space_deleted = False

        space_node = cmds.listConnections(space_attr + ".space_node")
        if space_node is not None:
            connections = cmds.listConnections(space_node[0] + ".message")
            if connections is not None:
                for each in connections:
                    if cmds.nodeType(each) == "transform":
                        buffer_constraint = cmds.listConnections(each + ".translateX")
                        if buffer_constraint is not None:
                            if len(cmds.ls(buffer_constraint, readOnly=True)) == 0:
                                cmds.delete(buffer_constraint)
                                space_deleted = True
                                if cmds.objExists(space_node[0]):
                                    cmds.delete(space_node[0])
                                cmds.parentConstraint(space_node[0] + "_buffer",
                                                      control + "_space_switcher_follow",
                                                      edit=True,
                                                      remove=True)
                                cmds.delete(space_node[0] + "_buffer")
                            else:
                                raise RuntimeError("Cannot delete that space, as it is read-only (referenced)")

        if space_deleted:
            cmds.removeMultiInstance(space_attr, b=True)
            condition_node = cmds.listConnections(control + ".follow")[0]
            cmds.delete(condition_node)
            enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
            split_string = enum_val.split(":")
            new_enum = ""
            for each in split_string:
                if each != space_to_delete:
                    new_enum += each + ":"
                    cmds.addAttr(control + ".follow", edit=True, en=new_enum)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class BakeSpace(object):
    """
    Class for baking into a space over a frame range.

    Example:

    .. code-block:: python

        import Tools.Animation.ART_SpaceSwitcher as sw
        sw.BakeSpace("char:weapon_jnt_anim", "r hand", 0, 52)
        sw.BakeSpace("char:weapon_jnt_anim", "l hand", 53, 72)

    """

    def __init__(self, control, space_to_bake, start, end):
        """
        :param str control: The name of the control to bake the space onto.
        :param str space_to_bake:  The name of the space to bake.
        :param start: The start frame of the range to bake.
        :param end: The end frame of the range to bake.
        :type start: float
        :type end: float

        """

        valid = self._validate_inputs(control, space_to_bake)
        if valid:
            self._bake_space(control, space_to_bake, start, end)
        else:
            raise RuntimeError("Invalid inputs.")

    def _validate_inputs(self, control, space_to_bake):
        if cmds.objExists(control):
            if space_to_bake == "default":
                return True
            space_info = find_control_spaces(control)
            if len(space_info) > 0:
                spaces = [space for space in space_info]
                if space_to_bake in spaces:
                    return True
        return False

    def _bake_space(self, control, space_to_bake, start, end):

        # set pre-key
        cmds.currentTime(start - 1)
        cmds.setKeyframe(control)
        cmds.setKeyframe(control + ".follow", itt="stepnext", ott="step")

        # set the currentTime back to start frame
        cmds.currentTime(start)

        # mark the control's current location with a locator then bake it over the frame range
        loc = cmds.spaceLocator()[0]
        cmds.parentConstraint(control, loc)
        cmds.bakeResults(loc, simulation=True, time=(float(start), float(end)))

        # switch the attr to trigger the space switch
        enumVal = cmds.addAttr(control + ".follow", q=True, en=True)
        splitString = enumVal.split(":")
        value = splitString.index(space_to_bake)
        for i in range(start, end):
            cmds.currentTime(i)
            cmds.setAttr(control + ".follow", value)
            cmds.setKeyframe(control + ".follow", itt="stepnext", ott="step")

        duplicate_control = cmds.duplicate(control, po=True)[0]

        # constrain the duplicate to the locator
        constraints = []
        try:
            point_constraint = cmds.pointConstraint(loc, duplicate_control)[0]
            constraints.append(point_constraint)
        except StandardError:
            pass
        try:
            orient_constraint = cmds.orientConstraint(loc, duplicate_control)[0]
            constraints.append(orient_constraint)
        except StandardError:
            pass

        # get the keyable attrs on the duplicate_control
        query_attrs = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
        attrs = cmds.listAttr(duplicate_control, keyable=True)

        for i in range(start, end):
            cmds.currentTime(i)
            for attr in attrs:
                if attr in query_attrs:
                    cmds.setAttr(control + "." + attr, cmds.getAttr(duplicate_control + "." + attr))

            cmds.setKeyframe(control)

        # delete stuff
        cmds.delete(loc)
        if cmds.objExists(duplicate_control):
            cmds.delete(duplicate_control)

        # refresh scene
        cmds.currentTime(start + 1)
        cmds.currentTime(start)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class UpdateSpaceMatching(object):
    """
    This class updates matching on space switching frames for cases when the motion has been changed since the space-
    switching occurred.
    """

    def __init__(self, control, match_previous, match_next):
        """
        :param str control: The control to update the matching on.
        :param match_previous: Whether to match the previous frame's pose.
        :param match_next: Whether to match the next frame's pose.
        :type match_previous: bool
        :type match_next: bool
        """

        if not cmds.objExists(control + ".follow"):
            cmds.warning("Control has no spaces. Function only works on controls with spaces")
            return
        self._update_matching(control, match_previous, match_next)

    def _get_new_transforms(self, control, locator):

        duplicate_control = cmds.duplicate(control, po=True)[0]

        # constrain the duplicate to the locator
        constraints = []
        try:
            point_constraint = cmds.pointConstraint(locator, duplicate_control)[0]
            constraints.append(point_constraint)
        except StandardError:
            pass

        try:
            orient_constraint = cmds.orientConstraint(locator, duplicate_control)[0]
            constraints.append(orient_constraint)
        except StandardError:
            pass

        # get the keyable attrs on the duplicate_control
        query_attrs = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
        attrs = cmds.listAttr(duplicate_control, keyable=True)

        for attr in attrs:
            if attr in query_attrs:
                cmds.setAttr(control + "." + attr, cmds.getAttr(duplicate_control + "." + attr))

        cmds.setKeyframe(control)
        cmds.setKeyframe(control + ".follow", itt="stepnext", ott="step")

        cmds.delete(duplicate_control)
        cmds.delete(locator)

    def _update_matching(self, control, match_previous=True, match_next=False):

        if match_next:
            current = cmds.currentTime(q=True)
            cmds.currentTime(current + 1)
            locator = cmds.spaceLocator()[0]
            cmds.delete(cmds.parentConstraint(control, locator)[0])
            cmds.cutKey(control, time=(current, current))
            cmds.currentTime(current)
            self._get_new_transforms(control, locator)

        if match_previous:
            current = cmds.currentTime(q=True)
            cmds.currentTime(current - 1)
            locator = cmds.spaceLocator()[0]
            cmds.delete(cmds.parentConstraint(control, locator)[0])
            cmds.cutKey(control, time=(current, current))
            cmds.currentTime(current)
            self._get_new_transforms(control, locator)


class CreateGlobalSpaces(object):
    """
    This class creates a global space for multiple controls in one go, rather than having to create the same space on
    individual controls one at a time. It takes in a template file (*.spaces) that can be created with the GUI.

    .. seealso:: Tools.Animation.Interfaces.ART_SpaceSwitcherUI.ART_CreateGlobalSpacesUI
    """

    def __init__(self, template=None):
        """
        :param template: File path to the *.spaces file to build global spaces from.
        :type template: file path string
        """

        self.space_controls = []
        self._get_space_controls()

        if template is not None:
            self._generate_global_spaces(template)

    def _get_space_controls(self):
        all_controls = utils.get_all_controls()
        for control in all_controls:
            if cmds.objExists(control + "_space_switcher_follow"):
                self.space_controls.append(control)

    def _create_global_space(self, space_name, space_object, exclusion_list):

        if exclusion_list is None:
            exclusion_list = []

        for control in self.space_controls:
            if control not in exclusion_list:
                if control != "master_anim":
                    space_exists = self._check_for_space(control, space_name)
                    if space_exists is False:
                        CreateSpace(space_name, control, space_object)

    def _check_for_space(self, control, space_name):

        if cmds.objExists(control + ".follow"):
            enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
            spaces = enum_val.split(":")
            if space_name in spaces:
                return True

        return False

    def _generate_global_spaces(self, template):

        json_file = open(template)
        space_data = json.load(json_file)
        json_file.close()

        for space_name in space_data:
            data = space_data.get(space_name)

            if data[0] in self.space_controls:
                if data[1] is not None:
                    if data[0] not in data[1]:
                        data[1].append(data[0])
                else:
                    data[1] = [data[0]]

            self._create_global_space(space_name, data[0], data[1])
