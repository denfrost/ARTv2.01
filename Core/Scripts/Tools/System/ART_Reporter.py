from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import maya.cmds as cmds
import Utilities.interfaceUtils as interfaceUtils
import Utilities.git_utils as git

windowTitle = "ARTv2: Report an Issue"
windowObject = "pyArtReporterWin"


class ART_Reporter(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(ART_Reporter, self).__init__(parent)

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")
        self.scriptPath = settings.value("scriptPath")
        self.projPath = settings.value("projectPath")

        # build the UI
        self.buildSettingsUi()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildSettingsUi(self):

        # fonts
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        self.font.setBold(False)

        self.fontSmall = QtGui.QFont()
        self.fontSmall.setPointSize(9)
        self.fontSmall.setBold(False)

        self.titleFont = QtGui.QFont()
        self.titleFont.setPointSize(40)
        self.titleFont.setBold(True)

        # load stylesheet
        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setStyleSheet(self.style)
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.resize(300, 600)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(300, 600))
        self.setMaximumSize(QtCore.QSize(300, 600))

        # create the QFrame
        self.frame = QtWidgets.QFrame()
        self.layout.addWidget(self.frame)
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        # Title of Issue
        self.titleLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.addLayout(self.titleLayout)

        titleLabel = QtWidgets.QLabel("Title: ")
        self.titleLayout.addWidget(titleLabel)

        self.issueTitle = QtWidgets.QLineEdit()
        self.issueTitle.setPlaceholderText("Title of Issue")
        self.titleLayout.addWidget(self.issueTitle)
        self.issueTitle.setMinimumWidth(200)
        self.issueTitle.setMaximumWidth(200)

        # Type of Issue (from labels)
        self.labelLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.addLayout(self.labelLayout)

        typeLabel = QtWidgets.QLabel("Issue Type: ")
        self.labelLayout.addWidget(typeLabel)

        self.issueType = QtWidgets.QComboBox()
        self.labelLayout.addWidget(self.issueType)
        self.issueType.setMinimumWidth(200)
        self.issueType.setMaximumWidth(200)

        # Information
        summaryLabel = QtWidgets.QLabel("Summary: ")
        self.widgetLayout.addWidget(summaryLabel)

        infoText = QtWidgets.QTextEdit()
        infoText.setReadOnly(True)
        infoText.setEnabled(False)
        self.widgetLayout.addWidget(infoText)
        infoText.setMinimumHeight(60)
        infoText.setMaximumHeight(60)
        infoText.setTextColor(QtGui.QColor(120, 120, 120))
        infoText.append(
            "(Please include any errors and stacktrace if applicable. Also include any reproduction steps if possible.)")

        self.issueInfo = QtWidgets.QTextEdit()
        self.widgetLayout.addWidget(self.issueInfo)

        # Create Issue
        self.createIssueBtn = QtWidgets.QPushButton("Create Issue")
        self.createIssueBtn.setObjectName("settings")
        self.widgetLayout.addWidget(self.createIssueBtn)
        self.createIssueBtn.clicked.connect(self.createIssue)

        self.credentials = git.getGitCreds()
        if self.credentials == None:
            git.gitCredsUI(self)
            self.credentials = git.getGitCreds()

        self.getLabels()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def getLabels(self):

        labels = self.githubInfo("label")
        ignoreLabel = ["wontfix", "duplicate", "invalid"]
        if labels != None:
            for label in labels:
                if label.name not in ignoreLabel:
                    self.issueType.addItem(label.name)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createIssue(self):

        title = self.issueTitle.text()
        issueType = self.issueType.currentText()

        body = "User: " + str(self.credentials[0]) + "\n"
        body += "Maya Version: " + str(cmds.about(iv=True)) + "\n"
        body += "OS: " + str(cmds.about(os=True)) + "\n" + "\n"
        body += self.issueInfo.toPlainText()

        repo = self.githubInfo("repo")
        issueCreated = False
        try:
            issue = repo.create_issue(title, body)
            issue.set_labels(issueType)
            issueCreated = True

        except Exception, e:
            cmds.warning("unable to create issue. Error: " + str(e))
            self.close()
            return

        if issueCreated:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Your issue has been created")
            msgBox.setDetailedText("To view your issue, please visit:\nhttps://github.com/epicernst/Test/issues")
            ret = msgBox.exec_()
            self.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def githubInfo(self, type):

        # github section
        # try:
        from ThirdParty.github import Github
        # except:
        #     cmds.warning("unable to import github module. You will not be able to create an issue")
        #     self.close()
        #     return

        repoOwner = "epicernst"
        try:
            g = Github(self.credentials[0], self.credentials[1])
            repo = g.get_user(repoOwner).get_repo("Test")
            labels = repo.get_labels()

            if type == "repo":
                return repo
            if type == "label":
                return labels
        except:
            return None
            pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    if cmds.window("pyArtReporterWin", exists=True):
        cmds.deleteUI("pyArtReporterWin", wnd=True)

    gui = ART_Reporter(interfaceUtils.getMainWindow())
    gui.show()
