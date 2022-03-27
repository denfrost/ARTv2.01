label = "Toggle Pose Library UI"
cat = "Animation"
grp = "Interface and Tools"


def run():

    import maya.cmds as cmds
    import Tools.Animation.ART_PoseLibrary as ART_PoseLibrary

    try:
        cmds.deleteUI("pyARTv2_PoseLibraryWin", window=True)
    except RuntimeError:

        ART_PoseLibrary.run()
