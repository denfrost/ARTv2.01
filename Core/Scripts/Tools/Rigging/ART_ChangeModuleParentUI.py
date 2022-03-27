"""
Author: Jeremy Ernst
"""
import maya.cmds as cmds
import os
import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


def getMainWindow():
    """
    Returns a pointer to Maya's window as a QWidget.

    """

    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    # pyside QMainWindow takes in a QWidget rather than QObject
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


windowTitle = "Change Module Parent"
windowObject = "pyArtChangeModuleParentUi"


class ART_ChangeModuleParent_UI(QtWidgets.QMainWindow):
    """
    This class allows the user to change the parent module bone of a given module. It is found within the
    skeletonSettingsUI of an individual module in the Rig Creator.

        .. image:: /images/changeModParent.png

    """

    def __init__(self, currentParent, moduleInst, rigUiInst, parent=None):
        """
        Instantiates the class, taking in current module information, and builds the interface.

        :param currentParent: The current module parent bone of this module.
        :param moduleInst: The instance in memory of the module whose name is to change.
        :param rigUiInst: The instance in memory of the Rig Creator UI from which this class was called.

        """
        super(ART_ChangeModuleParent_UI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # create class variables
        self.currentParent = currentParent
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
        self.setMinimumSize(QtCore.QSize(250, 400))
        self.setMaximumSize(QtCore.QSize(250, 400))

        # create the background image
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        label = QtWidgets.QLabel("Choose New Parent:")
        font = QtGui.QFont()
        font.setBold(True)
        label.setFont(font)
        self.widgetLayout.addWidget(label)

        self.boneSearch = QtWidgets.QLineEdit()
        self.boneSearch.setPlaceholderText("Search..")
        self.boneSearch.textChanged.connect(self.searchList)
        self.widgetLayout.addWidget(self.boneSearch)
        self.boneList = QtWidgets.QListWidget()
        self.widgetLayout.addWidget(self.boneList)
        self.boneList.setMinimumHeight(200)

        # add items to comboBox
        bones = utils.getViableParents()

        # get our own bones
        modBones = self.modInst.returnCreatedJoints

        for bone in bones:
            if bone not in modBones:
                self.boneList.addItem(bone)
            if bone == "root":
                index = bones.index(bone)
                self.boneList.setCurrentRow(index)

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
        self.updateBtn.clicked.connect(self.applyModuleParentChange)

        self.updateBtn.setFocus()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def searchList(self):
        """
        Reads the text in the QLineEdit and searches the list widget for any items containing the search text,
        hiding all listWidgetItems that do not contain the search text.

        """

        searchText = self.boneSearch.text()

        for i in range(self.boneList.count()):
            lwItem = self.boneList.item(i)
            if lwItem.text().find(searchText) != -1:
                lwItem.setHidden(False)
            else:
                lwItem.setHidden(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleParentChange(self):
        """
        Gets the new parent from the selected ListWidgetItem text and then checks to make sure the selected parent
        isn't a bone that is part of the module we're trying to change the parent on. Then updates text and attribute
        values where needed.

        .. note::
            The following things get updated:
                  * Current Parent text item in the Skeleton Settings UI
                  * Network Node .parentModuleBone attribute
                  * Constrains nodes based on new parenting relationship

        """

        # get new parent
        newParent = self.boneList.currentItem().text()

        # check to make sure new parent is not in this module's created bones list
        createdBones = self.modInst.returnCreatedJoints

        if newParent in createdBones:
            cmds.confirmDialog(title="Error", icon="critical",
                               message="Cannot parent a module to a bone created by the module.")
            return

        # update current parent text
        self.modInst.currentParent.setText(newParent)

        # update network node parentModuleBone attribute
        networkNode = self.modInst.returnNetworkNode
        cmds.setAttr(networkNode + ".parentModuleBone", lock=False)
        cmds.setAttr(networkNode + ".parentModuleBone", newParent, type="string", lock=True)

        # delete the old constraint and create the new one
        if cmds.objExists(self.modInst.name + "_mover_grp"):
            parent_constraint = cmds.listConnections(self.modInst.name + "_mover_grp.translateX")
            scale_constraint = cmds.listConnections(self.modInst.name + "_mover_grp.scaleX")
            if parent_constraint is not None:
                cmds.delete(parent_constraint[0])
            if scale_constraint is not None:
                cmds.delete(scale_constraint[0])

        networkNodes = utils.returnRigModules()
        mover = utils.findMoverNodeFromJointName(networkNodes, newParent, False, True)
        if mover is None:
            mover = utils.findMoverNodeFromJointName(networkNodes, newParent, True, False)

        if mover is not None:
            cmds.parentConstraint(mover, self.modInst.name + "_mover_grp", mo=True)
            cmds.scaleConstraint(mover, self.modInst.name + "_mover_grp", mo=True)

        # delete the UI
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        cmds.deleteUI(mayaWindow + "|" + windowObject)

        cmds.select(clear=True)
