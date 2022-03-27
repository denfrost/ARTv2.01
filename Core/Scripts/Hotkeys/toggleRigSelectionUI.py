label = "Toggle Select Rig Controls UI"
cat = "Animation"
grp = "Interface and Tools"

from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


def getMainWindow():
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    # pyside QMainWindow takes in a QWidget rather than QObject
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


def run():

    import maya.cmds as cmds
    try:
        cmds.deleteUI("pyART_SelectControlsWIN", window=True)
    except:
        import Tools.Animation.ART_SelectControlsUI as ART_SelectControlsUI
        ART_SelectControlsUI.ART_SelectControls(getMainWindow(), True)