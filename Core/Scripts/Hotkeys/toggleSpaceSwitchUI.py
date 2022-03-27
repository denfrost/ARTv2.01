label = "Toggle Space Switcher UI"
cat = "Animation"
grp = "Interface and Tools"

import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui


def run():
    import maya.cmds as cmds
    try:
        cmds.deleteUI("ART_SpaceSwitcherUI", window=True)
    except Exception, e:
        ssui.run()
