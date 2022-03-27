"""
Author: Jeremy Ernst
"""

from functools import partial
import os
import maya.cmds as cmds
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils

from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_BoneCounter():
    """
    This class builds a simple interface that allows a user to see what the total bone count of their asset will be
    given the current module settings. It also allows the user to set a bone count target.

    It can be found on the Rig Creator toolbar with this icon:
        .. image:: /images/boneCounterButton.png

    The interface looks like this:
        .. image:: /images/boneCounter.png

    """
    def __init__(self, mainUI):
        """
        Instantiates this class, getting the QSettings and calling on the method to build the interface for the tool.

        :param mainUI: The instance of the Rig Creator UI from which this class was called.

        .. seealso:: ART_BoneCounter.buildBoneCounterUI

        """

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        self.buildBoneCounterUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildBoneCounterUI(self):
        """
        Builds the interface for the bone counter tool, which is comprised off a QLineEdit that shows the current
        bone count, a QPushButton to launch another simple UI that allows the user to set a bone count target,
        and QProgressBar that shows a percentage to target bone count.

        .. seealso:: ART_BoneCounter.setBoneCountTarget

        """

        if cmds.window("ART_BoneCounterWin", exists=True):
            cmds.deleteUI("ART_BoneCounterWin", wnd=True)

        # launch a UI to get the name information
        self.boneCounterWin = QtWidgets.QMainWindow(self.mainUI)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.boneCounterWin.setWindowIcon(window_icon)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.boneCounterWin_mainWidget = QtWidgets.QWidget()
        self.boneCounterWin.setCentralWidget(self.boneCounterWin_mainWidget)

        # set qt object name
        self.boneCounterWin.setObjectName("ART_BoneCounterWin")
        self.boneCounterWin.setWindowTitle("Bone Counter")

        # create the mainLayout for the rig creator UI
        self.boneCounterWin_mainLayout = QtWidgets.QVBoxLayout(self.boneCounterWin_mainWidget)
        self.boneCounterWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.boneCounterWin.resize(300, 100)
        self.boneCounterWin.setSizePolicy(mainSizePolicy)
        self.boneCounterWin.setMinimumSize(QtCore.QSize(300, 100))
        self.boneCounterWin.setMaximumSize(QtCore.QSize(300, 100))

        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # load toolbar stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")

        # create the background image
        self.boneCounterWin_frame = QtWidgets.QFrame()
        self.boneCounterWin_mainLayout.addWidget(self.boneCounterWin_frame)
        self.boneCounterWin.setStyleSheet(self.style)

        # create the layout for the widgets
        self.boneCounterWin_widgetLayoutMain = QtWidgets.QVBoxLayout(self.boneCounterWin_frame)
        self.boneCounterWin_widgetLayoutMain.setContentsMargins(5, 5, 5, 5)
        self.boneCounterWin_widgetLayout = QtWidgets.QHBoxLayout()
        self.boneCounterWin_widgetLayoutMain.addLayout(self.boneCounterWin_widgetLayout)

        # label creation
        self.boneCount = QtWidgets.QLabel("Bone Count:      ")
        self.boneCount.setFont(headerFont)
        self.boneCounterWin_widgetLayout.addWidget(self.boneCount)

        self.boneCounter = QtWidgets.QSpinBox()
        self.boneCounter.setReadOnly(True)
        self.boneCounter.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.boneCounter.setRange(1, 9999)
        self.boneCounter.setMinimumWidth(60)
        self.boneCounter.setMaximumWidth(60)
        self.boneCounterWin_widgetLayout.addWidget(self.boneCounter)

        # create the button
        self.boneMaxButton = QtWidgets.QPushButton("Set Target")
        self.boneCounterWin_widgetLayout.addWidget(self.boneMaxButton)
        self.boneMaxButton.clicked.connect(partial(self.setBoneCountTarget))
        self.boneMaxButton.setMinimumHeight(30)
        self.boneMaxButton.setStyleSheet(self.style)
        self.boneMaxButton.setObjectName("settings")

        # add the progress bar
        self.boneCountBar = QtWidgets.QProgressBar()
        self.boneCounterWin_widgetLayoutMain.addWidget(self.boneCountBar)
        self.boneCountBar.setValue(1)
        self.boneCountBar.setRange(0, 100)
        self.boneCountBar.setFormat("target = %m")

        # add the max range of the progress bar to the main network node
        if cmds.objExists("ART_Root_Module.target"):
            value = cmds.getAttr("ART_Root_Module.target")
            currentValue = self.boneCountBar.value()
            self.boneCountBar.setMaximum(value)

            if value < currentValue:
                self.boneCountBar.setValue(value)

            if currentValue > value:
                self.boneCountBar.setObjectName("max")
            else:
                self.boneCountBar.setObjectName("normal")
            self.boneCountBar.style().unpolish(self.boneCountBar)
            self.boneCountBar.style().polish(self.boneCountBar)

        else:
            cmds.addAttr("ART_Root_Module", sn="target", keyable=False)
            cmds.setAttr("ART_Root_Module.target", 100, lock=True)

        # get the current bone count
        modules = utils.returnRigModules()
        allBones = []
        for module in modules:
            joints = cmds.getAttr(module + ".Created_Bones")
            splitJoints = joints.split("::")

            for bone in splitJoints:
                if bone != "":
                    allBones.append(bone)

        # update the spinBox and progress bar
        self.boneCounter.setValue(len(allBones))
        max = self.boneCountBar.maximum()

        if len(allBones) <= max:
            self.boneCountBar.setValue(len(allBones))
            self.boneCountBar.setObjectName("normal")
            self.boneCountBar.style().unpolish(self.boneCountBar)
            self.boneCountBar.style().polish(self.boneCountBar)
        if len(allBones) > max:
            self.boneCountBar.setValue(max)
            self.boneCountBar.setObjectName("max")
            self.boneCountBar.style().unpolish(self.boneCountBar)
            self.boneCountBar.style().polish(self.boneCountBar)

        # show window
        self.boneCounterWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setBoneCountTarget(self):
        """
        Builds a UI that allows the user to set the target bone count.

            .. image:: /images/boneCountTarget.png

        """

        # launch a UI to get the name information
        self.targetWindow = QtWidgets.QMainWindow()
        self.targetWindow.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.targetWindow_mainWidget = QtWidgets.QWidget()
        self.targetWindow.setCentralWidget(self.targetWindow_mainWidget)

        # set qt object name
        self.targetWindow.setObjectName("ART_setBoneCountTarget_UI")
        self.targetWindow.setWindowTitle("Bone Count")

        # create the mainLayout for the rig creator UI
        self.targetWindow_topLayout = QtWidgets.QVBoxLayout(self.targetWindow_mainWidget)
        self.targetWindow_mainLayout = QtWidgets.QFormLayout()
        self.targetWindow_topLayout.addLayout(self.targetWindow_mainLayout)

        self.targetWindow_topLayout.setContentsMargins(10, 10, 10, 10)
        self.targetWindow.resize(250, 70)
        self.targetWindow.setSizePolicy(mainSizePolicy)
        self.targetWindow.setMinimumSize(QtCore.QSize(250, 70))
        self.targetWindow.setMaximumSize(QtCore.QSize(250, 70))

        # add label
        label = QtWidgets.QLabel("Enter a target bone count:        ")
        self.targetWindow_mainLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, label)

        # add spinBox
        self.targetWindow_SpinBox = QtWidgets.QSpinBox()
        self.targetWindow_SpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.targetWindow_SpinBox.setRange(1, 9999)
        self.targetWindow_SpinBox.setMinimumWidth(70)
        self.targetWindow_SpinBox.setStyleSheet(self.style)
        self.targetWindow_mainLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.targetWindow_SpinBox)
        self.targetWindow_SpinBox.setValue(100)
        self.targetWindow_SpinBox.setObjectName("ART_targetWindowSpinBox")

        # add a confirm button
        self.targetWindow_confirmButton = QtWidgets.QPushButton("Confirm")
        self.targetWindow_topLayout.addWidget(self.targetWindow_confirmButton)

        self.targetWindow_confirmButton.setObjectName("settings")
        self.targetWindow_confirmButton.setMinimumHeight(30)
        self.targetWindow_confirmButton.setMaximumHeight(30)
        self.targetWindow_confirmButton.clicked.connect(self.setBoneCountTarget_Confirm)

        # show the window
        self.targetWindow.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setBoneCountTarget_Confirm(self):
        """
        Take the QSpinBox value for the new target and refresh the main UI with the new data.

        """

        newMax = self.targetWindow_SpinBox.value()
        cmds.deleteUI("ART_setBoneCountTarget_UI", wnd=True)

        value = self.boneCounter.value()
        currentValue = self.boneCountBar.value()
        self.boneCountBar.setMaximum(newMax)
        max = self.boneCountBar.maximum()

        cmds.setAttr("ART_Root_Module.target", lock=False)
        cmds.setAttr("ART_Root_Module.target", newMax, lock=True)

        if newMax < currentValue:
            self.boneCountBar.setValue(max)

        if value <= max:
            self.boneCountBar.setObjectName("normal")
            self.boneCountBar.style().unpolish(self.boneCountBar)
            self.boneCountBar.style().polish(self.boneCountBar)
        if value > max:
            self.boneCountBar.setObjectName("max")
            self.boneCountBar.style().unpolish(self.boneCountBar)
            self.boneCountBar.style().polish(self.boneCountBar)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def updateBoneCount(self):
        """
        Updates the interface based on new module information. Usually triggered when a module has had its settings
        changed.

        """

        try:
            modules = utils.returnRigModules()
            allBones = []
            for module in modules:
                joints = cmds.getAttr(module + ".Created_Bones")
                splitJoints = joints.split("::")

                for bone in splitJoints:
                    if bone != "":
                        allBones.append(bone)

            # update the spinBox and progress bar
            self.boneCounter.setValue(len(allBones))
            max = self.boneCountBar.maximum()

            if len(allBones) <= max:
                self.boneCountBar.setObjectName("normal")
                self.boneCountBar.style().unpolish(self.boneCountBar)
                self.boneCountBar.style().polish(self.boneCountBar)
            if len(allBones) > max:
                self.boneCountBar.setObjectName("max")
                self.boneCountBar.style().unpolish(self.boneCountBar)
                self.boneCountBar.style().polish(self.boneCountBar)
        except:
            pass
