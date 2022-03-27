'''
Created on Aug 21, 2015

@author: jeremy.ernst
'''

# import statements
import os

from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import maya.cmds as cmds
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


class ART_MovePickerToTab(object):
    def __init__(self, animPickerUI, modulesToAdd, parent=None):

        super(ART_MovePickerToTab, self).__init__()
        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        self.pickerUI = animPickerUI
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

        if cmds.window("pyART_movePickerToTabWIN", exists=True):
            cmds.deleteUI("pyART_movePickerToTabWIN", wnd=True)

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.pickerUI)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.layout)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.mainWin.setStyleSheet(self.style)

        self.mainWin.setMinimumSize(QtCore.QSize(400, 400))
        self.mainWin.setMaximumSize(QtCore.QSize(400, 400))
        self.mainWin.resize(400, 400)

        # set qt object name
        self.mainWin.setObjectName("pyART_movePickerToTabWIN")
        self.mainWin.setWindowTitle("Move Picker")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.mainWin.setWindowIcon(window_icon)

        self.mainWin.closeEvent = self.closeEvent

        # create 2 columns
        self.column1 = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.column1)

        self.column2 = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.column2)

        # create left side list widget, which will house the picker items
        self.pickerItemsList = QtWidgets.QListWidget()
        self.column1.addWidget(self.pickerItemsList)
        self.pickerItemsList.setMinimumSize(180, 300)
        self.pickerItemsList.setMaximumSize(180, 300)

        # get the current tab index and the widget
        index = self.pickerUI.characterTabs.currentIndex()
        widget = self.pickerUI.characterTabs.widget(index)

        # get the tab text
        character = self.pickerUI.characterTabs.tabToolTip(index)

        # find character nodes in the scene, and compare namespace to selected tab
        characterMods = utils.returnCharacterModules()
        nodeNamespace = ""

        for each in characterMods:
            if cmds.objExists(each + ".namespace"):
                namespace = cmds.getAttr(each + ".namespace")
                if namespace == character:
                    nodeNamespace = namespace + ":"

        for module in self.modulesToAdd:
            if module[0] is not None:
                if module[2] is None:
                    modName = cmds.getAttr(nodeNamespace + module[0] + ".moduleName")
                else:
                    modName = module[2]

                qlistItem = QtWidgets.QListWidgetItem(modName)
                qlistItem.setData(QtCore.Qt.UserRole, module[1])
                self.pickerItemsList.addItem(qlistItem)

        # create right side list widget, which will house the available tabs
        self.tabList = QtWidgets.QListWidget()
        self.column2.addWidget(self.tabList)
        self.tabList.setMinimumSize(180, 300)
        self.tabList.setMaximumSize(180, 300)

        tabs = self.findTabs(False)
        for tab in tabs:
            qlistItem = QtWidgets.QListWidgetItem(tab[0])
            qlistItem.setData(QtCore.Qt.UserRole, tab[1])
            self.tabList.addItem(qlistItem)

        # create button for move selected picker to selected tab
        self.movePickerBtn = QtWidgets.QPushButton("Move Selected Picker To Selected Tab")
        self.mainLayout.addWidget(self.movePickerBtn)
        self.movePickerBtn.setObjectName("settings")
        self.movePickerBtn.setMinimumHeight(50)
        self.movePickerBtn.setMaximumHeight(50)
        self.movePickerBtn.clicked.connect(self.moveToTab)

        # show ui
        self.mainWin.show()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "MovePickerToTab")
        self.mainWin.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "MovePickerToTab")
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self.mainWin, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findTabs(self, moving, newTab=None):

        # get the current tab index and the widget
        index = self.pickerUI.characterTabs.currentIndex()
        widget = self.pickerUI.characterTabs.widget(index)
        tabs = []

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child

                for i in range(tab.count()):
                    tabName = tab.tabText(i)
                    tabs.append([tabName, i])

                    if moving == True:
                        tab.setCurrentIndex(newTab)
                        canvasIndex = tab.currentIndex()
                        canvasWidget = tab.widget(canvasIndex)
                        canvasChildren = canvasWidget.children()

                        for canvasChild in canvasChildren:
                            if type(canvasChild) == QtWidgets.QGraphicsView:
                                view = canvasChild
                                scene = view.scene()

        if moving:
            return scene
        else:
            return tabs

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def moveToTab(self):

        selectedItem = self.pickerItemsList.currentItem()
        selectedTab = self.tabList.currentItem()

        try:
            newTab = selectedTab.data(QtCore.Qt.UserRole)
        except:
            cmds.warning("Please Select a Tab from the list.")
            return

        # get selected tab's scene
        scene = self.findTabs(True, newTab)

        # get data from selectedItem
        pickerItem = selectedItem.data(QtCore.Qt.UserRole)
        try:
            parentXform = pickerItem.parentItem().transform()
        except:
            parentXform = pickerItem.transform()

        # add to scene
        scene.addItem(pickerItem)

        # =======================================================================
        # #mirror if needed
        # =======================================================================
        if parentXform.m11() == -1:
            pickerItem.setTransformOriginPoint(pickerItem.boundingRect().center())
            pickerItem.setTransform(QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, scene.sceneRect().width(), 0.0))
            pickerItem.setTransformOriginPoint(pickerItem.boundingRect().center())

            children = pickerItem.childItems()
            for child in children:
                if type(child) == QtWidgets.QGraphicsSimpleTextItem:
                    child.setTransformOriginPoint(child.boundingRect().center())
                    child.setTransform(QtGui.QTransform(-1.0, 0.0, 0.0, 1.0, child.boundingRect().width(), 0.0))


                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def closeWin(self, event):

        cmds.deleteUI("pyART_movePickerToTabWIN", wnd=True)
