"""
Author: Jeremy Ernst
"""

import maya.cmds as cmds
import os

import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

windowTitle = "Add Module"
windowObject = "pyArtAddModuleUi"


class ART_AddModule_UI(QtWidgets.QMainWindow):
    """
    This class builds a UI used by the rig creator, and is called when a user pushed a module button to add to their
    rig. This UI presents options like prefix, suffix, and ability to specify the parent module bone.

    .. image:: /images/addModuleUI.png

    """

    def __init__(self, baseName, className, rigUiInst, parent=None):
        """
        Initialize the class, taking in the base name of the module to be added, the name of the class of the module
        to be added, and the instance of the rig creator UI. Then build the interface for the tool.

        :param baseName: The base name of the module to be added, defined in the module class file at the top.
        :param className: The class name of the module to be added, so we can then initialize that module.
        :param rigUiInst: The instance of the rig creator UI, from which this function was called.

        """

        super(ART_AddModule_UI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # create class variables
        self.baseName = baseName
        self.className = className
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
        self.mainLayout = QtWidgets.QHBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(500, 220))
        self.setMaximumSize(QtCore.QSize(500, 520))

        # create the background
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.column1layout = QtWidgets.QVBoxLayout(self.frame)
        self.mainLayout.addLayout(self.column1layout)

        self.column2Layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.column2Layout)

        font = QtGui.QFont()
        font.setBold(True)

        label = QtWidgets.QLabel("Choose Parent Bone")
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.column2Layout.addWidget(label)

        self.boneSearch = QtWidgets.QLineEdit()
        self.column2Layout.addWidget(self.boneSearch)
        self.boneSearch.setObjectName("light")
        self.boneSearch.setPlaceholderText("Search...")
        self.boneSearch.textChanged.connect(self.searchList)

        self.hierarchyTree = QtWidgets.QListWidget()
        self.column2Layout.addWidget(self.hierarchyTree)

        # add items to listWidget
        parents = utils.getViableParents()
        for bone in parents:
            self.hierarchyTree.addItem(bone)

            if bone == "root":
                index = parents.index(bone)
                self.hierarchyTree.setCurrentRow(index)

        # create the prefix pair of fields
        self.prefixForm = QtWidgets.QFormLayout()
        self.column1layout.addLayout(self.prefixForm)

        self.prefixLabel = QtWidgets.QLabel("Prefix: ")
        self.prefixForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.prefixLabel)

        self.prefix = QtWidgets.QLineEdit()
        self.prefix.setObjectName("light")
        self.prefixForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.prefix)

        # hookup signal/slot connection
        self.prefix.textChanged.connect(self.updatePreview)

        # create the suffix pair of fields
        self.suffixForm = QtWidgets.QFormLayout()
        self.column1layout.addLayout(self.suffixForm)

        self.suffixLabel = QtWidgets.QLabel("Suffix: ")
        self.suffixForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.suffixLabel)

        self.suffix = QtWidgets.QLineEdit()
        self.suffix.setObjectName("light")
        self.suffixForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.suffix)

        # hookup signal/slot connection
        self.suffix.textChanged.connect(self.updatePreview)

        self.previewLabel = QtWidgets.QLabel("Module Name: ")
        self.column1layout.addWidget(self.previewLabel)

        self.previewName = QtWidgets.QLabel(self.baseName)
        self.previewName.setMinimumSize(QtCore.QSize(255, 25))
        self.previewName.setMaximumSize(QtCore.QSize(255, 25))
        self.previewName.setAlignment(QtCore.Qt.AlignHCenter)
        self.column1layout.addWidget(self.previewName)

        # set preview font
        font = QtGui.QFont()
        font.setPointSize(12)
        self.previewName.setFont(font)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.column1layout.addItem(spacerItem1)

        # special cases (arms and legs)
        specialCaseModules = ["ART_Leg_Standard", "ART_Arm_Standard"]
        if className in specialCaseModules:
            # spacer
            groupBox = QtWidgets.QGroupBox("")
            self.column1layout.addWidget(groupBox)
            layout = QtWidgets.QVBoxLayout(groupBox)

            self.radioButtonLayout = QtWidgets.QHBoxLayout()
            layout.addLayout(self.radioButtonLayout)
            self.rightRadioBtn = QtWidgets.QRadioButton("Right Side")
            self.leftRadioBtn = QtWidgets.QRadioButton("Left Side")
            self.radioButtonLayout.addWidget(self.rightRadioBtn)
            self.radioButtonLayout.addWidget(self.leftRadioBtn)
            self.leftRadioBtn.setChecked(True)

        # spacer
        spacerItem2 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.column1layout.addItem(spacerItem2)

        # create button
        self.createButton = QtWidgets.QPushButton("CREATE")
        self.column1layout.addWidget(self.createButton)
        self.createButton.setMinimumSize(QtCore.QSize(255, 40))
        self.createButton.setMaximumSize(QtCore.QSize(255, 40))
        self.createButton.setSizePolicy(mainSizePolicy)
        self.createButton.setObjectName("settings")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.createButton.setFont(font)

        # hookup signal/slot on create button
        self.createButton.clicked.connect(self.createModule)

        self.hierarchyTree.setFocus()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updatePreview(self):
        """
        Read the prefix and suffix QLineEdits, append an underscore, and update the previewName QLabel with the
        prefix, basename, and suffix to show what the final module name will be.

        """

        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        string = ""
        if len(prefix) > 0:
            string += prefix + "_"

        string += self.baseName

        if len(suffix) > 0:
            string += "_" + suffix

        self.previewName.setText(string)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createModule(self):
        """
        Instantiate our module class to create with the user specified name, creating the network node, building
        the Skeleton Settings UI for the module, adding the joint mover for that module (importing the joint mover
        file), and adding the joint mover to the outliner.

        """

        mod = __import__("RigModules." + self.className, {}, {}, [self.className])

        # get the up-axis
        self.up = cmds.upAxis(q=True, ax=True)

        # get the class name from that module file (returns RigModules.ART_Root.ART_Root for example)
        moduleClass = getattr(mod, mod.className)
        jmPath = mod.jointMover

        if self.up == "y":
            jmPath = jmPath.replace("z_up", "y_up")

        # get the name for the module to be created
        userSpecName = str(self.previewName.text())

        # check to see if a module already has that name
        modules = utils.returnRigModules()
        for module in modules:
            name = cmds.getAttr(module + ".moduleName")
            if name == userSpecName:
                cmds.confirmDialog(title="Name Exists",
                                   message="A module with that name already exists. Please enter a unique name.",
                                   icon="critical")
                return

        # call functions to create network node, skeleton settings UI
        moduleInst = moduleClass(self.rigUiInst, userSpecName)
        self.rigUiInst.moduleInstances.append(moduleInst)  # add this instance to the ui's list of module instances
        networkNode = moduleInst.buildNetwork()

        # figure out side
        specialCaseModules = ["ART_Leg_Standard", "ART_Arm_Standard"]
        if self.className in specialCaseModules:
            side = "Left"
            if self.rightRadioBtn.isChecked():
                side = "Right"
                cmds.setAttr(networkNode + ".side", lock=False)
                cmds.setAttr(networkNode + ".side", "Right", type="string", lock=True)

            # build new jmPath name
            jmPath = jmPath.partition(".ma")[0] + "_" + side + ".ma"

        moduleInst.skeletonSettings_UI(userSpecName)
        moduleInst.jointMover_Build(jmPath)
        moduleInst.addJointMoverToOutliner()



        # update the created joints attribute on the network node with the new names
        prefix = str(self.prefix.text())
        suffix = str(self.suffix.text())

        if len(prefix) > 0:
            prefix = prefix + "_"
        if len(suffix) > 0:
            suffix = "_" + suffix

        createdBones = cmds.getAttr(networkNode + ".Created_Bones")
        createdBones = createdBones.split("::")

        attrString = ""
        if self.className in ["ART_Chain"]:
            for i in range(len(createdBones) - 1):
                attrString += prefix + createdBones[i] + suffix + "_0" + str(i + 1) + "::"

        else:
            for bone in createdBones:
                if len(bone) > 1:
                        attrString += prefix + bone + suffix + "::"

        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # update the self.currentParent label and the parentModuleBone attr on the network node
        parent = (self.hierarchyTree.currentItem().text())
        moduleInst.currentParent.setText(parent)

        cmds.setAttr(networkNode + ".parentModuleBone", lock=False)
        cmds.setAttr(networkNode + ".parentModuleBone", parent, type="string", lock=True)

        # parent the joint mover to the offset mover of the parent
        mover = ""

        if parent == "root":
            mover = "root_mover"

        else:
            # find the parent mover name to parent to
            networkNodes = utils.returnRigModules()

            mover = utils.findMoverNodeFromJointName(networkNodes, parent, False, True)

            if mover is None:
                mover = utils.findMoverNodeFromJointName(networkNodes, parent, True, False)

        if mover is not None:
            cmds.parentConstraint(mover, userSpecName + "_mover_grp", mo=True)
            cmds.scaleConstraint(mover, userSpecName + "_mover_grp")

        # delete the UI
        cmds.deleteUI(windowObject)

        # obey the current UI visibility toggles
        self.rigUiInst.setMoverVisibility()
        moduleInst.updateBoneCount()
        self.rigUiInst.populateNetworkList()

        # turn on aim mode
        moduleInst.aimMode(True)

        # select global mover and fit to viewport
        globalMover = utils.findGlobalMoverFromName(userSpecName)
        cmds.select(globalMover)
        cmds.setToolTo("moveSuperContext")

        utils.fitViewAndShade()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def searchList(self):
        """
        Get the search text from the QLineEdit and search the items in the QListWidget for any matches. Anything that
        does not match will be hidden in the QListWidget.

        """

        searchText = self.boneSearch.text()

        for i in range(self.hierarchyTree.count()):
            lwItem = self.hierarchyTree.item(i)
            if lwItem.text().find(searchText) != -1:
                lwItem.setHidden(False)
            else:
                lwItem.setHidden(True)
