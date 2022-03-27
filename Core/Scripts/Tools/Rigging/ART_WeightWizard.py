from ThirdParty.Qt import QtGui, QtCore, QtWidgets
from functools import partial
import maya.cmds as cmds
import os
import Utilities.utils as utils
import Utilities.riggingUtils as riggingUtils
import Utilities.interfaceUtils as interfaceUtils

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


def getMainWindow():
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    # pyside QMainWindow takes in a QWidget rather than QObject
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


windowTitle = "Weight Wizard"
windowObject = "pyArtWeightWizardWin"


class WeightWizard(QtWidgets.QMainWindow):
    def __init__(self, rigUiInst, parent=None):
        # call base class constructor
        super(WeightWizard, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # store rigUiInst in class
        self.rigUiInst = rigUiInst

        # set size policy
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)

        # load toolbar stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # set qt object name
        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.resize(600, 400)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(600, 400))
        self.setMaximumSize(QtCore.QSize(600, 400))

        # Create a stackedWidget
        self.stackWidget = QtWidgets.QStackedWidget()
        self.layout.addWidget(self.stackWidget)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # PAGE ONE: SKIN PROXY GEO
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.page1 = QtWidgets.QFrame()
        self.page1.setObjectName("dark")
        self.stackWidget.addWidget(self.page1)
        self.page1MainLayout = QtWidgets.QVBoxLayout(self.page1)

        # label
        pageOneLabel = QtWidgets.QLabel("Skin Weight Proxy Geometry?")
        pageOneLabel.setStyleSheet("background: transparent;")
        self.page1MainLayout.addWidget(pageOneLabel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        pageOneLabel.setFont(font)

        # image
        self.pageOneInfo = QtWidgets.QFrame()
        self.pageOneInfo.setMinimumSize(QtCore.QSize(560, 250))
        self.pageOneInfo.setMaximumSize(QtCore.QSize(560, 250))
        self.page1MainLayout.addWidget(self.pageOneInfo)

        image = utils.returnNicePath(self.iconsPath, "System/backgrounds/weightProxy.png")
        self.pageOneInfo.setStyleSheet("background-image: url(" + image + ");")

        # buttons
        self.pageOneButtonLayout = QtWidgets.QHBoxLayout()
        self.page1MainLayout.addLayout(self.pageOneButtonLayout)
        self.skinProxyFalseBtn = QtWidgets.QPushButton("No")
        self.skinProxyFalseBtn.setMinimumHeight(50)
        self.skinProxyFalseBtn.setFont(font)
        self.skinProxyTrueBtn = QtWidgets.QPushButton("Yes")
        self.skinProxyTrueBtn.setMinimumHeight(50)
        self.skinProxyTrueBtn.setFont(font)
        self.pageOneButtonLayout.addWidget(self.skinProxyFalseBtn)
        self.pageOneButtonLayout.addWidget(self.skinProxyTrueBtn)

        self.skinProxyFalseBtn.setObjectName("settings")
        self.skinProxyTrueBtn.setObjectName("settings")

        # button hookups
        self.skinProxyFalseBtn.clicked.connect(self.checkForCustomMeshes)
        self.skinProxyTrueBtn.clicked.connect(self.skinProxyGeo)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # PAGE TWO: NO CUSTOM GEO FOUND
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.page2 = QtWidgets.QFrame()
        self.stackWidget.addWidget(self.page2)
        self.page2MainLayout = QtWidgets.QVBoxLayout(self.page2)
        self.page2.setObjectName("dark")

        # label
        pageTwoLabel = QtWidgets.QLabel("Skin Weight Custom Geometry?")
        self.page2MainLayout.addWidget(pageTwoLabel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        pageTwoLabel.setFont(font)

        # image
        self.pageTwoInfo = QtWidgets.QFrame()
        self.pageTwoInfo.setMinimumSize(QtCore.QSize(560, 250))
        self.pageTwoInfo.setMaximumSize(QtCore.QSize(560, 250))
        self.page2MainLayout.addWidget(self.pageTwoInfo)

        image = utils.returnNicePath(self.iconsPath, "System/backgrounds/geoNotFound.png")
        self.pageTwoInfo.setStyleSheet("background-image: url(" + image + ");")

        # buttons
        self.pageTwoButtonLayout = QtWidgets.QHBoxLayout()
        self.page2MainLayout.addLayout(self.pageTwoButtonLayout)
        self.skipStepButton = QtWidgets.QPushButton("Skip This Step")
        self.skipStepButton.setMinimumHeight(50)
        self.skipStepButton.setFont(font)
        self.addMeshesButton = QtWidgets.QPushButton("Add Meshes")
        self.addMeshesButton.setMinimumHeight(50)
        self.addMeshesButton.setFont(font)
        self.pageTwoButtonLayout.addWidget(self.skipStepButton)
        self.pageTwoButtonLayout.addWidget(self.addMeshesButton)
        self.addMeshesButton.setObjectName("settings")
        self.skipStepButton.setObjectName("settings")

        # connect button
        self.skipStepButton.clicked.connect(self.closeWizard)
        self.addMeshesButton.clicked.connect(self.addCustomMeshes)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # PAGE THREE: SKIN CUSTOM GEO
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.page3 = QtWidgets.QFrame()
        self.stackWidget.addWidget(self.page3)
        self.page3MainLayout = QtWidgets.QVBoxLayout(self.page3)
        self.page3.setObjectName("dark")

        # label
        pageThreeLabel = QtWidgets.QLabel("Skin Weight Custom Geometry?")
        self.page3MainLayout.addWidget(pageThreeLabel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        pageThreeLabel.setFont(font)

        # image
        self.pageThreeInfo = QtWidgets.QFrame()
        self.pageThreeInfo.setMinimumSize(QtCore.QSize(560, 250))
        self.pageThreeInfo.setMaximumSize(QtCore.QSize(560, 250))
        self.page3MainLayout.addWidget(self.pageThreeInfo)

        image = utils.returnNicePath(self.iconsPath, "System/backgrounds/skinCustom.png")
        self.pageThreeInfo.setStyleSheet("background-image: url(" + image + ");")

        # buttons
        self.pageThreeButtonLayout = QtWidgets.QHBoxLayout()
        self.page3MainLayout.addLayout(self.pageThreeButtonLayout)
        self.skinGeoFalseBtn = QtWidgets.QPushButton("No")
        self.skinGeoFalseBtn.setMinimumHeight(50)
        self.skinGeoFalseBtn.setFont(font)
        self.skinGeoTrueBtn = QtWidgets.QPushButton("Yes")
        self.skinGeoTrueBtn.setMinimumHeight(50)
        self.skinGeoTrueBtn.setFont(font)
        self.pageThreeButtonLayout.addWidget(self.skinGeoFalseBtn)
        self.pageThreeButtonLayout.addWidget(self.skinGeoTrueBtn)
        self.skinGeoTrueBtn.setObjectName("settings")
        self.skinGeoFalseBtn.setObjectName("settings")

        # connect buttons
        self.skinGeoTrueBtn.clicked.connect(self.skinTools)
        self.skinGeoFalseBtn.clicked.connect(self.closeWizard)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # PAGE FOUR: SKIN TOOLS
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.page4 = QtWidgets.QFrame()
        self.stackWidget.addWidget(self.page4)
        self.page4TopLayout = QtWidgets.QVBoxLayout(self.page4)
        self.page4MainLayout = QtWidgets.QHBoxLayout()
        self.page4TopLayout.addLayout(self.page4MainLayout)

        # vertical layout for lists
        self.page4VerticalLayout = QtWidgets.QVBoxLayout()
        self.page4MainLayout.addLayout(self.page4VerticalLayout)

        # list widgets for meshes/joints
        self.splitter = QtWidgets.QSplitter()
        self.page4VerticalLayout.addWidget(self.splitter)

        # add geo list widget
        self.geoLayoutWidget = QtWidgets.QWidget()
        self.geoLayout = QtWidgets.QVBoxLayout(self.geoLayoutWidget)
        label = QtWidgets.QLabel("Skinnable Geo:")
        label.setFont(font)
        self.geoLayout.addWidget(label)

        self.geoList = QtWidgets.QListWidget()
        self.geoLayout.addWidget(self.geoList)
        self.splitter.addWidget(self.geoLayoutWidget)

        # populate geo list
        skinnableGeo = self.findCustomGeo()
        for geo in skinnableGeo:
            self.geoList.addItem(geo)

        # geo list signals
        self.geoList.itemDoubleClicked.connect(self.selectGeo)

        # add joint list/layout
        self.splitterWidget = QtWidgets.QWidget()
        self.splitter.addWidget(self.splitterWidget)
        self.splitterLayout = QtWidgets.QVBoxLayout(self.splitterWidget)

        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.splitterLayout.addWidget(self.search)
        self.jointList = QtWidgets.QListWidget()
        self.jointList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.splitterLayout.addWidget(self.jointList)

        # populate joint list
        joints = self.findJoints()
        for joint in joints:
            self.jointList.addItem(joint)

        # search bar
        self.search.textChanged.connect(self.searchJoints)

        # add bottom layout for options/filters
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayoutFrame = QtWidgets.QFrame()
        self.bottomLayoutFrame.setMaximumHeight(70)
        self.bottomLayout.addWidget(self.bottomLayoutFrame)
        self.optionsLayout = QtWidgets.QHBoxLayout(self.bottomLayoutFrame)
        self.page4VerticalLayout.addLayout(self.bottomLayout)

        # add bottom options/smooth bind (max influences, maintain max, dropoff rate

        # MAX INFLUENCES
        self.maxInfluenceLayout = QtWidgets.QVBoxLayout()
        self.optionsLayout.addLayout(self.maxInfluenceLayout)

        label = QtWidgets.QLabel("Max Influences: ")
        label.setMaximumHeight(20)
        label.setStyleSheet("color: rgb(25,175,255); background:transparent;")
        self.maxInfluenceLayout.addWidget(label)

        self.maxInfOptionsLayout = QtWidgets.QHBoxLayout()
        self.maxInfluenceLayout.addLayout(self.maxInfOptionsLayout)

        self.maxInfluences = QtWidgets.QSlider()
        self.maxInfluences.setRange(1, 8)
        self.maxInfluences.setSingleStep(1)
        self.maxInfluences.setPageStep(1)
        self.maxInfluences.setOrientation(QtCore.Qt.Horizontal)
        self.maxInfOptionsLayout.addWidget(self.maxInfluences)

        self.maxInfluencesReadout = QtWidgets.QSpinBox()
        self.maxInfOptionsLayout.addWidget(self.maxInfluencesReadout)
        self.maxInfluencesReadout.setReadOnly(True)
        self.maxInfluencesReadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.maxInfluences.valueChanged.connect(self.maxInfluencesReadout.setValue)

        # DROPOFF RATE
        self.dropoffRateLayout = QtWidgets.QVBoxLayout()
        self.optionsLayout.addLayout(self.dropoffRateLayout)

        label2 = QtWidgets.QLabel("Dropoff Rate:")
        label2.setMaximumHeight(20)
        label2.setStyleSheet("color: rgb(25,175,255); background:transparent;")
        self.dropoffRateLayout.addWidget(label2)

        self.dropRateOptionsLayout = QtWidgets.QHBoxLayout()
        self.dropoffRateLayout.addLayout(self.dropRateOptionsLayout)

        self.dropoffRate = QtWidgets.QSlider()
        self.dropoffRate.setRange(.1, 100)
        self.dropoffRate.setSingleStep(.1)
        self.dropoffRate.setPageStep(1)
        self.dropoffRate.setOrientation(QtCore.Qt.Horizontal)
        self.dropRateOptionsLayout.addWidget(self.dropoffRate)

        self.dropoffReadout = QtWidgets.QSpinBox()
        self.dropRateOptionsLayout.addWidget(self.dropoffReadout)
        self.dropoffReadout.setReadOnly(True)
        self.dropoffReadout.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dropoffRate.valueChanged.connect(self.dropoffReadout.setValue)

        # MAINTAIN MAX
        self.maintainMaxInf = QtWidgets.QPushButton("Maintain Max Influences")
        self.optionsLayout.addWidget(self.maintainMaxInf)
        self.maintainMaxInf.setMinimumWidth(160)
        self.maintainMaxInf.setCheckable(True)
        self.maintainMaxInf.setChecked(True)
        self.maintainMaxInf.clicked.connect(partial(self.toggleButtonState, self.maintainMaxInf))
        self.maintainMaxInf.setObjectName("settings")
        self.maintainMaxInf.setMinimumHeight(60)
        self.maintainMaxInf.setMaximumHeight(60)

        # button layout
        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.optionsLayout.addLayout(self.buttonLayout)

        # SMOOTH BIND
        self.smoothBind = QtWidgets.QPushButton("Smooth Bind")
        self.smoothBind.setMinimumWidth(150)
        self.smoothBind.setMinimumHeight(30)
        self.buttonLayout.addWidget(self.smoothBind)
        self.smoothBind.clicked.connect(self.smoothBindSelected)
        self.smoothBind.setObjectName("settings")
        self.smoothBind.setMinimumHeight(30)
        self.smoothBind.setMaximumHeight(30)

        # CLOSE
        self.closeBtn = QtWidgets.QPushButton("Close")
        self.closeBtn.setMinimumWidth(150)
        self.closeBtn.setMinimumHeight(30)
        self.buttonLayout.addWidget(self.closeBtn)
        self.closeBtn.clicked.connect(self.closeWizard)
        self.closeBtn.setObjectName("settings")
        self.closeBtn.setMinimumHeight(30)
        self.closeBtn.setMaximumHeight(30)

        # set values
        self.dropoffRate.setValue(4)
        self.maxInfluences.setValue(4)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # PAGE  FIVE: SKIN WEIGHTS FOUND
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        self.page5 = QtWidgets.QFrame()
        self.page5.setObjectName("dark")
        self.stackWidget.addWidget(self.page5)
        self.page5MainLayout = QtWidgets.QVBoxLayout(self.page5)

        # label
        pageFiveLabel = QtWidgets.QLabel("Skin Weights Found For These Meshes:")
        self.page5MainLayout.addWidget(pageFiveLabel)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        pageFiveLabel.setFont(font)

        # columnLayout
        self.page5ColumnLayout = QtWidgets.QHBoxLayout()
        self.page5MainLayout.addLayout(self.page5ColumnLayout)

        # left column has list widget of meshes
        self.page5MeshList = QtWidgets.QListWidget()
        self.page5ColumnLayout.addWidget(self.page5MeshList)
        self.page5MeshList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.page5MeshList.setMinimumWidth(250)
        self.page5MeshList.setMaximumWidth(250)

        # right column has import method, and import/do not import buttons
        self.page5VerticalLayout = QtWidgets.QVBoxLayout()
        self.page5ColumnLayout.addLayout(self.page5VerticalLayout)

        layout = QtWidgets.QHBoxLayout()
        self.page5VerticalLayout.addLayout(layout)

        label = QtWidgets.QLabel("Import Method: ")
        label.setStyleSheet("background: transparent;")
        layout.addWidget(label)
        layout.setSpacing(10)
        label.setMinimumWidth(130)
        label.setMaximumWidth(130)

        self.page5ImportOptions = QtWidgets.QComboBox()
        self.page5ImportOptions.addItem("Vertex Order")
        self.page5ImportOptions.addItem("World Position")
        self.page5ImportOptions.addItem("Local Position")
        self.page5ImportOptions.addItem("UV Position")
        layout.addWidget(self.page5ImportOptions)
        self.page5ImportOptions.setMinimumWidth(155)
        self.page5ImportOptions.setMaximumWidth(155)

        self.page5VerticalLayout.addSpacerItem(
            QtWidgets.QSpacerItem(0, 200, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed))

        self.page5ImportWeights = QtWidgets.QPushButton("Import Weights")
        self.page5ImportWeights.setMinimumHeight(50)
        self.page5ImportWeights.setFont(font)
        self.page5VerticalLayout.addWidget(self.page5ImportWeights)
        self.page5ImportWeights.clicked.connect(partial(self.importWeights))
        self.page5ImportWeights.setObjectName("blueButton")

        self.page5IgnoreWeights = QtWidgets.QPushButton("Skip")
        self.page5IgnoreWeights.setMinimumHeight(50)
        self.page5IgnoreWeights.setFont(font)
        self.page5VerticalLayout.addWidget(self.page5IgnoreWeights)
        self.page5IgnoreWeights.clicked.connect(partial(self.skipWeightImport))
        self.page5IgnoreWeights.setObjectName("blueButton")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def checkForCustomMeshes(self, has_proxy_geo=False):

        if not has_proxy_geo:
            if cmds.objExists("proxy_geo_layer"):
                cmds.delete("proxy_geo_layer")
        # check for custom geometry
        skinnableGeo = self.findCustomGeo()
        meshes = list(skinnableGeo)

        if len(skinnableGeo) > 0:

            matches = []

            # check to see if weight files exist for this geo on disk
            for i in range(len(meshes)):
                filePath = utils.returnFriendlyPath(os.path.join(cmds.internalVar(utd=True), meshes[i] + ".WEIGHTS"))
                if os.path.exists(filePath):
                    matches.append(meshes[i])

            if len(matches) > 0:
                for match in matches:
                    listWidgetItem = QtWidgets.QListWidgetItem(match)
                    self.page5MeshList.addItem(listWidgetItem)
                    listWidgetItem.setSelected(True)

                # go to page 5
                self.stackWidget.setCurrentIndex(4)

            else:
                # go to page 3
                self.stackWidget.setCurrentIndex(2)

        else:
            # go to page 2
            self.stackWidget.setCurrentIndex(1)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def selectGeo(self):

        selected = self.geoList.selectedItems()
        selected = selected[0].text()

        cmds.select(selected, r=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def searchJoints(self):

        # get current search terms
        searchKey = self.search.text()

        # get all items in the joint list
        allItems = []
        for i in range(self.jointList.count()):
            item = self.jointList.item(i)
            itemName = item.text()
            allItems.append([item, itemName])

        # hide all items in list
        for item in allItems:
            item[0].setHidden(True)

        # find items in list with search key and show item
        if searchKey.find("*") == 0:
            matchedItems = self.jointList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchWildcard)
            for item in matchedItems:
                item.setHidden(False)

        else:
            matchedItems = self.jointList.findItems(searchKey, QtCore.Qt.MatchFlag.MatchContains)
            for item in matchedItems:
                item.setHidden(False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skinProxyGeo(self):

        # get modules in scene and call the skinProxyGeo function
        for module in self.rigUiInst.moduleInstances:
            try:
                module.skinProxyGeo()
            except RuntimeError, e:
                cmds.warning("Error skinning proxy geometry for " + module.name + ". " + str(e))

        if cmds.objExists("skinned_proxy_geo"):
            if not cmds.objExists("proxy_geo_layer"):
                cmds.createDisplayLayer(name="proxy_geo_layer")
            cmds.select("skinned_proxy_geo", hi=True)
            selection = cmds.ls(sl=True)
            cmds.editDisplayLayerMembers("proxy_geo_layer", selection)
            cmds.setAttr("proxy_geo_layer.displayType", 2)

            cmds.select(clear=True)

        self.checkForCustomMeshes(True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addCustomMeshes(self):

        try:
            files = cmds.fileDialog2(fm=4, okc="Add Selected Meshes")

            if len(files) > 0:
                for f in files:
                    try:
                        cmds.file(f, i=True, dns=True)
                    except:
                        cmds.warning("Could not import file: " + str(f))

                # add new meshes to list
                skinnableGeo = self.findCustomGeo()
                for geo in skinnableGeo:
                    self.geoList.addItem(geo)

                # next page
                self.stackWidget.setCurrentIndex(2)

        except:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skinTools(self):
        self.stackWidget.setCurrentIndex(3)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeWizard(self):

        mayaWindow = getMainWindow()
        mayaWindow = mayaWindow.objectName()
        if cmds.window(mayaWindow + "|pyArtWeightWizardWin", q=True, exists=True):
            cmds.deleteUI(mayaWindow + "|pyArtWeightWizardWin")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findCustomGeo(self):
        meshes = cmds.ls(type="mesh")
        skinnableGeo = []

        for mesh in meshes:
            parent = cmds.listRelatives(mesh, parent=True, type="transform")[0]
            if parent != None:
                if parent.find("proxy_geo") == -1:
                    if parent.find("lra") == -1:
                        if parent.find("bone_geo") == -1:
                            skinnableGeo.append(parent)
        skinnableGeo = set(skinnableGeo)
        return skinnableGeo

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def findJoints(self):
        if cmds.objExists("root"):
            cmds.select("root", hi=True)
            selection = cmds.ls(sl=True)
            joints = []

            for each in selection:
                if cmds.nodeType(each) == "joint":
                    joints.append(each)

            return joints

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def smoothBindSelected(self):

        # get selected geo from list
        selectedGeo = self.geoList.selectedItems()[0]
        geoRow = self.geoList.row(selectedGeo)
        geo = selectedGeo.text()

        # selected joints
        selectedJoints = self.jointList.selectedItems()
        joints = []
        for joint in selectedJoints:
            joints.append(joint.text())

        # get smooth skin settings
        maxInf = self.maxInfluences.value()
        dropoff = self.dropoffRate.value()
        maintainMax = self.maintainMaxInf.isChecked()

        # smooth bind
        cmds.select(clear=True)
        for joint in joints:
            cmds.select(joint, add=True)
        cmds.select(geo, add=True)

        skinCluster = \
        cmds.skinCluster(tsb=True, maximumInfluences=maxInf, obeyMaxInfluences=maintainMax, dropoffRate=dropoff,
                         bindMethod=0, skinMethod=0, normalizeWeights=1, name=geo + "_skinCluster")[0]

        # clear selection and remove geo from list
        cmds.select(clear=True)
        self.geoList.takeItem(geoRow)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importWeights(self):

        # get the selected items in the mesh list
        selected = self.page5MeshList.selectedItems()

        # get the import method
        method = self.page5ImportOptions.currentText()

        meshes = []
        for each in selected:
            meshes.append(each.text())

        for mesh in meshes:
            filePath = utils.returnFriendlyPath(os.path.join(cmds.internalVar(utd=True), mesh + ".WEIGHTS"))
            if os.path.exists(filePath):
                riggingUtils.import_skin_weights(filePath, mesh, True)

        self.closeWizard()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def skipWeightImport(self):
        # go to page 3
        self.stackWidget.setCurrentIndex(2)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def toggleButtonState(self, button):

        # button background image
        buttonImageOn = os.path.normcase(os.path.join(self.iconsPath, "System/button_background_hover.png"))
        if buttonImageOn.partition("\\")[2] != "":
            buttonImageOn = buttonImageOn.replace("\\", "/")

        buttonImageOff = os.path.normcase(os.path.join(self.iconsPath, "System/button_background_disabled.png"))
        if buttonImageOff.partition("\\")[2] != "":
            buttonImageOff = buttonImageOff.replace("\\", "/")

        state = button.isChecked()
        if state:
            button.setStyleSheet("background-image: url(" + buttonImageOn + "); background-color: rgb(25,175,255)")

        else:
            button.setStyleSheet("background-image: url(" + buttonImageOff + "); background-color: rgb(0,0,0)")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def closeWizard(self):
        mayaWindow = getMainWindow()
        mayaWindow = mayaWindow.objectName()
        if cmds.window(mayaWindow + "|pyArtWeightWizardWin", q=True, exists=True):
            cmds.deleteUI(mayaWindow + "|pyArtWeightWizardWin")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run(rigUiInst):
    mayaWindow = getMainWindow()
    mayaWindow = mayaWindow.objectName()
    if cmds.window(mayaWindow + "|pyArtWeightWizardWin", q=True, exists=True):
        cmds.deleteUI(mayaWindow + "|pyArtWeightWizardWin")

    gui = WeightWizard(rigUiInst, getMainWindow())
    gui.show()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def runOnlySkinTools(rigUiInst):
    mayaWindow = getMainWindow()
    mayaWindow = mayaWindow.objectName()
    if cmds.window(mayaWindow + "|pyArtWeightWizardWin", q=True, exists=True):
        cmds.deleteUI(mayaWindow + "|pyArtWeightWizardWin")

    gui = WeightWizard(rigUiInst, getMainWindow())
    gui.show()

    gui.stackWidget.setCurrentIndex(3)
