"""
Module containing interface class for the override joint names tool.
"""
from functools import partial
import os

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Tools.Rigging.ART_OverrideJointNames as ojn


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_OverrideJointNames_UI(interfaceUtils.baseWindow):
    """
    Class for creating the interface to access the joint name override functionality, which is used to override the
    default joint names provided by the tools.

    """

    def __init__(self, parent=None):

        super(ART_OverrideJointNames_UI, self).__init__(465, 395, 465, 395, parent)

        self.widgets = []

        self._build_interface()
        self._add_widgets()
        self._populate_ui()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        # set qt object name
        self.setObjectName("ART_OverrideJointNamesWIN")
        self.setWindowTitle("Override Joint Names")

        # create the main widget
        main_widget = QtWidgets.QFrame()
        main_widget.setObjectName("dark")
        self.setCentralWidget(main_widget)

        # create the mainLayout
        self.main_layout = QtWidgets.QVBoxLayout(main_widget)

        # search layout
        search_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(search_layout)

        save_button = QtWidgets.QPushButton()
        save_button.setMinimumSize(QtCore.QSize(32, 32))
        save_button.setMaximumSize(QtCore.QSize(32, 32))
        save_button.setObjectName("save")
        save_button.clicked.connect(self._save_template)
        search_layout.addWidget(save_button)

        load_button = QtWidgets.QPushButton()
        load_button.setMinimumSize(QtCore.QSize(32, 32))
        load_button.setMaximumSize(QtCore.QSize(32, 32))
        load_button.setObjectName("load")
        search_layout.addWidget(load_button)
        load_button.clicked.connect(self._load_template)

        spacer = QtWidgets.QSpacerItem(200, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        search_layout.addItem(spacer)

        self.filter_list = QtWidgets.QComboBox()
        self.filter_list.setObjectName("light")
        for each in ["Show All", "Show Edited", "Show Unedited"]:
            self.filter_list.addItem(each)
        search_layout.addWidget(self.filter_list)
        self.filter_list.currentIndexChanged.connect(self._filter)

        self.search = QtWidgets.QLineEdit()
        self.search.setMinimumWidth(180)
        self.search.setObjectName("light")
        self.search.setPlaceholderText("Search...")
        word_list = self._get_joints()
        completer = QtWidgets.QCompleter(word_list)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.search.setCompleter(completer)
        self.search.editingFinished.connect(self._search)

        search_layout.addWidget(self.search)

        # scroll area
        self.scroll_contents = QtWidgets.QFrame()
        self.scroll_contents.setObjectName("light")
        self.scroll_contents_layout = QtWidgets.QVBoxLayout()

        # button
        self.close_btn = QtWidgets.QPushButton("Save and Close")
        self.close_btn.setObjectName("settings")
        self.close_btn.setMinimumHeight(30)
        self.close_btn.clicked.connect(self._save_and_close)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _add_widgets(self):

        joints = self._get_joints()
        self._build_joint_widgets(joints)

        self.scroll_contents.setLayout(self.scroll_contents_layout)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)
        scroll_area.setWidget(self.scroll_contents)
        self.main_layout.addWidget(self.close_btn)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_joints(self):
        modules = utils.returnRigModules()
        all_bones = []
        for mod in modules:
            joints = cmds.getAttr(mod + ".Created_Bones")
            split_joints = joints.split("::")

            for bone in split_joints:
                if bone != "":
                    all_bones.append(bone)
        return all_bones

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_joint_widgets(self, joints):

        for joint in joints:

            frame = QtWidgets.QFrame()
            frame.setObjectName("light")
            layout = QtWidgets.QHBoxLayout(frame)
            checkbox = QtWidgets.QCheckBox("Override")
            layout.addWidget(checkbox)

            label = QtWidgets.QLabel(joint)
            layout.addWidget(label)

            text_field = QtWidgets.QLineEdit()
            text_field.setEnabled(False)
            text_field.setMinimumWidth(150)
            text_field.setMaximumWidth(150)

            rx = QtCore.QRegExp("^\\S+$")
            validator = QtGui.QRegExpValidator(rx, self)
            text_field.setValidator(validator)
            layout.addWidget(text_field)

            checkbox.setProperty("label", joint)
            checkbox.setProperty("textField", text_field)
            checkbox.setProperty("layout", frame)
            self.widgets.append(checkbox)

            self.scroll_contents_layout.addWidget(frame)
            checkbox.stateChanged.connect(partial(self._enable_overrides, checkbox, text_field))

        spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.scroll_contents_layout.addItem(spacer)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _search(self):

        self.filter_list.setCurrentIndex(0)
        search_text = self.search.text()

        if search_text == "":
            for widget in self.widgets:
                layout = widget.property("layout")
                if layout is not None:
                    layout.setVisible(True)

        for widget in self.widgets:
            label = widget.property("label")
            layout = widget.property("layout")
            if layout is not None:
                layout.setVisible(True)
            if search_text not in label:
                if layout is not None:
                    layout.setVisible(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _filter(self):

        current_text = self.filter_list.currentText()

        if current_text == "Show Edited":

            for widget in self.widgets:
                layout = widget.property("layout")
                layout.setVisible(True)
                if not widget.isChecked():
                    layout.setVisible(False)

        if current_text == "Show Unedited":

            for widget in self.widgets:
                layout = widget.property("layout")
                layout.setVisible(True)
                if widget.isChecked():
                    layout.setVisible(False)

        if current_text == "Show All":

            for widget in self.widgets:
                layout = widget.property("layout")
                layout.setVisible(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _save_template(self):

        user_dir = utils.returnFriendlyPath(os.path.join(self.tools_path, "User"))
        overrides_dir = utils.returnFriendlyPath(os.path.join(user_dir, "Joint Name Overrides"))

        if not os.path.exists(user_dir):
            try:
                os.makedirs(user_dir)
            except Exception, e:
                cmds.warning(str(e))

        if not os.path.exists(overrides_dir):
            try:
                os.makedirs(overrides_dir)
            except Exception, e:
                cmds.warning(str(e))

        # ask for the file name to give the template
        file_name = cmds.fileDialog2(fm=0, okc="Save Template", dir=overrides_dir, ff="*.jno")

        if file_name is not None:
            inst = ojn.ART_OverrideJointNames(overrides=None, file_path=file_name[0])
            inst.save_template()
        else:
            cmds.warning("No valid file name given. Aborting save.")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_template(self):

        user_dir = utils.returnFriendlyPath(os.path.join(self.tools_path, "User"))
        overrides_dir = utils.returnFriendlyPath(os.path.join(user_dir, "Joint Name Overrides"))

        if not os.path.exists(overrides_dir):
            overrides_dir = self.toolsPath

        file_name = cmds.fileDialog2(fm=1, okc="Load Template", dir=overrides_dir, ff="*.jno")
        if file_name is not None:
            inst = ojn.ART_OverrideJointNames(overrides=None, file_path=file_name[0])
            inst.load_template()
        else:
            cmds.warning("No valid file name given. Aborting load.")

        self.populate_UI()
        self.filter_list.setCurrentIndex(0)
        self.filter_list.setCurrentIndex(1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _save_and_close(self):

        overrides = []
        invalidChars = ["!", "?", "/", "#", "@", "$", "%", "^", "&", "*", "(", ")", "{", "}", "[", "]", "|", "\\", ".",
                        ",", "<", ">", "`", "~", "-", "+", "="]

        # go through widgets and find checkboxes that are checked
        errors = []

        for widget in self.widgets:
            if widget.isChecked():
                label = widget.property("label")
                textField = widget.property("textField")
                override_name = textField.text()

                # store that data in a list, where each entry is label. textField.text()
                valid = False
                for each in override_name:
                    if each not in invalidChars:
                        valid = True
                    else:
                        valid = False
                        errors.append([label, override_name])
                        break

                if valid is True:
                    overrides.append([label, override_name])

        # list any name errors
        if len(errors) > 0:

            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("Override names contain invalid characters.")
            informative_string = ""

            for error in errors:
                informative_string += ("Override name: " + error[1] + " for joint: " + error[0] +
                                       " contains invalid characters.\n\n")

            msgBox.setDetailedText(informative_string)
            msgBox.exec_()
            return

        inst = ojn.ART_OverrideJointNames(overrides=overrides, file_path=None)
        inst.save()
        self.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # noinspection PyUnusedLocal
    def _enable_overrides(self, checkBox, textField, *args):
        state = checkBox.isChecked()
        if state is True:
            textField.setEnabled(True)
        if state is False:
            textField.setEnabled(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_ui(self):

        if cmds.objExists("artv2_override_data"):

            attrs = cmds.listAttr("artv2_override_data", ud=True)
            if attrs is not None:
                for each in self.widgets:
                    label = each.property("label")
                    if label in attrs:
                        value = cmds.getAttr("artv2_override_data." + label)
                        text_field = each.property("textField")
                        each.setChecked(True)
                        text_field.setEnabled(True)
                        text_field.setText(value)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """
    Check for an instance of the UI, and if it exists, delete it. Then create a new instance of the UI.
    :return:
    """
    if cmds.window("ART_OverrideJointNamesWIN", exists=True):
        cmds.deleteUI("ART_OverrideJointNamesWIN", wnd=True)

    gui = ART_OverrideJointNames_UI(interfaceUtils.getMainWindow())
    gui.show()
    return gui
