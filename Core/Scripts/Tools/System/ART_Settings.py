from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken

from functools import partial
import maya.cmds as cmds
import os
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


def getMainWindow():
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    # pyside QMainWindow takes in a QWidget rather than QObject
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


windowTitle = "ART_Settings"
windowObject = "pyArtSettingsWin"


class ART_Settings(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(ART_Settings, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")
        self.projPath = settings.value("projectPath")

        # build the UI
        self.buildSettingsUi()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildSettingsUi(self):

        # fonts
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)

        fontSmall = QtGui.QFont()
        fontSmall.setPointSize(9)
        fontSmall.setBold(True)

        # load the stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.resize(600, 260)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(600, 240))
        self.setMaximumSize(QtCore.QSize(600, 240))

        # create the QFrame
        self.frame = QtWidgets.QFrame()
        self.layout.addWidget(self.frame)
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        # location
        self.locationLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.addLayout(self.locationLayout)

        # location -> label
        label = QtWidgets.QLabel("Tools Location:  ")
        self.locationLayout.addWidget(label)
        label.setFont(font)
        label.setMinimumWidth(150)

        # location -> line edit
        path = utils.returnFriendlyPath(self.toolsPath)
        self.locationPath = QtWidgets.QLineEdit(path)
        self.locationLayout.addWidget(self.locationPath)
        self.locationPath.setMinimumHeight(30)

        # location -> browse button
        self.locationBrowse = QtWidgets.QPushButton()
        self.locationLayout.addWidget(self.locationBrowse)

        self.locationBrowse.setMinimumSize(30, 30)
        self.locationBrowse.setMaximumSize(30, 30)
        self.locationBrowse.setObjectName("load")
        self.locationBrowse.clicked.connect(partial(self.browse, self.locationPath))

        # scripts folder
        self.scriptsLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.addLayout(self.scriptsLayout)

        # scripts -> label
        label = QtWidgets.QLabel("Scripts:  ")
        self.scriptsLayout.addWidget(label)
        label.setFont(fontSmall)
        label.setMinimumWidth(150)

        # scripts -> line edit
        path = utils.returnFriendlyPath(self.scriptPath)
        self.scriptsPath = QtWidgets.QLineEdit(path)
        self.scriptsLayout.addWidget(self.scriptsPath)
        self.scriptsPath.setMinimumHeight(30)

        # scripts -> browse button
        self.scriptsBrowse = QtWidgets.QPushButton()
        self.scriptsLayout.addWidget(self.scriptsBrowse)

        self.scriptsBrowse.setMinimumSize(30, 30)
        self.scriptsBrowse.setMaximumSize(30, 30)
        self.scriptsBrowse.setObjectName("load")
        self.scriptsBrowse.clicked.connect(partial(self.browse, self.scriptsPath))

        # icons folder
        self.iconsLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.addLayout(self.iconsLayout)

        # icons -> label
        label = QtWidgets.QLabel("Icons:  ")
        self.iconsLayout.addWidget(label)
        label.setFont(fontSmall)
        label.setMinimumWidth(150)

        # icons -> line edit
        path = utils.returnFriendlyPath(self.iconsPath)
        self.iconPath = QtWidgets.QLineEdit(path)
        self.iconsLayout.addWidget(self.iconPath)
        self.iconPath.setMinimumHeight(30)

        # icons -> browse button
        self.iconsBrowse = QtWidgets.QPushButton()
        self.iconsLayout.addWidget(self.iconsBrowse)

        self.iconsBrowse.setMinimumSize(30, 30)
        self.iconsBrowse.setMaximumSize(30, 30)
        self.iconsBrowse.setObjectName("load")
        self.iconsBrowse.clicked.connect(partial(self.browse, self.iconsPath))

        # projects folder
        self.projectsLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.addLayout(self.projectsLayout)

        # projects -> label
        label = QtWidgets.QLabel("Projects:  ")
        self.projectsLayout.addWidget(label)
        label.setFont(fontSmall)
        label.setMinimumWidth(150)

        # projects -> line edit
        path = utils.returnFriendlyPath(self.projPath)
        self.projectsPath = QtWidgets.QLineEdit(path)
        self.projectsLayout.addWidget(self.projectsPath)
        self.projectsPath.setMinimumHeight(30)

        # projects -> browse button
        self.projectsBrowse = QtWidgets.QPushButton()
        self.projectsLayout.addWidget(self.projectsBrowse)

        self.projectsBrowse.setMinimumSize(30, 30)
        self.projectsBrowse.setMaximumSize(30, 30)
        self.projectsBrowse.setObjectName("load")
        self.projectsBrowse.clicked.connect(partial(self.browse, self.projectsPath))

        # Save button
        self.saveChangesBtn = QtWidgets.QPushButton("Save Changes")
        self.widgetLayout.addWidget(self.saveChangesBtn)
        self.saveChangesBtn.setFont(font)
        self.saveChangesBtn.setObjectName("settings")
        self.saveChangesBtn.setMinimumHeight(40)
        self.saveChangesBtn.clicked.connect(partial(self.saveSettings))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def browse(self, lineEdit):

        try:
            newPath = cmds.fileDialog2(dir=self.toolsPath, fm=3)[0]
            newPath = utils.returnFriendlyPath(newPath)
            lineEdit.setText(newPath)

        except:
            pass  # in case user cancels on Maya's browse dialog

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveSettings(self):

        # get data from ui
        mayaToolsDir = self.locationPath.text()
        scriptDir = self.scriptsPath.text()
        iconsDir = self.iconPath.text()
        projectsDir = self.projectsPath.text()

        # save data

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        settings.setValue("toolsPath", mayaToolsDir)
        settings.setValue("scriptPath", scriptDir)
        settings.setValue("iconPath", iconsDir)
        settings.setValue("projectPath", projectsDir)

        # Give message regarding data being saved, but it won't take effect until Maya is restarted.
        cmds.confirmDialog(title="Settings Saved",
                           message="Please close Maya and reopen in order to have these settings take effect.")

        # close UI
        if cmds.window("pyArtSettingsWin", exists=True):
            cmds.deleteUI("pyArtSettingsWin", wnd=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    if cmds.window("pyArtSettingsWin", exists=True):
        cmds.deleteUI("pyArtSettingsWin", wnd=True)

    gui = ART_Settings(getMainWindow())
    gui.show()
