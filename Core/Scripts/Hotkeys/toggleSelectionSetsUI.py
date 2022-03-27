label = "Toggle Selection Sets UI"
cat = "Animation"
grp = "Interface and Tools"


def run():

    import maya.cmds as cmds

    try:
        cmds.deleteUI("pyART_SelectionSetsWIN", window=True)
    except:
        import Tools.Animation.ART_SelectionSetsUI as ART_SelectionSetsUI
        ART_SelectionSetsUI.run()
