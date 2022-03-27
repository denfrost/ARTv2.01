label = "Next Frame Custom"
cat = "Animation"
grp = "Misc."

import maya.cmds as cmds


def run(**kwargs):
    cmds.play(state=False)
    next_frame = cmds.currentTime(q=True) + 1
    # time_max = cmds.playbackOptions(q=True, max=True)
    # time_min = cmds.playbackOptions(q=True, min=True)
    #
    # if next_frame > time_max:
    #     next_frame = time_min
    cmds.currentTime(next_frame, edit=True)