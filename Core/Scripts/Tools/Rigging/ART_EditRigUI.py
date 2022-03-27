# coding=utf-8
"""
Author: Jeremy Ernst
"""

import json
import os
from functools import partial

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatibility
try:
    import shiboken as shiboken
except ImportError:
    import shiboken2 as shiboken


# noinspection PyArgumentList
def getMainWindow():
    """
    Get Maya’s window as a QWidget and return the item in memory.
    :return: a QWidget of Maya’s window
    """

    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


windowTitle = "Edit Rig"
windowObject = "pyArtEditRigWin"

# noinspection SpellCheckingInspection
kneeTwistScript = """
class artv2_kneeTwist():
    def __init__(self):
        self.kneeVal = 0
        self.previousTool = None
        self.footControl = None
        self.side = "Left"

        cmds.scriptJob(event=['idle', self.kneeTwistCheck], kws=True)
        if not cmds.draggerContext('kneeTwistCtx', q=True, exists=True):
            cmds.draggerContext('kneeTwistCtx', pc = self.kneeTwistPress, dc = self.kneeTwistDrag, undoMode="sequence")

    def kneeTwistPress(self):
        self.getCharacters()
        if self.footControl is not None:
            self.kneeVal = cmds.getAttr(self.footControl + '.knee_twist')

    def kneeTwistDrag(self):
        anchorPoint = cmds.draggerContext('kneeTwistCtx', query=True, anchorPoint=True)
        dragPosition = cmds.draggerContext('kneeTwistCtx', query=True, dragPoint=True)
        button = cmds.draggerContext('kneeTwistCtx', query=True, button=True)
        mult = 0.1
        if button == 2:
            sliderMultiplier = 0.1
        if self.side == "Left":
            cmds.setAttr(self.footControl + '.knee_twist', self.kneeVal + ((dragPosition[0] - anchorPoint[0]) * mult))
        if self.side == "Right":
            cmds.setAttr(self.footControl + '.knee_twist', self.kneeVal + ((anchorPoint[0] - dragPosition[0]) * mult))
        cmds.refresh()

    def getCharacters(self):
        nodes = cmds.ls(type='network')
        controls = []
        selection = cmds.ls(sl = True)

        for node in nodes:
            attrs = cmds.listAttr(node, ud=True)
            if attrs is not None:
                if "rigModules" in attrs:
                    rigModules = cmds.listConnections(node + ".rigModules")
                    for module in rigModules:
                        if cmds.getAttr(module + ".moduleType") == "ART_Leg_Standard":

                            controlNode = cmds.listConnections(module + ".controls")[0]
                            ikControls = cmds.listConnections(controlNode + ".ikV1Controls")
                            ikControls = sorted(ikControls)

                            for each in ikControls:
                                if each in selection:
                                    self.footControl = ikControls[0]
                                    self.side = cmds.getAttr(module + ".side")
                                    controls = ikControls
                                    return controls



    def kneeTwistCheck(self):
        mods = cmds.getModifiers()
        ctrl = (mods & 4) > 0
        if ctrl is False:
            if cmds.currentCtx() == 'kneeTwistCtx':
                try:
                    cmds.setToolTo(self.previousTool)
                except:
                    cmds.setToolTo('moveSuperContext')
        else:
            controls = self.getCharacters()
            selection = cmds.ls(sl = True)
            if len(selection) > 0:
                if controls is not None:
                    if selection[0] in controls:
                        currentContext = cmds.currentCtx()
                        if currentContext != 'kneeTwistCtx':
                            self.previousTool = currentContext
                        cmds.setToolTo('kneeTwistCtx')

artv2_kneeTwist()
"""


# noinspection SpellCheckingInspection
class ARTv2_Add_Rig(object):
    """
    Class for adding an ARTv2 rig and handling namespace assignment as well as creating default spaces and script nodes.
    """

    def __init__(self, file_path, character, launch_ui=True):
        self.file_path = file_path
        self.character = character
        self.launch_ui = launch_ui

        self._add_rig()

    # noinspection SpellCheckingInspection
    def _add_rig(self):

        if os.path.exists(self.file_path):
            namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

            # reference the rig file
            cmds.file(self.file_path, r=True, type="mayaAscii", loadReferenceDepth="all", namespace=self.character,
                      options="v=0")

            # find new namespaces in scene to figure out the namespace that was created upon referencing the
            # character
            newNamespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
            for name in newNamespaces:
                if name not in namespaces:
                    self.character = name

            # add an attr to the rig root (if needed) and set the namespace attr to the newCharacterName
            if cmds.objExists(self.character + ":ART_RIG_ROOT"):
                if not cmds.objExists(self.character + ":ART_RIG_ROOT.namespace"):
                    cmds.addAttr(self.character + ":ART_RIG_ROOT", ln="namespace", dt="string",
                                 keyable=False)
                cmds.setAttr(self.character + ":ART_RIG_ROOT.namespace", self.character, type="string")

            # create ik knee twist manip script node
            self._knee_twist_manip()

        # clear selection and fit view
        cmds.select(clear=True)
        cmds.viewFit()
        panels = cmds.getPanel(type='modelPanel')

        # turn on smooth shading
        for panel in panels:
            editor = cmds.modelPanel(panel, q=True, modelEditor=True)
            cmds.modelEditor(editor, edit=True, displayAppearance="smoothShaded", displayTextures=True,
                             textures=True)

        if self.launch_ui:
            self._launch_ui()

    def _launch_ui(self):
        # launch anim UI
        cmds.refresh(force=True)

        import Tools.Animation.ART_AnimationUI as ART_AnimationUI
        ART_AnimationUI.run()

    def _knee_twist_manip(self):
        nodes = cmds.ls(type='network')
        for node in nodes:
            attrs = cmds.listAttr(node, ud=True)
            if attrs is not None:
                if "rigModules" in attrs:
                    rigModules = cmds.listConnections(node + ".rigModules")
                    for module in rigModules:
                        if cmds.getAttr(module + ".moduleType") == "ART_Leg_Standard":

                            if not cmds.objExists("artv2_kneeTwistScript"):
                                # create the script node
                                cmds.scriptNode(st=2, bs=kneeTwistScript, n='artv2_kneeTwistScript', stp='python')

                                # eval the script right away, as the script node won't execute until file load.
                                exec kneeTwistScript


class ARTv2_Edit_Rig(object):
    """ Class for editing a rig by opening the file and launching the rig creator tools."""

    def __init__(self, file_path):

        self.file_path = file_path

        self._edit_rig()

    def _edit_rig(self):
        if os.path.exists(self.file_path):
            launchUI = False

            # get current file
            currentFile = cmds.file(q=True, sceneName=True)
            if cmds.file(currentFile, q=True, modified=True) is True:
                proceed = self._unsaved_changes()

                if proceed == 0:
                    cmds.file(save=True, force=True)
                    cmds.file(self.file_path, open=True, prompt=True, options="v=0", ignoreVersion=True,
                              typ="mayaAscii", f=True)
                    launchUI = True

                if proceed == 1:
                    cmds.file(self.file_path, open=True, prompt=True, options="v=0", ignoreVersion=True,
                              typ="mayaAscii", f=True)
                    launchUI = True

                if proceed == 2:
                    return
            else:
                cmds.file(self.file_path, open=True, prompt=True, options="v=0", ignoreVersion=True,
                          typ="mayaAscii", f=True)
                launchUI = True

            if launchUI:
                import Tools.Rigging.ART_RigCreatorUI as ART_RigCreatorUI
                ART_RigCreatorUI.createUI()

    def _unsaved_changes(self):

        # message box for letting user know current file has unsaved changes
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Current File Has Unsaved Changes!")
        msgBox.addButton("Save Changes", QtWidgets.QMessageBox.YesRole)
        msgBox.addButton("Don't Save", QtWidgets.QMessageBox.NoRole)
        msgBox.addButton("Cancel", QtWidgets.QMessageBox.NoRole)
        ret = msgBox.exec_()

        return ret


# noinspection PyUnusedLocal
class ART_EditRigUI(QtWidgets.QMainWindow):
    """
    This class builds a tool that allows a user to Edit a Rig or Add Character for Animation. Both functions use the
    same interface. The title and button text get swapped out depending on which situation has been called for by
    the A.R.T.2.0 menu.

        .. image:: /images/editRig.png

    """

    def __init__(self, edit, add, parent=None):
        """
        Instantiates the class, getting the QSettings and building the interface.

        :param edit: Whether or not the operation is to edit the rig.
        :param add: Whether or not the operation is to add the character for animation.

        """

        super(ART_EditRigUI, self).__init__(parent)
        self.edit = edit
        self.add = add
        self.items = []

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        # build the UI
        self._create_interface()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_interface(self):
        """
        Builds the UI, listing options for choosing a project and showing all assets belonging to that project for
        edit or add.

        """

        # fonts
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        fontSmall = QtGui.QFont()
        fontSmall.setPointSize(9)
        fontSmall.setBold(True)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # =======================================================================
        # #create the main widget
        # =======================================================================
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName(windowObject)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        if self.edit:
            self.setWindowTitle(windowTitle)
        if self.add:
            self.setWindowTitle("Add Rig For Animation")

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.resize(494, 381)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(494, 381))
        self.setMaximumSize(QtCore.QSize(494, 381))

        # create the QFrame
        self.frame = QtWidgets.QFrame()
        self.layout.addWidget(self.frame)
        self.widgetLayout = QtWidgets.QHBoxLayout(self.frame)

        # =======================================================================
        # #create two VBox Layouts to create 2 columns
        # =======================================================================
        self.leftColumn = QtWidgets.QVBoxLayout()
        self.widgetLayout.addLayout(self.leftColumn)

        self.rightColumn = QtWidgets.QVBoxLayout()
        self.widgetLayout.addLayout(self.rightColumn)

        # =======================================================================
        # #left column : project comboBox, group comboBox, listWidget of characters
        # =======================================================================

        self.tree_search = QtWidgets.QLineEdit()
        self.tree_search.setObjectName("light")
        self.tree_search.setPlaceholderText("Search...")
        self.tree_search.textChanged.connect(self._search)
        self.leftColumn.addWidget(self.tree_search)

        self.directory_tree = QtWidgets.QTreeWidget()
        self.directory_tree.setMinimumSize(QtCore.QSize(250, 290))
        self.directory_tree.setMaximumSize(QtCore.QSize(250, 290))

        self.header_text = os.path.basename(self.projectPath)
        header = QtWidgets.QTreeWidgetItem([self.header_text + ":"])
        
        self.directory_tree.setHeaderItem(header)
        self.leftColumn.addWidget(self.directory_tree)
        self.directory_tree.setColumnWidth(0, 250)
        self.directory_tree.itemSelectionChanged.connect(self._populate_icon)

        self._populate_tree()
        self.word_list = self._get_items()
        completer = QtWidgets.QCompleter(self.word_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.tree_search.setCompleter(completer)

        # =======================================================================
        # #right column: icon frame, edit button/add button, close button
        # =======================================================================

        self.characterIcon = QtWidgets.QLabel()
        self.characterIcon.setMinimumSize(200, 200)
        self.characterIcon.setMaximumSize(200, 200)
        self.rightColumn.addWidget(self.characterIcon)

        # default image
        self.defaultPixMap = QtGui.QPixmap(utils.returnNicePath(self.iconsPath, "System/noCharacter.png"))
        self.characterIcon.setPixmap(self.defaultPixMap)

        # if edit:
        if self.edit:
            self.editButton = QtWidgets.QPushButton("Edit Selected")
            self.editButton.setFont(font)
            self.rightColumn.addWidget(self.editButton)
            self.editButton.setMinimumSize(200, 40)
            self.editButton.setMaximumSize(200, 40)
            self.editButton.clicked.connect(partial(self._edit_selected))
            self.editButton.setObjectName("settings")
            text = "Opens the rig file for edit. Use this if you want to polish skin-weights, adjust module" \
                   " settings or placement, modify rig defaults, or manually add custom rigging to the file."
            self.editButton.setToolTip(text)

        # if add:
        if self.add:
            self.addButton = QtWidgets.QPushButton("Add Selected")
            self.addButton.setFont(font)
            self.rightColumn.addWidget(self.addButton)
            self.addButton.setMinimumSize(200, 40)
            self.addButton.setMaximumSize(200, 40)
            self.addButton.clicked.connect(partial(self._add_selected_character))
            self.addButton.setObjectName("settings")

        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.setFont(font)
        self.rightColumn.addWidget(self.closeButton)
        self.closeButton.setMinimumSize(200, 40)
        self.closeButton.setMaximumSize(200, 40)
        self.closeButton.clicked.connect(partial(self._close_ui))
        self.closeButton.setObjectName("settings")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_tree(self):
        """
        Find all projects on disk (using the project path setting) and add each project to the tree widget with the
        sub-folders of that project.
        """

        # if the project path doesn't exist on disk, create it
        if not os.path.exists(self.projectPath):
            os.makedirs(self.projectPath)

        # get a list of the existing folders in projects
        existingProjects = os.listdir(self.projectPath)
        folders = []

        # find out which returned items are directories
        for each in existingProjects:
            if os.path.isdir(os.path.join(self.projectPath, each)):
                folders.append(each)

        items = []
        self._populate_project_tree(self.projectPath, items)

        for each in items:
            file_name = os.path.splitext(each[1])[0]
            file_item = QtWidgets.QTreeWidgetItem(each[2], [file_name])
            file_item.setData(0, QtCore.Qt.UserRole, ["file", each[0]])
            icon_path = utils.returnNicePath(self.iconsPath, 'System/file.png')
            file_item.setIcon(0, QtGui.QIcon(icon_path))

        self.directory_tree.resizeColumnToContents(0)
        self._validate_tree_items()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_project_tree(self, directory, item_list, parent_item=None):

        # creating some lists for filtering folders and files
        banned = [".mayaSwatches"]
        file_filters = [".png"]

        # get items in passed in directory
        sub_items = os.listdir(directory)
        for each in sub_items:

            # if the item is a directory (not a file), check for children
            if os.path.isdir(os.path.join(directory, each)):
                if not parent_item:
                    if each not in banned:
                        folder_item = QtWidgets.QTreeWidgetItem(self.directory_tree, [each])
                        folder_item.setData(0, QtCore.Qt.UserRole, ["folder", os.path.join(directory, each)])
                        icon_path = utils.returnNicePath(self.iconsPath, 'System/folder.png')
                        folder_item.setIcon(0, QtGui.QIcon(icon_path))
                        self._populate_project_tree(os.path.join(directory, each), item_list, folder_item)
                else:
                    if each not in banned:
                        folder_item = QtWidgets.QTreeWidgetItem(parent_item, [each])
                        folder_item.setData(0, QtCore.Qt.UserRole, ["folder", os.path.join(directory, each)])
                        icon_path = utils.returnNicePath(self.iconsPath, 'System/folder.png')
                        folder_item.setIcon(0, QtGui.QIcon(icon_path))

                        self._populate_project_tree(os.path.join(directory, each), item_list, folder_item)

            # if the item is a file, add the item to the tree widget
            if os.path.isfile(os.path.join(directory, each)):
                if not os.path.splitext(each)[1] in file_filters:
                    item_list.append([os.path.join(directory, each), each, parent_item])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _validate_tree_items(self):

        iterator = QtWidgets.QTreeWidgetItemIterator(self.directory_tree)
        while iterator.value():
            item = iterator.value()
            item.setHidden(True)
            item_data = item.data(0, QtCore.Qt.UserRole)
            item_ext = os.path.splitext(item_data[1])

            if item_ext[1] == ".ma":
                if os.path.exists(item_data[1].replace(".ma", ".png")):
                    item.setHidden(False)
                    self.items.append(item)

                    nice_path = utils.returnFriendlyPath(item_data[1])
                    parents = nice_path.split("/")
                    for parent in parents:
                        items = self.directory_tree.findItems(parent, QtCore.Qt.MatchRecursive)
                        for item in items:
                            item.setHidden(False)

            iterator += 1

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_items(self):

        items = []
        for each in self.items:
            items.append(each.text(0))
        return items

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # noinspection PyUnusedLocal
    def _populate_icon(self, *args):

        # default
        self.characterIcon.setPixmap(self.defaultPixMap)

        # get selected item in tree
        selectedItem = self.directory_tree.selectedItems()
        if len(selectedItem) > 0:
            selectedItem = selectedItem[0]
            item_data = selectedItem.data(0, QtCore.Qt.UserRole)
            if item_data[0] == "file":
                icon_path = item_data[1].replace(".ma", ".png")

                if os.path.exists(icon_path):
                    pixmap = QtGui.QPixmap(icon_path)
                    self.characterIcon.setPixmap(pixmap)

                else:
                    self.characterIcon.setPixmap(self.defaultPixMap)

            else:
                self.characterIcon.setPixmap(self.defaultPixMap)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _edit_selected(self, *args):
        """
        Find the selected character in the tree widget, and open that file for edit.
        """

        # get selected item in tree
        selected = self.directory_tree.selectedItems()
        if len(selected) > 0:
            item_data = selected[0].data(0, QtCore.Qt.UserRole)
            if item_data[0] == "file":
                mayaFile = item_data[1]

                ARTv2_Edit_Rig(mayaFile)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _add_selected_character(self, *args):

        # get selected item in tree
        selected = self.directory_tree.selectedItems()
        if len(selected) > 0:
            item_data = selected[0].data(0, QtCore.Qt.UserRole)
            if item_data[0] == "file":
                mayaFile = item_data[1]
                selectedCharacter = selected[0].text(0)

                ARTv2_Add_Rig(mayaFile, selectedCharacter)

                # delete any interfaces that may be up
                self._close_ui()

                if cmds.dockControl("pyArtRigCreatorDock", q=True, exists=True):
                    if cmds.window("pyArtRigCreatorUi", exists=True):
                        cmds.deleteUI("pyArtRigCreatorUi", wnd=True)
                    cmds.deleteUI("pyArtRigCreatorDock", control=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _search(self):

        for item in self.items:
            item.setSelected(False)
        text = self.tree_search.text()

        if text in self.word_list:
            index = self.word_list.index(text)
            item = self.items[index]
            item.setSelected(True)
            self.directory_tree.scrollToItem(item)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _close_ui(self):

        if cmds.window("pyArtEditRigWin", exists=True):
            cmds.deleteUI("pyArtEditRigWin", wnd=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """Creates an instance of the class for Editing a rig. The ARTv2 menu calls on this function."""

    if cmds.window("pyArtEditRigWin", exists=True):
        cmds.deleteUI("pyArtEditRigWin", wnd=True)

    gui = ART_EditRigUI(True, False, getMainWindow())
    gui.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def runAdd():
    """Creates an instance of the class for adding a rig for animation. The artv2 menu calls this function."""

    if cmds.window("pyArtEditRigWin", exists=True):
        cmds.deleteUI("pyArtEditRigWin", wnd=True)

    gui = ART_EditRigUI(False, True, getMainWindow())
    gui.show()
