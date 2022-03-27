label = "Filter Curves"
cat = "Animation"
grp = "Misc."


import maya.cmds as cmds


def run():
    curves = cmds.ls(type="animCurve")
    cmds.filterCurve(curves)