label = "Next Key Custom"
cat = "Animation"
grp = "Misc."

import maya.cmds as cmds


def run(**kwargs):
    cmds.play(state=False)
    cmds.currentTime(cmds.findKeyframe(cmds.ls(sl=True), timeSlider=True, which="next"), edit=True)