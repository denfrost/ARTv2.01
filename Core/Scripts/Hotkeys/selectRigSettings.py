label = "Select Rig Settings"
cat = "Animation"
grp = "Rig Manipulation"


import maya.cmds as cmds


def run():

    # get character nodes in scene
    nodes = cmds.ls(type='network')
    characters = []

    for node in nodes:
        attrs = cmds.listAttr(node, ud=True)
        if attrs is not None:
            if "rigModules" in attrs:
                characters.append(node)

    index = 0
    for character in characters:

        namespace = cmds.getAttr(character + ".namespace")
        settingsNode = namespace + ":rig_settings"
        selection = cmds.ls(sl=True)

        if settingsNode in selection:
            index += 1
            if index > len(characters) - 1:
                index = 0
        else:
            index = characters.index(character)
            settingsNode = namespace + ":rig_settings"
            cmds.select(settingsNode)
            break
