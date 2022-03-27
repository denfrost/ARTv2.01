from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import maya.cmds as cmds
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
import os

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


windowTitle = "Set Mirror Module"
windowObject = "pyArtSetMirrorModuleUi"


class ART_SetMirrorModule_UI(QtWidgets.QMainWindow):
    def __init__(self, moduleInst, rigUiInst, parent=None):

        super(ART_SetMirrorModule_UI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # create class variables
        self.modInst = moduleInst
        self.rigUiInst = rigUiInst

        # load stylesheet
        style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(style)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)

        # create the mainLayout for the rig creator UI
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(250, 200))
        self.setMaximumSize(QtCore.QSize(250, 200))

        # create the background image
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        label = QtWidgets.QLabel("Choose Mirror Module:")
        self.widgetLayout.addWidget(label)
        font = QtGui.QFont()
        font.setBold(True)

        self.moduleList = QtWidgets.QListWidget()
        self.moduleList.addItem("None")
        self.widgetLayout.addWidget(self.moduleList)

        # add items to comboBox
        networkNode = self.modInst.returnNetworkNode
        modules = utils.returnRigModules()
        for mod in modules:
            modName = cmds.getAttr(mod + ".moduleName")
            modType = cmds.getAttr(mod + ".moduleType")

            if modType == cmds.getAttr(networkNode + ".moduleType"):
                if mod != networkNode:
                    self.moduleList.addItem(modName)

        self.moduleList.setCurrentRow(0)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLayout.addItem(spacerItem1)

        # update button
        self.updateBtn = QtWidgets.QPushButton("UPDATE")
        self.widgetLayout.addWidget(self.updateBtn)
        self.updateBtn.setMinimumSize(QtCore.QSize(230, 40))
        self.updateBtn.setMaximumSize(QtCore.QSize(230, 40))
        self.updateBtn.setSizePolicy(mainSizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateBtn.setFont(font)
        self.updateBtn.setObjectName("settings")

        # hookup signal/slot on create button
        self.updateBtn.clicked.connect(self.setMirrorModule)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setMirrorModule(self):

        # get new parent
        mirrorModule = self.moduleList.currentItem().text()

        # update current parent text
        self.modInst.mirrorMod.setText(mirrorModule)

        # update network node parentModuleBone attribute
        networkNode = self.modInst.returnNetworkNode
        cmds.setAttr(networkNode + ".mirrorModule", lock=False)
        cmds.setAttr(networkNode + ".mirrorModule", mirrorModule, type="string", lock=True)

        # also do this change to the mirror as well
        modules = utils.returnRigModules()
        for mod in modules:
            modName = cmds.getAttr(mod + ".moduleName")
            if modName == mirrorModule:

                # set the mirrored version
                mirror = cmds.getAttr(networkNode + ".moduleName")

                cmds.setAttr(mod + ".mirrorModule", lock=False)
                cmds.setAttr(mod + ".mirrorModule", mirror, type="string", lock=True)

                # get instance of mirror module's class
                modType = cmds.getAttr(mod + ".moduleType")
                modName = cmds.getAttr(mod + ".moduleName")
                module = __import__("RigModules." + modType, {}, {}, [modType])

                # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
                moduleClass = getattr(module, module.className)

                # find the instance of that module and call on the skeletonSettings_UI function
                moduleInst = moduleClass(self.rigUiInst, modName)

                # update mirrorModtext
                # find the current groupBox for this module
                for i in range(self.rigUiInst.moduleSettingsLayout.count()):
                    if type(self.rigUiInst.moduleSettingsLayout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                        if self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().title() == modName:
                            self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().setParent(None)

                            # relaunch the skeleton settings UI with new info
                            moduleInst.skeletonSettings_UI(modName)

        # delete the UI
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        cmds.deleteUI(mayaWindow + "|" + windowObject)
