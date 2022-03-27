label = "Toggle Animation Tools UI"
cat = "Animation"
grp = "Interface and Tools"


def run():
    import maya.cmds as cmds
    try:
        cmds.deleteUI("pyART_AnimTools_Win", window=True)
        cmds.deleteUI("pyArtv2AnimToolsDock", control=True)
    except:
        import Tools.Animation.ART_AnimationUI as ART_AnimationUI
        ART_AnimationUI.run()
