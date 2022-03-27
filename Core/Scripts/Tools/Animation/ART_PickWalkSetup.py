"""
Module containing class that creates pick-walk connections, saves pick-walk template files, and loads pick-walk template
files.
"""

import json
import os
import maya.cmds as cmds


class ART_PickWalk(object):
    """
    Class for setting up pick-walking on controls or saving out pick-walking templates.
    Usage:
        .. code-block:: python

                    import Tools.Animation.ART_PickWalkSetup as pick_walk
                    inst = pick_walk.ART_PickWalk("my_character", "C:\\test.pickWalk", False)

                    # load a pick-walk template
                    inst.load_template()

                    # save a pick-walk template
                    inst.save_template()

    Arguments:

        +---------------------+---------+------------------------------------------------------------------------+
        | Keyword Argument    | Type    | Description                                                            |
        +=====================+=========+========================================================================+
        | character           | string  | The name of the character (or namespace if in a referenced file).      |
        +---------------------+---------+------------------------------------------------------------------------+
        | template_file       | string  | The file path of the template file to load or save.                    |
        +---------------------+---------+------------------------------------------------------------------------+
        | strip_namespace     | bool    | Whether or not to strip namespaces when loading a template.            |
        |                     |         | Valid only if the template was saved from a referenced rig.            |
        +---------------------+---------+------------------------------------------------------------------------+


    """
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def __init__(self, character=None, template_file=None, strip_namespace=True):

        self.character = character
        self.strip_namespace = strip_namespace
        self.template_file = template_file

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def save_template(self):
        """
        Saves out a file of the pick-walking setup on all controls of the given character.
        """

        data = {}
        character_node = self._get_character_node(self.character)

        network_nodes = cmds.listConnections(character_node + ".rigModules")
        controls = self._get_character_controls(self.character, network_nodes)

        ctrl_data = {}
        for control in controls:
            ctrl_data[control] = self._get_control_pickwalk_setup(control)
        data[self.character] = ctrl_data

        f = open(self.template_file, 'w')
        json.dump(data, f)
        f.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def load_template(self):
        """
        Loads a template file and processes the data to setup pick-walking on the given character using the data from
        the file.
        """

        # load data into memory
        if not os.path.exists(self.template_file):
            raise IOError("File: " + str(self.template_file) + " does not exist.")
        f = open(self.template_file, 'r')
        data = json.load(f)
        f.close()

        # loop through data
        keys = data.keys()
        missing = []

        for key in keys:
            # get control data
            controlData = data.get(key)
            controls = controlData.keys()

            # loop through controls, and first, check for stripping namespaces or search/replace with loadName
            for control in controls:
                this_control = self._validate_control_name(control, key, self.character, self.strip_namespace)
                if cmds.objExists(this_control):
                    self._disconnect_pickwalks(this_control)

                    attrList = controlData.get(control)
                    for each in attrList:
                        # [0] = attribute to connect. [1] = connectNode
                        if not cmds.objExists(this_control + "." + each[0]):
                            cmds.addAttr(this_control, ln=each[0], at="message")

                        pickwalk_obj = self._validate_control_name(each[1], key, self.character, self.strip_namespace)
                        self.create_pickwalk_connection(this_control, pickwalk_obj, each[0])
                else:
                    missing.append(this_control)

        # report nodes that were missing
        for ctrl in missing:
            cmds.warning(ctrl + " was not found. Pick-walking was not setup.")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_pickwalk_connection(self, control, pickwalk_object, attr):
        """
        Setup pick-walking between the control and the pick-walk object using the given pick-walk attribute.

        :param str control: The control from which the user pick-walks away from.
        :param str pickwalk_object: The control or object that the user pick-walks to.
        :param str attr: The pick-walk direction (pickWalkLeft, pickWalkRight, pickWalkUp, pickWalkDown)
        """

        if cmds.objExists(control + "." + attr):
            connections = cmds.listConnections(control + "." + attr, plugs=True)
            if connections is not None:
                cmds.disconnectAttr(connections[0], control + "." + attr)

        # create connection
        if not cmds.objExists(control + "." + attr):
            cmds.addAttr(control, ln=attr, at="message")

        connections = cmds.listConnections(control + "." + attr)
        if connections is None:
            if cmds.objExists(pickwalk_object):
                cmds.connectAttr(pickwalk_object + ".message", control + "." + attr)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_character_controls(self, character, network_nodes):

        controls = []
        for network_node in network_nodes:
            control_node = cmds.listConnections(network_node + ".controls")[0]
            attrs = cmds.listAttr(control_node, string="*Control*", ud=True)
            if attrs is not None:
                for attr in attrs:
                    try:
                        controls.extend(cmds.listConnections(control_node + "." + attr))
                    except StandardError:
                        pass

            # add settings node
        if cmds.objExists(character + ":rig_settings"):
            controls.append(character + ":rig_settings")
        else:
            controls.append("rig_settings")

        return controls

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_control_pickwalk_setup(self, control):

        pick_walk_attrs = ["pickWalkUp", "pickWalkDown", "pickWalkLeft", "pickWalkRight"]
        ctrl_info = []
        ctrlAttrs = cmds.listAttr(control, ud=True)

        for pick_walk_attr in pick_walk_attrs:
            if pick_walk_attr in ctrlAttrs:
                node = cmds.listConnections(control + "." + pick_walk_attr)
                if node is not None:
                    ctrl_info.append([pick_walk_attr, node[0]])

        return ctrl_info

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _validate_control_name(self, control, original_name, new_name, strip_namespace):
        if new_name != original_name:
            control = control.replace(original_name, new_name)

        # check to see if the template has no namespace, but is being loaded onto a character that does
        if len(control.split(":")) < 2:
            if not cmds.objExists(control):
                if cmds.objExists(original_name + ":" + control):
                    control = original_name + ":" + control

        # strip namespaces if checked
        if strip_namespace:
            splitString = control.split(":")
            if len(splitString[0]) > 0:
                control = splitString[1]

        return control

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _disconnect_pickwalks(self, control):

        pick_walk_attrs = ["pickWalkUp", "pickWalkDown", "pickWalkLeft", "pickWalkRight"]

        attrs = cmds.listAttr(control, ud=True)
        for attr in pick_walk_attrs:
            if attr in attrs:
                connection = cmds.listConnections(control + "." + attr)
                if connection is not None:
                    cmds.disconnectAttr(connection[0] + ".message", control + "." + attr)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_character_node(self, character):

        networkNodes = cmds.ls(type="network")

        for node in networkNodes:
            attrs = cmds.listAttr(node, ud=True)
            if "rigModules" in attrs:
                name = cmds.getAttr(node + ".name")
                if cmds.objExists(node + ".namespace"):
                    name = cmds.getAttr(node + ".namespace")

                if name == character:
                    return node
