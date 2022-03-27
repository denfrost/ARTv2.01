label = "Toggle Spaces On Control"
cat = "Animation"
grp = "Rig Manipulation"

import maya.cmds as cmds
import Tools.Animation.ART_SpaceSwitcher as space_switcher


def run():

    # get selection
    selection = cmds.ls(sl=True)
    if len(selection) > 1:
        cmds.warning("Toggle Spaces only works on one control at a time.")

    if len(selection) == 1:
        control = selection[0]

        if cmds.objExists(control + ".follow"):
            enumVal = cmds.addAttr(control + ".follow", q=True, en=True)
            spaces = enumVal.split(":")

            # get current space
            currentSpace = cmds.getAttr(control + ".follow", asString=True)

            # switch to next space in list
            listLength = len(spaces)
            currentSpace_index = spaces.index(currentSpace)

            if listLength == 1:
                try:
                    message = " <hl>No space to switch to. Already in only available space.</hl>"
                    cmds.inViewMessage(amg=message, pos='topCenter', fade=True)
                except Exception:
                    cmds.warning("No space to switch to. Already in only available space.")
                return

            if currentSpace_index == listLength - 1:
                space_switcher.SwitchSpace(control, spaces[0])
                try:
                    message = " <hl>Switched to space: " + str(spaces[0]) + "</hl>"
                    cmds.inViewMessage(amg=message, pos='topCenter', fade=True)
                except Exception:
                    pass

            else:
                space_switcher.SwitchSpace(control, spaces[currentSpace_index + 1])
                try:
                    message = " <hl>Switched to space: " + str(spaces[currentSpace_index + 1]) + "</hl>"
                    cmds.inViewMessage(amg=message, pos='topCenter', fade=True)
                except Exception:
                    pass

            # reselect control
            cmds.select(control)
