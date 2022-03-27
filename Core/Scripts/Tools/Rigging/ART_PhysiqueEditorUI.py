from functools import partial
import os
import math

import Utilities.interfaceUtils as interfaceUtils
import Utilities.utils as utils
import maya.cmds as cmds
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except Exception:
    import shiboken2 as shiboken


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_PhysiqueEditorUI(QtWidgets.QMainWindow):
    """
    This class creates the physique editor tool, which allows you to change the form of the proxy geo.

    For this tool to work, the joint mover files associated with each of the modules must have morph targets added
    that follow the naming convention.
    For the weight sliders, the morph must be named either **thin_[proxy_geo_name]** or **heavy_[proxy_geo_name]**,
    where [proxy_geo_name] would be something like: pelvis_proxy_geo.
    For the muscle sliders, the morph targets will have a prefix of either slim or buff, followed by the proxy geo name.

    .. important:: The valid morph target prefixes are listed below.

       * slim_      : muscle slider
       * buff_      : muscle slider
       * thin_      : weight slider
       * heavy_     : weight slider
       * female_    : gender slider
       * long_      : module height slider

    .. important:: The blendshape nodes themselves are named: physique_[proxy_geo_name]_shapes.

    If implementing length, a length_grp must be created and is parented under the top-most mover of the module. In the
    case of the torso module, this would be the pelvis mover. Under this group, is an empty group node for each of the
    child movers, so in this case, spine 1 - 3, and these are named [joint_name]_length_pos, where joint name would be
    spine_01 for example. These group nodes are currently aligned perfectly to the corresponding joint mover. The idea
    here is that when the length group is scaled, the actual joint movers can then be snapped to these length_pos nodes
    to match that scaled amount. This is different than just scaling the pelvis mover in the torso example, as that
    globally scales everything. This length group only gives us the positions from the scaling, meaning the thickness
    of the proxy geometry remains unchanged, but the distance between the joints has increased.

    .. note:: As of now, only the 3 spine torso module has physique support, and only the 1 neck head module. Support
              for the other variants will come in the future.

    .. important:: morph targets should be removed from the scene once iteration is complete, otherwise errors will
       occur during the building of the rig.

    """

    # TODO: see if having a torso module with no pelvis breaks the length group!
    # TODO: add physique setups to torso module 2, 4, and 5 joint spine files
    # TODO: add physique setups to head module 2 and 3 joint neck files.

    def __init__(self, mainUI, parent=None):
        """
        Instantiates the class, gets settings values from QSettings. Calls on building the interface.
        Creates a bunch of lists for the different slider types and slider states. Calls on findModuleShapes.

        .. seealso:: ART_PhysiqueEditorUI.findModuleShapes()

        """

        super(ART_PhysiqueEditorUI, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.scriptPath = settings.value("scriptPath")
        self.iconsPath = settings.value("iconPath")
        self.projectPath = settings.value("projectPath")

        # create a dictionary of UI widgets to track as well as other sliders to track
        self.widgets = {}
        self.moduleGlobalSliders = {}
        self.moduleSliders = {}
        self.weightSliders = []
        self.muscleSliders = []
        self.genderSliders = []

        # list of unique sliders for reset all function
        self.sliders = []

        # rig creator UI instance
        self.mainUI = mainUI

        # track unlocked sliders
        self.unlocked = []

        # find shapes
        self.findModuleShapes()

        # build the interface
        self.buildInterface()

        # add everything to the groubox scroll area (space switching tab)
        self.overrides_scrollContents.setLayout(self.scrollContents_layout)
        scroll_area_vertical = QtWidgets.QScrollArea()
        scroll_area_vertical.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area_vertical.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area_vertical.setWidgetResizable(True)
        self.module_overrides_layout.addWidget(scroll_area_vertical)
        scroll_area_vertical.setWidget(self.overrides_scrollContents)

        # get the up-axis
        self.up = cmds.upAxis(q=True, ax=True)

        # get bounds
        self.getHeight()
        self.adjustModuleHeight(self.global_height_slider, True)

        self.resetAll()

        # populate UI
        self.populateUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildInterface(self):
        """

        Main function that builds the innterface for the tool. The interface consists of a global section, a module
        overrides section, and within each module override, a proxy geo override for each piece of proxy geo.

        .. image:: /images/physiqueEditor.png

        :return: None

        """

        # set the window size
        self.setMinimumSize(QtCore.QSize(400, 620))
        self.setMaximumSize(QtCore.QSize(400, 620))

        # load the stylesheets
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)
        self.unlock_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/unlocked2.png"))
        self.lock_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/locked2.png"))
        self.reset_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/reset2.png"))
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)

        # set qt object name
        self.setObjectName("ART_PhysiqueEditorUI")
        self.setWindowTitle("Physique Editor")

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("dark")
        self.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # GLOBAL SLIDERS
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        global_grp_box = QtWidgets.QGroupBox("Global Settings:")
        global_grp_box.setMinimumSize(QtCore.QSize(380, 130))
        global_grp_box.setMaximumSize(QtCore.QSize(380, 130))
        global_grp_box.setObjectName("light")
        self.mainLayout.addWidget(global_grp_box)

        global_grp_box_layout = QtWidgets.QVBoxLayout(global_grp_box)

        # GENDER
        global_gender_layout = QtWidgets.QHBoxLayout()
        global_grp_box_layout.addLayout(global_gender_layout)

        gender_label = QtWidgets.QLabel("GENDER: ")
        gender_label.setStyleSheet("background: transparent; font: bold;")
        gender_label.setMinimumSize(QtCore.QSize(60, 20))
        gender_label.setMaximumSize(QtCore.QSize(60, 20))

        male_label = QtWidgets.QLabel("Male")
        male_label.setStyleSheet("background: transparent; font: italic;")
        male_label.setMinimumSize(QtCore.QSize(60, 20))
        male_label.setMaximumSize(QtCore.QSize(60, 20))
        male_label.setAlignment(QtCore.Qt.AlignRight)

        female_label = QtWidgets.QLabel("Female")
        female_label.setStyleSheet("background: transparent; font: italic;")
        female_label.setMinimumSize(QtCore.QSize(60, 20))
        female_label.setMaximumSize(QtCore.QSize(60, 20))
        female_label.setAlignment(QtCore.Qt.AlignLeft)

        self.global_gender_slider = QtWidgets.QSlider()
        self.global_gender_slider.setMinimumWidth(100)
        self.global_gender_slider.setRange(0, 100)
        self.global_gender_slider.setProperty("type", "gender")
        self.global_gender_slider.setOrientation(QtCore.Qt.Horizontal)
        self.global_gender_slider.valueChanged.connect(partial(self.setGlobalSliders, self.global_gender_slider,
                                                               self.genderSliders))

        global_gender_spacer = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        global_gender_layout.addWidget(gender_label)
        global_gender_layout.addWidget(male_label)
        global_gender_layout.addWidget(self.global_gender_slider)
        global_gender_layout.addWidget(female_label)
        global_gender_layout.addItem(global_gender_spacer)

        # MUSCLE
        global_muscle_layout = QtWidgets.QHBoxLayout()
        global_grp_box_layout.addLayout(global_muscle_layout)

        muscle_label = QtWidgets.QLabel("MUSCLE: ")
        muscle_label.setStyleSheet("background: transparent; font: bold;")
        muscle_label.setMinimumSize(QtCore.QSize(60, 20))
        muscle_label.setMaximumSize(QtCore.QSize(60, 20))

        muscle_label_1 = QtWidgets.QLabel("Slight")
        muscle_label_1.setStyleSheet("background: transparent; font: italic;")
        muscle_label_1.setMinimumSize(QtCore.QSize(60, 20))
        muscle_label_1.setMaximumSize(QtCore.QSize(60, 20))
        muscle_label_1.setAlignment(QtCore.Qt.AlignRight)

        muscle_label_2 = QtWidgets.QLabel("Muscular")
        muscle_label_2.setStyleSheet("background: transparent; font: italic;")
        muscle_label_2.setMinimumSize(QtCore.QSize(60, 20))
        muscle_label_2.setMaximumSize(QtCore.QSize(60, 20))
        muscle_label_2.setAlignment(QtCore.Qt.AlignLeft)

        self.global_muscle_slider = QtWidgets.QSlider()
        self.global_muscle_slider.setMinimumWidth(100)
        self.global_muscle_slider.setRange(0, 100)
        self.global_muscle_slider.setProperty("type", "muscle")
        self.global_muscle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.global_muscle_slider.valueChanged.connect(partial(self.setGlobalSliders, self.global_muscle_slider,
                                                               self.muscleSliders))

        self.global_muscle_reset = QtWidgets.QPushButton()
        self.global_muscle_reset.setMinimumSize(QtCore.QSize(20, 20))
        self.global_muscle_reset.setMaximumSize(QtCore.QSize(20, 20))
        self.global_muscle_reset.setIconSize(QtCore.QSize(20, 20))
        self.global_muscle_reset.setIcon(self.reset_icon)
        img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
        self.global_muscle_reset.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
        self.global_muscle_reset.clicked.connect(partial(self.resetSliderGlobal, self.global_muscle_slider, 0,
                                                         self.muscleSliders, True))

        global_muscle_layout.addWidget(muscle_label)
        global_muscle_layout.addWidget(muscle_label_1)
        global_muscle_layout.addWidget(self.global_muscle_slider)
        global_muscle_layout.addWidget(muscle_label_2)
        global_muscle_layout.addWidget(self.global_muscle_reset)

        # WEIGHT
        global_weight_layout = QtWidgets.QHBoxLayout()
        global_grp_box_layout.addLayout(global_weight_layout)

        weight_label = QtWidgets.QLabel("WEIGHT: ")
        weight_label.setStyleSheet("background: transparent; font: bold;")
        weight_label.setMinimumSize(QtCore.QSize(60, 20))
        weight_label.setMaximumSize(QtCore.QSize(60, 20))

        thin_label = QtWidgets.QLabel("Thin")
        thin_label.setStyleSheet("background: transparent; font: italic;")
        thin_label.setMinimumSize(QtCore.QSize(60, 20))
        thin_label.setMaximumSize(QtCore.QSize(60, 20))
        thin_label.setAlignment(QtCore.Qt.AlignRight)

        heavy_label = QtWidgets.QLabel("Heavy")
        heavy_label.setStyleSheet("background: transparent; font: italic;")
        heavy_label.setMinimumSize(QtCore.QSize(60, 20))
        heavy_label.setMaximumSize(QtCore.QSize(60, 20))
        heavy_label.setAlignment(QtCore.Qt.AlignLeft)

        self.global_weight_slider = QtWidgets.QSlider()
        self.global_weight_slider.setMinimumWidth(100)
        self.global_weight_slider.setRange(0, 100)
        self.global_weight_slider.setValue(50)
        self.global_weight_slider.setProperty("type", "weight")
        self.global_weight_slider.setOrientation(QtCore.Qt.Horizontal)
        self.global_weight_slider.valueChanged.connect(partial(self.setGlobalSliders, self.global_weight_slider,
                                                               self.weightSliders))

        self.global_weight_reset = QtWidgets.QPushButton()
        self.global_weight_reset.setMinimumSize(QtCore.QSize(20, 20))
        self.global_weight_reset.setMaximumSize(QtCore.QSize(20, 20))
        self.global_weight_reset.setIconSize(QtCore.QSize(20, 20))
        self.global_weight_reset.setIcon(self.reset_icon)
        img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
        self.global_weight_reset.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
        self.global_weight_reset.clicked.connect(partial(self.resetSliderGlobal, self.global_weight_slider, 50, self.weightSliders, True))

        global_weight_layout.addWidget(weight_label)
        global_weight_layout.addWidget(thin_label)
        global_weight_layout.addWidget(self.global_weight_slider)
        global_weight_layout.addWidget(heavy_label)
        global_weight_layout.addWidget(self.global_weight_reset)

        # HEIGHT
        global_height_layout = QtWidgets.QHBoxLayout()
        global_grp_box_layout.addLayout(global_height_layout)

        height_label = QtWidgets.QLabel("HEIGHT: ")
        height_label.setStyleSheet("background: transparent; font: bold;")
        height_label.setMinimumSize(QtCore.QSize(60, 20))
        height_label.setMaximumSize(QtCore.QSize(60, 20))

        small_label = QtWidgets.QLabel("Small")
        small_label.setStyleSheet("background: transparent; font: italic;")
        small_label.setMinimumSize(QtCore.QSize(60, 20))
        small_label.setMaximumSize(QtCore.QSize(60, 20))
        small_label.setAlignment(QtCore.Qt.AlignRight)

        tall_label = QtWidgets.QLabel("Tall")
        tall_label.setStyleSheet("background: transparent; font: italic;")
        tall_label.setMinimumSize(QtCore.QSize(60, 20))
        tall_label.setMaximumSize(QtCore.QSize(60, 20))
        tall_label.setAlignment(QtCore.Qt.AlignLeft)

        self.global_height_slider = QtWidgets.QSlider()
        self.global_height_slider.setMinimumWidth(100)
        self.global_height_slider.setRange(0, 100)
        self.global_height_slider.setValue(50)
        self.global_height_slider.setProperty("type", "height")
        self.global_height_slider.setOrientation(QtCore.Qt.Horizontal)
        self.global_height_slider.valueChanged.connect(partial(self.adjustModuleHeight, self.global_height_slider,
                                                               False))

        self.global_height_reset = QtWidgets.QPushButton()
        self.global_height_reset.setMinimumSize(QtCore.QSize(20, 20))
        self.global_height_reset.setMaximumSize(QtCore.QSize(20, 20))
        self.global_height_reset.setIconSize(QtCore.QSize(20, 20))
        self.global_height_reset.setIcon(self.reset_icon)
        img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
        self.global_height_reset.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
        self.global_height_reset.clicked.connect(partial(self.resetHeight, self.global_height_slider, 50))

        global_height_layout.addWidget(height_label)
        global_height_layout.addWidget(small_label)
        global_height_layout.addWidget(self.global_height_slider)
        global_height_layout.addWidget(tall_label)
        global_height_layout.addWidget(self.global_height_reset)

        # Statistics
        spacer = QtWidgets.QSpacerItem(30, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        global_grp_box_layout.addItem(spacer)
        global_stats_layout = QtWidgets.QHBoxLayout()
        global_grp_box_layout.addLayout(global_stats_layout)

        stats_label = QtWidgets.QLabel("STATS: ")
        stats_label.setStyleSheet("background: transparent; font: bold;")
        stats_label.setMinimumSize(QtCore.QSize(60, 15))
        stats_label.setMaximumSize(QtCore.QSize(60, 15))

        characterHeightLabelCM = QtWidgets.QLabel("Character Height (cm): ")
        characterHeightLabelCM.setStyleSheet("background: transparent; font: italic;")
        characterHeightLabelFT = QtWidgets.QLabel("Character Height (ft): ")
        characterHeightLabelFT.setStyleSheet("background: transparent; font: italic;")

        self.cm_height = QtWidgets.QLabel("")
        self.cm_height.setStyleSheet("background: transparent; font: bold; color: #9b7643;")

        self.ft_height = QtWidgets.QLabel("")
        self.ft_height.setStyleSheet("background: transparent; font: bold; color: #9b7643;")

        global_stats_layout.addWidget(stats_label)
        global_stats_layout.addWidget(characterHeightLabelCM)
        global_stats_layout.addWidget(self.cm_height)
        global_stats_layout.addWidget(characterHeightLabelFT)
        global_stats_layout.addWidget(self.ft_height)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # MODULE OVERRIDES
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.module_overrides_group = QtWidgets.QGroupBox("Module Overrides")
        self.module_overrides_group.setObjectName("light")
        self.module_overrides_group.setMinimumSize(QtCore.QSize(380, 420))
        self.module_overrides_group.setMaximumSize(QtCore.QSize(380, 420))
        self.mainLayout.addWidget(self.module_overrides_group)
        self.module_overrides_layout = QtWidgets.QVBoxLayout(self.module_overrides_group)

        # create the scroll contents and the vboxlayout to populate
        self.overrides_scrollContents = QtWidgets.QFrame()
        self.overrides_scrollContents.setObjectName("dark")
        self.scrollContents_layout = QtWidgets.QVBoxLayout()

        # for each valid module, add UI elements
        for each in self.blendshapes:
            if len(each[1]) > 0:
                moduleName = cmds.getAttr(each[0] + ".moduleName")

                # create the module groupbox
                self.widgets[each[0]] = QtWidgets.QGroupBox(moduleName)
                self.widgets[each[0]].setMaximumWidth(360)
                self.widgets[each[0]].setMinimumHeight(0)
                self.widgets[each[0]].setObjectName("light")
                self.widgets[each[0]].setCheckable(True)
                self.widgets[each[0]].setProperty("module", each[0])
                self.widgets[each[0]].setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                                          QtWidgets.QSizePolicy.Fixed))

                self.scrollContents_layout.addWidget(self.widgets[each[0]])

                # groupbox layout
                groupBoxLayout = QtWidgets.QVBoxLayout(self.widgets[each[0]])
                groupBoxFrame = QtWidgets.QFrame(self.widgets[each[0]])
                groupBoxFrame.setStyleSheet("background: transparent;")
                groupBoxFrame.setMinimumWidth(310)
                groupBoxFrame.setMaximumWidth(310)
                groupBoxLayout.addWidget(groupBoxFrame)
                frameLayout = QtWidgets.QVBoxLayout(groupBoxFrame)

                # GENDER
                gender_layout = QtWidgets.QHBoxLayout()
                gender_layout.setProperty("module", each[0])
                gender_layout.setProperty("sliderType", "gender")
                gender_layout.setSpacing(0)
                frameLayout.addLayout(gender_layout)

                gender_label = QtWidgets.QLabel("GENDER: ")
                gender_label.setStyleSheet("background: transparent; font: bold;")
                gender_label.setMinimumSize(QtCore.QSize(50, 20))
                gender_label.setMaximumSize(QtCore.QSize(50, 20))

                male_label = QtWidgets.QLabel("Male")
                male_label.setStyleSheet("background: transparent; font: italic;")
                male_label.setMinimumSize(QtCore.QSize(40, 20))
                male_label.setMaximumSize(QtCore.QSize(40, 20))
                male_label.setAlignment(QtCore.Qt.AlignRight)

                female_label = QtWidgets.QLabel("Female")
                female_label.setStyleSheet("background: transparent; font: italic;")
                female_label.setMinimumSize(QtCore.QSize(50, 20))
                female_label.setMaximumSize(QtCore.QSize(50, 20))
                female_label.setAlignment(QtCore.Qt.AlignLeft)

                gender_slider = QtWidgets.QSlider()
                gender_slider.setProperty("type", "gender")
                gender_slider.setProperty("module", each[0])
                gender_slider.setMinimumWidth(100)
                gender_slider.setRange(0, 100)
                gender_slider.setEnabled(False)
                gender_slider.setOrientation(QtCore.Qt.Horizontal)
                self.genderSliders.append(gender_slider)
                gender_slider.valueChanged.connect(partial(self.setComboSliderValues, each[0], gender_slider, "female", None))

                gender_lock = QtWidgets.QPushButton()
                gender_lock.setMinimumSize(QtCore.QSize(20, 20))
                gender_lock.setMaximumSize(QtCore.QSize(20, 20))
                gender_lock.setIconSize(QtCore.QSize(20, 20))
                gender_lock.setIcon(self.lock_icon)
                gender_lock.clicked.connect(partial(self.toggleSlider, gender_lock, gender_slider))
                img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_lock.png")
                gender_lock.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")

                gender_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

                gender_layout.addWidget(gender_label)
                gender_layout.addWidget(male_label)
                gender_layout.addWidget(gender_slider)
                gender_layout.addWidget(female_label)
                gender_layout.addWidget(gender_lock)
                gender_layout.addItem(gender_spacer)

                # MUSCLE
                muscle_layout = QtWidgets.QHBoxLayout()
                muscle_layout.setProperty("module", each[0])
                muscle_layout.setProperty("sliderType", "muscle")
                muscle_layout.setSpacing(0)
                frameLayout.addLayout(muscle_layout)

                muscle_label = QtWidgets.QLabel("MUSCLE: ")
                muscle_label.setStyleSheet("background: transparent; font: bold;")
                muscle_label.setMinimumSize(QtCore.QSize(50, 20))
                muscle_label.setMaximumSize(QtCore.QSize(50, 20))

                muscle_label_1 = QtWidgets.QLabel("Slight")
                muscle_label_1.setStyleSheet("background: transparent; font: italic;")
                muscle_label_1.setMinimumSize(QtCore.QSize(40, 20))
                muscle_label_1.setMaximumSize(QtCore.QSize(40, 20))
                muscle_label_1.setAlignment(QtCore.Qt.AlignRight)

                muscle_label_2 = QtWidgets.QLabel("Muscular")
                muscle_label_2.setStyleSheet("background: transparent; font: italic;")
                muscle_label_2.setMinimumSize(QtCore.QSize(50, 20))
                muscle_label_2.setMaximumSize(QtCore.QSize(50, 20))
                muscle_label_2.setAlignment(QtCore.Qt.AlignLeft)

                muscle_slider = QtWidgets.QSlider()
                muscle_slider.setProperty("type", "muscle")
                muscle_slider.setProperty("module", each[0])
                muscle_slider.setMinimumWidth(100)
                muscle_slider.setRange(0, 100)
                muscle_slider.setEnabled(False)
                muscle_slider.setOrientation(QtCore.Qt.Horizontal)
                self.muscleSliders.append(muscle_slider)
                muscle_slider.valueChanged.connect(partial(self.setComboSliderValues, each[0], muscle_slider, "buff",
                                                           None))

                muscle_lock = QtWidgets.QPushButton()
                muscle_lock.setStyleSheet(self.style)
                muscle_lock.setMinimumSize(QtCore.QSize(20, 20))
                muscle_lock.setMaximumSize(QtCore.QSize(20, 20))
                muscle_lock.setIconSize(QtCore.QSize(20, 20))
                muscle_lock.setIcon(self.lock_icon)
                muscle_lock.clicked.connect(partial(self.toggleSlider, muscle_lock, muscle_slider))
                img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_lock.png")
                muscle_lock.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")

                muscle_reset = QtWidgets.QPushButton()
                muscle_reset.setMinimumSize(QtCore.QSize(20, 20))
                muscle_reset.setMaximumSize(QtCore.QSize(20, 20))
                muscle_reset.setIconSize(QtCore.QSize(20, 20))
                muscle_reset.setIcon(self.reset_icon)
                img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
                muscle_reset.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
                muscle_reset.clicked.connect(partial(self.resetSliderModule, muscle_slider, 0, each[0], ["buff"]))

                muscle_layout.addWidget(muscle_label)
                muscle_layout.addWidget(muscle_label_1)
                muscle_layout.addWidget(muscle_slider)
                muscle_layout.addWidget(muscle_label_2)
                muscle_layout.addWidget(muscle_lock)
                muscle_layout.addWidget(muscle_reset)

                # WEIGHT
                weight_layout = QtWidgets.QHBoxLayout()
                weight_layout.setProperty("module", each[0])
                weight_layout.setProperty("sliderType", "weight")
                weight_layout.setSpacing(0)
                frameLayout.addLayout(weight_layout)

                weight_label = QtWidgets.QLabel("WEIGHT: ")
                weight_label.setStyleSheet("background: transparent; font: bold;")
                weight_label.setMinimumSize(QtCore.QSize(50, 20))
                weight_label.setMaximumSize(QtCore.QSize(50, 20))

                thin_label = QtWidgets.QLabel("Thin")
                thin_label.setStyleSheet("background: transparent; font: italic;")
                thin_label.setMinimumSize(QtCore.QSize(40, 20))
                thin_label.setMaximumSize(QtCore.QSize(40, 20))
                thin_label.setAlignment(QtCore.Qt.AlignRight)

                heavy_label = QtWidgets.QLabel("Heavy")
                heavy_label.setStyleSheet("background: transparent; font: italic;")
                heavy_label.setMinimumSize(QtCore.QSize(50, 20))
                heavy_label.setMaximumSize(QtCore.QSize(50, 20))
                heavy_label.setAlignment(QtCore.Qt.AlignLeft)

                weight_slider = QtWidgets.QSlider()
                weight_slider.setProperty("type", "weight")
                weight_slider.setProperty("module", each[0])
                self.weightSliders.append(weight_slider)
                weight_slider.setMinimumWidth(100)
                weight_slider.setRange(0, 100)
                weight_slider.setValue(50)
                weight_slider.setEnabled(False)
                weight_slider.setOrientation(QtCore.Qt.Horizontal)
                weight_slider.valueChanged.connect(partial(self.setComboSliderValues, each[0], weight_slider,
                                                           "heavy", "slim"))

                weight_lock = QtWidgets.QPushButton()
                weight_lock.setMinimumSize(QtCore.QSize(20, 20))
                weight_lock.setMaximumSize(QtCore.QSize(20, 20))
                weight_lock.setIconSize(QtCore.QSize(20, 20))
                weight_lock.setIcon(self.lock_icon)
                weight_lock.clicked.connect(partial(self.toggleSlider, weight_lock, weight_slider))
                img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_lock.png")
                weight_lock.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")

                weight_reset = QtWidgets.QPushButton()
                weight_reset.setMinimumSize(QtCore.QSize(20, 20))
                weight_reset.setMaximumSize(QtCore.QSize(20, 20))
                weight_reset.setIconSize(QtCore.QSize(20, 20))
                weight_reset.setIcon(self.reset_icon)
                img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
                weight_reset.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
                weight_reset.clicked.connect(partial(self.resetSliderModule, weight_slider, 50, each[0], ["heavy", "slim"]))

                weight_layout.addWidget(weight_label)
                weight_layout.addWidget(thin_label)
                weight_layout.addWidget(weight_slider)
                weight_layout.addWidget(heavy_label)
                weight_layout.addWidget(weight_lock)
                weight_layout.addWidget(weight_reset)

                # LENGTH
                modName = cmds.getAttr(each[0] + ".moduleName")
                if cmds.objExists(modName + "_length_grp"):

                    length_layout = QtWidgets.QHBoxLayout()
                    length_layout.setProperty("module", each[0])
                    length_layout.setProperty("sliderType", "length")
                    length_layout.setSpacing(0)
                    frameLayout.addLayout(length_layout)

                    length_label = QtWidgets.QLabel("LENGTH: ")
                    length_label.setStyleSheet("background: transparent; font: bold;")
                    length_label.setMinimumSize(QtCore.QSize(50, 20))
                    length_label.setMaximumSize(QtCore.QSize(50, 20))

                    short_label = QtWidgets.QLabel("Short")
                    short_label.setStyleSheet("background: transparent; font: italic;")
                    short_label.setMinimumSize(QtCore.QSize(40, 20))
                    short_label.setMaximumSize(QtCore.QSize(40, 20))
                    short_label.setAlignment(QtCore.Qt.AlignRight)

                    long_label = QtWidgets.QLabel("Long")
                    long_label.setStyleSheet("background: transparent; font: italic;")
                    long_label.setMinimumSize(QtCore.QSize(50, 20))
                    long_label.setMaximumSize(QtCore.QSize(50, 20))
                    long_label.setAlignment(QtCore.Qt.AlignLeft)

                    length_slider = QtWidgets.QSlider()
                    length_slider.setProperty("type", "length")
                    length_slider.setProperty("module", each[0])
                    length_slider.setMinimumWidth(100)
                    length_slider.setRange(0, 100)
                    length_slider.setValue(50)
                    length_slider.setOrientation(QtCore.Qt.Horizontal)
                    length_slider.valueChanged.connect(partial(self.adjustModuleLength, each[0], length_slider))

                    length_spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

                    length_reset = QtWidgets.QPushButton()
                    length_reset.setMinimumSize(QtCore.QSize(20, 20))
                    length_reset.setMaximumSize(QtCore.QSize(20, 20))
                    length_reset.setIconSize(QtCore.QSize(20, 20))
                    length_reset.setIcon(self.reset_icon)
                    img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
                    length_reset.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
                    length_reset.clicked.connect(partial(self.resetSliderModule, length_slider, 50, each[0], ["length"], True))
                    self.sliders.append([length_slider, 50, each[0], ["length"], True])

                    length_layout.addWidget(length_label)
                    length_layout.addWidget(short_label)
                    length_layout.addWidget(length_slider)
                    length_layout.addWidget(long_label)
                    length_layout.addItem(length_spacer)
                    length_layout.addWidget(length_reset)

                    self.moduleGlobalSliders[each[0]] = [gender_slider, muscle_slider, weight_slider, length_slider]

                if not cmds.objExists(modName + "_length_grp"):
                    self.moduleGlobalSliders[each[0]] = [gender_slider, muscle_slider, weight_slider]

                # ADVANCED SECTION
                advanced_groupBox = QtWidgets.QGroupBox("Advanced")
                advanced_groupBox.setMinimumWidth(300)
                advanced_groupBox.setMaximumWidth(300)
                advanced_groupBox.setMinimumHeight(0)
                advanced_groupBox.setCheckable(True)
                advanced_groupBox.setProperty("module", each[0])
                advanced_groupBox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                                          QtWidgets.QSizePolicy.Fixed))

                frameLayout.addWidget(advanced_groupBox)

                # add layouts for advanced section
                advancedLayout = QtWidgets.QVBoxLayout(advanced_groupBox)
                advancedFrame = QtWidgets.QFrame(advanced_groupBox)
                advancedFrame.setStyleSheet("background: transparent;")
                advancedFrame.setMinimumWidth(280)
                advancedFrame.setMaximumWidth(280)
                advancedLayout.addWidget(advancedFrame)
                advancedContentLayout = QtWidgets.QVBoxLayout(advancedFrame)

                sliderList = []

                # add direct control of each geo's morphs
                for geoData in each[1]:
                    geo = geoData[0]
                    morphs = geoData[1]

                    geo_label = QtWidgets.QLabel(geo.partition("_proxy_geo")[0])
                    geo_label.setStyleSheet("background: transparent; font: bold;")
                    advancedContentLayout.addWidget(geo_label)

                    # add sliders for each morph
                    for morph in morphs:
                        morph_layout = QtWidgets.QHBoxLayout()
                        morph_layout.setSpacing(0)
                        advancedContentLayout.addLayout(morph_layout)
                        spacerItem = QtWidgets.QSpacerItem(30, 0, QtWidgets.QSizePolicy.Fixed,
                                                           QtWidgets.QSizePolicy.Fixed)
                        morph_layout.addItem(spacerItem)

                        morph_niceName = morph.rpartition(".")[2].partition("_")[0]
                        morph_label = QtWidgets.QLabel(morph_niceName)
                        morph_label.setStyleSheet("background: transparent; font: italic;")
                        morph_label.setAlignment(QtCore.Qt.AlignRight)
                        morph_layout.addWidget(morph_label)

                        morph_slider = QtWidgets.QSlider()
                        morph_slider.setEnabled(False)
                        morph_slider.setMinimumWidth(150)
                        morph_slider.setMaximumWidth(150)
                        morph_slider.setRange(0, 100)
                        morph_slider.setValue(0)
                        morph_slider.setProperty("name", morph_niceName)
                        morph_slider.setProperty("shape", morph)
                        morph_slider.setProperty("module", each[0])
                        morph_slider.setProperty("geo", geo.partition("_proxy_geo")[0])
                        morph_slider.setOrientation(QtCore.Qt.Horizontal)
                        morph_slider.valueChanged.connect(partial(self.setSliderValues, morph_slider, morph))
                        morph_layout.addWidget(morph_slider)
                        sliderList.append(morph_slider)

                        lock_button = QtWidgets.QPushButton()
                        lock_button.setMinimumSize(QtCore.QSize(20, 20))
                        lock_button.setMaximumSize(QtCore.QSize(20, 20))
                        lock_button.setIconSize(QtCore.QSize(20, 20))
                        lock_button.setIcon(self.lock_icon)
                        lock_button.clicked.connect(partial(self.toggleSlider, lock_button, morph_slider))
                        img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_lock.png")
                        lock_button.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
                        morph_layout.addWidget(lock_button)

                        reset_button = QtWidgets.QPushButton()
                        reset_button.setMinimumSize(QtCore.QSize(20, 20))
                        reset_button.setMaximumSize(QtCore.QSize(20, 20))
                        reset_button.setIconSize(QtCore.QSize(20, 20))
                        reset_button.setIcon(self.reset_icon)
                        img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset.png")
                        reset_button.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
                        morph_layout.addWidget(reset_button)
                        reset_button.clicked.connect(partial(self.resetSlider, morph_slider, 0))

                # add data to module sliders dict
                self.moduleSliders[each[0]] = sliderList

                # setup collapsible groupbox signal/slot
                QtCore.QObject.connect(advanced_groupBox, QtCore.SIGNAL("toggled(bool)"), advancedFrame.setVisible)
                advanced_groupBox.setChecked(False)
                # setup collapsible groupbox signal/slot
                QtCore.QObject.connect(self.widgets[each[0]], QtCore.SIGNAL("toggled(bool)"), groupBoxFrame.setVisible)
                self.widgets[each[0]].setChecked(False)

        # add a spacer
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scrollContents_layout.addItem(spacerItem)

        # add reset all button
        self.resetAll_button = QtWidgets.QPushButton("Reset All")
        self.resetAll_button.setObjectName("settings")
        self.resetAll_button.setMinimumHeight(30)
        self.resetAll_button.setMaximumHeight(30)
        img = utils.returnNicePath(self.iconsPath, "Help/tooltips/physique_reset_all.png")
        self.resetAll_button.setToolTip("<img src = \"" + img + "\" width = \"300\" height = \"150\"/>")
        self.resetAll_button.clicked.connect(self.resetAll)
        self.mainLayout.addWidget(self.resetAll_button)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findModuleShapes(self):
        """

        Go through each module, and select all module nodes under that module. Within those nodes, find the proxy geo,
        and see if any of the proxy geo has blendshapes. If there are blendshapes, append that data to self.blendshapes
        list.

        :return: None

        """

        self.blendshapes = []

        modules = utils.returnRigModules()
        for mod in modules:
            modName = cmds.getAttr(mod + ".moduleName")

            geoList = []

            # select module nodes
            cmds.select(modName + "_mover_grp", hi=True)
            moduleNodes = cmds.ls(sl=True)

            # find proxy geo
            for node in moduleNodes:
                if node.find("proxy_geo") != -1:
                    if cmds.nodeType(node) == "transform":
                        shapeNodes = cmds.listRelatives(node, shapes=True)
                        if len(shapeNodes) > 0:
                            # see if the proxy geo shape has a blendshape connected
                            for shapeNode in shapeNodes:
                                connections = cmds.listConnections(shapeNode + ".inMesh")
                                if connections is not None:
                                    morphList = []
                                    # if so, get the targets
                                    for connection in connections:
                                        if cmds.objExists(connection + ".weight"):
                                            targets = cmds.listAttr(connection + ".weight", m=True)
                                            # add all that to the morph list.
                                            for target in targets:
                                                morphList.append(connection + "." + target)
                                            # add the morph list to the geoList
                                            geoList.append([node, morphList])

            # append the geo list to the main list
            self.blendshapes.append([mod, geoList])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def adjustModuleHeight(self, slider, passive=False, *args):
        """

        Takes in the slider value of the passed in slider, and scales the root mover within a remapped range.

        :param slider: Slider of which to query the value.
        :param passive: Whether or not to scale the root mover or to just simply update the UI with the height info.
        :param args:
        :return: None

        """

        value = slider.value()

        if cmds.objExists("root_mover"):

            # remap slider value into scale value then set scale
            newScale = self.remapRange(100.0, 0.0, 2.0, 0.0, float(value))

            if passive is False:
                cmds.setAttr("root_mover.scaleX", newScale)
                cmds.setAttr("root_mover.scaleY", newScale)
                cmds.setAttr("root_mover.scaleZ", newScale)

            # 50 on slider == 182.88 cm, and 0 = 0cm, and 100 = 365.76
            self.getHeight()

            self.cm_height.setText("%.2f" % self.height)
            inches = self.height * 0.39
            feet = inches / 12
            fact, whole = math.modf(feet)
            inches = fact/.083
            string = "%.0f" % whole + "' " + "%.0f\"" % inches
            self.ft_height.setText(string)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def adjustModuleLength(self, module, slider, *args):
        """

        For the given module, take in the passed in slider to get the value, and scale the module's length grp by
        the remapped range amount, then snap the joint movers of the module to the children of the module's length
        group to quickly change the length of the module.

        .. note:: This does not need to be implemented on every module. Only a couple modules have this functionality.

        :param module: the module to operate on.
        :param slider: the slider whose value to query.
        :param args:
        :return: None

        """

        # ToDo The torso module with no pelvis has issues with module length. See notes:
        # Because the length grp is still under the pelvis, the length function is snapping relative to that location
        # rather than spine 01, which is now the base of the module. This is an edge case, and it doesn't really break
        # anything, it just causes a minor inconvenience, so leaving it be for now.

        modName = cmds.getAttr(module + ".moduleName")
        value = slider.value()

        # get length group
        if cmds.objExists(modName + "_length_grp"):

            # remap slider value into scale value then set scale
            newScale = self.remapRange(100.0, 0.0, 2.0, 0.0, float(value))
            cmds.setAttr(modName + "_length_grp.scaleX", newScale)

            # get children
            children = cmds.listRelatives(modName + "_length_grp", children=True)

            if children is not None:
                for child in children:
                    if cmds.objExists(child + ".mover"):
                        mover = cmds.listConnections(child + ".mover")[0]

                        cmds.delete(cmds.pointConstraint(child, mover)[0])

        for each in self.moduleSliders[module]:
            name = each.property("name")
            valueData = self.setComoboValue(float(value), "long", "short")

            for data in valueData:
                if name == data[0]:
                    if each.isEnabled() is False:
                        each.setValue(data[1] * 100)

        # get bounds
        if cmds.objExists("JointMover"):
            cmds.select("*_mover")
            selection = cmds.ls(sl=True)
            bounds = cmds.exactWorldBoundingBox(selection, ce=True, ii=True)
            height = abs(bounds[2] - bounds[5])

            self.cm_height.setText("%.2f" % height)
            inches = height * 0.39
            feet = inches / 12
            fact, whole = math.modf(feet)
            inches = fact/.083
            string = "%.0f" % whole + "' " + "%.0f\"" % inches
            self.ft_height.setText(string)
            cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setGlobalSliders(self, slider, sliderList, *args):
        """

        Takes the value of a global slider and applies it to a list of sliders associated to the global slider. For
        example, adjusting the global weight slider should then adjust all module weight sliders.

        :param slider: the global slider whose value to query.
        :param sliderList: the list of sliders this global slider should affect.
        :param args:
        :return: None

        """

        # get slider value
        value = slider.value()

        for each in sliderList:
            if each.isEnabled() is False:
                each.setValue(value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setSliderValues(self, slider, morph, *args):
        """
        Takes in a slider whose value is queried, then remaps that to a 0.0 - 1.0 range and sets the corresponding
        morph target to that value.

        :param slider: The slider whose value to query.
        :param morph: The morph whose value needs to be set.
        :param args:
        :return: None

        """

        value = float(slider.value()) / 100.0
        cmds.setAttr(morph, value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setComboSliderValues(self, module, slider, keyword1, keyword2, *args):
        """
        Given the arguments, look at all sliders belonging to the input module, searching for sliders whose 'name'
        property matches the keywords, then setting those sliders' values accordingly.

        :param module: The module to act on
        :param slider: The slider whose value to query.
        :param keyword1: The first property keyword to search for in the list of moduleSliders
        :param keyword2: The second property keyword to search for in the list of moduleSliders
        :param args:
        :return: None

        .. seealso:: ART_PhysiqueEditorUI.setComoboValue()

        """

        value = slider.value()

        for each in self.moduleSliders[module]:
            name = each.property("name")
            valueData = self.setComoboValue(value, keyword1, keyword2)

            for data in valueData:
                if name == data[0]:
                    if each.isEnabled() is False:
                        each.setValue(data[1] * 100)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setComoboValue(self, value, keyword1, keyword2):
        """
        Takes an input value and remaps it to 0.0 - 1.0 to then be set on an opposing set of morph targets. ( like thin
        and heavy)

        :param value: a value between 0 and 100.
        :param keyword1: a search keyword for a morph target (for example, thin and heavy).
        :param keyword2: a search keyword for a morph target (for example, thin and heavy).
        :return: list of pair values, where the first entry is the morph target keyword and the second is the value.

        .. seealso:: ART_PhysiqueEditor.remapRange()

        """

        if value == 50:
            return [[keyword1, 0], [keyword2, 0]]

        if value < 50:
            newValue = self.remapRange(0.0, 50.0, 1.0, 0.0, value)
            return [[keyword1, 0], [keyword2, newValue]]

        if value > 50:
            newValue = self.remapRange(100.0, 50.0, 1.0, 0.0, value)
            return [[keyword1, newValue], [keyword2, 0]]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setSingleValue(self, value, keyword1):
        """
        Takes an input value and remaps it to 0.0 - 1.0 to then be set on a single morph target.

        :param value: a value between 0 and 100.
        :param keyword1: a search keyword for a morph target (for example, gender).
        :return: pair of data where the first entry is the morph target, and the second is the value to set.

        .. seealso:: ART_PhysiqueEditor.remapRange()

        """

        if value == 50:
            return [keyword1, 0]

        if value < 50:
            newValue = self.remapRange(0.0, 50.0, 1.0, 0.0, value)
            return [keyword1, 0]

        if value > 50:
            newValue = self.remapRange(100.0, 50.0, 1.0, 0.0, value)
            return [keyword1, newValue]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetSliderGlobal(self, slider, value, sliders, macro=False):
        """
        When a global slider is reset, that slider's value is set to the input value. If macro is True, then any
        associated sliders to that global slider (for example, all module weight sliders) are also reset.

        :param slider: slider whose value to set
        :param value: the value to set the slider to.
        :param sliders: any subsequent sliders that should also be set to that value.
        :param macro: Whether or not to reset associated sliders
        :return: None

        """

        slider.setValue(value)

        if macro is True:
            for each in sliders:
                each.setValue(value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetSlider(self, slider, value):
        """

        Resets a singular slider to the given default value.

        :param slider: Slider whose value to reset.
        :param value: The value to reset to.
        :return: None

        """

        slider.setValue(value)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetSliderModule(self, slider, value, module, keywords, length=False):
        """

        Takes in a global module slider, and a value to reset to, and for all module sliders whose 'name' property
        matches any of the keywords, set those morph target sliders to 0.

        :param slider: global module override slider whose value to reset
        :param value: value to reset to.
        :param module: module to act on.
        :param keywords: keywords to search for on each module slider's name property.
        :param length: whether or not to reset length (scale to 1)
        :return: None

        """

        slider.setValue(value)

        for each in self.moduleSliders[module]:
            data = each.property("name")
            if data in keywords:
                each.setValue(0)

        if length is True:
            modName = cmds.getAttr(module + ".moduleName")

            # get length group
            if cmds.objExists(modName + "_length_grp"):
                cmds.setAttr(modName + "_length_grp.scaleX", 1)

                # get children
                children = cmds.listRelatives(modName + "_length_grp", children=True)

                if children is not None:
                    for child in children:
                        if cmds.objExists(child + ".mover"):
                            mover = cmds.listConnections(child + ".mover")[0]
                            cmds.delete(cmds.pointConstraint(child, mover)[0])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetAll(self):
        """

        Resets all sliders: global, module overrides, and morph target overrides.

        :return: None

        """

        self.resetSliderGlobal(self.global_muscle_slider, 0, self.muscleSliders, True)
        self.resetSliderGlobal(self.global_weight_slider, 50, self.weightSliders, True)

        for each in self.sliders:
            self.resetSliderModule(each[0], each[1], each[2], each[3], each[4])

        for each in self.unlocked:
            each[1].setEnabled(False)
            each[0].setIcon(self.lock_icon)
            each[0].setProperty("locked", True)

        self.unlocked = []

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def resetHeight(self, slider, value):
        """

        Resets the character height to 1.0 (whatever 1 represents, which is the original height).

        :param slider: slider whose value to set.
        :param value: value to set on the slider.
        :return: None

        """

        slider.setValue(value)

        cmds.setAttr("root_mover.scaleX", 1.0)
        cmds.setAttr("root_mover.scaleY", 1.0)
        cmds.setAttr("root_mover.scaleZ", 1.0)

        # get bounds
        self.getHeight()
        self.adjustModuleHeight(self.global_height_slider, True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def remapRange(self, oldMax, oldMin, newMax, newMin, value):
        """

        Takes in the old range, and a new range, and a slider value, and returns a value remapped from the old range to
        the new range. For example, if the old range is 0 - 100, and the new range is 0.0 to 2.0, and the slider value
        is 65, the returned value would be 1.3.

        :param oldMax: the old maximum value in the range
        :param oldMin: the old minimum value in the range
        :param newMax: the new maximum value in the new range
        :param newMin: the new minimum value in the new range
        :param value: the current slider value

        :return: the new value in the newly remapped range.

        """

        OldRange = (oldMax - oldMin)
        NewRange = (newMax - newMin)
        newValue = (((value - oldMin) * NewRange) / OldRange) + 0.0

        return newValue

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleSlider(self, button, slider, *args):
        """

        Toggles whether the slider is enabled or disabled for user input. By default, override sliders are disabled
        until toggled.

        :param button: The lock/unlock button whose state to query.
        :param slider: The slider to disable/enable
        :param args:
        :return: None

        """

        state = button.property("locked")

        if state is None:
            state = True

        if state is True:
            slider.setEnabled(True)
            button.setIcon(self.unlock_icon)
            button.setProperty("locked", False)

            # add to self.unlocked list
            self.unlocked.append([button, slider])

        if state is False:
            slider.setEnabled(False)
            button.setIcon(self.lock_icon)
            button.setProperty("locked", True)

            if [button, slider] in self.unlocked:
                index = self.unlocked.index([button, slider])
                self.unlocked.pop(index)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):
        """

        When the interface is closed, this function gathers the slider data and adds it to a network node, so that
        when the interface is opened again, the sliders are in the state they were last in, which is the state that
        represents the character's physique.

        :param event: close event
        :return: None

        """
        print "CLOSE EVENT"
        if cmds.objExists("physique_data"):
            cmds.delete("physique_data")
        cmds.createNode("network", name="physique_data")

        # GLOBAL SLIDERS
        try:
            for each in [self.global_gender_slider, self.global_muscle_slider, self.global_weight_slider,
                         self.global_height_slider]:
                sliderType = each.property("type")
                sliderValue = each.value()

                if not cmds.objExists("physique_data.global_" + str(sliderType)):
                    cmds.addAttr("physique_data", ln="global_" + str(sliderType))
                cmds.setAttr("physique_data.global_" + str(sliderType), sliderValue)

        except Exception, e:
            print "ART_PhysiqueEditorUI.py: closeEvent: Global Sliders: " + str(e)

        # MODULE SLIDERS
        modules = utils.returnRigModules()
        for mod in modules:

            try:
                for slider in self.moduleGlobalSliders[mod]:
                    sliderType = slider.property("type")
                    sliderValue = slider.value()

                    if not cmds.objExists("physique_data." + str(mod) + "_" + str(sliderType)):
                        cmds.addAttr("physique_data", ln=str(mod) + "_" + str(sliderType))
                    cmds.setAttr("physique_data." + str(mod) + "_" + str(sliderType), sliderValue)

            except Exception, e:
                print "ART_PhysiqueEditorUI.py: closeEvent: Module Sliders: " + str(e)

            # MORPH SLIDERS
            try:
                for morphSlider in self.moduleSliders[mod]:

                    slider_type = morphSlider.property("name")
                    slider_name = morphSlider.property("geo")
                    slider_value = morphSlider.value()

                    if not cmds.objExists("physique_data.morph_" + str(slider_name) + "_" + str(slider_type)):
                        cmds.addAttr("physique_data", ln="morph_" + str(slider_name) + "_" + str(slider_type))
                    cmds.setAttr("physique_data.morph_" + str(slider_name) + "_" + str(slider_type), slider_value)

            except Exception, e:
                print "ART_PhysiqueEditorUI.py: closeEvent: Morph Sliders: " + str(e)

        # MISC
        if not cmds.objExists("physique_data.cmText"):
            cmds.addAttr("physique_data", ln="cmText", dt="string")
        cmds.setAttr("physique_data.cmText", self.cm_height.text(), type="string")

        if not cmds.objExists("physique_data.ftText"):
            cmds.addAttr("physique_data", ln="ftText", dt="string")
        cmds.setAttr("physique_data.ftText", self.ft_height.text(), type="string")

        self.getHeight()
        if not cmds.objExists("physique_data.height"):
            cmds.addAttr("physique_data", ln="height")
        cmds.setAttr("physique_data.height", self.height)

        if not cmds.objExists("physique_data.scale"):
            cmds.addAttr("physique_data", ln="scale")
        cmds.setAttr("physique_data.scale", cmds.getAttr("root_mover.scaleX"))

        # event.accept()
        self.deleteLater()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getHeight(self):
        """

        Gets the character's bounds and computes the height in centimeters.

        :return: None

        """

        # get bounds
        if cmds.objExists("JointMover"):
            cmds.select("*_mover")
            selection = cmds.ls(sl=True)
            bounds = cmds.exactWorldBoundingBox(selection, ce=True, ii=True)
            if self.up == "z":
                self.height = abs(bounds[2] - bounds[5])
            if self.up == "y":
                self.height = abs(bounds[1] - bounds[4])
        cmds.select(clear=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def populateUI(self):
        """

        When the interface is launched, if there is a physique_data node in the scene, that data is used to set the
        sliders on the UI to represent the character's physique.

        .. todo:: This only works within a maya session. If a character has been saved with a physique, and the maya
                  session is new, then when the UI is opened, these lists will have no data to populate and the UI
                  will not represent the character's physique settings. This data needs to ideally be stored on the
                  character node in the scene rather than in these lists.

        :return: None

        """

        if cmds.objExists("physique_data"):
            attrs = cmds.listAttr("physique_data", ud=True)

            globalData = []
            moduleData = []
            morphData = []

            for attr in attrs:

                if attr.find("global_") == 0:
                    globalData.append([attr, cmds.getAttr("physique_data." + attr)])

                if attr.find("Module") != -1:
                    moduleData.append([attr, cmds.getAttr("physique_data." + attr)])

                if attr.find("morph_") != -1:
                    morphData.append([attr, cmds.getAttr("physique_data." + attr)])

            # # GLOBAL SLIDERS
            for slider in [self.global_gender_slider, self.global_muscle_slider, self.global_weight_slider,
                           self.global_height_slider]:
                sliderType = slider.property("type")
                sliderType = "global_" + sliderType
                for each in globalData:
                    if sliderType == each[0]:
                        slider.setValue(each[1])

            # # MODULE SLIDERS
            modules = utils.returnRigModules()
            for mod in modules:
                try:
                    for moduleSlider in self.moduleGlobalSliders[mod]:
                        sliderType = moduleSlider.property("type")
                        sliderType = mod + "_" + sliderType
                        for each in moduleData:
                            if sliderType == each[0]:
                                moduleSlider.setValue(each[1])
                except Exception, e:
                    print str(e)

                # # MORPH SLIDERS
                try:
                    for morphSlider in self.moduleSliders[mod]:
                        sliderType = morphSlider.property("name")
                        geo = morphSlider.property("geo")
                        sliderType = "morph_" + geo + "_" + sliderType

                        for each in morphData:
                            if sliderType == each[0]:
                                morphSlider.setValue(each[1])
                except Exception, e:
                    print str(e)

            # # MISC
            try:
                self.cm_height.setText(cmds.getAttr("physique_data.cmText"))
                self.ft_height.setText(cmds.getAttr("physique_data.ftText"))
                self.height = cmds.getAttr("physique_data.height")
                cmds.setAttr("root_mover.scaleX", cmds.getAttr("physique_data.scale"))
                cmds.setAttr("root_mover.scaleY", cmds.getAttr("physique_data.scale"))
                cmds.setAttr("root_mover.scaleZ", cmds.getAttr("physique_data.scale"))
            except Exception, e:
                print str(e)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run(ui_inst):
    """

    Deletes the UI if it exists, then instatiates the class, building the tool and the UI.

    :param ui_inst: the ART_RigCreatorUI instance.
    :return: the instance of this tool

    """

    if cmds.window("ART_PhysiqueEditorUI", exists=True):
        cmds.deleteUI("ART_PhysiqueEditorUI", wnd=True)

    gui = ART_PhysiqueEditorUI(ui_inst, interfaceUtils.getMainWindow())
    gui.show()
    return gui
