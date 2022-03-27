from functools import partial
import os

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

windowName = "pyART_RigSettingsWIN"
windowTitle = "Rig Settings"

noKeys = """
    border: 2px solid rgb(0,0,0);
    border-radius: 5px;
    background-color: rgb(30,30,30);
    font: bold 12px;
    selection-background-color: black;
"""

keys = """
    border: 2px solid rgb(0,0,0);
    border-radius: 5px;
    background-color: rgb(210,0,0);
    font: bold 12px;
    selection-background-color: black;
"""


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_RigSettingsUI(QtWidgets.QMainWindow):
    """
    This class creates an interface that compiles all of the rig settings. You can select the settings, change their
    values, and key the settings from within the interface.

    .. image:: /images/rig_settings_tool.png
    """

    def __init__(self, animUI, parent=None):
        """
        Instantiates the class, gets settings values from QSettings. Calls on building the interface.
        """

        super(ART_RigSettingsUI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")
        self.projectPath = settings.value("projectPath")

        self.character = ""

        # load the stylesheets
        self.style = interfaceUtils.get_style_sheet("artv2_style")

        # create some lists for search function
        self.groups = {}
        self.attrs = {}
        self.fields = []

        # build the interface
        self.animUI = animUI
        self.buildInterface()

        # add everything to the scroll area
        self.scroll_contents.setLayout(self.scroll_contents_layout)
        self.scroll_area_vertical = QtWidgets.QScrollArea()
        self.scroll_area_vertical.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area_vertical.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_vertical.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scroll_area_vertical)
        self.scroll_area_vertical.setWidget(self.scroll_contents)
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.scroll_contents_layout.addItem(spacer)

        cmds.scriptJob(event=["timeChanged", self._update_fields], kws=True, parent=windowName)

        self._update_fields()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildInterface(self):
        """
        Builds the interface for the tool.

            .. seealso:: build_settings_widget
            .. seealso:: _build_attr_widget

        """

        # define main window dimensions, object name, title, etc.
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName, wnd=True)

        self.window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(self.window_icon)
        self.setStyleSheet(self.style)

        # set the window size
        self.setMinimumSize(QtCore.QSize(300, 600))
        self.setMaximumSize(QtCore.QSize(300, 600))

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)

        # set qt object name
        self.setObjectName(windowName)
        self.setWindowTitle(windowTitle)

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("dark")
        self.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        # create the search bar and key all buttons
        topLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(topLayout)

        self.searchBar = QtWidgets.QLineEdit()
        self.searchBar.setObjectName("light")
        self.searchBar.setMinimumSize(QtCore.QSize(160, 30))
        self.searchBar.setMaximumSize(QtCore.QSize(160, 30))
        self.searchBar.setPlaceholderText("Search Modules...")
        self.searchBar.textChanged.connect(self.search)
        tooltip = "Search for a specific module's settings."
        self.searchBar.setToolTip(tooltip)

        word_list = self._get_modules()
        completer = QtWidgets.QCompleter(word_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.searchBar.setCompleter(completer)

        topLayout.addWidget(self.searchBar)

        self.key_all_btn = QtWidgets.QPushButton("Key All")
        self.key_all_btn.setMinimumSize(QtCore.QSize(56, 30))
        self.key_all_btn.setMaximumSize(QtCore.QSize(56, 30))
        self.key_all_btn.setObjectName("settings")
        self.key_all_btn.clicked.connect(self.key_all_settings)
        topLayout.addWidget(self.key_all_btn)
        tooltip = "Key all rig settings for all modules of this character."
        self.key_all_btn.setToolTip(tooltip)

        self.select_settings_btn = QtWidgets.QPushButton("")
        self.select_settings_btn.setMinimumSize(QtCore.QSize(30, 30))
        self.select_settings_btn.setMaximumSize(QtCore.QSize(30, 30))
        self.select_settings_btn.setObjectName("select")
        self.select_settings_btn.clicked.connect(self.select_settings)
        tooltip = "Selects the main settings node that has all settings listed."
        self.select_settings_btn.setToolTip(tooltip)

        topLayout.addWidget(self.select_settings_btn)

        # create the scroll contents and the vboxlayout to populate selection sets into
        self.scroll_contents = QtWidgets.QFrame()
        self.scroll_contents.setObjectName("dark")
        self.scroll_contents_layout = QtWidgets.QVBoxLayout()

        # populate settings
        self.populateSettings()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "RigSettings")
        self.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "RigSettings")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateSettings(self):
        """
        Find all settings nodes, then call on function to build groupbox for each setting

            .. seealso:: _get_settings_nodes()
            .. seealso:: build_settings_widget()
        """

        # find all rig settings
        settings = self._get_settings_nodes()

        # construct the widget for each module's settings
        for each in settings:
            self.build_settings_widget(each)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def build_settings_widget(self, data):
        """
        Builds the groupbox for each module's settings.

        :param data: a list comprised of lists that contain the module name and the corresponding settings node.

            .. seealso:: _build_attr_widget()

        """

        modName = data[0]
        settingsNode = data[1]

        attrs = cmds.listAttr(settingsNode, keyable=True)

        if attrs is not None:

            groupBox = QtWidgets.QGroupBox(modName)
            groupBox.setMinimumSize(QtCore.QSize(250, 30 * len(attrs) + 20))
            groupBox.setMaximumSize(QtCore.QSize(250, 30 * len(attrs) + 20))
            groupBox.setCheckable(True)
            groupBox.toggled.connect(partial(self._collapse_group, groupBox, 250, (30 * len(attrs) + 20)))
            groupBox.setProperty("max", 30 * len(attrs) + 20)
            self.scroll_contents_layout.addWidget(groupBox)

            self.groups[modName] = groupBox

            layout = QtWidgets.QVBoxLayout(groupBox)

            for attr in attrs:
                self._build_attr_widget(attr, settingsNode, layout)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_attr_widget(self, attr, settings, parent):
        """
        Builds a widget for each settings attribute that contains a label of the attribute, a lineEdit to modify the
        attribute, and a button to key that settings attribute.

        :param attr: The attribute name, which will be used for the label.
        :param settings: The settings node.
        :param parent: The groupbox layout that these widgets will be added to.
        """

        # create the layout
        layout = QtWidgets.QHBoxLayout()
        parent.addLayout(layout)

        # create the label
        label = QtWidgets.QLabel("    " + attr)
        label.setStyleSheet("background: transparent;")
        label.setMinimumWidth(140)
        label.setMaximumWidth(140)
        layout.addWidget(label)

        # create the lineEdit widget
        field = QtWidgets.QLineEdit()
        field.setMinimumWidth(50)
        field.setMaximumWidth(50)
        layout.addWidget(field)
        self.fields.append(field)

        # get the type of attribute and set the appropriate validator
        attr_type = cmds.getAttr(settings + "." + attr, type=True)
        if attr_type == "double":
            try:
                min = cmds.attributeQuery(attr, node=settings, min=True)[0]
            except RuntimeError:
                min = -360

            try:
                max = cmds.attributeQuery(attr, node=settings, max=True)[0]
            except RuntimeError:
                max = 360
            validator = QtGui.QDoubleValidator()
            validator.setRange(min, max)
            validator.setDecimals(3)
            validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
            field.setValidator(validator)

        # set the value to the attr's current value
        value = cmds.getAttr(settings + "." + attr)
        field.setText(str(value))

        # set some properties on the field
        field.setProperty("setting", settings)
        field.setProperty("attr", attr)
        field.setProperty("attr_type", attr_type)
        field.setProperty("keys", False)

        # hook up signal/slot
        field.editingFinished.connect(partial(self._set_attr, field, attr_type, settings, attr))

        # create the key settings button
        button = QtWidgets.QPushButton("K")
        button.setObjectName("orange")
        button.setMinimumSize(QtCore.QSize(20, 20))
        button.setMaximumSize(QtCore.QSize(20, 20))
        button.clicked.connect(partial(self._key_attr, field, settings, attr))
        layout.addWidget(button)
        tooltip = "Keys this specific attribute on this settings node."
        button.setToolTip(tooltip)

        self.attrs[settings + "_" + attr] = layout

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _set_attr(self, widget, attr_type, node, attr, *args):
        """
        Sets the setting attribute to the value in the lineEdit.

        :param widget: the lineEdit to read the value from
        :param attr_type: What type of attribute we are working with (used for validators)
        :param node: The settings node.
        :param attr: The attribute on the settings node we want to manipulate:
        """

        value = widget.text()
        if attr_type == "double":
            value = float(value)

        cmds.setAttr(node + "." + attr, value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _key_attr(self, field, node, attr, *args):
        """
        Keys the given attribute on the given node.

        :param field: The lineEdit to modify the stylesheet to show the attribute has a keyframe.
        :param node: The settings node.
        :param attr: The attribute to key.
        """

        cmds.setKeyframe(node + "." + attr)
        field.setStyleSheet(keys)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def key_all_settings(self):
        """
        Keys all setting attributes on all modules.
        """

        cmds.setKeyframe(self.character + ":rig_settings")

        for each in self.fields:
            each.setStyleSheet(keys)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def select_settings(self):
        """
        Selects the uber settings node.
        """

        cmds.select(self.character + ":rig_settings")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _collapse_group(self, widget, width, height, *args):
        """
        Collapses the groupbox, or expands the groupbox, depending on the check state.

        :param widget: the groupBox widget
        :param width: the width to set
        :param height: the max height to set.
        """

        if widget.isChecked():
            widget.setMinimumSize(QtCore.QSize(width, height))
            widget.setMaximumSize(QtCore.QSize(width, height))
        else:
            widget.setMinimumSize(QtCore.QSize(width, 20))
            widget.setMaximumSize(QtCore.QSize(width, 20))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_modules(self):
        """
        Finds all rig modules of the active character.

        :return: Returns a list of module names for the auto-completer.
        """

        index = self.animUI.characterTabs.currentIndex()
        character = self.animUI.characterTabs.tabToolTip(index)

        self.character = character
        self.setWindowTitle(character + " Rig Settings")

        returnData = []

        if cmds.objExists(character + ":" + "ART_RIG_ROOT"):
            modules = cmds.listConnections(character + ":" + "ART_RIG_ROOT.rigModules")
            for module in modules:
                modName = cmds.getAttr(module + ".moduleName")
                returnData.append(modName)

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_settings_nodes(self):
        """
        Find all module settings nodes for the active character.

        :return: Returns a list of pairs that contain the module name and the corresponding settings node.
        """

        index = self.animUI.characterTabs.currentIndex()
        character = self.animUI.characterTabs.tabToolTip(index)

        self.character = character
        self.setWindowTitle(character + " Rig Settings")

        returnData = []

        if cmds.objExists(character + ":" + "ART_RIG_ROOT"):
            modules = cmds.listConnections(character + ":" + "ART_RIG_ROOT.rigModules")
            for module in modules:
                modName = cmds.getAttr(module + ".moduleName")
                settings = character + ":" + modName + "_settings"
                if cmds.objExists(settings):
                    returnData.append([modName, settings])

        elif cmds.objExists("ART_RIG_ROOT"):
            modules = cmds.listConnections("ART_RIG_ROOT.rigModules")
            for module in modules:
                modName = cmds.getAttr(module + ".moduleName")
                settings = modName + "_settings"
                if cmds.objExists(settings):
                    returnData.append([modName, settings])

        return returnData

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _update_fields(self):
        """
        Updates the lineEdits when the time changes to show the correct values based on the actual attributes.
        """
        for widget in self.fields:
            node = widget.property("setting")
            attr = widget.property("attr")

            ct = cmds.currentTime(q=True)
            currentVal = cmds.getAttr(node + "." + attr, t=ct)
            keyframes = cmds.keyframe(node, at=attr, q=True, tc=True)
            currentVal = "%.3f" % currentVal
            widget.setText(str(currentVal))

            if keyframes is not None:
                if ct in keyframes:
                    widget.setProperty("keys", True)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                else:
                    widget.setProperty("keys", False)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def search(self):
        """
        Hides or shows groupboxes depending on whether any of the groupbox titles match the search terms.
        """

        search_text = self.searchBar.text()

        for each in self.groups:
            group = self.groups.get(each)
            if each.find(search_text) == -1:
                group.setMinimumHeight(0)
                group.setMaximumHeight(0)

            else:
                height = group.property("max")
                group.setMinimumHeight(height)
                group.setMaximumHeight(height)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run(animUI):
    """
    Deletes the UI if it exists, then instatiates the class, building the tool and the UI.
    :return: the instance of this tool
    """

    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, wnd=True)

    gui = ART_RigSettingsUI(animUI, interfaceUtils.getMainWindow())
    gui.show()
    return gui
