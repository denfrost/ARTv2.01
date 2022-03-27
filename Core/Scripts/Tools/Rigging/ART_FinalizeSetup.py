from functools import partial
import os

import maya.cmds as cmds

import Utilities.utils as utils
import Utilities.riggingUtils as riggingUtils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_FinalizeSetup():

    def __init__(self, mainUI, skinToolsInst):

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.icons_path = settings.value("iconPath")

        self.rig_creator_inst = mainUI
        self.skin_tools_inst = skinToolsInst

        # build the UI
        self._build_interface()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        if cmds.window("ART_finalizeSetupWin", exists=True):
            cmds.deleteUI("ART_finalizeSetupWin", wnd=True)

        # launch a UI to get the name information
        self.window = QtWidgets.QMainWindow(self.rig_creator_inst)
        window_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/logo.png"))
        self.window.setWindowIcon(window_icon)

        # size policies
        main_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # load toolbar stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.window.setStyleSheet(self.style)

        # create the main widget
        self.central_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.central_widget)

        # set qt object name
        self.window.setObjectName("ART_finalizeSetupWin")
        self.window.setWindowTitle("Finalize Setup")

        # create the mainLayout for the rig creator UI
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.window.resize(450, 300)
        self.window.setSizePolicy(main_size_policy)
        self.window.setMinimumSize(QtCore.QSize(450, 300))
        self.window.setMaximumSize(QtCore.QSize(450, 300))

        # create the background image
        self.background_frame = QtWidgets.QFrame()
        self.main_layout.addWidget(self.background_frame)

        # create the main vertical layout inside the frame
        self.frame_layout = QtWidgets.QVBoxLayout(self.background_frame)

        self.image_label = QtWidgets.QLabel()
        self.image_label.setMinimumSize(QtCore.QSize(430, 230))
        self.image_label.setMaximumSize(QtCore.QSize(430, 230))
        self.frame_layout.addWidget(self.image_label)
        image = utils.returnNicePath(self.icons_path, "System/backgrounds/finalizeSetup.png")
        icon = QtGui.QPixmap(image)
        self.image_label.setPixmap(icon)

        # # # # BUTTON LAYOUT # # # #
        self.button_layout = QtWidgets.QHBoxLayout()
        self.frame_layout.addLayout(self.button_layout)

        self.continue_button = QtWidgets.QPushButton("Continue")
        self.continue_button.setMinimumHeight(25)
        self.continue_button.setMaximumHeight(25)
        self.continue_button.setObjectName("settings")
        self.continue_button.clicked.connect(partial(self._finalize_setup))
        self.button_layout.addWidget(self.continue_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setMinimumHeight(25)
        self.cancel_button.setMaximumHeight(25)
        self.cancel_button.setObjectName("settings")
        self.cancel_button.clicked.connect(partial(self._cancel_setup))
        self.button_layout.addWidget(self.cancel_button)

        self.help_button = QtWidgets.QPushButton("?")
        self.help_button.setMinimumSize(QtCore.QSize(25, 25))
        self.help_button.setMaximumSize(QtCore.QSize(25, 25))
        self.help_button.setObjectName("settings")
        self.help_button.clicked.connect(partial(self._launch_help))
        self.button_layout.addWidget(self.help_button)

        # show window
        self.window.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _finalize_setup(self):

        # delete UI
        self._cancel_setup()

        # toggle tab visibility
        self.rig_creator_inst.toolModeStack.setCurrentIndex(1)

        # update network node with state change
        if not cmds.objExists("ART_RIG_ROOT.state"):
            cmds.addAttr("ART_RIG_ROOT", ln="state", keyable=False)
        cmds.setAttr("ART_RIG_ROOT.state", 1)

        # wipe model pose attribute if it exists
        rig_modules = cmds.listConnections("ART_RIG_ROOT.rigModules")
        for rig_module in rig_modules:
            if cmds.objExists(rig_module + ".modelPose"):
                cmds.deleteAttr(rig_module + ".modelPose")

        # build bind skeleton
        renamed = riggingUtils.buildSkeleton()[1]
        if len(renamed) > 0:
            renamed_elements = []
            for each in renamed:
                prior_name = each.rpartition("_renamed")[0]
                renamed_elements.append([prior_name, "renamed to", each])
            win = interfaceUtils.DialogMessage("Warning", "The following items were renamed due to naming conflicts:",
                                               renamed_elements, 3, interfaceUtils.getMainWindow())
            win.show()

        # hide joint mover and lock
        lock_nodes = cmds.listRelatives("JointMover", children=True)
        for node in lock_nodes:
            cmds.setAttr(node + ".v", 0, lock=True)

        # lock nodes
        cmds.select("JointMover", hi=True)
        joint_mover_nodes = cmds.ls(sl=True)
        for node in joint_mover_nodes:
            cmds.lockNode(node, lock=True)

        # clear selection
        cmds.select(clear=True)

        # launch weight wizard
        import Tools.Rigging.ART_WeightWizard as aww
        aww.run(self.rig_creator_inst)

        # remove outliner scriptJobs
        for job in self.rig_creator_inst.scriptJobs:
            cmds.scriptJob(kill=job, force=True)

        # weight table scriptJob
        self.rig_creator_inst.scriptJobs.append(self.skin_tools_inst.weightTable_scriptJob())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _cancel_setup(self):

        if cmds.window("ART_finalizeSetupWin", exists=True):
            cmds.deleteUI("ART_finalizeSetupWin", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _launch_help(self):
        print "Not implemented yet. This will need to link to documentation online."
