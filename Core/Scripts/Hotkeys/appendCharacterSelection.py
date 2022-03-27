label = "Append Character Selection"
cat = "Animation"
grp = "Rig Manipulation"

import maya.cmds as cmds


def getControls(character):

    controlsToSelect = []
    modules = cmds.listConnections(character + ".rigModules")
    character_name = cmds.getAttr(character + ".name")

    for module in modules:
        inst = get_instance(module, character_name)
        controls = inst.getControls()

        for data in controls:
            for control in data:
                control_type = cmds.getAttr(control + ".controlType")
                if control_type == "FK":
                    controlsToSelect.append(control)
                if control_type == "IK":
                    controlsToSelect.append(control)
                if control_type == "Special":
                    controlsToSelect.append(control)

                fullPath = cmds.listRelatives(control, fullPath=True)[0]
                parents = fullPath.split("|")
                for parent in parents:
                    if parent.find("space_switcher") != -1:
                        if parent.find("_follow") == -1:
                            if cmds.getAttr(parent + ".sourceModule") == cmds.getAttr(module + ".moduleName"):
                                if parent not in controlsToSelect:
                                    controlsToSelect.append(parent)

        mod_name = cmds.getAttr(module + ".moduleName")
        controlsToSelect.append(character_name + ":" + mod_name + "_settings")
        controlsToSelect.append(character_name + ":" + "rig_settings")

    return controlsToSelect


def get_instance(module, character_name):

    modType = cmds.getAttr(module + ".moduleType")
    modName = cmds.getAttr(module + ".moduleName")
    mod = __import__("RigModules." + modType, {}, {}, [modType])

    moduleClass = getattr(mod, mod.className)
    moduleInst = moduleClass(None, modName)
    moduleInst.namespace = character_name + ":"

    return moduleInst


def run():

    # get character nodes in scene
    nodes = cmds.ls(type='network')
    characters = []

    for node in nodes:
        attrs = cmds.listAttr(node, ud=True)
        if attrs is not None:
            if "rigModules" in attrs:
                characters.append(node)

    # go through characters, check selection, and figure out character to select
    index = 0
    for character in characters:
        selection = cmds.ls(sl=True)

        # get character controls
        charControls = getControls(character)

        # if a character's controls are currently selected, select next character's controls
        if selection == charControls:
            index += 1
            if index > len(characters) - 1:
                index = 0
        else:
            index = characters.index(character)
            controls = getControls(characters[index])

            for each in controls:
                if cmds.objExists(each):
                    cmds.select(each, add=True)
                else:
                    print "{0} does not exist.".format(each)
            break
