import os
import sys
from functools import partial
import traceback

import maya.cmds as cmds

# noinspection PyUnresolvedReferences
from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils


class ART_Batcher(QtWidgets.QMainWindow):
    """
    This class is used to create an interface to run batch processes on files.
    """

    def __init__(self, parent=None):
        """
        Instantiates the class, gets settings values from QSettings. Calls on building the interface.
        """

        super(ART_Batcher, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")

        self.widgets = {}
        self.error_messages = {}
        self.num_errors = 0
        self.completed = 0

        # build the interface
        self.build_interface()

    def build_interface(self):
        """
        build the interface to setup and run batch processes.
        """
        # set the window size
        self.setMinimumSize(QtCore.QSize(500, 320))
        self.setMaximumSize(QtCore.QSize(500, 320))

        # create the main widget
        self.main_widget = QtWidgets.QFrame()
        self.setCentralWidget(self.main_widget)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)

        # set qt object name
        self.setObjectName("ARTv2_Batcher_Win")
        self.setWindowTitle("ARTv2 Batcher")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # create the mainLayout
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        # load the stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)
        self.main_widget.setStyleSheet(self.style)

        # top section: directory inputs
        input_layout = self.build_directory_widgets("Input Directory:", "input", "")
        # output_layout = self.build_directory_widgets("Output Directory:", "output", "optional")
        script_layout = self.build_directory_widgets("Script:", "script", "", False, True)

        self.main_layout.addLayout(input_layout)
        # self.main_layout.addLayout(output_layout)
        self.main_layout.addLayout(script_layout)

        # file filters
        file_filter_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(file_filter_layout)

        file_filter_label = QtWidgets.QLabel("Operate on:")
        file_filter_layout.addWidget(file_filter_label)

        self.file_filters = QtWidgets.QComboBox()

        index = 0
        for item in [["All Maya Files", [".ma", ".mb"]], ["Maya Ascii Files", [".ma"]],
                     ["Maya Binary Files", [".mb"]], ["FBX Files", [".fbx"]]]:
            self.file_filters.addItem(item[0])
            self.file_filters.setItemData(index, item[1])
            index += 1
        file_filter_layout.addWidget(self.file_filters)

        # replace reference
        reference_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(reference_layout)
        self.replace_reference = QtWidgets.QCheckBox("Replace Reference")

        self.reference_node = QtWidgets.QLineEdit()
        self.reference_node.setPlaceholderText("Reference Node Name...")
        self.new_reference = QtWidgets.QLineEdit()
        self.new_reference.setPlaceholderText("New Reference Path...")
        self.reference_node.setEnabled(False)
        self.new_reference.setEnabled(False)
        self.replace_reference.stateChanged.connect(self.reference_node.setEnabled)
        self.replace_reference.stateChanged.connect(self.new_reference.setEnabled)
        reference_layout.addWidget(self.replace_reference)
        reference_layout.addWidget(self.reference_node)
        reference_layout.addWidget(self.new_reference)

        # status group box
        status_group_box = QtWidgets.QGroupBox("Status")
        status_group_box.setMinimumSize(QtCore.QSize(482, 100))
        status_group_box.setMaximumSize(QtCore.QSize(482, 100))
        self.main_layout.addWidget(status_group_box)

        group_box_layout = QtWidgets.QVBoxLayout(status_group_box)
        status_info_layout = QtWidgets.QHBoxLayout()
        group_box_layout.addLayout(status_info_layout)

        total_files_label = QtWidgets.QLabel("Total Files:")
        self.total_files = QtWidgets.QLabel("")
        completed_files_label = QtWidgets.QLabel("Completed Files:")
        self.completed_files = QtWidgets.QLabel("")
        errors_label = QtWidgets.QLabel("Errors:")
        self.errors = QtWidgets.QPushButton(str(self.num_errors))
        self.errors.setMinimumSize(QtCore.QSize(20, 20))
        self.errors.setMaximumSize(QtCore.QSize(20, 20))
        self.errors.setObjectName("orange")
        self.errors.clicked.connect(self._show_errors)

        status_info_layout.addWidget(total_files_label)
        status_info_layout.addWidget(self.total_files)
        status_info_layout.addWidget(completed_files_label)
        status_info_layout.addWidget(self.completed_files)
        status_info_layout.addWidget(errors_label)
        status_info_layout.addWidget(self.errors)

        self.progress_bar = QtWidgets.QProgressBar()
        group_box_layout.addWidget(self.progress_bar)

        self.status = QtWidgets.QLabel()
        group_box_layout.addWidget(self.status)

        # batch button
        batch_button = QtWidgets.QPushButton("Run Batch")
        batch_button.setMinimumSize(QtCore.QSize(480, 37))
        batch_button.setMaximumSize(QtCore.QSize(480, 37))
        batch_button.setObjectName("settings")
        self.main_layout.addWidget(batch_button)
        batch_button.clicked.connect(self._batch)

    def build_directory_widgets(self, label, key, placeholder_text, directory=True, single_file=False):

        layout = QtWidgets.QHBoxLayout()

        label_widget = QtWidgets.QLabel(label)
        label_widget.setMinimumSize(QtCore.QSize(100, 30))
        label_widget.setMaximumSize(QtCore.QSize(100, 30))
        layout.addWidget(label_widget)

        text_field = QtWidgets.QLineEdit()
        text_field.setMinimumSize(QtCore.QSize(342, 22))
        text_field.setMaximumSize(QtCore.QSize(342, 22))
        text_field.setEnabled(False)
        text_field.setPlaceholderText(placeholder_text)
        layout.addWidget(text_field)
        self.widgets[key] = text_field

        browse_button = QtWidgets.QPushButton()
        browse_button.setMinimumSize(QtCore.QSize(30, 30))
        browse_button.setMaximumSize(QtCore.QSize(30, 30))
        browse_button.setObjectName("load")
        layout.addWidget(browse_button)
        browse_button.clicked.connect(partial(self._browse, directory, single_file, text_field))

        return layout

    def _browse(self, directory, single_file, text_field):

        nice_path = None
        if directory:
            path = cmds.fileDialog2(fm=3)
            if path is not None:
                nice_path = utils.returnFriendlyPath(path[0])
        if single_file:
            path = cmds.fileDialog2(fm=1, ff="*.py;;*.mel")
            if path is not None:
                nice_path = utils.returnFriendlyPath(path[0])

        if nice_path is not None:
            text_field.setText(nice_path)

    def _gather_info(self):

        file_filter = self.file_filters.currentIndex()
        file_filters = self.file_filters.itemData(file_filter)

        input_text_field = self.widgets.get("input")
        input_directory = input_text_field.text()

        all_files = os.listdir(input_directory)
        self.files = []

        for each in all_files:
            if os.path.isfile(os.path.join(input_directory, each)):
                if os.path.splitext(each)[1] in file_filters:
                    self.files.append(utils.returnFriendlyPath(os.path.join(input_directory, each)))

        self.total_files.setText(str(len(self.files)))
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(self.files))

    def _batch(self):
        self._gather_info()
        script_text_field = self.widgets.get("script")
        script = script_text_field.text()
        script_path = os.path.dirname(script)
        sys.path.append(script_path)

        # go through each file, open the file, run the script, increment status info
        for each in self.files:
            self.status.setText("working on: " + str(each))
            try:
                if self.replace_reference.isChecked():
                    cmds.file(each, open=True, force=True, ignoreVersion=True, lrd="none", prompt=False)
                    # cmds.file(r"{0}".format(self.new_reference.text()), loadReference=self.reference_node.text())
                else:
                    cmds.file(each, open=True, force=True, ignoreVersion=True)
                cmds.refresh()
                self._execute(script)

            except StandardError:
                self.error_messages[each] = traceback.format_exc()
                self.num_errors += 1
                self.errors.setText(str(self.num_errors))

            self.completed += 1
            self.completed_files.setText(str(self.completed))
            self.progress_bar.setValue(self.completed)

    def _execute(self, script):

        sourceType = ""
        if script.find(".py") != -1:
            sourceType = "python"

        if script.find(".mel") != -1:
            sourceType = "mel"

        # MEL
        if sourceType == "mel":
            command = ""
            f = open(script, 'r')
            lines = f.readlines()
            for line in lines:
                command += line

            import maya.mel as mel
            mel.eval(command)

        # PYTHON
        if sourceType == "python":
            exec(open(script).read(), globals(), globals())

    def _show_errors(self):
        window = QtWidgets.QDialog(interfaceUtils.getMainWindow())

        scroll = QtWidgets.QTextEdit()
        scroll.setMinimumSize(QtCore.QSize(400, 300))
        scroll.setMaximumSize(QtCore.QSize(400, 300))

        for each in self.error_messages:
            scroll.append("####Error:")
            scroll.append("File: " + each)
            scroll.append("\n")
            scroll.append(self.error_messages.get(each))
            scroll.append("\n\n")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll)
        window.setLayout(layout)
        window.show()


def art_batcher_ui():
    if cmds.window("ARTv2_Batcher_Win", exists=True):
        cmds.deleteUI("ARTv2_Batcher_Win", wnd=True)
    gui = ART_Batcher(interfaceUtils.getMainWindow())
    gui.show()
