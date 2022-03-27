"""
Author: Jeremy Ernst
"""

# import statements
import json
import os
import sys
import subprocess
import tempfile
from functools import partial

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
import maya.mel as mel
# noinspection PyUnresolvedReferences
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class Export_FBX(object):
    """
    Class for export FBX animation data.
    """
    def __init__(self, force=False, euler=False, quat=True):

        self.force = force
        self.euler = euler
        self.quat = quat
        self._fbx_export()

    def _get_sequence_data(self):

        character_modules = utils.returnCharacterModules()
        characters = []
        for each in character_modules:
            characters.append(cmds.getAttr(each + ".namespace"))

        sequence_data = []

        for character in characters:
            if cmds.objExists(character + ":ART_RIG_ROOT.fbxAnimData"):
                fbxData = json.loads(cmds.getAttr(character + ":ART_RIG_ROOT.fbxAnimData"))

                # each entry in the fbxData list is a sequence with all the needed information
                for data in fbxData:
                    export_data = data[7]
                    export_data.extend(data[5])
                    export_data.extend(data[6])
                    sequence_data.append(export_data)

        return sequence_data

    def _set_export_flags(self, startFrame, endFrame):

        # in 2015, if oneClick isn't loaded, it will throw up an error
        try:
            cmds.loadPlugin("OneClick.mll")
            sys.stdout.write("Loaded OneClick plugin.")
            sys.stdout.write("\n")
        except RuntimeError:
            sys.stderr.write("unable to load OneClick plugin.")
            sys.stderr.write("\n")

        try:
            cmds.loadPlugin("fbxmaya.mll")
            sys.stdout.write("Loaded FBX plugin.")
            sys.stdout.write("\n")
        except RuntimeError:
            sys.stderr.write("unable to load FBX plugin.")
            sys.stderr.write("\n")

        # Mesh
        mel.eval("FBXExportSmoothingGroups -v true")
        mel.eval("FBXExportHardEdges -v false")
        mel.eval("FBXExportTangents -v false")
        mel.eval("FBXExportInstances -v false")
        mel.eval("FBXExportInAscii -v true")
        mel.eval("FBXExportSmoothMesh -v false")

        # Animation
        mel.eval("FBXExportBakeComplexAnimation -v true")
        mel.eval("FBXExportBakeComplexStart -v " + str(startFrame))
        mel.eval("FBXExportBakeComplexEnd -v " + str(endFrame))
        mel.eval("FBXExportReferencedAssetsContent -v true")
        mel.eval("FBXExportBakeComplexStep -v 1")
        mel.eval("FBXExportUseSceneName -v false")
        mel.eval("FBXExportFileVersion -v FBX201400")

        if self.euler:
            mel.eval("FBXExportQuaternion -v euler")

        if self.quat:
            mel.eval("FBXExportQuaternion -v quaternion")

        mel.eval("FBXExportShapes -v true")
        mel.eval("FBXExportSkins -v true")
        mel.eval("FBXExportUpAxis z")

        # garbage we don't want
        # Constraints
        mel.eval("FBXExportConstraints -v false")

        # Cameras
        mel.eval("FBXExportCameras -v false")

        # Lights
        mel.eval("FBXExportLights -v false")

        # Embed Media
        mel.eval("FBXExportEmbeddedTextures -v false")

        # Connections
        mel.eval("FBXExportInputConnections -v false")

    def _fbx_export(self):
        """
        exports the FBX animation data for each sequence found in the file.
        """

        if cmds.objExists("root"):
            if self.force is True:
                try:
                    cmds.delete("root")
                except StandardError:
                    cmds.warning("unable to delete root joint. Aborting")
                    return
            else:
                status = self._warn_user()
                if status is False:
                    return

        current_start = cmds.playbackOptions(q=True, min=True)
        current_end = cmds.playbackOptions(q=True, max=True)

        sequences = self._get_sequence_data()

        # Loop through sequence data.
        for sequence_info in sequences:
            character = sequence_info[0]
            do_export = sequence_info[1]
            export_path = sequence_info[2]
            start_frame = sequence_info[3]
            end_frame = sequence_info[4]
            pre_script = sequence_info[10]
            post_script = sequence_info[12]

            if os.path.exists(pre_script):
                self._execute_script(pre_script)

            if not os.path.exists(os.path.dirname(export_path)):
                cmds.warning("path does not exist: " + os.path.dirname(export_path))
                continue

            cmds.playbackOptions(min=start_frame, max=end_frame)

            if do_export is True:
                # Duplicate the skeleton and constrain it to the original.
                duplicate_joints = cmds.duplicate(character + ":root")

                for joint in duplicate_joints:
                    attrs = cmds.listAttr(joint, keyable=True, unlocked=True)
                    for each in attrs:
                        cmds.connectAttr(character + ":" + joint + "." + each, joint + "." + each)

                # Rename joints if override data is present.
                self._rename_joints(character)
                self._set_export_flags(start_frame, end_frame)

                if os.path.exists(post_script):
                    self._execute_script(post_script)

                # Export the FBX file.
                cmds.select(duplicate_joints[0])
                export_path = utils.returnFriendlyPath(export_path)
                mel.eval("FBXExport -f \"" + export_path + "\" -s")

                if cmds.objExists(duplicate_joints[0]):
                    cmds.delete(duplicate_joints[0])

        cmds.playbackOptions(min=current_start, max=current_end)

    def _rename_joints(self, character):
        if cmds.objExists(character + ":ART_RIG_ROOT.exportOverrides"):
            connections = cmds.listConnections(character + ":ART_RIG_ROOT.exportOverrides")
            if connections is not None:
                attrs = cmds.listAttr(connections[0], ud=True)
                for attr in attrs:
                    value = cmds.getAttr(connections[0] + "." + attr)
                    if cmds.objExists(attr):
                        cmds.rename(attr, value)

    def _warn_user(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("There is a joint named \"root\" in the scene without a namespace. This should not be the"
                       " case. If this is from a skeleton other than ARTv2, please rename or add a namespace."
                       " Otherwise, this is likely errant and should be deleted. Delete this root and continue?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        ret = msgBox.exec_()
        if ret == QtWidgets.QMessageBox.Ok:
            try:
                cmds.delete("root")
            except StandardError:
                cmds.warning("unable to delete root joint. Aborting")
                return False
        else:
            return False

    def _execute_script(self, script):

        source_type = ""
        status = False

        if script.find(".py") != -1:
            source_type = "python"

        if script.find(".mel") != -1:
            source_type = "mel"

        # MEL
        if source_type == "mel":
            try:
                command = ""
                # open the file, and for each line in the file, add it to our command string.
                f = open(script, 'r')
                lines = f.readlines()
                for line in lines:
                    command += line

                import maya.mel as mel
                mel.eval(command)
                status = True
            except:
                pass

        # PYTHON
        if source_type == "python":
            try:
                execfile("" + script + "")
                status = True
            except:
                pass

        return status



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_ExportMotion(object):
    """
    This class is used to export FBX animation from the rig to Unreal Engine. It supports morph targets,
    custom attribute curves, and pre/post

    It can be found on the animation sidebar with this icon:
        .. image:: /images/exportMotionButton.png

    .. todo:: Add the ability to export alembic and animation curve data.

    """

    def __init__(self, animPickerUI):
        """
        Instantiates the class, getting the QSettings and calling on the function to build the interface.

        :param animPickerUI: Instance of the Animation UI from which this class was called.

        """

        super(ART_ExportMotion, self).__init__()

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.pickerUI = animPickerUI

        # build the UI
        self._buildUI()

    def _buildUI(self):

        if cmds.window("pyART_ExportMotionWIN", exists=True):
            cmds.deleteUI("pyART_ExportMotionWIN", wnd=True)

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.pickerUI)
        self.mainWin.resizeEvent = self._window_resized

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.tabStyle = interfaceUtils.get_style_sheet("small_tabs")
        self.mainWin.setStyleSheet(self.style)

        self.mainWin.setMinimumSize(QtCore.QSize(470, 500))
        self.mainWin.setMaximumSize(QtCore.QSize(470, 900))
        self.mainWin.resize(470, 500)
        self.mainWin.closeEvent = self.closeEvent

        # set qt object name
        self.mainWin.setObjectName("pyART_ExportMotionWIN")
        self.mainWin.setWindowTitle("Export Motion")

        # tabs
        self.exportTabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.exportTabs)
        self.exportTabs.setStyleSheet(self.tabStyle)

        # FBX Tab
        self.fbxExportTab = QtWidgets.QWidget()
        self.exportTabs.addTab(self.fbxExportTab, "FBX")

        # ABC Tab
        self.abcExportTab = QtWidgets.QWidget()
        self.exportTabs.addTab(self.abcExportTab, "ABC")

        # Anim Curve Tab
        self.animExportTab = QtWidgets.QWidget()
        self.exportTabs.addTab(self.animExportTab, "Animation")

        # =======================================================================
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # #FBX TAB
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # =======================================================================
        self.fbxTabLayoutFrame = QtWidgets.QFrame(self.fbxExportTab)
        self.fbxTabLayoutFrame.setObjectName("dark")
        self.fbxTabLayoutFrame.setMinimumSize(450, 410)
        self.fbxTabLayoutFrame.setMaximumSize(450, 900)
        self.fbxTabLayoutFrame.setStyleSheet(self.style)

        self.fbxTabLayout = QtWidgets.QVBoxLayout(self.fbxTabLayoutFrame)

        # FBX Export Tabs
        self.fbxTabs = QtWidgets.QTabWidget()
        self.fbxTabLayout.addWidget(self.fbxTabs)

        self.fbxTabs.setStyleSheet(self.tabStyle)

        # Settings Tab
        self.exportSettings = QtWidgets.QWidget()
        self.fbxTabs.addTab(self.exportSettings, "Settings")
        self.settingsTabLayout = QtWidgets.QVBoxLayout(self.exportSettings)

        # Anim Curve Tab
        self.sequencesTab = QtWidgets.QWidget()
        self.fbxTabs.addTab(self.sequencesTab, "Sequences")
        self.sequenceTabLayout = QtWidgets.QVBoxLayout(self.sequencesTab)

        # =======================================================================
        # =======================================================================
        # =======================================================================
        # # Export Settings
        # =======================================================================
        # =======================================================================
        # =======================================================================
        self.exportSettings = QtWidgets.QFrame()
        self.exportSettings.setMinimumSize(QtCore.QSize(415, 330))
        self.exportSettings.setMaximumSize(QtCore.QSize(415, 900))
        self.settingsTabLayout.addWidget(self.exportSettings)

        self.settingsLayout = QtWidgets.QVBoxLayout(self.exportSettings)

        # export meshes checkbox
        self.exportMeshCB = QtWidgets.QCheckBox("Export Meshes")
        self.settingsLayout.addWidget(self.exportMeshCB)
        self.exportMeshCB.setChecked(False)

        # horizontal layout for morphs and custom attr curves
        self.settings_cb_layout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.settings_cb_layout)

        # export morphs and custom attr curves checkboxes
        self.exportMorphsCB = QtWidgets.QCheckBox("Export Morph Targets")
        self.settings_cb_layout.addWidget(self.exportMorphsCB)
        self.exportMorphsCB.setChecked(True)

        self.exportCustomAttrsCB = QtWidgets.QCheckBox("Export Custom Attribute Curves")
        self.settings_cb_layout.addWidget(self.exportCustomAttrsCB)
        self.exportCustomAttrsCB.setChecked(True)

        # horizontal layout for list widgets (morphs and custom attrs)
        self.settings_list_layout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.settings_list_layout)

        # list widgets for listing morphs and custom attr curves
        self.exportMorphList = QtWidgets.QListWidget()
        self.exportMorphList.setMinimumSize(QtCore.QSize(185, 150))
        self.exportMorphList.setMaximumSize(QtCore.QSize(185, 150))
        self.settings_list_layout.addWidget(self.exportMorphList)
        self.exportMorphList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.exportCurveList = QtWidgets.QListWidget()
        self.exportCurveList.setMinimumSize(QtCore.QSize(185, 150))
        self.exportCurveList.setMaximumSize(QtCore.QSize(185, 150))
        self.settings_list_layout.addWidget(self.exportCurveList)
        self.exportCurveList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # signal slots for checkboxes and lists
        self.exportMorphsCB.stateChanged.connect(partial(self._disable_widget, self.exportMorphList,
                                                         self.exportMorphsCB))
        self.exportCustomAttrsCB.stateChanged.connect(
            partial(self._disable_widget, self.exportCurveList, self.exportCustomAttrsCB))
        self.exportMorphsCB.stateChanged.connect(self.exportMeshCB.setChecked)
        self.exportMeshCB.stateChanged.connect(self.exportMorphsCB.setChecked)

        # horizontal layout for pre-script
        self.preScript_layout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.preScript_layout)

        # pre-script checkbox, lineEdit, and button
        self.preScriptCB = QtWidgets.QCheckBox("Pre-Script: ")
        self.preScript_layout.addWidget(self.preScriptCB)

        self.preScript_path = QtWidgets.QLineEdit()
        self.preScript_path.setObjectName("light")
        self.preScript_layout.addWidget(self.preScript_path)

        ps_browseBtn = QtWidgets.QPushButton()
        ps_browseBtn.setMinimumSize(30, 30)
        ps_browseBtn.setMaximumSize(30, 30)
        ps_browseBtn.setObjectName("load")
        ps_browseBtn.clicked.connect(partial(self._file_browse_script, self.preScript_path, self.preScriptCB))
        self.preScript_layout.addWidget(ps_browseBtn)

        # horizontal layout for post-script
        self.postScript_layout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.postScript_layout)

        # pre-script checkbox, lineEdit, and button
        self.postScriptCB = QtWidgets.QCheckBox("Post-Script: ")
        self.postScript_layout.addWidget(self.postScriptCB)

        self.postScript_path = QtWidgets.QLineEdit()
        self.postScript_path.setObjectName("light")
        self.postScript_layout.addWidget(self.postScript_path)

        pps_browseBtn = QtWidgets.QPushButton()
        pps_browseBtn.setMinimumSize(30, 30)
        pps_browseBtn.setMaximumSize(30, 30)
        pps_browseBtn.setObjectName("load")
        pps_browseBtn.clicked.connect(partial(self._file_browse_script, self.postScript_path, self.postScriptCB))
        self.postScript_layout.addWidget(pps_browseBtn)

        # save settings button
        button = QtWidgets.QPushButton("Save Export Settings")
        button.setMinimumHeight(30)
        button.setObjectName("settings")
        self.settingsLayout.addWidget(button)
        button.clicked.connect(self._fbx_save_export_data)

        # spacer
        self.settingsLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # =======================================================================
        # =======================================================================
        # =======================================================================
        # # FBX Sequences
        # =======================================================================
        # =======================================================================
        # =======================================================================

        # # Add Sequence
        self.addFbxAnimSequence = QtWidgets.QPushButton("Add Sequence")
        self.addFbxAnimSequence.setMinimumSize(QtCore.QSize(415, 50))
        self.addFbxAnimSequence.setMaximumSize(QtCore.QSize(415, 50))
        self.addFbxAnimSequence.setObjectName("settings")
        self.addFbxAnimSequence.clicked.connect(partial(self._fbx_add_sequence))
        self.sequenceTabLayout.addWidget(self.addFbxAnimSequence)

        # #Main Export Section
        self.fbxAnimSequenceFrame = QtWidgets.QFrame()
        self.fbxAnimSequenceFrame.setMinimumWidth(415)
        self.fbxAnimSequenceFrame.setMaximumWidth(415)
        scrollSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.fbxAnimSequenceFrame.setSizePolicy(scrollSizePolicy)

        self.fbxMainScroll = QtWidgets.QScrollArea()
        self.sequenceTabLayout.addWidget(self.fbxMainScroll)
        self.fbxMainScroll.setMinimumSize(QtCore.QSize(415, 280))
        self.fbxMainScroll.setMaximumSize(QtCore.QSize(415, 900))
        self.fbxMainScroll.setWidgetResizable(True)
        self.fbxMainScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.fbxMainScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fbxMainScroll.setWidget(self.fbxAnimSequenceFrame)

        self.fbxSequenceLayout = QtWidgets.QVBoxLayout(self.fbxAnimSequenceFrame)
        self.fbxSequenceLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # spacer
        self.sequenceTabLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # =======================================================================
        # #export button
        # =======================================================================
        export_layout = QtWidgets.QHBoxLayout()
        self.fbxTabLayout.addLayout(export_layout)

        save_button = QtWidgets.QPushButton()
        save_button.setMinimumSize(QtCore.QSize(30, 30))
        save_button.setMaximumSize(QtCore.QSize(30, 30))
        save_button.setObjectName("save")
        export_layout.addWidget(save_button)
        save_button.clicked.connect(self._save_data)

        self.doFbxExportBtn = QtWidgets.QPushButton("Export")
        export_layout.addWidget(self.doFbxExportBtn)
        self.doFbxExportBtn.setObjectName("settings")
        self.doFbxExportBtn.setMinimumSize(QtCore.QSize(385, 40))
        self.doFbxExportBtn.setMaximumSize(QtCore.QSize(385, 40))
        self.doFbxExportBtn.clicked.connect(self._fbx_export)

        # show window
        self.mainWin.show()
        self.fbxTabs.setCurrentIndex(1)

        # find morphs
        self._find_morphs()

        # find custom curves
        self._find_custom_curves()

        # populate UI
        self._fbx_populate_interface()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "ExportMotion")
        self.mainWin.restoreGeometry(settings.value("geometry"))

    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "ExportMotion")
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self.mainWin, event)

    def _fbx_check_export_mesh(self):

        if self.exportMorphsCB.isChecked():
            if not self.exportMeshCB.isChecked():
                self.exportMeshCB.setChecked(True)
                self.exportMeshCB.setEnabled(False)

        else:
            self.exportMeshCB.setEnabled(True)

    def _fbx_populate_interface(self, *args):

        # remove existing animation sequences
        widgetsToRemove = []

        for i in range(self.fbxSequenceLayout.count()):
            child = self.fbxSequenceLayout.itemAt(i)
            if child is not None:
                if type(child.widget()) == QtWidgets.QGroupBox:
                    widgetsToRemove.append(child.widget())

        for widget in widgetsToRemove:
            self._fbx_remove_anim_sequence(widget)

        # get characters in scene
        characters = []
        characterInfo = self._find_characters()
        for info in characterInfo:
            characters.append(info[0])

        # check character nodes for fbxAnimData
        for currentChar in characters:
            # loop through data, adding sequences and setting settings
            if cmds.objExists(currentChar + ":ART_RIG_ROOT.fbxAnimData"):
                fbxData = json.loads(cmds.getAttr(currentChar + ":ART_RIG_ROOT.fbxAnimData"))

                # each entry in the fbxData list is a sequence with all the needed information
                for data in fbxData:

                    # first, set export settings
                    self.exportMeshCB.setChecked(data[0])
                    self.exportMorphsCB.setChecked(data[1])
                    self.exportCustomAttrsCB.setChecked(data[2])

                    # select morphs and curves to export in the lists if they exist
                    for i in range(self.exportMorphList.count()):
                        bShape = self.exportMorphList.item(i)
                        text = bShape.text()
                        if text in data[3]:
                            bShape.setSelected(True)

                    for i in range(self.exportCurveList.count()):
                        cCurve = self.exportCurveList.item(i)
                        text = cCurve.text()
                        if text in data[4]:
                            cCurve.setSelected(True)

                    # set pre/post script info
                    self.preScriptCB.setChecked(data[5][0])
                    self.preScript_path.setText(data[5][1])

                    self.postScriptCB.setChecked(data[6][0])
                    self.postScript_path.setText(data[6][1])

                    # add anim sequence
                    self._fbx_add_sequence(data[7])

    def _fbx_add_sequence(self, data=None):

        # get number of children of fbxSequenceLayout
        children = self.fbxSequenceLayout.count()
        index = children - 1

        # contained groupBox for each sequence
        groupBox = QtWidgets.QGroupBox()
        groupBox.setCheckable(True)
        groupBox.setMaximumHeight(260)
        groupBox.setMaximumWidth(380)
        self.fbxSequenceLayout.insertWidget(index, groupBox)

        # set context menu policy on groupbox
        groupBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        groupBox.customContextMenuRequested.connect(partial(self._fbx_create_context_menu, groupBox))

        # add frame layout to groupbox
        frameLayout = QtWidgets.QVBoxLayout(groupBox)

        # add frame to groupbox
        frame = QtWidgets.QFrame()
        frame.setObjectName("light")
        frameLayout.addWidget(frame)

        vLayout = QtWidgets.QVBoxLayout(frame)
        vLayout.setObjectName("vLayout")

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(groupBox, QtCore.SIGNAL("toggled(bool)"), frame.setVisible)
        groupBox.setChecked(True)

        # =======================================================================
        # #portrait and character combo box
        # =======================================================================
        characterLayout = QtWidgets.QHBoxLayout()
        characterLayout.setObjectName("charLayout")
        vLayout.addLayout(characterLayout)

        portrait = QtWidgets.QLabel()
        portrait.setObjectName("charPortrait")
        portrait.setMinimumSize(QtCore.QSize(30, 30))
        portrait.setMaximumSize(QtCore.QSize(30, 30))
        characterLayout.addWidget(portrait)

        characterComboBox = QtWidgets.QComboBox()
        characterComboBox.setObjectName("charComboBox")
        characterComboBox.setMinimumHeight(30)
        characterComboBox.setMaximumHeight(30)
        characterLayout.addWidget(characterComboBox)

        # populate combo box
        characters = self._find_characters()
        for character in characters:
            characterName = character[0]
            characterComboBox.addItem(characterName)
        self._update_icon(characterComboBox, portrait, characters)
        characterComboBox.currentIndexChanged.connect(partial(self._update_icon, characterComboBox, portrait,
                                                              characters))

        # =======================================================================
        # #Checkbox, path, and browse button
        # =======================================================================
        pathLayout = QtWidgets.QHBoxLayout()
        pathLayout.setObjectName("pathLayout")
        vLayout.addLayout(pathLayout)

        checkBox = QtWidgets.QCheckBox()
        checkBox.setObjectName("exportCheckBox")
        checkBox.setChecked(True)
        pathLayout.addWidget(checkBox)

        pathField = QtWidgets.QLineEdit()
        pathField.setObjectName("exportPath")
        pathLayout.addWidget(pathField)
        pathField.setMinimumWidth(200)

        browseBtn = QtWidgets.QPushButton()
        browseBtn.setMinimumSize(30, 30)
        browseBtn.setMaximumSize(30, 30)
        pathLayout.addWidget(browseBtn)
        browseBtn.setObjectName("load")
        browseBtn.clicked.connect(partial(self._file_browse_export, pathField))

        # =======================================================================
        # #frame range, and frame rate
        # =======================================================================
        optionLayout = QtWidgets.QHBoxLayout()
        vLayout.addLayout(optionLayout)
        optionLayout.setObjectName("optionLayout")

        label1 = QtWidgets.QLabel("Start Frame: ")
        optionLayout.addWidget(label1)
        label1.setStyleSheet("background: transparent;")

        startFrame = QtWidgets.QSpinBox()
        startFrame.setObjectName("startFrame")
        optionLayout.addWidget(startFrame)
        startFrame.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        startFrame.setRange(-1000, 10000)

        label2 = QtWidgets.QLabel(" End Frame: ")
        optionLayout.addWidget(label2)
        label2.setStyleSheet("background: transparent;")
        label2.setAlignment(QtCore.Qt.AlignCenter)

        endFrame = QtWidgets.QSpinBox()
        endFrame.setObjectName("endFrame")
        optionLayout.addWidget(endFrame)
        endFrame.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        endFrame.setRange(-1000, 10000)

        # set frame range by default based on current timeline
        start = cmds.playbackOptions(q=True, ast=True)
        end = cmds.playbackOptions(q=True, aet=True)
        startFrame.setValue(start)
        endFrame.setValue(end)

        frameRate = QtWidgets.QComboBox()
        frameRate.setObjectName("frameRate")
        optionLayout.addWidget(frameRate)
        frameRate.hide()

        # add items to frame rate
        frameRate.addItem("ntsc")
        frameRate.addItem("ntscf")
        frameRate.addItem("film")

        # set the FPS to the current scene setting
        fps = cmds.currentUnit(q=True, time=True)
        if fps == "film":
            frameRate.setCurrentIndex(2)
        if fps == "ntsc":
            frameRate.setCurrentIndex(0)
        if fps == "ntscf":
            frameRate.setCurrentIndex(1)

        # =======================================================================
        # #advanced options
        # =======================================================================
        advancedGroup = QtWidgets.QGroupBox("Advanced Settings")
        vLayout.addWidget(advancedGroup)
        advancedGroup.setCheckable(True)

        advancedLayout = QtWidgets.QVBoxLayout(advancedGroup)
        advancedFrame = QtWidgets.QFrame()
        advancedFrame.setObjectName("light")
        advancedLayout.addWidget(advancedFrame)
        advancedFrameLayout = QtWidgets.QVBoxLayout(advancedFrame)

        # =======================================================================
        # #rotation interpolation
        # =======================================================================
        interpLayout = QtWidgets.QHBoxLayout()
        advancedFrameLayout.addLayout(interpLayout)

        label3 = QtWidgets.QLabel("Rotation Interpolation: ")
        interpLayout.addWidget(label3)
        label3.setStyleSheet("background: transparent;")

        interpCombo = QtWidgets.QComboBox()
        interpLayout.addWidget(interpCombo)
        interpCombo.setObjectName("rotInterp")
        interpCombo.setMinimumWidth(150)

        interpCombo.addItem("Quaternion Slerp")
        interpCombo.addItem("Independent Euler-Angle")

        # =======================================================================
        # #sample rate and root options
        # =======================================================================
        rateRootLayout = QtWidgets.QHBoxLayout()
        advancedFrameLayout.addLayout(rateRootLayout)

        label4 = QtWidgets.QLabel("Sample Rate: ")
        rateRootLayout.addWidget(label4)

        sampleRate = QtWidgets.QDoubleSpinBox()
        sampleRate.setObjectName("sampleRate")
        rateRootLayout.addWidget(sampleRate)
        sampleRate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        sampleRate.setRange(0, 1)
        sampleRate.setSingleStep(0.1)
        sampleRate.setValue(1.00)

        rootComboBox = QtWidgets.QComboBox()
        rootComboBox.setObjectName("rootExportOptions")
        rootComboBox.addItem("Export Root Animation")
        rootComboBox.addItem("Zero Root")
        rootComboBox.addItem("Zero Root, Keep World Space")
        rateRootLayout.addWidget(rootComboBox)

        # signal slot for groupbox checkbox
        QtCore.QObject.connect(advancedGroup, QtCore.SIGNAL("toggled(bool)"), advancedFrame.setVisible)
        advancedGroup.setChecked(False)

        # signal slot for groupbox title
        characterComboBox.currentIndexChanged.connect(partial(self._fbx_update_title, groupBox))
        pathField.textChanged.connect(partial(self._fbx_update_title, groupBox))
        startFrame.valueChanged.connect(partial(self._fbx_update_title, groupBox))
        endFrame.valueChanged.connect(partial(self._fbx_update_title, groupBox))
        checkBox.stateChanged.connect(partial(self._fbx_update_title, groupBox))

        # create groupbox title
        self._fbx_update_title(groupBox)

        # set data if coming from duplicate call
        if data:

            # set character combo box
            for i in range(characterComboBox.count()):
                text = characterComboBox.itemText(i)
                if text == data[0]:
                    characterComboBox.setCurrentIndex(i)

            # set export checkbox
            checkBox.setChecked(data[1])

            # set export path
            pathField.setText(data[2])

            # set start frame
            startFrame.setValue(data[3])

            # set end frame
            endFrame.setValue(data[4])

            # set FPS
            for i in range(frameRate.count()):
                text = frameRate.itemText(i)
                if text == data[5]:
                    frameRate.setCurrentIndex(i)

            # set rotation interpolation
            for i in range(interpCombo.count()):
                text = interpCombo.itemText(i)
                if text == data[6]:
                    interpCombo.setCurrentIndex(i)

            # set sample rate
            sampleRate.setValue(data[7])

            # set root export
            for i in range(rootComboBox.count()):
                text = rootComboBox.itemText(i)
                if text == data[8]:
                    rootComboBox.setCurrentIndex(i)

    def _fbx_create_context_menu(self, widget, point):

        # icons
        icon_delete = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/delete.png"))
        icon_duplicate = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/duplicate.png"))
        icon_collapse = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/upArrow.png"))
        icon_expand = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/downArrow.png"))

        # create the context menu
        contextMenu = QtWidgets.QMenu()
        contextMenu.addAction(icon_delete, "Remove Sequence", partial(self._fbx_remove_anim_sequence, widget))
        contextMenu.addAction(icon_duplicate, "Duplicate Sequence", partial(self._fbx_duplicate_sequence, widget))
        contextMenu.addAction(icon_expand, "Expand All Sequences", partial(self._fbx_expand_all_sequences, True))
        contextMenu.addAction(icon_collapse, "Collapse All Sequences", partial(self._fbx_expand_all_sequences, False))
        contextMenu.exec_(widget.mapToGlobal(point))

    def _fbx_remove_anim_sequence(self, widget):

        widget.setParent(None)
        widget.close()
        self._fbx_save_export_data()

    def _fbx_duplicate_sequence(self, widget):

        sequenceData = self._fbx_get_sequence_info(widget)
        self._fbx_add_sequence(sequenceData)

    def _file_browse_export(self, widget):

        starting_directory = self.projectPath

        current_path = widget.text()
        if os.path.exists(os.path.dirname(current_path)):
            starting_directory = os.path.dirname(current_path)
        else:
            scene_path = cmds.file(q=True, sceneName=True)
            if os.path.exists(os.path.dirname(scene_path)):
                starting_directory = scene_path
        try:
            path = cmds.fileDialog2(fm=0, okc="Export", dir=starting_directory, ff="*.fbx")
            nicePath = utils.returnFriendlyPath(path[0])
            widget.setText(nicePath)
        except StandardError:
            pass

    def _file_browse_script(self, widget, checkbox=None):

        try:
            path = cmds.fileDialog2(fm=1, okc="Accept", dir=self.projectPath, ff="*.py;;*.mel")
            nicePath = utils.returnFriendlyPath(path[0])
            widget.setText(nicePath)

            if checkbox is not None:
                checkbox.setChecked(True)
        except StandardError:
            pass

    def _fbx_export(self):
        # This is temporary until I re-write the actual exporter to use a factory design and fix some of the issues.

        Export_FBX()

    def _fbx_export_old(self):
        # currently unused until I get the batcher factory built.

        # get up axis
        upAxis = cmds.upAxis(q=True, ax=True)

        # find mayapy interpreter location
        mayapy = utils.getMayaPyLoc()

        # message box for confirming save action
        export = True

        currentFile = cmds.file(q=True, sceneName=True)
        if cmds.file(currentFile, q=True, modified=True) is True:
            export = False

            msgBax = QtWidgets.QMessageBox()
            msgBax.setText("There are unsaved changes in this file. Those changes will not be exported.")
            msgBax.setIcon(QtWidgets.QMessageBox.Warning)
            msgBax.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Ignore
                                      | QtWidgets.QMessageBox.Abort)
            msgBax.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBax.exec_()

            if ret == QtWidgets.QMessageBox.Save:
                if currentFile == "":

                    msgBax = QtWidgets.QMessageBox()
                    msgBax.setText("File has no name. Please save the file manually to enter a name.")
                    msgBax.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBax.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgBax.setDefaultButton(QtWidgets.QMessageBox.Ok)
                    ret = msgBax.exec_()

                    if ret == QtWidgets.QMessageBox.Ok:
                        return

                else:
                    cmds.file(save=True, force=True)
                    export = True

            if ret == QtWidgets.QMessageBox.Ignore:
                export = True

        if export is True:

            # save settings
            characterData = self._fbx_save_export_data()

            # save copy of scene to temp location
            sourceFile = cmds.file(q=True, sceneName=True)
            filePath = os.path.dirname(sourceFile)
            tempFile = os.path.join(filePath, "export_TEMP.ma")

            cmds.file(rename=tempFile)
            cmds.file(save=True, type="mayaAscii", force=True)

            # pass tempFile and characterData to mayapy instance for processing
            if os.path.exists(mayapy):
                script_path = os.path.join(self.toolsPath, "Core\Scripts\Utilities\ART_FbxExport.py")
                script = utils.returnFriendlyPath(script_path)

                # create a temp file with the json data
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    json.dump(characterData, temp)
                    temp.close()

                # create a log file
                stdoutFile = os.path.join(filePath, "export_log.txt")
                out = file(stdoutFile, 'w')

                # open mayapy, passing in export file and character data
                subprocess.Popen(mayapy + ' ' + "\"" + script + "\"" + ' ' + "\"" + tempFile + "\"" + ' ' +
                                 "\"" + temp.name + "\"" + ' ' + "\"" + upAxis + "\"", stdout=out, stderr=out)

                # close the output file (for logging)
                out.close()

            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("mayapy executable not found. Currently not implemented for mac and linux.")
                msgBox.setIcon(QtWidgets.QMessageBox.Error)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msgBox.exec_()

            # reopen the original file
            cmds.file(sourceFile, open=True, force=True)

            # report back
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Export Complete")
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()

    def _find_morphs(self):

        # clear list
        self.exportMorphList.clear()
        characterMeshes = []

        # get all characters
        characters = self._find_characters()

        for character in characters:
            currentCharacter = character[0]

            # get meshes off of character node
            if cmds.objExists(currentCharacter + ":ART_RIG_ROOT"):
                if cmds.objExists(currentCharacter + ":ART_RIG_ROOT.LOD_0_Meshes"):
                    characterMeshes = cmds.listConnections(currentCharacter + ":ART_RIG_ROOT.LOD_0_Meshes")

            # get skinClusters in scene and query their connections
            skins = cmds.ls(type="skinCluster")

            for skin in skins:
                shapeInfo = cmds.listConnections(skin, c=True, type="blendShape", et=True)
                mesh = cmds.listConnections(skin, type="mesh")

                if characterMeshes:
                    if mesh is not None:
                        # confirm that the blendshape found belongs to one of our character meshes. Then add to list
                        if mesh[0] in characterMeshes:
                            if shapeInfo is not None:
                                for info in shapeInfo:
                                    if cmds.nodeType(info) == "blendShape":
                                        item = QtWidgets.QListWidgetItem(info)
                                        self.exportMorphList.addItem(item)
                                        item.setSelected(False)

    def _find_custom_curves(self):

        # get all characters
        characters = self._find_characters()

        for character in characters:
            currentCharacter = character[0]
            rootBone = currentCharacter + ":root"
            attrs = cmds.listAttr(rootBone, keyable=True)

            standardAttrs = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ",
                             "scaleX", "scaleY", "scaleZ", "visibility"]

            for attr in attrs:
                if attr not in standardAttrs:
                    item = QtWidgets.QListWidgetItem(currentCharacter + ":" + attr)
                    self.exportCurveList.addItem(item)
                    item.setSelected(False)

    def _find_characters(self):

        characterInfo = []

        allNodes = cmds.ls(type="network")
        characterNodes = []
        for node in allNodes:
            attrs = cmds.listAttr(node)
            if "rigModules" in attrs:
                characterNodes.append(node)

        # go through each node, find the character name, the namespace on the node, and the picker attribute
        for node in characterNodes:
            try:
                namespace = cmds.getAttr(node + ".namespace")
            except StandardError:
                namespace = cmds.getAttr(node + ".name")

            # add the icon found on the node's icon path attribute to the tab
            iconPath = cmds.getAttr(node + ".iconPath")
            iconPath = utils.returnNicePath(self.projectPath, iconPath)

            characterInfo.append([namespace, iconPath])

        return characterInfo

    def _update_icon(self, comboBox, label, characterInfo, *args):

        print args
        # get current selection of combo box
        characterName = comboBox.currentText()

        # loop through characterInfo, find matching characterName, and get icon path
        for each in characterInfo:
            if characterName == each[0]:
                iconPath = each[1]
                img = QtGui.QImage(iconPath)
                pixmap = QtGui.QPixmap(img.scaledToWidth(30))
                label.setPixmap(pixmap)
                label.show()

    def _window_resized(self, event):

        currentSize = self.mainWin.size()
        height = currentSize.height()

        self.fbxTabLayoutFrame.resize(450, height - 50)

        width = self.fbxTabs.size()
        width = width.width()
        self.fbxTabs.resize(width, height - 50)
        self.fbxMainScroll.setMinimumSize(415, height - 220)
        event.accept()

    def _disable_widget(self, widget, checkbox):

        state = checkbox.isChecked()
        if state:
            widget.setEnabled(True)
            for i in range(widget.count()):
                item = widget.item(i)
                item.setHidden(False)
        else:
            widget.setEnabled(False)
            for i in range(widget.count()):
                item = widget.item(i)
                item.setHidden(True)

    def _fbx_update_title(self, groupBox, *args):

        print args
        # get info from interface
        data = []
        children = groupBox.children()
        for each in children:
            if type(each) == QtWidgets.QFrame:
                contents = each.children()

                for child in contents:
                    objectName = child.objectName()

                    if objectName == "charComboBox":
                        char = child.currentText()
                        data.append(char)

                    if objectName == "exportCheckBox":
                        value = child.isChecked()
                        data.append(value)

                    if objectName == "exportPath":
                        path = child.text()
                        filename = os.path.basename(path)
                        data.append(filename.partition(".")[0])

                    if objectName == "startFrame":
                        startFrame = child.value()
                        data.append(startFrame)

                    if objectName == "endFrame":
                        endFrame = child.value()
                        data.append(endFrame)

        titleString = ""
        if data[1]:
            titleString += data[0] + ", "
            titleString += data[2] + ", "
            titleString += "["
            titleString += str(data[3]) + ": "
            titleString += str(data[4]) + "]"
        else:
            titleString += "Not Exporting.."
        groupBox.setTitle(titleString)

    def _save_data(self):

        # save export data
        self._fbx_save_export_data()

        # try to save scene
        try:
            cmds.file(save=True, force=True)
            status = "Settings and file saved successfully."
        except StandardError, e:
            status = str(e)

        # report back
        try:
            cmds.inViewMessage(amg=' <hl>' + status + '.</hl>', pos='topCenter', fade=True)
        except StandardError:
            print status

    def _fbx_save_export_data(self):

        exportData = []

        # get main export settings
        exportMesh = self.exportMeshCB.isChecked()
        exportMorph = self.exportMorphsCB.isChecked()
        exportCurve = self.exportCustomAttrsCB.isChecked()

        exportData.append(exportMesh)
        exportData.append(exportMorph)
        exportData.append(exportCurve)

        # get selected morphs
        morphs = []
        for i in range(self.exportMorphList.count()):
            item = self.exportMorphList.item(i)
            if item.isSelected():
                morphs.append(item.text())

        # get selected curves
        curves = []
        for i in range(self.exportCurveList.count()):
            item = self.exportCurveList.item(i)
            if item.isSelected():
                curves.append(item.text())

        # pre and post script
        preScript = self.preScriptCB.isChecked()
        preScript_path = self.preScript_path.text()

        postScript = self.postScriptCB.isChecked()
        postScript_path = self.postScript_path.text()

        exportData.append(morphs)
        exportData.append(curves)
        exportData.append([preScript, preScript_path])
        exportData.append([postScript, postScript_path])

        # get fbx sequences and settings
        characterData = {}
        for i in range(self.fbxSequenceLayout.count()):
            child = self.fbxSequenceLayout.itemAt(i)
            if type(child.widget()) == QtWidgets.QGroupBox:
                data = []
                sequenceData = self._fbx_get_sequence_info(child.widget())
                data.extend(exportData)
                data.append(sequenceData)

                if sequenceData[0] not in characterData:
                    characterData[sequenceData[0]] = [data]
                else:
                    currentData = characterData.get(sequenceData[0])
                    currentData.append(data)
                    characterData[sequenceData[0]] = currentData

        # loop through each key (character) in the dictionary, and write its data to the network node
        for each in characterData:
            data = characterData.get(each)

            # Add that data to the character node
            networkNode = each + ":ART_RIG_ROOT"
            if not cmds.objExists(networkNode + ".fbxAnimData"):
                cmds.addAttr(networkNode, ln="fbxAnimData", dt="string")

            cmds.setAttr(networkNode + ".fbxAnimData", json.dumps(data), type="string")

        return characterData

    def _fbx_get_sequence_info(self, groupBox):

        # get info from interface
        data = []

        children = groupBox.children()
        for each in children:
            if type(each) == QtWidgets.QFrame:
                contents = each.children()

                for child in contents:
                    objectName = child.objectName()

                    if objectName == "charComboBox":
                        char = child.currentText()
                        data.append(char)

                    if objectName == "exportCheckBox":
                        value = child.isChecked()
                        data.append(value)

                    if objectName == "exportPath":
                        path = child.text()
                        data.append(path)

                    if objectName == "startFrame":
                        startFrame = child.value()
                        data.append(startFrame)

                    if objectName == "endFrame":
                        endFrame = child.value()
                        data.append(endFrame)

                    if objectName == "frameRate":
                        fps = child.currentText()
                        data.append(fps)

                    if type(child) == QtWidgets.QGroupBox:
                        subChildren = child.children()

                        for sub in subChildren:
                            if type(sub) == QtWidgets.QFrame:
                                advancedChildren = sub.children()
                                for advancedChild in advancedChildren:
                                    advancedObj = advancedChild.objectName()

                                    if advancedObj == "sampleRate":
                                        rate = advancedChild.value()
                                        data.append(rate)

                                    if advancedObj == "rotInterp":
                                        interp = advancedChild.currentText()
                                        data.append(interp)

                                    if advancedObj == "rootExportOptions":
                                        root = advancedChild.currentText()
                                        data.append(root)

        return data

    def _fbx_expand_all_sequences(self, state):

        # get info from interface
        for i in range(self.fbxSequenceLayout.count()):
            child = self.fbxSequenceLayout.itemAt(i)
            if type(child.widget()) == QtWidgets.QGroupBox:
                child.widget().setChecked(state)
