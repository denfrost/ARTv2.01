label = "Toggle Rig Settings UI"
cat = "Animation"
grp = "Interface and Tools"


def run():

    import maya.cmds as cmds
    import Tools.Animation.ART_AnimationUI as ART_AnimationUI

    try:
        cmds.deleteUI("pyART_RigSettingsWIN", window=True)
    except:

        inst = None
        for instance in ART_AnimationUI.ART_AnimationUI._instances:
            inst = instance

        import Tools.Animation.ART_RigSettingsUI as ART_RigSettingsUI
        ART_RigSettingsUI.run(inst)
