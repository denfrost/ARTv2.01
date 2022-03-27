import json
import os
from functools import partial

import maya.OpenMaya as openMaya
import maya.OpenMayaUI as mui
import maya.cmds as cmds

import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatibility
try:
    import shiboken as shiboken
except ImportError:
    import shiboken2 as shiboken


class ART_Publish():

    def __init__(self, rig_interface_instance):

        # publish file info
        self.publish_file_info = []
        self.current_module = None

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.tools_path = settings.value("toolsPath")
        self.project_path = settings.value("projectPath")
        self.icons_path = settings.value("iconPath")
        self.rig_interface_instance = rig_interface_instance

        # build the UI
        if cmds.window("ART_PublishWin", exists=True):
            cmds.deleteUI("ART_PublishWin", wnd=True)

        # create model poses
        for inst in self.rig_interface_instance.moduleInstances:
            if inst.name != "root":
                inst.aimMode_Setup(False)
                inst.setupForRigPose(store=True)
                inst.getReferencePose("modelPose")
                inst.cleanUpRigPose()

        self._build_interface()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        # create the main window
        self.window = QtWidgets.QMainWindow(self.rig_interface_instance)
        self.window.closeEvent = self.close_window
        window_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/logo.png"))
        self.window.setWindowIcon(window_icon)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.window.setStyleSheet(self.style)

        # create the main widget
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setStyleSheet(self.style)
        self.window.setCentralWidget(self.central_widget)

        # set qt object name
        self.window.setObjectName("ART_PublishWin")
        self.window.setWindowTitle("Publish")

        # font
        header_font = QtGui.QFont()
        header_font.setPointSize(8)
        header_font.setBold(True)

        # set size policy
        main_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # create the menu bar
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.setMaximumHeight(20)
        self.layout.addWidget(self.menu_bar)

        # add items to menu bar
        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction("Help On Publish..", self.publishHelp)
        help_menu.addAction("Help On Create Rig Pose..", self.rigPoseHelp)

        self.window.resize(600, 400)
        self.window.setSizePolicy(main_size_policy)
        self.window.setMinimumSize(QtCore.QSize(600, 400))
        self.window.setMaximumSize(QtCore.QSize(600, 400))

        # Create a stackedWidget
        self.stack_widget = QtWidgets.QStackedWidget()
        self.layout.addWidget(self.stack_widget)

        # build pages
        self._create_info_widget()
        self._create_project_widget()
        self.createRigPosePage()
        self.createMeshSlicerPage()
        self.createThumbnailCreatorPage()
        self.createSummaryPage()

        # show window
        self.window.show()
        self.stack_widget.setCurrentIndex(0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_info_widget(self):

        self.info_widget = QtWidgets.QFrame()
        self.stack_widget.addWidget(self.info_widget)
        self.info_widget_layout = QtWidgets.QVBoxLayout(self.info_widget)
        self.info_widget.setStyleSheet(self.style)

        info_label = QtWidgets.QLabel("Publish Your Rig")
        info_label.setStyleSheet("background: transparent;")
        self.info_widget_layout.addWidget(info_label)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        info_label.setFont(font)

        self.info_frame = QtWidgets.QFrame()
        self.info_frame.setMinimumSize(QtCore.QSize(560, 250))
        self.info_frame.setMaximumSize(QtCore.QSize(560, 250))
        self.info_widget_layout.addWidget(self.info_frame)

        image = utils.returnFriendlyPath(os.path.join(self.icons_path, "System/backgrounds/publishInfo.png"))
        self.info_frame.setStyleSheet("background-image: url(" + image + ");")

        self.info_button_layout = QtWidgets.QHBoxLayout()
        self.info_widget_layout.addLayout(self.info_button_layout)
        
        self.info_widget_cancel_button = QtWidgets.QPushButton("Cancel")
        self.info_widget_cancel_button.setMinimumHeight(50)
        self.info_widget_cancel_button.setFont(font)
        self.info_widget_cancel_button.setObjectName("settings")
        self.info_button_layout.addWidget(self.info_widget_cancel_button)
        self.info_widget_cancel_button.clicked.connect(partial(self.cancelPublish))
        
        self.info_widget_continue_button = QtWidgets.QPushButton("Continue")
        self.info_widget_continue_button.setMinimumHeight(50)
        self.info_widget_continue_button.setFont(font)
        self.info_widget_continue_button.setObjectName("settings")
        self.info_button_layout.addWidget(self.info_widget_continue_button)
        self.info_widget_continue_button.clicked.connect(partial(self.continueToProject))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_project_widget(self):

        # create the QFrame for this page
        project_widget = QtWidgets.QFrame()
        self.stack_widget.addWidget(project_widget)
        project_widget_layout = QtWidgets.QHBoxLayout(project_widget)
        project_widget.setStyleSheet(self.style)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        # the HBoxLayout will have 2 VBoxLayouts
        project_widget_left_column = QtWidgets.QVBoxLayout()
        project_widget_right_column = QtWidgets.QVBoxLayout()
        project_widget_layout.addLayout(project_widget_left_column)
        project_widget_layout.addLayout(project_widget_right_column)

        # #Left Column # #
        # 2 HBox children that contain comboBox + pushButton, listWidget that lists characters in that project/group
        self.directory_tree = QtWidgets.QTreeWidget()
        self.directory_tree.setMinimumSize(QtCore.QSize(250, 250))
        self.directory_tree.setMaximumSize(QtCore.QSize(250, 250))

        self.header_text = os.path.basename(self.project_path)

        header = QtWidgets.QTreeWidgetItem([self.header_text + ":"])
        self.directory_tree.setHeaderItem(header)
        project_widget_left_column.addWidget(self.directory_tree)
        self.directory_tree.setColumnWidth(0, 240)
        self.directory_tree.itemSelectionChanged.connect(self._update_project_path)

        # populate tree
        self.populateProjects()

        # create buttons for adding new project and adding new directories
        add_project_button = QtWidgets.QPushButton("Add New Project")
        add_project_button.setMinimumSize(QtCore.QSize(250, 30))
        add_project_button.setMaximumSize(QtCore.QSize(250, 30))
        add_project_button.setObjectName("settings")
        project_widget_left_column.addWidget(add_project_button)
        add_project_button.clicked.connect(partial(self.addNewProject, True))

        add_project_dir_button = QtWidgets.QPushButton("Add New Directory to Project")
        add_project_dir_button.setMinimumSize(QtCore.QSize(250, 30))
        add_project_dir_button.setMaximumSize(QtCore.QSize(250, 30))
        add_project_dir_button.setObjectName("settings")
        project_widget_left_column.addWidget(add_project_dir_button)
        add_project_dir_button.clicked.connect(self.addNewProjectDirectory)

        # RIGHT COLUMN
        self.path_label = QtWidgets.QLabel(self.header_text + "/")
        project_widget_right_column.addWidget(self.path_label)

        self.character_name = QtWidgets.QLineEdit()
        project_widget_right_column.addWidget(self.character_name)
        self.character_name.setMinimumHeight(50)
        self.character_name.setMaximumHeight(50)
        self.character_name.setPlaceholderText("Asset Name")
        self.character_name.setAlignment(QtCore.Qt.AlignCenter)
        spacer_item = QtWidgets.QSpacerItem(20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        project_widget_right_column.addItem(spacer_item)
        self.character_name.setToolTip("Name the asset will be published with.")

        # character node
        character_node = utils.returnCharacterModule()
        attrs = cmds.listAttr(character_node, ud=True)

        # select character, if applicable
        version = 0
        for attr in attrs:
            if attr.find("version") == 0:
                version = cmds.getAttr(character_node + ".version")

        if version > 0:
            version_group_box = QtWidgets.QGroupBox("Versioning")
            version_group_box.setMinimumSize(QtCore.QSize(300, 130))
            version_group_box.setMaximumSize(QtCore.QSize(300, 130))
            version_group_box.setCheckable(True)
            project_widget_right_column.addWidget(version_group_box)
            version_group_box.toggled.connect(partial(self.toggle_version_layout, version_group_box))

            group_box_layout = QtWidgets.QVBoxLayout(version_group_box)

            # change type (for versioning)
            revision_type_layout = QtWidgets.QHBoxLayout()
            group_box_layout.addLayout(revision_type_layout)

            label = QtWidgets.QLabel("Change Type:")
            label.setStyleSheet("background: transparent;")
            revision_type_layout.addWidget(label)
            self.revision_type = QtWidgets.QComboBox()
            revision_type_layout.addWidget(self.revision_type)

            self.revision_type.addItem("Cosmetic Change")
            self.revision_type.addItem("Minor Change")
            self.revision_type.addItem("Major Change")
            self.revision_type.setToolTip("The type of change that was done, leading to a republish.")

            # add note box for revision
            revision_note_label = QtWidgets.QLabel("Revision Note (optional):")
            revision_note_label.setStyleSheet("background: transparent;")
            group_box_layout.addWidget(revision_note_label)

            self.revision_note = QtWidgets.QTextEdit()
            group_box_layout.addWidget(self.revision_note)

        self.project_spacer_item = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum,
                                                         QtWidgets.QSizePolicy.Minimum)
        project_widget_right_column.addItem(self.project_spacer_item)

        # pre script
        pre_script_layout = QtWidgets.QHBoxLayout()
        project_widget_right_column.addLayout(pre_script_layout)

        self.pre_script_line_edit = QtWidgets.QLineEdit()
        self.pre_script_line_edit.setMinimumHeight(24)
        self.pre_script_line_edit.setMaximumHeight(24)
        self.pre_script_line_edit.setPlaceholderText("Pre-Script (optional)")
        pre_script_layout.addWidget(self.pre_script_line_edit)
        self.pre_script_line_edit.setToolTip(
            "If you want to run any custom code before the rig is built, load in a MEL or Python script here.")

        pre_script_browse_button = QtWidgets.QPushButton()
        pre_script_layout.addWidget(pre_script_browse_button)
        pre_script_browse_button.setMinimumSize(24, 24)
        pre_script_browse_button.setMaximumSize(24, 24)
        pre_script_browse_button.clicked.connect(partial(self.addCustomScripts, True, False))
        icon = QtGui.QIcon(os.path.join(self.icons_path, "System/fileBrowse.png"))
        pre_script_browse_button.setIconSize(QtCore.QSize(24, 24))
        pre_script_browse_button.setIcon(icon)
        pre_script_browse_button.setObjectName("settings")

        # post script
        post_script_layout = QtWidgets.QHBoxLayout()
        project_widget_right_column.addLayout(post_script_layout)

        self.post_script_line_edit = QtWidgets.QLineEdit()
        self.post_script_line_edit.setMinimumHeight(24)
        self.post_script_line_edit.setMaximumHeight(24)
        self.post_script_line_edit.setPlaceholderText("Post-Script (optional)")
        post_script_layout.addWidget(self.post_script_line_edit)
        self.post_script_line_edit.setToolTip(
            "If you want to run any custom code after the rig is built, load in a MEL or Python script here.")

        post_script_browse_button = QtWidgets.QPushButton()
        post_script_layout.addWidget(post_script_browse_button)
        post_script_browse_button.setMinimumSize(24, 24)
        post_script_browse_button.setMaximumSize(24, 24)
        post_script_browse_button.clicked.connect(partial(self.addCustomScripts, False, True))
        icon = QtGui.QIcon(os.path.join(self.icons_path, "System/fileBrowse.png"))
        post_script_browse_button.setIconSize(QtCore.QSize(24, 24))
        post_script_browse_button.setIcon(icon)
        post_script_browse_button.setObjectName("settings")

        spacer_item = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        project_widget_right_column.addItem(spacer_item)

        # continue btn
        continue_to_rig_pose_button = QtWidgets.QPushButton("Continue")
        continue_to_rig_pose_button.setFont(font)
        continue_to_rig_pose_button.setMinimumHeight(50)
        continue_to_rig_pose_button.setMaximumHeight(50)
        project_widget_right_column.addWidget(continue_to_rig_pose_button)
        continue_to_rig_pose_button.clicked.connect(self.createNewCharacter)
        continue_to_rig_pose_button.setObjectName("settings")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createRigPosePage(self):

        # create the QFrame for this page
        self.rigPosePage = QtWidgets.QFrame()
        self.rigPosePage.setMinimumSize(560, 250)
        self.stack_widget.addWidget(self.rigPosePage)
        self.rpPageMainLayout = QtWidgets.QHBoxLayout(self.rigPosePage)
        self.rigPosePage.setStyleSheet(self.style)
        self.rigPosePage.setObjectName("dark")

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        # the HBoxLayout will have 2 VBoxLayouts
        self.rpPageLeftColumn = QtWidgets.QVBoxLayout()
        self.rpPageRightColumn = QtWidgets.QVBoxLayout()
        self.rpPageMainLayout.addLayout(self.rpPageLeftColumn)
        self.rpPageMainLayout.addLayout(self.rpPageRightColumn)

        # left column (list of modules, back button)
        self.rpPage_moduleList = QtWidgets.QListWidget()
        self.rpPage_moduleList.setMinimumSize(200, 280)
        self.rpPage_moduleList.setMaximumSize(200, 280)
        self.rpPageLeftColumn.addWidget(self.rpPage_moduleList)
        self.rpPage_moduleList.setToolTip(
            "This list of modules make up your character."
            " Select a module from the list to alter the rig pose for that module.\n\n"
            " A rig pose is the ideal pose for each\nmodule for rigging."
            " For legs, this means that\nthe leg is coplanar for the IK solve and\nthe feet are aligned to the world."
            " \n\nFor arms, the same. It's the T-Pose that's\nbest suited to building the rig,"
            " since models\nare not always built in that pose.")

        self.rpPage_moduleList.setFont(font)
        self.rpPage_moduleList.setSpacing(3)

        # populate list
        modules = utils.returnRigModules()
        for mod in modules:
            name = cmds.getAttr(mod + ".moduleName")
            if name != "root":
                self.rpPage_moduleList.addItem(name)

        self.rpPage_moduleList.itemClicked.connect(self.moduleSelected)

        # button layout
        self.rpPage_leftButtonLayout = QtWidgets.QHBoxLayout()
        self.rpPageLeftColumn.addLayout(self.rpPage_leftButtonLayout)
        self.rpPage_leftButtonLayout.setContentsMargins(0, 0, 100, 0)

        # button/spacer
        self.rpPage_backButton = QtWidgets.QPushButton("Back")
        self.rpPage_leftButtonLayout.addWidget(self.rpPage_backButton)
        self.rpPage_backButton.setFont(font)
        self.rpPage_backButton.setMinimumHeight(50)
        self.rpPage_backButton.setMaximumHeight(50)
        self.rpPage_backButton.clicked.connect(self.backToProject)
        self.rpPage_backButton.setObjectName("settings")

        # right column (scrollArea for module settings)

        # scroll area contents
        self.rpPage_scrollContents = QtWidgets.QFrame()
        scrollSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.rpPage_scrollContents.setSizePolicy(scrollSizePolicy)
        self.rpPage_scrollContents.setObjectName("dark")

        # scroll area
        self.rpPage_Settings = QtWidgets.QScrollArea()
        self.rpPage_Settings.setMinimumSize(350, 280)
        self.rpPage_Settings.setMaximumSize(350, 280)
        self.rpPageRightColumn.addWidget(self.rpPage_Settings)
        self.rpPage_Settings.setWidgetResizable(True)
        self.rpPage_Settings.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.rpPage_Settings.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.rpPage_Settings.setWidget(self.rpPage_scrollContents)

        # layout for scroll area
        self.rpPage_layout = QtWidgets.QVBoxLayout(self.rpPage_scrollContents)

        # stacked widget
        self.rpPage_stackWidget = QtWidgets.QStackedWidget()
        self.rpPage_layout.addWidget(self.rpPage_stackWidget)

        # message
        self.message = QtWidgets.QLabel("Select a module from the list to adjust the rig pose for that module.")
        self.message.setStyleSheet("background: transparent;")
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.rpPage_stackWidget.addWidget(self.message)

        # button layout
        self.rpPage_righttButtonLayout = QtWidgets.QHBoxLayout()
        self.rpPageRightColumn.addLayout(self.rpPage_righttButtonLayout)
        self.rpPage_righttButtonLayout.setContentsMargins(100, 0, 0, 0)

        # button/spacer
        self.rpPage_continueButton = QtWidgets.QPushButton("Continue")
        self.rpPage_righttButtonLayout.addWidget(self.rpPage_continueButton)
        self.rpPage_continueButton.setFont(font)
        self.rpPage_continueButton.setMinimumHeight(50)
        self.rpPage_continueButton.setMaximumHeight(50)
        self.rpPage_continueButton.clicked.connect(partial(self.continueToCreateAnimMesh))
        self.rpPage_continueButton.setObjectName("settings")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createMeshSlicerPage(self):

        # create the QFrame for this page
        self.meshSlicerPage = QtWidgets.QFrame()
        self.meshSlicerPage.setMinimumSize(560, 250)
        self.stack_widget.addWidget(self.meshSlicerPage)
        self.msPageMainLayout = QtWidgets.QVBoxLayout(self.meshSlicerPage)

        # info page styling
        self.meshSlicerPage.setStyleSheet(self.style)
        self.meshSlicerPage.setObjectName("dark")

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        # create the label for the instructional gif
        self.movie_screen = QtWidgets.QLabel()

        # expand and center the label
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.msPageMainLayout.addWidget(self.movie_screen)

        # set movie from file path
        gif = utils.returnFriendlyPath(os.path.join(self.icons_path, "Help/meshSlicer.gif"))
        self.movie = QtGui.QMovie(gif, QtCore.QByteArray())
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)

        # button layout
        self.msPageButtonLayout = QtWidgets.QHBoxLayout()
        self.msPageMainLayout.addLayout(self.msPageButtonLayout)

        self.msPageBackBtn = QtWidgets.QPushButton("Back")
        self.msPageBackBtn.setMinimumHeight(50)
        self.msPageBackBtn.setFont(font)
        self.msPageBackBtn.clicked.connect(partial(self.backToRigPose))
        self.msPageBackBtn.setObjectName("settings")

        self.msPageSkipBtn = QtWidgets.QPushButton("Skip")
        self.msPageSkipBtn.setMinimumHeight(50)
        self.msPageSkipBtn.setFont(font)
        self.msPageSkipBtn.clicked.connect(partial(self.skipToCreateThumbnail))
        self.msPageSkipBtn.setObjectName("settings")

        self.mePageContBtn = QtWidgets.QPushButton("Continue")
        self.mePageContBtn.setMinimumHeight(50)
        self.mePageContBtn.setFont(font)
        self.mePageContBtn.clicked.connect(partial(self.continueToCreateThumbnail))
        self.mePageContBtn.setObjectName("settings")

        self.msPageButtonLayout.addWidget(self.msPageBackBtn)
        spacer = QtWidgets.QSpacerItem(200, 20)
        self.msPageButtonLayout.addSpacerItem(spacer)
        self.msPageButtonLayout.addWidget(self.msPageSkipBtn)
        self.msPageButtonLayout.addWidget(self.mePageContBtn)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createThumbnailCreatorPage(self):

        # create the QFrame for this page
        self.thumbCreatorPage = QtWidgets.QFrame()
        self.thumbCreatorPage.setMinimumSize(560, 250)
        self.stack_widget.addWidget(self.thumbCreatorPage)
        self.tcPageMainLayout = QtWidgets.QVBoxLayout(self.thumbCreatorPage)

        # info page styling
        self.thumbCreatorPage.setStyleSheet(self.style)

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)

        buttonFont = QtGui.QFont()
        buttonFont.setPointSize(12)
        buttonFont.setBold(True)

        # viewport and tabs layout
        self.tcPageViewportLayout = QtWidgets.QHBoxLayout()
        self.tcPageMainLayout.addLayout(self.tcPageViewportLayout)
        self.viewportToggle = QtWidgets.QStackedWidget()
        self.viewportToggle.setMinimumSize(200, 200)
        self.viewportToggle.setMaximumSize(200, 200)
        self.tcPageViewportLayout.addWidget(self.viewportToggle)

        # custom image loaded
        self.customImg = QtWidgets.QFrame()
        self.customImg.setObjectName("darkborder")
        self.customImg.setMinimumSize(200, 200)
        self.customImg.setMaximumSize(200, 200)
        self.viewportToggle.addWidget(self.customImg)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.customImg)
        shadow.setBlurRadius(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.customImg.setGraphicsEffect(shadow)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # first element in this layout is our viewport

        # create the camera for the viewport
        self.thumbnailCamera = cmds.camera(name="thumbnail_camera")[0]
        cmds.parentConstraint("persp", self.thumbnailCamera)
        cmds.setAttr(self.thumbnailCamera + ".v", 0)
        cmds.lockNode(self.thumbnailCamera, lock=True)

        # create light rig
        self.lightGrp = cmds.group(empty=True, name="thumbnail_lights")

        # key light
        self.spot1 = cmds.spotLight(rgb=(.902, .785, .478), name="thumbnail_spot1", ca=100, do=1)
        cmds.setAttr(self.spot1 + ".useDepthMapShadows", 1)
        self.spot1Parent = cmds.listRelatives(self.spot1, parent=True)[0]
        cmds.setAttr(self.spot1Parent + ".tx", 150)
        cmds.setAttr(self.spot1Parent + ".ty", -150)
        cmds.setAttr(self.spot1Parent + ".tz", 300)
        aim = \
        cmds.aimConstraint("root", self.spot1Parent, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType="scene")[0]
        cmds.delete(aim)

        # bounce light
        self.spot2 = cmds.spotLight(rgb=(.629, .799, .949), name="thumbnail_spot2", ca=100, do=1)
        cmds.setAttr(self.spot2 + ".useDepthMapShadows", 1)
        self.spot2Parent = cmds.listRelatives(self.spot2, parent=True)[0]
        cmds.setAttr(self.spot2Parent + ".tx", -150)
        cmds.setAttr(self.spot2Parent + ".ty", -150)
        cmds.setAttr(self.spot2Parent + ".tz", 300)
        aim = \
        cmds.aimConstraint("root", self.spot2Parent, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType="scene")[0]
        cmds.delete(aim)

        # fill light
        self.spot3 = cmds.spotLight(rgb=(1, 1, 1), name="thumbnail_spot3", ca=100, do=1)
        cmds.setAttr(self.spot3 + ".useDepthMapShadows", 1)
        self.spot3Parent = cmds.listRelatives(self.spot3, parent=True)[0]
        cmds.setAttr(self.spot3Parent + ".tx", 0)
        cmds.setAttr(self.spot3Parent + ".ty", 150)
        cmds.setAttr(self.spot3Parent + ".tz", 300)
        aim = \
        cmds.aimConstraint("root", self.spot3Parent, aimVector=[0, 0, -1], upVector=[0, 1, 0], worldUpType="scene")[0]
        cmds.delete(aim)

        cmds.parent([self.spot1Parent, self.spot2Parent, self.spot3Parent], self.lightGrp)

        cmds.lockNode(self.spot1Parent, lock=True)
        cmds.lockNode(self.spot2Parent, lock=True)
        cmds.lockNode(self.spot3Parent, lock=True)
        cmds.lockNode(self.lightGrp, lock=True)

        # model editor
        self.tcViewport = cmds.modelEditor(camera=self.thumbnailCamera, dl="all", da="smoothShaded", hud=False,
                                           gr=False, dtx=True, sdw=True, j=False, ca=False, lt=False)
        pointer = mui.MQtUtil.findControl(self.tcViewport)
        self.tcViewWidget = shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)
        self.viewportToggle.addWidget(self.tcViewWidget)
        self.tcViewWidget.setMinimumSize(200, 200)
        self.tcViewWidget.setMaximumSize(200, 200)
        self.viewportToggle.setCurrentIndex(1)

        # add image plane with image
        imagePlanePath = utils.returnFriendlyPath(os.path.join(self.icons_path, "System/backgrounds/imagePlane.png"))
        self.imagePlane = cmds.imagePlane(fn=imagePlanePath, c=self.thumbnailCamera, lt=self.thumbnailCamera, sia=False)
        cmds.setAttr(self.imagePlane[1] + ".depth", 3000)
        cmds.setAttr(self.imagePlane[1] + ".sizeX", 2)
        cmds.setAttr(self.imagePlane[1] + ".sizeY", 2)

        # second element in this layout is a tabWidget

        # tab stylesheet (tab stylesheet via QSS doesn't seem to work for some reason
        self.tab_style = interfaceUtils.get_style_sheet("tabs")
        self.tcPageTabs = QtWidgets.QTabWidget()
        self.tcPageTabs.setStyleSheet(self.tab_style)
        self.tcPageViewportLayout.addWidget(self.tcPageTabs)
        self.tcPageTabs.setMinimumHeight(200)
        self.tcPageTabs.setMaximumHeight(200)

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # rendering tab
        self.renderTab = QtWidgets.QFrame()
        self.renderTab.setObjectName("light")
        self.tcPageTabs.addTab(self.renderTab, "LIGHT OPTIONS")

        # rendering tab main layout
        self.renderTabLayout = QtWidgets.QHBoxLayout(self.renderTab)
        self.renderTabLayout.setSpacing(10)

        # left column of render tab options
        self.renderTabLeft = QtWidgets.QVBoxLayout()
        self.renderTabLayout.addLayout(self.renderTabLeft)

        icon = utils.returnFriendlyPath(os.path.join(self.icons_path, "System/spotLight.png"))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # light 1
        self.light1Layout = QtWidgets.QHBoxLayout()
        self.renderTabLeft.addLayout(self.light1Layout)

        self.light1Img = QtWidgets.QLabel("")
        self.light1Img.setFont(font)
        self.light1Img.setMinimumSize(40, 40)
        self.light1Img.setMaximumSize(40, 40)
        self.light1Img.setStyleSheet("background-image: url(" + icon + "); border: black solid 0px;")
        self.light1Layout.addWidget(self.light1Img)

        self.light1Dial = QtWidgets.QDial()
        self.light1Dial.setToolTip("Light Intensity")
        self.light1Layout.addWidget(self.light1Dial)
        self.light1Dial.setMinimumSize(50, 50)
        self.light1Dial.setMaximumSize(50, 50)
        self.light1Dial.setRange(0, 100)
        self.light1Dial.setValue(50)
        shadow1 = QtWidgets.QGraphicsDropShadowEffect(self.light1Dial)
        shadow1.setBlurRadius(5)
        shadow1.setColor(QtGui.QColor(0, 0, 0, 255))
        self.light1Dial.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.light1Dial.setGraphicsEffect(shadow1)
        self.light1Dial.valueChanged.connect(partial(self.changeLightIntensity, self.spot1, self.light1Dial))

        self.light1Swatch = QtWidgets.QPushButton("Color")
        self.light1Swatch.setObjectName("settings")
        self.light1Layout.addWidget(self.light1Swatch)
        self.light1Swatch.setMinimumSize(60, 30)
        self.light1Swatch.setMaximumSize(60, 30)
        self.light1Swatch.setFont(buttonFont)
        self.light1Swatch.setStyleSheet("color: rgb(230, 200, 122);")
        shadow2 = QtWidgets.QGraphicsDropShadowEffect(self.light1Swatch)
        shadow2.setBlurRadius(5)
        shadow2.setColor(QtGui.QColor(0, 0, 0, 255))
        self.light1Swatch.setGraphicsEffect(shadow2)
        self.light1Swatch.clicked.connect(partial(self.changeLightColor, self.spot1, self.light1Swatch))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # light 2
        self.light2Layout = QtWidgets.QHBoxLayout()
        self.renderTabLeft.addLayout(self.light2Layout)

        self.light2Img = QtWidgets.QLabel("")
        self.light2Img.setFont(font)
        self.light2Img.setMinimumSize(40, 40)
        self.light2Img.setMaximumSize(40, 40)
        self.light2Img.setStyleSheet("background-image: url(" + icon + "); border: black solid 0px;")
        self.light2Layout.addWidget(self.light2Img)

        self.light2Dial = QtWidgets.QDial()
        self.light2Dial.setToolTip("Light Intensity")
        self.light2Layout.addWidget(self.light2Dial)
        self.light2Dial.setMinimumSize(50, 50)
        self.light2Dial.setMaximumSize(50, 50)
        self.light2Dial.setRange(0, 100)
        self.light2Dial.setValue(50)
        shadow1 = QtWidgets.QGraphicsDropShadowEffect(self.light2Dial)
        shadow1.setBlurRadius(5)
        shadow1.setColor(QtGui.QColor(0, 0, 0, 255))
        self.light2Dial.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.light2Dial.setGraphicsEffect(shadow1)
        self.light2Dial.valueChanged.connect(partial(self.changeLightIntensity, self.spot2, self.light2Dial))

        self.light2Swatch = QtWidgets.QPushButton("Color")
        self.light2Swatch.setObjectName("settings")
        self.light2Layout.addWidget(self.light2Swatch)
        self.light2Swatch.setMinimumSize(60, 30)
        self.light2Swatch.setMaximumSize(60, 30)
        self.light2Swatch.setFont(buttonFont)
        self.light2Swatch.setStyleSheet("color: rgb(160, 204, 242);")
        shadow2 = QtWidgets.QGraphicsDropShadowEffect(self.light2Swatch)
        shadow2.setBlurRadius(5)
        shadow2.setColor(QtGui.QColor(0, 0, 0, 255))
        self.light2Swatch.setGraphicsEffect(shadow2)
        self.light2Swatch.clicked.connect(partial(self.changeLightColor, self.spot2, self.light2Swatch))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # light 3
        self.light3Layout = QtWidgets.QHBoxLayout()
        self.renderTabLeft.addLayout(self.light3Layout)

        self.light3Img = QtWidgets.QLabel("")
        self.light3Img.setFont(font)
        self.light3Img.setMinimumSize(40, 40)
        self.light3Img.setMaximumSize(40, 40)
        self.light3Img.setStyleSheet("background-image: url(" + icon + "); border: black solid 0px;")
        self.light3Layout.addWidget(self.light3Img)

        self.light3Dial = QtWidgets.QDial()
        self.light3Dial.setToolTip("Light Intensity")
        self.light3Layout.addWidget(self.light3Dial)
        self.light3Dial.setMinimumSize(50, 50)
        self.light3Dial.setMaximumSize(50, 50)
        self.light3Dial.setRange(0, 100)
        self.light3Dial.setValue(50)
        shadow1 = QtWidgets.QGraphicsDropShadowEffect(self.light3Dial)
        shadow1.setBlurRadius(5)
        shadow1.setColor(QtGui.QColor(0, 0, 0, 255))
        self.light3Dial.setStyleSheet("background-color: rgb(60, 60, 60);")
        self.light3Dial.setGraphicsEffect(shadow1)
        self.light3Dial.valueChanged.connect(partial(self.changeLightIntensity, self.spot3, self.light3Dial))

        self.light3Swatch = QtWidgets.QPushButton("Color")
        self.light3Layout.addWidget(self.light3Swatch)
        self.light3Swatch.setObjectName("settings")
        self.light3Swatch.setMinimumSize(60, 30)
        self.light3Swatch.setMaximumSize(60, 30)
        self.light3Swatch.setFont(buttonFont)
        self.light3Swatch.setStyleSheet("color: rgb(255, 255, 255);")
        shadow2 = QtWidgets.QGraphicsDropShadowEffect(self.light3Swatch)
        shadow2.setBlurRadius(5)
        shadow2.setColor(QtGui.QColor(0, 0, 0, 255))
        self.light3Swatch.setGraphicsEffect(shadow2)
        self.light3Swatch.clicked.connect(partial(self.changeLightColor, self.spot3, self.light3Swatch))

        # right column
        self.renderTabRight = QtWidgets.QVBoxLayout()
        self.renderTabLayout.addLayout(self.renderTabRight)

        # orbit layout
        self.orbitLayout = QtWidgets.QHBoxLayout()
        self.renderTabRight.addLayout(self.orbitLayout)

        label = QtWidgets.QLabel("Orbit: ")
        label.setStyleSheet("background: transparent;")
        label.setFont(buttonFont)
        label.setMinimumHeight(30)
        label.setMaximumHeight(30)
        self.orbitLayout.addWidget(label)

        self.orbitDial = QtWidgets.QDial()
        self.orbitDial.setToolTip("Light Rig Position")
        self.orbitLayout.addWidget(self.orbitDial)
        self.orbitDial.setMinimumSize(75, 75)
        self.orbitDial.setMaximumSize(75, 75)
        self.orbitDial.setRange(0, 360)
        self.orbitDial.setValue(0)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.orbitDial)
        shadow.setBlurRadius(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.orbitDial.setGraphicsEffect(shadow)
        self.orbitDial.valueChanged.connect(partial(self.orbitLights, self.lightGrp, self.orbitDial))

        # pitch layout
        self.pitchLayout = QtWidgets.QHBoxLayout()
        self.renderTabRight.addLayout(self.pitchLayout)

        label = QtWidgets.QLabel("Pitch: ")
        label.setStyleSheet("background: transparent;")
        label.setFont(buttonFont)
        label.setMinimumHeight(30)
        label.setMaximumHeight(30)
        self.pitchLayout.addWidget(label)

        self.pitchSlider = QtWidgets.QSlider()
        self.pitchSlider.setOrientation(QtCore.Qt.Horizontal)
        self.pitchSlider.setToolTip("Light Aim Height")
        self.pitchSlider.setRange(-180, 180)
        self.pitchLayout.addWidget(self.pitchSlider)
        self.pitchSlider.valueChanged.connect(
            partial(self.pitchLights, [self.spot1Parent, self.spot2Parent, self.spot3Parent], self.pitchSlider))

        # options layout
        self.tcPageOptionsLayout = QtWidgets.QHBoxLayout()
        self.tcPageMainLayout.addLayout(self.tcPageOptionsLayout)

        self.hqRenderCB = QtWidgets.QCheckBox("High Quality")
        self.tcPageOptionsLayout.addWidget(self.hqRenderCB)
        self.hqRenderCB.clicked.connect(partial(self.highQualityToggle))
        self.hqRenderCB.setChecked(False)

        self.shadowsCB = QtWidgets.QCheckBox("Shadows")
        self.tcPageOptionsLayout.addWidget(self.shadowsCB)
        self.shadowsCB.setChecked(False)
        self.shadowsCB.clicked.connect(partial(self.shadowsToggle, [self.spot1, self.spot2, self.spot3]))

        self.customThumbnail = QtWidgets.QLineEdit()
        self.tcPageOptionsLayout.addWidget(self.customThumbnail)

        self.loadThumbBtn = QtWidgets.QPushButton("Load Custom")
        self.tcPageOptionsLayout.addWidget(self.loadThumbBtn)
        self.loadThumbBtn.clicked.connect(self.loadCustomImg)
        self.loadThumbBtn.setMinimumSize(QtCore.QSize(80, 30))
        self.loadThumbBtn.setObjectName("settings")

        # button layout
        self.tcPageButtonLayout = QtWidgets.QHBoxLayout()
        self.tcPageMainLayout.addLayout(self.tcPageButtonLayout)

        self.tcPageBackBtn = QtWidgets.QPushButton("Back")
        self.tcPageBackBtn.setMinimumHeight(50)
        self.tcPageBackBtn.setFont(font)
        self.tcPageBackBtn.clicked.connect(partial(self.backToMeshSlicer))
        self.tcPageBackBtn.setObjectName("settings")

        self.tcPageContBtn = QtWidgets.QPushButton("Continue")
        self.tcPageContBtn.setMinimumHeight(50)
        self.tcPageContBtn.setFont(font)
        self.tcPageContBtn.clicked.connect(partial(self.continueToSummary, False))
        self.tcPageContBtn.setObjectName("settings")

        self.tcPageButtonLayout.addWidget(self.tcPageBackBtn)
        spacer = QtWidgets.QSpacerItem(200, 20)
        self.tcPageButtonLayout.addSpacerItem(spacer)
        self.tcPageButtonLayout.addWidget(self.tcPageContBtn)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createSummaryPage(self):

        # create the QFrame for this page
        self.summaryPage = QtWidgets.QFrame()
        self.summaryPage.setMinimumSize(560, 250)
        self.stack_widget.addWidget(self.summaryPage)
        self.sumPageMainLayout = QtWidgets.QVBoxLayout(self.summaryPage)

        # info page styling
        self.summaryPage.setStyleSheet(self.style)

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)

        buttonFont = QtGui.QFont()
        buttonFont.setPointSize(12)
        buttonFont.setBold(True)

        # top section of UI will contain Hbox layout with icon and character information
        self.sumPageTopLayout = QtWidgets.QHBoxLayout()
        self.sumPageMainLayout.addLayout(self.sumPageTopLayout)

        # left side of top layout
        self.sumPageIcon = QtWidgets.QFrame()
        self.sumPageIcon.setMinimumSize(200, 200)
        self.sumPageIcon.setMaximumSize(200, 200)
        self.sumPageTopLayout.addWidget(self.sumPageIcon)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self.sumPageIcon)
        shadow.setBlurRadius(5)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.sumPageIcon.setGraphicsEffect(shadow)

        # right side of top layout (vbox with 5 hbox children)
        self.sumPageTopRight = QtWidgets.QVBoxLayout()
        self.sumPageTopLayout.addLayout(self.sumPageTopRight)

        # character name
        assetNameLayout = QtWidgets.QHBoxLayout()
        self.sumPageTopRight.addLayout(assetNameLayout)
        assetNameLayout.setContentsMargins(3, 0, 3, 0)

        label = QtWidgets.QLabel("Asset Name: ")
        label.setStyleSheet("background: transparent;")
        assetNameLayout.addWidget(label)
        label.setAlignment(QtCore.Qt.AlignLeft)
        label.setMinimumWidth(80)
        label.setMaximumWidth(80)

        self.sumPageAssetName = QtWidgets.QLineEdit()
        assetNameLayout.addWidget(self.sumPageAssetName)
        self.sumPageAssetName.setMinimumWidth(240)
        self.sumPageAssetName.setMaximumWidth(240)
        self.sumPageAssetName.setAlignment(QtCore.Qt.AlignRight)
        self.sumPageAssetName.setReadOnly(True)

        # project
        projLayout = QtWidgets.QHBoxLayout()
        self.sumPageTopRight.addLayout(projLayout)
        projLayout.setContentsMargins(3, 0, 3, 0)

        label = QtWidgets.QLabel("Project: ")
        label.setStyleSheet("background: transparent;")
        projLayout.addWidget(label)
        label.setAlignment(QtCore.Qt.AlignLeft)
        label.setMinimumWidth(80)
        label.setMaximumWidth(80)

        self.sumPageProj = QtWidgets.QLineEdit()
        projLayout.addWidget(self.sumPageProj)
        self.sumPageProj.setMinimumWidth(240)
        self.sumPageProj.setMaximumWidth(240)
        self.sumPageProj.setAlignment(QtCore.Qt.AlignRight)
        self.sumPageProj.setReadOnly(True)

        # group
        groupNameLayout = QtWidgets.QHBoxLayout()
        self.sumPageTopRight.addLayout(groupNameLayout)
        groupNameLayout.setContentsMargins(3, 0, 3, 0)

        label = QtWidgets.QLabel("Group: ")
        label.setStyleSheet("background: transparent;")
        groupNameLayout.addWidget(label)
        label.setAlignment(QtCore.Qt.AlignLeft)
        label.setMinimumWidth(80)
        label.setMaximumWidth(80)

        self.sumPageGroup = QtWidgets.QLineEdit()
        groupNameLayout.addWidget(self.sumPageGroup)
        self.sumPageGroup.setMinimumWidth(240)
        self.sumPageGroup.setMaximumWidth(240)
        self.sumPageGroup.setAlignment(QtCore.Qt.AlignRight)
        self.sumPageGroup.setReadOnly(True)

        # revision type
        revisionTypeLayout = QtWidgets.QHBoxLayout()
        self.sumPageTopRight.addLayout(revisionTypeLayout)
        revisionTypeLayout.setContentsMargins(3, 0, 3, 0)

        label = QtWidgets.QLabel("Revision Type: ")
        label.setStyleSheet("background: transparent;")
        revisionTypeLayout.addWidget(label)
        label.setAlignment(QtCore.Qt.AlignLeft)
        label.setMinimumWidth(80)
        label.setMaximumWidth(80)

        self.sumPageRevisionType = QtWidgets.QLineEdit()
        revisionTypeLayout.addWidget(self.sumPageRevisionType)
        self.sumPageRevisionType.setMinimumWidth(240)
        self.sumPageRevisionType.setMaximumWidth(240)
        self.sumPageRevisionType.setAlignment(QtCore.Qt.AlignRight)
        self.sumPageRevisionType.setReadOnly(True)

        # options
        optionsLayout = QtWidgets.QHBoxLayout()
        self.sumPageTopRight.addLayout(optionsLayout)
        optionsLayout.setContentsMargins(3, 0, 3, 0)

        self.sp_preScriptCB = QtWidgets.QCheckBox("Pre-Script?")
        optionsLayout.addWidget(self.sp_preScriptCB)
        self.sp_preScriptCB.setEnabled(False)

        self.sp_postScriptCB = QtWidgets.QCheckBox("Post-Script?")
        optionsLayout.addWidget(self.sp_postScriptCB)
        self.sp_postScriptCB.setEnabled(False)

        self.sp_animMeshCB = QtWidgets.QCheckBox("Animation Mesh?")
        optionsLayout.addWidget(self.sp_animMeshCB)
        self.sp_animMeshCB.setEnabled(False)

        # button layout
        self.sp_PageButtonLayout = QtWidgets.QHBoxLayout()
        self.sumPageMainLayout.addLayout(self.sp_PageButtonLayout)

        self.sp_PageBackBtn = QtWidgets.QPushButton("Back")
        self.sp_PageBackBtn.setMinimumHeight(50)
        self.sp_PageBackBtn.setFont(font)
        self.sp_PageBackBtn.clicked.connect(partial(self.backToMeshIconCreation))
        self.sp_PageBackBtn.setObjectName("settings")

        self.sp_PageContBtn = QtWidgets.QPushButton("BUILD")
        self.sp_PageContBtn.setMinimumHeight(50)
        self.sp_PageContBtn.setFont(font)
        self.sp_PageContBtn.clicked.connect(partial(self.launchBuild))
        self.sp_PageContBtn.setObjectName("settings")

        self.sp_PageButtonLayout.addWidget(self.sp_PageBackBtn)
        spacer = QtWidgets.QSpacerItem(200, 20)
        self.sp_PageButtonLayout.addSpacerItem(spacer)
        self.sp_PageButtonLayout.addWidget(self.sp_PageContBtn)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def highQualityToggle(self):

        state = self.hqRenderCB.isChecked()

        if state:
            cmds.modelEditor(self.tcViewport, edit=True, rnm="ogsRenderer")

        if not state:
            cmds.modelEditor(self.tcViewport, edit=True, rnm="base_OpenGL_Renderer")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def shadowsToggle(self, lights):

        state = self.shadowsCB.isChecked()

        for light in lights:
            cmds.setAttr(light + ".useDepthMapShadows", state)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pitchLights(self, lights, slider, *args):

        value = slider.value()

        for light in lights:
            cmds.setAttr(light + ".rotateX", value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeLightIntensity(self, light, dial, *args):

        # get dial value
        value = dial.value()
        value = float(value) / 50.0

        cmds.setAttr(light + ".intensity", value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeLightColor(self, light, button, *args):

        # launch color dialog
        self.qColorDialog = QtWidgets.QColorDialog.getColor()
        color = self.qColorDialog.getRgb()
        red = float(color[0])
        green = float(color[1])
        blue = float(color[2])

        cmds.setAttr(light + ".colorR", float(red / 255))
        cmds.setAttr(light + ".colorG", float(green / 255))
        cmds.setAttr(light + ".colorB", float(blue / 255))

        button.setStyleSheet("color: rgb(" + str(red) + "," + str(green) + "," + str(blue) + ");")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def orbitLights(self, group, dial, *args):

        value = dial.value()
        cmds.setAttr(group + ".rotateZ", value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def loadCustomImg(self):

        try:
            imgPath = cmds.fileDialog2(fm=1, dir=self.icons_path)[0]
            imgPath = utils.returnFriendlyPath(imgPath)

            # check to make sure image is valid
            extension = imgPath.rpartition(".")[2]
            if extension != "png":
                cmds.warning("Please upload only png files!")
            else:
                self.customImg.setStyleSheet("background-image: url(" + imgPath + ");")
                self.customThumbnail.setText(imgPath)
                self.viewportToggle.setCurrentIndex(0)

        except:
            cmds.warning("No File Chosen")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def moduleSelected(self):

        currentSelection = cmds.ls(sl=True)

        # run toggleMoverVisibility
        self.rig_interface_instance.setMoverVisibility()

        # clean up current module
        if self.current_module is not None:
            self.current_module.cleanUpRigPose()

        # find the currently selected module
        selected = self.rpPage_moduleList.selectedItems()
        module = selected[0].text()

        # find the network node this module belongs to
        networkNode = None
        modules = utils.returnRigModules()
        for mod in modules:
            modName = cmds.getAttr(mod + ".moduleName")
            if modName == module:
                networkNode = mod
                break

        # find the instance in memory of the selected module
        if networkNode != None:

            for inst in self.rig_interface_instance.moduleInstances:

                if inst.returnNetworkNode == networkNode:
                    # call on module's method for unhiding and constraining joints
                    inst.setupForRigPose()

                    # call on the module's getRigPose method
                    inst.getReferencePose("rigPose")

                    # call on the module's rigPose_UI method
                    index = self.rpPage_stackWidget.indexOf(inst.rigPoseFrame)
                    self.rpPage_stackWidget.setCurrentIndex(index)

                    # set current module
                    self.current_module = inst

        cmds.select(clear=True)
        if len(currentSelection) > 0:
            cmds.select(currentSelection)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_project_tree(self, directory, folder_list, item_list, parent_item=None):

        # creating some lists for filtering folders and files
        banned = [".mayaSwatches"]
        filter = [".png", ".v2pose", ".pickWalk"]

        # get items in passed in directory
        sub_items = os.listdir(directory)
        for each in sub_items:

            # if the item is a directory (not a file), check for children
            if os.path.isdir(os.path.join(directory, each)):
                folder_list.append([os.path.join(directory, each), each])
                children = os.listdir(os.path.join(directory, each))

                # if there are children in the folder, add items to the tree widget and do a recursive search
                # if len(children) > 0:

                if not parent_item:
                    if each not in banned:
                        folder_item = QtWidgets.QTreeWidgetItem(self.directory_tree, [each])
                        folder_item.setData(0, QtCore.Qt.UserRole, ["folder", os.path.join(directory, each)])
                        icon_path = utils.returnNicePath(self.icons_path, 'System/folder.png')
                        folder_item.setIcon(0, QtGui.QIcon(icon_path))
                        self._populate_project_tree(os.path.join(directory, each), folder_list, item_list,
                                                    folder_item)
                else:
                    if each not in banned:
                        folder_item = QtWidgets.QTreeWidgetItem(parent_item, [each])
                        folder_item.setData(0, QtCore.Qt.UserRole, ["folder", os.path.join(directory, each)])
                        icon_path = utils.returnNicePath(self.icons_path, 'System/folder.png')
                        folder_item.setIcon(0, QtGui.QIcon(icon_path))

                        self._populate_project_tree(os.path.join(directory, each), folder_list, item_list,
                                                    folder_item)

            # if the item is a file, add the item to the tree widget
            if os.path.isfile(os.path.join(directory, each)):
                if not os.path.splitext(each)[1] in filter:
                    item_list.append([os.path.join(directory, each), each, parent_item])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _update_project_path(self):

        selected = self.directory_tree.selectedItems()
        if len(selected) > 0:
            selected = selected[0]
            item_type = selected.data(0, QtCore.Qt.UserRole)

            path = item_type[1].replace(self.project_path, '')
            path = utils.returnFriendlyPath(path)

            if item_type[0] == "folder":
                self.path_label.setText(self.header_text + path + "/")

            if item_type[0] == "file":
                file_data = path.rpartition("/")
                path_name = file_data[0]
                file_name = os.path.splitext(file_data[2])[0]

                self.path_label.setText(self.header_text + path_name + "/")
                self.character_name.setText(file_name)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_projects(self):

        projects = []
        existingProjects = os.listdir(self.project_path)

        for each in existingProjects:
            if each is not ".mayaSwatches":
                if os.path.isdir(os.path.join(self.project_path, each)):
                    projects.append(each)

        return projects

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateProjects(self):

        self.directory_tree.clear()

        # if the project path doesn't exist on disk, create it
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)

        # get a list of the existing folders in projects
        existingProjects = os.listdir(self.project_path)
        folders = []

        # find out which returned items are directories
        for each in existingProjects:
            if os.path.isdir(os.path.join(self.project_path, each)):
                folders.append(each)

        # if there are no projects, bring up add project interface
        if len(folders) == 0:
            self.addNewProject(False)

        # otherwise, search for projects and build up the tree widget
        else:
            folders = []
            items = []
            self._populate_project_tree(self.project_path, folders, items)

            for each in items:
                file_name = os.path.splitext(each[1])[0]
                file_item = QtWidgets.QTreeWidgetItem(each[2], [file_name])
                file_item.setData(0, QtCore.Qt.UserRole, ["file", each[0]])
                icon_path = utils.returnNicePath(self.icons_path, 'System/file.png')
                file_item.setIcon(0, QtGui.QIcon(icon_path))

        self.directory_tree.resizeColumnToContents(0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addNewProject(self, fromButton):

        # simple UI for user to add new Project
        if cmds.window("ART_Publish_AddNewProjUI", exists=True):
            cmds.deleteUI("ART_Publish_AddNewProjUI", wnd=True)

        # launch a UI to get the name information
        self.addNewProjWindow = QtWidgets.QMainWindow(self.window)

        # size policies
        main_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.addNewProjWindow_mainWidget = QtWidgets.QWidget()
        self.addNewProjWindow.setCentralWidget(self.addNewProjWindow_mainWidget)

        # set qt object name
        self.addNewProjWindow.setObjectName("ART_Publish_AddNewProjUI")
        self.addNewProjWindow.setWindowTitle("Add New Project")

        # create the mainLayout for the rig creator UI
        self.addNewProjWindow_mainLayout = QtWidgets.QVBoxLayout(self.addNewProjWindow_mainWidget)
        self.addNewProjWindow_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.addNewProjWindow.resize(300, 115)
        self.addNewProjWindow.setSizePolicy(main_size_policy)
        self.addNewProjWindow.setMinimumSize(QtCore.QSize(300, 115))
        self.addNewProjWindow.setMaximumSize(QtCore.QSize(300, 115))

        # add stackWidget for ability to swap between two different pages (page 1: No projects exist.
        # page 2: add new project)
        self.addNewProjWindow_stackWidget = QtWidgets.QStackedWidget()
        self.addNewProjWindow_mainLayout.addWidget(self.addNewProjWindow_stackWidget)

        # NO PROJECT EXISTS PAGE

        # add background image/QFrame for first page
        page1Widget = QtWidgets.QWidget()
        self.addNewProjWindow_stackWidget.addWidget(page1Widget)

        self.addNewProjWindow_frame = QtWidgets.QFrame(page1Widget)
        self.addNewProjWindow_frame.setMinimumSize(QtCore.QSize(300, 115))
        self.addNewProjWindow_frame.setMaximumSize(QtCore.QSize(300, 115))

        # Add simple VBoxLayout for page
        self.addNewProjWindow_page1Layout = QtWidgets.QVBoxLayout(self.addNewProjWindow_frame)

        # add label
        label = QtWidgets.QLabel("No projects exist in this directory. Would you like to add one now?")
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.addNewProjWindow_page1Layout.addWidget(label)

        # add buttons for Yes/Cancel
        self.addNewProjWinPage1_buttonLayout = QtWidgets.QHBoxLayout()
        self.addNewProjWindow_page1Layout.addLayout(self.addNewProjWinPage1_buttonLayout)

        self.addNewProjWinPage1_CancelButton = QtWidgets.QPushButton("Cancel")
        self.addNewProjWinPage1_CancelButton.setObjectName("settings")
        self.addNewProjWinPage1_buttonLayout.addWidget(self.addNewProjWinPage1_CancelButton)
        self.addNewProjWinPage1_CancelButton.clicked.connect(self.addNewProjWindow.close)

        self.addNewProjWinPage1_YesButton = QtWidgets.QPushButton("Yes")
        self.addNewProjWinPage1_YesButton.setObjectName("settings")
        self.addNewProjWinPage1_buttonLayout.addWidget(self.addNewProjWinPage1_YesButton)
        self.addNewProjWinPage1_YesButton.clicked.connect(partial(self.addNewProjWindow_stackWidget.setCurrentIndex, 1))

        # ADD NEW PROJECT PAGE

        # add background image/QFrame for first page
        page2Widget = QtWidgets.QWidget()
        self.addNewProjWindow_stackWidget.addWidget(page2Widget)

        self.addNewProjWinPage2_frame = QtWidgets.QFrame(page2Widget)
        self.addNewProjWinPage2_frame.setMinimumSize(QtCore.QSize(300, 115))
        self.addNewProjWinPage2_frame.setMaximumSize(QtCore.QSize(300, 115))

        # Add simple VBoxLayout for page
        self.addNewProjWindow_page2Layout = QtWidgets.QVBoxLayout(self.addNewProjWinPage2_frame)

        # line edit for writing project name
        layout = QtWidgets.QHBoxLayout()
        self.addNewProjWindow_page2Layout.addLayout(layout)

        label = QtWidgets.QLabel("Project Name:")
        layout.addWidget(label)

        self.addNewProjLineEdit = QtWidgets.QLineEdit()
        self.addNewProjLineEdit.setPlaceholderText("Enter a project name")
        layout.addWidget(self.addNewProjLineEdit)

        # add project button
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        self.addNewProj_AddButton = QtWidgets.QPushButton("Create New Project")
        self.addNewProjWindow_page2Layout.addWidget(self.addNewProj_AddButton)
        self.addNewProj_AddButton.setFont(font)
        self.addNewProj_AddButton.setObjectName("settings")
        self.addNewProj_AddButton.setMinimumHeight(40)
        self.addNewProj_AddButton.clicked.connect(self.createNewProject)

        # show the ui
        self.addNewProjWindow.show()

        if not fromButton:
            self.addNewProjWindow_stackWidget.setCurrentIndex(0)
        if fromButton:
            self.addNewProjWindow_stackWidget.setCurrentIndex(1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addNewProjectDirectory(self):

        selected = self.directory_tree.selectedItems()
        if len(selected) == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Must select a project or an existing project directory to add a new directory to.")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.exec_()
            return

        # simple UI for user to add new Group
        if cmds.window("ART_Publish_AddNewGrpUI", exists=True):
            cmds.deleteUI("ART_Publish_AddNewGrpUI", wnd=True)

        # launch a UI to get the name information
        self.addNewGrpWin = QtWidgets.QMainWindow(self.window)

        # size policies
        main_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.addNewGrpWin_mainWidget = QtWidgets.QWidget()
        self.addNewGrpWin.setCentralWidget(self.addNewGrpWin_mainWidget)

        # set qt object name
        self.addNewGrpWin.setObjectName("ART_Publish_AddNewGrpUI")
        self.addNewGrpWin.setWindowTitle("Add New Directory")

        # create the mainLayout for the rig creator UI
        self.addNewGrpWin_mainLayout = QtWidgets.QVBoxLayout(self.addNewGrpWin_mainWidget)
        self.addNewGrpWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.addNewGrpWin.resize(310, 153)
        self.addNewGrpWin.setSizePolicy(main_size_policy)
        self.addNewGrpWin.setMinimumSize(QtCore.QSize(310, 153))
        self.addNewGrpWin.setMaximumSize(QtCore.QSize(310, 153))

        # add background image/QFrame for first page
        self.addNewGrpWin_frame = QtWidgets.QFrame()
        self.addNewGrpWin_mainLayout.addWidget(self.addNewGrpWin_frame)
        self.addNewGrpWin_frame.setMinimumSize(QtCore.QSize(310, 153))
        self.addNewGrpWin_frame.setMaximumSize(QtCore.QSize(310, 153))

        # create vertical layout
        self.addNewGrpWin_vLayout = QtWidgets.QVBoxLayout(self.addNewGrpWin_frame)

        label = QtWidgets.QLabel("Adding directory to:")
        self.addNewGrpWin_vLayout.addWidget(label)

        # project path widget
        self.addNewGrpWin_parentDir = QtWidgets.QLineEdit()
        self.addNewGrpWin_parentDir.setEnabled(False)
        self.addNewGrpWin_vLayout.addWidget(self.addNewGrpWin_parentDir)

        # set project path to selected directory structure (if possible)
        selected = self.directory_tree.selectedItems()
        if len(selected) > 0:
            item_data = selected[0].data(0, QtCore.Qt.UserRole)

            if item_data[0] == "folder":
                full_path = item_data[1]
                partial_path = full_path.split(self.header_text)[1]
                partial_path = utils.returnFriendlyPath(partial_path)
                self.addNewGrpWin_parentDir.setText(self.header_text + partial_path)

        # directory name layout/widgets
        dir_layout = QtWidgets.QHBoxLayout()
        self.addNewGrpWin_vLayout.addLayout(dir_layout)

        label2 = QtWidgets.QLabel("Directory Name:")
        dir_layout.addWidget(label2)

        self.addNewGrpWinLineEdit = QtWidgets.QLineEdit()
        self.addNewGrpWinLineEdit.setPlaceholderText("Enter a directory name")
        self.addNewGrpWinLineEdit.setMinimumWidth(185)
        self.addNewGrpWinLineEdit.setMaximumWidth(185)
        dir_layout.addWidget(self.addNewGrpWinLineEdit)

        # add group button
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        self.addNewGrpWin_AddButton = QtWidgets.QPushButton("Create New Directory")
        self.addNewGrpWin_vLayout.addWidget(self.addNewGrpWin_AddButton)
        self.addNewGrpWin_AddButton.setFont(font)
        self.addNewGrpWin_AddButton.setMinimumHeight(40)
        self.addNewGrpWin_AddButton.setObjectName("settings")
        self.addNewGrpWin_AddButton.clicked.connect(self.createNewDirectory)

        # show the ui
        self.addNewGrpWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createNewProject(self):

        # get name from lineEdit
        projectName = self.addNewProjLineEdit.text()
        if len(projectName) == 0:
            cmds.warning("No valid Project Name entered.")
            return

        # make sure there are no naming conflicts
        existingProjects = os.listdir(self.project_path)
        if projectName in existingProjects:
            cmds.warning("Project with that name already exists. Aborting..")
            return

        # make the directory
        path = os.path.join(self.project_path, projectName)
        os.makedirs(path)

        # close the ui
        self.addNewProjWindow.close()

        # repopulate
        self.populateProjects()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createNewDirectory(self):

        # get name from lineEdit
        dir_name = self.addNewGrpWinLineEdit.text()
        if len(dir_name) == 0:
            cmds.warning("No valid Directory name entered.")
            return

        # make sure there are no naming conflicts
        selectedProject = self.addNewGrpWin_parentDir.text()
        selectedProject = selectedProject.partition(self.header_text + "/")[2]
        item_names = selectedProject.split("/")

        project = os.path.join(self.project_path, selectedProject)
        existingGroups = os.listdir(project)

        if dir_name in existingGroups:
            cmds.warning("Directory with that name already exists. Aborting..")
            return

        # make the directory
        path = os.path.join(project, dir_name)
        os.makedirs(path)

        # close the ui
        self.addNewGrpWin.close()

        # repopulate
        self.populateProjects()

        # expand project to show new directory
        for each in item_names:
            items = self.directory_tree.findItems(each, QtCore.Qt.MatchRecursive)
            for item in items:
                self.directory_tree.setItemExpanded(item, True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createNewCharacter(self):

        # get character name from lineEdit
        characterName = self.character_name.text()
        toContinue = False

        # get existing names in characterList
        existingCharacters = []

        path = self.path_label.text()
        path = path.partition(self.header_text + "/")[2]
        full_path = utils.returnNicePath(self.project_path, path)
        files = os.listdir(full_path)
        for file in files:
            existingCharacters.append(file.partition(".ma")[0])

        # check if name is unique. If not, ask if user wants to overwrite
        if characterName not in existingCharacters:
            toContinue = True

        else:
            toContinue = self.overwriteCharacterUI()

        if toContinue:

            # if the name is not an empty string, proceed.
            if len(characterName) > 0:

                # check for attributes on ART_RIG_ROOT node
                character_node = utils.returnCharacterModule()
                firstVersion = False

                if cmds.objExists(character_node + ".project") is False:
                    cmds.addAttr(character_node, ln="project", dt="string", keyable=True)

                if cmds.objExists(character_node + ".subDirectory") is False:
                    cmds.addAttr(character_node, ln="subDirectory", dt="string", keyable=True)

                if cmds.objExists(character_node + ".name") is False:
                    cmds.addAttr(character_node, ln="name", dt="string", keyable=True)

                if cmds.objExists(character_node + ".version") is False:
                    cmds.addAttr(character_node, ln="version", keyable=True)
                    firstVersion = True

                if cmds.objExists(character_node + ".versionNote") is False:
                    cmds.addAttr(character_node, ln="versionNote", dt="string", keyable=True)

                if cmds.objExists(character_node + ".publishedBy") is False:
                    cmds.addAttr(character_node, ln="publishedBy", dt="string", keyable=True)

                # get data from UI
                projectName = path.split("/")[0]
                subDirName = path.partition(projectName)[2]
                charName = self.character_name.text()

                # get user
                for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                    user = os.environ.get(name)
                cmds.setAttr(character_node + ".publishedBy", user, type="string")

                # version character
                if firstVersion:
                    cmds.setAttr(character_node + ".version", 1)
                    cmds.setAttr(character_node + ".versionNote",
                                 json.dumps([[1, "initial checkin", cmds.getAttr(character_node + ".publishedBy")]]),
                                 type="string")

                # if this is not the firstVersion, check to see if it's technically being saved as a new file
                if not firstVersion:
                    # get current data off node
                    currentProj = cmds.getAttr(character_node + ".project")
                    currentSubDir = cmds.getAttr(character_node + ".subDirectory")
                    currentName = cmds.getAttr(character_node + ".name")

                    if type(currentSubDir) == type(None):
                        currentSubDir = " "

                    # figure out if this is truly a new version, or if this is getting published as something else
                    doVersion = False
                    if projectName == currentProj:
                        if subDirName == currentSubDir:
                            if charName == currentName:
                                doVersion = True

                    if doVersion:
                        currentVersion = cmds.getAttr(character_node + ".version")

                        # find type of revision
                        value = .01
                        changeType = self.revision_type.currentText()
                        if changeType == "Minor Change":
                            value = .1
                        if changeType == "Major Change":
                            value = 1
                        cmds.setAttr(character_node + ".version", currentVersion + value)

                    else:
                        cmds.setAttr(character_node + ".version", 1)
                        cmds.setAttr(character_node + ".versionNote",
                                     json.dumps([1, "initial checkin", cmds.getAttr(character_node + ".publishedBy")]),
                                     type="string")

                    # version note
                    string = self.revision_note.toPlainText()
                    revisionHistory = json.loads(cmds.getAttr(character_node + ".versionNote"))
                    revisionHistory.append([cmds.getAttr(character_node + ".version"), string,
                                            cmds.getAttr(character_node + ".publishedBy")])
                    cmds.setAttr(character_node + ".versionNote", json.dumps(revisionHistory), type="string")

                # set data on character_node
                cmds.setAttr(character_node + ".project", projectName, type="string")
                cmds.setAttr(character_node + ".subDirectory", subDirName, type="string")
                cmds.setAttr(character_node + ".name", charName, type="string")

                # save file
                fullPath = utils.returnFriendlyPath(os.path.join(full_path, charName + ".ma"))
                cmds.file(rename=fullPath)
                cmds.file(save=True, type="mayaAscii")

                # repopulate character list
                self.populateProjects()

                # add info to publishFileInfo
                self.publish_file_info.append([fullPath, projectName, subDirName, charName])

                # go to next page
                self.continueToRigPose()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def overwriteCharacterUI(self):

        # message box for confirming if character should be overwritten or not
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("A character already exists with the given name!")
        msgBox.addButton("Overwrite", QtWidgets.QMessageBox.YesRole)
        msgBox.addButton("Cancel", QtWidgets.QMessageBox.NoRole)
        ret = msgBox.exec_()

        if ret == 1:
            return False
        else:
            return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def overwriteIconUI(self, path):

        # message box for confirming if icon should be overwritten or not
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText("This asset already has an icon associated with it.")
        msgBox.addButton("Overwrite", QtWidgets.QMessageBox.YesRole)
        msgBox.addButton("Keep Current Icon", QtWidgets.QMessageBox.NoRole)
        msgBox.setDetailedText("Current Icon:\n\n" + path)
        ret = msgBox.exec_()

        if ret == 1:
            return False
        else:
            return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def cancelPublish(self):

        cmds.deleteUI("ART_PublishWin", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggle_version_layout(self, widget, *args):

        state = widget.isChecked()
        if state is True:
            widget.setMinimumHeight(130)
            widget.setMaximumHeight(130)
            self.project_spacer_item.changeSize(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        else:
            widget.setMinimumHeight(30)
            widget.setMaximumHeight(30)
            self.project_spacer_item.changeSize(20, 105, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def continueToProject(self):

        self.stack_widget.setCurrentIndex(1)

        # pre-select UI elements if data exists
        character_node = utils.returnCharacterModule()

        attrs = cmds.listAttr(character_node, ud=True)
        for attr in attrs:
            # set project if applicable
            if attr.find("project") == 0:
                project = cmds.getAttr(character_node + ".project")

                items = self.directory_tree.findItems(project, QtCore.Qt.MatchRecursive)
                for item in items:
                    self.directory_tree.setItemExpanded(item, True)

            # set subDirectory if applicable
            if attr.find("subDirectory") == 0:
                subDirectory = cmds.getAttr(character_node + ".subDirectory")
                folders = subDirectory.split("/")

                for folder in folders:
                    items = self.directory_tree.findItems(folder, QtCore.Qt.MatchRecursive)
                    for item in items:
                        self.directory_tree.setItemExpanded(item, True)

            # select character, if applicable
            if attr.find("name") == 0:
                name = cmds.getAttr(character_node + ".name")
                items = self.directory_tree.findItems(name, QtCore.Qt.MatchRecursive)
                for item in items:
                    item.setSelected(True)

            # set pre-script, if applicable
            if attr.find("preScriptPath") == 0:
                path = cmds.getAttr(character_node + ".preScriptPath")
                self.pre_script_line_edit.setText(path)

            # set post-script, if applicable
            if attr.find("postScriptPath") == 0:
                path = cmds.getAttr(character_node + ".postScriptPath")
                self.post_script_line_edit.setText(path)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def continueToRigPose(self):

        self.stack_widget.setCurrentIndex(2)
        self.window.setWindowTitle("Create Rig Pose")

        # if pre/post script slots are empty, and the attrs exist, remove attrs
        characterModule = utils.returnCharacterModule()

        if self.pre_script_line_edit.text() == "":
            if cmds.objExists(characterModule + ".preScriptPath"):
                cmds.deleteAttr(characterModule, at="preScriptPath")

        if self.post_script_line_edit.text() == "":
            if cmds.objExists(characterModule + ".postScriptPath"):
                cmds.deleteAttr(characterModule, at="postScriptPath")

        # setup the interfaces
        data_exists = False
        for inst in self.rig_interface_instance.moduleInstances:
            listItems = []

            networkNode = inst.returnNetworkNode
            if cmds.objExists(networkNode + ".rigPoseState"):
                data_exists = True

            for i in range(self.rpPage_moduleList.count()):
                text = self.rpPage_moduleList.item(i).text()
                listItems.append(text)
            if inst.name in listItems:
                inst.rigPose_UI(self.rpPage_stackWidget)

        # message box for asking if user wants to restore rig pose values
        populate_data = False
        if data_exists is True:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setText("Restore previous rig pose slider values?")
            msgBox.setInformativeText("This may take a couple minutes..")
            msgBox.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            msgBox.addButton("No", QtWidgets.QMessageBox.NoRole)
            msgBox.addButton("Reset Values", QtWidgets.QMessageBox.ResetRole)
            ret = msgBox.exec_()

            if ret == 0:
                populate_data = True
            print ret
            if ret == 2:
                import pymel.core as pm
                nodes = pm.ls(type="network")
                for node in nodes:
                    if node.hasAttr("rigPose"):
                        node.deleteAttr("rigPose")
                    if node.hasAttr("rigPoseState"):
                        node.deleteAttr("rigPoseState")
                    if node.hasAttr("modelPose"):
                        node.deleteAttr("modelPose")

        # populate data if user chose to
        if populate_data is True:
            for inst in self.rig_interface_instance.moduleInstances:
                # set slider states if attribute exists
                networkNode = inst.returnNetworkNode
                if cmds.objExists(networkNode + ".rigPoseState"):
                    sliderData = json.loads(cmds.getAttr(networkNode + ".rigPoseState"))

                    # create progress bar
                    progBar = QtWidgets.QProgressDialog(self.window)
                    progBar.setMinimumSize(QtCore.QSize(300, 100))
                    progBar.setMaximumSize(QtCore.QSize(300, 100))
                    progBar.setCancelButton(None)
                    progBar.setStyleSheet(self.style)
                    progBar.setLabelText("Setting rig pose slider values for " + inst.name)
                    progBar.setMinimum(0)

                    # get the slider children, if there is a match between the name property and the name data in
                    # the list set slider value
                    sliders = inst.rigPoseFrame.findChildren(QtWidgets.QSlider)

                    instData = {}
                    for each in sliders:
                        name = each.property("name")
                        instData[name] = each

                    progBar.setMaximum(len(sliderData))
                    progBar.show()
                    QtWidgets.QApplication.processEvents()

                    for data in sliderData:
                        sliderName = data.get("name")
                        if sliderName in instData:
                            progBar.setValue(progBar.value() + 1)
                            QtWidgets.QApplication.processEvents()
                            value = data.get("value")
                            inst.setupForRigPose()
                            slider = instData.get(sliderName)
                            slider.setValue(value)
                            if cmds.objExists(networkNode + ".rigPose"):
                                inst.setReferencePose("rigPose")
                            inst.cleanUpRigPose()
                    progBar.close()

        self.rpPage_stackWidget.setCurrentIndex(0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def continueToCreateAnimMesh(self):

        # save slider states and rig pose
        for inst in self.rig_interface_instance.moduleInstances:
            if inst.name != "root":
                networkNode = inst.returnNetworkNode
                inst.cleanUpRigPose()

                # add attr if it doesn't exist
                if not cmds.objExists(networkNode + ".rigPoseState"):
                    cmds.addAttr(networkNode, ln="rigPoseState", dt="string")

                # if rig pose doesn't exist, get and set it
                inst.getReferencePose("rigPose", False)

                # get the sliders from this widget (name and value)
                sliderList = []
                sliders = inst.rigPoseFrame.findChildren(QtWidgets.QSlider)
                for slider in sliders:

                    if slider.value() > 0:
                        sliderData = {}
                        sliderData["name"] = slider.property("name")
                        sliderData["value"] = slider.value()
                        sliderList.append(sliderData)

                # set the rigPoseState attr
                jsonString = json.dumps(sliderList)
                cmds.setAttr(networkNode + ".rigPoseState", jsonString, type="string")

        # go to next UI page
        self.window.setWindowTitle("Create Animation Mesh")
        self.stack_widget.setCurrentIndex(3)
        self.movie.start()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skipToCreateThumbnail(self):

        # get the character node
        character_node = utils.returnCharacterModule()

        # get the icon path if present
        if cmds.objExists(character_node + ".iconPath"):
            path = cmds.getAttr(character_node + ".iconPath")
            if os.path.exists(utils.returnNicePath(self.project_path, path)):
                toContinue = self.overwriteIconUI(path)

                # if the user wants to overwrite the existing icon
                if toContinue:

                    self.stack_widget.setCurrentIndex(4)
                    self.window.setWindowTitle("Create Thumbnail")
                # if the user wants to keep the existing icon
                else:
                    self.continueToSummary(True)

            # if the icon path did not exist on disc
            else:
                self.stack_widget.setCurrentIndex(4)
                self.window.setWindowTitle("Create Thumbnail")

        else:
            self.stack_widget.setCurrentIndex(4)
            self.window.setWindowTitle("Create Thumbnail")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def continueToCreateThumbnail(self):

        # get the character node
        character_node = utils.returnCharacterModule()

        # get asset name
        name = cmds.getAttr(character_node + ".name")

        # get LOD0 meshes
        if cmds.objExists(character_node + ".LOD_0"):
            jsonData = json.loads(cmds.getAttr(character_node + ".LOD_0"))
            meshes = jsonData.get("Meshes")
        else:
            meshes = utils.findAllSkinnableGeo()

        for mesh in meshes:
            newMesh = utils.splitMesh(mesh, name)
            cmds.select(newMesh)

            # select all new meshes and add to layer if layer doesn't exist
            if not cmds.objExists("Animation_Mesh_Geo"):
                cmds.createDisplayLayer(newMesh, name="Animation_Mesh_Geo")

            else:
                cmds.editDisplayLayerMembers("Animation_Mesh_Geo", newMesh)

        # get the icon path if present
        cmds.select(clear=True)
        if cmds.objExists(character_node + ".iconPath"):
            path = cmds.getAttr(character_node + ".iconPath")
            if os.path.exists(utils.returnNicePath(self.project_path, path)):
                toContinue = self.overwriteIconUI(path)
                if toContinue:

                    self.stack_widget.setCurrentIndex(4)
                    self.window.setWindowTitle("Create Thumbnail")

                else:
                    self.continueToSummary(True)
        else:
            self.stack_widget.setCurrentIndex(4)
            self.window.setWindowTitle("Create Thumbnail")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def continueToSummary(self, skip):

        # set window title
        self.window.setWindowTitle("Summary")

        # get character attributes to build up the path
        character_node = utils.returnCharacterModule()
        project = cmds.getAttr(character_node + ".project")
        group = cmds.getAttr(character_node + ".subDirectory")
        name = cmds.getAttr(character_node + ".name")
        version = cmds.getAttr(character_node + ".version")

        # create the path
        if len(group) > 1:
            path = utils.returnFriendlyPath(project + "/" + group + "/" + name + ".png")
        else:
            path = utils.returnFriendlyPath(project + "/" + name + ".png")

        # add icon attr to character node if needed
        if not cmds.objExists(character_node + ".iconPath"):
            cmds.addAttr(character_node, ln="iconPath", dt="string", keyable=True)

        cmds.setAttr(character_node + ".iconPath", path, type="string")

        # render our images if needed
        if not skip:
            if self.viewportToggle.currentIndex() == 1:

                # use API to grab image from view
                newView = mui.M3dView()
                mui.M3dView.getM3dViewFromModelEditor(self.tcViewport, newView)

                # read the color buffer from the view, and save the MImage to disk
                image = openMaya.MImage()
                newView.readColorBuffer(image, True)
                image.writeToFile(utils.returnNicePath(self.project_path, path), 'png')

            # if user passed in an image, save it to the appropriate location with the correct extension
            else:
                customPath = self.customThumbnail.text()
                import shutil
                try:
                    if not os.path.exists(utils.returnNicePath(self.project_path, path)):
                        shutil.copyfile(customPath, utils.returnNicePath(self.project_path, path))
                    else:
                        cmds.warning("Unable to copy " + str(customPath) + " to: " +
                                     str(utils.returnNicePath(self.project_path, path)) + ". File already exists.")
                except Exception, e:
                    print e

        # switch to summary page
        self.stack_widget.setCurrentIndex(5)

        # find if pre/post script added
        preScript = False
        if cmds.objExists(character_node + ".preScriptPath"):
            preScript = True

        postScript = False
        if cmds.objExists(character_node + ".postScriptPath"):
            postScript = True

        # get latest icon
        self.sumPageIcon.setStyleSheet("background-image: url(" + utils.returnNicePath(self.project_path, path) + ");")

        # set info
        self.sumPageAssetName.setText(name)
        self.sumPageProj.setText(project)
        self.sumPageGroup.setText(group)
        self.sumPageRevisionType.setText(str(version))
        self.sp_preScriptCB.setChecked(preScript)
        self.sp_postScriptCB.setChecked(postScript)

        if cmds.objExists(name + "_animMeshGrp"):
            self.sp_animMeshCB.setChecked(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def backToMeshIconCreation(self):

        self.stack_widget.setCurrentIndex(4)
        self.window.setWindowTitle("Create Thumbnail")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def backToMeshSlicer(self):

        self.stack_widget.setCurrentIndex(3)
        self.window.setWindowTitle("Create Animation Mesh")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def backToProject(self):

        self.stack_widget.setCurrentIndex(1)
        self.window.setWindowTitle("Publish")

        # make sure we hide all joint movers when going back and put things in the proper state
        for inst in self.rig_interface_instance.moduleInstances:
            listItems = []
            for i in range(self.rpPage_moduleList.count()):
                text = self.rpPage_moduleList.item(i).text()
                listItems.append(text)

            if inst.name in listItems:
                inst.cleanUpRigPose()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def backToRigPose(self):

        self.stack_widget.setCurrentIndex(2)
        self.window.setWindowTitle("Create Rig Pose")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addCustomScripts(self, preScript, postScript):

        # launch the file dialog window
        try:
            fileName = cmds.fileDialog2(startingDirectory=cmds.internalVar(usd=True), ff="*.py;;*.mel", fm=1,
                                        okCaption="Load Script")[0]
            fileName = utils.returnFriendlyPath(fileName)

        except Exception, e:
            print e
            return

        # add attributes if they don't exist to character node
        character_node = utils.returnCharacterModule()

        # edit the lineEdit to have the path to the script
        if preScript:
            self.pre_script_line_edit.setText(fileName)

            if not cmds.objExists(character_node + ".preScriptPath"):
                cmds.addAttr(character_node, ln="preScriptPath", dt="string", keyable=True)

            # set attrs
            cmds.setAttr(character_node + ".preScriptPath", fileName, type="string")

        # edit the lineEdit to have the path to the script
        if postScript:
            self.post_script_line_edit.setText(fileName)

            if not cmds.objExists(character_node + ".postScriptPath"):
                cmds.addAttr(character_node, ln="postScriptPath", dt="string", keyable=True)

            # set attrs
            cmds.setAttr(character_node + ".postScriptPath", fileName, type="string")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def publishHelp(self):

        from Tools.System import ART_Help

        helpMovie = utils.returnFriendlyPath(os.path.join(self.icons_path, "Help/publish.gif"))
        ART_Help.ART_HelpMovie(self.window, helpMovie)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def rigPoseHelp(self):

        from Tools.System import ART_Help

        helpMovie = utils.returnFriendlyPath(os.path.join(self.icons_path, "Help/rigPose.gif"))
        ART_Help.ART_HelpMovie(self.window, helpMovie)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def launchBuild(self):

        if cmds.window("ART_PublishWin", exists=True):
            self.close_window(QtCore.QEvent(QtCore.QEvent.User))

        # save the file
        cmds.file(save=True)

        # check to see if the necessary plugins are loaded/available
        try:
            cmds.loadPlugin("ARTv2_Stretchy_IK")
        except Exception:
            cmds.warning("ARTv2_Stretchy_IK plugin needed to build rigs. Aborting")
            return

        try:
            cmds.loadPlugin('matrixNodes.dll')
        except Exception:
            cmds.warning("matrixNodes.dll plugin needed to build rigs. Aborting")
            return

        # launch build progress UI
        from Tools.Rigging import ART_BuildProgressUI
        ART_BuildProgressUI.ART_BuildProgress_UI(self.rig_interface_instance)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def close_window(self, event):
        # override the close event for the window with a custom function that makes sure the scene is cleaned up

        # delete thumbnail camera nodes
        try:
            for node in [self.thumbnailCamera, self.lightGrp]:
                children = cmds.listRelatives(node, children=True)
                if len(children) > 0:
                    for each in children:
                        cmds.lockNode(each, lock=False)
                cmds.lockNode(node, lock=False)
                cmds.delete(node)
        except Exception:
            pass

        # if launching the rig build, hide the UI for now.
        if event.type() == QtCore.QEvent.User:
            if cmds.window("ART_PublishWin", exists=True):
                cmds.window("ART_PublishWin", edit=True, vis=False)

        # if closing the publish UI, but not building, set joint mover back to model pose and delete UI.
        if event.type() == QtCore.QEvent.Close:
            print "close event"
            if cmds.window("ART_PublishWin", exists=True):
                cmds.deleteUI("ART_PublishWin", wnd=True)

            try:
                for inst in self.rig_interface_instance.moduleInstances:
                    if inst.name != "root":
                        try:
                            inst.setupForRigPose()
                            inst.setReferencePose("modelPose")
                            inst.cleanUpRigPose()
                        except Exception, e:
                            cmds.warning(str(e))
            except Exception:
                pass

        event.accept()
