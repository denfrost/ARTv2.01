label = "Toggle Import Motion UI"
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
        cmds.deleteUI("pyART_ImportMotionWIN", window=True)
    except:
        import Tools.Animation.ART_ImportMotionUI as ART_ImportMotionUI
        ART_ImportMotionUI.ART_ImportMotion(getMainWindow())
