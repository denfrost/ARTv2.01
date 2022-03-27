"""
Author: Jeremy Ernst
"""

# import statements
import maya.cmds as cmds
import os

import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_AddModuleToCanvas(object):
    """
    This tool presents a UI that lists all modules not currently on the animation picker canvas, and allows the user
    to choose modules from the list to add to the animation picker canvas. This is an animator-facing tool.

    .. image:: /images/addModuleToCanvas.png

    """

    def __init__(self, animPickerUI, modulesToAdd, parent=None):
        """
        initialize the class, get the QSettings for the tool, and call on buildUI.

        :param animPickerUI: the instance of the animation picker class that launched this class.
        :param modulesToAdd: A list of the modules to add, which is a list of modules currently not on the animPickerUI

        """
        super(ART_AddModuleToCanvas, self).__init__()
        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.pickerUI = animPickerUI
        self.modules = []
        self.modulesToAdd = modulesToAdd

        # assign close event
        self.closeEvent = self.closeWin

        # build the UI
        self.buildUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        """
        Builds the interface for the tool, showing a list of modules not currently displayed on the picker.

        """

        if cmds.window("pyART_AddToCanvasWIN", exists=True):
            cmds.deleteUI("pyART_AddToCanvasWIN", wnd=True)

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.pickerUI)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.mainWin.setStyleSheet(self.style)

        self.mainWin.setMinimumSize(QtCore.QSize(250, 400))
        self.mainWin.setMaximumSize(QtCore.QSize(250, 400))
        self.mainWin.resize(250, 400)
        self.mainWin.closeEvent = self.closeEvent

        # set qt object name
        self.mainWin.setObjectName("pyART_AddToCanvasWIN")
        self.mainWin.setWindowTitle("Add Module To Canvas")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.mainWin.setWindowIcon(window_icon)

        # label, listWidget, button
        label = QtWidgets.QLabel("Available Modules:")
        label.setProperty("boldFont", True)
        self.layout.addWidget(label)

        self.moduleList = QtWidgets.QListWidget()
        self.moduleList.setMaximumSize(230, 300)
        self.moduleList.setMinimumSize(230, 300)
        self.layout.addWidget(self.moduleList)

        # add modules to listWidget
        self.addModulesToList()

        # create add button
        button = QtWidgets.QPushButton("Add Selected To Canvas")
        button.setMinimumHeight(30)
        self.layout.addWidget(button)
        button.setObjectName("settings")
        button.clicked.connect(self.addSelectedToCanvas)

        # show ui
        self.mainWin.show()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "AddModuleToPicker")
        self.mainWin.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "AddModuleToPicker")
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self.mainWin, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addModulesToList(self):
        """
        Take the modules passed into the class, and if the modules do not already exist on the canvas, add them to
        the list widget.

        """

        existing = self.getExistingModules()

        for module in self.modulesToAdd:
            if module not in existing:
                modName = cmds.getAttr(module + ".moduleName")

                # add to listWIdget
                index = self.pickerUI.characterTabs.currentIndex()
                widget = self.pickerUI.characterTabs.widget(index)
                characterNode = widget.property("charNode")

                item = QtWidgets.QListWidgetItem(modName)
                item.setData(QtCore.Qt.UserRole, [module, characterNode])
                self.moduleList.addItem(item)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addSelectedToCanvas(self):
        """
        Takes the selected module in the list widget and adds it to the picker canvas. The picker UI is contained in
        the self.pickerUI.

        """

        selected = self.moduleList.currentItem()
        module = selected.data(QtCore.Qt.UserRole)[0]

        index = self.pickerUI.characterTabs.currentIndex()
        widget = self.pickerUI.characterTabs.widget(index)
        characterNode = widget.property("charNode")

        # get inst
        modType = cmds.getAttr(module + ".moduleType")
        modName = cmds.getAttr(module + ".moduleName")
        mod = __import__("RigModules." + modType, {}, {}, [modType])

        # get the class name from that module file (returns RigModules.ART_Root.ART_Root for example)
        moduleClass = getattr(mod, mod.className)

        # find the instance of that module
        moduleInst = moduleClass(self, modName)
        self.modules.append(moduleInst)

        scene = self.getCurrentCanvasTab()

        # find out if charNode has a namespace
        if cmds.objExists(characterNode + ".namespace"):
            namespace = cmds.getAttr(characterNode + ".namespace") + ":"
        else:
            namespace = ""

        # pass in the network node and the namespace
        picker = moduleInst.pickerUI(scene.sceneRect().center(), self.pickerUI, module, namespace)
        scene.addItem(picker[0])
        self.pickerUI.selectionScriptJobs.append(picker[2])

        # =======================================================================
        # #mirror the module's pickerBorderItem if needed
        # =======================================================================
        if picker[1] == True:
            picker[0].setTransformOriginPoint(picker[0].boundingRect().center())
            picker[0].setTransform(QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, picker[0].boundingRect().width() * 2, 0.0))

            children = picker[0].childItems()
            if children is not None:
                self.mirrorChildren(children)

        row = self.moduleList.row(selected)
        self.moduleList.takeItem(row)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mirrorChildren(self, children):
        """
        Take the passed in children and mirror the item so the text is not backwards. When a module is added to the
        canvas, if it was a right side module, it will be mirrored. This then unmirrors the text.

        :param children: List of QGraphicsSimpleTextItems that need to be mirrored.

        """

        # for mirroring text on any child items of a pickerBorderItem
        for child in children:
            if type(child) == QtWidgets.QGraphicsSimpleTextItem:
                child.setTransformOriginPoint(child.boundingRect().center())
                child.setTransform(QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, child.boundingRect().width(), 0.0))

            children = child.childItems()
            if children is not None:
                self.mirrorChildren(children)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getCurrentCanvasTab(self):
        """
        Get the current tab of the current character of the animation picker.
        :return: returns the QGraphicsScene that items can then be added to.

        """
        # get the current tab index and the widget
        index = self.pickerUI.characterTabs.currentIndex()
        widget = self.pickerUI.characterTabs.widget(index)

        children = widget.children()
        for child in children:
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                canvasIndex = tab.currentIndex()
                canvasWidget = tab.widget(canvasIndex)

                canvasChildren = canvasWidget.children()
                for canvasChild in canvasChildren:
                    if type(canvasChild) == QtWidgets.QGraphicsView:
                        view = canvasChild
                        scene = view.scene()

        return scene

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getExistingModules(self):
        """
        Find all existing modules on the canvas and return those modules as a list.
        :return: List of modules whose picker exists on the canvas.

        """

        # get the current tab index and the widget
        index = self.pickerUI.characterTabs.currentIndex()
        widget = self.pickerUI.characterTabs.widget(index)
        characterNode = widget.property("charNode")
        characterNodeModules = cmds.listConnections(characterNode + ".rigModules")

        namespace = None
        if cmds.objExists(characterNode + ".namespace"):
            namespace = cmds.getAttr(characterNode + ".namespace") + ":"

        returnData = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                selectedTab = tab.currentIndex()

                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            # get all items in the gfxScene
                            itemsInScene = scene.items()

                            for item in itemsInScene:
                                # if we find our top level picker item (the borderItem), get it's data
                                if type(item) == interfaceUtils.pickerBorderItem or item.type() == 3:
                                    module = item.data(QtCore.Qt.UserRole)

                                    if module is not None:
                                        if namespace is None:
                                            if module not in returnData:
                                                returnData.append(module)
                                        else:
                                            if (namespace + module) not in returnData:
                                                returnData.append(namespace + module)
                tab.setCurrentIndex(selectedTab)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeWin(self, event):
        """
        deletes the UI.

        """

        cmds.deleteUI("pyART_AddToCanvasWIN", wnd=True)
