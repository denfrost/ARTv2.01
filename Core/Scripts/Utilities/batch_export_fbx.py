
import json
import os
import maya.cmds as cmds
import Tools.Animation.ART_ExportMotionUI as export
import Utilities.utils as utils


def gather_export_data():

    can_export = []

    character_modules = utils.returnCharacterModules()
    for each in character_modules:
        character_name = cmds.getAttr(each + ".name")

        if cmds.objExists(character_name + ":ART_RIG_ROOT.fbxAnimData"):
            fbxData = json.loads(cmds.getAttr(character_name + ":ART_RIG_ROOT.fbxAnimData"))
            for data in fbxData:
                sequence_data = data[7]
                output_path = sequence_data[2]

                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    can_export.append(False)
                    raise StandardError("Export path: " + output_dir + " does not exist")

                file_writable = os.access(output_path, os.W_OK)
                if not file_writable:
                    can_export.append(False)
                    raise StandardError("FBX file: " + os.path.basename(output_path) + " is not writable.")

                if file_writable:
                    can_export.append(True)

    if False in can_export:
        return False
    else:
        return True


def batch_export():

    can_export = gather_export_data()
    if can_export:
        export.Export_FBX(True, False, True)


batch_export()
