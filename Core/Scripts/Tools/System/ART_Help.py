from ThirdParty.Qt import QtGui, QtCore, QtWidgets
from functools import partial
import maya.cmds as cmds
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils


# Original Author: Jeremy Ernst


class ART_HelpMovie():
    def __init__(self, mainUI, moviePath):
        # Original Author: Jeremy Ernst

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.projectPath = settings.value("projectPath")
        self.iconsPath = settings.value("iconPath")
        self.mainUI = mainUI

        # build the UI
        if cmds.window("ART_HelpMovieWin", exists=True):
            cmds.deleteUI("ART_HelpMovieWin", wnd=True)

        self.buildHelpMovieUI(moviePath)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildHelpMovieUI(self, moviePath):
        # Original Author: Jeremy Ernst

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(self.mainUI)
        self.mainWin.setMinimumSize(660, 520)
        self.mainWin.setMaximumSize(660, 520)

        # images
        self.playImage = self.mainWin.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        self.pauseImage = self.mainWin.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
        self.backImage = self.mainWin.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipBackward)
        self.forwardImage = self.mainWin.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipForward)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # load the stylesheet
        self.styleSheet = interfaceUtils.get_style_sheet("artv2_style")

        # create the qFrame so we can have a background
        self.frame = QtWidgets.QFrame(self.mainWidget)
        self.frame.setMinimumSize(660, 520)
        self.frame.setMaximumSize(660, 520)
        self.frame.setObjectName("dark")

        # set qt object name
        self.mainWin.setObjectName("ART_HelpMovieWin")
        self.mainWin.setWindowTitle("Help")

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(10)
        headerFont.setBold(True)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.frame)

        # set up the screen
        self.movie_screen = QtWidgets.QLabel()
        self.movie_screen.setStyleSheet("background: transparent;")
        dropShadow = QtWidgets.QGraphicsDropShadowEffect(self.mainWin)
        dropShadow.setColor(QtGui.QColor(0, 0, 0))
        dropShadow.setOffset(10)
        self.movie_screen.setGraphicsEffect(dropShadow)

        # expand and center the label 
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.movie_screen)

        # buttons and button layout
        self.buttonlayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.buttonlayout)

        spacer = QtWidgets.QSpacerItem(60, 0)
        self.buttonlayout.addSpacerItem(spacer)

        self.backBtn = QtWidgets.QPushButton()
        self.buttonlayout.addWidget(self.backBtn)
        self.backBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.backBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.backBtn.setFont(headerFont)
        self.backBtn.setObjectName("orange")
        self.backBtn.setIcon(self.backImage)

        self.pauseBtn = QtWidgets.QPushButton()
        self.buttonlayout.addWidget(self.pauseBtn)
        self.pauseBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.pauseBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.pauseBtn.setFont(headerFont)
        self.pauseBtn.setObjectName("orange")
        self.pauseBtn.setIcon(self.pauseImage)

        self.forwardBtn = QtWidgets.QPushButton()
        self.buttonlayout.addWidget(self.forwardBtn)
        self.forwardBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.forwardBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.forwardBtn.setFont(headerFont)
        self.forwardBtn.setObjectName("orange")
        self.forwardBtn.setIcon(self.forwardImage)

        self.playBtn = QtWidgets.QPushButton("Close")
        self.buttonlayout.addWidget(self.playBtn)
        self.playBtn.clicked.connect(partial(self.close))
        self.playBtn.setMinimumHeight(40)
        self.playBtn.setMaximumHeight(40)
        self.playBtn.setFont(headerFont)
        self.playBtn.setObjectName("settings")

        spacer = QtWidgets.QSpacerItem(60, 0)
        self.buttonlayout.addSpacerItem(spacer)

        # set movie from file path
        self.movie = QtGui.QMovie(moviePath, QtCore.QByteArray())
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)

        self.movie.start()
        self.pauseBtn.clicked.connect(self.pause)
        self.forwardBtn.clicked.connect(self.forward)
        self.backBtn.clicked.connect(self.back)

        # show
        self.mainWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def close(self):
        # Original Author: Jeremy Ernst

        if cmds.window("ART_HelpMovieWin", exists=True):
            cmds.deleteUI("ART_HelpMovieWin", wnd=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def pause(self):

        state = self.movie.state()
        if state == QtGui.QMovie.MovieState.Running:
            self.movie.setPaused(True)
            self.pauseBtn.setIcon(self.playImage)
        if state == QtGui.QMovie.MovieState.Paused:
            self.movie.setPaused(False)
            self.pauseBtn.setIcon(self.pauseImage)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def forward(self):
        currentFrame = self.movie.currentFrameNumber()
        self.movie.jumpToFrame(currentFrame + 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def back(self):

        currentFrame = self.movie.currentFrameNumber()
        self.movie.jumpToFrame(currentFrame - 1)
