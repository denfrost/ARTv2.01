"""
This module contains the class for overriding joint names, so users can change the output joint names from the defaults
that ARTv2 spits out from the modules.
"""
import json
import maya.cmds as cmds


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_OverrideJointNames(object):
    """
    Class containing functions for overriding joint names, and saving and loading template files to override joint
    names.
    """

    def __init__(self, overrides=None, file_path=None):

        self.overrides = overrides
        self.file_path = file_path

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def save(self):
        """
        Save the joint name override data on a network node. This data is used by other tools (exporters usually).
        """

        if self.overrides is not None:

            # create a network node (delete if one exists and recreate) to store that data
            if cmds.objExists("artv2_override_data"):
                cmds.disconnectAttr("artv2_override_data.message", "ART_RIG_ROOT.exportOverrides")
                cmds.delete("artv2_override_data")

            node = cmds.createNode("network", name="artv2_override_data")

            for each in self.overrides:
                cmds.addAttr(node, ln=each[0], dt="string")
                cmds.setAttr(node + "." + each[0], each[1], type="string")

            # hook network node up to character node
            if not cmds.objExists("ART_RIG_ROOT.exportOverrides"):
                cmds.addAttr("ART_RIG_ROOT", ln="exportOverrides", at="message")

            cmds.connectAttr(node + ".message", "ART_RIG_ROOT.exportOverrides")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def save_template(self):
        """
        Save a template file (*.jno) that stores the joint name overrides.

        usage:
            .. code-block:: python
                # Save a template of the joint name overrides in the current scene to file file test.jno.

                import Tools.Rigging.ART_OverrideJointNames as ojn
                inst = ojn.ART_OverrideJointNames(overrides=None, file_path="C:\\Users\\me\\test.jno")
                inst.save_template()

        """

        saveData = []

        if cmds.objExists("artv2_override_data"):
            attrs = cmds.listAttr("artv2_override_data", ud=True)
            for attr in attrs:
                value = cmds.getAttr("artv2_override_data." + attr)
                saveData.append([attr, value])

        try:
            f = open(self.file_path, 'w')
            json.dump(saveData, f)
            f.close()
        except Exception, e:
            cmds.warning(str(e))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def load_template(self):
        """
        Load a template file (*.jno) that sets up joint name overrides on the network node in the scene for any joints
        in the scene that match joints in the template.

        usage:
            .. code-block:: python

                import Tools.Rigging.ART_OverrideJointNames as ojn
                inst = ojn.ART_OverrideJointNames(overrides=None, file_path="C:\\Users\\me\\test.jno")
                inst.load_template()
        """

        if self.file_path is not None:

            json_file = open(self.file_path)
            data = json.load(json_file)
            json_file.close()

            # create a network node (delete if one exists and recreate) to store that data
            if cmds.objExists("artv2_override_data"):
                cmds.disconnectAttr("artv2_override_data.message", "ART_RIG_ROOT.exportOverrides")
                cmds.delete("artv2_override_data")

            node = cmds.createNode("network", name="artv2_override_data")

            for each in data:
                cmds.addAttr(node, ln=each[0], dt="string")
                cmds.setAttr(node + "." + each[0], each[1], type="string")

            # hook network node up to character node
            if not cmds.objExists("ART_RIG_ROOT.exportOverrides"):
                cmds.addAttr("ART_RIG_ROOT", ln="exportOverrides", at="message")

            cmds.connectAttr(node + ".message", "ART_RIG_ROOT.exportOverrides")
