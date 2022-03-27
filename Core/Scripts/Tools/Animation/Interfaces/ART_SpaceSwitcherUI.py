"""
Module for creating user interfaces that interact with the ART_SpaceSwitcher module classes.
"""

from functools import partial
import os
import string
import random
import json

import maya.cmds as cmds

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import Tools.Animation.ART_SpaceSwitcher as space_switcher

# noinspection PyUnresolvedReferences
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016 < maya2017 > compatibility
try:
    import shiboken as shiboken
except ImportError:
    import shiboken2 as shiboken


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def populate_line_edit(line_edit, combo_box, control=False):
    """
    Takse a control and adds its text as the text for the given lineEdit.

    :param str control: Control whose text to query.
    :param combo_box: combo box needed for populating spaces to.
    :param line_edit: lineEdit to populate the control's text with.
    :type combo_box: QtWidgets.QComboBox
    :type line_edit: QtWidgets.QLineEdit
    """

    if control is not False:
        line_edit.setText("")
        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            cmds.warning("No selection provided.")
            populate_spaces(combo_box, line_edit)
            return
        try:
            if cmds.objExists(selection[0] + "_space_switcher_follow"):
                fullPath = cmds.listRelatives(selection[0], parent=True, f=True)[0]
                pathList = fullPath.split("|")
                pathList.reverse()

                if selection[0] + "_space_switcher_follow" in pathList:
                    line_edit.setText(selection[0])
                else:
                    raise RuntimeError

        except RuntimeError:
            cmds.warning("Control is not a valid control for space switching!")

    else:
        line_edit.setText(cmds.ls(sl=True)[0])

    populate_spaces(combo_box, line_edit)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def show_selection_widget(parent, line_edit, combo_box, has_spaces=False):
    """
    Shows a dialog of a list of all controls that have space switching ability.

    :param parent: parent widget of this dialog.
    :param line_edit: line edit whose text to populate with the selected control from the list.
    :param combo_box: combo box needed for populating spaces to.
    :param has_spaces: Whether or not the controls to populate need to have existing spaces to be considered.
    :type parent: QtWidgets.QWidget
    :type combo_box: QtWidgets.QComboBox
    :type line_edit: QtWidgets.QLineEdit
    :type has_spaces: bool
    """

    inst = SelectControlsWidget(parent, multi_select=False, selection_list=None, has_spaces=has_spaces)
    inst.exec_()

    if len(inst.selected) > 0:
        line_edit.setText(inst.selected[0])
        populate_spaces(combo_box, line_edit)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def search_controls(completer_model, combo_box, text_field, *args):
    """
    Searches all controls for the text in the line edit that the completer is assigned to. Adds matches to the completer
    model.

    :param completer_model: completer model to add matches to the search results to, from the line edit
    :param combo_box: combo box needed for populating spaces.
    :param text_field: text field needed for populating spaces.
    :type completer_model: QtGui.QStringListModel
    :type combo_box: QtWidgets.QComboBox
    :type text_field: QtWidgets.QLineEdit
    """

    controls = utils.get_all_controls()
    control_list = []

    current_text = args[0]
    matching = [s for s in controls if current_text in s]
    for each in matching:
        control_list.append(each)
    completer_model.setStringList(control_list)
    populate_spaces(combo_box, text_field)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def populate_spaces(combo_box, text_field, *args):
    """
    Populates the combo box with the spaces for the control specified in the line edit.

    :param combo_box: combo box needed for populating spaces.
    :param text_field: text field needed for populating spaces.
    :type combo_box: QtWidgets.QComboBox
    :type text_field: QtWidgets.QLineEdit
    """

    if combo_box is not None:
        combo_box.clear()
        control = text_field.text()

        if cmds.objExists(control):
            if cmds.objExists(control + ".follow"):
                spaces = ["default"]
                spaces.extend(space_switcher.find_control_spaces(control))
                for space in spaces:
                    combo_box.addItem(space)

                active_index = cmds.getAttr(control + ".follow")
                enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
                split_string = enum_val.split(":")
                active_space = split_string[active_index]
                combo_box.setCurrentText(active_space)

            else:
                combo_box.addItem("No spaces available.")
        else:
            combo_box.addItem("No spaces available.")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_CreateSpaceUI(interfaceUtils.baseWindow):
    """
    User interface class that requests the control to create a space for, the space object, the name of the space, and
    what type of constraint to use.
    This information then gets passed to the main space switcher class and creates the space.


    .. figure:: /images/space_switcher_create_ui.png
        :width: 351px
        :height: 206px

        The interface for creating a space for a control.

    To run from a command line, use:

    .. code-block:: python

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
        ssui.create_space(None, None)

    """

    def __init__(self, control=None, uiInst=None, parent=None):
        """
        :param str control: The name of the control that will receive the created space.
        :param uiInst: Instance of the animation interface.
        :param parent: Parent widget.
        :type uiInst: ART_AnimationUI
        :type parent: QtWidgets.QWidget
        """

        super(ART_CreateSpaceUI, self).__init__(350, 180, 350, 180, parent)

        self.control = control
        self.uiInst = uiInst
        self._build_interface()

    def _build_interface(self):

        # Create the main widget for the window.
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("dark")
        self.setCentralWidget(self.mainWidget)

        # Set size policy, object name, and window title.
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)
        self.setObjectName("ART_CreateSpaceUI")
        self.setWindowTitle("Create Space")

        # Create the main layout.
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        # Create the first row (control label, lineEdit, pushButton).
        row_one_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(row_one_layout)

        control_label = QtWidgets.QLabel("control: ")
        control_label.setStyleSheet("background: transparent; font: bold;")
        control_label.setMinimumWidth(40)
        control_label.setMaximumWidth(40)
        row_one_layout.addWidget(control_label)

        self.control_lineEdit = QtWidgets.QLineEdit(self.control)
        self.control_lineEdit.setObjectName("light")
        self.control_lineEdit.setMinimumWidth(200)
        self.control_lineEdit.setMaximumWidth(200)
        row_one_layout.addWidget(self.control_lineEdit)

        self.control_button = QtWidgets.QPushButton("<")
        self.control_button.setMinimumHeight(25)
        self.control_button.setObjectName("settings")
        row_one_layout.addWidget(self.control_button)

        picker_button = QtWidgets.QPushButton()
        picker_button.setMinimumHeight(25)
        picker_button.setObjectName("settings")
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/list.png"))
        picker_button.setIconSize(QtCore.QSize(31, 21))
        picker_button.setIcon(list_icon)
        picker_button.setToolTip("Open a list of all available controls with space-switching capability to choose "
                                 "from.")
        picker_button.clicked.connect(partial(show_selection_widget, self, self.control_lineEdit, None))
        row_one_layout.addWidget(picker_button)

        # Create the second row (space label, lineEdit, pushButton).
        row_two_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(row_two_layout)

        space_label = QtWidgets.QLabel("space: ")
        space_label.setStyleSheet("background: transparent; font: bold;")
        space_label.setMinimumWidth(40)
        space_label.setMaximumWidth(40)
        row_two_layout.addWidget(space_label)

        self.space_lineEdit = QtWidgets.QLineEdit("")
        self.space_lineEdit.setObjectName("light")
        self.space_lineEdit.setMinimumWidth(200)
        self.space_lineEdit.setMaximumWidth(200)
        row_two_layout.addWidget(self.space_lineEdit)

        self.space_button = QtWidgets.QPushButton("<")
        self.space_button.setMinimumSize(QtCore.QSize(25, 25))
        self.space_button.setObjectName("settings")
        row_two_layout.addWidget(self.space_button)

        # Create the third row (space niceName label, lineEdit).
        row_three_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(row_three_layout)

        niceName_label = QtWidgets.QLabel("name: ")
        niceName_label.setStyleSheet("background: transparent; font: bold;")
        niceName_label.setMinimumWidth(40)
        niceName_label.setMaximumWidth(40)
        row_three_layout.addWidget(niceName_label)

        self.space_name_lineEdit = QtWidgets.QLineEdit("")
        self.space_name_lineEdit.setObjectName("light")
        self.space_name_lineEdit.setPlaceholderText("enter a name for the space")
        self.space_name_lineEdit.setMinimumWidth(200)

        regexp = QtCore.QRegExp("[A-Za-z_ ]+")
        validator = QtGui.QRegExpValidator(regexp, self.space_name_lineEdit)
        self.space_name_lineEdit.setValidator(validator)
        row_three_layout.addWidget(self.space_name_lineEdit)

        # Space type layout
        space_type_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(space_type_layout)

        type_label = QtWidgets.QLabel("type: ")
        type_label.setMinimumWidth(40)
        type_label.setMaximumWidth(40)
        space_type_layout.addWidget(type_label)

        self.space_type_options = QtWidgets.QComboBox()
        self.space_type_options.setMinimumHeight(25)
        self.space_type_options.setObjectName("light")

        parent_space_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/space_parent.png"))
        translate_space_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/space_translate.png"))
        rotate_space_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/space_rotate.png"))

        self.space_type_options.addItem(parent_space_icon, "Translation and Rotation")
        self.space_type_options.setItemData(0, "parent")
        self.space_type_options.addItem(translate_space_icon, "Translation")
        self.space_type_options.setItemData(1, "translation")
        self.space_type_options.addItem(rotate_space_icon, "Rotation")
        self.space_type_options.setItemData(2, "rotation")
        space_type_layout.addWidget(self.space_type_options)

        # Create the "CREATE" buttons
        row_four_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(row_four_layout)

        create_and_close_button = QtWidgets.QPushButton("Create and Close")
        create_and_close_button.setObjectName("settings")
        create_and_close_button.setMinimumHeight(30)
        create_and_close_button.clicked.connect(partial(self._createSpace, True))
        row_four_layout.addWidget(create_and_close_button)

        create_space_button = QtWidgets.QPushButton("Create")
        create_space_button.setObjectName("settings")
        create_space_button.setMinimumHeight(30)
        create_space_button.clicked.connect(partial(self._createSpace))
        row_four_layout.addWidget(create_space_button)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setObjectName("settings")
        close_button.setMinimumHeight(30)
        close_button.clicked.connect(partial(self.close))
        row_four_layout.addWidget(close_button)

        # Hook up the signals and slots.
        self.control_button.clicked.connect(partial(populate_line_edit, self.control_lineEdit, None, True))
        self.space_button.clicked.connect(partial(populate_line_edit, self.space_lineEdit, None))

    def _createSpace(self, close=False):

        # Get information from the UI.
        control = self.control_lineEdit.text()
        space = self.space_lineEdit.text()
        name = self.space_name_lineEdit.text()
        current_index = self.space_type_options.currentIndex()
        space_type = self.space_type_options.itemData(current_index)

        if len(name) == 0:
            cmds.warning("No name given.")
            return

        # Create the space.
        space_switcher.CreateSpace(name, control, space, space_type)
        self.space_name_lineEdit.setText("")
        self.space_lineEdit.setText("")
        if close is True:
            self.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# noinspection PyUnusedLocal
class ART_SpaceSwitcherUI(interfaceUtils.baseWindow):
    """
    This class provides a user interface for switching and baking spaces.

    .. figure:: /images/space_switcher_switch_ui.png
        :width: 458px
        :height: 251px

        The interface for switching spaces. Also includes functions for updating matching on spaces.

    .. figure:: /images/space_switcher_bake_ui.png
        :width: 458px
        :height: 255px

        The interface for baking spaces.

    To run from a command line, use:

    .. code-block:: python

        import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
        ssui.run()

    """

    def __init__(self, parent=None):
        """
        :param parent: Parent widget
        :type parent: QtWidgets.QWidget
        """
        super(ART_SpaceSwitcherUI, self).__init__(455, 220, 455, 200, parent)

        self._build_interface()

        cmds.scriptJob(event=["timeChanged", self._update_space_via_time], kws=True, parent="ART_SpaceSwitcherUI")

    def _build_interface(self):

        # Create the main widget.
        main_widget = QtWidgets.QFrame()
        self.setCentralWidget(main_widget)

        # Set size policy, object name, and window title.
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setObjectName("ART_SpaceSwitcherUI")
        self.setWindowTitle("ARTv2 Space Switcher")

        # Create the mainLayout.
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # Create the space-switching tab.
        space_switch_tab = QtWidgets.QFrame()
        main_layout.addWidget(space_switch_tab)
        space_switch_tab.setObjectName("darkborder")

        space_switcher_layout = QtWidgets.QVBoxLayout(space_switch_tab)

        # Create the first row of widgets, used for choosing the operation mode of the tool.
        space_switch_row_1_layout = QtWidgets.QHBoxLayout()
        space_switcher_layout.addLayout(space_switch_row_1_layout)

        operation_label = QtWidgets.QLabel("Operation: ")
        button_group = QtWidgets.QButtonGroup(space_switch_row_1_layout)
        self.switch_operation = QtWidgets.QRadioButton("Switch Space")
        self.bake_operation = QtWidgets.QRadioButton("Bake Space")

        button_group.addButton(self.switch_operation)
        button_group.addButton(self.bake_operation)
        button_group.buttonClicked.connect(partial(self._operation_toggle))

        self.switch_operation.setChecked(True)
        self.bake_operation.setChecked(False)

        space_switch_row_1_layout.addWidget(operation_label)
        space_switch_row_1_layout.addWidget(self.switch_operation)
        space_switch_row_1_layout.addWidget(self.bake_operation)

        v_spacer = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        space_switcher_layout.addItem(v_spacer)

        # Create the second row of widgets, used for specifying the control to use for space-switching.
        space_switch_row_2_layout = QtWidgets.QHBoxLayout()
        space_switcher_layout.addLayout(space_switch_row_2_layout)

        ss_control_label = QtWidgets.QLabel("Control: ")
        self.space_switch_control_field = QtWidgets.QLineEdit()
        self.space_switch_control_field.setObjectName("light")
        self.space_switch_control_field.setPlaceholderText("Search..")

        self.control_completer = QtWidgets.QCompleter()
        self.completer_model = QtGui.QStringListModel()
        self.control_completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.control_completer.setModel(self.completer_model)
        self.control_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.space_switch_control_field.setCompleter(self.control_completer)

        ss_load_selection_btn = QtWidgets.QPushButton()
        ss_load_selection_btn.setMinimumSize(QtCore.QSize(35, 25))
        ss_load_selection_btn.setMaximumSize(QtCore.QSize(35, 25))
        ss_load_selection_btn.setObjectName("settings")
        selection_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/use_selection.png"))
        ss_load_selection_btn.setIconSize(QtCore.QSize(31, 21))
        ss_load_selection_btn.setIcon(selection_icon)
        ss_load_selection_btn.setToolTip("Load currently selected control for space-switching.")
        ss_load_selection_btn.clicked.connect(partial(self._add_selected_control))

        ss_open_picker_btn = QtWidgets.QPushButton()
        ss_open_picker_btn.setMinimumSize(QtCore.QSize(35, 25))
        ss_open_picker_btn.setMaximumSize(QtCore.QSize(35, 25))
        ss_open_picker_btn.setObjectName("settings")
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/list.png"))
        ss_open_picker_btn.setIconSize(QtCore.QSize(31, 21))
        ss_open_picker_btn.setIcon(list_icon)
        ss_open_picker_btn.setToolTip("Open a list of all available controls with spaces to choose from.")

        space_switch_row_2_layout.addWidget(ss_control_label)
        space_switch_row_2_layout.addWidget(self.space_switch_control_field)
        space_switch_row_2_layout.addWidget(ss_load_selection_btn)
        space_switch_row_2_layout.addWidget(ss_open_picker_btn)

        # Create the third row of widgets, which will contain the spaces for the control.
        space_switch_row_3_layout = QtWidgets.QHBoxLayout()
        space_switcher_layout.addLayout(space_switch_row_3_layout)

        ss_space_label = QtWidgets.QLabel("Space: ")
        self.space_switch_combo_box = QtWidgets.QComboBox()
        self.space_switch_combo_box.setObjectName("light")
        self.space_switch_combo_box.setMinimumWidth(270)
        self.space_switch_combo_box.activated.connect(partial(self._switch_space))

        # hook up signals/slots for text field
        self.space_switch_control_field.textEdited.connect(partial(search_controls, self.completer_model,
                                                           self.space_switch_combo_box,
                                                                   self.space_switch_control_field))
        self.space_switch_control_field.textChanged.connect(partial(populate_spaces, self.space_switch_combo_box,
                                                                    self.space_switch_control_field))
        ss_open_picker_btn.clicked.connect(partial(show_selection_widget, self, self.space_switch_control_field,
                                                   self.space_switch_combo_box, True))

        # add button spacer
        button_spacer = QtWidgets.QSpacerItem(90, 25, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        space_switch_row_3_layout.addWidget(ss_space_label)
        space_switch_row_3_layout.addWidget(self.space_switch_combo_box)
        space_switch_row_3_layout.addItem(button_spacer)

        # add section for updating matching
        self.update_matching_group = QtWidgets.QGroupBox("Update Matching")
        space_switcher_layout.addWidget(self.update_matching_group)

        hbox_layout = QtWidgets.QHBoxLayout(self.update_matching_group)

        prev_button = QtWidgets.QPushButton()
        prev_button.setObjectName("settings")
        prev_button.setMinimumSize(QtCore.QSize(25, 25))
        prev_button.setMaximumSize(QtCore.QSize(25, 25))
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/prev.png"))
        prev_button.setIconSize(QtCore.QSize(20, 20))
        prev_button.setIcon(list_icon)
        hbox_layout.addWidget(prev_button)
        prev_button.setToolTip("Go to previous space-switch key.")
        prev_button.clicked.connect(partial(self._prev_key))

        match_previous_button = QtWidgets.QPushButton("Match Previous")
        match_previous_button.setObjectName("settings")
        match_previous_button.setMinimumHeight(25)
        hbox_layout.addWidget(match_previous_button)
        match_previous_button.setToolTip("Match the previous frame's pose.")
        match_previous_button.clicked.connect(partial(self._update_matching, True, False))

        match_next_button = QtWidgets.QPushButton("Match Next")
        match_next_button.setObjectName("settings")
        match_next_button.setMinimumHeight(25)
        hbox_layout.addWidget(match_next_button)
        match_next_button.setToolTip("Match the next frame's pose.")
        match_next_button.clicked.connect(partial(self._update_matching, False, True))

        next_button = QtWidgets.QPushButton()
        next_button.setObjectName("settings")
        next_button.setMinimumSize(QtCore.QSize(25, 25))
        next_button.setMaximumSize(QtCore.QSize(25, 25))
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/next.png"))
        next_button.setIconSize(QtCore.QSize(20, 20))
        next_button.setIcon(list_icon)
        hbox_layout.addWidget(next_button)
        next_button.setToolTip("Go to next space-switch key.")
        next_button.clicked.connect(partial(self._next_key))

        # Create the fourth row, which will hold widgets for setting the frame range for baking.
        space_switch_row_4_layout = QtWidgets.QHBoxLayout()
        space_switcher_layout.addLayout(space_switch_row_4_layout)

        self.bake_label = QtWidgets.QLabel("Bake Range: ")
        self.bake_label.setVisible(False)

        h_spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.start_label = QtWidgets.QLabel("Start Frame: ")
        self.start_label.setVisible(False)

        self.end_label = QtWidgets.QLabel("End Frame: ")
        self.end_label.setVisible(False)

        self.start_frame = QtWidgets.QLineEdit()
        self.start_frame.setObjectName("light")
        self.start_frame.setMaximumWidth(60)
        self.start_frame.setVisible(False)
        self.end_frame = QtWidgets.QLineEdit()
        self.end_frame.setObjectName("light")
        self.end_frame.setMaximumWidth(60)
        self.end_frame.setVisible(False)

        space_switch_row_4_layout.addWidget(self.bake_label)
        space_switch_row_4_layout.addItem(h_spacer)
        space_switch_row_4_layout.addWidget(self.start_label)
        space_switch_row_4_layout.addWidget(self.start_frame)
        space_switch_row_4_layout.addWidget(self.end_label)
        space_switch_row_4_layout.addWidget(self.end_frame)

        # Add the button for baking spaces.
        self.bake_spaces_btn = QtWidgets.QPushButton("Bake Space")
        self.bake_spaces_btn.setMinimumHeight(30)
        self.bake_spaces_btn.setObjectName("settings")
        self.bake_spaces_btn.setVisible(False)
        self.bake_spaces_btn.clicked.connect(self._bake_space)

        space_switcher_layout.addWidget(self.bake_spaces_btn)

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        space_switcher_layout.addItem(spacer)

        # Restore the window position.
        settings = QtCore.QSettings("ARTv2", "SpaceSwitcher")
        self.restoreGeometry(settings.value("geometry"))

    def _next_key(self):

        control = self.space_switch_control_field.text()
        if cmds.objExists(control + ".follow"):
            keys = self._find_keys(control)
            current = cmds.currentTime(q=True)

            for key in keys:
                if key > current:
                    cmds.currentTime(key)
                    break

            if keys[-1] <= current:
                cmds.currentTime(keys[0])

    def _prev_key(self):

        control = self.space_switch_control_field.text()
        if cmds.objExists(control + ".follow"):
            keys = self._find_keys(control)
            current = cmds.currentTime(q=True)
            keys.reverse()

            for key in keys:
                if key < current:
                    cmds.currentTime(key)
                    break

            if keys[-1] >= current:
                cmds.currentTime(keys[0])

    def _find_keys(self, control):

        keyframes = cmds.keyframe(control + ".follow", q=True, tc=True)
        switch_keys = []
        for i in range(len(keyframes)):
            try:
                if keyframes[i] + 1 == keyframes[i + 1]:
                    switch_keys.append(keyframes[i])
                    switch_keys.append(keyframes[i+1])
            except IndexError:
                pass
        return switch_keys

    def _update_matching(self, match_prev, match_next):
        control = self.space_switch_control_field.text()
        print control
        if cmds.objExists(control + ".follow"):
            space_switcher.UpdateSpaceMatching(control, match_prev, match_next)
        else:
            cmds.warning("control is not valid.")

    def _operation_toggle(self, *args):

        if self.switch_operation.isChecked():
            self._toggle_states(False)
            self.space_switch_combo_box.activated.connect(partial(self._switch_space))
        else:
            self._toggle_states(True)
            self.space_switch_combo_box.activated.disconnect()

    def _toggle_states(self, state):
        self.bake_label.setVisible(state)
        self.start_label.setVisible(state)
        self.start_frame.setVisible(state)
        self.end_label.setVisible(state)
        self.end_frame.setVisible(state)
        self.bake_spaces_btn.setVisible(state)

        if state is True:
            self.update_matching_group.setVisible(False)
        if state is False:
            self.update_matching_group.setVisible(True)

    def _add_selected_control(self):
        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            cmds.warning("No selection provided.")
            return
        self.space_switch_control_field.setText(selection[0])

    def _find_control_spaces(self, control):

        spaces = space_switcher.find_control_spaces(control)
        if len(spaces) == 0:
            self.space_switch_combo_box.addItem("No spaces available.")
        return spaces

    def _switch_space(self, *args):
        print "switch space activated"
        control = self.space_switch_control_field.text()
        space = self.space_switch_combo_box.currentText()
        space_switcher.SwitchSpace(control, space)

    def _update_space_via_time(self):
        control = self.space_switch_control_field.text()
        if cmds.objExists(control + ".follow"):
            active_index = cmds.getAttr(control + ".follow")
            enum_val = cmds.addAttr(control + ".follow", q=True, en=True)
            split_string = enum_val.split(":")
            active_space = split_string[active_index]
            self.space_switch_combo_box.setCurrentText(active_space)

    def _bake_space(self):
        control = self.space_switch_control_field.text()
        if cmds.objExists(control + ".follow"):
            space = self.space_switch_combo_box.currentText()
            start = int(self.start_frame.text())
            end = int(self.end_frame.text())

            space_switcher.BakeSpace(control, space, start, end)
        else:
            cmds.warning("No space switcher found on the control.")

    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):

        self.settings = QtCore.QSettings("ARTv2", "SpaceSwitcher")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QMainWindow.closeEvent(self, event)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SelectControlsWidget(interfaceUtils.baseDialog):
    """
    Shows a user interface of all controls that have a space switcher. The user can then choose from this list to
    populate the main ART_SpaceSwitcherUI control lineEdit.

    .. figure:: /images/space_switch_selection_widget.png
        :width: 180px
        :height: 335px

        Select controls widget.
    """

    def __init__(self, parent=None, multi_select=False, selection_list=None, has_spaces=False):
        """

        :param parent: Parent widget.
        :param multi_select: Whether or not the list widget allows multi-selection.
        :param selection_list: A supplied list of items to select by default in the list widget.
        :param has_spaces: Whether or not the controls need to have spaces to be valid or just have the ability.
        :type parent: QtWidgets.QtWidget
        :type multi_select: bool
        :type selection_list: string array
        :type has_spaces: bool
        """

        super(SelectControlsWidget, self).__init__(177, 300, 177, 300, parent)

        self.has_spaces = has_spaces
        self.selection_mode = QtWidgets.QAbstractItemView.SingleSelection
        if multi_select:
            self.selection_mode = QtWidgets.QAbstractItemView.ExtendedSelection

        self._build_interface()

        if selection_list is not None:
            for i in range(self.control_list.count()):
                item = self.control_list.item(i)
                if item.text() in selection_list:
                    item.setSelected(True)
            self.control_list.setFocus()

        self.selected = []

    def _build_interface(self):

        # Create the main widget.
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        main_widget = QtWidgets.QFrame()
        layout.addWidget(main_widget)

        # Set size policy, object name, and window title.
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setObjectName("artSelectControlsWidget")
        self.setWindowTitle("Controls")

        # Create the mainLayout.
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # There will be four widgets: a search bar (lineEdit), a comboBox of the character, a listWidget, and a button.
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search..")
        main_layout.addWidget(self.search_bar)
        self.search_bar.textChanged.connect(self._search)

        self.characters = QtWidgets.QComboBox()
        main_layout.addWidget(self.characters)
        self.characters.currentIndexChanged.connect(self._change_character)

        self.control_list = QtWidgets.QListWidget()
        main_layout.addWidget(self.control_list)
        self._populate_controls()
        self.control_list.setSelectionMode(self.selection_mode)

        select_button = QtWidgets.QPushButton("Select")
        select_button.setObjectName("settings")
        select_button.setMinimumHeight(30)
        main_layout.addWidget(select_button)
        select_button.clicked.connect(self._select_control)

        self._change_character()

    def _populate_controls(self):
        controls = utils.get_all_controls()
        valid_controls = []
        characters = []

        for control in controls:
            if cmds.objExists(control + "_space_switcher_follow"):
                if self.has_spaces is True:
                    if cmds.objExists(control + ".spaces"):
                        array_size = space_switcher.get_array_size(control)
                        if len(array_size) >= 1:
                            if ":" in control:
                                character_name = control.partition(":")[0]
                                if character_name not in characters:
                                    characters.append(character_name)
                            valid_controls.append(control)
                else:
                    if ":" in control:
                        character_name = control.partition(":")[0]
                        if character_name not in characters:
                            characters.append(character_name)
                    valid_controls.append(control)

        if len(characters) > 0:
            for character in characters:
                self.characters.addItem(character)
        else:
            self.characters.setVisible(False)

        for each in valid_controls:
            name = each
            character_name = None

            if ":" in name:
                name = each.partition(":")[2]
                character_name = each.partition(":")[0]
            list_widget_item = QtWidgets.QListWidgetItem(name)
            list_widget_item.setData(QtCore.Qt.UserRole, each)
            if character_name is not None:
                list_widget_item.setToolTip(character_name)
            self.control_list.addItem(list_widget_item)

    def _change_character(self):
        current_character = self.characters.currentText()

        for i in range(self.control_list.count()):
            list_widget_item = self.control_list.item(i)
            item_data = list_widget_item.data(QtCore.Qt.UserRole)
            if current_character not in item_data:
                list_widget_item.setHidden(True)
            else:
                list_widget_item.setHidden(False)

    def _search(self):
        search_term = self.search_bar.text()
        current_character = self.characters.currentText()

        for i in range(self.control_list.count()):
            list_widget_item = self.control_list.item(i)
            item_data = list_widget_item.data(QtCore.Qt.UserRole)
            if current_character in item_data:
                if search_term not in list_widget_item.text():
                    list_widget_item.setHidden(True)

                else:
                    list_widget_item.setHidden(False)

    def _select_control(self):
        selection = self.control_list.selectedItems()
        for each in selection:
            item_data = each.data(QtCore.Qt.UserRole)
            self.selected.append(item_data)
        self.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class RenameSpaceWidget(interfaceUtils.baseWindow):
    """
    Presents a user interface for renaming a space found on the control passed into the instance of this class.

    .. figure:: /images/space_switcher_rename_ui.png
        :width: 401px
        :height: 190px

        The interface for renaming a space.

    """

    def __init__(self, control=None, parent=None):
        """
        :param str control: The name of the control which contains the space to be renamed.
        :param parent: Parent widget of the UI.
        :type parent: QtWidgets.QWidget
        """

        super(RenameSpaceWidget, self).__init__(400, 160, 400, 160, parent)

        if cmds.window("artRenameSpaceWidget", q=True, exists=True):
            cmds.deleteUI("artRenameSpaceWidget", wnd=True)

        self.control = control
        self._build_interface()

    def _build_interface(self):

        # Create the main widget.
        main_widget = QtWidgets.QFrame()
        self.setCentralWidget(main_widget)

        # Set size policy, object name, and window title.
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setObjectName("artRenameSpaceWidget")
        self.setWindowTitle("Rename Space")

        # Create the mainLayout.
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # The first row consists of a label, a text field of the control, and two buttons for selecting the control.
        first_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(first_row_layout)

        control_label = QtWidgets.QLabel("Control: ")
        control_label.setMinimumWidth(98)
        control_label.setMaximumWidth(98)
        first_row_layout.addWidget(control_label)

        self.control_text_field = QtWidgets.QLineEdit()
        if self.control is not None:
            self.control_text_field.setText(self.control)
        first_row_layout.addWidget(self.control_text_field)

        self.control_completer = QtWidgets.QCompleter()
        self.completer_model = QtGui.QStringListModel()
        self.control_completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.control_completer.setModel(self.completer_model)
        self.control_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.control_text_field.setCompleter(self.control_completer)

        add_selection_button = QtWidgets.QPushButton("<<")
        add_selection_button.setMinimumSize(QtCore.QSize(35, 25))
        add_selection_button.setObjectName("settings")
        first_row_layout.addWidget(add_selection_button)

        picker_button = QtWidgets.QPushButton()
        picker_button.setMinimumSize(QtCore.QSize(35, 25))
        picker_button.setObjectName("settings")
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/list.png"))
        picker_button.setIconSize(QtCore.QSize(31, 21))
        picker_button.setIcon(list_icon)
        picker_button.setToolTip("Open a list of all available controls with space-switching capability to choose "
                                 "from.")
        first_row_layout.addWidget(picker_button)

        # The second row consists of a label and a combo box of the available spaces.
        second_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(second_row_layout)

        rename_label = QtWidgets.QLabel("Space to rename: ")
        rename_label.setMinimumWidth(98)
        rename_label.setMaximumWidth(98)
        second_row_layout.addWidget(rename_label)

        self.spaces = QtWidgets.QComboBox()
        second_row_layout.addWidget(self.spaces)
        populate_spaces(self.spaces, self.control_text_field)
        add_selection_button.clicked.connect(partial(populate_line_edit, self.control_text_field, self.spaces, True))

        # hook up signals/slots for text field
        self.control_text_field.textEdited.connect(partial(search_controls, self.completer_model, self.spaces,
                                                           self.control_text_field))
        self.control_text_field.textChanged.connect(partial(populate_spaces, self.spaces, self.control_text_field))
        picker_button.clicked.connect(partial(show_selection_widget, self, self.control_text_field, self.spaces))

        # The third row consists of a label and a text field for entering the new space name.
        third_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(third_row_layout)

        name_label = QtWidgets.QLabel("New name: ")
        name_label.setMinimumWidth(98)
        name_label.setMaximumWidth(98)
        third_row_layout.addWidget(name_label)

        self.new_name = QtWidgets.QLineEdit()

        regexp = QtCore.QRegExp("[A-Za-z_ ]+")
        validator = QtGui.QRegExpValidator(regexp, self.new_name)
        self.new_name.setValidator(validator)

        third_row_layout.addWidget(self.new_name)

        # Lastly, buttons for executing the rename.
        fourth_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(fourth_row_layout)

        rename_and_close_button = QtWidgets.QPushButton("Rename and Close")
        rename_and_close_button.setObjectName("settings")
        rename_and_close_button.setMinimumHeight(30)
        fourth_row_layout.addWidget(rename_and_close_button)
        rename_and_close_button.clicked.connect(partial(self._rename_space, True))

        rename_button = QtWidgets.QPushButton("Rename")
        rename_button.setObjectName("settings")
        rename_button.setMinimumHeight(30)
        fourth_row_layout.addWidget(rename_button)
        rename_button.clicked.connect(partial(self._rename_space))

        close_button = QtWidgets.QPushButton("Close")
        close_button.setObjectName("settings")
        close_button.setMinimumHeight(30)
        fourth_row_layout.addWidget(close_button)
        close_button.clicked.connect(self.close)

    def _rename_space(self, close=False):
        space = self.spaces.currentText()
        new_name = self.new_name.text()
        space_switcher.RenameSpace(self.control_text_field.text(), space, new_name)
        self.new_name.setText("")
        populate_spaces(self.spaces, self.control_text_field)
        if close is True:
            self.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class DeleteSpaceWidget(interfaceUtils.baseWindow):
    """
    Presents a user interface for deleting a space found on the control passed into the instance of this class.

    .. figure:: /images/space_switcher_remove_ui.png
        :width: 404px
        :height: 153px

        The interface for deleting a space.
    """

    def __init__(self, control, parent=None):
        """
        :param str control: The name of the control to delete a space from.
        :param parent: Parent widget for the UI.
        :type parent: QtWidgets.QWidget
        """

        super(DeleteSpaceWidget, self).__init__(400, 120, 400, 120, parent)

        self.control = control
        self._build_interface()

    def _build_interface(self):

        # Create the main widget.
        main_widget = QtWidgets.QFrame()
        self.setCentralWidget(main_widget)

        # Set size policy, object name, and window title.
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setObjectName("artDeleteSpaceWidget")
        self.setWindowTitle("Delete Space")

        # Create the mainLayout.
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # The first row has a label, a text field for the control, and two buttons for selecting a control.
        first_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(first_row_layout)

        control_label = QtWidgets.QLabel("Control: ")
        control_label.setMinimumWidth(98)
        control_label.setMaximumWidth(98)
        first_row_layout.addWidget(control_label)

        self.control_text_field = QtWidgets.QLineEdit()
        if self.control is not None:
            self.control_text_field.setText(self.control)
        first_row_layout.addWidget(self.control_text_field)

        self.control_completer = QtWidgets.QCompleter()
        self.completer_model = QtGui.QStringListModel()
        self.control_completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.control_completer.setModel(self.completer_model)
        self.control_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.control_text_field.setCompleter(self.control_completer)

        add_selection_button = QtWidgets.QPushButton("<<")
        add_selection_button.setMinimumSize(QtCore.QSize(35, 25))
        add_selection_button.setObjectName("settings")
        first_row_layout.addWidget(add_selection_button)

        picker_button = QtWidgets.QPushButton()
        picker_button.setMinimumSize(QtCore.QSize(35, 25))
        picker_button.setObjectName("settings")
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/list.png"))
        picker_button.setIconSize(QtCore.QSize(31, 21))
        picker_button.setIcon(list_icon)
        picker_button.setToolTip("Open a list of all available controls with space-switching capability to choose "
                                 "from.")
        first_row_layout.addWidget(picker_button)

        # The second row has a label and a combo box for choosing which space to delete.
        second_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(second_row_layout)

        label = QtWidgets.QLabel("Space to delete: ")
        label.setMaximumWidth(98)
        second_row_layout.addWidget(label)

        self.spaces = QtWidgets.QComboBox()
        second_row_layout.addWidget(self.spaces)
        populate_spaces(self.spaces, self.control_text_field)
        add_selection_button.clicked.connect(partial(populate_line_edit, self.control_text_field, self.spaces, True))

        # hook up signals/slots for text field.
        self.control_text_field.textEdited.connect(partial(search_controls, self.completer_model, self.spaces,
                                                           self.control_text_field))
        self.control_text_field.textChanged.connect(partial(populate_spaces, self.spaces, self.control_text_field))
        picker_button.clicked.connect(partial(show_selection_widget, self, self.control_text_field, self.spaces))

        # Lastly, there are buttons for confirming deletion of the space.
        third_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(third_row_layout)

        delete_space_and_close_button = QtWidgets.QPushButton("Delete and Close")
        delete_space_and_close_button.setObjectName("settings")
        delete_space_and_close_button.setMinimumHeight(30)
        third_row_layout.addWidget(delete_space_and_close_button)
        delete_space_and_close_button.clicked.connect(partial(self._delete_space, True))

        delete_space_button = QtWidgets.QPushButton("Delete Space")
        delete_space_button.setObjectName("settings")
        delete_space_button.setMinimumHeight(30)
        third_row_layout.addWidget(delete_space_button)
        delete_space_button.clicked.connect(partial(self._delete_space))

        close_button = QtWidgets.QPushButton("Close")
        close_button.setObjectName("settings")
        close_button.setMinimumHeight(30)
        third_row_layout.addWidget(close_button)
        close_button.clicked.connect(self.close)

    def _delete_space(self, close=False):
        space = self.spaces.currentText()

        try:
            space_switcher.DeleteSpace(self.control_text_field.text(), space)
            populate_spaces(self.spaces, self.control_text_field)
            if close is True:
                self.close()

        except RuntimeError, error:
            cmds.warning("Unable to delete space.")
            raise RuntimeError(error)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_CreateGlobalSpacesUI(interfaceUtils.baseWindow):
    """
    Creating global spaces is like setting up standard space "slots" you always want controls to have. You could create
    individual spaces one at a time using the create space tool, but this allows you to achieve the same result in a few
    clicks. They also give you the option to exclude controls for getting a global space created on them.

    These can be saved and loaded as templates as well.

    .. figure:: /images/space_switcher_global_spaces_ui.png
        :width: 406px
        :height: 536px

        The interface for creating a global space, which will create a space for multiple controls at once.

    .. note:: Global spaces are always created with parentConstraints!

    """

    def __init__(self, parent=None):
        super(ART_CreateGlobalSpacesUI, self).__init__(400, 500, 400, 500, parent)

        self.widgets = {}

        self._build_interface()

    def _build_interface(self):

        # Create the main widget.
        main_widget = QtWidgets.QFrame()
        self.setCentralWidget(main_widget)

        # Set size policy, object name, and window title.
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setObjectName("artCreateGlobalSpaceWin")
        self.setWindowTitle("Create Global Spaces")

        # Create the mainLayout.
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # Create the top row, which has save, load, and add space buttons
        top_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(top_row_layout)

        save_button = QtWidgets.QPushButton()
        save_button.setObjectName("save")
        save_button.setMinimumSize(QtCore.QSize(30, 30))
        save_button.setMaximumSize(QtCore.QSize(30, 30))
        top_row_layout.addWidget(save_button)
        save_button.clicked.connect(self._save_template)

        load_button = QtWidgets.QPushButton()
        load_button.setObjectName("load")
        load_button.setMinimumSize(QtCore.QSize(30, 30))
        load_button.setMaximumSize(QtCore.QSize(30, 30))
        top_row_layout.addWidget(load_button)
        load_button.clicked.connect(self._load_template)

        button_spacer = QtWidgets.QSpacerItem(10, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        top_row_layout.addItem(button_spacer)

        add_button = QtWidgets.QPushButton("Add Global Space")
        add_button.setObjectName("settings")
        add_button.setMinimumSize(QtCore.QSize(100, 30))
        add_button.setMaximumSize(QtCore.QSize(100, 30))
        top_row_layout.addWidget(add_button)
        add_button.clicked.connect(self._add_entry)

        # The middle section will have a scroll area where spaces can be added and information filled out.
        scroll_contents_frame = QtWidgets.QFrame()
        scrollSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        scroll_contents_frame.setSizePolicy(scrollSizePolicy)

        scroll_area = QtWidgets.QScrollArea()
        main_layout.addWidget(scroll_area)
        scroll_area.setMinimumHeight(400)
        scroll_area.setMaximumHeight(1200)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_contents_frame)

        self.scroll_layout = QtWidgets.QVBoxLayout(scroll_contents_frame)
        self.scroll_layout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))

        # The last row, will have buttons for generating spaces and closing, just generating spaces, and just closing.
        last_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(last_row_layout)

        generate_close_button = QtWidgets.QPushButton("Generate and Close")
        generate_close_button.setObjectName("settings")
        generate_close_button.setMinimumHeight(30)
        last_row_layout.addWidget(generate_close_button)
        generate_close_button.clicked.connect(partial(self._generate_spaces, True))

        generate_button = QtWidgets.QPushButton("Generate Spaces")
        generate_button.setObjectName("settings")
        generate_button.setMinimumHeight(30)
        last_row_layout.addWidget(generate_button)
        generate_button.clicked.connect(self._generate_spaces)

        close_button = QtWidgets.QPushButton("Close")
        close_button.setObjectName("settings")
        close_button.setMinimumHeight(30)
        last_row_layout.addWidget(close_button)
        close_button.clicked.connect(self.close)

    def _add_entry(self, space_name=None, space_object=None, exclude_list=None):
        children = self.scroll_layout.count()
        index = children - 1

        group_box = self._global_space_widget(space_name, space_object, exclude_list)
        self.scroll_layout.insertWidget(index, group_box)

    def _global_space_widget(self, space_name=None, space_object=None, exclude_list=None):

        # create a unique identifier
        widget_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))

        group_box = QtWidgets.QGroupBox()
        group_box.setMinimumHeight(100)
        group_box.setMaximumHeight(100)

        main_layout = QtWidgets.QVBoxLayout(group_box)

        # add context menu
        group_box.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        group_box.customContextMenuRequested.connect(partial(self._create_context_menu, group_box))

        # second row
        second_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(second_row_layout)

        name_label = QtWidgets.QLabel("Space Name: ")
        name_label.setMinimumWidth(100)
        name_label.setMaximumWidth(100)
        second_row_layout.addWidget(name_label)

        name_field = QtWidgets.QLineEdit()
        name_field.setMinimumWidth(180)
        name_field.setMaximumWidth(180)
        second_row_layout.addWidget(name_field)
        regexp = QtCore.QRegExp("[A-Za-z_ ]+")
        validator = QtGui.QRegExpValidator(regexp, name_field)
        name_field.setValidator(validator)
        if space_name is not None:
            name_field.setText(space_name)

        second_row_spacer = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        second_row_layout.addItem(second_row_spacer)

        # third row
        third_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(third_row_layout)

        object_label = QtWidgets.QLabel("Space Object: ")
        object_label.setMinimumWidth(100)
        object_label.setMaximumWidth(100)
        third_row_layout.addWidget(object_label)

        object_field = QtWidgets.QLineEdit()
        object_field.setMinimumWidth(180)
        object_field.setMaximumWidth(180)
        third_row_layout.addWidget(object_field)
        if space_object is not None:
            object_field.setText(space_object)

        add_object_selection_button = QtWidgets.QPushButton("<<")
        add_object_selection_button.setMinimumHeight(20)
        add_object_selection_button.setMaximumHeight(20)
        add_object_selection_button.setObjectName("settings")
        third_row_layout.addWidget(add_object_selection_button)
        add_object_selection_button.clicked.connect(partial(self._add_selected_item, object_field))

        # fourth row
        fourth_row_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(fourth_row_layout)

        excluded_label = QtWidgets.QLabel("Exluded: ")
        excluded_label.setMinimumWidth(100)
        excluded_label.setMaximumWidth(100)
        fourth_row_layout.addWidget(excluded_label)

        excluded_field = QtWidgets.QLineEdit()
        excluded_field.setMinimumWidth(180)
        excluded_field.setMaximumWidth(180)
        fourth_row_layout.addWidget(excluded_field)
        if exclude_list is not None:
            excluded_field.setText(exclude_list)

        excluded_picker_button = QtWidgets.QPushButton()
        excluded_picker_button.setObjectName("settings")
        excluded_picker_button.setMinimumHeight(20)
        excluded_picker_button.setMaximumHeight(20)
        list_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/list.png"))
        excluded_picker_button.setIconSize(QtCore.QSize(25, 15))
        excluded_picker_button.setIcon(list_icon)
        fourth_row_layout.addWidget(excluded_picker_button)
        excluded_picker_button.clicked.connect(partial(self._show_selection_widget, self, excluded_field))

        self.widgets[widget_id] = [name_field, object_field, excluded_field]

        return group_box

    def _remove_entry(self, widget):
        widget.setParent(None)
        widget.close()

    def _create_context_menu(self, widget, point):
        # icons
        icon_delete = QtGui.QIcon(utils.returnNicePath(self.icons_path, "System/delete.png"))

        # create the context menu
        contextMenu = QtWidgets.QMenu()
        contextMenu.addAction(icon_delete, "Remove", partial(self._remove_entry, widget))
        contextMenu.exec_(widget.mapToGlobal(point))

    def _add_selected_item(self, widget):
        if len(cmds.ls(sl=True)) > 0:
            if 'transform' in cmds.nodeType(cmds.ls(sl=True)[0], inherited=True):
                widget.setText(cmds.ls(sl=True)[0])
            else:
                cmds.warning("Object is not a dag node.")
        else:
            cmds.warning("No selection given.")

    def _show_selection_widget(self, parent, line_edit):

        items = line_edit.text()
        item_list = items.split(", ")

        inst = SelectControlsWidget(parent, True, item_list)
        inst.exec_()

        if len(inst.selected) > 0:
            text = ""
            for each in inst.selected:
                if each == inst.selected[-1]:
                    text += each
                else:
                    text += each + ", "

            line_edit.setText(text)

    def _save_template(self, file_path=None):

        space_data = {}

        for each in self.widgets:
            widgets = self.widgets.get(each)
            space_name = widgets[0].text()
            space_object = widgets[1].text()
            exlusion_list = widgets[2].text()

            # validate information
            if len(space_name) == 0:
                cmds.warning("No space name given in entry.")
                return
            if not cmds.objExists(space_object):
                cmds.warning("Invalid space object given in entry.")
                return

            if len(exlusion_list) > 0:
                split_string = exlusion_list.split(", ")
                for split in split_string:
                    if not cmds.objExists(split):
                        cmds.warning("Invalid object given in exclusion list.")
                        return

            # add to space data
            if len(exlusion_list) == 0:
                exlusion_list = None
            else:
                exlusion_list = exlusion_list.split(", ")

            space_data[space_name] = [space_object, exlusion_list]

        # dump to file
        if file_path is None:
            spaces_directory = self._check_for_directory()
            file_path = cmds.fileDialog2(fm=0, okc="Save Template", dir=spaces_directory, ff="*.spaces")
            if file_path is not None:
                file_path = file_path[0]

        f = open(file_path, 'w')
        json.dump(space_data, f)
        f.close()

    def _load_template(self):
        spaces_directory = self._check_for_directory()
        file_path = cmds.fileDialog2(fm=1, okc="Load Template", dir=spaces_directory, ff="*.spaces")
        if file_path is not None:

            json_file = open(file_path[0])
            space_data = json.load(json_file)
            json_file.close()

            # clear existing entries
            while self.scroll_layout.count():
                child = self.scroll_layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()

            # add the spacer item back and reset self.widgets
            self.scroll_layout.addSpacerItem(
                QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))
            self.widgets = {}

            # add a space entry widget for each element in space data
            for each in space_data:
                data = space_data.get(each)
                text = ""
                if data[1] is not None:
                    for obj in data[1]:
                        if obj != data[1][-1]:
                            text += obj + ", "
                        else:
                            text += obj

                self._add_entry(each, data[0], text)

    def _check_for_directory(self):
        user_dir = utils.returnFriendlyPath(os.path.join(self.tools_path, "User"))
        spaces_dir = utils.returnFriendlyPath(os.path.join(user_dir, "Global Space Templates"))

        if not os.path.exists(user_dir):
            try:
                os.makedirs(user_dir)
            except Exception, e:
                cmds.warning(str(e))

        if not os.path.exists(spaces_dir):
            try:
                os.makedirs(spaces_dir)
            except Exception, e:
                cmds.warning(str(e))

        return spaces_dir

    def _generate_spaces(self, close=False):

        # save a temporary template file
        temp_file = os.path.join(cmds.internalVar(utd=True), "global_spaces.spaces")
        self._save_template(temp_file)

        # call on space_switcher.CreateGlobalSpaces, passing inm the temp file
        space_switcher.CreateGlobalSpaces(temp_file)

        if close:
            self.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """
    Instantiates the ART_SpaceSwitcherUI, which provides user interfaces for switching and baking spaces.
    """

    if cmds.window("ART_SpaceSwitcherUI", exists=True):
        cmds.deleteUI("ART_SpaceSwitcherUI", wnd=True)

    gui = ART_SpaceSwitcherUI(interfaceUtils.getMainWindow())
    gui.show()
    return gui


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def create_space(control, uiInst=None):
    """
    Instantiate the ART_CreateSpaceUI.

    :param str control: The control to create the space for.
    :param uiInst: The animation interface instance
    :type: uiInst: QtWidgets.QWidget
    """

    if cmds.window("ART_CreateSpaceUI", exists=True):
        cmds.deleteUI("ART_CreateSpaceUI", wnd=True)

    gui = ART_CreateSpaceUI(control, uiInst, interfaceUtils.getMainWindow())
    gui.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def rename_space(control):
    """
    Instantiate the ART_RenameSpaceWidget.

    :param str control: The control to create the space for.
    """

    if cmds.window("artRenameSpaceWidget", exists=True):
        cmds.deleteUI("artRenameSpaceWidget", wnd=True)

    gui = RenameSpaceWidget(control, interfaceUtils.getMainWindow())
    gui.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def delete_space(control):
    """
    Instantiate the ART_DeleteSpaceWidget.

    :param str control: The control to delete a given space from.
    """

    if cmds.window("artDeleteSpaceWidget", exists=True):
        cmds.deleteUI("artDeleteSpaceWidget", wnd=True)

    gui = DeleteSpaceWidget(control, interfaceUtils.getMainWindow())
    gui.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def create_global_spaces():
    """
    Instantiate the ART_CreateGlobalSpacesUI class.
    """

    if cmds.window("artCreateGlobalSpaceWin", exists=True):
        cmds.deleteUI("artCreateGlobalSpaceWin", wnd=True)

    gui = ART_CreateGlobalSpacesUI(interfaceUtils.getMainWindow())
    gui.show()
