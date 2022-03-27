# import statements
import maya.cmds as cmds
import os
from functools import partial
import json

import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# load stylesheet
settings = QtCore.QSettings("Epic Games", "ARTv2")
toolsPath = settings.value("toolsPath")
artv2_style = interfaceUtils.get_style_sheet("artv2_style")


class ART_ScriptEditor(QtWidgets.QDialog):
    """
    Class that creates a simple widget for writing a script in mel or python, similar to Maya's shelf editor script
    window.

    It then stores the script contents and type in a property.

    """
    def __init__(self, animInst, text, parent=None):
        """
        Initialize the class, getting the settings, and calling on buildUI

        :param animInst: Instance of class that called on this class
        :param text: Existing script contents (if any)
        :param parent: Parent widget
        """

        super(ART_ScriptEditor, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")
        self.animInst = animInst

        self.existingText = text
        self.script_type = "python"
        self.script = ""

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
        Build the simple script editor widget.
        """

        # create the main widget
        self.mainWidget = QtWidgets.QFrame(self)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        # stylesheet
        self.style = artv2_style
        self.setStyleSheet(self.style)

        self.setMinimumSize(QtCore.QSize(400, 500))
        self.setMaximumSize(QtCore.QSize(400, 500))
        self.resize(400, 500)

        # set qt object name
        self.setWindowTitle("Script Editor")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # add script type layout
        layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(layout)

        label = QtWidgets.QLabel("Script Type:")
        layout.addWidget(label)

        self.scriptType = QtWidgets.QButtonGroup()
        self.mel_button = QtWidgets.QRadioButton("mel")
        layout.addWidget(self.mel_button)
        self.mel_button.setChecked(False)

        self.py_button = QtWidgets.QRadioButton("python")
        layout.addWidget(self.py_button)
        self.py_button.setChecked(True)

        self.scriptType.addButton(self.mel_button, 1)
        self.scriptType.addButton(self.py_button, 2)

        # text edit
        self.editor = QtWidgets.QTextEdit()
        self.editor.setMinimumSize(QtCore.QSize(380, 420))
        self.editor.setMaximumSize(QtCore.QSize(380, 420))
        self.layout.addWidget(self.editor)
        self.editor.setText(self.existingText)

        # save and close
        button = QtWidgets.QPushButton("Save and Close")
        button.setObjectName("settings")
        button.setMinimumHeight(30)
        self.layout.addWidget(button)
        button.clicked.connect(self.saveAndClose)

        # restore window position
        settings = QtCore.QSettings("ARTv2", "ScriptEditor")
        self.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):
        """
        override close event to save window positions.
        """

        self.settings = QtCore.QSettings("ARTv2", "ScriptEditor")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def saveAndClose(self):
        """
        Store the script type and script contents into some class variables. Close the widget.
        """

        scriptType = self.scriptType.checkedButton()
        self.script_type = scriptType.text()
        self.script = self.editor.toPlainText()
        self.accept()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_AddCustomButton(QtWidgets.QMainWindow):
    """
    Class that adds custom selection buttons, script buttons, or labels to the animation picker. This class handles
    building the interface to create those objects, and the functions for creating and adding them to the picker.
    """

    def __init__(self, animInst, parent=None):
        """
        Instantiate the class, getting the QSettings and building the UI
        :param animInst: Animation UI instance
        :param parent: parent widget (usually maya window)
        """

        super(ART_AddCustomButton, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")
        self.animInst = animInst

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
        Populates the main window with all the widgets necessary to add our custom selection, script, or label objects
        to the picker.
        """

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        self.setMinimumSize(QtCore.QSize(315, 395))
        self.setMaximumSize(QtCore.QSize(315, 395))
        self.resize(315, 395)

        # set qt object name
        self.setObjectName("pyART_AddCustomButtonToPickerWIN")
        self.setWindowTitle("Add Custom Picker Object")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Button type
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        type_group = QtWidgets.QGroupBox("Type")
        type_group.setMinimumSize(QtCore.QSize(294, 49))
        type_group.setMaximumSize(QtCore.QSize(294, 49))
        self.layout.addWidget(type_group)

        button_type_layout = QtWidgets.QHBoxLayout(type_group)

        self.button_type_group = QtWidgets.QButtonGroup()
        self.selection_button = QtWidgets.QRadioButton("Selection Button")
        button_type_layout.addWidget(self.selection_button)
        self.selection_button.setChecked(True)

        self.script_button = QtWidgets.QRadioButton("Script Button")
        button_type_layout.addWidget(self.script_button)

        self.label_object = QtWidgets.QRadioButton("Label")
        button_type_layout.addWidget(self.label_object)

        self.button_type_group.addButton(self.selection_button, 1)
        self.button_type_group.addButton(self.script_button, 2)
        self.button_type_group.addButton(self.label_object, 3)

        self.button_type_group.buttonClicked.connect(self.changeType)

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Options group
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        options_group = QtWidgets.QGroupBox("Options")
        options_group.setMinimumSize(QtCore.QSize(294, 226))
        options_group.setMaximumSize(QtCore.QSize(294, 226))

        self.layout.addWidget(options_group)
        stack_layout = QtWidgets.QVBoxLayout(options_group)

        self.options_stack = QtWidgets.QStackedWidget()
        stack_layout.addWidget(self.options_stack)
        self.options_stack.setMinimumSize(QtCore.QSize(272, 200))
        self.options_stack.setMaximumSize(QtCore.QSize(272, 200))

        self.build_selection_options()
        self.build_label_options()

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Tab Layout
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        tab_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(tab_layout)

        label = QtWidgets.QLabel("Add to Tab:")
        tab_layout.addWidget(label)

        self.tab_comboBox = QtWidgets.QComboBox()
        self.tab_comboBox.setObjectName("light")
        tab_layout.addWidget(self.tab_comboBox)

        # get tabs
        index = self.animInst.characterTabs.currentIndex()
        widget = self.animInst.characterTabs.widget(index)

        # get the children of the current tab widget
        children = widget.children()
        for child in children:

            # if we find a tab widget, search for the gfxScene
            if type(child) == QtWidgets.QTabWidget:
                tab = child
                for i in range(tab.count()):
                    tab.setCurrentIndex(i)
                    canvasIndex = tab.currentIndex()
                    canvasWidget = tab.widget(canvasIndex)
                    canvasChildren = canvasWidget.children()

                    for canvasChild in canvasChildren:
                        if type(canvasChild) == QtWidgets.QGraphicsView:
                            view = canvasChild
                            scene = view.scene()

                            self.tab_comboBox.addItem(tab.tabText(i))
                            self.tab_comboBox.setItemData(i, scene)

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Add Button
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        add_button = QtWidgets.QPushButton("Add")
        add_button.setObjectName("settings")
        add_button.setMinimumHeight(30)
        add_button.clicked.connect(partial(self.add_custom_object))
        self.layout.addWidget(add_button)

        # restore window position
        settings = QtCore.QSettings("ARTv2", "AddCustomPickerObj")
        self.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):
        """
        Override close event to store window positions.
        """

        self.settings = QtCore.QSettings("ARTv2", "AddCustomPickerObj")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def build_label_options(self):
        """
        Builds the widget for creating a custom label object to add to the animation picker.
        """

        self.label_options = QtWidgets.QFrame()
        self.label_options.setObjectName("lightnoborder")
        self.label_options.setMinimumSize(QtCore.QSize(272, 200))
        self.label_options.setMaximumSize(QtCore.QSize(272, 200))

        main_layout = QtWidgets.QVBoxLayout(self.label_options)

        color_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(color_layout)

        label = QtWidgets.QLabel("Text Color: ")
        self.label_color_button = QtWidgets.QPushButton()
        self.label_color_button.setMinimumSize(QtCore.QSize(30, 30))
        self.label_color_button.setMaximumSize(QtCore.QSize(30, 30))
        self.label_color_button.setObjectName("tool")
        self.label_color_button.setContentsMargins(1, 1, 1, 1)

        self.label_color_swatch = QtWidgets.QLabel(self.label_color_button)
        self.label_color_swatch.setMinimumSize(QtCore.QSize(28, 28))
        self.label_color_swatch.setMaximumSize(QtCore.QSize(28, 28))
        self.label_color_swatch.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_color_swatch.setProperty("rgb", [255, 255, 255])
        self.label_color_button.clicked.connect(partial(self.set_color, self.label_color_swatch))

        color_layout.addWidget(label)
        color_layout.addWidget(self.label_color_button)

        main_layout.addWidget(QtWidgets.QLabel("Text: "))

        self.label_text_field = QtWidgets.QLineEdit()
        main_layout.addWidget(self.label_text_field)

        spacer = QtWidgets.QSpacerItem(10, 100, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        self.options_stack.addWidget(self.label_options)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def build_selection_options(self):
        """
        Builds the widget for creating selection buttons, either with a solid color or an icon AND creating script
        buttons. All widgets for both are created, and their visibility is toggled depending on which object the user
        is trying to create.
        """

        self.selection_options = QtWidgets.QFrame()
        self.selection_options.setObjectName("lightnoborder")
        self.selection_options.setMinimumSize(QtCore.QSize(272, 200))
        self.selection_options.setMaximumSize(QtCore.QSize(272, 200))

        main_layout = QtWidgets.QVBoxLayout(self.selection_options)

        # top section (button style)
        top_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(top_layout)

        color_label = QtWidgets.QLabel("Button Style:")
        color_label.setMinimumWidth(75)
        color_label.setMaximumWidth(75)
        self.selection_button_combo = QtWidgets.QComboBox()
        self.selection_button_combo.addItem("Color")
        self.selection_button_combo.addItem("Icon")
        self.selection_button_combo.currentIndexChanged.connect(self.update_button_style)

        self.selection_color_button = QtWidgets.QPushButton()
        self.selection_color_button.setMinimumSize(QtCore.QSize(30, 30))
        self.selection_color_button.setMaximumSize(QtCore.QSize(30, 30))
        self.selection_color_button.setObjectName("tool")
        self.selection_color_button.setContentsMargins(1, 1, 1, 1)

        self.color_swatch = QtWidgets.QLabel(self.selection_color_button)
        self.color_swatch.setMinimumSize(QtCore.QSize(28, 28))
        self.color_swatch.setMaximumSize(QtCore.QSize(28, 28))
        self.color_swatch.setStyleSheet("background-color: rgb(82, 67, 155);")
        self.color_swatch.setProperty("rgb", [82, 67, 155])
        self.selection_color_button.clicked.connect(partial(self.set_color, self.color_swatch))

        self.icon_swatch = QtWidgets.QLabel(self.selection_color_button)
        self.icon_swatch.setMinimumSize(QtCore.QSize(28, 28))
        self.icon_swatch.setMaximumSize(QtCore.QSize(28, 28))
        self.selection_button_icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/select_set.png"))
        self.icon_swatch.setPixmap(self.selection_button_icon.pixmap(28))
        self.icon_swatch.setProperty("icon", True)
        self.icon_swatch.setVisible(False)

        top_layout.addWidget(color_label)
        top_layout.addWidget(self.selection_button_combo)
        top_layout.addWidget(self.selection_color_button)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # optional label section
        mid_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(mid_layout)

        self.selection_label_cb = QtWidgets.QCheckBox("Add Label")

        self.selection_label = QtWidgets.QLineEdit()
        self.selection_label.setPlaceholderText("Enter a label..")
        self.selection_label.setEnabled(False)

        self.selection_label_pos = QtWidgets.QComboBox()
        self.selection_label_pos.setEnabled(False)
        for each in ["top", "bottom", "center", "left", "right"]:
            self.selection_label_pos.addItem(each)

        mid_layout.addWidget(self.selection_label_cb)
        mid_layout.addWidget(self.selection_label)
        mid_layout.addWidget(self.selection_label_pos)

        self.selection_label_cb.stateChanged.connect(partial(self.toggle_label, self.selection_label_cb,
                                                             self.selection_label, self.selection_label_pos))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # selection section

        self.button_label = QtWidgets.QLabel("Selection:")
        main_layout.addWidget(self.button_label)

        selection_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(selection_layout)

        self.selection_text = QtWidgets.QTextEdit()
        self.selection_text.setMinimumSize(QtCore.QSize(205, 100))
        self.selection_text.setMaximumSize(QtCore.QSize(205, 100))
        self.selection_text.setEnabled(False)
        self.selection_text.setText("Use the button on the side to add your selection for this button.")
        selection_layout.addWidget(self.selection_text)

        self.add_selection_button = QtWidgets.QPushButton("<<")
        self.add_selection_button.setMinimumSize(QtCore.QSize(40, 100))
        self.add_selection_button.setMaximumSize(QtCore.QSize(40, 100))
        self.add_selection_button.setObjectName("settings")
        selection_layout.addWidget(self.add_selection_button)
        self.add_selection_button.clicked.connect(self.set_selection)

        self.selection_spacer = QtWidgets.QSpacerItem(10, 100, QtWidgets.QSizePolicy.Fixed,
                                                      QtWidgets.QSizePolicy.Expanding)
        main_layout.addItem(self.selection_spacer)

        self.create_script_button = QtWidgets.QPushButton("Write Script")
        self.create_script_button.setObjectName("settings")
        self.create_script_button.setMinimumHeight(30)
        self.create_script_button.setVisible(False)
        main_layout.addWidget(self.create_script_button)
        self.create_script_button.clicked.connect(self.launchScriptEditor)

        self.options_stack.addWidget(self.selection_options)
        self.options_stack.setCurrentWidget(self.selection_options)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def choose_icon(self, label):
        """
        Builds a simple widget that shows all icons created for ARTv2 and allows the user to pick an icon for their
        custom button object (script or selection button).

        :param label: This is a QLabel that is a child of the main QPushButton that holds the icon image.
        """

        # get icons available to us
        dir = utils.returnNicePath(self.iconsPath, "System")
        icons = []

        for each in os.listdir(dir):
            if os.path.splitext(utils.returnNicePath(dir, each))[1] == ".png":
                if each.find("noIcon") == -1:
                    icons.append(utils.returnNicePath(dir, each))

        # create a basic widget using QDialog
        widget = QtWidgets.QDialog(self)
        main_layout = QtWidgets.QVBoxLayout(widget)
        widget.setWindowTitle("Choose Icon")
        widget.setMinimumWidth(280)
        widget.setMaximumWidth(280)

        # Create a grid layout with 5 columns to store the icons found
        columns = 5
        layout = QtWidgets.QGridLayout()

        # Need to create a scroll area so that the widget can hold as many icons as there are without compromising
        # window size.
        contents = QtWidgets.QFrame()
        scrollArea = QtWidgets.QScrollArea()
        main_layout.addWidget(scrollArea)

        # loop through our icon files and add them to the grid layout as qpushbuttons.
        count = 0
        for i in icons:
            btn = QtWidgets.QPushButton()
            icon = QtGui.QIcon(i)
            btn.setIconSize(QtCore.QSize(28, 28))
            btn.setIcon(icon)
            btn.setObjectName("tool")
            btn.setProperty("path", i)
            btn.clicked.connect(partial(self.set_icon, btn, label, widget))
            layout.addWidget(btn, count / columns, count % columns)
            count += 1

        # add the grid layout to the scroll area
        contents.setLayout(layout)
        scrollArea.setWidget(contents)

        # Add a cancel button
        button = QtWidgets.QPushButton("Cancel / No Icon")
        button.setObjectName("settings")
        button.setMinimumHeight(30)
        button.clicked.connect(partial(self.set_icon, button, label, widget, True))
        main_layout.addWidget(button)

        widget.exec_()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def set_icon(self, button, label, widget, cancel=False):
        """
        Called on by self.choose_icon to set the QLabel to the chosen icon image.
        :param button: The button that the user pressed that holds the icon they wanted
        :param label: The QLabel that the icon will be presented on
        :param widget: The QDialog to close
        :param cancel: Whether or not Cancel was chosen

        .. seealso:: choose_icon
        """

        if cancel is False:
            icon = button.icon()
            img_path = button.property("path")
            label.setPixmap(icon.pixmap(28))
            label.setProperty("icon", True)
            label.setProperty("path", img_path)
            widget.accept()

        if cancel is True:
            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/select_set.png"))
            label.setPixmap(icon.pixmap(28))
            label.setProperty("icon", True)
            widget.accept()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def set_color(self, label):
        """
        Present a QColorDialog and set the QLabel stylesheet to the chose color.
        :param label: the QLabel that is a child of the QPushButton. It displays the chosen color.
        """

        colorDialog = QtWidgets.QColorDialog.getColor()
        color = colorDialog.getRgb()
        red = float(color[0])
        green = float(color[1])
        blue = float(color[2])

        label.setProperty("rgb", [red, green, blue])
        label.setStyleSheet("background-color: rgb(" + str(red) + ", " + str(green) + ", " + str(blue) + ");")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def set_selection(self):
        """
        Dumps the current selection as text to the text edit widget for custom selection buttons.
        """

        selection = cmds.ls(sl=True)
        self.selection_text.setText(json.dumps(selection))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_button_style(self):
        """
        Depending on whether the selection button is set to "color" or "icon", determines the functionality of the
        QPushButton. If the style is set to 0 (color button), then we pull up a QColorDialog and set the label color.
        If the style is set to 1 (icon button), then we pull up choose_icon and set the label icon.
        .. seealso:: choose_icon
        """

        if self.selection_button_combo.currentIndex() == 0:
            self.icon_swatch.setVisible(False)
            self.color_swatch.setVisible(True)
            self.selection_color_button.clicked.disconnect()
            self.selection_color_button.clicked.connect(partial(self.set_color, self.color_swatch))

        if self.selection_button_combo.currentIndex() == 1:
            self.icon_swatch.setVisible(True)
            self.color_swatch.setVisible(False)
            self.selection_color_button.clicked.disconnect()
            self.selection_color_button.clicked.connect(partial(self.choose_icon, self.icon_swatch))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggle_label(self, checkBox, lineEdit, comboBox, *args):
        """
        If the user wants to add a label to a selection or script button, they press a checkbox. That then calls on
        this, which checks the value of that checkbox, and enables or disables the label option widgets depending.

        :param checkBox: "Add Label" checkbox to check state
        :param lineEdit: Label QLineEdit that holds label text. Set to either enable or disable depending on state
        :param comboBox: Label positioning options. Enable or disable depending on state.
        """

        if checkBox.isChecked():
            lineEdit.setEnabled(True)
            comboBox.setEnabled(True)
        else:
            lineEdit.setEnabled(False)
            comboBox.setEnabled(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeType(self, *args):
        """
        Called on when the user changes the custom object type to either selection button or script button. Since both
        button types use the same widget, and just toggle visibility on certain child widgets, this function toggles
        that visibility on those children depending on which QRadioButton is checked. If "label" is chosen, the
        stackWidget has its current index set to display the label widget instead.

        :param args:  radio button that is checked in button group
        """

        button = args[0]
        if button.text() == "Selection Button":
            self.options_stack.setCurrentWidget(self.selection_options)
            self.button_label.setVisible(True)
            self.selection_text.setVisible(True)
            self.add_selection_button.setVisible(True)
            self.create_script_button.setVisible(False)
            self.selection_button_combo.setCurrentIndex(0)
            self.selection_button_combo.setEnabled(True)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/noIcon.png"))
            self.icon_swatch.setPixmap(icon.pixmap(28))
            self.icon_swatch.setProperty("icon", False)

        if button.text() == "Script Button":
            self.options_stack.setCurrentWidget(self.selection_options)
            self.button_label.setVisible(False)
            self.selection_text.setVisible(False)
            self.add_selection_button.setVisible(False)
            self.create_script_button.setVisible(True)
            self.selection_button_combo.setCurrentIndex(1)
            self.selection_button_combo.setEnabled(False)

            icon = QtGui.QIcon(utils.returnNicePath(self.iconsPath, "System/file.png"))
            self.icon_swatch.setPixmap(icon.pixmap(28))
            self.icon_swatch.setProperty("icon", True)
            self.icon_swatch.setProperty("path", utils.returnNicePath(self.iconsPath, "System/file.png"))

        if button.text() == "Label":
            self.options_stack.setCurrentWidget(self.label_options)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def launchScriptEditor(self):
        """
        Create an instance of the ART_ScriptEditor class and then pull the script type and script contents from that
        instance. Set that data as properties on our "Write Script" button.
        """

        text = self.create_script_button.property("script")
        inst = ART_ScriptEditor(self, text)
        inst.exec_()

        self.create_script_button.setToolTip(inst.script)
        self.create_script_button.setProperty("script", inst.script)
        self.create_script_button.setProperty("type", inst.script_type)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def add_custom_object(self):
        """
        This handles adding the custom object type to the animation picker.
        :return:
        """
        objType = self.button_type_group.checkedId()

        # selection button
        if objType == 1:

            # get tab and scene to add to
            selected = self.tab_comboBox.currentIndex()
            scene = self.tab_comboBox.itemData(selected)

            # get style type
            style = self.selection_button_combo.currentIndex()

            # get button color
            color = self.color_swatch.property("rgb")

            # get button icon
            image = None
            path = ""
            if style == 1:
                icon = self.icon_swatch.property("icon")
                path = self.icon_swatch.property("path")
                if icon is True:
                    image = self.icon_swatch.pixmap()

            # get selection
            selection = json.loads(self.selection_text.toPlainText())

            brush = QtGui.QColor(color[0], color[1], color[2])
            clearBrush = QtGui.QBrush(QtCore.Qt.black)
            clearBrush.setStyle(QtCore.Qt.NoBrush)

            # create the border item that allows button to be moved, rotated, and scaled
            border = interfaceUtils.customBorderItem(10, 10, 48, 48, clearBrush, None)

            # create the selection button (either with color or icon)
            if style == 1:
                button = SelectionButton_Icon(28, 28, [10, 10], selection, path, image, border)
            if style == 0:
                button = SelectionButton_Color(28, 28, [10, 10], selection, brush, color, parent=border)

            # check to see if there is a label, if so, get info
            if self.selection_label_cb.isChecked():
                label = self.selection_label.text()
                position = self.selection_label_pos.currentText()
                Custom_Text_Item(label, position, customColor=None, parent=button)

                # set data for notifying that the button has a label associated with it
                button.setData(9, True)
                button.setData(10, label)
                button.setData(11, position)

            scene.addItem(border)

        # script button
        if objType == 2:
            # get tab and scene to add to
            selected = self.tab_comboBox.currentIndex()
            scene = self.tab_comboBox.itemData(selected)

            # get style type
            style = self.selection_button_combo.currentIndex()

            # get button icon
            image = None
            path = ""
            if style == 1:
                icon = self.icon_swatch.property("icon")
                path = self.icon_swatch.property("path")
                if icon is True:
                    image = self.icon_swatch.pixmap()

            # get script
            script = self.create_script_button.property("script")
            script_type = self.create_script_button.property("type")

            clearBrush = QtGui.QBrush(QtCore.Qt.black)
            clearBrush.setStyle(QtCore.Qt.NoBrush)

            # create the border item that allows button to be moved, rotated, and scaled
            border = interfaceUtils.customBorderItem(10, 10, 48, 48, clearBrush, None)

            # create the button that executes the script
            button = ScriptButton_Icon(28, 28, [10, 10], script, script_type, path, image, border)

            # check to see if there is a label, if so, get info
            if self.selection_label_cb.isChecked():
                label = self.selection_label.text()
                position = self.selection_label_pos.currentText()
                Custom_Text_Item(label, position, customColor=None, parent=button)

                # set data for notifying that the button has a label associated with it
                button.setData(9, True)
                button.setData(10, label)
                button.setData(11, position)

            scene.addItem(border)

        # label
        if objType == 3:
            # get tab and scene to add to
            selected = self.tab_comboBox.currentIndex()
            scene = self.tab_comboBox.itemData(selected)

            # add the text
            label_text = self.label_text_field.text()
            color = self.label_color_swatch.property("rgb")

            clearBrush = QtGui.QBrush(QtCore.Qt.black)
            clearBrush.setStyle(QtCore.Qt.NoBrush)

            # create the border item that allows button to be moved, rotated, and scaled
            border = interfaceUtils.customBorderItem(10, 10, 48, 48, clearBrush, None)

            # create the custom label object
            label = Custom_Text_Item(label_text, "center", color, border, True)
            label.setData(99, "label")
            label.setData(6, color)
            label.setData(10, label_text)
            scene.addItem(border)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Custom_Text_Item(QtWidgets.QGraphicsSimpleTextItem):
    """
    Class that makes the custom label object (from a QGraphicsSimpleTextItem). The main additions to this class is
    the context menu features and the positioning functions.
    """

    def __init__(self, text, position, customColor=None, parent=None, static=False):
        """
        Instantiate the class, setting the pen, brush, and position of the text. As well as building the menu and
        populating the menu with actions.

        :param text: The label text
        :param position: The label position (options are center, top, bottom, left, and right)
        :param customColor: The color of the text
        :param parent: The parent widget (border item)
        :param static: Whether or not this is a stand-alone label, or a label that accompanies a button. (True = solo)
        """
        super(Custom_Text_Item, self).__init__(text, parent)
        self.static = static

        # Set the pen and the brush for the label
        self.setPen(QtGui.QPen(QtCore.Qt.transparent))
        if customColor is None:
            self.setBrush(QtGui.QBrush(QtCore.Qt.white))
        else:
            self.setBrush(QtGui.QBrush(QtGui.QColor(customColor[0], customColor[1], customColor[2])))

        # Set the font
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)

        # Set the position of the label. (Only used when label accompanies a button. Otherwise defaults to center)
        textPos = parent.boundingRect().center()
        textRect = self.boundingRect()
        parentRect = parent.boundingRect()

        if position == "center":
            self.setPos(textPos.x() - textRect.width() / 2, textPos.y() - textRect.height() / 2)

        if position == "top":
            self.setPos(textPos.x() - textRect.width() / 2, textPos.y() - (parentRect.height() / 2 + textRect.height()))

        if position == "bottom":
            self.setPos(textPos.x() - textRect.width() / 2, textPos.y() + (parentRect.height() / 2))

        if position == "right":
            self.setPos((textPos.x() * 2) + 2, textPos.y() - (parentRect.height() / 2))

        if position == "left":
            self.setPos((textRect.width() + 2) * -1, textPos.y() - (parentRect.height() / 2))

        # build a menu
        self.menu = QtWidgets.QMenu()

        # menu icons
        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.iconsPath = settings.value("iconPath")

        remove = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/removeModule.png"))))
        label = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/edit.png"))))

        # add right click menu to select settings
        self.menu.addAction(remove, "Remove", self.remove_item)
        self.menu.addAction(label, "Edit Label", self.edit_label)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        """
        Calls on the QMenu to display
        """

        self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def remove_item(self):
        """
        Remove the label from the animation picker.
        """

        scene = self.scene()
        parent = self.parentItem()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Delete label from picker?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        ret = msgBox.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            scene.removeItem(parent)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_label(self):
        """
        Launch a QDialog that asks for label text and label position (position only if static = False)
        """

        # Get information from the QDialog
        returnData = self.edit_label_UI(self.text())

        # Edit the label
        self.setText(returnData[0])

        # If the label can be positioned, set the position now
        if self.static is False:
            textPos = self.boundingRect().center()
            textRect = self.boundingRect()
            parentRect = self.boundingRect()

            if returnData[1] == "center":
                self.setPos(textPos.x() - textRect.width() / 2, textPos.y() - textRect.height() / 2)

            if returnData[1] == "top":
                self.setPos(textPos.x() - textRect.width() / 2, textPos.y() -
                                     (parentRect.height() / 2 + textRect.height()))

            if returnData[1] == "bottom":
                self.setPos(textPos.x() - textRect.width() / 2, textPos.y() + (parentRect.height() / 2))

            if returnData[1] == "right":
                self.setPos((textPos.x() * 2) + 2, textPos.y() - (parentRect.height() / 2))

            if returnData[1] == "left":
                self.setPos((textRect.width() + 2) * -1, textPos.y() - (parentRect.height() / 2))

        # set HasLabel to True, and label text data
        self.setData(9, True)
        self.setData(10, returnData[0])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_label_UI(self, text=None):
        """
        The QDialog widget that edit_label launches. Asks for new label text and label position
        (if self.static is False)

        :param text: Existing label text (if any)
        :return: list. Label text and label position (both strings)
        """

        # Create the QDialog, size it
        dialog = QtWidgets.QDialog()
        dialog.setMinimumSize(QtCore.QSize(300, 140))
        dialog.setMaximumSize(QtCore.QSize(300, 140))
        dialog.resize(300, 140)

        # create the main layout and the first row layout
        layout = QtWidgets.QVBoxLayout(dialog)
        layout_1 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_1)

        # First row widgets: Gets label text
        layout_1.addWidget(QtWidgets.QLabel("Label Text:"))
        self.label_lineEdit = QtWidgets.QLineEdit()
        if text is not None:
            self.label_lineEdit.setText(text)
        layout_1.addWidget(self.label_lineEdit)

        # Second row widgets: Gets label position
        layout_2 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_2)

        if self.static is False:
            layout_2.addWidget(QtWidgets.QLabel("Label Position:"))
            self.labelPosition = QtWidgets.QComboBox()
            for each in ["top", "bottom", "center", "left", "right"]:
                self.labelPosition.addItem(each)
            layout_2.addWidget(self.labelPosition)

        # Last row: Cancel or Accept buttons
        layout_3 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_3)

        cancel = QtWidgets.QPushButton("Cancel")
        layout_3.addWidget(cancel)
        accept = QtWidgets.QPushButton("Accept")
        layout_3.addWidget(accept)
        cancel.clicked.connect(dialog.reject)
        accept.clicked.connect(dialog.accept)

        # launch the dialog
        ret = dialog.exec_()

        # if accept, get the text and append to return data. If self.static is False, also get position and append
        if ret == 1:
            text = self.label_lineEdit.text()
            returnData = [text]

            if self.static is False:
                pos = self.labelPosition.currentText()
                returnData.append(pos)

            return returnData


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Custom_Button_Item(QtWidgets.QGraphicsItem):
    """
    Base class for creating custom picker buttons with a single fill color. Extends QGraphicsItem by adding context
    menu functions for editing button.
    """

    def __init__(self, width, height, relativePos, parent=None):
        """
        Instantiate the class, setting class variables, geting settings, and creating context menu
        :param width: button width
        :param height: button height
        :param relativePos: relative position from parent widget
        :param parent: parent widget (usually customBorderItem)
        """
        super(Custom_Button_Item, self).__init__(parent)

        # set the parent depth to be behind self.
        if parent is not None:
            self.parentItem().setZValue(1)
        self.setZValue(2)

        # set class variables
        self.width = width
        self.height = height
        self.relativePos = relativePos

        # create a menu for the context menu
        self.menu = QtWidgets.QMenu()

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.iconsPath = settings.value("iconPath")

        # menu icons
        remove = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/removeModule.png"))))
        color = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/moduleList.png"))))
        selection = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select_set.png"))))
        label = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/edit.png"))))

        # add right click menu to select settings
        self.menu.addAction(remove, "Remove", self.remove_item)
        self.menu.addAction(color, "Edit Button Color", self.edit_color)
        self.menu.addAction(label, "Edit Label", self.edit_label)
        self.menu.addAction(selection, "Edit Selection Set", self.edit_selection_UI)

        # set position
        if parent is not None:
            self.setPos(self.parentItem().boundingRect().topLeft())

        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def remove_item(self):
        """
        Removes the custom button item from the animation picker
        """

        scene = self.scene()
        parent = self.parentItem()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Delete button from picker?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        ret = msgBox.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            scene.removeItem(parent)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_color(self):
        """
        Launches a QColorDialog that allows the user to choose a different color for the button.
        """

        colorDialog = QtWidgets.QColorDialog.getColor()
        color = colorDialog.getRgb()
        red = float(color[0])
        green = float(color[1])
        blue = float(color[2])

        self.brush = QtGui.QBrush(QtGui.QColor(red, green, blue))
        self.update()
        self.setData(6, color)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_label(self):
        """
        Launch a QDialog to edit the label text and label position. Then apply those edits.
        """

        # Determine if there is an existing label to edit under the button
        childItems = self.childItems()

        # if there is, launch the dialog passing in the button's text so the QLineEdit is prefilled
        if len(childItems) > 0:
            text = childItems[0].text()
            returnData = self.edit_label_UI(text)

        # if there is not an existing label, simply launch the dialog
        else:
            returnData = self.edit_label_UI()

        # If there was an existing label, set its text and position
        if len(childItems) > 0:
            childItems[0].setText(returnData[0])

            textPos = self.boundingRect().center()
            textRect = childItems[0].boundingRect()
            parentRect = self.boundingRect()

            if returnData[1] == "center":
                childItems[0].setPos(textPos.x() - textRect.width() / 2, textPos.y() - textRect.height() / 2)

            if returnData[1] == "top":
                childItems[0].setPos(textPos.x() - textRect.width() / 2, textPos.y() -
                                     (parentRect.height() / 2 + textRect.height()))

            if returnData[1] == "bottom":
                childItems[0].setPos(textPos.x() - textRect.width() / 2, textPos.y() + (parentRect.height() / 2))

            if returnData[1] == "right":
                childItems[0].setPos((textPos.x() * 2) + 2, textPos.y() - (parentRect.height() / 2))

            if returnData[1] == "left":
                childItems[0].setPos((textRect.width() + 2) * -1, textPos.y() - (parentRect.height() / 2))

        # If there was not, add a label now
        else:
            Custom_Text_Item(returnData[0], returnData[1], customColor=None, parent=self)

        self.setData(9, True)
        self.setData(10, returnData[0])
        self.setData(11, returnData[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_selection(self, dialog):
        """
        Sets the internal data to the new selection set by loading the text from the text edit
        :param dialog: The QDialog to close once operation is complete
        """

        self.objects = json.loads(self.label_selection.toPlainText())
        self.setData(5, self.objects)
        dialog.accept()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_label_UI(self, text=None):
        """
        QDialog widget that allows user to edit label text and label position.
        :param text: Existing label text (if any)
        :return: List. New label text and new label position. Both strings
        """

        # Create the QDialog
        dialog = QtWidgets.QDialog()
        dialog.setMinimumSize(QtCore.QSize(300, 140))
        dialog.setMaximumSize(QtCore.QSize(300, 140))
        dialog.resize(300, 140)

        # Set stylesheet
        dialog.setStyleSheet(artv2_style)

        # Create the main layout and then add a new row layout
        layout = QtWidgets.QVBoxLayout(dialog)
        layout_1 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_1)

        # First row widgets: Label text inputs
        layout_1.addWidget(QtWidgets.QLabel("Label Text:"))
        self.label_lineEdit = QtWidgets.QLineEdit()
        if text is not None:
            self.label_lineEdit.setText(text)
        layout_1.addWidget(self.label_lineEdit)

        # Create a second row layout
        layout_2 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_2)

        # Second row widgets: Label position inputs
        layout_2.addWidget(QtWidgets.QLabel("Label Position:"))
        self.labelPosition = QtWidgets.QComboBox()
        for each in ["top", "bottom", "center", "left", "right"]:
            self.labelPosition.addItem(each)
        layout_2.addWidget(self.labelPosition)

        # Create a third row layout for cancel and accept button
        layout_3 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_3)

        cancel = QtWidgets.QPushButton("Cancel")
        cancel.setObjectName("settings")
        layout_3.addWidget(cancel)

        accept = QtWidgets.QPushButton("Accept")
        accept.setObjectName("settings")
        layout_3.addWidget(accept)
        cancel.clicked.connect(dialog.reject)
        accept.clicked.connect(dialog.accept)

        # launch the dialog and capture the data to return
        ret = dialog.exec_()
        if ret == 1:

            text = self.label_lineEdit.text()
            pos = self.labelPosition.currentText()
            return [text, pos]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_selection_UI(self):
        """
        Creates a simple QDialog widget that allows user to load current selection into the text edit (as json data)
        """

        # Create the QDialog
        dialog = QtWidgets.QDialog(interfaceUtils.getMainWindow())
        dialog.setMinimumSize(QtCore.QSize(300, 300))
        dialog.setMaximumSize(QtCore.QSize(300, 300))
        dialog.resize(300, 300)

        # Set stylesheet
        dialog.setStyleSheet(artv2_style)

        # Create the main layout and add a first row
        layout = QtWidgets.QVBoxLayout(dialog)
        layout_1 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_1)

        # First row widgets: Text Edit and QPushButton that loads selection into text edit as json data
        self.label_selection = QtWidgets.QTextEdit()
        self.label_selection.setMinimumSize(QtCore.QSize(240, 240))
        self.label_selection.setMaximumSize(QtCore.QSize(240, 240))
        self.label_selection.setEnabled(False)
        self.label_selection.setText(json.dumps(self.objects))
        layout_1.addWidget(self.label_selection)

        button = QtWidgets.QPushButton("<<")
        button.setObjectName("settings")
        button.setMinimumSize(QtCore.QSize(30, 240))
        button.setMaximumSize(QtCore.QSize(30, 240))
        layout_1.addWidget(button)
        button.clicked.connect(self.set_selection)

        # Second row widgets: Accept and cancel buttons
        layout_2 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_2)

        cancel = QtWidgets.QPushButton("Cancel")
        cancel.setObjectName("settings")
        layout_2.addWidget(cancel)
        accept = QtWidgets.QPushButton("Accept")
        accept.setObjectName("settings")
        layout_2.addWidget(accept)
        cancel.clicked.connect(dialog.reject)
        accept.clicked.connect(partial(self.edit_selection, dialog))

        # Show the dialog
        dialog.setModal(False)
        dialog.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def set_selection(self):
        """
        Takes the current selection and dumps it as json data into the textEdit
        """

        selection = cmds.ls(sl=True)
        self.label_selection.setText(json.dumps(selection))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_icon(self):
        """
        Launches a widget that allows user to choose a new button icon. If a new icon is chosen, the button icon is
        updated.
        """

        returnData = self.edit_icon_UI()

        if returnData is not None:
            image = returnData.property("path")
            self.image = QtWidgets.QPixmap(image)
            self.setPixmap(self.image.scaled(28, 28))
            self.setData(8, image)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_icon_UI(self):
        """
        Builds a simple widget that shows all icons created for ARTv2 and allows the user to pick an icon for their
        custom button object.
        """

        # Get all available icons
        dir = utils.returnNicePath(self.iconsPath, "System")
        icons = []

        for each in os.listdir(dir):
            if os.path.splitext(utils.returnNicePath(dir, each))[1] == ".png":
                if each.find("noIcon") == -1:
                    icons.append(utils.returnNicePath(dir, each))

        # Create the QDialog
        widget = QtWidgets.QDialog()
        main_layout = QtWidgets.QVBoxLayout(widget)
        widget.setWindowTitle("Choose Icon")
        widget.setMinimumWidth(280)
        widget.setMaximumWidth(280)

        widget.setStyleSheet(artv2_style)

        # Create a grid layout with 5 columns
        columns = 5
        layout = QtWidgets.QGridLayout()

        # Create the scroll area that will be able to hold as many icons as there are.
        contents = QtWidgets.QFrame()
        scrollArea = QtWidgets.QScrollArea()
        main_layout.addWidget(scrollArea)

        # Cancel and accept buttons
        cancel = QtWidgets.QPushButton("Cancel")
        cancel.setObjectName("settings")
        cancel.setMinimumHeight(30)
        cancel.clicked.connect(widget.reject)

        accept = QtWidgets.QPushButton("Accept")
        accept.setObjectName("settings")
        accept.setMinimumHeight(30)
        accept.clicked.connect(widget.accept)

        # For each icon, create a qpushbutton with the icon as the button icon, and add it to the grid layout
        count = 0
        for i in icons:
            btn = QtWidgets.QPushButton()
            icon = QtGui.QIcon(i)
            btn.setIconSize(QtCore.QSize(28, 28))
            btn.setIcon(icon)
            btn.setObjectName("tool")
            btn.setProperty("path", i)
            btn.clicked.connect(partial(self.icon_chosen, btn, accept, widget))
            layout.addWidget(btn, count / columns, count % columns)
            count += 1

        # add the grid layout to the scroll area
        contents.setLayout(layout)
        scrollArea.setWidget(contents)

        # add the rest of the widgets
        button_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout)
        button_layout.addWidget(cancel)
        button_layout.addWidget(accept)

        # launch the dialog
        ret = widget.exec_()

        if ret == 1:
            return accept

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def icon_chosen(self, icon, button, dialog):
        path = icon.property("path")
        button.setProperty("path", path)
        dialog.accept()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SelectionButton_Color(Custom_Button_Item):
    """
    Inherits from Custom Button Item and adds functionality for button press and paint functions
    """

    def __init__(self, width, height, relativePos, controlObjects, brush, rgb, parent=None):
        """
        Instantiates the class, set button data

        :param width: button width
        :param height: button height
        :param relativePos: relative position from parent widget
        :param controlObjects: the objects the button will select
        :param brush: the color of the button
        :param rgb: the rgb values
        :param parent: the parent widget
        """

        super(SelectionButton_Color, self).__init__(width, height, relativePos, parent)

        self.brush = QtGui.QBrush(brush)
        self.brushColor = brush
        self.objects = controlObjects

        self.setData(99, "selection")
        self.setData(5, self.objects)
        self.setData(6, rgb)
        self.setData(7, 0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paint(self, painter, option, widget):
        rec = self.boundingRect()

        blackPen = QtGui.QPen(QtCore.Qt.black)
        blackPen.setWidth(1)
        painter.setPen(blackPen)

        painter.fillRect(rec, self.brush)
        painter.drawRect(rec)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):
        """
        Select self.objects
        """

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            for obj in self.objects:
                cmds.select(obj, add=True)

        if (mods & 1) == 0:
            cmds.select(clear=True)
            for obj in self.objects:
                cmds.select(obj, tgl=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Custom_Button_Icon_Item(QtWidgets.QGraphicsPixmapItem):
    """
    Extends QGraphicsPixmapItem to add right-click menu and functions.
    """

    def __init__(self, width, height, relativePos, parent=None):
        """
        Instantiate the class, set class variables, and create menu
        :param width: button width
        :param height: button height
        :param relativePos: relative position from parent widget
        :param parent: parent widget
        """

        super(Custom_Button_Icon_Item, self).__init__(parent)

        # set Z depth of parent to be behind self
        if parent is not None:
            self.parentItem().setZValue(1)
        self.setZValue(2)

        # set class variables
        self.width = width
        self.height = height
        self.relativePos = relativePos

        # create context menu
        self.menu = QtWidgets.QMenu()

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.iconsPath = settings.value("iconPath")

        # menu icons
        remove = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/removeModule.png"))))
        icon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/background.png"))))
        label = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/edit.png"))))

        # add right click menu to select settings
        self.menu.addAction(remove, "Remove", self.remove_item)
        self.menu.addAction(icon, "Edit Button Icon", self.edit_icon)
        self.menu.addAction(label, "Edit Label", self.edit_label)

        # position button (from parent)
        if parent is not None:
            self.setPos(self.parentItem().boundingRect().topLeft())

        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def remove_item(self):
        """
        Removes item from animation picker
        """

        scene = self.scene()
        parent = self.parentItem()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Delete button from picker?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        ret = msgBox.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            scene.removeItem(parent)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_color(self):
        """
        Launches a QColorDialog to change button color.
        """

        colorDialog = QtWidgets.QColorDialog.getColor()
        color = colorDialog.getRgb()
        red = float(color[0])
        green = float(color[1])
        blue = float(color[2])

        self.brush = QtGui.QBrush(QtGui.QColor(red, green, blue))
        self.update()
        self.setData(6, color)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_label(self):
        """
        Launch a QDialog widget to edit label and label position, then apply those edits.
        """

        # find out if there is an existing label to edit
        childItems = self.childItems()

        # if so, pass in its text into the QDialog so that the lineEdit already has the current label text populated
        if len(childItems) > 0:
            text = childItems[0].text()
            returnData = self.edit_label_UI(text)

        # if not, call on the QDialog with no pre-existing text
        else:
            returnData = self.edit_label_UI()

        #
        # If a label already existed, edit its text and position based on the return data from the QDialog
        if len(childItems) > 0:
            childItems[0].setText(returnData[0])
            textPos = self.boundingRect().center()
            textRect = childItems[0].boundingRect()
            parentRect = self.boundingRect()

            if returnData[1] == "center":
                childItems[0].setPos(textPos.x() - textRect.width() / 2, textPos.y() - textRect.height() / 2)

            if returnData[1] == "top":
                childItems[0].setPos(textPos.x() - textRect.width() / 2, textPos.y() -
                                     (parentRect.height() / 2 + textRect.height()))

            if returnData[1] == "bottom":
                childItems[0].setPos(textPos.x() - textRect.width() / 2, textPos.y() + (parentRect.height() / 2))

            if returnData[1] == "right":
                childItems[0].setPos((textPos.x() * 2) + 2, textPos.y() - (parentRect.height() / 2))

            if returnData[1] == "left":
                childItems[0].setPos((textRect.width() + 2) * -1, textPos.y() - (parentRect.height() / 2))

        # if not, add a new label now
        else:
            Custom_Text_Item(returnData[0], returnData[1], customColor=None, parent=self)

        self.setData(9, True)
        self.setData(10, returnData[0])
        self.setData(11, returnData[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_selection(self, dialog):
        """
        Loads the text from the text Edit as json data and sets the buttons self.objects to that new selection data
        :param dialog: QDialog to close when operation is complete
        """

        self.objects = json.loads(self.label_selection.toPlainText())
        self.setData(5, self.objects)
        dialog.accept()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_label_UI(self, text=None):
        """
        Builds the QDialog Widget for editing label text and position.
        :param text: Pre-existing label text (if any) to populate the QLineEdit
        :return: List. Contains new label text and label position. Both strings
        """

        # create the QDialog
        dialog = QtWidgets.QDialog()
        dialog.setMinimumSize(QtCore.QSize(300, 140))
        dialog.setMaximumSize(QtCore.QSize(300, 140))
        dialog.resize(300, 140)
        dialog.setStyleSheet(artv2_style)

        # create the main layout and add a first row
        layout = QtWidgets.QVBoxLayout(dialog)
        layout_1 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_1)

        # first row widgets: label text inputs
        layout_1.addWidget(QtWidgets.QLabel("Label Text:"))
        self.label_lineEdit = QtWidgets.QLineEdit()
        if text is not None:
            self.label_lineEdit.setText(text)
        layout_1.addWidget(self.label_lineEdit)

        # create a second row
        layout_2 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_2)

        # second row widgets: label position inputs
        layout_2.addWidget(QtWidgets.QLabel("Label Position:"))
        self.labelPosition = QtWidgets.QComboBox()
        for each in ["top", "bottom", "center", "left", "right"]:
            self.labelPosition.addItem(each)
        layout_2.addWidget(self.labelPosition)

        # create a third row
        layout_3 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_3)

        # third row widgets: cancel and accept buttons
        cancel = QtWidgets.QPushButton("Cancel")
        cancel.setObjectName("settings")
        layout_3.addWidget(cancel)
        accept = QtWidgets.QPushButton("Accept")
        accept.setObjectName("settings")
        layout_3.addWidget(accept)
        cancel.clicked.connect(dialog.reject)
        accept.clicked.connect(dialog.accept)

        # launch the dialog
        ret = dialog.exec_()

        # if user accepted, get data and return it
        if ret == 1:

            text = self.label_lineEdit.text()
            pos = self.labelPosition.currentText()
            return [text, pos]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_selection_UI(self):
        """
        Builds a QDialog widget to take current selection and dump it as json data into a textEdit.
        """

        # Create the QDialog
        dialog = QtWidgets.QDialog(interfaceUtils.getMainWindow())
        dialog.setMinimumSize(QtCore.QSize(300, 300))
        dialog.setMaximumSize(QtCore.QSize(300, 300))
        dialog.resize(300, 300)
        dialog.setStyleSheet(artv2_style)

        # Create the main layout and add a first row
        layout = QtWidgets.QVBoxLayout(dialog)
        layout_1 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_1)

        # first row widgets: Text edit to hold selection list and button that dumps current selection into text edit
        self.label_selection = QtWidgets.QTextEdit()
        self.label_selection.setMinimumSize(QtCore.QSize(240, 240))
        self.label_selection.setMaximumSize(QtCore.QSize(240, 240))
        self.label_selection.setEnabled(False)
        self.label_selection.setText(json.dumps(self.objects))
        layout_1.addWidget(self.label_selection)

        button = QtWidgets.QPushButton("<<")
        button.setMinimumSize(QtCore.QSize(30, 240))
        button.setMaximumSize(QtCore.QSize(30, 240))
        layout_1.addWidget(button)
        button.clicked.connect(self.set_selection)

        # second row widgets: cancel and accept buttons
        layout_2 = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_2)

        cancel = QtWidgets.QPushButton("Cancel")
        cancel.setObjectName("settings")
        layout_2.addWidget(cancel)
        accept = QtWidgets.QPushButton("Accept")
        accept.setObjectName("settings")
        layout_2.addWidget(accept)
        cancel.clicked.connect(dialog.reject)
        accept.clicked.connect(partial(self.edit_selection, dialog))

        # launch the dialog
        dialog.setModal(False)
        dialog.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def set_selection(self):
        """
        Takes user's current selection and dumps it as json data into the QTextEdit
        """

        selection = cmds.ls(sl=True)
        self.label_selection.setText(json.dumps(selection))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_icon(self):
        """
        Launch a QDialog widget for user to choose a new icon for the button. Then set that data.
        """

        returnData = self.edit_icon_UI()

        if returnData is not None:
            image = returnData.property("path")
            self.image = QtWidgets.QPixmap(image)
            self.setPixmap(self.image.scaled(28, 28))
            self.setData(8, image)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_icon_UI(self):
        """
        Builds the QDialog widget that lists all available icons for the user to choose from for their button icon.

        :return:  Returns accept state
        """

        # Get all available icons
        dir = utils.returnNicePath(self.iconsPath, "System")
        icons = []

        for each in os.listdir(dir):
            if os.path.splitext(utils.returnNicePath(dir, each))[1] == ".png":
                if each.find("noIcon") == -1:
                    icons.append(utils.returnNicePath(dir, each))

        # create QDialog widget
        widget = QtWidgets.QDialog()
        main_layout = QtWidgets.QVBoxLayout(widget)
        widget.setWindowTitle("Choose Icon")
        widget.setMinimumWidth(280)
        widget.setMaximumWidth(280)
        widget.setStyleSheet(artv2_style)

        # Create grid layout with 5 columns
        columns = 5
        layout = QtWidgets.QGridLayout()

        # create scroll area tol hold grid layout
        contents = QtWidgets.QFrame()
        scrollArea = QtWidgets.QScrollArea()
        main_layout.addWidget(scrollArea)

        # create cancel and accept buttons
        cancel = QtWidgets.QPushButton("Cancel")
        cancel.setObjectName("settings")
        cancel.setMinimumHeight(30)
        cancel.clicked.connect(widget.reject)
        accept = QtWidgets.QPushButton("Accept")
        accept.setObjectName("settings")
        accept.setMinimumHeight(30)
        accept.clicked.connect(widget.accept)

        # go through each icon, creating a button for the icon, and setting that button's icon to the icon. Add to
        # the gridLayout
        count = 0
        for i in icons:
            btn = QtWidgets.QPushButton()
            icon = QtGui.QIcon(i)
            btn.setIconSize(QtCore.QSize(28, 28))
            btn.setIcon(icon)
            btn.setObjectName("tool")
            btn.setProperty("path", i)
            btn.clicked.connect(partial(self.icon_chosen, btn, accept, widget))
            layout.addWidget(btn, count / columns, count % columns)
            count += 1

        # Add the grid layout to the scroll area
        contents.setLayout(layout)
        scrollArea.setWidget(contents)

        # add the rest of the widgets to the qDialog
        button_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout)
        button_layout.addWidget(cancel)
        button_layout.addWidget(accept)

        # launch dialog
        ret = widget.exec_()

        if ret == 1:
            return accept

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def icon_chosen(self, icon, button, dialog):

        path = icon.property("path")
        button.setProperty("path", path)
        dialog.accept()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SelectionButton_Icon(Custom_Button_Icon_Item):
    """
    Extends Custom Button Icon Item to add mouse press event for selecting selection set items. Also adds editing of
    selection set to the context menu
    """

    def __init__(self, width, height, relativePos, controlObjects, path, image, parent=None):
        """
        Instantiate the class, adding the menu action for editing selection sets, and then setting data

        :param width: button width
        :param height: button height
        :param relativePos: relative position from parent widget
        :param controlObjects: controls or objects to select when button is pushed
        :param path: image path on disk
        :param image: QImage
        :param parent: parent widget
        """
        super(SelectionButton_Icon, self).__init__(width, height, relativePos, parent)

        self.objects = controlObjects
        self.image = image
        self.setPixmap(self.image.scaled(28, 28))

        selection = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/select_set.png"))))
        self.menu.addAction(selection, "Edit Selection Set", self.edit_selection_UI)

        self.setData(QtCore.Qt.UserRole, path)
        self.setData(99, "selection")
        self.setData(5, self.objects)
        self.setData(7, 1)
        self.setData(8, path)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):
        """
        Selects self.objects
        """

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            for obj in self.objects:
                cmds.select(obj, add=True)

        if (mods & 1) == 0:
            cmds.select(clear=True)
            for obj in self.objects:
                cmds.select(obj, tgl=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ScriptButton_Icon(Custom_Button_Icon_Item):
    """
    Extends Custom_Button_Icon_Item to be used as a button that will execute a script. Also adds menu action to edit
    script to the menu.
    """

    def __init__(self, width, height, relativePos, script, script_type, path, image, parent=None):
        """
        Instantiates the class, setting variables, adding the new menu action for editing scripts, and setting data.

        :param width: button width
        :param height: button height
        :param relativePos: relative position of button from parent widget
        :param script: the contents of the script to execute
        :param script_type: the type of script (mel or python)
        :param path: the image path on disk
        :param image: the QImage (of above image)
        :param parent: the parent widget
        """

        super(ScriptButton_Icon, self).__init__(width, height, relativePos, parent)

        self.image = image
        self.setPixmap(self.image.scaled(28, 28))
        self.script = script
        self.script_type = script_type

        # menu icons
        script_contents = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/file.png"))))

        # add right click menu to select settings
        self.menu.addAction(script_contents, "Edit Script", self.edit_script)

        self.setData(QtCore.Qt.UserRole, path)
        self.setData(99, "script")
        self.setData(7, 1)
        self.setData(8, path)
        self.setData(20, script_type)
        self.setData(21, script)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):
        """
        Executes the script based on script type
        """

        if self.script_type == "python":
            try:
                exec("" + self.script + "")
            except:
                pass

        if self.script_type == "mel":
            try:
                import maya.mel as mel
                mel.eval(self.script)
            except:
                pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def edit_script(self):
        """
        Creates an ART_ScriptEditor instance to edit the script, passing in the current script contents. Takes instance
        data and resets class vars to edited data.
        """

        inst = ART_ScriptEditor(None, self.script, None)
        inst.exec_()

        self.script_type = inst.script_type
        self.script = inst.script
        self.setData(20, self.script_type)
        self.setData(21, self.script)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run(animInst):
    """
    Create an instance of ART_AddCustomButton
    :param animInst: animation picker instance
    :return: instance of ART_AddCustomButton
    """

    if cmds.window("pyART_AddCustomButtonToPickerWIN", exists=True):
        cmds.deleteUI("pyART_AddCustomButtonToPickerWIN", wnd=True)

    inst = ART_AddCustomButton(animInst, interfaceUtils.getMainWindow())
    inst.show()
    return inst
