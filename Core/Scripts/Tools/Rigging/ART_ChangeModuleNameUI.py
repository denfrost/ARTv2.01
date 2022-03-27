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


windowTitle = "Change Module Name"
windowObject = "pyArtChangeModuleNameUi"


class ART_ChangeModuleName_UI(QtWidgets.QMainWindow):
    """
    This class allows the user to change the prefix or suffix or both, of a given module. It is found within the
    skeletonSettingsUI of an individual module in the Rig Creator.

        .. image:: /images/changeModName.png

    """

    def __init__(self, baseName, moduleInst, rigUiInst, prefix, suffix, parent=None):
        """
        Instantiates the class, taking in current module information, and builds the interface.

        :param baseName: The base name of the module, found on the network node attribute.
        :param moduleInst: The instance in memory of the module whose name is to change.
        :param rigUiInst: The instance in memory of the Rig Creator UI from which this class was called.
        :param prefix: The existing prefix of the module name.
        :param suffix: The existing suffix of the module name.

        """

        super(ART_ChangeModuleName_UI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # create class variables
        self.baseName = baseName
        self.modInst = moduleInst
        self.rigUiInst = rigUiInst
        self.prefixInc = prefix
        self.suffixInc = suffix

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

        self.resize(300, 150)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(300, 150))
        self.setMaximumSize(QtCore.QSize(300, 150))

        # create the background image
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        # create the prefix pair of fields
        self.prefixForm = QtWidgets.QFormLayout()
        self.widgetLayout.addLayout(self.prefixForm)

        self.prefixLabel = QtWidgets.QLabel("Prefix: ")
        self.prefixForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.prefixLabel)

        self.prefix = QtWidgets.QLineEdit(self.prefixInc)
        self.prefixForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.prefix)

        # hookup signal/slot connection
        self.prefix.textChanged.connect(self.updatePreview)

        # create the suffix pair of fields
        self.suffixForm = QtWidgets.QFormLayout()
        self.widgetLayout.addLayout(self.suffixForm)

        self.suffixLabel = QtWidgets.QLabel("Suffix: ")
        self.suffixForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.suffixLabel)

        self.suffix = QtWidgets.QLineEdit(self.suffixInc)
        self.suffixForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.suffix)

        # hookup signal/slot connection
        self.suffix.textChanged.connect(self.updatePreview)

        # spacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLayout.addItem(spacerItem)

        # realtime preview of final module name
        self.previewForm = QtWidgets.QFormLayout()
        self.widgetLayout.addLayout(self.previewForm)
        self.previewLabel = QtWidgets.QLabel("Preview: ")
        self.previewName = QtWidgets.QLabel(self.prefixInc + self.baseName + self.suffixInc)
        self.previewName.setMinimumSize(QtCore.QSize(200, 20))
        self.previewName.setMaximumSize(QtCore.QSize(200, 20))
        self.previewName.setAlignment(QtCore.Qt.AlignHCenter)
        self.previewForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.previewLabel)
        self.previewForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.previewName)

        # set preview font
        font = QtGui.QFont()
        font.setPointSize(12)
        self.previewName.setFont(font)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLayout.addItem(spacerItem1)

        # update button
        self.updateBtn = QtWidgets.QPushButton("UPDATE")
        self.widgetLayout.addWidget(self.updateBtn)
        self.updateBtn.setMinimumSize(QtCore.QSize(285, 40))
        self.updateBtn.setMaximumSize(QtCore.QSize(285, 40))
        self.updateBtn.setSizePolicy(mainSizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateBtn.setFont(font)
        self.updateBtn.setObjectName("settings")

        # hookup signal/slot on create button
        self.updateBtn.clicked.connect(self.applyModuleNameChange)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updatePreview(self):
        """
        Updates the QLabel with the current prefix + basename + suffix, adding in underscores where needed.

        """

        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        string = ""
        if len(prefix) > 0:
            if not prefix.endswith("_"):
                string += prefix + "_"
            else:
                string += prefix

        string += self.baseName

        if len(suffix) > 0:
            if not suffix.startswith("_"):
                string += "_" + suffix
            else:
                string += suffix

        self.previewName.setText(string)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def applyModuleNameChange(self):
        """
        Checks to make sure a module doesn't exist with the new name, and if not, updates naming of the module in a
        multitude of places. Any UI elements, joint movers, attribute values (like .Created_Bones), etc.

        .. note::
            The following things get updated:
                  * QGroupBox label of the SkeletonSettingsUI
                  * Network Node .moduleName attribute
                  * Module Instance variable of self.name gets updated
                  * Created_Bones attribute values
                  * Joint Mover Nodes
                  * Rig Creator Outliner names for module
                  * Selection Script Job for outliner
                  * Any modules' attributes that have a value that matches the old name (like parent module bone)
                  * Any modules that are a mirror of this module, and their mirrorModule attribute value

        """

        # check to see if a module already has that name. If so, return out and do not continue
        modules = utils.returnRigModules()
        validName = False
        msg = "A module with that name already exists. Please enter a unique name for the module"

        for module in modules:
            name = cmds.getAttr(module + ".moduleName")
            if name == str(self.previewName.text()):
                cmds.confirmDialog(title="Name Exists", message=msg, icon="critical")
                return

        # update groupbox label
        originalName = self.modInst.groupBox.title()
        self.modInst.groupBox.setTitle(str(self.previewName.text()))

        # update network node moduleName attribute
        networkNode = self.modInst.returnNetworkNode
        cmds.setAttr(networkNode + ".moduleName", lock=False)
        cmds.setAttr(networkNode + ".moduleName", str(self.previewName.text()), type="string", lock=True)

        # update self.name for rig module
        self.modInst.name = str(self.previewName.text())

        # update created bones attribute values
        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        if len(prefix) > 0:
            if not prefix.endswith("_"):
                prefix += "_"
        if len(suffix) > 0:
            if not suffix.startswith("_"):
                suffix = "_" + suffix

        createdBones = self.modInst.returnCreatedJoints

        attrString = ""

        for bone in createdBones:
            trail = ""
            if cmds.getAttr(self.modInst.returnNetworkNode + ".moduleType") == "ART_Chain":
                trail = bone.rpartition("_")[2]

            niceName = bone
            if len(bone) > 1:
                if self.prefixInc != "":
                    niceName = bone.partition(self.prefixInc)[2]
                if self.suffixInc != "":
                    niceName = niceName.partition(self.suffixInc)[0]

                if cmds.getAttr(self.modInst.returnNetworkNode + ".moduleType") == "ART_Chain":
                    attrString += prefix + niceName + suffix + "_" + trail + "::"
                else:
                    attrString += prefix + niceName + suffix + "::"

        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # joint mover renaming
        cmds.select(originalName + "_mover_grp", hi=True)
        jointMoverNodes = cmds.ls(sl=True, type="transform")
        constraints = ["pointConstraint", "orientConstraint", "parentConstraint"]

        for node in jointMoverNodes:
            try:
                if cmds.nodeType(node) not in constraints:
                    locked = cmds.lockNode(node, q=True)
                    if locked:
                        cmds.lockNode(node, lock=False)
                    nodeName = node.partition(originalName)[2]
                    newName = self.modInst.name + nodeName
                    cmds.rename(node, newName)

                    if locked:
                        cmds.lockNode(node, lock=True)
            except Exception, e:
                pass

        # update outliner names
        utils.findAndRenameOutlinerChildren(self.modInst.outlinerWidgets[self.modInst.originalName + "_treeModule"],
                                            originalName, self.modInst.name)
        self.modInst.outlinerWidgets[self.modInst.originalName + "_treeModule"].setText(0, self.modInst.name)

        # fix module instance outliner widgets keys to reference new module name
        value = self.modInst.outlinerWidgets.get(originalName + "_treeModule")
        del self.modInst.outlinerWidgets[originalName + "_treeModule"]
        self.modInst.outlinerWidgets[self.modInst.name + "_treeModule"] = value

        # find module's selection scriptJob and delete it
        jobs = cmds.scriptJob(lj=True)
        for job in jobs:
            compareString = job.partition(":")[0]
            try:
                if str(self.modInst.scriptJob) == str(compareString):
                    cmds.scriptJob(kill=self.modInst.scriptJob)
                    break
            except AttributeError:
                pass

        # replace module's outliner control entries with the new control name
        for item in self.modInst.outlinerControls:
            item[1] = item[1].replace(originalName, self.modInst.name)

        # create the selection script job again
        self.modInst.createScriptJob()

        # find any modules using any of the created joints from this module that match the OLD name
        createdJoints = self.modInst.returnCreatedJoints
        modules = self.modInst.getAllModules

        for mod in modules:
            attrs = cmds.listAttr(mod)
            if "parentModuleBone" in attrs:
                value = cmds.getAttr(mod + ".parentModuleBone")
                if value in createdBones:
                    index = createdBones.index(value)

                    # update those modules' network node parentModuleBone attribute
                    cmds.setAttr(mod + ".parentModuleBone", lock=False)
                    cmds.setAttr(mod + ".parentModuleBone", createdJoints[index], type="string", lock=True)

                    # and also those modules' skeletonSettingsUI currentParent label
                    modName = cmds.getAttr(mod + ".moduleName")

                    for each in self.rigUiInst.moduleInstances:
                        try:
                            if each.networkNode == mod:
                                # find the current groupBox for this module
                                for i in range(self.rigUiInst.moduleSettingsLayout.count()):
                                    if type(self.rigUiInst.moduleSettingsLayout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                                        if self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().title() == modName:
                                            self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().setParent(None)

                                            # relaunch the skeleton settings UI with new info
                                            each.skeletonSettings_UI(modName)
                        except AttributeError:
                            pass

        # update mirrorModule field
        for mod in modules:
            attrs = cmds.listAttr(mod)
            if "mirrorModule" in attrs:
                value = cmds.getAttr(mod + ".mirrorModule")

                if value == originalName:
                    cmds.setAttr(mod + ".mirrorModule", lock=False)
                    cmds.setAttr(mod + ".mirrorModule", self.modInst.name, type="string", lock=True)

                    # and also those modules' skeletonSettingsUI currentParent label
                    modName = cmds.getAttr(mod + ".moduleName")

                    for each in self.rigUiInst.moduleInstances:
                        try:
                            if each.networkNode == mod:
                                # find the current groupBox for this module
                                for i in range(self.rigUiInst.moduleSettingsLayout.count()):
                                    if type(self.rigUiInst.moduleSettingsLayout.itemAt(i).widget()) == QtWidgets.QGroupBox:
                                        if self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().title() == modName:
                                            self.rigUiInst.moduleSettingsLayout.itemAt(i).widget().setParent(None)

                                            # relaunch the skeleton settings UI with new info
                                            each.skeletonSettings_UI(modName)
                        except AttributeError:
                            print each

        # delete the UI
        mayaWindow = interfaceUtils.getMainWindow()
        mayaWindow = mayaWindow.objectName()
        cmds.deleteUI(mayaWindow + "|" + windowObject)

        cmds.select(clear=True)
