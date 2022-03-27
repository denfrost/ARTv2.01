label = "Match and Switch Rig Mode"
cat = "Animation"
grp = "Rig Manipulation"

import maya.cmds as cmds
from ThirdParty.Qt import QtWidgets


def run():

    # get selection
    selection = cmds.ls(sl=True)

    for each in selection:
        if cmds.objExists(each + ".mode"):

            # get the current mode value
            control_node = cmds.listConnections(each + ".controlClass")[0]
            module_node = cmds.listConnections(control_node + ".parentModule")[0]
            character_node = cmds.listConnections(module_node + ".parent")[0]
            module_name = cmds.getAttr(module_node + ".moduleName")
            character_name = cmds.getAttr(character_node + ".namespace")

            settings_node = "{0}:{1}_settings".format(character_name, module_name)

            if cmds.objExists(settings_node + ".mode"):
                currentMode = cmds.getAttr(settings_node + ".mode")

                switchTo = "FK"
                if currentMode == 0:
                    switchTo = "IK"

                # import instance of module
                modType = cmds.getAttr(module_node + ".moduleType")
                mod = __import__("RigModules." + modType, {}, {}, [modType])
                moduleClass = getattr(mod, mod.className)
                moduleInst = moduleClass(None, module_name)
                moduleInst.namespace = character_name

                # run switch mode
                checkBox = QtWidgets.QCheckBox()
                checkBox.setChecked(True)
                moduleInst.switchMode(switchTo, checkBox)
