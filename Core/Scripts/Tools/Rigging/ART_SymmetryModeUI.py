import os
from functools import partial

import maya.cmds as cmds

from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


class ART_SymmetryMode():
    def __init__(self, rig_creator_inst):

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.tools_path = settings.value("toolsPath")
        self.icons_path = settings.value("iconPath")

        self._build_interface(rig_creator_inst)
        self.rig_creator_inst = rig_creator_inst

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self, rig_creator_inst):

        if cmds.window("ART_SymmetryModeWin", exists=True):
            cmds.deleteUI("ART_SymmetryModeWin", wnd=True)

        self.window = QtWidgets.QMainWindow(rig_creator_inst)
        window_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/logo.png"))
        self.window.setWindowIcon(window_icon)

        style = interfaceUtils.get_style_sheet("artv2_style")
        self.window.setStyleSheet(style)

        main_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.central_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.window.setObjectName("ART_SymmetryModeWin")
        self.window.setWindowTitle("Mass Mirror Mode")

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.window.setSizePolicy(main_size_policy)
        self.window.setMinimumSize(QtCore.QSize(600, 250))
        self.window.setMaximumSize(QtCore.QSize(600, 250))

        self.background_frame = QtWidgets.QFrame()
        self.main_layout.addWidget(self.background_frame)

        self.widget_layout = QtWidgets.QHBoxLayout(self.background_frame)
        self.widget_layout.setContentsMargins(5, 5, 5, 5)

        self.module_list_background = QtWidgets.QFrame()
        self.module_list_background.setMinimumSize(QtCore.QSize(450, 200))
        self.module_list_background.setMaximumSize(QtCore.QSize(450, 200))
        self.module_list_background.setContentsMargins(20, 0, 20, 0)

        self.module_list = QtWidgets.QListWidget(self.module_list_background)
        self.widget_layout.addWidget(self.module_list_background)
        self.module_list.setMinimumSize(QtCore.QSize(450, 200))
        self.module_list.setMaximumSize(QtCore.QSize(450, 200))
        self.module_list.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.module_list.setSpacing(3)

        self.button_layout = QtWidgets.QVBoxLayout()
        self.widget_layout.addLayout(self.button_layout)
        self.button_layout.setContentsMargins(5, 20, 5, 20)

        self.selection_button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.addLayout(self.selection_button_layout)
        self.select_all_button = QtWidgets.QPushButton("Select All")
        self.select_all_button.setMinimumSize(QtCore.QSize(115, 25))
        self.select_all_button.setMaximumSize(QtCore.QSize(115, 25))
        self.selection_button_layout.addWidget(self.select_all_button)
        self.select_all_button.clicked.connect(partial(self._toggle_selection_for_mirror, True))
        self.select_all_button.setObjectName("settings")

        self.clear_selection_button = QtWidgets.QPushButton("Clear Selection")
        self.clear_selection_button.setMinimumSize(QtCore.QSize(115, 25))
        self.clear_selection_button.setMaximumSize(QtCore.QSize(115, 25))
        self.selection_button_layout.addWidget(self.clear_selection_button)
        self.clear_selection_button.clicked.connect(partial(self._toggle_selection_for_mirror, False))
        self.clear_selection_button.setObjectName("settings")

        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.button_layout.addItem(spacer_item)

        self.mirror_button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.addLayout(self.mirror_button_layout)
        self.mirror_button = QtWidgets.QPushButton("Mirror Checked")
        self.mirror_button.setToolTip("Mirror selected modules to unselected modules")
        self.mirror_button.setMinimumSize(QtCore.QSize(115, 25))
        self.mirror_button.setMaximumSize(QtCore.QSize(115, 25))
        self.mirror_button_layout.addWidget(self.mirror_button)
        self.mirror_button.setObjectName("settings")

        self.mirror_button.clicked.connect(partial(self._mirror_transformations))

        # Populate the list widget with modules and their mirrored module.
        modules = utils.returnRigModules()
        entries = []
        modules_to_list = []

        for mod in modules:
            module_name = cmds.getAttr(mod + ".moduleName")
            mirror_module = cmds.getAttr(mod + ".mirrorModule")
            invalid_types = [None, "None"]
            if mirror_module not in invalid_types:
                if module_name not in modules_to_list:
                    entries.append([module_name, mirror_module])
                    modules_to_list.append(module_name)
                    modules_to_list.append(mirror_module)

        if len(entries) == 0:
            item = QtWidgets.QListWidgetItem(self.module_list)
            label = QtWidgets.QLabel("No modules with mirroring setup")
            item.setSizeHint(label.sizeHint())
            self.module_list.addItem(item)
            self.module_list.setItemWidget(item, label)

        for each in entries:
            # Create a custom widget to add to each entry in the listWidget.
            main_widget = QtWidgets.QWidget()
            button_layout = QtWidgets.QHBoxLayout(main_widget)

            check_box = QtWidgets.QCheckBox()
            check_box.setMinimumSize(QtCore.QSize(12, 12))
            check_box.setMaximumSize(QtCore.QSize(12, 12))
            check_box.setChecked(True)
            button_layout.addWidget(check_box)

            label = QtWidgets.QLabel("Mirror ")
            button_layout.addWidget(label)

            mirror_from = QtWidgets.QComboBox()
            mirror_from.addItem(each[0])
            mirror_from.addItem(each[1])
            button_layout.addWidget(mirror_from)
            mirror_from.setMinimumWidth(150)

            label = QtWidgets.QLabel(" To ")
            button_layout.addWidget(label)
            label.setAlignment(QtCore.Qt.AlignCenter)

            mirror_to = QtWidgets.QComboBox()
            mirror_to.addItem(each[1])
            mirror_to.addItem(each[0])
            button_layout.addWidget(mirror_to)
            mirror_to.setMinimumWidth(150)

            mirror_from.currentIndexChanged.connect(partial(self._toggle_combo_box_left, mirror_from, mirror_to))
            mirror_to.currentIndexChanged.connect(partial(self._toggle_combo_box_right, mirror_from, mirror_to))

            # Add this item widget to the list widget.
            item = QtWidgets.QListWidgetItem(self.module_list)
            index = entries.index(each)
            if (index % 2) == 0:
                item.setBackground(QtGui.QColor(106, 106, 108))
            else:
                item.setBackground(QtGui.QColor(46, 46, 48))

            item.setSizeHint(main_widget.sizeHint())
            self.module_list.addItem(item)
            self.module_list.setItemWidget(item, main_widget)

        self.window.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _toggle_selection_for_mirror(self, state):

        # Find all items in the list widget. Toggle the checkbox for that item depending on the current state.
        items = self.module_list.findItems('', QtCore.Qt.MatchRegExp)
        for item_in_list in items:
            item_widget = self.module_list.itemWidget(item_in_list)
            layout = item_widget.findChild(QtWidgets.QHBoxLayout)

            for i in range(layout.count()):
                item = layout.itemAt(i)
                if type(item.widget()) == QtWidgets.QCheckBox:
                    item.widget().setChecked(state)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _toggle_combo_box_left(self, mirror_from, mirror_to):

        if mirror_from.currentText() == mirror_to.currentText():
            index = mirror_to.findText(mirror_from.currentText(), QtCore.Qt.MatchExactly)
            if index == 0:
                mirror_to.setCurrentIndex(1)
            else:
                mirror_to.setCurrentIndex(0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _toggle_combo_box_right(self, mirror_from, mirror_to):

        if mirror_to.currentText() == mirror_from.currentText():
            index = mirror_from.findText(mirror_to.currentText(), QtCore.Qt.MatchExactly)
            if index == 0:
                mirror_from.setCurrentIndex(1)
            else:
                mirror_from.setCurrentIndex(0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _mirror_transformations(self):

        items = self.module_list.findItems('', QtCore.Qt.MatchRegExp)

        for i in range(len(items)):
            for item_in_selected in items:
                item_widget = self.module_list.itemWidget(item_in_selected)
                layout = item_widget.findChild(QtWidgets.QHBoxLayout)

                # If the checkbox state is true, mirror transformations.
                state = False
                for i in range(layout.count()):
                    item = layout.itemAt(i)

                    if type(item.widget()) == QtWidgets.QCheckBox:
                        state = item.widget().isChecked()

                    if type(item.widget()) == QtWidgets.QComboBox:
                        if state is True:
                            widget_text = item.widget().currentText()
                            modules = utils.returnRigModules()
                            for mod in modules:
                                module_name = cmds.getAttr(mod + ".moduleName")

                                if module_name == widget_text:
                                    modType = cmds.getAttr(mod + ".moduleType")
                                    imported_mod = __import__("RigModules." + modType, {}, {}, [modType])

                                    module_class = getattr(imported_mod, imported_mod.className)
                                    module_inst = module_class(self.rig_creator_inst, module_name)
                                    module_inst.mirrorTransformations()
