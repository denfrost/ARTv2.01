"""
Module for building pick-walk setup interfaces.
"""

import json
import os
from functools import partial

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Tools.Animation.ART_PickWalkSetup as pick_walk

# maya 2016< maya2017> compatibility
try:
    import shiboken as shiboken
except ImportError:
    import shiboken2 as shiboken


class ART_PickWalkSetupUI(interfaceUtils.baseWindow):
    """
    This class is used to create an interface to setup and manage pick-walking between ARTv2 rig controls.

    .. image:: /images/pickWalkUI.png

    """

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def __init__(self, parent=None):

        super(ART_PickWalkSetupUI, self).__init__(900, 320, 900, 320, parent)

        self._build_interface()

        # setup signal/slot on character combo box
        self.character_combo.currentIndexChanged.connect(self._populate_modules)

        # find characters
        self._populate_characters(self.character_combo)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        # create the main widget
        self.main_widget = QtWidgets.QFrame()
        self.setCentralWidget(self.main_widget)

        # set qt object name
        self.setObjectName("ART_PickWalkSetupUI")
        self.setWindowTitle("ARTv2 Pick-Walking Setup")

        # create top level layout
        self.top_level_layout = QtWidgets.QVBoxLayout(self.main_widget)

        # create the menu bar
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.setMaximumHeight(25)
        self.top_level_layout.addWidget(self.menu_bar)

        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")
        icon__save_template = QtGui.QIcon(os.path.join(self.icons_path, "System/save.png"))
        icon__load_template = QtGui.QIcon(os.path.join(self.icons_path, "System/load.png"))
        icon_help = self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxQuestion)

        file_menu.addAction(icon__save_template, "Save Template", self._save_template)
        file_menu.addAction(icon__load_template, "Load Template", self._load_template_ui)
        help_menu.addAction(icon_help, "Help", self._launch_help)
        help_menu.addAction(icon_help, "Technical Documentation", self._launch_helpDoc)

        # create the mainLayout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.top_level_layout.addLayout(self.main_layout)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Create the first column, which will hold the modules listWidget
        self.column_a = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.column_a)

        # display a label
        label = QtWidgets.QLabel("Modules for: ")
        label.setStyleSheet("background: transparent;")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.column_a.addWidget(label)

        # add combo box
        self.character_combo = QtWidgets.QComboBox()
        self.character_combo.setObjectName("light")
        self.column_a.addWidget(self.character_combo)

        # build the listWidget
        self.module_list = QtWidgets.QListWidget()
        self.module_list.setMinimumSize(QtCore.QSize(170, 225))
        self.module_list.setMaximumSize(QtCore.QSize(170, 225))
        self.column_a.addWidget(self.module_list)
        self.module_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # add spacer
        spacer_item = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.column_a.addItem(spacer_item)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Create the second column, which will hold buttons for convenience functions that act on selected modules
        self.column_b = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.column_b)

        # add spacer
        spacer_item = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.column_b.addItem(spacer_item)

        settings_button = QtWidgets.QPushButton("Select Settings")
        settings_button.setMinimumWidth(120)
        settings_button.setMaximumWidth(120)
        settings_button.setMinimumHeight(30)
        settings_button.setObjectName("settings")
        self.column_b.addWidget(settings_button)
        settings_button.clicked.connect(self._select_settings)

        hide_ctrl_button = QtWidgets.QPushButton("Hide Controls")
        hide_ctrl_button.setMinimumWidth(120)
        hide_ctrl_button.setMaximumWidth(120)
        hide_ctrl_button.setMinimumHeight(30)
        hide_ctrl_button.setObjectName("settings")
        self.column_b.addWidget(hide_ctrl_button)
        hide_ctrl_button.clicked.connect(partial(self._toggle_control_display, False))

        show_ctrl_button = QtWidgets.QPushButton("Show Controls")
        show_ctrl_button.setMinimumWidth(120)
        show_ctrl_button.setMaximumWidth(120)
        show_ctrl_button.setMinimumHeight(30)
        show_ctrl_button.setObjectName("settings")
        self.column_b.addWidget(show_ctrl_button)
        show_ctrl_button.clicked.connect(partial(self._toggle_control_display, True))

        # add spacer
        spacer_item = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.column_b.addItem(spacer_item)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Create the third column, which will hold the pickwalking widget
        self.column_c = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.column_c)

        # add spacer
        spacer_item = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.column_c.addItem(spacer_item)

        # add a groupbox for the frame
        self.group_box = QtWidgets.QGroupBox("Pick-Walking Setup")
        self.group_box.setObjectName("mid")
        self.group_box.setMinimumSize(QtCore.QSize(540, 250))
        self.group_box.setMaximumSize(QtCore.QSize(540, 250))
        self.column_c.addWidget(self.group_box)
        self.group_box.setContentsMargins(0, 0, 0, 0)

        # add VBoxLayout for the groupbox
        self.group_box_layout = QtWidgets.QVBoxLayout(self.group_box)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # first row (up direction)
        pick_walk_row_1 = QtWidgets.QHBoxLayout()
        self.group_box_layout.addLayout(pick_walk_row_1)

        spacer_item = QtWidgets.QSpacerItem(150, 10)
        pick_walk_row_1.addItem(spacer_item)

        self.up_button = QtWidgets.QPushButton("")
        self.up_button.setMinimumWidth(150)
        self.up_button.setMaximumWidth(150)
        self.up_button.setMinimumHeight(30)
        self.up_button.setObjectName("pickwalk")
        pick_walk_row_1.addWidget(self.up_button)
        self.up_button.clicked.connect(partial(self._setup_pick_walk, self.up_button, "pickWalkUp"))

        spacer_item = QtWidgets.QSpacerItem(150, 10)
        pick_walk_row_1.addItem(spacer_item)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # second row (up arrow label)
        pick_walk_row_2 = QtWidgets.QHBoxLayout()
        self.group_box_layout.addLayout(pick_walk_row_2)

        spacer_item = QtWidgets.QSpacerItem(184, 10)
        pick_walk_row_2.addItem(spacer_item)

        up_arrow = QtWidgets.QLabel()
        icon = QtGui.QIcon(utils.returnNicePath(self.icons_path, "System/arrow_up.png"))
        up_arrow.setPixmap(icon.pixmap(20))
        up_arrow.setStyleSheet("background: transparent;")
        pick_walk_row_2.addWidget(up_arrow)
        up_arrow.setAlignment(QtCore.Qt.AlignCenter)

        spacer_item = QtWidgets.QSpacerItem(184, 10)
        pick_walk_row_2.addItem(spacer_item)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # third row (left box, left arrow label, center, right arrow label, right box)
        pick_walk_row_3 = QtWidgets.QHBoxLayout()
        self.group_box_layout.addLayout(pick_walk_row_3)

        self.left_button = QtWidgets.QPushButton("")
        self.left_button.setMinimumWidth(150)
        self.left_button.setMaximumWidth(150)
        self.left_button.setMinimumHeight(30)
        self.left_button.setObjectName("pickwalk")
        pick_walk_row_3.addWidget(self.left_button)
        self.left_button.clicked.connect(partial(self._setup_pick_walk, self.left_button, "pickWalkLeft"))

        left_arrow = QtWidgets.QLabel("")
        icon = QtGui.QIcon(utils.returnNicePath(self.icons_path, "System/arrow_left.png"))
        left_arrow.setPixmap(icon.pixmap(20))
        left_arrow.setStyleSheet("background: transparent;")
        pick_walk_row_3.addWidget(left_arrow)

        self.center_button = QtWidgets.QPushButton("")
        self.center_button.setMinimumWidth(150)
        self.center_button.setMaximumWidth(150)
        self.center_button.setMinimumHeight(30)
        self.center_button.setObjectName("pickwalk")
        pick_walk_row_3.addWidget(self.center_button)
        self.center_button.clicked.connect(self._find_connections)

        right_arrow = QtWidgets.QLabel("")
        icon = QtGui.QIcon(utils.returnNicePath(self.icons_path, "System/arrow_right.png"))
        right_arrow.setStyleSheet("background: transparent;")
        right_arrow.setPixmap(icon.pixmap(20))
        pick_walk_row_3.addWidget(right_arrow)

        self.right_button = QtWidgets.QPushButton("")
        self.right_button.setMinimumWidth(150)
        self.right_button.setMaximumWidth(150)
        self.right_button.setMinimumHeight(30)
        self.right_button.setObjectName("pickwalk")
        pick_walk_row_3.addWidget(self.right_button)
        self.right_button.clicked.connect(partial(self._setup_pick_walk, self.right_button, "pickWalkRight"))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # fourth row (down arrow label)
        pick_walk_row_4 = QtWidgets.QHBoxLayout()
        self.group_box_layout.addLayout(pick_walk_row_4)

        spacer_item = QtWidgets.QSpacerItem(184, 10)
        pick_walk_row_4.addItem(spacer_item)

        down_arrow = QtWidgets.QLabel("")
        icon = QtGui.QIcon(utils.returnNicePath(self.icons_path, "System/arrow_down.png"))
        down_arrow.setPixmap(icon.pixmap(20))
        down_arrow.setStyleSheet("background: transparent;")
        pick_walk_row_4.addWidget(down_arrow)
        down_arrow.setAlignment(QtCore.Qt.AlignCenter)

        spacer_item = QtWidgets.QSpacerItem(184, 10)
        pick_walk_row_4.addItem(spacer_item)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # fifth row (up direction)
        pick_walk_row_5 = QtWidgets.QHBoxLayout()
        self.group_box_layout.addLayout(pick_walk_row_5)

        spacer_item = QtWidgets.QSpacerItem(150, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        pick_walk_row_5.addItem(spacer_item)

        self.down_button = QtWidgets.QPushButton("")
        self.down_button.setMinimumWidth(150)
        self.down_button.setMaximumWidth(150)
        self.down_button.setMinimumHeight(30)
        self.down_button.setObjectName("pickwalk")
        pick_walk_row_5.addWidget(self.down_button)
        self.down_button.clicked.connect(partial(self._setup_pick_walk, self.down_button, "pickWalkDown"))

        spacer_item = QtWidgets.QSpacerItem(150, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        pick_walk_row_5.addItem(spacer_item)

        # add spacer
        spacer_item = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.column_c.addItem(spacer_item)

        # restore window position
        settings = QtCore.QSettings("ARTv2", "PickWalkSetup")
        self.restoreGeometry(settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "PickWalkSetup")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_characters(self, comboBox):

        network_nodes = cmds.ls(type="network")
        characters = []

        for node in network_nodes:
            attrs = cmds.listAttr(node, ud=True)
            if "rigModules" in attrs:
                if node not in characters:
                    characters.append(node)

        for character in characters:
            if cmds.objExists(character + ".namespace"):
                name = cmds.getAttr(character + ".namespace")
                comboBox.addItem(name, character)
            if not cmds.objExists(character + ".namespace"):
                if len(characters) == 1:
                    name = cmds.getAttr(character + ".name")
                    comboBox.addItem(name, character)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_modules(self):

        # get currently selected character from combo box.
        self.module_list.clear()
        character = self.character_combo.itemData(self.character_combo.currentIndex())

        modules = cmds.listConnections(character + ".rigModules")
        for mod in modules:
            mod_name = cmds.getAttr(mod + ".moduleName")
            mod_item = QtWidgets.QListWidgetItem()
            mod_item.setData(1, mod)
            mod_item.setText(mod_name)

            self.module_list.addItem(mod_item)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _setup_pick_walk(self, button, attr):
        
        selection = cmds.ls(sl=True)
        if len(selection) > 1:
            cmds.warning("Too many objects selected. Only select 1 item to add to pickwalking.")
            return

        source_object = self.center_button.text()
        destination_object = button.text()

        if len(selection) >= 0:
            self._disconnect_pick_walking(source_object, destination_object, button, attr)

        if len(selection) > 0:
            selected = selection[0]
            button.setText(selected)

            if not cmds.objExists(source_object + "." + attr):
                cmds.addAttr(source_object, ln=attr, at="message")

            connections = cmds.listConnections(source_object + "." + attr)
            if connections is None:
                pick_walker = pick_walk.ART_PickWalk()
                pick_walker.create_pickwalk_connection(source_object, selected, attr)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _disconnect_pick_walking(self, source_object, destination_object, button, attr):

        if len(destination_object) == 0:
            button.setText("")

        if len(destination_object) > 0:
            if cmds.objExists(source_object + "." + attr):
                connections = cmds.listConnections(source_object + "." + attr)
                if connections is not None:
                    result = self._confirm_disconnect()
                    if result == QtWidgets.QMessageBox.Yes:
                        try:
                            cmds.disconnectAttr(destination_object + ".message", source_object + "." + attr)
                            button.setText("")
                        except Exception, e:
                            print str(e)

                    else:
                        return

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_connections(self):

        attrs = ["pickWalkUp", "pickWalkDown", "pickWalkLeft", "pickWalkRight"]
        buttons = [self.up_button, self.down_button, self.left_button, self.right_button]

        # clear all button text
        for button in buttons:
            button.setText("")
        selection = cmds.ls(sl=True)
        if len(selection) > 1:
            cmds.warning("too many items selected for pick-walk setup. Select only 1 item.")
            return

        # if an item selected, set the center button's text to the name of the object
        if len(selection) > 0:
            obj = selection[0]
            self.center_button.setText(obj)

            # now find any pickwalk connections
            connections = []
            objAttrs = cmds.listAttr(obj, ud=True)

            for attr in attrs:
                if attr in objAttrs:
                    connection = cmds.listConnections(obj + "." + attr)
                    if connection is not None:
                        connection = connection[0]
                        if connection not in connections:
                            connections.append([attr, connection])

            # if there were pickwalk connections, set the text to the appropriate buttons
            if len(connections) > 0:

                for each in connections:
                    # first get the attr, then get the index of that item in the attrs list
                    attr = each[0]
                    index = attrs.index(attr)
                    button = buttons[index]

                    button.setText(each[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _confirm_disconnect(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Are you sure you want to remove the current pickwalk relationship?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        ret = msgBox.exec_()
        return ret

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _select_settings(self):

        # get selected items in list widget
        selected = self.module_list.selectedItems()

        select_nodes = []

        for each in selected:
            node = each.data(1)
            if cmds.objExists(node):
                characterNode = cmds.listConnections(node + ".parent")[0]
                mod_name = each.text()
                namespace = ""
                if cmds.objExists(characterNode + ".namespace"):
                    namespace = cmds.getAttr(characterNode + ".namespace")
                select_nodes.append(namespace + ":" + mod_name + "_settings")

        cmds.select(clear=True)
        for node in select_nodes:
            if cmds.objExists(node):
                cmds.select(node, add=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _toggle_control_display(self, show=False):

        # get selected items in list widget
        selected = self.module_list.selectedItems()

        display_nodes = []

        for each in selected:
            node = each.data(1)
            if cmds.objExists(node):
                character_node = cmds.listConnections(node + ".parent")[0]
                mod_name = each.text()
                if cmds.objExists(character_node + ".namespace"):
                    namespace = cmds.getAttr(character_node + ".namespace")
                else:
                    namespace = ""

                display_nodes.append(namespace + ":" + mod_name + "_group")

        for node in display_nodes:
            if cmds.objExists(node):
                cmds.setAttr(node + ".visibility", show)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _save_template(self):

        if os.path.exists(os.path.normcase(os.path.join(self.tools_path, "Projects"))):
            starting_dir = self.tools_path
        else:
            starting_dir = os.path.normcase(os.path.join(self.tools_path, "Projects"))

        filename = cmds.fileDialog2(fm=0, okc="Save Template", dir=starting_dir, ff="*.pickWalk")
        if filename is not None:
            file_path = filename[0]

            characters = []
            for i in range(self.character_combo.count()):
                character_name = self.character_combo.itemText(i)
                character_node = self.character_combo.itemData(i)
                characters.append([character_name, character_node])

            # if there is more than one character in the scene, ask which character to save template data for
            character = characters[0][0]

            if len(characters) > 1:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Which character do you want to save the template for?")
                for character in characters:
                    msgBox.addButton(character[0], QtWidgets.QMessageBox.AcceptRole)
                choice = msgBox.exec_()
                character = characters[choice][0]

            pick_walker = pick_walk.ART_PickWalk(character, file_path)
            pick_walker.save_template()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_template_ui(self):

        # create a QMainWindow and parent to self
        window = QtWidgets.QDialog(self)
        window.setMinimumSize(QtCore.QSize(400, 200))
        window.setMaximumSize(QtCore.QSize(400, 200))
        window.setObjectName("ART_pickwalk__load_template_window")
        window.setWindowTitle("Load pick-walking template")

        # add a central widget
        main_widget = QtWidgets.QFrame(window)
        main_widget.setMinimumSize(QtCore.QSize(400, 200))
        main_widget.setMaximumSize(QtCore.QSize(400, 200))
        main_widget.setObjectName("dark")

        # add main layout
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # add first row (lineEdit for path and browse button)
        first_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(first_row_layout)

        self._load_template_lineEdit = QtWidgets.QLineEdit()
        browse_button = QtWidgets.QPushButton()
        browse_button.setMinimumSize(QtCore.QSize(30, 30))
        browse_button.setMaximumSize(QtCore.QSize(30, 30))
        browse_button.setObjectName("tool")
        icon_browse = QtGui.QIcon(os.path.join(self.icons_path, "System/fileBrowse.png"))
        browse_button.setIcon(icon_browse)
        browse_button.clicked.connect(self._load_template_file)

        first_row_layout.addWidget(self._load_template_lineEdit)
        first_row_layout.addWidget(browse_button)

        # add second row (checkbox for stripping namespaces)
        second_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(second_row_layout)

        self._load_template_namespaceCB = QtWidgets.QCheckBox("Strip Namespaces")
        second_row_layout.addWidget(self._load_template_namespaceCB)
        self._load_template_namespaceCB.setToolTip("If the pick-walk template file has namespaces present,\n"
                                                   "this option will remove them on load.\nThis is useful for when a"
                                                   " pick-walking template\nfile has been saved out from a referenced"
                                                   " rig.")
        self._load_template_namespaceCB.setChecked(False)

        self.namespace_label = QtWidgets.QLabel()
        second_row_layout.addWidget(self.namespace_label)
        self.namespace_label.setStyleSheet("background: transparent;")

        # add third row (label and combo box for list of characters)
        third_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(third_row_layout)

        label = QtWidgets.QLabel("Load Template on: ")
        label.setStyleSheet("background: transparent;")
        third_row_layout.addWidget(label)

        self._load_template_characters = QtWidgets.QComboBox()
        third_row_layout.addWidget(self._load_template_characters)
        self._populate_characters(self._load_template_characters)

        # add fourth row (load button)
        load_button = QtWidgets.QPushButton("Load Pick-Walking Template")
        load_button.setMinimumHeight(40)
        load_button.setMaximumHeight(40)
        load_button.setObjectName("blueButton")
        main_layout.addWidget(load_button)
        load_button.clicked.connect(self._load_template)

        window.exec_()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_template_file(self):

        # ask for the file name to give the template and then save the template
        if os.path.exists(os.path.normcase(os.path.join(self.tools_path, "Projects"))):
            starting_dir = self.tools_path
        else:
            starting_dir = os.path.normcase(os.path.join(self.tools_path, "Projects"))

        filename = cmds.fileDialog2(fm=1, okc="Load Template", dir=starting_dir, ff="*.pickWalk")

        if filename is not None:
            self._load_template_lineEdit.setText(filename[0])

            template_file = self._load_template_lineEdit.text()
            # search the first entry to see if a namespace is found
            f = open(template_file, 'r')
            data = json.load(f)
            f.close()

            for key in data.keys():
                control_data = data.get(key)
                controls = control_data.keys()

                if controls[0].find(":") != -1:
                    self.namespace_label.setText("Namespace in file: " + controls[0].split(":")[0])
                else:
                    self.namespace_label.setText("No namespace in file.")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_template(self):

        # gather info from the UI and close the UI
        template_file = self._load_template_lineEdit.text()
        strip_namespaces = self._load_template_namespaceCB.isChecked()
        character_name = self._load_template_characters.currentText()

        if len(template_file) == 0:
            cmds.warning("No template file to load!")
            return

        cmds.deleteUI("ART_pickwalk__load_template_window", wnd=True)

        pick_walker = pick_walk.ART_PickWalk(character_name, template_file, strip_namespaces)
        pick_walker.load_template()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _launch_help(self):

        from Tools.System import ART_Help

        help_movie = utils.returnFriendlyPath(os.path.join(self.icons_path, "Help/pickWalkHelp.gif"))
        ART_Help.ART_HelpMovie(self, help_movie)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _launch_helpDoc(self):

        import webbrowser

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        toolsPath = settings.value("toolsPath")
        html_file = os.path.join(toolsPath, "Documentation\\build\\animation_docs\\pickwalker.html")

        webbrowser.get().open('file://' + os.path.realpath(html_file))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """
    Instantiates the PickWalkSetupUI class
    """

    if cmds.window("ART_PickWalkSetupUI", exists=True):
        cmds.deleteUI("ART_PickWalkSetupUI", wnd=True)

    gui = ART_PickWalkSetupUI(interfaceUtils.getMainWindow())
    gui.show()
