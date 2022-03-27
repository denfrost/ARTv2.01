import os
import json
import maya.cmds as cmds
from functools import partial

from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


windowName = "pyART_SelectionSetsWIN"
windowTitle = "Selection Sets"


class ART_SelectionSetsUI(QtWidgets.QMainWindow):
    """
    This class creates the selection sets interface tool. This tool allows the user to add and modify selection sets.
    """

    def __init__(self, parent=None):
        """
        Instantiates the class, gets settings values from QSettings. Calls on building the interface.
        Lastly, populates the UI.

            .. image:: /images/selectionSetsMaster.png
        """

        super(ART_SelectionSetsUI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projectPath = settings.value("projectPath")

        # load the stylesheets
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.menu_style = interfaceUtils.get_style_sheet("menu")

        # build the UI
        self.buildUI()

        # add everything to the scroll area (selection sets)
        self.scroll_contents.setLayout(self.scroll_contents_layout)
        scroll_area_vertical = QtWidgets.QScrollArea()
        scroll_area_vertical.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area_vertical.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area_vertical.setWidgetResizable(True)
        self.selection_sets_layout.addWidget(scroll_area_vertical)
        scroll_area_vertical.setWidget(self.scroll_contents)

        # populate UI
        self._populate_categories()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        """
        Builds the interface for the tool.

            .. seealso:: _populate_sets
            .. seealso:: _populate_categories
            .. seealso:: _add_button

            .. image:: /images/selectionSets.png

        """

        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName, wnd=True)

        self.window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(self.window_icon)
        self.setStyleSheet(self.style)

        # set the window size
        self.setMinimumSize(QtCore.QSize(320, 300))
        self.setMaximumSize(QtCore.QSize(320, 1000))
        self.resize(QtCore.QSize(320, 570))

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

        # character combo box
        character_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(character_layout)

        character_layout.addWidget(QtWidgets.QLabel("Character: "))
        self.characters = QtWidgets.QComboBox()
        self.characters.setObjectName("mid")
        self.characters.setMinimumWidth(200)
        character_layout.addWidget(self.characters)

        # populate characters
        self.findCharacters()

        # add button for creating new selection set
        self.add_set_button = QtWidgets.QPushButton("Create New Selection Set")
        self.add_set_button.setMinimumSize(QtCore.QSize(300, 30))
        self.add_set_button.setMaximumSize(QtCore.QSize(300, 30))
        self.add_set_button.setObjectName("settings")
        self.add_set_button.clicked.connect(self.create_new_set_UI)
        self.mainLayout.addWidget(self.add_set_button)
        text = "Create a new selection set using your current selection.\n\nBy default, selection sets strip" \
               " namespaces. If you want to keep the namespaces, check the box to keep them. Note: this will make" \
               " the selection set only work on that character!"
        self.add_set_button.setToolTip(text)

        # add hbox layout for 2 columns
        self.columnLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.columnLayout)

        # left column  (combo box and scroll area)
        self.left_column_layout = QtWidgets.QVBoxLayout()
        self.columnLayout.addLayout(self.left_column_layout)

        # combo box for selecting filters
        self.filter_combo_box = QtWidgets.QComboBox()
        self.filter_combo_box.setObjectName("mid")
        self.filter_combo_box.setMinimumSize(QtCore.QSize(230, 25))
        self.filter_combo_box.setMaximumSize(QtCore.QSize(230, 25))
        self.left_column_layout.addWidget(self.filter_combo_box)
        self.filter_combo_box.currentIndexChanged.connect(self._populate_sets)
        text = "When creating a selection set, you can give the set a category. This is purely for organization." \
               " This drop-down allows you to choose your categories of your selection sets."
        self.filter_combo_box.setToolTip(text)

        # selection sets layout
        self.selection_sets_layout = QtWidgets.QVBoxLayout()
        self.left_column_layout.addLayout(self.selection_sets_layout)

        # create the scroll contents and the vboxlayout to populate selection sets into
        self.scroll_contents = QtWidgets.QFrame()
        self.scroll_contents_layout = QtWidgets.QVBoxLayout()

        # right column
        self.right_column = QtWidgets.QGroupBox()
        self.right_column.setMinimumSize(QtCore.QSize(60, 515))
        self.right_column.setMaximumSize(QtCore.QSize(60, 515))
        self.right_column.setObjectName("dark")
        self.columnLayout.addWidget(self.right_column)
        self.right_column_layout = QtWidgets.QVBoxLayout(self.right_column)
        self.right_column_layout.setContentsMargins(6, 0, 2, 0)

        # add tangent buttons to right column
        self.auto_tan_btn = self._add_button("autotan", "Sets keys for selected objects to auto-tangents.")
        self.right_column_layout.addWidget(self.auto_tan_btn)
        self.auto_tan_btn.clicked.connect(partial(self.set_tangents, "auto"))

        self.spline_tan_btn = self._add_button("splinetan", "Sets keys for selected objects to spline tangents.")
        self.right_column_layout.addWidget(self.spline_tan_btn)
        self.spline_tan_btn.clicked.connect(partial(self.set_tangents, "spline"))

        self.flat_tan_btn = self._add_button("flattan", "Sets keys for selected objects to flat tangents.")
        self.right_column_layout.addWidget(self.flat_tan_btn)
        self.flat_tan_btn.clicked.connect(partial(self.set_tangents, "flat"))

        self.step_tan_btn = self._add_button("steptan", "Sets keys for selected objects to stepped tangents.")
        self.right_column_layout.addWidget(self.step_tan_btn)
        self.step_tan_btn.clicked.connect(partial(self.set_tangents, "step"))

        self.linear_tan_btn = self._add_button("lintan", "Sets keys for selected objects to linear tangents.")
        self.right_column_layout.addWidget(self.linear_tan_btn)
        self.linear_tan_btn.clicked.connect(partial(self.set_tangents, "linear"))

        self.plat_tan_btn = self._add_button("plattan", "Sets keys for selected objects to plateau tangents.")
        self.right_column_layout.addWidget(self.plat_tan_btn)
        self.plat_tan_btn.clicked.connect(partial(self.set_tangents, "plateau"))

        self.clamp_tan_btn = self._add_button("clamptan", "Sets keys for selected objects to clamped tangents.")
        self.right_column_layout.addWidget(self.clamp_tan_btn)
        self.clamp_tan_btn.clicked.connect(partial(self.set_tangents, "clamped"))

        # add spacer
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.right_column_layout.addItem(spacer)

        # restore window position
        settings = QtCore.QSettings("ARTv2", "SelectionSets")
        self.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "SelectionSets")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_categories(self):
        """
        populate the categories comboBox with the categories found in the selection sets.
        """

        user_dir = utils.returnFriendlyPath(os.path.join(self.toolsPath, "User"))
        sets_dir = utils.returnFriendlyPath(os.path.join(user_dir, "Selection_Sets"))

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        if not os.path.exists(sets_dir):
            os.makedirs(sets_dir)

        selection_sets = os.listdir(sets_dir)
        categories = []

        for each in selection_sets:
            full_path = (utils.returnFriendlyPath(os.path.join(sets_dir, each)))
            print full_path
            print each
            f = open(full_path, 'r')
            data = json.load(f)
            f.close()

            if data.get("category") not in categories:
                categories.append(data.get("category"))

        for category in categories:
            self.filter_combo_box.addItem(category)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_sets(self):
        """
        Populate the UI with buttons for each selection set. (If the category of the selection set matches the
        current category, or if the current category is all.)

            .. seealso:: _add_selection_sets
        """

        self._clearLayout(self.scroll_contents_layout)

        user_dir = utils.returnFriendlyPath(os.path.join(self.toolsPath, "User"))
        sets_dir = utils.returnFriendlyPath(os.path.join(user_dir, "Selection_Sets"))

        selection_sets = os.listdir(sets_dir)

        for each in selection_sets:
            full_path = (utils.returnFriendlyPath(os.path.join(sets_dir, each)))
            f = open(full_path, 'r')
            data = json.load(f)
            f.close()

            # get current category
            category = self.filter_combo_box.currentText()
            if data.get("category") == category or category == "All":
                self._add_selection_sets(data, full_path)

        # add spacer
        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.scroll_contents_layout.addItem(spacer)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _add_button(self, objectName, tooltip):
        """
        Adds toolbar buttons for the tangent tools.

        :param image: the image to be used for QIcon
        :param tooltip: the tooltip image path
        :return: returns the QPushButton created

            .. seealso:: buildUI
        """

        button = QtWidgets.QPushButton("")
        button.setMinimumSize(QtCore.QSize(43, 43))
        button.setMaximumSize(QtCore.QSize(43, 43))
        button.setObjectName(objectName)
        button.setToolTip(tooltip)

        return button

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_new_set_UI(self):
        """
        Builds an interface for creating a new selection set.
        """

        # if window exists, delete first
        if cmds.window("ART_CreateNewSelectionSetWin", exists=True):
            cmds.deleteUI("ART_CreateNewSelectionSetWin", wnd=True)

        # launch a UI to get the set name information
        self.create_new_set_win = QtWidgets.QMainWindow(self)
        self.create_new_set_win.setStyleSheet(self.style)
        self.create_new_set_win.closeEvent = self.newSet_closeEvent

        # set window size
        self.create_new_set_win.resize(300, 150)
        self.create_new_set_win.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                                    QtWidgets.QSizePolicy.Fixed))
        self.create_new_set_win.setMinimumSize(QtCore.QSize(300, 150))
        self.create_new_set_win.setMaximumSize(QtCore.QSize(300, 150))

        # set window name/title/icon
        self.create_new_set_win.setObjectName("ART_CreateNewSelectionSetWin")
        self.create_new_set_win.setWindowTitle("Create New Set")
        self.create_new_set_win.setWindowIcon(self.window_icon)

        # create the main widget
        new_set_main_widget = QtWidgets.QFrame()
        new_set_main_widget.setObjectName("dark")
        self.create_new_set_win.setCentralWidget(new_set_main_widget)

        # create the main layout
        main_layout = QtWidgets.QVBoxLayout(new_set_main_widget)

        # first row
        row_1_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(row_1_layout)

        row_1_label = QtWidgets.QLabel("Set Name: ")
        row_1_label.setStyleSheet("background: transparent; font: bold;")
        row_1_layout.addWidget(row_1_label)

        self.new_set_name = QtWidgets.QLineEdit()
        self.new_set_name.setObjectName("light")
        self.new_set_name.setMinimumWidth(215)
        self.new_set_name.setMaximumWidth(215)
        self.new_set_name.setPlaceholderText("Enter a name for the selection set..")
        row_1_layout.addWidget(self.new_set_name)

        # second row
        row_2_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(row_2_layout)

        row_2_label = QtWidgets.QLabel("Category: ")
        row_2_label.setStyleSheet("background: transparent; font: bold;")
        row_2_layout.addWidget(row_2_label)

        self.new_set_category = QtWidgets.QLineEdit()
        self.new_set_category.setObjectName("light")
        self.new_set_category.setMinimumWidth(215)
        self.new_set_category.setMaximumWidth(215)
        self.new_set_category.setPlaceholderText("(Optional)")
        row_2_layout.addWidget(self.new_set_category)

        word_list = self._get_categories()
        completer = QtWidgets.QCompleter(word_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.new_set_category.setCompleter(completer)

        # add checkbox for keeping namespace
        self.namespace_check_box = QtWidgets.QCheckBox("Store namespaces in selection set")
        main_layout.addWidget(self.namespace_check_box)

        # add set button
        add_new_set_button = QtWidgets.QPushButton("Create Selection Set")
        add_new_set_button.setMinimumSize(QtCore.QSize(280, 30))
        add_new_set_button.setMaximumSize(QtCore.QSize(280, 30))
        add_new_set_button.setObjectName("settings")
        add_new_set_button.clicked.connect(self.create_new_set)
        main_layout.addWidget(add_new_set_button)

        # show window
        self.create_new_set_win.show()

        # restore window position
        settings = QtCore.QSettings("ARTv2", "createNewSelectionSet")
        self.create_new_set_win.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def newSet_closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "createNewSelectionSet")
        self.settings.setValue("geometry", self.create_new_set_win.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def create_new_set(self):
        """
        Creates a new selection set. Called on from create_new_set_UI().

            .. seealso:: create_new_set_UI
            .. seealso:: write_set_to_file
        """

        # get current selection
        selected = cmds.ls(sl=True)
        if not self.namespace_check_box.isChecked():
            selection = self._strip_namespaces(selected)
        else:
            selection = selected

        if len(selection) > 0:
            # get set name
            name = self.new_set_name.text()

            # get set category
            category = self.new_set_category.text()
            if len(category) == 0:
                category = "All"

            # write set to file
            self.write_set_to_file(name, category, selection)

            # add category if it doesn't exist
            if len(category) > 0:
                current_categories = self._get_categories()
                if category not in current_categories:
                    self.filter_combo_box.addItem(category)

            # set category to new set category (if category)
            self._get_filter_index(category)

            # close the window
            self.create_new_set_win.close()
        else:
            cmds.warning("Nothing selected.")
            return

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _clearLayout(self, layout):
        """
        Clears the given layout of all child widgets

        :param layout: the layout to clear widgets from
        """

        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self._clearLayout(child.layout())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _strip_namespaces(self, selection):
        """
        Takes the passed in controls and strips any namespaces.

        :param selection: objects to strip namespaces from
        :return: new list of controls without namespaces
        """

        controls = []
        for each in selection:
            controls.append(each.partition(":")[2])
        return controls

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def write_set_to_file(self, file_name, category, selection):
        """
        Writes the selection set to disk.

        :param file_name: The name of the file and the selection set
        :param category: The category name
        :param selection: The controls for the selection set
        """

        user_dir = utils.returnFriendlyPath(os.path.join(self.toolsPath, "User"))
        sets_dir = utils.returnFriendlyPath(os.path.join(user_dir, "Selection_Sets"))

        if not os.path.exists(user_dir):
            try:
                os.makedirs(user_dir)
            except Exception, e:
                cmds.warning(str(e))

        if not os.path.exists(sets_dir):
            try:
                os.makedirs(sets_dir)
            except Exception, e:
                cmds.warning(str(e))

        full_path = utils.returnFriendlyPath(os.path.join(sets_dir, file_name + ".selection"))

        data = {}
        data["name"] = file_name
        data["category"] = category
        data["controls"] = selection

        # dump the data with json
        try:
            f = open(full_path, 'w')
            json.dump(data, f)
            f.close()
        except Exception, e:
            cmds.warning(str(e))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_categories(self):
        """
        Find the categories from all of the selection sets and compose a list.

        :return: A list of all categories from the selection sets.
        """

        categories = []

        for i in range(self.filter_combo_box.count()):
            self.filter_combo_box.setCurrentIndex(i)
            current_text = self.filter_combo_box.currentText()
            categories.append(current_text)

        return categories

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_filter_index(self, text):
        """
        Finds the index of the given text in the category combo box.

        :param text: the text to
        :return: returns the index of the text in the category combo box.
        """

        index = 0

        for i in range(self.filter_combo_box.count()):
            self.filter_combo_box.setCurrentIndex(i)
            current_text = self.filter_combo_box.currentText()
            if current_text == text:
                index = i
        return index

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _add_selection_sets(self, data, path):
        """
        Creates the selection set buttons in the UI.

        :param data: The data from the selection set file (name, category, controls)
        :param path: The file path of the selectioh set file.

            .. seealso: createContextMenu
        """

        button = QtWidgets.QPushButton(data.get("name"))
        button.setMinimumSize(QtCore.QSize(196, 30))
        button.setMaximumSize(QtCore.QSize(196, 30))
        button.setObjectName("orange")
        self.scroll_contents_layout.addWidget(button)
        button.clicked.connect(partial(self.select_controls, data))
        button.setProperty("file", path)

        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(partial(self.createContextMenu, button))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createContextMenu(self, button, point):
        """
        Creates a context menu for the selection set buttons.

        :param button: Which button to create the context menu for.
        :param point: the cursor position.

            .. seealso: _add_selection_sets
        """

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(self.menu_style)

        file_path = button.property("file")

        menu.addAction("Add Selected to Set", partial(self.add_remove_set_UI, True, False, file_path))
        menu.addAction("Remove Items from Set", partial(self.add_remove_set_UI, False, True, file_path))
        menu.addAction("Rename Set", partial(self.rename_set, file_path, button))
        menu.addAction("Delete Set", partial(self.delete_set, file_path))
        menu.exec_(button.mapToGlobal(point))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def select_controls(self, data):
        """
        Selects the controls in the selection set. If shift is held down while selecting, it will append the selection.

        :param data: selection set file data (name, category, controls)
        """

        character = self.characters.currentText()
        controls = data.get("controls")

        # if shift isn't held down, clear the selection
        mods = cmds.getModifiers()
        if not (mods & 1) > 0:
            cmds.select(clear=True)

        missingControls = []

        for each in controls:
            if cmds.objExists(character + ":" + each):
                cmds.select(character + ":" + each, add=True)
            else:
                missingControls.append(character + ":" + each)

        if len(missingControls) > 0:
            for each in missingControls:
                cmds.warning("Unable to select: " + each + ", as it was not found.")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def set_tangents(self, tangentType):
        """
        Sets the tangents of the selections' keys to the given tangent type.

        :param tangentType: auto, spline, step, flat, etc..
        """

        # select keys
        cmds.selectKey()

        # set tangent type
        if tangentType != "step":
            cmds.keyTangent(itt=tangentType, ott=tangentType)
        else:
            cmds.keyTangent(ott=tangentType)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def delete_set(self, path):
        """
        Deletes the selection set from disk.

        :param path: path of the file to delete.
        """

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Really Delete Selection Set?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        ret = msgBox.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            # delete the file on disk
            try:
                os.remove(path)
            except Exception, e:
                cmds.warning(str(e))
                return

            # populate sets
            self._populate_sets()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def add_remove_set_UI(self, add, remove, path):
        """
        Creates the UI for adding new items to the selection set or removing items from the selection set.

        :param add: If add is true, the UI functions will be changed to allow for adding items to the set.
        :param remove: if remove is true, the UI functions will be changed to allow for removing items from the set.
        :param path: the file path of the selection set
        """

        # if window exists, delete first
        if cmds.window("ART_AddRemoveSelectionSetWin", exists=True):
            cmds.deleteUI("ART_AddRemoveSelectionSetWin", wnd=True)

        # launch a UI to get the set name information
        self.add_remove_win = QtWidgets.QMainWindow(self)
        self.add_remove_win.setStyleSheet(self.style)

        # set window size
        self.add_remove_win.resize(225, 396)
        self.add_remove_win.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                                QtWidgets.QSizePolicy.Fixed))
        self.add_remove_win.setMinimumSize(QtCore.QSize(225, 380))
        self.add_remove_win.setMaximumSize(QtCore.QSize(225, 380))

        # set window name/title/icon
        self.add_remove_win.setObjectName("ART_AddRemoveSelectionSetWin")
        if add:
            self.add_remove_win.setWindowTitle("Add to Set")
        if remove:
            self.add_remove_win.setWindowTitle("Remove from Set")

        self.add_remove_win.setWindowIcon(self.window_icon)

        # create the main widget
        new_set_main_widget = QtWidgets.QFrame()
        new_set_main_widget.setObjectName("dark")
        self.add_remove_win.setCentralWidget(new_set_main_widget)

        # create the main layout
        main_layout = QtWidgets.QVBoxLayout(new_set_main_widget)

        # create the list widget
        self.add_remove_listWidget = QtWidgets.QListWidget()
        self.add_remove_listWidget.setMinimumSize(QtCore.QSize(205, 292))
        self.add_remove_listWidget.setMaximumSize(QtCore.QSize(205, 292))
        self.add_remove_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        main_layout.addWidget(self.add_remove_listWidget)

        if add:
            self.add_remove_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # populate list widget
        controls = self._populate_add_remove_UI(path)
        for each in controls:
            self.add_remove_listWidget.addItem(each)

        # if remove, create the remove button
        if remove:
            button = QtWidgets.QPushButton("Remove Selected from Set")
            button.setMinimumSize(QtCore.QSize(205, 50))
            button.setMaximumSize(QtCore.QSize(205, 50))
            button.setObjectName("settings")
            main_layout.addWidget(button)
            button.clicked.connect(partial(self.remove_from_set, path))

        # if add, add a checkbox, and a button
        if add:
            checkbox = QtWidgets.QCheckBox("Store namespaces in selection set")
            main_layout.addWidget(checkbox)

            button = QtWidgets.QPushButton("Add Selection to Set")
            button.setMinimumSize(QtCore.QSize(205, 30))
            button.setMaximumSize(QtCore.QSize(205, 30))
            button.setObjectName("settings")
            main_layout.addWidget(button)
            button.clicked.connect(partial(self.add_to_set, checkbox, path))

        self.add_remove_win.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_add_remove_UI(self, path):
        """
        Populates the listWidget in the add/remove UI.

        :param path: Path to the selection set file.
        :return: returns a list of the controls to add to the list widget.
        """

        # open the file and load the data.
        f = open(path, 'r')
        data = json.load(f)
        f.close()

        return data.get("controls")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def remove_from_set(self, path):
        """
        Removes the selected listWidget items from the selection set, then modifies the selection set file to reflect
        those changes.

        :param path: selection set file path.
        """

        selectedItems = self.add_remove_listWidget.selectedItems()

        # remove the selected items from the list widget
        selected_controls = []
        for each in selectedItems:
            selected_controls.append(each.text())
            index = self.add_remove_listWidget.row(each)
            self.add_remove_listWidget.takeItem(index)

        # find a list of all the controls NOT selected. This will be the new data in the set file.
        new_controls = []
        for i in range(self.add_remove_listWidget.count()):
            widget_item = self.add_remove_listWidget.item(i)
            if widget_item.text() not in selected_controls:
                new_controls.append(widget_item.text())

        # read the file, get the data.
        f = open(path, 'r')
        data = json.load(f)
        f.close()

        # overwrite the controls data item
        data["controls"] = new_controls

        # save the file
        f = open(path, 'w')
        json.dump(data, f)
        f.close()

        # update UI
        self._populate_sets()
        # add_remove_win

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def add_to_set(self, checkbox, path):
        """
        Adds current selection to the selection set. Modifies the selection set file to reflect those changes.

        :param checkbox: the checkbox widget to see if we should store namespaces or not.
        :param path: the selection set file path
        """

        # get selection
        selected = cmds.ls(sl=True)

        # get checkbox state
        keep_namespaces = checkbox.isChecked()

        # read the file, get the data.
        f = open(path, 'r')
        data = json.load(f)
        f.close()

        # strip namespaces if needed
        if not keep_namespaces:
            selection = self._strip_namespaces(selected)
        else:
            selection = selected

        # append controls to list
        controls = data.get("controls")
        controls.extend(selection)
        data["controls"] = controls

        # save file
        f = open(path, 'w')
        json.dump(data, f)
        f.close()

        # update UI
        for each in selection:
            self.add_remove_listWidget.addItem(each)

        # update UI
        self._populate_sets()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def rename_set(self, path, button):
        """
        Renames the selection set.

        :param path: Selection set file path
        :param button: the button widget whose context menu was called. Used to set text of button after the rename.
        """

        # open a dialog to get a new name
        text, ok = QtWidgets.QInputDialog.getText(self, "Rename Set:", "New name:")
        if ok and text:

            # open the file and load the data.
            f = open(path, 'r')
            data = json.load(f)
            f.close()

            # change the name key to the new name value
            data["name"] = text

            # write over this file path
            f = open(path, 'w')
            data = json.dump(data, f)
            f.close()

            button.setText(text)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findCharacters(self):

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
            except:
                namespace = cmds.getAttr(node + ".name")

            # add the icon found on the node's icon path attribute to the tab
            iconPath = cmds.getAttr(node + ".iconPath")
            iconPath = utils.returnNicePath(self.projectPath, iconPath)
            icon = QtGui.QIcon(iconPath)

            self.characters.addItem(icon, namespace)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """
    Deletes the UI if it exists, then instatiates the class, building the tool and the UI.

    :return: the instance of this tool
    """

    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, wnd=True)

    gui = ART_SelectionSetsUI(interfaceUtils.getMainWindow())
    gui.show()
    return gui
