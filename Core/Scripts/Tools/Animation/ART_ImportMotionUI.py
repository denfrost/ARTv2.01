"""Module containing classes for importing FBX animation data onto the rig and a UI front-end."""

import json
import os
import shutil
import tempfile
from functools import partial

import Utilities.utils as utils
import maya.cmds as cmds
import maya.mel as mel
# import statements
# noinspection PyUnresolvedReferences
from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Utilities.interfaceUtils as interfaceUtils


class Import_FBX(object):
    """
    usage:
    import Tools.Animation.ART_ImportMotionUI as im
    im.Import_FBX(fbx file path, character_namespace, frame offset, optional settings file)
    """

    def __init__(self, file_path, character, frame_offset, settings_file=None):

        self.file_path = utils.returnFriendlyPath(file_path)
        self.character = character
        self.frame_offset = frame_offset
        self.settings_file = settings_file

        if not os.path.exists(file_path):
            cmds.warning("file does not exist: " + os.path.normpath(file_path))
            return
        if settings_file is not None:
            if not os.path.exists(settings_file):
                cmds.warning("file does not exist: " + os.path.normpath(settings_file))
                return

        self.import_fbx()

    def import_fbx(self):
        """
        imports fbx animation data onto the rig controls, baking the data down.
        """

        for plugin in ["OneClick.mll", "fbxmaya.mll"]:
            try:
                cmds.loadPlugin(plugin)
            except RuntimeError:
                cmds.warning(plugin + " failed to load. Aborting import operation.")
                return

        if not os.path.exists(self.file_path):
            cmds.warning("No such file exists")
            return

        # duplicate the character's root
        if cmds.objExists("root"):
            cmds.warning("There is already a skeleton in the scene with the name \"root\". Aborting")
            return

        newSkeleton = cmds.duplicate(self.character + ":root")
        cmds.select(newSkeleton)
        cmds.delete(constraints=True)

        module_items = self._setup_module_import_method()

        returned_data = self._setup_constraints(module_items)
        controls = returned_data[0]
        postModules = returned_data[1]

        # ensure that the scene is in 30fps
        cmds.currentUnit(time='ntsc')
        cmds.playbackOptions(min=0, max=100, animationStartTime=0, animationEndTime=100)
        cmds.currentTime(0)
        cmds.refresh(force=True)

        self._rename_joints()

        self._import_fbx_file(controls)

        # Post Modules: Modules that have post-bake operations needing to be done
        cmds.refresh(force=True)
        for each in postModules:
            method = each[0]
            character = each[1]
            inst = each[2]
            inst.importFBX_post(method, character)

        # Clean up (delete duplicate skeleton)
        cmds.delete("root")

        self._add_frame_offset(controls)

    def _setup_module_import_method(self):

        # get rig modules
        if cmds.objExists(self.character + ":" + "ART_RIG_ROOT"):
            modules = cmds.listConnections(self.character + ":" + "ART_RIG_ROOT.rigModules")

            module_items = []
            for module in modules:
                moduleType = cmds.getAttr(module + ".moduleType")
                mod = __import__("RigModules." + moduleType, {}, {}, [moduleType])
                fbx_options = mod.fbxImport

                if self.settings_file is None:
                    if "FK" in fbx_options:
                        module_items.append([module, "FK"])
                    else:
                        module_items.append([module, "None"])
                else:
                    # open and read the file
                    f = open(utils.returnFriendlyPath(self.settings_file), 'r')
                    data = json.load(f)
                    f.close()

                    for each in data:
                        if each[0] == module:
                            module_items.append([module, fbx_options[each[1]]])

            return module_items

    def _setup_constraints(self, module_items):

        controls = []
        postModules = []

        # setup the constraints
        for each in module_items:
            # get inst
            modType = cmds.getAttr(each[0] + ".moduleType")
            modName = cmds.getAttr(each[0] + ".moduleName")
            mod = __import__("RigModules." + modType, {}, {}, [modType])

            # list of modules that have post bake operations needed
            specialModules = ["ART_Leg_Standard"]

            # get the class name from that module file (returns Modules.ART_Root.ART_Root for example)
            moduleClass = getattr(mod, mod.className)

            # find the instance of that module
            moduleInst = moduleClass(self, modName)

            # set namespace for instance
            moduleInst.namespace = self.character + ":"

            # run the module's pre import function
            moduleInst.importFBX_pre(each[1], self.character)

            if modType in specialModules:
                postModules.append([each[1], self.character, moduleInst])

            returnControls = moduleInst.importFBX(each[1], self.character)
            cmds.refresh(force=True)
            if returnControls is not None:
                controls.extend(returnControls)

        return [controls, postModules]

    def _rename_joints(self):
        # rename joints if override data is present
        if cmds.objExists(self.character + ":ART_RIG_ROOT.exportOverrides"):
            connections = cmds.listConnections(self.character + ":ART_RIG_ROOT.exportOverrides")
            if connections is not None:
                attrs = cmds.listAttr(connections[0], ud=True)

                for attr in attrs:
                    value = cmds.getAttr(connections[0] + "." + attr)

                    if cmds.objExists(attr):
                        cmds.rename(attr, value)

    def _import_fbx_file(self, controls):
        # import the FBX file
        string = "FBXImportMode -v \"exmerge\";"
        string += "FBXImport -file \"" + self.file_path + "\";"
        string += "FBXImportFillTimeline -v true;"
        string += "FBXImportProtectDrivenKeys   -v true;"
        mel.eval(string)

        # ensure we're on the base layer
        animLayers = cmds.ls(type="animLayer")
        if len(animLayers) > 0:
            for layer in animLayers:
                cmds.animLayer(layer, edit=True, selected=False)
            cmds.animLayer("BaseAnimation", edit=True, selected=True, preferred=True)

        # snap timeline to length of imported animation
        cmds.select("root", hi=True)
        firstFrame = cmds.findKeyframe(cmds.ls(sl=True), which='first')
        lastFrame = cmds.findKeyframe(cmds.ls(sl=True), which='last')
        if lastFrame == firstFrame:
            lastFrame = lastFrame + 1

        cmds.playbackOptions(min=firstFrame, max=lastFrame, animationStartTime=firstFrame, animationEndTime=lastFrame)

        # BAKE!maya
        cmds.select(controls)
        cmds.refresh(force=True)

        currentMode = cmds.evaluationManager(q=True, mode=True)[0]
        cmds.evaluationManager(mode="off")
        cmds.bakeResults(simulation=True, t=(firstFrame, lastFrame), pok=True, sampleBy=1, disableImplicitControl=False,
                         minimizeRotation=False, sparseAnimCurveBake=False,
                         at=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"])
        cmds.evaluationManager(mode=currentMode)

    def _add_frame_offset(self, controls):

        # Look at frame offset, and offset animation based on that
        cmds.select(controls)
        cmds.keyframe(timeChange=self.frame_offset, r=True)

        firstFrame = cmds.findKeyframe(which='first')
        lastFrame = cmds.findKeyframe(which='last')
        cmds.playbackOptions(min=firstFrame, max=lastFrame, animationStartTime=firstFrame, animationEndTime=lastFrame)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_ImportMotion(object):
    """
    front-end interface for importing FBX animation data. Allows user to choose fbx file, set module import methods,
    and specify a frame offset.
    """
    
    def __init__(self, animPickerUI):

        super(ART_ImportMotion, self).__init__()

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.pickerUI = animPickerUI

        # build the UI
        self._build_interface()

    def _build_interface(self):

        if cmds.window("pyART_ImportMotionWIN", exists=True):
            cmds.deleteUI("pyART_ImportMotionWIN", wnd=True)

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.pickerUI)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.tabStyle = interfaceUtils.get_style_sheet("small_tabs")
        self.mainWin.setStyleSheet(self.style)

        self.mainWin.setMinimumSize(QtCore.QSize(600, 350))
        self.mainWin.setMaximumSize(QtCore.QSize(600, 350))
        self.mainWin.resize(600, 350)
        self.mainWin.closeEvent = self.closeEvent

        # set qt object name
        self.mainWin.setObjectName("pyART_ImportMotionWIN")
        self.mainWin.setWindowTitle("Import Motion")

        # tabs
        self.importTabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.importTabs)

        self.importTabs.setStyleSheet(self.tabStyle)

        # FBX Tab
        self._fbx_importTab = QtWidgets.QFrame()
        self._fbx_importTab.setObjectName("dark")
        self.importTabs.addTab(self._fbx_importTab, "FBX")

        # Anim Curve Tab
        self.animImportTab = QtWidgets.QWidget()
        self.importTabs.addTab(self.animImportTab, "Animation")

        # =======================================================================
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # #FBX TAB
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # =======================================================================

        # horizontal layout
        self.fbxMainLayout = QtWidgets.QHBoxLayout(self._fbx_importTab)

        # LEFT SIDE

        # module list widget
        self.fbxModuleList = QtWidgets.QListWidget()
        self.fbxMainLayout.addWidget(self.fbxModuleList)
        self.fbxModuleList.setMinimumSize(QtCore.QSize(300, 280))
        self.fbxModuleList.setMaximumSize(QtCore.QSize(300, 280))
        self.fbxModuleList.setSpacing(15)
        self.fbxModuleList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # RIGHT SIDE

        self.fbxRightLayout = QtWidgets.QVBoxLayout()
        self.fbxMainLayout.addLayout(self.fbxRightLayout)

        self.fbxCharacterCombo = QtWidgets.QComboBox()
        self.fbxCharacterCombo.setObjectName("mid")
        self.fbxRightLayout.addWidget(self.fbxCharacterCombo)
        self.fbxCharacterCombo.setMinimumSize(QtCore.QSize(250, 50))
        self.fbxCharacterCombo.setMaximumSize(QtCore.QSize(250, 50))
        self.fbxCharacterCombo.setIconSize(QtCore.QSize(45, 45))
        self.fbxCharacterCombo.currentIndexChanged.connect(partial(self._find_character_modules))

        self.fbxPathLayout = QtWidgets.QHBoxLayout()
        self.fbxRightLayout.addLayout(self.fbxPathLayout)

        self.fbxFilePath = QtWidgets.QLineEdit()
        self.fbxFilePath.setMinimumWidth(210)
        self.fbxFilePath.setMaximumWidth(210)
        self.fbxPathLayout.addWidget(self.fbxFilePath)
        self.fbxFilePath.setPlaceholderText("fbx file..")
        self.fbxFilePath.setObjectName("light")

        browseBtn = QtWidgets.QPushButton()
        browseBtn.setMinimumSize(30, 30)
        browseBtn.setMaximumSize(30, 30)
        self.fbxPathLayout.addWidget(browseBtn)
        browseBtn.setObjectName("load")
        browseBtn.clicked.connect(self._fbx_file_browse)

        self.frameOffsetLayout = QtWidgets.QHBoxLayout()
        self.fbxRightLayout.addLayout(self.frameOffsetLayout)

        frameOffset = QtWidgets.QLabel("Frame Offset:")
        frameOffset.setStyleSheet("background: transparent; font: bold;")
        self.frameOffsetLayout.addWidget(frameOffset)

        self.frameOffsetField = QtWidgets.QSpinBox()
        self.frameOffsetField.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.frameOffsetField.setRange(-1000, 10000)
        self.frameOffsetLayout.addWidget(self.frameOffsetField)

        # option to strip namespace
        self.stripNamespace = QtWidgets.QCheckBox("Strip Incoming Namespace")
        self.stripNamespace.setToolTip(
            "If the incoming FBX has a namespace, checking this\noption will strip that namespace upon import")
        self.stripNamespace.setChecked(False)
        # self.fbxRightLayout.addWidget(self.stripNamespace) running into an issue with this in 2016.5

        # Save/Load Settings
        saveLoadLayout = QtWidgets.QHBoxLayout()
        self.fbxRightLayout.addLayout(saveLoadLayout)

        _save_settingsBtn = QtWidgets.QPushButton("Save Settings")
        _save_settingsBtn.setMinimumSize(120, 30)
        _save_settingsBtn.setMaximumSize(120, 30)
        saveLoadLayout.addWidget(_save_settingsBtn)
        _save_settingsBtn.setObjectName("settings")
        _save_settingsBtn.setToolTip("Save out module import settings")
        _save_settingsBtn.clicked.connect(self._save_settings)

        _load_settingsBtn = QtWidgets.QPushButton("Load Settings")
        _load_settingsBtn.setMinimumSize(120, 30)
        _load_settingsBtn.setMaximumSize(120, 30)
        saveLoadLayout.addWidget(_load_settingsBtn)
        _load_settingsBtn.setObjectName("settings")
        _load_settingsBtn.setToolTip("Load and set module import settings")
        _load_settingsBtn.clicked.connect(self._load_settings)

        # SPACER!
        self.fbxRightLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # Button
        self.importFBXbutton = QtWidgets.QPushButton("Import")
        self.fbxRightLayout.addWidget(self.importFBXbutton)
        self.importFBXbutton.setObjectName("settings")
        self.importFBXbutton.setMinimumHeight(50)
        self.importFBXbutton.clicked.connect(self._fbx_import)

        # show window
        self.mainWin.show()

        # populate UI
        self._find_characters()
        self._find_character_modules()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "ImportMotion")
        self.mainWin.restoreGeometry(settings.value("geometry"))

    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "ImportMotion")
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self.mainWin, event)

    def _find_characters(self):

        self.characterInfo = []

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
            icon = QtGui.QIcon(iconPath)

            self.fbxCharacterCombo.addItem(icon, namespace)

    def _find_character_modules(self, *args):

        print args
        self.fbxModuleList.clear()

        # current character
        selectedChar = self.fbxCharacterCombo.currentText()

        # get rig modules
        if cmds.objExists(selectedChar + ":" + "ART_RIG_ROOT"):
            modules = cmds.listConnections(selectedChar + ":" + "ART_RIG_ROOT.rigModules")

            for module in modules:
                niceName = cmds.getAttr(module + ".moduleName")
                moduleType = cmds.getAttr(module + ".moduleType")

                # create widget
                item = QtWidgets.QListWidgetItem()

                widgetItem = QtWidgets.QGroupBox()
                widgetItem.setMinimumHeight(50)
                widgetItem.setProperty("module", module)
                widgetItem.setObjectName("light")

                layout = QtWidgets.QHBoxLayout(widgetItem)
                label = QtWidgets.QLabel(niceName)
                label.setStyleSheet("background: transparent; font: bold;")
                layout.addWidget(label)

                comboBox = QtWidgets.QComboBox()
                layout.addWidget(comboBox)

                # add items to combo box bases on module class var
                mod = __import__("RigModules." + moduleType, {}, {}, [moduleType])
                fbxOptions = mod.fbxImport

                for each in fbxOptions:
                    comboBox.addItem(each)

                comboBox.setCurrentIndex(1)

                self.fbxModuleList.addItem(item)
                self.fbxModuleList.setItemWidget(item, widgetItem)

    def _fbx_file_browse(self):

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        path = settings.value("ImportPath")
        if path is None:
            path = self.projectPath

        # see if export node exists, and if it does, see if there is an existing export path
        try:
            path = cmds.fileDialog2(fm=1, okc="Import FBX", dir=path, ff="*.fbx")
            nicePath = utils.returnFriendlyPath(path[0])

            self.fbxFilePath.setText(nicePath)
            settings.setValue("ImportPath", nicePath)

        except StandardError:
            pass

    def _fbx_import(self):

        # get info from the UI
        filePath = self.fbxFilePath.text()
        character = self.fbxCharacterCombo.currentText()
        frameOffset = self.frameOffsetField.value()

        dirpath = tempfile.mkdtemp()
        settings_file = os.path.join(dirpath, "import_settings.json")
        self._save_settings(settings_file)

        Import_FBX(filePath, character, frameOffset, settings_file)

        shutil.rmtree(dirpath)

    def _save_settings(self, file_path=None):

        # loop through each of the modules and read the qComboBox value
        moduleItems = []
        for i in range(self.fbxModuleList.count()):
            item = self.fbxModuleList.item(i)
            itemWidget = self.fbxModuleList.itemWidget(item)
            itemModule = itemWidget.property("module")

            children = itemWidget.children()
            for child in children:
                if type(child) == QtWidgets.QComboBox:
                    importMethod = child.currentIndex()
                    moduleItems.append([itemModule, importMethod])

        if file_path is None:
            # save import settings in the settings folder
            if not os.path.exists(os.path.join(self.toolsPath, "settings")):
                os.makedirs(os.path.join(self.toolsPath, "settings"))

            if not os.path.exists(os.path.join(self.toolsPath, "settings" + os.sep + "importSettings")):
                os.makedirs(os.path.join(self.toolsPath, "settings" + os.sep + "importSettings"))

            # open a file browser dialog for user to name file
            dialog = QtWidgets.QFileDialog(None, "Save",
                                           os.path.join(self.toolsPath, "settings" + os.sep + "importSettings"))
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setDefaultSuffix("json")
            dialog.exec_()
            fileName = dialog.selectedFiles()
            file_path = fileName[0]

        # write file
        f = open(file_path, 'w')
        json.dump(moduleItems, f)
        f.close()

    def _load_settings(self):

        # open a file browser dialog for user to name file
        dialog = QtWidgets.QFileDialog(None, "Open",
                                       os.path.join(self.toolsPath, "settings" + os.sep + "importSettings"))
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setDefaultSuffix("json")
        dialog.exec_()
        fileName = dialog.selectedFiles()

        # open and read the file
        f = open(fileName[0], 'r')
        data = json.load(f)
        f.close()

        # find items in UI
        modules = {}
        for i in range(self.fbxModuleList.count()):
            item = self.fbxModuleList.item(i)
            itemWidget = self.fbxModuleList.itemWidget(item)
            itemModule = itemWidget.property("module")

            children = itemWidget.children()
            for child in children:
                if type(child) == QtWidgets.QComboBox:
                    modules[itemModule] = child

        # loop through data
        keys = modules.keys()
        for each in data:
            if each[0] in keys:
                comboBox = modules.get(each[0])
                comboBox.setCurrentIndex(each[1])
